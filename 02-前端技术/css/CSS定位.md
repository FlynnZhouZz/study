# CSS 定位

CSS `position` 用于控制元素在页面中的 位置定位方式。

CSS 中有 5 种定位方式：

-   `static`（默认）
-   `relative`（相对定位）
-   `absolute`（绝对定位）
-   `fixed`（固定定位）
-   `sticky`（粘性定位）

## 五种定位方式详解

### 1. `static` - 静态定位（默认值）

元素遵循正常的文档流，忽略 `top, right, bottom, left, z-index` 属性。

特点：

-   元素在正常流中定位
-   不能使用偏移属性
-   不能使用 `z-index`

```css
.box {
    position: static; /* 默认值，可以不写 */
    top: 100px; /* 无效！ */
    left: 50px; /* 无效！ */
}
```

### 2. `relative` - 相对定位

元素相对于自身原本的位置进行偏移。

特点：

-   相对于自身原位置偏移
-   原位置仍被保留，不影响其他元素布局
-   可以使用 `z-index`

```html
<div class="container">
    <div class="box box1">Box 1</div>
    <div class="box box2">Box 2 - 相对定位</div>
    <div class="box box3">Box 3</div>
</div>
```

```css
.box {
    width: 100px;
    height: 60px;
    background: lightblue;
    margin: 10px;
}

.box2 {
    position: relative;
    top: 20px; /* 从原位置向下移动20px */
    left: 30px; /* 从原位置向右移动30px */
    background: lightcoral;
}
```

### 3. `absolute` - 绝对定位

元素相对于最近的已定位祖先元素（非 `static`）进行定位，如果没有，则相对于初始包含块（通常是 `<html>`）。

特点：

-   脱离正常文档流，不占据空间
-   相对于最近的定位祖先元素
-   如果没有定位祖先，相对于 `<html>`
-   可以使用 `z-index`

```html
<div class="container" style="position: relative;">
    <div class="box box1">Box 1</div>
    <div class="box box2">Box 2 - 绝对定位</div>
    <div class="box box3">Box 3</div>
</div>
```

```css
.container {
    position: relative; /* 定位上下文 */
    width: 300px;
    height: 200px;
    border: 2px solid #333;
    background: #f0f0f0;
}

.box {
    width: 80px;
    height: 40px;
    background: lightblue;
}

.box2 {
    position: absolute;
    top: 20px; /* 距离容器顶部20px */
    right: 30px; /* 距离容器右侧30px */
    background: lightcoral;
}
```

### 4. `fixed` - 固定定位

元素相对于浏览器视口进行定位，即使页面滚动也不会移动。

特点：

-   相对于浏览器视口定位
-   滚动页面时元素位置固定
-   脱离正常文档流
-   常用于导航栏、悬浮按钮

```css
.fixed-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background: #333;
    color: white;
    z-index: 1000;
}

.chat-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: #007bff;
    color: white;
}
```

### 5. `sticky` - 粘性定位

元素根据正常文档流定位，然后在达到特定阈值时变为固定定位。

特点：

-   在正常流和固定定位之间切换
-   需要指定阈值（`top, right, bottom, left`）
-   相对于最近的滚动祖先

```css
.sticky-header {
    position: sticky;
    top: 0;
    background: white;
    padding: 1rem;
    border-bottom: 1px solid #ddd;
    z-index: 100;
}

.table-header {
    position: sticky;
    top: 60px; /* 在距离顶部60px处固定 */
    background: #f8f9fa;
}
```

## 定位的辅助属性

### 1. 偏移属性

```css
.element {
    position: absolute;
    top: 10px; /* 距离参考元素顶部10px */
    right: 20px; /* 距离参考元素右侧20px */
    bottom: 30px; /* 距离参考元素底部30px */
    left: 40px; /* 距离参考元素左侧40px */
}
```

### 2. `z-index` - 堆叠顺序

控制定位元素的堆叠顺序（仅对定位元素有效）。

```css
.modal {
    position: fixed;
    z-index: 1000; /* 数值越大，越在上面 */
}

.overlay {
    position: fixed;
    z-index: 999; /* 在modal下面 */
}
```

## 实用场景与示例

### 场景 1：居中定位

```css
/* 方法1：绝对定位 + transform */
.center-absolute {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

/* 方法2：绝对定位 + margin */
.center-margin {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    margin: auto;
    width: 200px;
    height: 100px;
}

/* 方法3：Flexbox（现代推荐）*/
.flex-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
```

### 场景 2：下拉菜单

```css
.dropdown {
    position: relative;
    display: inline-block;
}

.dropdown-menu {
    position: absolute;
    top: 100%; /* 在父元素下方 */
    left: 0;
    min-width: 150px;
    background: white;
    border: 1px solid #ccc;
    display: none;
}

.dropdown:hover .dropdown-menu {
    display: block;
}
```

### 场景 3：模态框

```css
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1000;
}

.modal-content {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 2rem;
    border-radius: 8px;
    z-index: 1001;
}
```

### 场景 4：粘性表格头

```css
.table-container {
    height: 400px;
    overflow-y: auto;
}

table {
    width: 100%;
}

th {
    position: sticky;
    top: 0;
    background: #f8f9fa;
    z-index: 10;
}
```

### 场景 5：浮动操作按钮

```css
.fab {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: #007bff;
    color: white;
    border: none;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    cursor: pointer;
}
```

### 场景 6：进度指示器

```css
.progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: #007bff;
    transform-origin: left;
    animation: progress 2s linear infinite;
}

@keyframes progress {
    0% {
        transform: scaleX(0);
    }
    100% {
        transform: scaleX(1);
    }
}
```

## 定位上下文与层叠上下文

### 1. 定位上下文

```css
.container {
    position: relative; /* 创建定位上下文 */
}

.child {
    position: absolute; /* 相对于.container定位 */
    top: 10px;
    left: 10px;
}
```

### 2. 层叠上下文

```css
.parent {
    position: relative;
    z-index: 1; /* 创建层叠上下文 */
}

.child {
    position: absolute;
    z-index: 100; /* 只在父元素的层叠上下文中生效 */
}
```

## 常见问题与解决方案

### 问题 1：绝对定位元素超出容器

```css
.container {
    position: relative;
    overflow: hidden; /* 隐藏超出部分 */
}

.absolute-child {
    position: absolute;
    /* 可能超出容器 */
}
```

### 问题 2：固定定位在移动端的怪异行为

```css
.fixed-mobile {
    position: fixed;
    /* 在iOS Safari中可能需要 */
    -webkit-overflow-scrolling: touch;
}
```

### 问题 3：粘性定位不生效

```css
.sticky-element {
    position: sticky;
    top: 0;
    /* 确保父容器有明确高度且可滚动 */
}

.parent-container {
    height: 400px; /* 必须有高度限制 */
    overflow-y: auto; /* 必须可滚动 */
}
```
