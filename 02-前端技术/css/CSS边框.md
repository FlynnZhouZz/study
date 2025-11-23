# CSS 边框

CSS 边框（Border）是盒子模型的重要组成部分，用于围绕元素的内容和内边距绘制线条。边框不仅用于装饰，还能提供视觉分隔和焦点指示。

## 边框的基本属性

### 1. `border-width` - 边框宽度

设置边框的粗细。

常用值： `thin` | `medium` | `thick` | `<length>`（如 `2px`, `0.5em`）

```css
div {
    border-width: 2px; /* 所有边2px */
    border-width: 1px 3px; /* 上下1px，左右3px */
    border-width: 1px 2px 3px 4px; /* 上1px、右2px、下3px、左4px（顺时针）*/

    /* 也可以分别设置 */
    border-top-width: 5px;
    border-right-width: 3px;
    border-bottom-width: 1px;
    border-left-width: 3px;
}
```

### 2. `border-style` - 边框样式

设置边框的线条样式。

```css
div {
    border-style: solid; /* 实线 */
    border-style: dashed; /* 虚线 */
    border-style: dotted; /* 点线 */
    border-style: double; /* 双实线 */
    border-style: groove; /* 3D凹槽 */
    border-style: ridge; /* 3D凸槽 */
    border-style: inset; /* 3D内嵌 */
    border-style: outset; /* 3D外凸 */
    border-style: none; /* 无边框 */
    border-style: hidden; /* 隐藏边框 */
}
```

### 3. `border-color` - 边框颜色

设置边框的颜色。

```css
div {
    border-color: red; /* 所有边红色 */
    border-color: #ccc #333; /* 上下#ccc，左右#333 */
    border-color: red green blue yellow; /* 上红、右绿、下蓝、左黄 */

    /* 也可以分别设置 */
    border-top-color: #ff0000;
    border-right-color: #00ff00;
}
```

透明边框技巧：

```css
div {
    border: 2px solid transparent; /* 透明边框，占位但不显示 */
    border: 2px solid rgba(0, 0, 0, 0.3); /* 半透明边框 */
}
```

### 4. `border-radius` - 边框圆角

创建圆角边框，是现代网页设计的关键属性。

```css
div {
    border-radius: 10px; /* 所有角10px圆角 */
    border-radius: 50%; /* 圆形（当元素宽高相等时）*/
    border-radius: 10px 20px; /* 左上右下10px，右上左下20px */
    border-radius: 10px 20px 30px 40px; /* 左上10px，右上20px，右下30px，左下40px */

    /* 分别设置每个角的水平和垂直半径 */
    border-radius: 10px 20px 30px 40px / 5px 10px 15px 20px;

    /* 也可以单独设置每个角 */
    border-top-left-radius: 15px;
    border-top-right-radius: 5px 10px; /* 水平半径 垂直半径 */
}
```

### 5. `border-image` - 边框图片

使用图像作为边框。

```css
div {
    border: 30px solid transparent;
    border-image: url("border.png") 30 round;
    /* 图片 切片 重复方式 */
}
```

### 6. `box-shadow` - 盒子阴影（虽然不是 border 属性，但常一起使用）

为元素添加阴影效果。

```css
div {
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    /* 水平偏移(x偏移) 垂直偏移(y偏移) 模糊半径 颜色 */

    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.1); /* 多重阴影 */

    box-shadow: inset 0 0 10px #000; /* 内阴影 */
}
```

## 边框 实践示例

### 示例 1： 半透明边框

```css
border: 2px solid rgba(0, 0, 0, 0.3);
```

### 示例 2： 渐变边框（常用技巧）

```css
.gradient-border {
    border: 4px solid transparent;
    border-radius: 10px;
    background: linear-gradient(45deg, #f00, #00f) border-box;
}
```

### 示例 3： 基础按钮样式

```css
.btn {
    display: inline-block;
    padding: 10px 20px;
    border: 2px solid #3498db;
    border-radius: 5px;
    background-color: #3498db;
    color: white;
    text-decoration: none;
    transition: all 0.3s ease;
}

.btn:hover {
    background-color: #2980b9;
    border-color: #2980b9;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.btn-outline {
    background-color: transparent;
    color: #3498db;
}

.btn-outline:hover {
    background-color: #3498db;
    color: white;
}
```

### 示例 4： 卡片设计（内外阴影）

```css
.card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease;
}

.card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    border-color: #3498db;
}

.card-header {
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 15px;
    margin-bottom: 15px;
}
```

### 示例 5：头像圆形效果

```css
.avatar {
    width: 100px;
    height: 100px;
    border: 3px solid white;
    border-radius: 50%;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    object-fit: cover; /* 确保图片按比例填充 */
}

.avatar-frame {
    border: 5px solid #3498db;
    border-radius: 50%;
    padding: 5px;
    display: inline-block;
    background: white;
}
```

### 示例 6：输入框焦点状态

```css
.input-field {
    width: 100%;
    padding: 10px;
    border: 2px solid #ddd;
    border-radius: 4px;
    transition: border-color 0.3s ease;
}

.input-field:focus {
    outline: none; /* 移除默认焦点轮廓 */
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
}
```

### 示例 7：特殊形状边框

```css
/* 对话气泡 */
.bubble {
    position: relative;
    background: #f0f0f0;
    border: 2px solid #ccc;
    border-radius: 10px;
    padding: 15px;
}

.bubble::after {
    content: "";
    position: absolute;
    bottom: -10px;
    left: 20px;
    border-width: 10px 10px 0;
    border-style: solid;
    border-color: #f0f0f0 transparent transparent;
}

/* 三角形 */
.triangle {
    width: 0;
    height: 0;
    border-left: 20px solid transparent;
    border-right: 20px solid transparent;
    border-bottom: 30px solid #3498db;
}
```

## 边框与性能优化

### 1. 使用 transparent 预占位

```css
.btn {
    border: 2px solid transparent; /* 预占位置，避免布局抖动 */
}

.btn:hover {
    border-color: #3498db; /* 悬停时显示边框 */
}
```

### 2. 避免过度使用阴影和复杂边框

```css
/* 不推荐 - 性能较差 */
.expensive {
    box-shadow: 0 0 20px 5px rgba(0, 0, 0, 0.3);
    border-image: url("complex-pattern.png") 30 round;
}

/* 推荐 - 性能较好 */
.optimized {
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    border: 1px solid #e0e0e0;
}
```
