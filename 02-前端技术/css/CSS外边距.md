# CSS 外边距

外边距是 CSS 盒子模型中最外层的部分，用于控制元素与其他元素之间的空间距离。

![外边距](./assets/1.png)

## 外边距的语法

### 1. 单独属性

```css
div {
    margin-top: 10px;
    margin-right: 20px;
    margin-bottom: 30px;
    margin-left: 40px;
}
```

### 2. 简写属性

记忆口诀： 上 → 右 → 下 → 左（顺时针方向）

```css
div {
    margin: 10px;                    /* 所有边都是10px */
    margin: 10px 20px;               /* 上下10px，左右20px */
    margin: 10px 20px 30px;          /* 上10px，左右20px，下30px */
    margin: 10px 20px 30px 40px;     /* 上10px，右20px，下30px，左40px（顺时针）*/
}
```

### 3. 外边距的特殊值

```css
div {
    margin: 0;           /* 无外边距 */
    margin: auto;        /* 自动计算，用于水平居中。条件：1. 必须是“块级元素”；2. 必须设置固定宽度 */
    margin: 10%;         /* 相对于父元素宽度的百分比 */
    margin: inherit;     /* 继承父元素的外边距 */
    margin: initial;     /* 重置为初始值 */
    margin: unset;       /* 重置为继承值或初始值 */
}
```

## 外边距合并现象

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

## 外边距的可用单位

- px（像素）
- em / rem
- % （基于父元素宽度）
- vh / vw
- auto
- calc()

## 常见问题与解决方案

### 问题 1：内联元素的上下外边距

```css
/* 内联元素的上下外边距无效 */
span {
    margin-top: 20px;    /* 无效 */
    margin-bottom: 20px; /* 无效 */
    margin-left: 20px;   /* 有效 */
    margin-right: 20px;  /* 有效 */
}

/* 解决方案：改为 inline-block */
span {
    display: inline-block;
    margin: 20px;        /* 现在上下外边距也有效了 */
}
```

> ps: 不建议使用 `inline-block`元素，会出现异响不到的布局

### 问题 2：浮动元素的外边距

```css
.float-left {
    float: left;
    margin-right: 20px; /* 创建与右侧元素的间距 */
}

.clearfix::after {
    content: '';
    display: table;
    clear: both;
}
```

### 问题 3：Flexbox 容器中的外边距

```css
.flex-container {
    display: flex;
    gap: 20px; /* 现代方法：使用 gap 替代外边距 */
}

.flex-item {
    /* 在 Flexbox 中，auto 外边距有特殊作用 */
    margin-left: auto; /* 将元素推到最右边 */
}
```

## 现代布局中的外边距

### 1. 使用 Gap 替代外边距

```css
/* 传统方法 */
.grid-item {
    margin: 10px;
}

/* 现代方法 */
.grid-container {
    display: grid;
    gap: 20px; /* 统一控制网格间距 */
}

.flex-container {
    display: flex;
    gap: 15px; /* 统一控制弹性项目间距 */
}
```

### 2. 逻辑属性（支持多语言）

```css
/* 物理属性 */
.physical {
    margin-top: 10px;
    margin-right: 20px;
    margin-bottom: 30px;
    margin-left: 40px;
}

/* 逻辑属性（根据书写模式自动适应）*/
.logical {
    margin-block-start: 10px;    /* 块级起始方向 */
    margin-inline-end: 20px;     /* 行内结束方向 */
    margin-block-end: 30px;      /* 块级结束方向 */
    margin-inline-start: 40px;   /* 行内起始方向 */
}
```
