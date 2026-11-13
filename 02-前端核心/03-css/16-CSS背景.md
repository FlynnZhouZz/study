# CSS 背景（background）

CSS 背景（Background）是用于定义元素背景样式的属性集合。通过它们，你可以设置颜色、图片、渐变等，极大地丰富页面的视觉效果。

## 最常用的背景属性

### 1. 背景颜色（background-color）

```css
div {
    background-color: coral; /* 颜色名 */
    background-color: #ff7f50; /* 十六进制 */
    background-color: rgb(255, 127, 80); /* RGB */
    background-color: rgba(255, 127, 80, 0.5); /* 半透明的珊瑚色 */
    background-color: transparent; /* 透明 */
}
```

### 2. 背景图片（background-image）

```css
div {
    background-image: url("path/to/image.jpg"); /* 设置一张背景图 */
    background-image: url("sky.jpg"), url("birds.png"); /* 设置多张背景图（层叠） */
    background-image: linear-gradient(to right, red, yellow); /* 使用渐变作为背景 */
}
```

### 3. 重复方式（background-repeat）

```css
div {
    background-repeat: repeat; /* 默认值，在x和y方向都重复 */
    background-repeat: repeat-x; /* 只水平重复 */
    background-repeat: repeat-y; /* 只垂直重复 */
    background-repeat: no-repeat; /* 不重复，只显示一次 */
    background-repeat: space; /* 重复图片但不裁剪，均匀分布 */
    background-repeat: round; /* 重复图片并拉伸以填满空间 */
}
```

### 4. 背景位置（background-position）

```css
div {
    background-position: center; /* 一个值：同时设置x和y为中心 */
    background-position: left top; /* 关键字：左上角 */
    background-position: center bottom; /* 关键字：底部居中 */

    /* 使用长度值 */
    background-position: 20px 50px; /* 距离左边20px，顶部50px */
    background-position: 50% 50%; /* 中心点（最常用） */
    background-position: right 10px bottom 20px; /* 距离右边10px，底部20px */
}
```

### 5. 设置背景图片的尺寸（background-size）

```css
div {
    background-size: auto; /* 默认值，图片原始尺寸 */
    background-size: cover; /* 保持宽高比，将图片缩放以完全覆盖背景区（可能图片部分看不见）*/
    background-size: contain; /* 保持宽高比，将图片缩放至完全装入背景区（可能背景区有空白）*/
    background-size: 200px 100px; /* 指定具体的宽和高 */
    background-size: 50% 80%; /* 指定相对于背景区的百分比 */
}
```

### 6. 背景固定方式（background-attachment）

```css
body {
    background-attachment: scroll; /* 默认值，背景随元素一起滚动 */
    background-attachment: fixed; /* 背景相对于视口固定，不随内容滚动（创造视差效果）*/
    background-attachment: local; /* 背景随元素的内容一起滚动 */
}
```

### 7. 定位区域（background-origin）

指定背景图片的定位区域。即 background-position 相对于哪里定位。

```css
div {
    background-origin: padding-box; /* 默认值，相对于内边距框定位 */
    background-origin: border-box; /* 相对于边框框定位 */
    background-origin: content-box; /* 相对于内容框定位 */
}
```

### 8. 背景区域（background-clip）

指定背景（颜色或图片）的绘制区域。即背景可以延伸到哪个框。

```css
div {
    background-clip: border-box; /* 默认值，背景延伸到边框外边缘 */
    background-clip: padding-box; /* 背景延伸到内边距外边缘（边框下无背景）*/
    background-clip: content-box; /* 背景仅在内容区绘制 */

    /* 给文字设置背景 */
    color: transparent;
    background-clip: text; /* 非标准属性，需要 -webkit- 前缀 */
    -webkit-background-clip: text;
}
```

## background 简写（最推荐的组合写法）

语法：

```css
/* 顺序可以打乱，但一般建议 */
background: [color] [image] [repeat] [attachment] [position]/[size] [origin] [clip];
```

-   顺序不重要，但通常推荐的顺序是：颜色、图片、位置、尺寸、重复、附着等。
-   未指定的属性会使用其默认值。

## 线性渐变背景

```css
div {
    background: linear-gradient(45deg, #ff7e5f, #feb47b);
}
```

## 径向渐变背景

```css
div {
    background: radial-gradient(circle, #4facfe, #00f2fe);
}
```
