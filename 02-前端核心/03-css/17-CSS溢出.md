# CSS 溢出

CSS 的 overflow 属性用于控制当元素内容超出其指定区域时的表现方式。

## `overflow` 基础

`overflow` 属性定义当内容溢出元素框时发生的事情。

### 基本语法：

```css
overflow: visible | hidden | scroll | auto | clip;
```

-   `overflow-x`：控制水平方向溢出
-   `overflow-y`：控制垂直方向溢出

## `overflow` 取值详解

| 值          | 说明                                       | 示例                 |
| ----------- | ------------------------------------------ | -------------------- |
| **visible** | 默认值，内容溢出显示                       | 内容超出容器仍可见   |
| **hidden**  | 内容溢出隐藏，不显示，也不滚动             | 剪切溢出部分         |
| **scroll**  | 内容溢出显示滚动条（无论是否溢出都会显示） | 横向/纵向滚动条      |
| **auto**    | 内容溢出时显示滚动条，否则不显示           | 常用响应式滚动       |
| **clip**    | 与 hidden 类似，但不产生滚动条             | CSS 2.1 新增，更轻量 |

## 方向特定的 `overflow` 属性

### 1. `overflow-x` - 水平方向

```css
.container {
    overflow-x: hidden; /* 水平方向隐藏 */
    overflow-x: scroll; /* 水平滚动条 */
    overflow-x: auto; /* 水平自动 */
}
```

### 2. `overflow-y` - 垂直方向

```css
.container {
    overflow-y: hidden; /* 垂直方向隐藏 */
    overflow-y: scroll; /* 垂直滚动条 */
    overflow-y: auto; /* 垂直自动 */
}
```

### 3. 组合使用

```css
.container {
    overflow-x: hidden; /* 水平隐藏 */
    overflow-y: auto; /* 垂直自动滚动 */

    /* 等价于 */
    overflow: hidden auto;
}
```

## 实用场景与示例

### 场景 1：模态框内容区域

```css
.modal-content {
    max-height: 70vh; /* 最大高度为视口的70% */
    overflow-y: auto; /* 内容多时垂直滚动 */
    padding: 20px;
}

.modal-body {
    /* 内容可能很长 */
    line-height: 1.6;
}
```

### 场景 2：代码块显示

```css
.code-block {
    background: #f4f4f4;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 15px;
    max-height: 300px;
    overflow: auto; /* 代码长时滚动 */
    font-family: "Courier New", monospace;
}

/* 添加好看的滚动条 */
.code-block::-webkit-scrollbar {
    width: 8px;
}

.code-block::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 4px;
}
```

### 场景 3：表格容器

```css
.table-container {
    width: 100%;
    max-height: 400px;
    overflow: auto; /* 表格太大时滚动 */
    border: 1px solid #e0e0e0;
}

table {
    width: 100%;
    border-collapse: collapse;
}

/* 固定表头 */
.table-container thead th {
    position: sticky;
    top: 0;
    background: white;
    z-index: 10;
}
```

### 场景 4：聊天消息区域

```css
.chat-messages {
    height: 400px;
    overflow-y: auto; /* 消息多时滚动 */
    padding: 10px;
    background: #f9f9f9;
    border: 1px solid #e0e0e0;
}

.message {
    margin-bottom: 10px;
    padding: 8px 12px;
    border-radius: 18px;
    max-width: 70%;
}

/* 自动滚动到底部 */
.chat-messages {
    scroll-behavior: smooth; /* 平滑滚动 */
}
```

### 场景 5：图片画廊

```css
.image-gallery {
    display: flex;
    gap: 10px;
    padding: 10px;
    overflow-x: auto; /* 水平滚动 */
    overflow-y: hidden; /* 垂直隐藏 */
    scroll-snap-type: x mandatory; /* 滚动吸附 */
}

.gallery-image {
    width: 200px;
    height: 150px;
    object-fit: cover;
    border-radius: 8px;
    scroll-snap-align: start; /* 滚动时吸附 */
    flex-shrink: 0; /* 防止图片被压缩 */
}
```

### 场景 6：工具提示

```css
.tooltip {
    position: absolute;
    max-width: 200px;
    padding: 8px 12px;
    background: #333;
    color: white;
    border-radius: 4px;
    font-size: 14px;

    /* 防止工具提示溢出屏幕 */
    overflow-wrap: break-word;
    overflow: hidden;
}

/* 确保长文本不会破坏布局 */
.tooltip-text {
    word-break: break-word;
    overflow: hidden;
    text-overflow: ellipsis;
}
```

### 场景 7：自定义滚动条（Webkit 浏览器）

```css
.custom-scrollbar {
    height: 300px;
    overflow: auto;
    background: #f0f0f0;
}

/* 滚动条轨道 */
.custom-scrollbar::-webkit-scrollbar {
    width: 12px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: #e0e0e0;
    border-radius: 6px;
}

/* 滚动条滑块 */
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 6px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #555;
}
```

### 场景 8：滚动行为控制

```css
.smooth-container {
    overflow: auto;
    scroll-behavior: smooth; /* 平滑滚动 */
}

/* 禁用滚动链 */
.isolated-scroll {
    overflow: auto;
    overscroll-behavior: contain; /* 防止滚动链 */
}

/* 页面级别的滚动控制 */
html {
    scroll-behavior: smooth; /* 整个页面平滑滚动 */
}
```

### 场景 9：响应式 overflow

```css
.responsive-container {
    width: 100%;
    height: 200px;
    overflow: auto;
}

/* 移动设备上调整 */
@media (max-width: 768px) {
    .responsive-container {
        height: 150px;
        overflow-x: hidden; /* 移动端禁用水平滚动 */
    }
}

/* 横屏模式 */
@media (max-height: 500px) and (orientation: landscape) {
    .responsive-container {
        height: 120px;
    }
}
```

### 场景 10：文本溢出处理

```css
/* 单行文本溢出显示省略号 */
.truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* 多行文本溢出显示省略号 */
.multiline-truncate {
    display: -webkit-box;
    -webkit-line-clamp: 3; /* 显示3行 */
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* 自定义溢出提示 */
.overflow-indicator::after {
    content: "...";
    position: absolute;
    bottom: 0;
    right: 0;
    background: white;
    padding-left: 5px;
}
```

## 常见问题与解决方案

### 问题 1：滚动条导致布局跳动

```css
/* 方案1：始终保留滚动条空间 */
.container {
    overflow-y: scroll; /* 始终显示滚动条 */
}

/* 方案2：使用CSS自定义属性计算 */
.container {
    --scrollbar-width: 17px;
    width: calc(100% - var(--scrollbar-width));
}

/* 方案3：隐藏原生滚动条，自定义样式 */
.hide-scrollbar {
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
}

.hide-scrollbar::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
}
```

### 问题 2：移动端滚动性能

```css
.mobile-scroll {
    overflow: auto;
    -webkit-overflow-scrolling: touch; /* 启用惯性滚动 */
    scroll-behavior: smooth;
}
```

### 问题 3：防止内容溢出破坏布局

```css
.breakout-prevention {
    max-width: 100%;
    overflow: hidden;
}

/* 处理长URL和单词 */
.break-words {
    overflow-wrap: break-word;
    word-break: break-word;
    hyphens: auto;
}
```
