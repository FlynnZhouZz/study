# CSS 函数（CSS Functions）

CSS 函数（CSS Functions） 是在 CSS 属性值中使用的“内置方法”，用于计算、颜色处理、尺寸适配、变换、判断等。

## 变量 & 计算类（最常用）

### `var()` —— 使用 CSS 变量

```css
color: var(--primary-color);
width: var(--w, 100px);
```

### `calc()` —— 动态计算

```css
width: calc(100% - 24px);
height: calc(var(--h) * 2);
```

规则：

-   `+ - * /` 必须有空格
-   可混合单位（px + %）

### `min()` / `max()` / `clamp()`

```css
width: min(600px, 100%);

font-size: clamp(14px, 2vw, 20px);
/* 视口宽度小时不小于 14px，大时不超过 20px，中间按 2vw 动态调整 */
```

`clamp(min, preferred, max)` = 响应式神器

-   min：最小值（下限）
-   preferred：首选值（通常使用相对单位，如 vw、%、em 等）
-   max：最大值（上限）

clamp() 返回的值会：

-   如果首选值小于最小值 → 返回最小值
-   如果首选值在最小值和最大值之间 → 返回首选值
-   如果首选值大于最大值 → 返回最大值

## 颜色函数

### `rgb()` / `rgba()`

```css
color: rgb(255 0 0);
color: rgba(0, 0, 0, 0.5);
```

### `hsl()` / `hsla()`

```css
background: hsl(210 50% 40%);
```

非常适合做主题色调整

### `color-mix()`（现代，旧浏览器不支持）

```css
background: color-mix(in srgb, red 70%, white);
```

语法：

```css
color-mix(in colorspace, color1 percentage, color2 percentage)
```

-   `in colorspace`：颜色空间，指定混合使用的色彩模型

    -   srgb（默认）
    -   srgb-linear
    -   lab
    -   oklab
    -   lch
    -   oklch
    -   hsl
    -   hwb
    -   xyz
    -   xyz-d50 / xyz-d65

-   `color1` 和 `color2`：要混合的颜色

    -   可以是任何有效的 CSS 颜色值（十六进制、rgb、hsl、颜色名称等）
    -   可以使用 color() 函数指定特定颜色空间的颜色

-   百分比：每个颜色在混合中的占比
    -   如果省略，默认各占 50%
    -   总和可以超过 100%（会按比例重新计算）
    -   如果只指定一个百分比，另一个会自动补全

示例说明：

```css
.element {
    /* 混合红色和蓝色，各占50% */
    color: color-mix(in srgb, red, blue);

    /* 红色70%，蓝色30% */
    background-color: color-mix(in srgb, red 70%, blue 30%);

    /* 只指定一个百分比 */
    border-color: color-mix(in srgb, #ff0000 25%, #0000ff);
    /* 等同于：红色25%，蓝色75% */
}
```

## 渐变函数（背景）

### `linear-gradient()`

```css
background: linear-gradient(to right, #409eff, #67c23a);
```

### `radial-gradient()`

```css
background: radial-gradient(circle, #fff, #000);
```

### `conic-gradient()`

```css
background: conic-gradient(red, yellow, green);
```

## 尺寸 / 路径 / 引用

### `url()`

```css
background-image: url("./bg.png");
```

### attr()（受限）

```css
content: attr(data-text);
```

目前主要用于 `content`

## 变换 & 动画函数

### transform

```css
transform: translate(50px, 20px) rotate(45deg) scale(1.2);
```

常见子函数：

-   translate()
-   translateX()
-   rotate()
-   scale()
-   skew()

### `cubic-bezier()`

```css
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

### `steps()`

```css
animation: typing 2s steps(10);
```

## 布局 & 逻辑判断

### `repeat()`（Grid）

```css
grid-template-columns: repeat(3, 1fr);
```

### `fit-content()`

```css
width: fit-content(300px);
```

### `env()` —— 环境变量

```css
padding-bottom: env(safe-area-inset-bottom);
/* safe-area-inset-bottom: iOS 刘海屏 */
```

## 滤镜函数（视觉效果）

### `filter`

```css
filter: blur(4px) brightness(1.2) grayscale(50%);
```

### `backdrop-filter`

```css
backdrop-filter: blur(10px);
```

## 文本 & 数学增强（现代）

### `counter()`

```css
content: counter(item);
```

### `round()` / `mod()`（新）

```css
width: round(33.3%, 1%);
```
