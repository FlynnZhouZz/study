# 03-框架与跨端

> 应用层。框架的价值在于"它替你做了哪些决定"，理解了这层才知道什么时候该绕开它。

## 目录

| 顺序 | 子目录 | 内容 | 篇数 | 索引 |
|------|--------|------|------|------|
| 01 | react | 组件、Hooks、状态管理、Fiber、性能优化 | 15 | [README](./01-react/README.md) |
| 02 | vue | Vue2/3 工程实践、后台管理系统搭建 | 6 | [README](./02-vue/README.md) |
| 03 | react-native | 环境、原生模块、性能、证书与上架 | 10 | [README](./03-react-native/README.md) |
| 04 | android | 为写 RN 原生模块服务的 Android 基础 | 3 | [README](./04-android/README.md) |

## 建议顺序

**React（4-6 周）**

1. 入门：[开发环境搭建](./01-react/01-开发环境搭建.md) → [JSX](./01-react/02-JSX.md) → [组件](./01-react/03-组件.md)
2. 心智模型：[生命周期](./01-react/04-生命周期.md) —— 理解挂载/更新/卸载，才能理解 Hooks 的依赖数组
3. 主力：[Hooks](./01-react/05-Hooks.md)（43KB，重点）→ [组件通信](./01-react/06-组件通信.md) → [状态管理](./01-react/07-状态管理.md)
4. 原理：[Fiber 架构](./01-react/11-Fiber架构.md) → [useCallback 闭包陷阱](./01-react/09-useCallback闭包陷阱.md)
5. 优化与版本：[常用的性能优化操作](./01-react/10-常用性能优化操作.md) → [React 19 新特性](./01-react/08-React19新特性.md)

**React Native（4-6 周）** 见 [RN 索引](./03-react-native/README.md)。典型路径：环境 → 原生模块 → 性能 → 证书与上架。

**Vue（按需）** [Vue 索引](./02-vue/README.md) 里最有价值的是完整的后台管理系统搭建实录。

## 与其他层的关系

- 向下依赖 [02-前端核心](../02-前端核心/README.md) 的 JS 内核能力——闭包没懂，Hooks 的依赖问题会反复踩。
- 向工程侧延伸：[构建工具原理与选型](../04-工程化/02-构建工具/01-构建工具原理与选型.md)、[微前端](../04-工程化/07-微前端/01-qiankun/README.md)。
- RN 落地部分与 [06-实战项目](../06-实战项目/README.md) 衔接。

> 已知缺口：路由、数据请求（SWR/React Query）、表单方案无正文；UniApp、小程序仅有面试提纲。
