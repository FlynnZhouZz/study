# CSS简介

## 什么是CSS？

CSS 的全称是 层叠样式表。它是一种用于描述网页外观和格式的样式表语言。

## CSS 的作用

CSS 可以控制：
- 文字颜色、大小、字体
- 背景颜色、背景图片
- 盒模型（margin、padding、border）
- 布局（flex、grid 等）
- 动画（transition、keyframes）

## CSS 如何工作

通过 选择器（selector） 找到网页中某些元素，再把样式规则应用到它们身上。

```html
<h1>Hello World</h1>

<style>
  h1 {
    color: red;
    font-size: 30px;
  }
</style>
```

## CSS 书写位置（3 种方式）

### 1. 行内样式（不推荐，仅用于临时）

```html
<h1 style="color: blue;">标题</h1>
```

### 2. 内部样式（写在 `<style>` 里）

```html
<style>
  p {
    color: green;
  }
</style>
```

### 3. 外部样式（最推荐）

```html
<link rel="stylesheet" href="style.css">
```

style.css:
```css
p {
  color: green;
}
```