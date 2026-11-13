# CSS 用户界面

CSS提供了丰富的用户界面属性，用于控制和美化表单元素、鼠标指针、选择文本等交互元素

## 调整大小 - `resize`

允许用户调整元素的大小

语法：
```css
.element {
    resize: none | both | horizontal | vertical | block | inline;
}
```
- none: 默认值，禁止调整大小
- both: 允许水平和垂直方向调整大小
- horizontal: 只允许水平方向调整大小
- vertical: 只允许垂直方向调整大小
- block (CSS3新增): 允许在块方向上调整大小（取决于书写模式）
- inline (CSS3新增): 允许在行内方向上调整大小

要使 `resize` 生效，元素必须满足以下条件之一：

- `overflow` 不是 `visible`
- `overflow` 是 `hidden、auto、scroll` 等

## 光标 - `cursor`

控制鼠标指针的外观。

```css
/* 基础用法 */
.element {
    cursor: pointer;        /* 手型指针 */
    cursor: default;        /* 默认箭头 */
    cursor: text;           /* 文本选择型（I型） */
    cursor: move;           /* 移动十字箭头 */
    cursor: not-allowed;    /* 禁止符号 */
    cursor: help;           /* 帮助问号 */
    cursor: wait;           /* 等待/加载 */
    cursor: progress;       /* 进度指示 */
    cursor: crosshair;      /* 十字线 */
    cursor: zoom-in;        /* 放大镜+ */
    cursor: zoom-out;       /* 放大镜- */
    cursor: grab;           /* 抓取手型 */
    cursor: grabbing;       /* 抓取中手型 */
}

/* 自定义光标 */
.button {
    cursor: url('cursor.png'), auto;          /* 自定义图片 */
    cursor: url('cursor.svg') 10 5, pointer;  /* 自定义偏移量 */
    cursor: url('cursor.cur'), url('cursor.png'), default; /* 多格式备用 */
}
```

应用示例：
```css
/* 可拖拽元素 */
.draggable {
    cursor: grab;
}

.draggable:active {
    cursor: grabbing;
}

/* 禁用状态 */
button:disabled {
    cursor: not-allowed;
    opacity: 0.6;
}

/* 可调整大小 */
.resizable {
    cursor: nwse-resize;    /* 西北-东南方向 */
    cursor: nesw-resize;    /* 东北-西南方向 */
    cursor: col-resize;     /* 列调整 */
    cursor: row-resize;     /* 行调整 */
}
```

## 用户选择 - `user-select`

控制用户能否选择文本

```css
/* 禁止选择文本 */
.no-select {
    user-select: none;      /* 标准属性 */
    -webkit-user-select: none;  /* Safari/Chrome */
    -moz-user-select: none;     /* Firefox */
    -ms-user-select: none;      /* IE10+ */
}

/* 允许选择文本 */
.selectable {
    user-select: text;      /* 只能选择文本 */
    user-select: all;       /* 点击选择所有内容 */
    user-select: auto;      /* 默认，浏览器决定 */
    user-select: contain;   /* 只能在元素内选择（实验性） */
}
```

应用示例：
```css
/* 按钮禁止选择 */
button {
    user-select: none;
    -webkit-touch-callout: none; /* iOS Safari */
    -webkit-tap-highlight-color: transparent; /* 移除点击高亮 */
}

/* 代码块允许选择 */
pre, code {
    user-select: text;
}

/* 拖拽时临时禁止选择 */
.dragging {
    user-select: none;
}

/* 输入框选择优化 */
input, textarea {
    user-select: text;
    cursor: text;
}
```

## 界面外观 - `appearance`

控制元素的原生外观

```css
/* 移除原生样式 */
input, button, select {
    appearance: none;           /* 标准 */
    -webkit-appearance: none;   /* Webkit */
    -moz-appearance: none;      /* Firefox */
}

/* 特定元素 */
select {
    appearance: menulist-button;    /* 下拉按钮 */
}

input[type="checkbox"] {
    appearance: checkbox;           /* 复选框 */
}

input[type="radio"] {
    appearance: radio;              /* 单选按钮 */
}

input[type="range"] {
    appearance: slider-horizontal;  /* 滑块 */
}

input[type="search"] {
    appearance: searchfield;        /* 搜索框 */
}
```

自定义表单控件示例
```css
/* 自定义复选框 */
.custom-checkbox {
    appearance: none;
    width: 20px;
    height: 20px;
    border: 2px solid #ddd;
    border-radius: 4px;
    position: relative;
    cursor: pointer;
}

.custom-checkbox:checked {
    background-color: #007bff;
    border-color: #007bff;
}

.custom-checkbox:checked::after {
    content: "✓";
    position: absolute;
    color: white;
    font-size: 14px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

/* 自定义滑块 */
.custom-range {
    appearance: none;
    width: 100%;
    height: 6px;
    background: #ddd;
    border-radius: 3px;
    outline: none;
}

.custom-range::-webkit-slider-thumb {
    appearance: none;
    width: 20px;
    height: 20px;
    background: #007bff;
    border-radius: 50%;
    cursor: pointer;
}

.custom-range::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: #007bff;
    border-radius: 50%;
    border: none;
    cursor: pointer;
}
```

## 轮廓 - `outline`

控制焦点轮廓样式

```css
/* 基础轮廓 */
button:focus {
    outline: 2px solid blue;       /* 实线轮廓 */
    outline: 2px dotted red;       /* 点状轮廓 */
    outline: 2px dashed green;     /* 虚线轮廓 */
}

/* 轮廓偏移 */
button:focus {
    outline: 2px solid blue;
    outline-offset: 4px;           /* 轮廓与元素间距 */
}

/* 移除轮廓（不推荐，除非提供替代方案） */
button:focus {
    outline: none;                 /* 移除默认轮廓 */
}

/* 替代焦点样式 */
button:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.5); /* 阴影替代 */
}

/* 轮廓样式组合 */
input:focus {
    outline: 2px solid;
    outline-color: #007bff;
    outline-offset: 2px;
    border-color: #007bff;
}
```

焦点管理示例

```css
/* 可访问性焦点样式 */
.focus-visible {
    outline: 3px solid #0066cc;
    outline-offset: 2px;
}

/* 鼠标和键盘焦点区分 */
button:focus:not(:focus-visible) {
    outline: none; /* 鼠标点击时不显示轮廓 */
}

button:focus-visible {
    outline: 3px solid #0066cc;
    outline-offset: 2px;
}
```

## 文本溢出 - `text-overflow`

控制文本溢出时的显示方式

```css
/* 单行文本溢出显示省略号 */
.truncate {
    white-space: nowrap;          /* 禁止换行 */
    overflow: hidden;             /* 隐藏溢出 */
    text-overflow: ellipsis;      /* 显示省略号 */
}

/* 多行文本溢出 */
.multi-line-truncate {
    display: -webkit-box;
    -webkit-line-clamp: 3;        /* 显示行数 */
    -webkit-box-orient: vertical; /* 垂直方向 */
    overflow: hidden;
    text-overflow: ellipsis;
}

/* 自定义溢出标记 */
.custom-ellipsis {
    overflow: hidden;
    text-overflow: " [...]";      /* 自定义标记 */
}

/* 鼠标悬停显示完整内容 */
.tooltip-container {
    position: relative;
}

.tooltip-container:hover::after {
    content: attr(data-tooltip);
    position: absolute;
    top: 100%;
    left: 0;
    background: #333;
    color: white;
    padding: 8px;
    border-radius: 4px;
    white-space: nowrap;
    z-index: 1000;
}
```

## 滚动条样式 - `scrollbar`

自定义滚动条外观（实验性属性）

```css
/* Webkit浏览器（Chrome, Safari, Edge） */
.scrollable {
    overflow-y: auto;
    max-height: 300px;
    
    /* 整个滚动条 */
    scrollbar-width: thin;               /* Firefox */
    scrollbar-color: #888 #f1f1f1;      /* Firefox */
    
    /* Webkit滚动条 */
    &::-webkit-scrollbar {
        width: 12px;                    /* 垂直滚动条宽度 */
        height: 12px;                   /* 水平滚动条高度 */
    }
    
    /* 滚动条轨道 */
    &::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 6px;
    }
    
    /* 滚动条滑块 */
    &::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 6px;
        border: 3px solid #f1f1f1;      /* 创建内边距效果 */
    }
    
    /* 滚动条滑块悬停 */
    &::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* 滚动条按钮（上下箭头） */
    &::-webkit-scrollbar-button {
        display: none;                  /* 隐藏按钮 */
    }
    
    /* 滚动条角落 */
    &::-webkit-scrollbar-corner {
        background: #f1f1f1;
    }
}
```

自定义滚动条示例
```css
/* 现代简约滚动条 */
.minimal-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: rgba(0,0,0,0.3) transparent;
}

.minimal-scrollbar::-webkit-scrollbar {
    width: 8px;
}

.minimal-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.minimal-scrollbar::-webkit-scrollbar-thumb {
    background: rgba(0,0,0,0.3);
    border-radius: 4px;
}

/* 彩色滚动条 */
.colorful-scrollbar {
    scrollbar-width: 12px;
    scrollbar-color: #4CAF50 #E8F5E9;
}

.colorful-scrollbar::-webkit-scrollbar {
    width: 12px;
}

.colorful-scrollbar::-webkit-scrollbar-track {
    background: #E8F5E9;
    border-radius: 10px;
}

.colorful-scrollbar::-webkit-scrollbar-thumb {
    background: #4CAF50;
    border-radius: 10px;
    background-clip: padding-box;
    border: 2px solid transparent;
}
```

## 输入框样式

```css
/* 占位符样式 */
input::placeholder {
    color: #999;
    font-style: italic;
    opacity: 1; /* Firefox默认0.54 */
}

/* 自动填充样式 */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px white inset !important;
    -webkit-text-fill-color: #333 !important;
}

/* 无效输入样式 */
input:invalid {
    border-color: #dc3545;
}

input:valid {
    border-color: #28a745;
}

/* 聚焦时的占位符 */
input:focus::placeholder {
    color: transparent;
}

/* 禁用状态 */
input:disabled {
    background-color: #e9ecef;
    cursor: not-allowed;
}
```

## 触摸操作 - `touch-action` 

控制触摸屏上的手势行为

```css
/* 允许所有触摸操作 */
.element {
    touch-action: auto;                /* 默认 */
}

/* 禁止缩放 */
.no-zoom {
    touch-action: pan-x pan-y;        /* 只允许平移 */
}

/* 只允许垂直滚动 */
.vertical-scroll {
    touch-action: pan-y;              /* 只允许垂直平移 */
}

/* 只允许水平滚动 */
.horizontal-scroll {
    touch-action: pan-x;              /* 只允许水平平移 */
}

/* 禁止触摸操作 */
.no-touch {
    touch-action: none;               /* 禁止所有触摸操作 */
}

/* 允许双击缩放 */
.allow-zoom {
    touch-action: manipulation;       /* 禁止双击缩放以外的操作 */
}
```

## 硬件加速和性能

```css
/* 启用硬件加速 */
.hardware-accelerated {
    transform: translateZ(0);
    backface-visibility: hidden;
    perspective: 1000px;
}

/* 优化滚动性能 */
.smooth-scroll {
    scroll-behavior: smooth;          /* 平滑滚动 */
    -webkit-overflow-scrolling: touch; /* iOS惯性滚动 */
}

/* 减少重绘 */
.will-change {
    will-change: transform, opacity;  /* 预告变化 */
}

/* 优化图像渲染 */
.optimized-image {
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
    image-rendering: pixelated;
}
```

## 完整的UI组件示例

```css
/* 自定义按钮组件 */
.btn {
    /* 基础样式 */
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    
    /* 用户界面属性 */
    user-select: none;
    touch-action: manipulation;
    outline: none;
    
    /* 交互状态 */
    &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    &:active {
        transform: translateY(0);
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    &:focus-visible {
        outline: 3px solid rgba(0, 123, 255, 0.5);
        outline-offset: 2px;
    }
    
    &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none !important;
        box-shadow: none !important;
    }
}

/* 自定义下拉菜单 */
.custom-select {
    appearance: none;
    width: 100%;
    padding: 12px 40px 12px 16px;
    border: 2px solid #ddd;
    border-radius: 6px;
    background: white url('data:image/svg+xml,<svg ...>') no-repeat right 16px center;
    background-size: 16px;
    cursor: pointer;
    
    &:focus {
        border-color: #007bff;
        outline: none;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
    }
    
    &:disabled {
        background-color: #f5f5f5;
        cursor: not-allowed;
    }
}

/* 模态框背景滚动锁定 */
.modal-open {
    overflow: hidden;
    touch-action: none;
}

.modal-scroll {
    overscroll-behavior: contain;  /* 防止滚动链 */
}
```

## 现代CSS UI特性

```css
/* CSS嵌套（现代浏览器） */
.card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    
    &:hover {
        border-color: #007bff;
        
        .card-title {
            color: #007bff;
        }
    }
    
    .card-title {
        margin: 0 0 10px 0;
        transition: color 0.2s ease;
    }
}

/* CSS容器查询（实验性） */
@container (min-width: 400px) {
    .card {
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: 20px;
    }
}

/* 滚动捕捉（Scroll Snap） */
.scroll-container {
    scroll-snap-type: x mandatory;
    overflow-x: auto;
    display: flex;
    gap: 20px;
    
    .scroll-item {
        scroll-snap-align: start;
        flex: 0 0 auto;
        width: 300px;
    }
}
```

## 可访问性考虑

```css
/* 屏幕阅读器隐藏但可访问 */
.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
    .button {
        border: 2px solid currentColor;
    }
}

/* 减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-color: #1a1a1a;
        --text-color: #ffffff;
        --border-color: #444;
    }
    
    .element {
        background-color: var(--bg-color);
        color: var(--text-color);
        border-color: var(--border-color);
    }
}
```

## 

### 

```css

```

### 

```css

```

### 

```css

```

### 

```css

```




