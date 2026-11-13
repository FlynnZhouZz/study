# vite 插件与生产构建

> vite 的插件体系是 Rollup 钩子的超集，理解钩子顺序与生效范围，才能让插件只在构建期、按正确时机介入。

本地 `vite dev` 里 `console.log` 正常，`vite build` 后产物还留着几十处调试日志；或配完 `manualChunks` 后报警告 `Generated an empty chunk: "vendor"`。答案都在钩子与 Rollup 输出配置里。

## 一、Vite 插件与 Rollup 插件的关系

Vite 插件对象是「Rollup 插件 + Vite 特有钩子 + 两个元字段」。

| 类别 | 钩子 |
|------|------|
| Rollup 构建 | `options`、`buildStart`、`resolveId`、`load`、`transform`、`buildEnd` |
| Rollup 输出 | `renderChunk`、`generateBundle`、`writeBundle`、`closeBundle` |
| Vite 特有 | `config`、`configResolved`、`configureServer`、`transformIndexHtml` |
| 元字段 | `enforce`、`apply` |

Rollup 插件基本能直接用，依赖 `this.parse`、`emitFile` 等上下文的插件偶尔要限定在 build 阶段。

## 二、钩子执行顺序

```text
config → configResolved → configureServer(仅 dev) → options → buildStart
→ resolveId → load → transform → moduleParsed → buildEnd
→ outputOptions → renderChunk → generateBundle → writeBundle → closeBundle

```

同一钩子内的顺序由 `enforce` 决定：

```text
alias → enforce:'pre' 的用户插件 → vite 核心插件 → 普通用户插件 → vite build 插件 → enforce:'post'

```

`apply` 限定环境：`apply: 'serve'` 只在 dev server 生效，`apply: 'build'` 只在打包生效，也可传函数按 `command` 判断。

## 三、生产构建去掉 console.log

```ts
export default (): Plugin => ({
  name: 'strip-console',
  apply: 'build',        // 开发态保留，保证本地能调试
  enforce: 'post',       // 在 TS/JSX 转换之后，语法已降级
  transform(code, id) {
    if (!/\.[jt]sx?$/.test(id)) return;
    const out = code.replace(/^[ \t]*console\.\w+\([^;\n]*\);?[ \t]*$/gm, '');
    return out === code ? undefined : { code: out, map: null };
  },
});

```

`map: null` 会让该模块 sourcemap 断掉，线上定位失真；要保留就接 `magic-string` 生成 map。

### 为什么不用 define

写成 `define: { 'console.log': '(() => {})' }` 有三个问题：

| 问题 | 说明 |
|------|------|
| 参数仍求值 | `console.log(expensive())` 变成 `(() => {})(expensive())`，副作用一个不少 |
| 删不掉语句 | 只把调用变空函数，字节还在，gzip 后仍有体积 |
| 无作用域分析 | 按标识符匹配，`const log = console.log` 会被误改 |

更直接的做法是让 esbuild 在压缩阶段 drop，它会语法级删除整条语句；自定义 `transform` 只在需要按路径过滤时才有价值：

```ts
esbuild: { drop: ['console', 'debugger'] },
// 或 terser，能精细保留 error
build: { minify: 'terser', terserOptions: { compress: { pure_funcs: ['console.log'] } } }

```

## 四、manualChunks 分包策略

```ts
build: {
  rollupOptions: {
    output: {
      manualChunks(id) {
        if (!id.includes('node_modules')) return;
        if (/[\\/](react|react-dom|scheduler)[\\/]/.test(id)) return 'react';
        if (id.includes('/echarts/')) return 'echarts';   // 大且低频
        return 'vendor';
      },
    },
  },
}

```

| 策略 | 做法 | 适用 |
|------|------|------|
| 全量 vendor | `node_modules` 统一进 `vendor` | 依赖不多、求缓存稳定 |
| 按库拆 | 大库单独成 chunk | 大库只在部分路由用 |
| 按路由拆 | 结合 `import()` 自动按入口拆 | 多页/多路由应用 |

**空 chunk 的成因**：某模块被指派到某个 chunk，但它同时被动态入口单独引用，Rollup 会把它提升为独立 chunk，原 chunk 变空。另一种是分组之间形成循环依赖，Rollup 只能保守处理。

判断标准：**同一份依赖闭包放进同一个 chunk**，react/react-dom/scheduler 同组。

## 五、build.target 与 legacy

```ts
build: { target: 'es2020' }   // 默认 'modules'，约 chrome87 / safari14 / firefox78

```

`target` 决定 esbuild 降级到哪一档，直接影响体积：降到 `es2015` 会让 async/await 变成 `__awaiter` 辅助代码，体积明显上升。需要兼容 iOS 12、旧 Android WebView 时加 legacy 插件，配置 `legacy({ targets: ['iOS >= 12'] })`。代价是**双份产物**：现代浏览器走 `<script type="module">`，老浏览器走 `nomodule` 加载 SystemJS 格式的 legacy chunk 与 core-js polyfill，构建时间与 `dist` 体积接近翻倍。

现代浏览器占比 99% 以上时，`target: 'es2020'` 加服务端兜底提示，比背一份 legacy 产物更划算。

## 六、环境变量与优先级

```bash
# .env                   VITE_APP_TITLE=学习笔记
# .env.production        VITE_API_BASE=https://api.example.com

```

`.env` 里只有 `VITE_` 前缀的变量会注入客户端，`import.meta.env` 还内置 `MODE`、`BASE_URL`。加载优先级（后者覆盖前者）：`.env` < `.env.local` < `.env.[mode]` < `.env.[mode].local`，**系统环境变量优先级最高**，CI 可 `VITE_API_BASE=xxx vite build` 覆盖。

`envPrefix` 可改前缀，别设成 `''`，否则 `AWS_SECRET_KEY` 这类变量会全打进产物。`import.meta.env` 是构建期静态替换，`import.meta.env[k]` 这种动态取值拿不到。

## 七、base 与子路径部署

`base: '/console/'` 表示部署在 `example.com/console/`，它影响三处：产物中静态资源的引用前缀、`import.meta.env.BASE_URL`、dev server 的路径前缀。漏配的典型症状是白屏——`index.html` 引用 `/assets/index.js`，文件实际在 `/console/assets/`。

配套要改路由的 `base`（`createWebHistory('/console/')`），以及服务端把 `/console/*` 的 404 回退到 `/console/index.html`。

## 八、SSR 构建的入口差异

普通构建入口是 `index.html`，SSR 的入口是导出渲染函数的模块：`build: { ssr: 'src/entry-server.ts' }`，模块导出 `render(url) => html`。`vite build` 跑两次，分别产出客户端资源（含 `ssr-manifest.json`）与服务端 bundle（Node 环境，外部化 `node_modules`），运行时由 Node 调 `render()` 得 HTML，再按 manifest 注入 `modulepreload`。

## 九、常见误区

1. **以为 `transform` 一定在所有插件之后跑**。它按插件顺序执行，`enforce: 'pre'` 的插件会先于 TS 转换拿到源码，看到的是未降级的 TS/JSX。
2. **以为 `apply: 'build'` 在 `vite build --watch` 下不生效**。`--watch` 仍是 build command，插件会反复执行；有状态的缓存要在 `buildStart` 里初始化。

## 面试怎么答

**Q：Vite 插件和 Rollup 插件什么关系？**
Vite 插件是 Rollup 插件的超集：`resolveId`/`load`/`transform`/`generateBundle` 语义一致，可直接复用生态；额外提供 `config`、`configureServer`、`transformIndexHtml` 这类钩子。`enforce` 控制同阶段顺序，`apply` 控制生效环境。

**Q：怎么在生产构建里去掉 console？**
优先用 `esbuild: { drop: ['console'] }` 或 terser 的 `pure_funcs`，语法级删除整条语句且能减小体积。`define` 换成空函数行不通：参数仍求值、字节还在、没有作用域分析。需要按路径过滤时才写自定义 `transform`，并设 `apply: 'build'`。

**Q：manualChunks 为什么会生成空 chunk？**
某模块被指派进某 chunk，但它同时是动态入口的依赖，Rollup 把它提升成独立 chunk，原分组变空；分组间形成循环依赖也有同样问题。解法是把同一依赖闭包放一组。

**Q：target 和 legacy 怎么选？**
`build.target` 只是语法降级档位，不注入 polyfill；`plugin-legacy` 才是给老浏览器的双份产物（SystemJS + core-js）。现代浏览器占比极高时只用 `target: 'es2020'`，覆盖 iOS 12 才引入 legacy。

## 关联阅读

- [vite 为什么快](./01-vite为什么快.md)：依赖预构建、请求瀑布与 HMR 边界
- [构建工具原理与选型](../01-构建工具原理与选型.md)：vite 与 webpack 的模型差异
- [前端性能优化体系](../../06-性能优化/01-性能优化体系.md)：产物体积与首屏指标的关系
