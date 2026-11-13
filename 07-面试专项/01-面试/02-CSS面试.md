# CSS 面试

> CSS 面试的分水岭不在会不会写样式，而在能不能说清「浏览器按什么规则算出这个结果」——盒模型、层叠、格式化上下文，三件事解释了绝大多数「为什么没生效」。

## 盒模型

`box-sizing: content-box`（默认）下 `width` 只算内容区，`border-box` 下 `width` 含 padding 与 border。

```css
*, *::before, *::after { box-sizing: border-box; }
```

追问会往「为什么现在普遍用 border-box」走：因为它让宽度可预测，`width: 100%` 加左右 padding 不会撑破容器。代价是 `height` 也把 padding 算进去，做等高布局时要留意。

## 选择器权重与层叠

权重按四元组比较，不是十进制相加：

| 权重位 | 来源 | 示例 |
|---|---|---|
| (1,0,0,0) | 内联样式 | `style="color:red"` |
| (0,1,0,0) | ID | `#app` |
| (0,0,1,0) | 类、属性、伪类 | `.btn`、`[type=text]`、`:hover` |
| (0,0,0,1) | 元素、伪元素 | `div`、`::before` |

`!important` 跳出这套比较；`*` 与继承来的样式权重为 0。

层叠顺序（从低到高）：浏览器默认 → 用户样式 → 作者样式 → 作者 `!important` → 用户 `!important` → 浏览器 `!important`。同权重时后出现的胜出，这就是「为什么加了样式没生效」的常见答案：不是权重不够，是顺序在后。

`:not()` 与 `:is()` 的权重取括号内**最高**的那个；`:where()` 权重恒为 0，适合写可覆盖的基础样式。

## 块级格式化上下文（BFC）

BFC 是一个独立的渲染区域，内部布局不影响外部。触发条件：

```css
/* 任意一条即可 */
overflow: hidden;          /* 不等于 visible */
display: flow-root;        /* 最干净的写法，无副作用 */
float: left | right;
position: absolute | fixed;
display: inline-block | flex | grid | table-cell;
contain: layout | paint;
```

它能解决三件事，面试基本都问：

1. **margin 塌陷**：父子元素的上外边距合并，父元素加 `overflow: hidden` 或 `display: flow-root` 隔断
2. **高度塌陷**：子元素浮动导致父元素高度为 0，触发 BFC 后父元素能包住浮动子元素
3. **阻止元素被浮动元素覆盖**：右侧文字块加 BFC 后不会绕排到浮动元素下方

`display: flow-root` 是专门为触发 BFC 而生的值，没有 `overflow: hidden` 裁剪内容、影响滚动条的副作用，现代项目优先用它。

## 居中

```css
/* 单行文本 */
.center { text-align: center; line-height: 100px; }

/* 绝对定位 + transform，不需要知道尺寸 */
.center {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}

/* flex，最通用 */
.center { display: flex; align-items: center; justify-content: center; }

/* grid，一行搞定 */
.center { display: grid; place-items: center; }

/* 块级元素水平居中（有确定宽度） */
.center { margin: 0 auto; }
```

追问「transform 的百分比相对谁」：相对元素自身的宽高，所以不需要预先知道尺寸。

## Flex 与 Grid 的分工

| 维度 | Flex | Grid |
|---|---|---|
| 方向 | 一维（主轴 + 交叉轴） | 二维（行 + 列同时控制） |
| 尺寸由谁决定 | 内容驱动（由内向外） | 容器驱动（由外向内） |
| 典型场景 | 导航栏、卡片内部、垂直居中 | 页面骨架、仪表盘、图片瀑布流 |

Flex 三个高频细节：

- `flex: 1` 是 `flex: 1 1 0%` 的简写，`flex-basis: 0` 才是「平均分」的关键；写 `flex: 1 1 auto` 会按内容分配
- `flex-shrink` 默认 1，子项 `min-width: auto` 导致长文本撑住不缩，要显式 `min-width: 0`
- `align-items` 控制交叉轴单行对齐，`align-content` 控制多行之间的分布，`flex-wrap: nowrap` 时后者无效

## 响应式

| 方案 | 原理 | 适用 |
|---|---|---|
| 媒体查询 | `@media (min-width: 768px)` | 断点式布局切换 |
| 相对单位 | `rem`（根字号）、`em`（父字号）、`vw/vh` | 整体缩放 |
| 弹性布局 | `%`、`flex`、`grid` 的 `fr` | 容器内自适应 |
| 容器查询 | `@container` | 组件级响应，与视口解耦 |

移动端适配主流做法：`html { font-size: calc(100vw / 7.5) }` 配合 `rem`，或直接用 `vw`。`clamp()` 能一步写出带上下限的自适应字号：

```css
font-size: clamp(14px, 2.5vw, 20px);
```

## 动画性能

只有 `transform` 与 `opacity` 能在合成线程完成，不触发 layout 与 paint；改 `width`、`left`、`margin` 会走完整流水线。

```css
/* 差：每帧重排 */
.move { transition: left .3s; }
/* 好：只做合成 */
.move { transition: transform .3s; will-change: transform; }
```

`will-change` 会提前创建图层，用多了导致图层爆炸、内存上升，用完应移除或在动画结束后置为 `auto`。

## BEM 命名规范

BEM（Block Element Modifier）是一种 CSS 类名命名方法论，由 Yandex 团队提出，旨在让前端代码更 **模块化、可维护、可扩展**，适用于大型项目。

BEM 将 UI 拆解为 3 个部分：

- Block（块）：独立的、可复用的组件（如 `.header`、`.menu`）
- Element（元素）：属于 Block 的一部分，不能单独使用（如 `.menu__item`）
- Modifier（修饰符）：表示 Block 或 Element 的状态或样式变体（如 `.button--disabled`）

它的实际价值是让选择器权重保持扁平（全是单类名），避免为了覆盖样式不断加深嵌套。配合 CSS Modules 或 `scoped` 使用时，BEM 更多是命名约定而非必需。

## 常见误区

**很多人以为 `z-index` 数值大就一定在上面**。`z-index` 只在同一层叠上下文内比较；父级建立了新的层叠上下文（`transform`、`opacity < 1`、`filter`、`will-change` 都会），子元素的 `z-index` 再大也跳不出父级那一层。

**很多人以为 `overflow: hidden` 只是裁剪**。它同时会创建 BFC 和新的滚动容器，可能让 `position: sticky` 失效——sticky 的滚动容器变成了这个 `overflow` 元素。

**很多人以为 `position: fixed` 相对视口定位**。祖先元素有 `transform`/`filter`/`perspective` 时，`fixed` 会退化成相对该祖先定位，这是「弹窗位置错乱」的常见原因。

## 面试怎么答

**Q：两个 div 之间的 margin 为什么合并了？**
A：相邻兄弟元素或父子元素（中间无 border/padding/内容）的垂直外边距会取较大值合并。解法是给父元素建立 BFC（`display: flow-root`）、加 padding 或 border，或者改用 flex/grid 布局（flex 容器的子项不参与 margin 塌陷）。

**Q：如何实现左侧固定、右侧自适应？**
A：三种写法——flex（左 `flex: 0 0 200px`，右 `flex: 1`，注意右侧要 `min-width: 0`）、grid（`grid-template-columns: 200px 1fr`）、或者左侧 `float` + 右侧 `overflow: hidden` 触发 BFC。前两种是现代首选。

**Q：CSS 变量和 Sass 变量的区别？**
A：CSS 变量是运行时属性，能被 JS 读写、能随媒体查询和继承变化、参与层叠；Sass 变量在编译期就被替换成字面量，产物里不存在。做主题切换必须用 CSS 变量。

## 关联阅读

- [CSS 索引](../../02-前端核心/03-css/README.md)
- [JS 面试](./03-JS面试.md)
- [网络八股](../02-面试八股/01-网络八股.md)
