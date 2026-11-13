# CSS 盒子模型

CSS 盒子模型是 CSS 中最核心、最重要的概念之一。它描述了在网页布局中，每个元素都被表示为一个矩形的"盒子"，这个盒子由内容、内边距、边框和外边距组成。

## 盒子模型概念

- content（内容区）：显示文本或图片的区域
- padding（内边距）：内容与边框之间的空白
- border（边框）：包围内容和内边距的边框
- margin（外边距）：元素与外部元素之间的间距

```text
┌─────────────────────────────────────────┐
│                  Margin                  │  ← 外边距（透明）
│  ┌─────────────────────────────────────┐ │
│  │               Border                │ │  ← 边框
│  │  ┌─────────────────────────────────┐ │ │
│  │  │            Padding             │ │ │  ← 内边距（透明）
│  │  │  ┌─────────────────────────────┐ │ │ │
│  │  │  │          Content            │ │ │ │  ← 内容（文字、图片等）
│  │  │  └─────────────────────────────┘ │ │ │
│  │  └─────────────────────────────────┘ │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## 详细解析

### 1. 内容 - Content

盒子的核心区域，包含文本、图像或其他媒体内容。

通过 `width` 和 `height` 属性设置大小。

```css
div {
    width: 300px;
    height: 200px;
}
```

### 2. 内边距 - Padding

内容区域与边框之间的透明空间。

使用 `padding` 属性设置。

```css
div {
    padding: 20px;                    /* 上下左右都是20px */
    padding: 10px 20px;               /* 上下10px，左右20px */
    padding: 10px 20px 30px 40px;     /* 上10px、右20px、下30px、左40px（顺时针）*/
    
    /* 也可以分别设置 */
    padding-top: 10px;
    padding-right: 20px;
    padding-bottom: 30px;
    padding-left: 40px;
}
```

### 3. 边框 - Border

围绕内边距和内容的线。

使用 border 属性设置。

```css
div {
    border: 2px solid #333;           /* 宽度 样式 颜色 */
    border: 1px dashed red;           /* 虚线边框 */
    border: 3px dotted blue;          /* 点线边框 */
    
    /* 也可以分别设置 */
    border-width: 2px;
    border-style: solid;
    border-color: #333;
    
    /* 或只设置某一边 */
    border-top: 1px solid #ccc;
    border-right: none;               /* 移除右边框 */
}
```

### 4. 外边距 - Margin

盒子与其他盒子之间的透明空间。

使用 `margin` 属性设置，语法与 `padding` 相同。

```css
div {
    margin: 20px;                     /* 上下左右都是20px */
    margin: 0 auto;                   /* 上下0，左右自动（水平居中）*/
    margin: 10px 20px 30px 40px;      /* 上10px、右20px、下30px、左40px */
    
    /* 也可以分别设置 */
    margin-top: 10px;
    margin-bottom: 20px;
}
```

## 两种盒子模型：标准 vs 怪异

这是盒子模型最重要的概念！CSS 有两种不同的盒子模型，它们计算元素总宽度和总高度的方式不同。

### 1. 标准盒子模型（content-box，默认）

总宽度 = `width` + `padding` + `border` + `margin`

```css
.box {
    box-sizing: content-box; /* 默认值 */
    width: 300px;
    padding: 20px;
    border: 5px solid #333;
    margin: 10px;
}
```

### 2. 怪异盒子模型（又称：IE 盒子模型 / 边框盒子模型）（border-box）

总宽度 = `width`（已包含 `padding` 和 `border`）+ `margin`

```css
.box {
    box-sizing: border-box; /* 使用怪异盒子模型 */
    width: 300px;           /* 这个宽度现在包含内容+padding+border */
    padding: 20px;
    border: 5px solid #333;
    margin: 10px;
}
```

推荐使用 border-box，避免宽度计算复杂。

Why?

- 更直观：设置的 width 就是元素实际占用的宽度
- 更容易实现响应式布局
- 简化了百分比和计算的使用

## 盒子模型实践示例

### 示例 1：直观对比两种模型

```html
<div class="box content-box">标准盒子模型</div>
<div class="box border-box">怪异盒子模型</div>
```

```css
.box {
    width: 200px;
    padding: 20px;
    border: 5px solid #333;
    margin: 10px;
    background-color: lightblue;
}

.content-box {
    box-sizing: content-box; /* 总宽度: 200 + 40 + 10 + 20 = 270px */
}

.border-box {
    box-sizing: border-box;  /* 总宽度: 200 + 20 = 220px */
}
```

### 示例 2：实用布局技巧
```css
/* 现代CSS开发的最佳实践 */
* {
    box-sizing: border-box; /* 为所有元素设置怪异盒子模型 */
}

.container {
    width: 1200px;
    margin: 0 auto; /* 水平居中 */
    padding: 20px;
}

.card {
    width: calc(33.333% - 30px); /* 三列布局，考虑margin */
    float: left;
    margin: 15px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: white;
}
```

### 示例 3：外边距合并现象

当两个垂直相邻块级元素的上下外边距相遇时，它们会合并成一个外边距，其大小为两者中的较大者。
> ps: 只有上下外边距会出现合并现象，左右外边距不会合并

```css
.box1 {
    margin-bottom: 30px;
    background: lightcoral;
}

.box2 {
    margin-top: 20px;
    background: lightblue;
}
```

实际效果： 两个盒子之间的间距是 30px（不是 30px + 20px = 50px）
