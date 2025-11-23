# CSS 表格

CSS 表格指的是使用 CSS 来样式化 HTML 中的 `<table>` 元素及其相关子元素（`<tr>`, `<td>`, `<th>` 等）。通过 CSS，你可以极大地改善表格的默认外观，使其更美观、更易读、更专业。

## HTML 表格结构回顾

```html
<table>
    <thead>
        <!-- 表头 -->
        <tr>
            <!-- 表头行 -->
            <th>姓名</th>
            <!-- 表头单元格 -->
            <th>年龄</th>
            <th>城市</th>
        </tr>
    </thead>
    <tbody>
        <!-- 表格主体 -->
        <tr>
            <!-- 数据行 -->
            <td>张三</td>
            <!-- 数据单元格 -->
            <td>25</td>
            <td>北京</td>
        </tr>
        <tr>
            <td>李四</td>
            <td>30</td>
            <td>上海</td>
        </tr>
    </tbody>
    <tfoot>
        <!-- 表脚 -->
        <tr>
            <td colspan="3">总计：2 人</td>
        </tr>
    </tfoot>
</table>
```

## 核心 CSS 表格属性

### 1. `border` - 边框（基础）

设置表格及其单元格的边框。

```css
table {
    border: 1px solid #ccc; /* 为整个表格设置边框 */
}

th,
td {
    border: 1px solid #ddd; /* 为每个单元格设置边框 */
    padding: 8px; /* 添加内边距，让内容不紧贴边框 */
}
```

### 2. `border-collapse` - 边框合并

这是**最重要的表格属性之一**，决定表格边框是分开的还是合并的。

```css
table {
    border-collapse: collapse; /* 合并相邻边框（推荐） */
    /* border-collapse: separate; */ /* 默认值，边框分开 */
}
```

解释：

-   `separate`：双线边框效果，单元格之间有间隙
-   `collapse`：单线边框效果，更现代、更简洁

### 3. `border-spacing` - 边框间距

当 `border-collapse: separate;` 时，此属性设置相邻单元格边框间的距离。

```css
table {
    border-collapse: separate;
    border-spacing: 10px; /* 水平和垂直间距都是10px */
    border-spacing: 5px 10px; /* 水平5px，垂直10px */
}
```

### 4. `empty-cells` - 空单元格显示

当 `border-collapse: separate;` 时，控制空单元格的边框和背景是否显示。

```css
table {
    border-collapse: separate;
    empty-cells: hide; /* 隐藏空单元格的边框和背景 */
    /* empty-cells: show; */ /* 默认值，显示空单元格 */
}
```

### 5. `table-layout` - 表格布局算法

控制表格单元格、行和列的布局算法。

```css
table {
    table-layout: fixed; /* 固定布局，列宽由表格宽度和列宽设置决定 */
    /* table-layout: auto; */ /* 默认值，自动布局，根据内容计算列宽 */
    width: 100%; /* 配合 fixed 使用效果更好 */
}
```

解释：

-   auto：浏览器根据内容自动计算列宽（可能性能较差）
-   fixed：列宽由表格宽度和列宽设置决定，渲染速度更快

## 实用样式示例

### 示例 1：基础美化表格（最常用）

```css
.basic-table {
    width: 100%;
    border-collapse: collapse; /* 关键：合并边框 */
    font-family: Arial, sans-serif;
}

.basic-table th,
.basic-table td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}

.basic-table th {
    background-color: #f2f2f2;
    color: #333;
    font-weight: bold;
}

.basic-table tr:hover {
    background-color: #f5f5f5; /* 行悬停效果 */
}
```

### 示例 2：斑马纹表格（交替行颜色）

```css
.zebra-table {
    width: 100%;
    border-collapse: collapse;
}

.zebra-table th,
.zebra-table td {
    border: 1px solid #ddd;
    padding: 12px;
}

.zebra-table th {
    background-color: #4caf50;
    color: white;
}

.zebra-table tr:nth-child(even) {
    background-color: #f2f2f2; /* 偶数行背景色 */
}

.zebra-table tr:hover {
    background-color: #e9e9e9;
}
```

### 示例 3：现代简约表格

```css
.modern-table {
    width: 100%;
    border-collapse: collapse;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 添加阴影 */
    border-radius: 8px; /* 圆角 */
    overflow: hidden; /* 确保圆角效果 */
}

.modern-table th {
    background-color: #3498db;
    color: white;
    padding: 15px;
    text-align: left;
    font-weight: 500;
}

.modern-table td {
    padding: 15px;
    border-bottom: 1px solid #ecf0f1;
}

.modern-table tr:last-child td {
    border-bottom: none; /* 最后一行无下边框 */
}

.modern-table tr:hover {
    background-color: #f8f9fa;
    transition: background-color 0.3s ease; /* 平滑过渡 */
}
```

### 示例 4：固定表头表格

当表格很长需要滚动时，固定表头非常有用。

```css
.scrollable-table-container {
    max-height: 400px;
    overflow-y: auto; /* 垂直滚动 */
    border: 1px solid #ddd;
}

.fixed-header-table {
    width: 100%;
    border-collapse: collapse;
}

.fixed-header-table thead {
    position: sticky; /* 关键：粘性定位 */
    top: 0;
    z-index: 1;
}

.fixed-header-table th {
    background-color: #34495e;
    color: white;
    padding: 12px;
    border-bottom: 2px solid #2c3e50;
}

.fixed-header-table td {
    padding: 10px;
    border-bottom: 1px solid #bdc3c7;
}
```

```html
<div class="scrollable-table-container">
    <table class="fixed-header-table">
        <thead>
            <tr>
                <th>姓名</th>
                <th>部门</th>
                <th>工资</th>
            </tr>
        </thead>
        <tbody>
            <!-- 很多行数据 -->
        </tbody>
    </table>
</div>
```

### 示例 5：响应式表格

在小屏幕上，将表格转换为卡片布局。

```css
.responsive-table {
    width: 100%;
    border-collapse: collapse;
}

/* 在大屏幕上正常显示 */
@media screen and (min-width: 768px) {
    .responsive-table th,
    .responsive-table td {
        padding: 12px;
        border: 1px solid #ddd;
    }
}

/* 在小屏幕上转换为卡片布局 */
@media screen and (max-width: 767px) {
    .responsive-table,
    .responsive-table thead,
    .responsive-table tbody,
    .responsive-table th,
    .responsive-table td,
    .responsive-table tr {
        display: block;
    }

    .responsive-table thead {
        display: none; /* 隐藏表头 */
    }

    .responsive-table tr {
        margin-bottom: 15px;
        border: 1px solid #ddd;
        padding: 10px;
    }

    .responsive-table td {
        border: none;
        position: relative;
        padding-left: 50%;
    }

    .responsive-table td::before {
        content: attr(data-label); /* 使用 data-label 属性作为标签 */
        position: absolute;
        left: 10px;
        width: 45%;
        font-weight: bold;
    }
}
```

```html
<table class="responsive-table">
    <thead>
        <tr>
            <th>产品</th>
            <th>价格</th>
            <th>库存</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td data-label="产品">笔记本电脑</td>
            <td data-label="价格">¥5,999</td>
            <td data-label="库存">25</td>
        </tr>
        <!-- 更多行 -->
    </tbody>
</table>
```

## 表格特定元素样式

### 1. 表头样式

```css
th {
    background-color: #2c3e50;
    color: white;
    font-weight: bold;
    text-transform: uppercase; /* 字母大写 */
    letter-spacing: 1px; /* 字间距 */
}
```

### 2. 列样式

```css
/* 为特定列设置样式 */
td:nth-child(2),
th:nth-child(2) {
    /* 第二列 */
    background-color: #f9f9f9;
    font-weight: bold;
}

/* 数值列右对齐 */
td:nth-child(3) {
    text-align: right;
}
```

### 3. 表脚样式

```css
tfoot {
    background-color: #e74c3c;
    color: white;
    font-weight: bold;
}

tfoot td {
    border: none !important;
}
```
