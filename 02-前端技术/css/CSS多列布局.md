# CSS 多列布局（CSS Multi-column Layout）

CSS 多列布局允许文本内容像报纸一样在多列中流动，非常适合创建杂志式的布局

## 主要属性

### `column-count`

指定列的数量

```css
.container {
    column-count: 3; /* 固定3列 */
}
```

### `column-width`

指定每列的理想宽度。

```css
.container {
    column-width: 200px; /* 每列最小宽度200px */
}
```

### `columns`（简写属性）

同时设置`column-count`和`column-width`。

```css
.container {
    columns: 3 200px; /* 列数 宽度 */
}
```

## 列间距和分隔线

### `column-gap`

设置列之间的间距。

```css
.container {
    column-gap: 40px; /* 固定间距 */
    column-gap: 2em; /* 相对单位 */
    column-gap: normal; /* 默认值，通常是1em */
}
```

### `column-rule`

设置列之间的分隔线（类似 border）。

```css
.container {
    /* 简写 */
    column-rule: 2px solid #ccc;

    /* 分开设置 */
    column-rule-width: 2px;
    column-rule-style: solid;
    column-rule-color: #ccc;

    /* 更多样式 */
    column-rule: 3px dotted red;
    column-rule: 1px dashed rgba(0, 0, 0, 0.5);
}
```

## 跨列控制

### `column-span`

允许元素跨越多列。

```css
h2 {
    column-span: all; /* 跨所有列 */
    column-span: none; /* 不跨列（默认） */
}
```

### `break-inside`

控制元素内部是否允许断列。

```css
.card {
    break-inside: avoid; /* 避免在元素内部断列 */
    break-inside: avoid-column; /* 避免在列中断开 */
    break-inside: auto; /* 默认，允许断开 */
}
```

### `break-before / break-after`

控制元素前后的断列行为。

```css
h2 {
    break-before: column; /* 在h2前断列 */
    break-after: avoid; /* 避免在h2后断列 */
}
```

## 列的高度和平衡

### `column-fill`

控制列的内容分布方式。

```css
.container {
    height: 400px; /* 必须设置高度 */
    column-fill: auto; /* 按顺序填充，可能列高度不同 */
    column-fill: balance; /* 尽量平衡各列高度（默认） */
    column-fill: balance-all; /* 平衡所有列（实验性） */
}
```

## 完整示例

### 示例 1：基础多列布局

```css
.article {
    columns: 3 250px; /* 最多3列，每列至少250px */
    column-gap: 40px; /* 列间距40px */
    column-rule: 1px solid #ddd; /* 灰色分隔线 */
    padding: 20px;
}

/* 标题跨列 */
.article h1 {
    column-span: all;
    text-align: center;
    margin-bottom: 30px;
}

/* 图片不断开 */
.article img {
    break-inside: avoid;
    max-width: 100%;
    margin: 10px 0;
}
```

### 示例 2：响应式多列

```css
.responsive-columns {
    /* 默认：单列 */
    column-count: 1;
    column-gap: 20px;

    /* 平板：双列 */
    @media (min-width: 768px) {
        column-count: 2;
        column-gap: 30px;
    }

    /* 桌面：三列 */
    @media (min-width: 1024px) {
        column-count: 3;
        column-gap: 40px;
    }
}
```

### 示例 3：带样式的多列

```css
.magazine-layout {
    columns: 4 200px;
    column-gap: 2em;
    column-rule: 3px double #333;

    /* 首字下沉 */
    p:first-of-type::first-letter {
        float: left;
        font-size: 3em;
        line-height: 1;
        margin: 0 5px 0 0;
    }
}

/* 防止列表断开 */
.magazine-layout ul,
.magazine-layout ol {
    break-inside: avoid-column;
}

/* 引用块跨列 */
.magazine-layout blockquote {
    column-span: all;
    font-style: italic;
    text-align: center;
    margin: 30px 0;
    padding: 20px;
    background: #f5f5f5;
}
```

## 实际应用案例

### 1. 新闻网站布局

```css
.news-grid {
    columns: 4 300px;
    column-gap: 30px;
}

.news-item {
    break-inside: avoid-column;
    margin-bottom: 30px;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.news-item img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.news-content {
    padding: 20px;
}

.news-content h3 {
    margin-top: 0;
    font-size: 1.2em;
}

.read-more {
    display: inline-block;
    margin-top: 10px;
    color: #0066cc;
    text-decoration: none;
}
```

### 2. 图片画廊

```css
.photo-gallery {
    columns: 5 200px;
    column-gap: 15px;
}

.photo {
    break-inside: avoid-column;
    margin-bottom: 15px;
    position: relative;
    overflow: hidden;
    border-radius: 5px;
}

.photo img {
    width: 100%;
    height: auto;
    display: block;
    transition: transform 0.3s ease;
}

.photo:hover img {
    transform: scale(1.05);
}

.photo-caption {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 10px;
    transform: translateY(100%);
    transition: transform 0.3s ease;
}

.photo:hover .photo-caption {
    transform: translateY(0);
}
```

### 3. 价格表/功能对比

```css
.feature-comparison {
    columns: 3 300px;
    column-gap: 20px;
}

.plan {
    break-inside: avoid-column;
    background: #fff;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 30px;
    margin-bottom: 20px;
    text-align: center;
}

.plan.popular {
    border-color: #4caf50;
    position: relative;
}

.plan.popular::before {
    content: "热门";
    position: absolute;
    top: -10px;
    left: 50%;
    transform: translateX(-50%);
    background: #4caf50;
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.9em;
}

.plan h3 {
    color: #333;
    margin-top: 0;
}

.price {
    font-size: 2.5em;
    font-weight: bold;
    color: #2196f3;
}

.feature-list {
    list-style: none;
    padding: 0;
    text-align: left;
}

.feature-list li {
    padding: 10px 0;
    border-bottom: 1px solid #eee;
}

.feature-list li::before {
    content: "✓";
    color: #4caf50;
    margin-right: 10px;
}
```

## JavaScript 交互

```js
// 动态改变列数
const container = document.querySelector(".multi-column");
const button = document.querySelector("#change-columns");

button.addEventListener("click", () => {
    const currentColumns = getComputedStyle(container).columnCount;
    const newColumns = currentColumns === "3" ? "1" : "3";
    container.style.columnCount = newColumns;
});

// 获取列信息
function getColumnInfo() {
    const container = document.querySelector(".multi-column");
    const computedStyle = getComputedStyle(container);

    return {
        columnCount: computedStyle.columnCount,
        columnWidth: computedStyle.columnWidth,
        columnGap: computedStyle.columnGap,
        columnFill: computedStyle.columnFill,
    };
}

// 监听窗口变化，调整列数
window.addEventListener("resize", () => {
    const container = document.querySelector(".responsive-columns");
    const width = container.offsetWidth;

    if (width < 600) {
        container.style.columnCount = 1;
    } else if (width < 900) {
        container.style.columnCount = 2;
    } else {
        container.style.columnCount = 3;
    }
});
```

## 性能考虑

-   避免过多的列：超过 4 列可能影响阅读体验和性能
-   图片优化：在多列布局中，确保图片适当压缩
-   小心使用`column-span`：跨列元素可能导致布局问题
-   测试断列：确保内容在断列处仍然可读

## 浏览器兼容性和前缀

```css
/* 兼容性处理 */
.multi-column {
    /* 旧版Webkit前缀 */
    -webkit-column-count: 3;
    -webkit-column-gap: 40px;
    -webkit-column-rule: 1px solid #ccc;

    /* 标准属性 */
    column-count: 3;
    column-gap: 40px;
    column-rule: 1px solid #ccc;
}

/* 跨列的兼容性处理 */
h2 {
    -webkit-column-span: all; /* Webkit */
    column-span: all; /* 标准 */
}
```

## 与 Flexbox/Grid 的对比

| 特性       | 多列布局               | Flexbox      | Grid                |
| ---------- | ---------------------- | ------------ | ------------------- |
| 主要用途   | 文本流布局             | 一维布局     | 二维布局            |
| 内容流     | 自动从上到下，从左到右 | 可控制方向   | 网格定位            |
| 响应式     | 基于宽度自动调整       | 需要媒体查询 | 需要媒体查询        |
| 跨元素     | 支持（column-span）    | 不支持       | 支持（grid-column） |
| 浏览器支持 | 很好                   | 很好         | 现代浏览器          |

## 最佳实践

-   设置合适的列宽：`column-width` 通常设置在 `200-300px` 之间
-   使用平衡填充：对于固定高度的容器，使用 `column-fill: balance`
-   考虑可读性：避免列过窄导致阅读困难
-   移动端优化：在移动设备上减少列数
-   测试断列：确保重要内容不会被不自然地分割
