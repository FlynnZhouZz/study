# CSS 选择器

## 基础选择器

### 1. 标签选择器（Element Selector）

选择所有某个标签的元素：

```css
/* 选择所有的 <p> 元素 */
p {
  color: blue;
}
```

### 2. 类选择器（Class Selector）

根据元素的 class 属性来选择。以点 `.` 开头。
- 一个元素可以有多个类，用空格隔开。
- 一个类可以被多个元素使用。

```html
<p class="warning">这是一个警告信息</p>
<div class="warning highlighted">这是一个高亮的警告框</div>
```

```css
/* 选择所有 class 包含 "warning" 的元素 */
.warning {
    background-color: yellow;
    border-left: 3px solid red;
}

/* 选择所有 class 同时包含 "warning" 和 "highlighted" 的元素 */
.highlighted {
    font-weight: bold;
}
```

### 3. ID 选择器（ID Selector）

根据元素的 id 属性来选择。以井号 `#` 开头。
- 一个 ID 在页面中应该是唯一的。
- specificity 很高，难以被覆盖，应谨慎使用。

```html
<div id="main-header">网站主标题</div>
```

```css
/* 选择 id 为 "main-header" 的元素 */
#main-header {
    background-color: #333;
    color: white;
}
```

### 4. 通配符选择器（Universal Selector）

使用星号 *，匹配页面中的每一个元素。

```css
/* 移除所有元素的默认外边距和内边距（常用于 CSS Reset） */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box; /* 更现代的盒模型计算方式 */
}
```

## 组合选择器（组合多个选择器）

### 1. 后代选择器（Descendant）（空格）

选择位于某个元素内部的所有指定后代元素（不限层级）。

```css
/* 选择 .nav 的所有子元素 <li> */
.nav li {
  color: red;
}
```

### 2. 子选择器（Child）（>）

选择作为某个元素直接子元素的元素（仅限一级层级）。

```css
/* 只选择 .nav 的直接子元素 <li> */
.nav > li {
    border-bottom: 1px solid #ccc;
}
```

### 3. 相邻兄弟选择器（Adjacent Sibling）（+）

选择紧接在另一个元素之后的兄弟元素（紧挨着的下一个）。

```html
<h2>这是一个标题</h2>
<p>这个段落紧跟在 h2 后面，会被选中。</p>
<p>这个段落不会被选中。</p>
```

```css
/* 选择紧跟在 <h2> 后面的第一个 <p> 元素 */
h2 + p {
    margin-top: 0;
    font-style: italic;
}
```

### 4. 通用兄弟选择器（General Sibling）（~）

选择某个元素之后的所有指定兄弟元素。

```html
<h3>一个小标题</h3>
<p>这个段落会被选中。</p>
<div>一个 div</div>
<p>这个段落也会被选中。</p>
```

```css
/* 选择 <h3> 元素之后的所有 <p> 兄弟元素 */
h3 ~ p {
    color: #666;
}
```

### 5. 组选择器（Group Selector）（,）

```css
/* 对多个元素使用同样样式： */
h1, h2, p {
  color: #333;
}
```

## 属性选择器

### 1. 基础属性选择器

```css
/* 选中有 type="text" 的 input： */
input[type="text"] {
  border: 1px solid #ccc;
}
```

### 2. 属性值包含某词（含空格分隔）
```css
/* 选择 class 中包含 btn（独立单词）： */
[class~="btn"] {
  padding: 10px;
}
```

### 3. 属性值以某字符串开头

```css
/* 例如以 icon- 开头： */
[class^="icon-"] {
  font-size: 20px;
}
```

### 4. 属性值以某字符串结尾

```css
/* 例如以 .png 结尾的图片： */
img[src$=".png"] {
  border: 1px solid red;
}
```

### 5. 属性值包含某子串

```css
/* 例如 URL 中包含 banner： */
a[href*="banner"] {
  color: green;
}
```

## 伪类选择器

- 用于选择元素的特定状态
- 语法：单冒号 `:`
- 例子：`:hover, :focus, :first-child, :root`

### 1. 链接状态伪类

```css
/* 未访问的链接 */
a:link   { color: blue; }
/* 已访问过的链接 */
a:visited{ color: purple; }
/* 鼠标悬停状态 */
a:hover  { color: red; }
/* 鼠标点击时的激活状态 */
a:active { color: orange; }
```

### 2. UI 状态伪类

```css
/* 输入框获得焦点时的样式 */
input:focus { border-color: blue; }
/* 复选框/单选按钮被选中时的样式 */
input:checked { background: black; }
```

### 3. 结构伪类（非常重要）

```css
/* 选择文档根元素 */
:root {
  --main-color: #3498db;
}

/* 选第一个元素： */
li:first-child {
  color: red;
}

/* 选最后一个元素： */
li:last-child {
  color: blue;
}

/* 选第 n 个元素： */
li:nth-child(3) {
  color: green;
}

/* 选所有奇数项 (1,3,5...) */
li:nth-child(odd) {}

/* 选所有偶数项 */
li:nth-child(even) {}

/* 倒数第 2 个： */
li:nth-last-child(2) {}

/* 选择前3个元素 */
li:nth-child(-n+3) {
  font-size: 1.2em;
}

/* 选择从第4个开始的所有元素 */
li:nth-child(n+4) {
  color: gray;
}

/* 选择每3个中的第1个 (1,4,7,10...) */
li:nth-child(3n+1) {
  background: #f0f0f0;
}

/* 选择空元素 */
li:empty {
  display: none;
}

/* 选择包含特定文本的元素 */
li:contains("特定文本") {
  color: red;
}

/* 选择唯一的子元素 */
li:only-child {
  color: purple;
}

/* 选择作为其父元素中唯一指定类型的子元素 */
li:only-of-type {
  font-weight: bold;
}

/* 选择同类型元素中的第一个 */
li:first-of-type {
  border-top: 1px solid #ccc;
}

/* 选择同类型元素中的最后一个 */
li:last-of-type {
  border-bottom: 1px solid #ccc;
}

/* 选择同类型元素中的第n个 */
li:nth-of-type(2) {
  background: yellow;
}

/* 选择同类型元素中的倒数第n个 */
li:nth-last-of-type(2) {
  background: lightblue;
}
```

## 伪元素

- 用于选择元素的特定部分
- 语法：双冒号 `::` (CSS3规范)
- 例子：`::before, ::after, ::first-line, ::selection`

### 1. `::before`

```css
/* 在元素内容之前插入内容 */
p::before {
  content: "→ ";
}
```

### 2. `::after`

```css
/* 在元素内容之后插入内容 */
p::after {
  content: " ✔";
}
```

### 3. `::first-letter`
```css
/* 选择元素的第一字母（用于首字下沉） */
p::first-letter {
  font-size: 40px;
}
```

### 4. `::first-line`

```css
/* 选择元素的第一行文字 */
p::first-line {
  color: red;
}

```

### 5. `::selection`

```css
/* 用户选中的文本部分 */
::selection {
    background-color: yellow;
    color: black;
}
```

## 选择器优先级（简要）

从低到高：
- 标签选择器
- 类选择器、属性选择器、伪类
- ID 选择器
- 行内样式
- `!important`
