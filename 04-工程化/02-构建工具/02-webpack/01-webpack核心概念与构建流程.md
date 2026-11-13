# webpack 核心概念与构建流程

> 分不清 module、chunk、bundle、asset 四层抽象，就无法解释为什么改一行业务代码会让 vendor 的 contenthash 整片失效。

线上 `main.[hash].js` 有 1.8 MB，analyzer 里一个方块占四分之三，`node_modules` 被整体塞进了初始 chunk。要定位是哪个 loader 或 resolve 规则，得先看清文件被加工成了哪几层对象。

## 一、六个配置项的职责

| 配置 | 职责 | 常见误用 |
|------|------|----------|
| `entry` | 依赖图起点，从此递归 | 多 entry 不配 `[name]`，产物互相覆盖 |
| `output` | 落盘路径与文件名模板 | `filename`、`chunkFilename` 混用，异步 chunk 变数字名 |
| `module.rules` | 某类文件交给哪些 loader | 只看 `test` 不看 `include`，把 `node_modules` 送进 babel |
| `resolve` | 说明符 → 真实路径的解析规则 | `extensions` 列十几个后缀，每次解析逐个 stat |
| `plugins` | 在生命周期钩子上做扩展 | 用 plugin 干 loader 的活 |
| `optimization` | 分包、tree shaking、压缩 | 只配 `splitChunks` 不配 `runtimeChunk` |

```js
entry: { app: './src/index.tsx' }, output: { filename: '[name].[contenthash:8].js', clean: true },
resolve: { extensions: ['.tsx', '.ts', '.js'] }, module: { rules: [{ test: /\.tsx?$/, use: 'ts-loader' }] },

```

resolve 找到文件 → rules 匹配出 loader → 转成 JS → acorn 解析 import → 递归。**loader 做单文件的形态转换，plugin 做整个构建过程的介入**，这是唯一可靠的区分标准。

## 二、loader 为什么从右往左

`use: ['style-loader', 'css-loader']` 里 `css-loader` 先跑，因为 loader 数组被编译成函数组合：

```js
const compose = (loaders) =>
  loaders.reduceRight((next, l) => (src) => l.call(ctx, next(src)), () => resource);

```

`reduceRight` 让数据从最右流出：`style-loader` 拿到的是 `css-loader` 输出的 JS，原始资源在最右，产物在最左。

| 阶段 | 方向 | 作用 |
|------|------|------|
| `pitch` | 左 → 右（style-loader 先） | 提前拦截，可跳过后续 loader |
| `normal` | 右 → 左（css-loader 先） | 真正转换源码 |

任一 loader 的 `pitch` 返回非 `undefined`，webpack 跳过剩余 loader 的 pitch 与 normal、也不再读文件，把返回值当作模块 source。`style-loader` 靠这个直接返回注入 `<style>` 的 JS，`css-loader` 不执行。

```js
module.exports.pitch = function () {
  if (fs.existsSync(this.resourcePath)) return; // undefined 才继续
  return 'export default null;';
};

```

## 三、plugin 与 Tapable

扩展点全部由 Tapable 提供：发布订阅 + 钩子类型约束返回值语义。

| Hook | 行为 | 用例 |
|------|------|------|
| `SyncHook` | 同步串行，忽略返回值 | `thisCompilation` |
| `SyncBailHook` | 任一 tap 返回非 undefined 即中断 | `optimizeChunks` |
| `AsyncSeriesHook` | 异步串行，等 callback / Promise | `emit`、`done`、`run` |

要做 IO 用 Async 系，链式改写用 `SyncWaterfallHook`，可中断用 Bail。

`Compiler` 进程级，`webpack(config)` 时创建，持有 options / hooks / watch；`Compilation` 每轮构建新建，持有 modules / chunks / assets。compiler 的钩子只 apply 一次，想拿模块信息要在 `thisCompilation` 里再 tap。

```js
const { Compilation, sources } = require('webpack');

module.exports = class ManifestPlugin {
  apply(compiler) {
    compiler.hooks.thisCompilation.tap('Manifest', (compilation) => {
      compilation.hooks.processAssets.tap(
        { name: 'Manifest', stage: Compilation.PROCESS_ASSETS_STAGE_REPORT },
        (assets) => {
          const map = Object.fromEntries(Object.entries(assets).map(([f, a]) => [f, a.size()]));
          compilation.emitAsset('manifest.json', new sources.RawSource(JSON.stringify(map)));
        }
      );
    });
  }
};

```

webpack 5 用 `processAssets` + `emitAsset`，`compilation.assets` 在 `emit` 之后已冻结。

## 四、完整构建流程

| 阶段 | 关键动作 |
|------|----------|
| 初始化参数 | 合并 CLI 与 config，normalize 成 options |
| 创建 compiler | `new Compiler(options)`，遍历 plugins 调 `apply` 注册钩子 |
| `run` | 启动一次构建（`beforeRun`、`run`） |
| `make` | EntryPlugin 从 entry 起逐层 `buildModule`：跑 loader、解析 AST、收集依赖 |
| `seal` | 依赖图封闭，module 分到 chunk，跑 usedExports / splitChunks / runtimeChunk |
| `emit` | chunk 走 template 渲染成代码 → 写进 assets → 落盘 |
| `done` | 输出 stats |

记法：**make 收集 module，seal 决定 chunk，emit 生成 asset**。

## 五、module / chunk / bundle / asset

| 概念 | 定义 | 落盘 |
|------|------|------|
| module | 一个源文件经 loader 转换后的结果，构建图最小节点 | 否 |
| chunk | module 的分组，构建期概念，`splitChunks` 操作的就是它 | 否 |
| bundle | chunk 经 template 渲染 + 压缩后的 JS，通常与 chunk 一一对应 | 是 |
| asset | output 目录里的任意文件：bundle、`.map`、抽出的 CSS、图片 | 是 |

**chunk 是构建期概念，bundle 是产物概念，asset 是文件系统概念**；一个 chunk 可产出多个 asset。

## 六、从 stats 读 module 与 chunk 的关系

```bash
webpack --profile --json > dist/stats.json

```

```js
const { chunks, modules } = require('./dist/stats.json');
chunks
  .map((c) => ({ names: c.names, size: c.size, n: c.modules.length }))
  .sort((a, b) => b.size - a.size)
  .slice(0, 5)
  .forEach((c) => console.log(c.names, c.n, 'modules', c.size));
modules                             // 反查：某模块进了哪些 chunk
  .filter((m) => m.name.includes('lodash'))
  .forEach((m) => console.log(m.name, '→', m.chunks));

```

`chunk.modules` 与 `module.chunks` 是双向索引，任选一侧都能定位它为什么在这个文件里；`module.reasons[].moduleName` 给出引入者。

## 七、最小可跑配置

```js
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = (env, { mode }) => ({
  mode,
  entry: { app: './src/index.tsx' },
  output: { path: path.resolve('dist'), filename: '[name].[contenthash:8].js', clean: true },
  resolve: { extensions: ['.tsx', '.ts', '.js'], alias: { '@': path.resolve('src') } },
  module: {
    rules: [
      { test: /\.tsx?$/, include: path.resolve('src'), use: 'ts-loader' },
      { test: /\.css$/, use: ['style-loader', 'css-loader'] },
    ],
  },
  plugins: [new HtmlWebpackPlugin({ template: './public/index.html' })],
  optimization: { splitChunks: { chunks: 'all' }, runtimeChunk: 'single' },
});

```

慢时可给 `ts-loader` 加 `transpileOnly`，类型检查交给 `fork-ts-checker`。

## 八、常见误区

1. **以为 loader 按配置数组从左往右执行**。normal 从右往左，pitch 从左往右；「先做」的逻辑放右边。
2. **以为一个 chunk 对应一个文件**。开 CSS 抽离后一个 chunk 输出 JS + CSS 两个 asset。
3. **以为异步 chunk 的 `[name]` 会取文件名**。默认是数字 id，要用 `webpackChunkName` 魔法注释。

## 面试怎么答

**Q：loader 和 plugin 的区别？**
loader 是文件级转换器，输入输出都是字符串，跑在 `buildModule`；plugin 通过 `apply(compiler)` 在钩子介入，能拿 `compilation` 访问模块图与 chunk。判断依据是需求要不要跨文件信息。

**Q：compiler 和 compilation 什么关系？**
compiler 代表构建进程，持有配置与 watch 状态；compilation 每轮构建创建一次，持有该轮的 modules、chunks、assets。watch 下只有 compilation 重建。

**Q：chunk 和 bundle 的区别？**
chunk 是构建期对 module 的分组，`splitChunks` 操作的就是它，只在内存里；bundle 是 chunk 渲染压缩后落盘的文件。

## 关联阅读

- [构建工具原理与选型](../01-构建工具原理与选型.md)：两代构建模型的差异与选型依据
- [webpack 性能优化](./02-webpack性能优化.md)：缓存、分包、tree shaking 的具体开关
- [前端性能优化体系](../../06-性能优化/01-性能优化体系.md)：产物指标如何落到真实体验
