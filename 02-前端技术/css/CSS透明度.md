# CSS 透明度

透明度（`opacity`） 表示元素的 不透明程度，取值范围 0~1：

-   0 → 完全透明
-   1 → 完全不透明（默认值）
-   小数 → 半透明

## `opacity` 属性

### 基本用法

opacity 属性设置元素的整体透明度，包括其所有内容（文本、背景、边框等）。

```css
.element {
    opacity: 0.5; /* 50% 透明度 */
}
```

## RGBA 和 HSLA 颜色

### 1. RGBA - 红绿蓝+透明度

```css
.element {
    background-color: rgba(255, 0, 0, 0.5); /* 半透明红色背景 */
    color: rgba(0, 0, 0, 0.8); /* 80% 不透明黑色文字 */
    border: 2px solid rgba(0, 0, 0, 0.3); /* 透明边框 */
}
```

### 2. HSLA - 色相饱和度亮度+透明度

```css
.element {
    background-color: hsla(120, 100%, 50%, 0.5); /* 半透明绿色 */
    color: hsla(0, 0%, 0%, 0.8); /* 80% 不透明黑色 */
}
```

### RGBA/HSLA vs Opacity 对比：

```html
<div class="comparison">
    <div class="box opacity-box">
        <p>使用 opacity</p>
        <span>文字也透明</span>
    </div>
    <div class="box rgba-box">
        <p>使用 RGBA</p>
        <span>只有背景透明</span>
    </div>
</div>
```

```css
.comparison {
    display: flex;
    gap: 20px;
    padding: 20px;
    background: #f8f9fa;
}

.box {
    width: 200px;
    height: 150px;
    padding: 20px;
    border: 2px solid #333;
    border-radius: 8px;
}

.opacity-box {
    opacity: 0.5; /* 整个元素包括文字都透明 */
    background: #e74c3c;
}

.rgba-box {
    background: rgba(231, 76, 60, 0.5); /* 只有背景透明 */
    border: 2px solid rgba(0, 0, 0, 0.3); /* 边框也透明 */
}
/* 文字保持不透明 */
.rgba-box p,
.rgba-box span {
    color: #000; /* 文字完全不透明 */
}
```

## 透明度与过渡动画

```css
.fade {
    opacity: 0;
    transition: opacity 0.3s;
}

.fade.show {
    opacity: 1;
}
```

## 实用场景示例

### 场景 1：图片悬停效果

```html
<div class="image-container">
    <img src="landscape.jpg" alt="风景" />
    <div class="image-overlay">
        <h3>美丽的风景</h3>
    </div>
</div>
```

```css
.image-container {
    position: relative;
    display: inline-block;
    overflow: hidden;
    border-radius: 8px;
}

.image-container img {
    width: 300px;
    height: 200px;
    object-fit: cover;
    transition: opacity 0.3s ease;
}

.image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.image-container:hover img {
    opacity: 0.8;
}

.image-container:hover .image-overlay {
    opacity: 1;
}
```

### 场景 2：模态框背景

```css
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* 半透明黑色遮罩 */
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    max-width: 500px;
    width: 90%;
}
```

### 场景 3：渐变透明导航栏

```css
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95); /* 半透明白色 */
    backdrop-filter: blur(10px); /* 毛玻璃效果 */
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1000;
    transition: background-color 0.3s ease;
}

.navbar.scrolled {
    background: rgba(255, 255, 255, 0.98); /* 滚动时更不透明 */
}
```

### 场景 4：透明按钮

```css
.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary {
    background: rgba(52, 152, 219, 0.9);
    color: white;
}

.btn-primary:hover {
    background: rgba(52, 152, 219, 1);
    transform: translateY(-2px);
}

.btn-outline {
    background: transparent;
    border: 2px solid rgba(52, 152, 219, 0.7);
    color: #3498db;
}

.btn-outline:hover {
    background: rgba(52, 152, 219, 0.1);
    border-color: rgba(52, 152, 219, 1);
}
```

### 场景 5：卡片阴影效果

```css
.card {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.card:hover {
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15), 0 5px 10px rgba(0, 0, 0, 0.1);
}
```

### 场景 6：多层透明度叠加

```css
.layered-transparency {
    position: relative;
    width: 300px;
    height: 200px;
}

.layer-1 {
    position: absolute;
    width: 100%;
    height: 100%;
    background: rgba(255, 0, 0, 0.5); /* 红色层 */
}

.layer-2 {
    position: absolute;
    width: 80%;
    height: 80%;
    top: 10%;
    left: 10%;
    background: rgba(0, 255, 0, 0.5); /* 绿色层 */
}

.layer-3 {
    position: absolute;
    width: 60%;
    height: 60%;
    top: 20%;
    left: 20%;
    background: rgba(0, 0, 255, 0.5); /* 蓝色层 */
}
```

### 场景 7：渐变透明度

```css
.gradient-transparency {
    width: 100%;
    height: 200px;
    background: linear-gradient(
        to right,
        rgba(255, 0, 0, 1),
        /* 不透明红色 */ rgba(255, 0, 0, 0.5),
        /* 半透明红色 */ rgba(255, 0, 0, 0) /* 完全透明 */
    );
}

.fade-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100px;
    background: linear-gradient(to top, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0));
}
```

### 场景 8：动画透明度

```css
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-element {
    animation: fadeIn 0.6s ease-out;
}

.pulsing-element {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%,
    100% {
        opacity: 1;
    }
    50% {
        opacity: 0.5;
    }
}
```

## 浏览器兼容性和性能

### 兼容性处理

```css
.transparent-element {
    /* 旧版浏览器备用 */
    background: rgb(255, 0, 0);
    /* 现代浏览器 */
    background: rgba(255, 0, 0, 0.5);

    /* IE 8及以下 */
    -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=50)";
    /* IE 5-7 */
    filter: alpha(opacity=50);
}
```

### 性能考虑

```css
/* 高性能 - 使用 transform 和 opacity */
.performance-good {
    opacity: 0.5;
    transform: translateZ(0); /* 触发硬件加速 */
}

/* 低性能 - 可能引起重排 */
.performance-bad {
    opacity: 0.5;
    margin-left: 10px; /* 可能引起布局重排 */
}
```
