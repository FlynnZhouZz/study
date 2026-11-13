# 02-前端核心

> 语言与样式层。这一层决定你写的代码"对不对"，框架层决定"快不快"。

## 目录

| 顺序 | 子目录 | 内容 | 篇数 | 索引 |
|------|--------|------|------|------|
| 01 | web开发 | Web 是什么、URL/域名、命令行、服务端认知 | 9 | [README](./01-web开发/README.md) |
| 02 | html | 标签语义、表单、多媒体、Canvas/SVG | 35 | [README](./02-html/README.md) |
| 03 | css | 盒模型、布局、动效、响应式 | 40 | [README](./03-css/README.md) |
| 04 | javascript | 语言内核 43 篇，编号即顺序 | 43 | [README](./04-javascript/README.md) |
| 05 | typescript | 类型系统与类型体操 | 2 | [README](./05-typescript/README.md) |

## 建议顺序

**第一步：Web 认知（1 周）**
[Web 和 Web 标准](./01-web开发/01-Web和Web标准.md) → [URL](./01-web开发/04-URL.md) → [域名](./01-web开发/05-域名.md) → [Web 服务器](./01-web开发/06-Web服务器.md) → [命令行](./01-web开发/07-命令行.md)

**第二步：HTML（1-2 周）**
先看 [HTML 基础语法](./02-html/01-HTML基础语法.md)，再按「结构 → 内容 → 表单 → 多媒体 → 进阶」推进，具体顺序见 [HTML 索引](./02-html/README.md)。重点是[语义元素](./02-html/11-语义元素.md)和[页面结构化和语义化](./02-html/12-页面结构化和语义化.md)——这是可访问性与 SEO 的基础。

**第三步：CSS（3-4 周）** 按能力块推进，不要按文件名：

| 能力块 | 文档 |
|--------|------|
| 入门 | [简介](./03-css/01-CSS简介.md) → [语法](./03-css/02-CSS语法.md) → [创建](./03-css/03-CSS创建.md) → [发展史](./03-css/04-CSS发展史.md) → [浏览器支持](./03-css/05-CSS浏览器支持.md) |
| 选择器 | [选择器](./03-css/06-CSS选择器.md) → [CSS !important](./03-css/07-CSS-important.md) |
| 文本与颜色 | [css颜色](./03-css/08-CSS颜色.md) → [文本格式](./03-css/09-CSS文本格式.md) |
| 盒模型 | [盒子模型](./03-css/10-CSS盒子模型.md) → [尺寸](./03-css/11-CSS尺寸.md) → [内边距](./03-css/12-CSS内边距.md) → [外边距](./03-css/13-CSS外边距.md) → [边框](./03-css/14-CSS边框.md) → [轮廓](./03-css/15-CSS轮廓.md) → [背景](./03-css/16-CSS背景.md) → [溢出](./03-css/17-CSS溢出.md) |
| 布局 | [文档流](./03-css/18-CSS文档流.md) → [显示和可见性](./03-css/19-CSS显示和可见性.md) → [浮动](./03-css/20-CSS浮动.md) → [定位](./03-css/21-CSS定位.md) → [对齐方式](./03-css/22-CSS对齐方式.md) → [网页布局](./03-css/23-CSS网页布局.md) → [多列布局](./03-css/24-CSS多列布局.md) → [透明度](./03-css/25-CSS透明度.md) |
| 响应式 | [响应式设计](./03-css/26-CSS响应式设计.md) → [媒体查询](./03-css/27-CSS媒体查询.md) |
| 组件样式 | [列表](./03-css/28-CSS列表.md) → [表格](./03-css/29-CSS表格.md) → [表单](./03-css/30-CSS表单.md) → [链接](./03-css/31-CSS链接.md) → [用户界面](./03-css/32-CSS用户界面.md) → [计数器](./03-css/33-CSS计数器.md) |
| 动效与新特性 | [过渡](./03-css/34-CSS过渡.md) → [动画](./03-css/35-CSS动画.md) → [2D 转换](./03-css/36-CSS-2D转换.md) → [3D 转换](./03-css/37-CSS-3D转换.md) → [变量](./03-css/38-CSS变量.md) → [原生嵌套](./03-css/39-CSS原生嵌套.md) → [函数](./03-css/40-CSS函数.md) |

**第四步：JavaScript（4-6 周）**
严格按 [JavaScript 索引](./04-javascript/README.md) 的编号顺序。三处必须读透：

- 执行机制：[执行上下文](./04-javascript/08-什么是执行上下文.md) → [垃圾回收](./04-javascript/09-垃圾回收机制.md) → [事件循环](./04-javascript/10-作业队列与事件循环.md)
- 语言难点：[闭包](./04-javascript/32-闭包.md) → [继承与原型链](./04-javascript/33-继承与原型链.md)
- 异步：[Promise](./04-javascript/25-Promise.md) → [async/await](./04-javascript/26-async-await.md)

**第五步：TypeScript（1-2 周）**
[类型系统基础](./05-typescript/01-类型系统基础.md) → [类型体操](./05-typescript/02-类型体操.md)。前者讲清结构化类型、收窄、泛型与条件类型，后者是纯练习。

> 已知缺口：CSS 缺 Flexbox/Grid 专题。见 [缺口清单](../00-路线/02-进度看板.md)。
