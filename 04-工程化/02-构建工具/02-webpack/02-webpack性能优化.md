# webpack 性能优化

> 构建优化的前提是分清「编译变快」与「产物变小」是两条独立的线，混着改只会把慢的部分藏起来。

冷启动 48 秒、改一个文件等 3 秒、CI 打包 6 分钟，分别卡在模块编译、增量构建与压缩阶段；产物 3 MB、首屏 4 秒则是另一维度。

## 一、两条线的边界

| 维度 | 优化对象 | 度量方式 | 手段 |
|------|----------|----------|------|
| 构建速度 | 命令执行到 `done` 的耗时 | `--profile`、`speed-measure-webpack-plugin` | 缓存、缩小范围、多线程、换编译器 |
| 产物体积 | `dist` 内 JS/CSS 字节数 | analyzer、`stats.toJson()` | splitChunks、tree shaking、按需、压缩 |

冲突点：多线程与缓存让编译更快，却让产物更难分析；激进拆包提高缓存命中率，却增加请求数。

## 二、构建速度：手段与代价

| 手段 | 收益 | 代价 | 适用 |
|------|------|------|------|
| filesystem cache | 二次启动只编译变更模块，常 5-10× | 首次不变、占磁盘 | 必开 |
| `include/exclude` | 跳过 `node_modules`，常 30%+ | 漏写导致新目录不编译 | 必开 |
| 精简 `resolve` | 减少无效 stat 与深层相对路径 | alias 过多路径难追 | 建议 |
| `thread-loader` | 昂贵 loader 并行 | 线程启动约 600 ms | 模块 > 500 |
| esbuild/swc loader | 比 babel 快 10-20× | babel 插件生态不可用 | 无自定义插件 |
| DLL | 依赖不重复编译 | 产物不可摇树 | 已淘汰 |

### 持久化缓存

```js
cache: { type: 'filesystem', buildDependencies: { config: [__filename] } },

```

与 `cache-loader` 的区别：后者只缓存单个 loader 的输出字符串，模块解析、依赖收集、chunk 生成全要重跑。filesystem cache 缓存 **module 级完整构建结果**，命中后连 AST 解析都省掉。

`buildDependencies.config` 必须配，否则改配置不生效，会出现「配置改了但行为没变」的假象。

### thread-loader 的边界

把 `thread-loader` 放在 `babel-loader` 之前，`workers` 取核数减一即可。它只在 loader 阶段并行，webpack 自身的模块图构建与 seal 仍是单线程。三种情况反而更慢：模块总数少、loader 本身很快（如 `css-loader`）、loader 依赖 compilation 上下文（如 `this.emitFile`）。

### DLL 为什么被淘汰

DLL 把不常变的依赖预打包成独立产物 + manifest，业务构建直接引用。代价是三份配置（`webpack.dll.config.js`、`DllPlugin`、`DllReferencePlugin`）、产物要额外分发、依赖升级要手动重打，且 DLL 包里的模块**无法参与 tree shaking 与细粒度拆包**。filesystem cache 用「模块级缓存 + 内容 hash 校验」达成同样的「依赖不重复编译」，还不需要额外产物，`hard-source-webpack-plugin` 同理被取代。

### 换掉 babel-loader 的风险

把 `module.rules` 里的 `babel-loader` 换成 `esbuild-loader`，`target` 交给 esbuild，收益是数量级的编译提速。风险在语义差异：`emitDecoratorMetadata`（NestJS/Angular）esbuild 不支持；`babel-plugin-import`、`styled-components` 的 babel 插件全部失效；`class` 字段语义可能与 tsc 默认值不同。判断标准是**项目里有没有必须在 AST 层改写代码的 babel 插件**。

## 三、产物体积：分包与摇树

### splitChunks 的默认策略

默认值里最要命的一条是 `chunks: 'async'`——**只对 `import()` 产生的 chunk 生效**，同步引入的 `node_modules` 全部留在入口 chunk。「配了 splitChunks 但 vendor 没拆出来」几乎都是这个原因。

```js
optimization: {
  splitChunks: {
    chunks: 'all',
    minSize: 20000,
    maxInitialRequests: 5,
    cacheGroups: {
      react: { test: /[\\/]node_modules[\\/](react|react-dom|scheduler)[\\/]/,
               name: 'react', priority: 30, chunks: 'all' },
      vendor: { test: /[\\/]node_modules[\\/]/, name: 'vendor',
                priority: 10, chunks: 'all', reuseExistingChunk: true },
      common: { minChunks: 2, priority: 5, chunks: 'all' },
    },
  },
  runtimeChunk: 'single',
}

```

`priority` 大的先匹配，`reuseExistingChunk` 避免同一模块复制进多个组。react 单独成组是因为它几乎不变，独立文件让 contenthash 长期稳定。

### runtimeChunk 为什么单独拆

runtime 里存着「模块 id → 文件」的映射表和 chunk 加载逻辑。业务代码增删模块，id 就变，映射表随之变化；runtime 混在 vendor 里，**每发一次版 vendor 的 contenthash 就全变**，浏览器缓存彻底失效。多入口用 `runtimeChunk: { name: (e) => \`runtime-${e.name}\` }`。

### Tree shaking 的三个前提

```js
// 1. 源码必须是 ESM；2. package.json 声明副作用；3. production + 标记 + 压缩
{ "sideEffects": ["*.css", "*.global.js"] }
optimization: { usedExports: true, sideEffects: true, providedExports: true, minimize: true }

```

`usedExports` 只做标记（代码旁加注释），删除由 Terser 完成；开了 production 但没开 minimize 时体积不会下降。

### minimizer 与 drop_console

```js
optimization: { minimizer: [new TerserPlugin({
  parallel: true,
  terserOptions: {
    compress: { drop_console: true, pure_funcs: ['console.log', 'console.info'] },
    format: { comments: false },
  },
  extractComments: false,
})] }

```

`drop_console` 会把 `console.error` 一并删掉，线上排障能力归零。多数团队该用 `pure_funcs` 精确指定。

### 按需引入与 babel-plugin-import

antd v4 及更早版本会把整包样式带进来，靠 `babel-plugin-import` 在编译期改写成 `antd/es/button`；v5 改为 ESM + CSS-in-JS，本身可摇树，不再需要它。lodash 同理：`import _ from 'lodash'` 是 CJS 全量，换 `lodash-es` 具名导入才真能摇掉。

## 四、排查顺序

```bash
npx webpack-bundle-analyzer dist/stats.json   # 1. 先看构成
npm ls lodash react                           # 2. 找重复版本
node -e "const s=require('./dist/stats.json'); \
 s.modules.sort((a,b)=>b.size-a.size).slice(0,10) \
 .forEach(m=>console.log(m.size, m.name));"    # 3. 按体积排模块

```

顺序是：可视化看构成 → `npm ls` 找重复版本 → `stats.toJson().modules` 排序定位 → 才动配置。

## 五、常见误区

1. **以为 `splitChunks` 配了就一定拆出 vendor**。默认 `chunks: 'async'`，同步依赖不参与；还要够 `minSize`，小包会被合并回入口。
2. **以为 `thread-loader` 线程越多越快**。超过物理核数会频繁切换，每个 worker 独立内存，大项目容易 OOM。
3. **以为 `drop_console` 无害**。它连 `console.error` 一起删，线上日志全丢；`const c = console; c.log()` 也处理不了。

## 面试怎么答

**Q：二次构建为什么快？**
filesystem cache 把每个 module 的构建结果（代码、依赖、hash）序列化到磁盘。二次启动按 snapshot 校验 mtime 与内容 hash，命中的模块直接复用，跳过 loader 与 AST 解析；`buildDependencies` 里的配置、loader 也参与校验，任一变化则整体失效。

**Q：splitChunks 怎么配才有效？**
`chunks: 'all'` 让同步依赖参与；`cacheGroups` 按优先级分组，把 react 这类长期不变的依赖单独成组；`minSize` 控制「小到不值得单独请求」的下限；`maxInitialRequests` 限制首屏并行数。配合 `runtimeChunk: 'single'`，否则 runtime 变化会让 vendor 的 hash 全失效。

**Q：为什么不再用 DLL？**
DLL 解决的是「依赖不重复编译」，代价是独立配置、额外 manifest、产物不可摇树、升级要手动重打。filesystem cache 达成同样目标且无需额外产物——它解决的是编译期问题，不是产物体积问题。

## 关联阅读

- [webpack 核心概念与构建流程](./01-webpack核心概念与构建流程.md)：chunk、module、asset 的区别与 stats 读法
- [构建工具原理与选型](../01-构建工具原理与选型.md)：Tree shaking 前提与体积排查总览
- [大体积媒体优化](../../06-性能优化/02-大体积媒体优化.md)：JS 之外的图片、字体、视频治理
