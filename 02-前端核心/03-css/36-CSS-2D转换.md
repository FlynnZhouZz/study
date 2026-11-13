# CSS 2D 转换

它允许您在不使用图像或脚本的情况下，对网页元素进行移动、旋转、缩放和倾斜。

CSS 2D 转换（2D Transform） 可以让元素在 二维平面（x、y） 上进行：

-   平移（translate）
-   旋转（rotate）
-   缩放（scale）
-   倾斜（skew）
-   或者将多个转换组合（matrix）

这些都通过 transform 属性实现。

语法：

```css
transform: 函数1 函数2...;
```

## transform 常见 2D 函数

将元素从其原始位置移动。

-   translate(x, y)：沿 X 轴和 Y 轴移动。x 为正值向右，y 为正值向下。
-   translateX(x)：仅沿 X 轴移动。
-   translateY(y)：仅沿 Y 轴移动。

应用场景：创建滑动效果、微调位置、实现相对定位的替代方案（不脱离文档流）。

```css
.box {
    transform: translate(50px, 100px); /* 向右 50px，向下 100px */
}
.box-x {
    transform: translateX(-20px); /* 向左 20px */
}
```

## scale() —— 缩放

改变元素的大小。

-   scale(sx, sy)：sx 控制宽度缩放，sy 控制高度缩放。如果只提供一个值，则宽高同时缩放。
-   scaleX(sx)：仅缩放宽度。
-   scaleY(sy)：仅缩放高度。

值：1 为原始大小，2 为两倍大，0.5 为一半大，0 则元素尺寸为 0（但 DOM 节点仍在）。负值会进行镜像翻转。

应用场景：悬停放大效果、视觉强调、创建镜像。

```css
.box {
    transform: scale(1.5); /* 放大到 1.5 倍 */
}
.box-flip {
    transform: scaleX(-1); /* 水平镜像翻转 */
}
```

## rotate() —— 旋转

围绕元素的变换原点（默认是中心点）旋转元素。

rotate(angle)：angle 为旋转角度，单位为 deg（度）。正值顺时针，负值逆时针。

应用场景：创建箭头方向、制作徽章倾斜效果、加载动画。

```css
.box {
    transform: rotate(30deg); /* 顺时针旋转 30 度 */
}
.box-reverse {
    transform: rotate(-90deg); /* 逆时针旋转 90 度 */
}
```

## skew() —— 倾斜（切变）

沿 X 和/或 Y 轴倾斜元素，使其呈现“平行四边形”或“菱形”效果。

-   skew(ax, ay)：ax 沿 X 轴倾斜角度，ay 沿 Y 轴倾斜角度。
-   skewX(ax)：仅沿 X 轴倾斜。
-   skewY(ay)：仅沿 Y 轴倾斜。

应用场景：创建倾斜的标签、模拟透视效果、动态视觉效果。

```css
.box {
    transform: skew(20deg, 10deg); /* X轴倾斜20度，Y轴倾斜10度 */
}
.box-x {
    transform: skewX(-15deg); /* 向左倾斜 15 度 */
}
```

## matrix() —— 矩阵转换（进阶）

等价于组合多种变换，如：

-   scale
-   skew
-   translate

应用场景：一般用于动画计算或复杂场景，日常用得少。

```css
transform: matrix(a, b, c, d, e, f);
```

## transform-origin（变换原点）

控制元素变换的基准点。默认是 50% 50%（元素的中心）。

语法：

```css
transform-origin: x-axis y-axis [z-axis]; /* 2D中忽略 z-axis */
```

值：可以是长度（px）、百分比（%）或关键词（left, center, right, top, bottom）。

```css
.box {
    transform: rotate(45deg);
    transform-origin: top left; /* 围绕左上角旋转 */
}
```

改变 transform-origin 会让旋转、缩放等效果产生截然不同的视觉感受。

## 多重变换

可以在一个 transform 属性中按顺序组合多个函数。

```css
.box {
    transform: translate(50px, 50px) rotate(45deg) scale(1.2);
    /* 执行顺序：先缩放 -> 再旋转 -> 最后平移 */
}
```

注意顺序的重要性：`rotate(45deg) translate(50px)` 和 `translate(50px) rotate(45deg)` 的结果完全不同。前者是先旋转坐标轴再平移，后者是在原始坐标轴上平移后再旋转。

## 变换与布局（重要！）

应用 transform 的元素会触发以下效果：

-   视觉上移动/变形，但不会影响原始的文档流布局。周围的元素依然会按照它变换前的位置进行排列。
-   会创建一个新的层叠上下文和包含块（对于 position: fixed 的子元素，其“视口”会变成这个变换元素）。
-   性能优化：transform 和 opacity 的动画通常可以由 GPU 加速（通过 will-change: transform 可以提示浏览器），实现更流畅的动画。

## 注意事项（容易踩坑）

1. transform 不会影响周围布局（非占位移动）

    > 移动或旋转只是视觉效果，元素原来的占位不变。

2. transform 会创建新的层叠上下文（z-index 相关）

    > 比如移动的元素可能盖住别人。

3. translate 使用 % 时，相对的是元素自身宽高，而不是父元素

```css
/* 移动自身宽度的 50%。 */
transform: translateX(50%);
```

4. 多重变换顺序必须牢记
    > 从右到左执行
