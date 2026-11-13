# CSS 网页布局

网页布局 = 控制 HTML 元素在页面中的排列方式

核心要点：

-   文档流：元素的默认排列顺序（标准文档流/非标准文档流）
-   盒子模型：元素宽高由 content + padding + border + margin 决定
-   定位方式：控制元素在页面的具体位置（static、relative、absolute、fixed、sticky）
-   对齐方式：水平/垂直对齐（text-align、vertical-align、flex/grid 对齐）

## 布局技术演进

| 时期 | 主要技术  | 特点                     |
| ---- | --------- | ------------------------ |
| 早期 | 表格布局  | 简单但语义差，已淘汰     |
| 传统 | 浮动+定位 | 灵活但复杂，需要清除浮动 |
| 现代 | Flexbox   | 一维布局，内容驱动       |
| 现代 | CSS Grid  | 二维布局，容器驱动       |
| 未来 | 容器查询  | 组件驱动响应式           |

## 传统布局方法

### 1. 浮动布局

```html
<div class="header">网站标题</div>
<div class="clearfix">
    <div class="sidebar">侧边栏</div>
    <div class="main-content">主要内容</div>
</div>
<div class="footer">页脚</div>
```

```css
/* 清除浮动 */
.clearfix::after {
    content: "";
    display: table;
    clear: both;
}

/* 两栏布局 */
.header {
    background: #333;
    color: white;
    padding: 20px;
}

.sidebar {
    float: left;
    width: 25%;
    background: #f4f4f4;
    padding: 20px;
}

.main-content {
    float: left;
    width: 75%;
    padding: 20px;
}

.footer {
    clear: both;
    background: #333;
    color: white;
    padding: 20px;
    text-align: center;
}
```

## Flexbox 布局（一维布局）

Flexbox 非常适合一维布局（行或列）。

### 1. 基础 Flex 布局

```html
<div class="flex-container">
    <div class="flex-item">项目 1</div>
    <div class="flex-item">项目 2</div>
    <div class="flex-item">项目 3</div>
</div>
```

```css
.flex-container {
    display: flex;
    gap: 20px; /* 项目间距 */
    padding: 20px;
    background: #f8f9fa;
}

.flex-item {
    flex: 1; /* 等分剩余空间 */
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

### 2. 常用 Flex 布局模式

导航栏：

```css
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: #333;
    color: white;
}

.nav-brand {
    font-size: 1.5rem;
    font-weight: bold;
}

.nav-menu {
    display: flex;
    gap: 2rem;
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-item a {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-item a:hover {
    color: #ffd700;
}
```

卡片布局：

```css
.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 20px;
}

.card {
    flex: 1 1 300px; /* 基础300px，可伸缩 */
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    transition: transform 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}
```

圣杯布局（Holy Grail）：

```css
.holy-grail {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.header {
    background: #2c3e50;
    color: white;
    padding: 1rem;
    text-align: center;
}

.main-content {
    display: flex;
    flex: 1;
}

.sidebar {
    width: 250px;
    background: #34495e;
    color: white;
    padding: 1rem;
}

.content {
    flex: 1;
    padding: 2rem;
    background: #ecf0f1;
}

.footer {
    background: #2c3e50;
    color: white;
    padding: 1rem;
    text-align: center;
}
```

## CSS Grid 布局（二维布局）

Grid 非常适合复杂的二维布局。

### 1. 基础 Grid 布局

```css
.grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* 3等分列 */
    grid-template-rows: auto;
    gap: 20px;
    padding: 20px;
}

.grid-item {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

### 2. 常用 Grid 布局模式

经典网页布局：

```html
<div class="page-layout">
    <header class="header">网站标题</header>
    <aside class="sidebar">侧边栏</aside>
    <main class="content">主要内容</main>
    <footer class="footer">版权信息</footer>
</div>
```

```css
.page-layout {
    display: grid;
    grid-template-areas:
        "header header header"
        "sidebar content content"
        "footer footer footer";
    grid-template-rows: auto 1fr auto;
    grid-template-columns: 250px 1fr;
    min-height: 100vh;
    gap: 0;
}

.header {
    grid-area: header;
    background: #2c3e50;
    color: white;
    padding: 1rem;
}

.sidebar {
    grid-area: sidebar;
    background: #34495e;
    color: white;
    padding: 1rem;
}

.content {
    grid-area: content;
    background: #ecf0f1;
    padding: 2rem;
}

.footer {
    grid-area: footer;
    background: #2c3e50;
    color: white;
    padding: 1rem;
    text-align: center;
}
```

瀑布流布局：

```css
.masonry-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    grid-auto-rows: 10px; /* 控制行高基数 */
    gap: 15px;
    padding: 20px;
}

.masonry-item {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
}

/* 不同高度的项目 */
.masonry-item:nth-child(2n) {
    grid-row: span 6; /* 占6行 */
}

.masonry-item:nth-child(3n) {
    grid-row: span 8; /* 占8行 */
}
```

仪表板布局：

```css
.dashboard {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: auto;
    gap: 20px;
    padding: 20px;
    background: #f5f6fa;
}

.widget {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.widget-large {
    grid-column: span 2;
    grid-row: span 2;
}

.widget-wide {
    grid-column: span 4;
}
```

## 响应式布局策略

### 1. 移动端优先

```css
/* 基础样式 - 移动端 */
.container {
    width: 100%;
    padding: 15px;
}

.grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 15px;
}

/* 平板 */
@media (min-width: 768px) {
    .container {
        max-width: 720px;
        margin: 0 auto;
        padding: 20px;
    }

    .grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }
}

/* 桌面 */
@media (min-width: 1024px) {
    .container {
        max-width: 1200px;
        padding: 30px;
    }

    .grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
    }
}

/* 大桌面 */
@media (min-width: 1440px) {
    .grid {
        grid-template-columns: repeat(4, 1fr);
    }
}
```

### 2. 混合布局技术

```css
.responsive-layout {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
}

/* 中等屏幕：Grid + Flexbox */
@media (min-width: 768px) {
    .responsive-layout {
        grid-template-columns: 250px 1fr;
    }

    .content-area {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
}

/* 大屏幕：复杂 Grid */
@media (min-width: 1024px) {
    .responsive-layout {
        grid-template-columns: 300px 1fr 200px;
        grid-template-areas:
            "sidebar main sidebar2"
            "sidebar main sidebar2";
    }
}
```

## 实用布局示例

### 示例 1：现代博客布局

```css
.blog-layout {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-areas:
        "header"
        "main"
        "sidebar"
        "footer";
    gap: 0;
    min-height: 100vh;
}

@media (min-width: 768px) {
    .blog-layout {
        grid-template-columns: 1fr 300px;
        grid-template-areas:
            "header header"
            "main sidebar"
            "footer footer";
    }
}

.blog-header {
    grid-area: header;
    background: #2c3e50;
    color: white;
    padding: 2rem;
}

.blog-main {
    grid-area: main;
    padding: 2rem;
    background: white;
}

.blog-sidebar {
    grid-area: sidebar;
    padding: 2rem;
    background: #f8f9fa;
}

.blog-footer {
    grid-area: footer;
    background: #34495e;
    color: white;
    padding: 2rem;
    text-align: center;
}
```

### 示例 2：电商产品网格

```css
.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
    padding: 20px;
}

.product-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.product-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
}

.product-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.product-info {
    padding: 20px;
}

.product-price {
    font-size: 1.25rem;
    font-weight: bold;
    color: #e74c3c;
    margin: 10px 0;
}
```

### 示例 3：个人作品集

```css
.portfolio {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-auto-rows: 250px;
    gap: 20px;
    padding: 20px;
}

.portfolio-item {
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
}

.portfolio-item::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(0, 0, 0, 0.8), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.portfolio-item:hover::before {
    opacity: 1;
}

.portfolio-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.portfolio-item:hover img {
    transform: scale(1.05);
}
```

## 布局最佳实践

### 1. 使用 CSS 自定义属性

```css
:root {
    --primary-color: #3182ce;
    --secondary-color: #718096;
    --spacing-xs: 0.5rem;
    --spacing-sm: 1rem;
    --spacing-md: 1.5rem;
    --spacing-lg: 2rem;
    --border-radius: 8px;
    --shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--spacing-md);
}

.card {
    background: white;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    padding: var(--spacing-lg);
}
```

### 2. 容器查询（现代方法）

```css
.component {
    container-type: inline-size;
}

@container (min-width: 400px) {
    .component {
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: 20px;
    }
}

@container (min-width: 600px) {
    .component {
        grid-template-columns: 1fr 3fr 1fr;
    }
}
```

### 3. 性能优化

```css
/* 使用 transform 和 opacity 实现动画（性能更好） */
.animated-element {
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.animated-element:hover {
    transform: scale(1.05);
    opacity: 0.9;
}

/* 使用 will-change 提示浏览器 */
.optimized-element {
    will-change: transform;
}

/* 避免布局抖动 */
.stable-layout {
    width: 100%;
    height: 200px; /* 固定高度避免重排 */
}
```

## 布局技术选择指南：

| 场景        | 推荐技术        | 理由               |
| ----------- | --------------- | ------------------ |
| 一维布局    | Flexbox         | 内容驱动，灵活对齐 |
| 二维布局    | CSS Grid        | 容器驱动，精确控制 |
| 导航/工具栏 | Flexbox         | 完美的对齐控制     |
| 卡片布局    | Grid            | 自动响应式         |
| 复杂页面    | Grid            | 清晰的区域划分     |
| 移动端优先  | Flexbox + Media | 渐进增强           |

## 核心原则：

-   移动端优先 - 从小屏幕开始设计
-   语义化 HTML - 使用正确的标签
-   渐进增强 - 确保基础功能可用
-   性能考虑 - 优化重绘和重排
-   可访问性 - 确保键盘导航和屏幕阅读器支持
