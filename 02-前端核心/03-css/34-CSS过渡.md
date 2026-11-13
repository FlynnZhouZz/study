# CSS 过渡

CSS 过渡允许你在 CSS 属性值之间添加平滑的动画效果，而不是立即改变。当元素从一种状态变为另一种状态时，过渡效果会自动执行。

CSS 过渡是创建简单动画的首选方案，因为它性能好、实现简单。对于更复杂的动画序列，可以考虑使用 CSS 动画（@keyframes）。

常见效果：

-   悬停变色
-   放大 / 缩小
-   位移
-   透明度变化
-   阴影变化

过渡必须满足两个条件：

1. 属性发生变化（如 `:hover`、类名切换）
2. 该属性是 可过渡属性

## 基本语法

```css
.element {
    /* 简写属性 */
    transition: property duration timing-function delay;

    /* 分开写法 */
    transition-property: all;
    transition-duration: 0.3s;
    transition-timing-function: ease;
    transition-delay: 0s;
}
```

## 过渡属性详解

### 1. `transition-property`

指定要应用过渡效果的 CSS 属性。

```css
transition-property: all; /* 所有属性 */
transition-property: width, height; /* 指定多个属性 */
transition-property: opacity; /* 单个属性 */
```

### 2. `transition-duration`

定义过渡效果持续的时间。

```css
transition-duration: 0.3s; /* 0.3秒 */
transition-duration: 500ms; /* 500毫秒 */
transition-duration: 2s; /* 2秒 */
```

### 3. `transition-timing-function`

定义过渡效果的速度曲线。

```css
transition-timing-function: ease; /* 默认，慢-快-慢 */
transition-timing-function: linear; /* 匀速 */
transition-timing-function: ease-in; /* 慢开始 */
transition-timing-function: ease-out; /* 慢结束 */
transition-timing-function: ease-in-out; /* 慢开始和结束 */
transition-timing-function: cubic-bezier(x1, y1, x2, y2); /* 自定义贝塞尔曲线 */
```

### 4. `transition-delay`

定义过渡效果开始前的延迟时间。

```css
transition-delay: 0s; /* 无延迟 */
transition-delay: 0.5s; /* 延迟0.5秒 */
transition-delay: 1s; /* 延迟1秒 */
```

## 可应用过渡的属性

大多数 CSS 属性都可以应用过渡效果，包括：

-   位置属性：`top, left, right, bottom`
-   尺寸属性：`width, height, padding, margin`
-   颜色属性：`color, background-color, border-color`
-   变换属性：`transform`（性能最佳）
-   透明度：`opacity`
-   字体属性：`font-size, line-height`

## 简单示例

### 基本示例

```css
.button {
    background-color: blue;
    transition: background-color 0.3s ease;
}

.button:hover {
    background-color: red;
}
```

### 多个属性过渡

```css
.box {
    width: 100px;
    height: 100px;
    background: lightblue;
    transition: width 0.5s, height 0.5s, background 1s;
}

.box:hover {
    width: 200px;
    height: 200px;
    background: lightcoral;
}
```

### 复杂示例

```css
.card {
    transform: scale(1);
    opacity: 1;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
    transform: scale(1.05);
    opacity: 0.9;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}
```

## 性能最佳实践

### 1. 优先使用`transform`和`opacity`

```css
/* 性能好 - 触发合成层 */
.element {
    transition: transform 0.3s, opacity 0.3s;
}

/* 性能较差 - 触发重排 */
.element {
    transition: width 0.3s, height 0.3s;
}
```

### 2. 避免过渡太多属性

```css
/* 不推荐 */
transition: all 0.3s;

/* 推荐 */
transition: transform 0.3s, opacity 0.3s;
```

## 链式过渡

可以创建连续的过渡效果：

```css
.element {
    transition: transform 0.3s ease, opacity 0.3s ease 0.3s; /* 延迟开始 */
}
```

## JavaScript 交互

```js
// 添加过渡类
element.classList.add("active");

// 动态设置过渡
element.style.transition = "transform 0.3s ease";

// 监听过渡结束
element.addEventListener("transitionend", function (event) {
    console.log("过渡完成:", event.propertyName);
});
```

## 浏览器兼容性

CSS 过渡在现代浏览器中支持良好：

-   Chrome 26+
-   Firefox 16+
-   Safari 6.1+
-   Edge 12+
-   Opera 12.1+

### 需要前缀的旧版浏览器：

```css
.element {
    -webkit-transition: all 0.3s ease;
    -moz-transition: all 0.3s ease;
    -o-transition: all 0.3s ease;
    transition: all 0.3s ease;
}
```
