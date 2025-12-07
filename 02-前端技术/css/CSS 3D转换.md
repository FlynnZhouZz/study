# CSS 3D 转换

CSS 3D 转换（3D Transform） 在二维平面的基础上增加了 Z 轴，让元素可以：

-   在 3D 空间移动（translateZ）
-   旋转（rotateX / rotateY / rotateZ）
-   缩放（scaleZ）
-   设置透视效果（perspective）
-   控制子元素是否保持 3D（transform-style: preserve-3d）

所有 3D 效果依赖于 transform 属性。

## 3D 坐标系统

CSS 中的 3D 坐标：

```text
X 轴：横向 → 右为正
Y 轴：纵向 → 下为正
Z 轴：垂直屏幕 → 朝向你为正（往外）
```

## 3D 透视：perspective（非常重要）

没有 perspective（透视），3D 就看不出来。

### 作为父容器属性

```css
.parent {
    perspective: 800px;
}
```

含义：

-   值越小 → 透视越强 → 3D 变形越夸张
-   值越大 → 透视越弱 → 更接近平面

### 单独作用于元素（function）

```css
transform: perspective(800px) rotateY(60deg);
```

和父容器 perspective 效果略有不同，不如父容器自然，通常不推荐。

### 设置透视视点：perspective-origin

```css
.parent {
    perspective-origin: center top;
}
```

决定观察者视线方向。

## 常用 3D 转换函数

### translateZ() —— 沿 Z 轴平移

```css
transform: translateZ(100px);
```

-   正值 → 元素向你“弹出来”
-   负值 → 元素“缩进去”

### translate3d(x, y, z)

三维平移

```css
transform: translate3d(50px, 0, 100px);
```

### rotateX() —— 绕 X 轴旋转（上下翻）

```css
transform: rotateX(60deg);
```

-   正值：顶部向屏幕里翻
-   负值：底部向屏幕里翻

### rotateY() —— 绕 Y 轴旋转（左右翻）

```css
transform: rotateY(60deg);
```

-   正值：右侧向屏幕里翻
-   负值：左侧向屏幕里翻

### rotateZ() —— 绕 Z 轴旋转

等同 2D rotate。

### rotate3d(x, y, z, angle)

绕任意轴旋转

```css
transform: rotate3d(1, 1, 0, 45deg);
```

### scaleZ() 与 scale3d()

```css
transform: scaleZ(2);
transform: scale3d(1, 1, 2);
```

由于 Z 轴缩放不直观，较少单独使用。

## 控制子元素 3D 行为

### transform-style

```css
.parent {
    transform-style: preserve-3d;
}
```

含义：

-   flat（默认） → 子元素转换会被“投影”成 2D
-   preserve-3d → 保留子元素的真实 3D 空间关系

要做 3D 立方体、3D 翻转卡片，必须加 preserve-3d。

### backface-visibility（隐藏元素背面）

```css
.box {
    backface-visibility: hidden;
}
```

用于卡片翻转时隐藏反面镜像。

## 注意事项（非常重要）

1. 没有 perspective 就没有真实 3D 效果

    > rotateX/rotateY 会看起来像扁平变形。

2. transform-style 只对子元素有效

    > 父元素自身的 transform-style 不影响自身。

3. 多重 3D 变换注意顺序
   依然是 从右到左 执行：

```css
transform: translateZ(100px) rotateY(45deg);
```

4. translateZ 与 scale 有时会一起使用以制造深度感

5. Safari 与部分移动端需要加前缀（旧代码）

```css
-webkit-transform-style: preserve-3d;
```
