## BEM 命名规范

BEM（Block Element Modifier）是一种 CSS 类名命名方法论，由 Yandex 团队提出，旨在让前端代码更 **模块化、可维护、可扩展**，适用于大型项目。

BEM 将 UI 拆解为 3 个部分：

- Block（块）：独立的、可复用的组件（如 .header, .menu）。
- Element（元素）：属于 Block 的一部分，不能单独使用（如 .menu__item）。
- Modifier（修饰符）：表示 Block 或 Element 的状态或样式变体（如 .button--disabled）。

