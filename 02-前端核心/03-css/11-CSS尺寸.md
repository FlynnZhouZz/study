# CSS 尺寸

CSS 尺寸（Dimension）属性用于控制元素的宽度和高度。这些是布局中最基础也是最重要的属性。

常见属性包括：

-   width / height
-   min-width / max-width
-   min-height / max-height
-   line-height（行高）
-   box-sizing（影响尺寸计算）
-   各种单位（px, %, vw, vh, em 等）

## 基础尺寸属性

### 1. width - 宽度

```css
div {
    width: 300px; /* 固定像素值 */
    width: 50%; /* 相对于父元素宽度 */
    width: auto; /* 默认值，浏览器计算宽度 */
    width: 100vw; /* 相对于视口宽度 */
}
```

### 2. height - 高度

```css
div {
    height: 200px; /* 固定像素值 */
    height: 50%; /* 相对于父元素高度 */
    height: auto; /* 默认值，由内容决定 */
    height: 100vh; /* 相对于视口高度 */
}
```

### 3. min-width / max-width - 最小/最大宽度

设置元素宽度的限制范围。

```css
.container {
    min-width: 300px; /* 最小宽度300px */
    max-width: 1200px; /* 最大宽度1200px */
    width: 90%; /* 在300px-1200px之间自适应 */
}

.responsive-image {
    max-width: 100%; /* 图片最大不超过容器宽度 */
    height: auto; /* 保持宽高比 */
}
```

### 4. min-height / max-height - 最小/最大高度

设置元素高度的限制范围。

```css
.card {
    min-height: 200px; /* 最小高度200px */
    max-height: 500px; /* 最大高度500px */
    height: auto; /* 在200px-500px之间自适应 */
}

.scrollable {
    max-height: 300px;
    overflow-y: auto; /* 内容超出时显示滚动条 */
}
```

## 尺寸单位详解

### 1. 绝对单位

```css
.pixel {
    width: 300px; /* 像素 - 最常用 */
}

.centimeter {
    width: 10cm; /* 厘米 - 打印样式常用 */
}

.millimeter {
    width: 100mm; /* 毫米 */
}

.inch {
    width: 4in; /* 英寸 (1in = 96px = 2.54cm) */
}
```

### 2. 相对单位（更灵活、响应式）

```css
/* 相对于字体大小 */
.em-unit {
    font-size: 16px;
    width: 10em; /* 10 × 16px = 160px */
    padding: 1.5em; /* 1.5 × 16px = 24px */
}

html {
    font-size: 16px;
}
.rem-unit {
    width: 10rem; /* 10 × 根元素字体大小(通常16px) = 160px */
}

/* 相对于视口 */
.viewport-unit {
    width: 50vw; /* 视口宽度的50% */
    height: 75vh; /* 视口高度的75% */
    min-width: 50vmin; /* 视口较小尺寸的50% */
    max-height: 80vmax; /* 视口较大尺寸的80% */
}

/* 相对于父元素 */
.percent-unit {
    width: 80%; /* 父元素宽度的80% */
    height: 50%; /* 父元素高度的50% */
}
```

### 3. 特殊单位

```css
/* 包含内边距和边框 */
.border-box {
    box-sizing: border-box;
    width: 300px; /* 总宽度为300px（包含padding和border）*/
    padding: 20px;
    border: 5px solid #333;
}

/* 自动计算 */
.auto-size {
    width: auto; /* 浏览器自动计算 */
    height: auto; /* 由内容决定 */
}

/* 适应内容 */
.fit-content {
    width: fit-content; /* 宽度由内容决定，但不超过可用空间 */
    width: max-content; /* 宽度由内容决定，可能超出容器 */
    width: min-content; /* 最小可能的宽度 */
}
```

## 实用尺寸技巧

### 1. 响应式图片

```css
.responsive-img {
    max-width: 100%; /* 不超过容器宽度 */
    height: auto; /* 保持宽高比 */
    display: block; /* 消除底部间隙 */
}

/* 保持正方形 */
.square {
    width: 100%;
    height: 0;
    padding-bottom: 100%; /* 通过padding创建高度 */
    position: relative;
}

.square img {
    position: absolute;
    width: 100%;
    height: 100%;
    object-fit: cover; /* 填充整个容器 */
}
```

### 2. 全屏布局

```css
.fullscreen {
    width: 100vw; /* 视口宽度 */
    height: 100vh; /* 视口高度 */
    margin: 0; /* 移除默认边距 */
}

.hero-section {
    width: 100%;
    min-height: 100vh; /* 至少满屏高度 */
    display: flex;
    align-items: center;
    justify-content: center;
}
```

### 3. 流式容器

```css
.container {
    width: 90%; /* 小屏幕上留边距 */
    max-width: 1200px; /* 大屏幕上限制最大宽度 */
    margin: 0 auto; /* 水平居中 */
}

/* 使用 clamp() 实现智能尺寸 */
.fluid-text {
    width: clamp(300px, 80%, 800px); /* 最小300px，首选80%，最大800px */
    font-size: clamp(1rem, 2.5vw, 2rem); /* 响应式字体大小 */
}
```

### 4. 网格系统

```css
.grid-container {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.grid-item {
    min-height: 200px; /* 统一最小高度 */
    height: auto; /* 内容多时自动扩展 */
}
```

### 5. 表单元素尺寸

```css
.form-group {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
}

.input-field {
    width: 100%; /* 填满父容器 */
    height: 48px; /* 统一的触摸友好高度 */
    padding: 0 16px;
    box-sizing: border-box;
}

.textarea {
    width: 100%;
    min-height: 120px; /* 最小高度 */
    max-height: 300px; /* 最大高度 */
    resize: vertical; /* 允许垂直调整 */
}
```

## 尺寸计算

### 1. calc() 函数

```css
.column {
    width: calc(33.333% - 20px); /* 三列布局，考虑间距 */
    margin: 10px;
}

.hero {
    height: calc(100vh - 80px); /* 视口高度减去头部高度 */
}

.responsive {
    width: calc(100% - 2rem); /* 100%宽度减去左右内边距 */
    padding: 0 1rem;
}
```

### 2. 复杂计算示例

```css
/* 黄金比例布局 */
.golden-ratio {
    width: 61.8%; /* 黄金比例 */
}

.golden-ratio-sidebar {
    width: 38.2%; /* 互补比例 */
}

/* 精确的网格系统 */
.grid-item {
    width: calc((100% - 60px) / 4); /* 4列，总间隙60px */
    margin: 10px;
}
```

## 浏览器兼容性与最佳实践

### 1. 盒模型设置

```css
/* 现代最佳实践 */
* {
    box-sizing: border-box; /* 宽度包含padding和border */
}

html {
    box-sizing: border-box;
}

*,
*::before,
*::after {
    box-sizing: inherit; /* 更精确的继承 */
}
```

### 2. 响应式断点

```css
.mobile-first {
    width: 100%; /* 移动端优先 */
    padding: 1rem;
}

/* 平板 */
@media (min-width: 768px) {
    .mobile-first {
        width: 80%;
        max-width: 600px;
        margin: 0 auto;
    }
}

/* 桌面 */
@media (min-width: 1024px) {
    .mobile-first {
        width: 70%;
        max-width: 800px;
    }
}
```

### 3. 安全尺寸考虑

```css
.safe-area {
    /* 考虑现代设备的刘海屏和安全区域 */
    width: 100%;
    padding-left: env(safe-area-inset-left);
    padding-right: env(safe-area-inset-right);

    /* 最小触摸目标尺寸 */
    min-width: 44px;
    min-height: 44px;
}
```

## 常见问题与解决方案

### 问题 1：百分比高度不生效

```css
/* 问题：父元素没有明确高度 */
.parent {
    height: 500px; /* 父元素必须有明确高度 */
}

.child {
    height: 50%; /* 现在50%才会生效 */
}

/* 替代方案：使用视口单位或Flexbox */
.modern-parent {
    min-height: 100vh; /* 至少满屏高度 */
    display: flex;
}
```

### 问题 2：内联元素的尺寸

```css
/* 内联元素无法设置宽高 */
span {
    display: inline-block; /* 改为inline-block或block */
    width: 200px;
    height: 100px;
}
```

> ps: 不建议使用 `inline-block`元素，会出现异响不到的布局

### 问题 3：表格单元格尺寸

```css
table {
    width: 100%; /* 表格宽度 */
    table-layout: fixed; /* 固定布局，列宽均匀分布 */
}

td,
th {
    width: 25%; /* 每列25%宽度 */
    height: 50px; /* 统一行高 */
}
```
