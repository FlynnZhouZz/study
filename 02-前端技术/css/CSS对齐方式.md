# CSS 对齐方式

## 水平对齐

### 1. 文本水平对齐

```css
.text-left {
    text-align: left;      /* 左对齐（默认）*/
}

.text-center {
    text-align: center;    /* 居中对齐 */
}

.text-right {
    text-align: right;     /* 右对齐 */
}

.text-justify {
    text-align: justify;   /* 两端对齐 */
}
```

### 2. 块级元素水平居中

```css
/* 方法1：margin auto（最常用）*/
.center-block {
    width: 300px;
    margin-left: auto;
    margin-right: auto;
}

/* 方法2：绝对定位 + transform */
.center-absolute {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
}

/* 方法3：Flexbox */
.flex-container {
    display: flex;
    justify-content: center;
}

/* 方法4：Grid */
.grid-container {
    display: grid;
    place-items: center;
}
```

## 垂直对齐

### 1. 行内元素垂直对齐

```css
.baseline {
    vertical-align: baseline;    /* 默认，与父元素基线对齐 */
}

.middle {
    vertical-align: middle;     /* 与父元素中线对齐 */
}

.top {
    vertical-align: top;        /* 与父元素顶部对齐 */
}

.bottom {
    vertical-align: bottom;     /* 与父元素底部对齐 */
}
```

### 2. 块级元素垂直居中

```css
/* 方法1：绝对定位 + transform */
.center-vertical {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
}

/* 方法2：Flexbox（推荐）*/
.flex-container {
    display: flex;
    align-items: center;
    height: 300px; /* 需要明确高度 */
}

/* 方法3：Grid */
.grid-container {
    display: grid;
    place-items: center;
    height: 300px;
}

/* 方法4：表格布局 */
.table-container {
    display: table;
    height: 300px;
}

.table-cell {
    display: table-cell;
    vertical-align: middle;
}
```

## Flexbox 对齐方式

Flexbox 提供了最强大的对齐控制：

### 1. 主轴对齐（水平方向默认）

```css
.flex-container {
    display: flex;
    justify-content: flex-start;    /* 左对齐（默认）*/
    justify-content: center;        /* 居中对齐 */
    justify-content: flex-end;      /* 右对齐 */
    justify-content: space-between; /* 两端对齐，项目间间隔相等 */
    justify-content: space-around;  /* 每个项目两侧间隔相等 */
    justify-content: space-evenly;  /* 项目间间隔完全相等 */
}
```

### 2. 交叉轴对齐（垂直方向默认）

```css
.flex-container {
    display: flex;
    align-items: stretch;      /* 拉伸填满容器（默认）*/
    align-items: flex-start;   /* 顶部对齐 */
    align-items: center;       /* 居中对齐 */
    align-items: flex-end;     /* 底部对齐 */
    align-items: baseline;     /* 基线对齐 */
}
```

### 3. 多行 Flex 容器对齐

```css
.flex-container {
    display: flex;
    flex-wrap: wrap;
    align-content: stretch;     /* 拉伸填满（默认）*/
    align-content: flex-start;  /* 多行顶部对齐 */
    align-content: center;      /* 多行居中对齐 */
    align-content: flex-end;    /* 多行底部对齐 */
    align-content: space-between; /* 多行两端对齐 */
    align-content: space-around;  /* 多行周围对齐 */
}
```

### 4. 单个 Flex 项目对齐

```css
.flex-item {
    align-self: auto;          /* 继承容器的 align-items */
    align-self: flex-start;    /* 项目顶部对齐 */
    align-self: center;        /* 项目居中对齐 */
    align-self: flex-end;      /* 项目底部对齐 */
    align-self: stretch;       /* 项目拉伸 */
}
```

## Grid 对齐方式

Grid 布局提供二维对齐控制：

### 1. 容器内对齐

```css
.grid-container {
    display: grid;
    /* 同时设置 align-items 和 justify-items */
    place-items: center;       /* 所有项目居中 */
    
    /* 或分别设置 */
    justify-items: start;      /* 水平起始对齐 */
    justify-items: center;     /* 水平居中 */
    justify-items: end;        /* 水平结束对齐 */
    justify-items: stretch;    /* 水平拉伸（默认）*/
    
    align-items: start;        /* 垂直起始对齐 */
    align-items: center;       /* 垂直居中 */
    align-items: end;          /* 垂直结束对齐 */
    align-items: stretch;      /* 垂直拉伸（默认）*/
}
```

### 2. 轨道对齐

```css
.grid-container {
    display: grid;
    /* 当网格总尺寸小于容器时 */
    justify-content: start;    /* 网格整体左对齐 */
    justify-content: center;   /* 网格整体水平居中 */
    justify-content: end;      /* 网格整体右对齐 */
    justify-content: space-between; /* 网格两端对齐 */
    justify-content: space-around;  /* 网格周围对齐 */
    justify-content: space-evenly;  /* 网格均匀分布 */
    
    align-content: start;      /* 网格整体顶部对齐 */
    align-content: center;     /* 网格整体垂直居中 */
    align-content: end;        /* 网格整体底部对齐 */
    align-content: space-between; /* 网格垂直两端对齐 */
}
```

### 3. 单个网格项目对齐

```css
.grid-item {
    justify-self: start;       /* 项目在网格单元中左对齐 */
    justify-self: center;      /* 项目在网格单元中水平居中 */
    justify-self: end;         /* 项目在网格单元中右对齐 */
    justify-self: stretch;     /* 项目在网格单元中拉伸（默认）*/
    
    align-self: start;         /* 项目在网格单元中顶部对齐 */
    align-self: center;        /* 项目在网格单元中垂直居中 */
    align-self: end;           /* 项目在网格单元中底部对齐 */
    align-self: stretch;       /* 项目在网格单元中拉伸（默认）*/
}
```

## 实用对齐示例

### 示例 1：完美居中（水平和垂直）

```css
/* 方法1：Flexbox（推荐）*/
.perfect-center-flex {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* 满视口高度 */
}

/* 方法2：Grid */
.perfect-center-grid {
    display: grid;
    place-items: center;
    height: 100vh;
}

/* 方法3：绝对定位 */
.perfect-center-absolute {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

/* 方法4：margin auto（需要明确尺寸）*/
.perfect-center-margin {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    margin: auto;
    width: 300px;
    height: 200px;
}
```

### 示例 2：导航菜单对齐

```css
.navbar {
    display: flex;
    justify-content: space-between; /* 品牌左，菜单右 */
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

### 示例 3：卡片布局对齐

```css
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    padding: 2rem;
}

.card {
    display: flex;
    flex-direction: column;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-header {
    padding: 1.5rem;
    background: #f8f9fa;
    text-align: center;
}

.card-body {
    padding: 1.5rem;
    flex-grow: 1; /* 填充剩余空间 */
}

.card-footer {
    padding: 1rem 1.5rem;
    background: #f8f9fa;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
```

### 示例 4：表单对齐

```css
.form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 1.5rem;
}

.form-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

.form-row .form-group {
    flex: 1;
    margin-bottom: 0;
}

label {
    margin-bottom: 0.5rem;
    font-weight: bold;
}

input, select, textarea {
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 2rem;
}

.btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
}

.btn-primary {
    background: #007bff;
    color: white;
}

.btn-secondary {
    background: #6c757d;
    color: white;
}
```

### 示例 5：页脚对齐

```css
.footer {
    background: #333;
    color: white;
    padding: 3rem 2rem;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.footer-section h3 {
    margin-bottom: 1rem;
    color: #ffd700;
}

.footer-bottom {
    text-align: center;
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid #555;
}
```

## 响应式对齐技巧

### 1. 移动端适配

```css
.container {
    display: flex;
    flex-direction: column; /* 移动端垂直排列 */
    gap: 1rem;
}

@media (min-width: 768px) {
    .container {
        flex-direction: row; /* 平板以上水平排列 */
        justify-content: space-between;
        align-items: center;
    }
}
```

### 2. 文本对齐响应式

```css
.responsive-text {
    text-align: left; /* 移动端左对齐 */
}

@media (min-width: 768px) {
    .responsive-text {
        text-align: center; /* 大屏幕居中对齐 */
    }
}
```
