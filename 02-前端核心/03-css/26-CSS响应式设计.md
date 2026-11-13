# CSS 响应式设计（Responsive Design）

CSS 响应式设计（Responsive Design） 的目标是：一套代码，适配不同屏幕尺寸和设备（手机 / 平板 / 桌面）。

## 视口设置 (Viewport)

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

## 媒体查询 (Media Queries)

```css
/* 移动设备优先（默认移动端样式） */
.container {
    padding: 10px;
}

/* 平板 */
@media (min-width: 768px) {
    .container {
        padding: 20px;
    }
}

/* 桌面 */
@media (min-width: 1024px) {
    .container {
        padding: 30px;
    }
}

/* 特定设备断点 */
@media (max-width: 600px) {
    /* 手机样式 */
}

@media (min-width: 601px) and (max-width: 1024px) {
    /* 平板样式 */
}
```

## 流式布局

```css
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
}

/* 百分比宽度 */
.col {
    width: 100%; /* 默认全宽 */
}

@media (min-width: 768px) {
    .col {
        width: 50%; /* 平板两列 */
    }
}

@media (min-width: 1024px) {
    .col {
        width: 25%; /* 桌面四列 */
    }
}
```

## 弹性盒子 (Flexbox)

```css
.container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.item {
    flex: 1 1 300px; /* 最小宽度300px，自动伸缩 */
}

/* 响应式调整 */
@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }
}
```

## 网格布局 (Grid)

```css
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

/* 响应式网格 */
@media (max-width: 768px) {
    .grid-container {
        grid-template-columns: 1fr;
    }
}
```

## 响应式单位

```css
.element {
    font-size: 1rem; /* 相对根元素 */
    padding: 2em; /* 相对父元素字体大小 */
    width: 50vw; /* 视口宽度的50% */
    height: 50vh; /* 视口高度的50% */
    margin: 2%; /* 相对父元素宽度 */
}

/* 使用clamp()函数 */
.heading {
    font-size: clamp(1.5rem, 4vw, 3rem);
}
```

## 响应式图片

```css
img {
    max-width: 100%;
    height: auto;
}

/* 背景图片 */
.hero {
    background-image: url("small.jpg");
}

@media (min-resolution: 2dppx) {
    .hero {
        background-image: url("large.jpg");
    }
}
```

## 实用断点系统

```css
/* Bootstrap风格断点 */
:root {
    --breakpoint-xs: 0;
    --breakpoint-sm: 576px;
    --breakpoint-md: 768px;
    --breakpoint-lg: 992px;
    --breakpoint-xl: 1200px;
    --breakpoint-xxl: 1400px;
}
```

常见断点（经验值）：
| 设备 | 宽度 |
| -- | -------------- |
| 手机 | ≤ 768px |
| 平板 | 769px – 1024px |
| 桌面 | ≥ 1025px |

```css
/* 手机 */
@media (max-width: 768px) {
}

/* 平板 */
@media (min-width: 769px) and (max-width: 1024px) {
}

/* 桌面 */
@media (min-width: 1025px) {
}
```

## 移动优先的完整示例

```css
/* 基础样式（移动端） */
body {
    font-size: 16px;
    line-height: 1.5;
}

.header {
    flex-direction: column;
}

.nav {
    flex-direction: column;
}

/* 平板 */
@media (min-width: 768px) {
    body {
        font-size: 18px;
    }

    .header {
        flex-direction: row;
        justify-content: space-between;
    }

    .nav {
        flex-direction: row;
        gap: 20px;
    }
}

/* 桌面 */
@media (min-width: 1024px) {
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }

    .main-content {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 40px;
    }
}
```

## 现代 CSS 特性

宗旨：少写媒体查询

### `flex` + 自动换行

```css
.list {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}
```

### `grid` + `auto-fit` / `auto-fill`

自适应列数，不用断点

```css
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
}
```

### `clamp()` 响应式字体

```css
font-size: clamp(14px, 2vw, 20px);
```

### 容器查询

```css
/* 容器查询（最新特性） */
@container (min-width: 500px) {
    .card {
        display: grid;
        grid-template-columns: 1fr 2fr;
    }
}

/* 嵌套语法 */
.container {
    & .item {
        color: blue;

        @media (min-width: 768px) {
            color: red;
        }
    }
}
```

## 最佳实践建议

-   移动优先：先写移动端样式，再用媒体查询增强
-   断点选择：根据内容选择断点，而不是特定设备
-   测试：使用浏览器开发者工具测试各种尺寸
-   性能：避免过多媒体查询，保持代码简洁
-   渐进增强：确保基本功能在所有设备上都可用
