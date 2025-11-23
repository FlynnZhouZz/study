# CSS 显示和可见性

CSS 的 `display` 和 `visibility` 都是控制元素显示和隐藏的重要属性，但它们的工作方式和效果有本质区别。

## `display` 属性

`display` 属性定义元素应该生成的框的类型，它决定了元素如何参与页面流式布局。

### 1. 常用 `display` 值

**块级元素：**

-   独占一行
-   可以设置宽度、高度
-   默认宽度为父元素的 100%
-   示例：`<div>`, `<p>`, `<h1>-<h6>`, `<section>`

```css
.element {
    display: block; /* 元素显示为块级元素，前后有换行符 */
}
```

**行内元素：**

-   在一行内显示
-   不能设置宽度、高度
-   宽度由内容决定
-   示例：`<span>`, `<a>`, `<strong>`, `<em>`

```css
.element {
    display: inline; /* 元素显示为行内元素，前后无换行符 */
}
```

**行内块元素：**

-   像行内元素一样排列（不换行）
-   像块级元素一样可以设置宽度、高度
-   示例：`<img>`, `<button>`, `<input>`

```css
.element {
    display: inline-block; /* 行内块元素 */
}
```

**隐藏并移除布局：**

```css
.element {
    display: none; /* 元素隐藏，且不占据空间 */
}
```

### 2. 现代布局 `display` 值

**Flexbox 布局：**

又称：弹性布局

```css
.container {
    display: flex; /* 块级弹性容器 */
    display: inline-flex; /* 行内弹性容器 */
}
```

**Grid 布局：**

又称：网格布局

```css
.container {
    display: grid; /* 块级网格容器 */
    display: inline-grid; /* 行内网格容器 */
}
```

**其他值：**

```css
.element {
    display: table; /* 像表格一样显示 */
    display: table-cell; /* 像表格单元格一样显示 */
    display: list-item; /* 像列表项一样显示 */
}
```

## `visibility` 属性

`visibility` 属性控制元素是否可见，但不改变元素的布局位置。

### 常用 `visibility` 值：

```css
.element {
    visibility: visible; /* 默认值，元素可见 */
    visibility: hidden; /* 元素不可见，但仍占据空间 */
    visibility: collapse; /* 主要用于表格元素，在 table-row 中可折叠行 */
}
```

## `display` vs `visibility` 的根本区别

| 属性                   | 是否可见 | 是否占空间 | 会不会影响布局 |
| ---------------------- | -------- | ---------- | -------------- |
| **display: none**      | 不可见   | 不占空间   | 会影响         |
| **visibility: hidden** | 不可见   | 占空间     | 会影响布局     |

### 视觉与布局效果对比

假设有三个盒子：

```css
[A] [B] [C]
```

`display: none`

```css
[A] [C]      （B 完全消失）
```

`visibility: hidden`

```css
[A] [ ] [C]  （B 的空间还在，只是透明）
```

## 常见使用场景

### 1. 使用 `display: none` 适用场景

-   隐藏菜单项
-   弹窗（modal）显示/关闭
-   SPA 页面切换
-   移动端切换 tab 内容
-   动态添加移除 DOM

### 2. 使用 `visibility: hidden` 适用场景

-   保持布局不变隐藏内容
-   表格某列隐形但保持宽度
-   防止跳动的动画
-   保留元素位置但不显示（占位）

## `display` 常见细节与陷阱

### 1. `inline` 元素不能设置 `width/height`

### 2. `display` 切换会影响 `animation/transition`

许多 CSS 动画无法对 `display` 做过渡，因此常用：

`opacity` + `visibility` 实现淡入淡出

```css
.fade {
    opacity: 0;
    visibility: hidden;
    transition: 0.3s;
}
.fade.show {
    opacity: 1;
    visibility: visible;
}
```

### 3. `visibility: hidden` 仍能被点击（取决于浏览器）

多数浏览器中：

-   visibility: hidden = 不可点
-   但 opacity: 0 = 可点击（容易踩坑）

## 性能与可访问性考虑

### 1. 性能影响

```css
/* 频繁切换时考虑性能 */
.high-performance {
    visibility: hidden; /* 重绘但不重排 */
}

.low-performance {
    display: none; /* 可能引起重排 */
}
```

### 2. 可访问性

```css
/* 错误的可访问性做法 */
[aria-hidden="true"] {
    display: none; /* 对屏幕阅读器隐藏 */
}

/* 确保焦点管理 */
.hidden-element {
    display: none; /* 从焦点顺序中移除 */
}

.visible-but-hidden {
    visibility: hidden; /* 仍在焦点顺序中，可能有问题 */
}
```

## 现代 CSS 的替代方案

### 1. 使用 opacity

```css
.fade-element {
    opacity: 0; /* 透明但占据空间 */
    pointer-events: none; /* 禁用交互 */
    transition: opacity 0.3s ease;
}

.fade-element.visible {
    opacity: 1;
    pointer-events: auto;
}
```

### 2. 使用 clip-path

```css
.clip-hidden {
    clip-path: inset(50%); /* 隐藏但占据空间 */
    transition: clip-path 0.3s ease;
}

.clip-visible {
    clip-path: inset(0); /* 完全显示 */
}
```

## `inline-block` 常见问题汇总

### 问题 1：`inline-block` 之间出现“神秘空隙”

现象：两个 `inline-block` 元素之间会出现 3px~6px 的空白间距：

```html
<div class="item"></div>
<div class="item"></div>
<!-- 中间出现空隙！ -->
```

原因：

> HTML 中换行/空格会被当成空白字符处理，浏览器会把它渲染为 inline 元素间距。

解决方案：

#### 方案 1：HTML 写在同一行

```html
<div class="item"></div>
<div class="item"></div>
```

#### 方案 2：移除中间的换行（注释法）

```html
<div class="item"></div>
<!--
-->
<div class="item"></div>
```

#### 方案 3：父元素设置 `font-size: 0`（最常用）

```css
.container {
    font-size: 0;
}
.item {
    font-size: 16px; /* 恢复 */
}
```

#### 方案 4：用 `flex` 或 `grid` 替代 `inline-block`（现代方案）

```css
.container {
    display: flex;
}
```

### 问题 2：`inline-block` 会受 `vertical-align` 影响（导致对齐异常）

现象: 多个 inline-block 元素可能顶对齐、底对齐不一致。

原因: `inline-block` 本质仍是 `inline`，因此会受 `line-height` 与 `vertical-align` 影响。

解决：

```css
inline-block-element {
    vertical-align: middle; /* 中线对齐 */
}
/* 或者 */
inline-block-element {
    vertical-align: top; /* 顶部对齐 */
}
```

### 问题 3：宽度被内容撑开，无法自动换行

现象：多个 `inline-block` 元素如果宽度不足，会自动换行，但换行位置难以控制。

解决：一般使用 flex-wrap 更可控：

```css
.container {
    display: flex;
    flex-wrap: wrap;
}
```

### 问题 4：`inline-block` 遇到中文时对齐异常

原因: 中文字体行高不同，line-height 影响更明显。

解决:

```css
.inline-block {
    line-height: 1;
}
```

### 问题 5：`inline-block` 超宽被挤压换行

如果父容器宽度太小，inline-block 元素会自动换行（和 inline 一样）。

解决：

```css
/* 要禁止换行 */
parent {
    white-space: nowrap;
}
```

### 问题 6：`inline-block` 元素高度不一致时对齐错乱

默认 `vertical-align` 情况下高度不同会导致底部不齐。

解决：

```css
.inline-block {
    vertical-align: top; /* 或 middle/bottom，按需求 */
}
```

### `inline-block` 的最佳实践

推荐使用 `flex` 或 `grid` 替代 `inline-block`

inline-block 在现代布局中使用越来越少，因为：

-   有空白间隙问题
-   vertical-align 影响布局
-   多行对齐困难
-   不是响应式设计友好
