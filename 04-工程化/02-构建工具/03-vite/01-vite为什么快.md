# vite 为什么快

> vite 开发态快的本质是把「编译时机」从启动时推迟到请求时，代价是首屏模块请求数随项目深度增长。

同一个项目，webpack 冷启动 32 秒、改一行等 2 秒；换成 vite 启动 800 毫秒，改一行几乎瞬时。但本地首屏白屏 2 秒，Network 面板里滚了 200 多个 JS 请求。这两件事是同一个设计的正反面。

## 一、开发态不打包

```text
webpack dev server   entry → 递归解析全部依赖 → 内存里生成 bundle → 浏览器加载 1-3 个文件
vite dev server      浏览器请求 /src/main.tsx → 服务端即时编译这一个文件 → 返回 ESM

```

浏览器原生支持 `<script type="module">`，每个 `import` 就是一次 HTTP 请求。vite 不需要提前知道依赖图，只在请求到来时用 esbuild 把该文件转成可执行的 ESM（TS/JSX 转换、CSS 处理、路径重写）。**没被请求到的文件永远不会被编译**，启动时间与业务代码规模解耦。

| 维度 | webpack | vite dev |
|------|---------|----------|
| 启动 | 编译全量依赖图 | 只做依赖预构建 |
| 改文件 | 重建受影响 chunk | 只编译该文件，浏览器重取 |
| 页面入口 | 打包后的 bundle | 源码入口 + 原生 ESM |
| 规模增长 | 线性变慢 | 近似不变 |

## 二、裸模块问题与依赖预构建

浏览器不认识 `import vue from 'vue'`：它不会去 `node_modules` 找文件，也不处理 CJS 的 `module.exports`。**依赖预构建（pre-bundle）**解决两件事：

1. **格式转换**：把 CJS / UMD 依赖转成 ESM，`react` 会被包成带 `export default` 的形式。
2. **请求数收敛**：`lodash-es` 有 600 多个内部文件，逐个请求会产生请求瀑布，预构建合并成单文件。

```text
node_modules/.vite/deps/
├── _metadata.json   # 记录每个包的 hash 与来源，用于判断缓存有效性
├── vue.js
└── chunk-XXXX.js

```

### 什么情况会触发重新预构建

| 触发条件 | 说明 |
|----------|------|
| lockfile 变化 | lock 文件 hash 变了，说明依赖版本可能变 |
| `optimizeDeps` 变化 | `include` / `exclude` / `esbuildOptions` 改动 |
| 相关配置变化 | `define`、`resolve.alias`、插件返回的 config 影响解析结果 |
| mode / `NODE_ENV` 变化 | 不同 mode 的 `define` 不同，产物不能复用 |
| 运行时发现新依赖 | 动态拼接的路径首次没扫到，vite 补跑并触发页面 reload |
| 手动 `--force` | 强制清空 `cacheDir` 重跑 |

## 三、optimizeDeps.exclude / include

```ts
optimizeDeps: {
  exclude: ['@my/ui', 'some-esm-lib'],          // 链接的本地包、已是 ESM 且要 HMR 的包
  include: ['my-lib/dist/deep-entry', 'cjs-only-pkg'], // 扫描不到的深层 CJS 依赖
}

```

`exclude` 用于 monorepo 里 `file:` 或 workspace 链接的包：源码是 ESM 且需要热更新，被预构建后会退化成「重新预构建 + 整页 reload」，HMR 失效。`include` 用于静态扫描识别不了的深层入口，`import('my-lib/' + name)` 这种拼接写法首屏才暴露，触发一次全量预构建并刷新页面，体验很差。

## 四、请求瀑布与 modulepreload

原生 ESM 的 `import` 是**串行发现**的：浏览器解析 `main.tsx` 才知道要请求 `App.tsx`，解析完才知道要请求 `router.ts`。层级越深，串行 RTT 越多：

```text
main.tsx (1 RTT) → App.tsx (2 RTT) → router.ts (3 RTT) → ...

```

缓解手段是 `<link rel="modulepreload">`，让浏览器提前并行抓取静态依赖，生产构建会自动注入。但**开发态的请求瀑布无法根治**，它是模型的固有开销；项目层级极深（单页 500+ 模块）时，vite 首屏可能比 webpack 的 bundle 模式更慢。

## 五、生产构建为什么还用 Rollup

| 原因 | 说明 |
|------|------|
| Tree shaking 更彻底 | 基于 ESM 静态分析，能跨模块删导出，配合 scope hoisting 产物更紧凑 |
| 插件生态成熟 | 大量 Rollup 插件可直接复用，vite 插件本身就是其超集 |
| 代码分割可控 | `manualChunks`、`output.format` 适合多入口与库构建 |
| esbuild 打包能力弱 | tree shaking、CSS 拆分、chunk 策略都不够完善 |

分工是：**开发用 esbuild（单文件转换快），生产用 Rollup（产物质量优先）**。这也解释了「vite 启动快 ≠ 打包快」——大项目 `vite build` 可能比 `webpack build` 更慢。

## 六、HMR 为什么快

webpack 的 HMR 要沿依赖图**向上找 boundary**：从变化的模块出发逐层检查 `module.hot.accept`，找不到就整页刷新，链越长重构建的 chunk 越多。

vite 的 HMR 建立在浏览器已有的 ESM 模块图上：文件变更 → 沿 import 链找到最近的 accept 边界 → 只让浏览器重新请求「该模块 + 失效的 importer」，URL 带 `?t=时间戳` 破缓存。每个模块本来就是独立 URL，失效粒度天然是文件级，不需要重新打包。

| 维度 | webpack HMR | vite HMR |
|------|-------------|----------|
| 失效粒度 | chunk / 模块，需重算边界 | 单文件 URL |
| 重建成本 | 重建受影响 chunk | 只编译变更文件 |
| 传输内容 | 新 chunk | 单模块 ESM |

## 七、vite.config.ts 示例

```ts
export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@': path.resolve(__dirname, 'src') } },
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://127.0.0.1:8080', changeOrigin: true,
                rewrite: (p) => p.replace(/^\/api/, '') },
    },
  },
  build: {
    target: 'es2020',
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes('node_modules')) return;
          if (/[\\/](react|react-dom|scheduler)[\\/]/.test(id)) return 'react';
          if (id.includes('lodash')) return 'lodash';
          return 'vendor';
        },
      },
    },
  },
});

```

`manualChunks` 返回 `undefined` 表示交回默认策略。react 系列必须同组，因为 `react-dom` 依赖 `scheduler`，分开会产生跨 chunk 循环引用。

## 八、常见误区

1. **以为 vite 开发态完全不编译**。TS、JSX、CSS Modules、路径重写都要在请求时处理，只是按需而非全量。
2. **以为预构建缓存永远正确**。改了 `optimizeDeps` 或 lockfile 后没生效，先删 `node_modules/.vite` 或 `vite --force`。
3. **以为 vite 打包一定比 webpack 快**。生产走 Rollup，大项目里 Rollup 的 tree shaking 与 chunk 生成可能更慢。
4. **以为 exclude 越多越好**。把 CJS 包 exclude 出去，浏览器会拿到 `module.exports` 报 `does not provide an export named`。

## 面试怎么答

**Q：vite 为什么启动快？**
开发态不做全量打包，只对 `node_modules` 做一次依赖预构建（esbuild），业务代码零编译启动；浏览器请求某个文件时才即时转换。启动耗时与项目模块数解耦，只与依赖数量相关。

**Q：依赖预构建解决什么问题？**
把 CJS/UMD 转成 ESM；把零散内部模块（如 `lodash-es` 的数百个文件）合并成单文件减少请求。产物在 `node_modules/.vite/deps`，靠 lockfile hash、`optimizeDeps` 配置、mode 判断是否复用。

**Q：生产构建为什么不用 esbuild？**
esbuild 的单文件转换极快，但 tree shaking 精细度、CSS 代码分割、chunk 策略不如 Rollup。生产更看重产物质量与插件生态，所以用 Rollup，也说明「开发快」和「打包快」是两件事。

**Q：vite 的 HMR 为什么比 webpack 快？**
webpack 要从变更模块沿依赖图向上找 accept boundary，再重建受影响 chunk；vite 的模块本来就是独立 URL，失效粒度是文件级，只需重取变更文件与失效的 importer，省掉打包与边界计算。

## 关联阅读

- [vite 插件与生产构建](./02-vite插件与生产构建.md)：钩子体系、manualChunks、legacy 与 base 配置
- [构建工具原理与选型](../01-构建工具原理与选型.md)：两代构建模型的差异与选型判断
- [前端性能优化体系](../../06-性能优化/01-性能优化体系.md)：首屏指标与资源加载策略
