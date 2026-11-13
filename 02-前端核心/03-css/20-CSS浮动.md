# CSS 浮动

CSS 浮动是一个历史悠久但非常重要的布局属性。虽然现代布局中 Flexbox 和 Grid 更常用，但理解浮动对于维护老代码和理解 CSS 发展历程仍然很有价值。

浮动 = 将元素脱离标准文档流，让其向左或向右“漂浮”，同时让文本或其他内联元素环绕它。

> 最初用于文字环绕图片，但在早期网页布局中也用作布局工具。

虽然浮动在现代布局中不再是首选，但理解它的工作原理对于：

-   维护老项目代码
-   理解 CSS 布局发展历程
-   处理特殊情况下的布局需求

## 浮动语法

```css
.element {
    float: left; /* 向左浮动 */
    float: right; /* 向右浮动 */
    float: none; /* 默认，不浮动 */
}
```

-   `float: left` → 元素靠左，其他内容围绕右边
-   `float: right` → 元素靠右，其他内容围绕左边
-   `float: none` → 不浮动（默认）

## 浮动元素的特点

1. 脱离文档流（Out of Normal Flow）

    - 浮动元素本身脱离标准文档流
    - 但会影响后续内联或行内元素

2. 宽高行为

    - 块级元素可自由设置宽高
    - 内联元素浮动后表现为块级元素（可以设置宽高）

3. 文本环绕

    - 后续内联元素（如文字、span）会环绕浮动元素

4. 父元素高度塌陷
    - 浮动元素脱离文档流，父容器无法撑高
    - 需要清除浮动（`clearfix` 或 `overflow`）

## 浮动带来的问题及解决方案

### 问题 1：父元素高度塌陷

这是浮动最经典的问题！

```html
<div class="parent">
    <div class="float-child">浮动子元素</div>
</div>
<div class="next-element">下一个元素</div>
```

```css
.parent {
    border: 3px solid red;
    padding: 10px;
}

.float-child {
    float: left;
    width: 200px;
    height: 150px;
    background: lightblue;
}

.next-element {
    background: lightcoral;
    padding: 20px;
}
```

问题现象： 父元素的红色边框会"塌陷"，高度为 0，因为浮动子元素不占据空间。

解决方案：清除浮动

方法 1：空元素清除法（传统）

```html
<div class="parent">
    <div class="float-child">浮动子元素</div>
    <div style="clear: both;"></div>
</div>
```

方法 2：伪元素清除法（推荐）

```html
<div class="parent clearfix">
    <div class="float-child">浮动子元素</div>
</div>
```

```css
.clearfix::after {
    content: "";
    display: table;
    clear: both;
}
```

方法 3：创建 BFC（块级格式化上下文）

```css
.parent {
    overflow: hidden; /* 或 auto */
    /* 或者 */
    display: flow-root; /* 现代方法，无副作用 */
}
```

### 问题 2：浮动元素之间的空白间隙

HTML 中的换行符和空格会被解析，产生间隙。

问题代码：

```html
<div class="container">
    <div class="box">Box 1</div>
    <div class="box">Box 2</div>
    <div class="box">Box 3</div>
</div>
```

解决方案：

```css
/* 方法1：负外边距 */
.box {
    float: left;
    width: 30%;
    margin-right: -4px;
}

/* 方法2：父元素 font-size: 0 */
.container {
    font-size: 0;
}
.box {
    float: left;
    width: 30%;
    font-size: 16px; /* 重置字体大小 */
}

/* 方法3：消除HTML中的空白 */
<div class="container">
    <div class="box">Box 1</div><div class="box">Box 2</div><div class="box">Box 3</div>
</div>
```

## `clear` 属性

`clear` 属性指定元素的哪一侧不允许出现浮动元素。

```css
.clear-left {
    clear: left; /* 左侧不允许浮动 */
}

.clear-right {
    clear: right; /* 右侧不允许浮动 */
}

.clear-both {
    clear: both; /* 两侧都不允许浮动 */
}
```

### 实用示例：

```html
<div class="float-left">左浮动元素</div>
<div class="float-right">右浮动元素</div>
<div class="cleared-element">这个元素会换行显示</div>
```

```css
.float-left {
    float: left;
    width: 100px;
    height: 100px;
    background: lightblue;
}

.float-right {
    float: right;
    width: 100px;
    height: 100px;
    background: lightcoral;
}

.cleared-element {
    clear: both; /* 在左右浮动元素下方显示 */
    background: lightgreen;
    padding: 20px;
}
```

## 实用布局示例

### 示例 1：传统多栏布局

```html
<div class="container">
    <header class="header">网站标题</header>

    <div class="clearfix">
        <aside class="sidebar">
            <h3>侧边栏</h3>
            <ul>
                <li>菜单项1</li>
                <li>菜单项2</li>
            </ul>
        </aside>

        <main class="main-content">
            <h2>主要内容</h2>
            <p>这里是网站的主要内容区域...</p>
        </main>
    </div>

    <footer class="footer">版权信息</footer>
</div>
```

```css
/* 清除浮动通用类 */
.clearfix::after {
    content: "";
    display: table;
    clear: both;
}

/* 布局样式 */
.container {
    width: 1200px;
    margin: 0 auto;
}

.header {
    background: #333;
    color: white;
    padding: 20px;
}

.sidebar {
    float: left;
    width: 25%;
    background: #f4f4f4;
    padding: 20px;
}

.main-content {
    float: left;
    width: 75%;
    padding: 20px;
    background: white;
}

.footer {
    clear: both; /* 确保在浮动元素下方 */
    background: #333;
    color: white;
    padding: 20px;
    text-align: center;
}
```

### 示例 2：图片画廊

```css
.gallery {
    margin: -5px; /* 补偿边缘间隙 */
}

.gallery-item {
    float: left;
    width: 25%; /* 4列布局 */
    padding: 5px;
    box-sizing: border-box;
}

.gallery-item img {
    width: 100%;
    height: auto;
    display: block;
    border-radius: 4px;
}

/* 响应式调整 */
@media (max-width: 768px) {
    .gallery-item {
        width: 33.333%; /* 3列 */
    }
}

@media (max-width: 480px) {
    .gallery-item {
        width: 50%; /* 2列 */
    }
}
```

### 示例 3：导航菜单

```css
.nav-menu {
    list-style: none;
    margin: 0;
    padding: 0;
    background: #333;
}

.nav-item {
    float: left;
}

.nav-link {
    display: block;
    padding: 15px 20px;
    color: white;
    text-decoration: none;
    transition: background 0.3s;
}

.nav-link:hover {
    background: #555;
}

/* 清除浮动 */
.nav-menu::after {
    content: "";
    display: table;
    clear: both;
}
```

## 浮动 vs 现代布局

### 传统浮动布局：

```css
.old-layout {
    float: left;
    width: 30%;
    margin-right: 5%;
}

.old-layout:last-child {
    margin-right: 0;
}
```

### 现代 Flexbox 替代：

```css
.modern-layout {
    display: flex;
    gap: 5%; /* 直接控制间距 */
}

.modern-item {
    flex: 1; /* 自动分配空间 */
}
```

### 现代 Grid 替代：

```css
.modern-layout {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5%;
}
```

## 最佳实践和注意事项

### 1. 清除浮动的最佳实践

```css
/* 现代清除浮动方法 */
.clearfix::after {
    content: "";
    display: table;
    clear: both;
}

/* 或者使用 flow-root */
.modern-clear {
    display: flow-root;
}
```

### 2. 盒模型设置

```css
/* 浮动布局中务必使用 border-box */
* {
    box-sizing: border-box;
}

.float-element {
    float: left;
    width: 33.33%;
    padding: 15px;
    border: 1px solid #ccc;
}
```

### 3. 响应式考虑

```css
.responsive-float {
    float: left;
    width: 100%; /* 移动端默认 */
}

@media (min-width: 768px) {
    .responsive-float {
        width: 50%; /* 平板端 */
    }
}

@media (min-width: 1024px) {
    .responsive-float {
        width: 33.33%; /* 桌面端 */
    }
}
```

###

```css

```
