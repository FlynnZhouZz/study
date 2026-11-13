# CSS 列表

CSS 列表指的是使用 CSS 来样式化 HTML 中的列表元素，主要是 `<ul>`（无序列表）和 `<ol>`（有序列表），以及它们的列表项 `<li>`。

## 核心 CSS 列表属性

### 1. `list-style-type` - 设置列表项标记的类型

用于改变列表项前面的标记

```css
/* 用于无序列表 (ul) 的值： */
ul {
    list-style-type: disc; /* 默认值，实心圆点 */
    list-style-type: circle; /* 空心圆圈 */
    list-style-type: square; /* 实心方块 */
    list-style-type: none; /* 无标记（常用于导航栏）*/
}

/* 用于有序列表 (ol) 的值： */
ol {
    list-style-type: decimal; /* 默认值，数字 1, 2, 3... */
    list-style-type: decimal-leading-zero; /* 前导零数字 01, 02, 03... */
    list-style-type: lower-roman; /* 小写罗马数字 i, ii, iii... */
    list-style-type: upper-roman; /* 大写罗马数字 I, II, III... */
    list-style-type: lower-alpha; /* 小写字母 a, b, c... */
    list-style-type: upper-alpha; /* 大写字母 A, B, C... */
}
```

### 2. `list-style-position` - 设置标记的位置

定义标记位于列表项内容框的内部还是外部。

```css
ul {
    list-style-position: outside; /* 默认值，标记在内容框外 */
    list-style-position: inside; /* 标记在内容框内，成为文本流的一部分 */
}
```

视觉效果对比：

-   `outside`: (标记) 这里是列表项的内容...
-   `inside`: 这里是列表项的内容...（标记与文本起始对齐）

### 3. `list-style-image` - 使用自定义图片作为标记

可以用小图标来代替默认的标记。

```css
ul {
    list-style-image: url("bullet.png");
}
```

## 简写属性：`list-style`

语法：

```css
list-style: [list-style-type] [list-style-position] [list-style-image];
```

顺序不重要，可以省略某个值，未指定的值会设置为默认值。

示例：

```css
ul {
    /* 完整写法 */
    list-style-type: square;
    list-style-position: inside;
    list-style-image: none;

    /* 等效的简写写法 */
    list-style: square inside;
}

ol {
    list-style: upper-roman outside; /* 类型 + 位置 */
}

.custom-list {
    list-style: url("custom-bullet.png") inside; /* 图片 + 位置 */
}
```

## 实用样式示例

### 示例 1：创建水平导航菜单（最经典用法）

```css
.nav-menu {
    list-style: none; /* 移除默认项目符号 */
    padding: 0;
    margin: 0;
    background-color: #333;
    text-align: center;
}

.nav-menu li {
    display: inline-block; /* 让列表项水平排列 */
}

.nav-menu a {
    display: block;
    color: white;
    text-decoration: none;
    padding: 14px 20px;
    transition: background-color 0.3s;
}

.nav-menu a:hover {
    background-color: #555;
}
```

```html
<ul class="nav-menu">
    <li><a href="#home">首页</a></li>
    <li><a href="#news">新闻</a></li>
    <li><a href="#contact">联系</a></li>
    <li><a href="#about">关于</a></li>
</ul>
```

### 示例 2：自定义有序列表样式

```css
.steps {
    list-style: none; /* 移除默认数字 */
    padding-left: 0;
    counter-reset: step-counter; /* 初始化计数器 */
}

.steps li {
    counter-increment: step-counter; /* 递增计数器 */
    margin-bottom: 15px;
    padding-left: 40px;
    position: relative;
}

.steps li::before {
    content: counter(step-counter); /* 使用计数器作为内容 */
    position: absolute;
    left: 0;
    top: 0;
    background-color: #4caf50;
    color: white;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    text-align: center;
    line-height: 30px;
    font-weight: bold;
}
```

### 示例 3：使用 Font Awesome 图标作为标记

```css
.icon-list {
    list-style: none;
    padding-left: 0;
}

.icon-list li {
    padding-left: 30px;
    position: relative;
    margin-bottom: 10px;
}

.icon-list li::before {
    content: "\f058"; /* Font Awesome Unicode */
    font-family: "Font Awesome 5 Free";
    font-weight: 900;
    position: absolute;
    left: 0;
    color: #4caf50;
}
```

### 示例 4：多级嵌套列表样式

```css
/* 第一级 */
ul {
    list-style-type: disc;
}

/* 第二级 */
ul ul {
    list-style-type: circle;
}

/* 第三级 */
ul ul ul {
    list-style-type: square;
}

/* 有序列表嵌套 */
ol {
    list-style-type: decimal;
}

ol ol {
    list-style-type: lower-alpha;
}

ol ol ol {
    list-style-type: lower-roman;
}
```

### 示例 5：新闻列表/文章列表

```css
.article-list {
    list-style: none;
    padding: 0;
}

.article-list li {
    border-bottom: 1px solid #eee;
    padding: 15px 0;
    position: relative;
    padding-left: 20px;
}

.article-list li::before {
    content: "▶";
    position: absolute;
    left: 0;
    color: #3498db;
    font-size: 0.8em;
}

.article-list li:last-child {
    border-bottom: none;
}
```

### 示例 6：去掉默认样式

```css
ul,
ol {
    list-style: none; /* 去掉默认小圆点或数字 */
    padding: 0;
    margin: 0;
}
```

### 示例 7：描述列表美化

```css
dl {
    margin: 16px 0;
}

dt {
    font-weight: bold;
}

dd {
    margin-left: 20px;
    color: #555;
}
```

### 示例 8：列表项目分隔线

```css
ul li {
    border-bottom: 1px solid #eee;
    padding: 8px 0;
}

ul li:last-child {
    border-bottom: none; /* 去掉最后一条分隔线 */
}
```

### 示例 9：列表悬停效果

```css
ul li:hover {
    background: #f9f9f9;
    cursor: pointer;
}
```
