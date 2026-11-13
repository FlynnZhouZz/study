# CSS 媒体查询

CSS 媒体查询是现代响应式网页设计的核心技术。它允许你根据设备的特性（如屏幕尺寸、分辨率、方向等）应用不同的 CSS 样式。

## 媒体查询基础

### 基本语法：

```css
@media media-type and (media-feature) {
    /* CSS 规则 */
}
```

### 在 HTML 中链接：

```html
<link rel="stylesheet" media="(max-width: 768px)" href="mobile.css" />
```

### 在 CSS 文件中：

```css
/* 基础样式 */
body {
    font-size: 16px;
}

/* 媒体查询 */
@media (max-width: 768px) {
    body {
        font-size: 14px;
    }
}
```

## 常用媒体特性

### 1. 视口尺寸

```css
/* 移动端优先 - 从小屏幕开始 */
@media (min-width: 576px) {
    /* ≥576px */
}
@media (min-width: 768px) {
    /* ≥768px - 平板 */
}
@media (min-width: 992px) {
    /* ≥992px - 小桌面 */
}
@media (min-width: 1200px) {
    /* ≥1200px - 大桌面 */
}

/* 桌面端优先 - 从大屏幕开始 */
@media (max-width: 1199px) {
    /* ≤1199px */
}
@media (max-width: 991px) {
    /* ≤991px */
}
@media (max-width: 767px) {
    /* ≤767px - 手机 */
}
```

### 2. 设备方向

```css
/* 横屏模式 */
@media (orientation: landscape) {
    .container {
        flex-direction: row;
    }
}

/* 竖屏模式 */
@media (orientation: portrait) {
    .container {
        flex-direction: column;
    }
}
```

### 3. 分辨率与像素比

```css
/* 高分辨率屏幕 (Retina) */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
    .logo {
        background-image: url("logo@2x.png");
        background-size: contain;
    }
}

/* 超高分辨率 */
@media (-webkit-min-device-pixel-ratio: 3), (min-resolution: 288dpi) {
    .logo {
        background-image: url("logo@3x.png");
    }
}
```

### 4. 其他常用特性

```css
/* 悬停支持 */
@media (hover: hover) {
    .button:hover {
        background-color: #f0f0f0;
    }
}

/* 指针设备精度 */
@media (pointer: coarse) {
    /* 触摸设备 */
}
@media (pointer: fine) {
    /* 鼠标设备 */
}

/* 减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
    body {
        background: #1a1a1a;
        color: #ffffff;
    }
}
```

## 响应式断点系统

### 1. 通用断点系统

```css
/* 超小设备 (手机, <576px) - 移动端优先基础样式 */
.container {
    width: 100%;
    padding: 15px;
}

/* 小设备 (≥576px) */
@media (min-width: 576px) {
    .container {
        max-width: 540px;
        margin: 0 auto;
    }
}

/* 中等设备 (≥768px) */
@media (min-width: 768px) {
    .container {
        max-width: 720px;
        padding: 30px;
    }

    .sidebar {
        display: block;
    }
}

/* 大设备 (≥992px) */
@media (min-width: 992px) {
    .container {
        max-width: 960px;
    }

    .main-content {
        display: grid;
        grid-template-columns: 1fr 300px;
        gap: 30px;
    }
}

/* 超大设备 (≥1200px) */
@media (min-width: 1200px) {
    .container {
        max-width: 1140px;
    }
}
```

### 2. 实用断点变量

```css
/* CSS 自定义属性定义断点 */
:root {
    --breakpoint-xs: 0;
    --breakpoint-sm: 576px;
    --breakpoint-md: 768px;
    --breakpoint-lg: 992px;
    --breakpoint-xl: 1200px;
    --breakpoint-xxl: 1400px;
}

/* 使用变量 */
@media (min-width: var(--breakpoint-md)) {
    .grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
```

## 嵌套媒体查询（Sass/Less 支持）

-   Sass/Less 可直接嵌套
-   结构更清晰，便于维护

```css
.container {
    display: flex;

    @media (max-width: 768px) {
        flex-direction: column;
    }
}
```

## 实用布局示例

### 示例 1：响应式导航

```css
/* 移动端导航 */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
}

.mobile-menu-btn {
    display: block;
}

.nav-menu {
    position: fixed;
    top: 0;
    left: -100%;
    width: 80%;
    height: 100vh;
    background: white;
    transition: left 0.3s ease;
}

/* 平板及以上 */
@media (min-width: 768px) {
    .mobile-menu-btn {
        display: none;
    }

    .nav-menu {
        position: static;
        width: auto;
        height: auto;
        background: transparent;
        display: flex;
        gap: 2rem;
    }
}
```

### 示例 2：响应式网格布局

```css
/* 移动端：单列 */
.grid {
    display: grid;
    gap: 1rem;
    grid-template-columns: 1fr;
}

/* 平板：2列 */
@media (min-width: 768px) {
    .grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
    }
}

/* 桌面：3列 */
@media (min-width: 992px) {
    .grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
    }
}

/* 大桌面：4列 */
@media (min-width: 1200px) {
    .grid {
        grid-template-columns: repeat(4, 1fr);
    }
}
```

### 示例 3：响应式字体大小

```css
/* 流体排版 */
html {
    font-size: 14px;
}

/* 小屏幕 */
@media (min-width: 576px) {
    html {
        font-size: 15px;
    }
}

/* 中等屏幕 */
@media (min-width: 768px) {
    html {
        font-size: 16px;
    }
}

/* 大屏幕 */
@media (min-width: 1200px) {
    html {
        font-size: 18px;
    }
}

/* 使用 clamp() 实现更流畅的字体缩放 */
.heading {
    font-size: clamp(1.5rem, 4vw, 3rem);
}

.subheading {
    font-size: clamp(1rem, 2.5vw, 1.5rem);
}
```

### 示例 4：响应式表格

```css
/* 默认样式 */
.data-table {
    width: 100%;
    border-collapse: collapse;
}

/* 小屏幕上转换为卡片布局 */
@media (max-width: 767px) {
    .data-table,
    .data-table thead,
    .data-table tbody,
    .data-table th,
    .data-table td,
    .data-table tr {
        display: block;
    }

    .data-table thead {
        display: none;
    }

    .data-table tr {
        margin-bottom: 1rem;
        border: 1px solid #ddd;
        padding: 1rem;
    }

    .data-table td {
        border: none;
        position: relative;
        padding-left: 50%;
    }

    .data-table td::before {
        content: attr(data-label);
        position: absolute;
        left: 1rem;
        width: 45%;
        font-weight: bold;
    }
}
```

## 高级媒体查询技巧

### 1. 复杂条件组合

```css
/* 横屏平板 */
@media (min-width: 768px) and (orientation: landscape) {
    .dashboard {
        grid-template-columns: 250px 1fr 200px;
    }
}

/* 大屏幕且支持悬停 */
@media (min-width: 1024px) and (hover: hover) {
    .tooltip:hover::after {
        content: attr(data-tooltip);
        /* 显示工具提示 */
    }
}

/* 打印且纵向 */
@media print and (orientation: portrait) {
    .resume {
        font-size: 12pt;
    }
}
```

### 2. 范围查询（现代语法）

```css
/* 传统方式 */
@media (min-width: 768px) and (max-width: 1199px) {
    /* 768px 到 1199px */
}

/* 现代范围语法 */
@media (768px <= width <= 1199px) {
    .container {
        max-width: 992px;
    }
}

/* 更简洁的范围查询 */
@media (width < 768px) {
    .mobile-layout {
        display: block;
    }
}

@media (768px <= width < 1200px) {
    .tablet-layout {
        display: block;
    }
}

@media (width >= 1200px) {
    .desktop-layout {
        display: block;
    }
}
```

### 3. 深色模式支持

```css
/* 浅色模式（默认） */
:root {
    --bg-color: #ffffff;
    --text-color: #333333;
    --primary-color: #007bff;
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-color: #1a1a1a;
        --text-color: #ffffff;
        --primary-color: #4dabf7;
    }
}

/* 应用变量 */
body {
    background: var(--bg-color);
    color: var(--text-color);
}

.button {
    background: var(--primary-color);
}
```

### 4. 可访问性媒体查询

```css
/* 减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}

/* 高对比度模式 */
@media (prefers-contrast: high) {
    .button {
        border: 2px solid currentColor;
    }

    .link {
        text-decoration: underline;
    }
}

/* 减少透明度偏好 */
@media (prefers-reduced-transparency: reduce) {
    .glass-effect {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: none;
    }
}
```

## 性能优化最佳实践

### 1. 组织媒体查询

```css
/* 推荐：按组件组织 */
.card {
    /* 基础样式 */
    padding: 1rem;
    margin: 1rem 0;
}

@media (min-width: 768px) {
    .card {
        padding: 1.5rem;
        margin: 1.5rem;
    }
}

.button {
    /* 按钮基础样式 */
    padding: 0.5rem 1rem;
}

@media (min-width: 768px) {
    .button {
        padding: 0.75rem 1.5rem;
    }
}
```

### 2. 避免重复断点

```css
/* 不推荐：重复断点 */
@media (min-width: 768px) {
    .header {
        padding: 2rem;
    }
}

@media (min-width: 768px) {
    .footer {
        margin: 2rem;
    }
}

/* 推荐：合并媒体查询 */
@media (min-width: 768px) {
    .header {
        padding: 2rem;
    }
    .footer {
        margin: 2rem;
    }
}
```

### 3. 使用现代单位

```css
/* 推荐：使用相对单位和容器查询 */
.container {
    container-type: inline-size;
}

@container (min-width: 400px) {
    .card {
        display: grid;
        grid-template-columns: 1fr 2fr;
    }
}
```
