# CSS 变量（CSS Custom Properties）

CSS 变量（也称为 CSS 自定义属性）允许你在样式表中定义可重用的值，并在整个文档中使用它们。

适合场景：

-   主题切换
-   颜色体系
-   间距规范

## 基本概念

### 定义变量

使用 `--` 前缀定义变量：

```css
:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --spacing-unit: 16px;
    --max-width: 1200px;
    --font-family-base: "Segoe UI", Arial, sans-serif;
}
```

### 使用变量

使用 var() 函数调用变量：

```css
.element {
    color: var(--primary-color);
    margin: var(--spacing-unit);
    max-width: var(--max-width);
    font-family: var(--font-family-base);
}
```

## 变量作用域

### 全局作用域（`:root`）

```css
:root {
    /* 全局变量，整个文档可用 */
    --global-bg-color: #f8f9fa;
    --global-text-color: #212529;
    --global-border-radius: 8px;
}

body {
    background-color: var(--global-bg-color);
    color: var(--global-text-color);
}
```

### 局部作用域

```css
/* 组件级别变量 */
.card {
    --card-bg: white;
    --card-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    --card-padding: 24px;

    background: var(--card-bg);
    box-shadow: var(--card-shadow);
    padding: var(--card-padding);
    border-radius: var(--global-border-radius); /* 可以使用全局变量 */
}

/* 元素级别变量 */
button {
    --btn-padding: 12px 24px;
    --btn-radius: 4px;

    padding: var(--btn-padding);
    border-radius: var(--btn-radius);
}
```

### 继承性

```css
/* 父元素定义，子元素继承 */
.parent {
    --parent-color: blue;
    color: var(--parent-color); /* 自身使用 */
}

.child {
    /* 继承父元素的 --parent-color */
    border-color: var(--parent-color);
}
```

## 变量语法详解

### `var()` 函数

```css
.element {
    /* 基础用法 */
    color: var(--primary-color);

    /* 带默认值 */
    color: var(--undefined-color, #000); /* 如果变量未定义，使用#000 */

    /* 嵌套使用 */
    background: var(--bg-color, var(--fallback-color, white));

    /* 在calc()中使用 */
    width: calc(var(--base-width) * 2 + 20px);
    margin: calc(var(--spacing) * 2);
}
```

### 动态值

```css
:root {
    --dynamic-size: 100px;
}

.box {
    width: var(--dynamic-size);
    height: var(--dynamic-size);

    /* 通过类名或伪类修改 */
    &.large {
        --dynamic-size: 200px;
    }

    &:hover {
        --dynamic-size: 150px;
        transition: width 0.3s, height 0.3s;
    }
}
```

## 实际应用示例

### 示例 1：主题系统

```css
/* 定义主题变量 */
:root {
    /* 明亮主题（默认） */
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --text-primary: #212529;
    --text-secondary: #6c757d;
    --border-color: #dee2e6;
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #17a2b8;
}

[data-theme="dark"] {
    /* 深色主题 */
    --bg-primary: #121212;
    --bg-secondary: #1e1e1e;
    --text-primary: #e0e0e0;
    --text-secondary: #b0b0b0;
    --border-color: #333333;
    --primary-color: #0d6efd;
    --secondary-color: #5a6268;
    --success-color: #198754;
    --danger-color: #c82333;
    --warning-color: #e0a800;
    --info-color: #138496;
}

[data-theme="blue"] {
    /* 蓝色主题 */
    --bg-primary: #e3f2fd;
    --bg-secondary: #bbdefb;
    --text-primary: #0d47a1;
    --text-secondary: #1565c0;
    --border-color: #90caf9;
    --primary-color: #1976d2;
    --success-color: #2e7d32;
    --danger-color: #c62828;
}

/* 应用主题 */
body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    transition: background-color 0.3s, color 0.3s;
}

.card {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
}

.button {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 4px;
}

.button.secondary {
    background-color: var(--secondary-color);
}

.button.success {
    background-color: var(--success-color);
}
```

### 示例 2：响应式设计

```css
/* 响应式变量 */
:root {
    /* 断点变量 */
    --breakpoint-sm: 576px;
    --breakpoint-md: 768px;
    --breakpoint-lg: 992px;
    --breakpoint-xl: 1200px;

    /* 间距变量 */
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;

    /* 响应式字体大小 */
    --font-size-base: 16px;
    --font-size-scale: 1.2;
}

/* 媒体查询中使用变量 */
@media (min-width: var(--breakpoint-md)) {
    :root {
        --font-size-base: 18px;
        --spacing-md: 20px;
    }
}

@media (min-width: var(--breakpoint-lg)) {
    :root {
        --font-size-base: 20px;
        --spacing-md: 24px;
    }
}

/* 应用响应式变量 */
body {
    font-size: var(--font-size-base);
    line-height: calc(var(--font-size-base) * 1.5);
}

.container {
    padding: var(--spacing-md);
    max-width: var(--breakpoint-xl);
    margin: 0 auto;
}

.grid {
    display: grid;
    gap: var(--spacing-md);

    @media (min-width: var(--breakpoint-md)) {
        grid-template-columns: repeat(2, 1fr);
        gap: var(--spacing-lg);
    }

    @media (min-width: var(--breakpoint-lg)) {
        grid-template-columns: repeat(3, 1fr);
        gap: var(--spacing-xl);
    }
}
```

### 示例 3：设计系统

```css
/* 设计系统变量 */
:root {
    /* 颜色系统 */
    --color-primary-50: #e3f2fd;
    --color-primary-100: #bbdefb;
    --color-primary-200: #90caf9;
    --color-primary-300: #64b5f6;
    --color-primary-400: #42a5f5;
    --color-primary-500: #2196f3;
    --color-primary-600: #1e88e5;
    --color-primary-700: #1976d2;
    --color-primary-800: #1565c0;
    --color-primary-900: #0d47a1;

    /* 阴影系统 */
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.12);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);

    /* 圆角系统 */
    --radius-sm: 2px;
    --radius-md: 4px;
    --radius-lg: 8px;
    --radius-xl: 16px;
    --radius-full: 9999px;

    /* 动画时间 */
    --duration-fast: 150ms;
    --duration-normal: 300ms;
    --duration-slow: 500ms;
}

/* 组件变量 */
.btn {
    /* 基础变量 */
    --btn-bg: var(--color-primary-500);
    --btn-color: white;
    --btn-border: none;
    --btn-padding-y: 12px;
    --btn-padding-x: 24px;
    --btn-radius: var(--radius-md);
    --btn-shadow: var(--shadow-sm);

    /* 应用变量 */
    background-color: var(--btn-bg);
    color: var(--btn-color);
    border: var(--btn-border);
    padding: var(--btn-padding-y) var(--btn-padding-x);
    border-radius: var(--btn-radius);
    box-shadow: var(--btn-shadow);
    transition: all var(--duration-normal);

    /* 变体 */
    &.btn-secondary {
        --btn-bg: var(--color-primary-100);
        --btn-color: var(--color-primary-800);
    }

    &.btn-outline {
        --btn-bg: transparent;
        --btn-color: var(--color-primary-500);
        --btn-border: 2px solid var(--color-primary-500);
    }

    &.btn-lg {
        --btn-padding-y: 16px;
        --btn-padding-x: 32px;
        --btn-radius: var(--radius-lg);
    }

    &:hover {
        --btn-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
}
```

## JavaScript 交互

### 获取和设置变量

```js
// 获取根元素
const root = document.documentElement;

// 获取变量值
const primaryColor = getComputedStyle(root).getPropertyValue("--primary-color").trim();

// 设置变量值
root.style.setProperty("--primary-color", "#ff0000");

// 删除变量
root.style.removeProperty("--primary-color");

// 批量设置变量
const theme = {
    "--primary-color": "#ff5722",
    "--secondary-color": "#607d8b",
    "--spacing-unit": "20px",
};

Object.entries(theme).forEach(([key, value]) => {
    root.style.setProperty(key, value);
});
```

### 动态主题切换

```js
class ThemeManager {
    constructor() {
        this.themes = {
            light: {
                "--bg-color": "#ffffff",
                "--text-color": "#000000",
                "--primary-color": "#007bff",
            },
            dark: {
                "--bg-color": "#121212",
                "--text-color": "#ffffff",
                "--primary-color": "#0d6efd",
            },
            blue: {
                "--bg-color": "#e3f2fd",
                "--text-color": "#0d47a1",
                "--primary-color": "#1976d2",
            },
        };

        this.currentTheme = localStorage.getItem("theme") || "light";
        this.applyTheme(this.currentTheme);
    }

    applyTheme(themeName) {
        const theme = this.themes[themeName];
        if (!theme) return;

        const root = document.documentElement;
        Object.entries(theme).forEach(([property, value]) => {
            root.style.setProperty(property, value);
        });

        // 设置data-theme属性
        document.body.setAttribute("data-theme", themeName);

        // 保存到localStorage
        localStorage.setItem("theme", themeName);
        this.currentTheme = themeName;
    }

    toggleTheme() {
        const themeOrder = ["light", "dark", "blue"];
        const currentIndex = themeOrder.indexOf(this.currentTheme);
        const nextIndex = (currentIndex + 1) % themeOrder.length;
        this.applyTheme(themeOrder[nextIndex]);
    }
}

// 使用示例
const themeManager = new ThemeManager();

// 切换主题按钮
document.getElementById("theme-toggle").addEventListener("click", () => {
    themeManager.toggleTheme();
});

// 根据系统主题自动切换
const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

prefersDarkScheme.addEventListener("change", e => {
    themeManager.applyTheme(e.matches ? "dark" : "light");
});
```

### 实时预览组件

```js
// 动态调整CSS变量预览效果
class StylePreview {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.inputs = {};
        this.initControls();
    }

    initControls() {
        // 创建控制面板
        const controls = [
            { id: "primary-color", label: "主颜色", type: "color", var: "--primary-color" },
            {
                id: "spacing",
                label: "间距",
                type: "range",
                var: "--spacing",
                min: 8,
                max: 48,
                step: 4,
            },
            {
                id: "radius",
                label: "圆角",
                type: "range",
                var: "--border-radius",
                min: 0,
                max: 24,
                step: 2,
            },
            {
                id: "shadow",
                label: "阴影强度",
                type: "range",
                var: "--shadow-intensity",
                min: 0,
                max: 50,
                step: 1,
            },
        ];

        controls.forEach(control => {
            const input = document.createElement("input");
            input.type = control.type;
            input.id = control.id;

            if (control.type === "range") {
                input.min = control.min;
                input.max = control.max;
                input.step = control.step;
            }

            input.addEventListener("input", e => {
                this.updateVariable(
                    control.var,
                    e.target.value + (control.type === "range" ? "px" : "")
                );
            });

            this.inputs[control.id] = input;
        });
    }

    updateVariable(variable, value) {
        this.container.style.setProperty(variable, value);
    }

    getVariables() {
        const computed = getComputedStyle(this.container);
        const variables = {};

        for (let i = 0; i < computed.length; i++) {
            const name = computed[i];
            if (name.startsWith("--")) {
                variables[name] = computed.getPropertyValue(name).trim();
            }
        }

        return variables;
    }
}

// 使用示例
const preview = new StylePreview("preview-container");
```

## 高级用法

### CSS 变量与 SASS/LESS 变量混合

```css
/* SASS变量编译时确定 */
$sass-primary: #007bff;
$sass-spacing: 16px;

/* CSS变量运行时可变 */
:root {
    --css-primary: #{$sass-primary};
    --css-spacing: #{$sass-spacing};
    --dynamic-value: 100px;
}

.component {
    /* 使用SASS变量（编译后固定） */
    color: $sass-primary;

    /* 使用CSS变量（可动态修改） */
    background-color: var(--css-primary);
    padding: var(--css-spacing);

    /* 动态计算 */
    width: calc(var(--dynamic-value) * 2);
}
```

### CSS 变量与 CSS-in-JS

```js
// 在React中使用CSS变量
import React, { useState } from "react";
import styled from "styled-components";

const Container = styled.div`
    --primary-color: ${props => props.primaryColor || "#007bff"};
    --spacing: ${props => props.spacing || "16px"};

    background-color: var(--primary-color);
    padding: var(--spacing);
    color: white;
    transition: background-color 0.3s;
`;

function ThemeComponent() {
    const [primaryColor, setPrimaryColor] = useState("#007bff");
    const [spacing, setSpacing] = useState("16px");

    return (
        <div>
            <Container primaryColor={primaryColor} spacing={spacing}>
                内容区域
            </Container>

            <input
                type="color"
                value={primaryColor}
                onChange={e => setPrimaryColor(e.target.value)}
            />

            <input
                type="range"
                min="8"
                max="32"
                value={parseInt(spacing)}
                onChange={e => setSpacing(`${e.target.value}px`)}
            />
        </div>
    );
}
```

## 性能优化

### 变量分组和复用

```css
/* 不好的做法：分散定义 */
:root {
    --color-red: #ff0000;
    --color-green: #00ff00;
    --color-blue: #0000ff;
    --spacing-small: 8px;
    --spacing-medium: 16px;
    --spacing-large: 24px;
}

/* 好的做法：分组定义 */
:root {
    /* 颜色组 */
    --colors-red: #ff0000;
    --colors-green: #00ff00;
    --colors-blue: #0000ff;

    /* 间距组 */
    --spacings-small: 8px;
    --spacings-medium: 16px;
    --spacings-large: 24px;

    /* 使用别名 */
    --primary-color: var(--colors-blue);
    --default-spacing: var(--spacings-medium);
}
```

### 避免过度嵌套

```css
/* 避免过度嵌套 */
.element {
    /* 不好：过度嵌套 */
    background-color: var(--theme-colors-primary-main-default);

    /* 好：适当简化 */
    background-color: var(--primary-color);
}
```

### 使用默认值减少计算

```css
/* 使用默认值避免未定义错误 */
.element {
    color: var(--undefined-color, #000);
    padding: var(--spacing, 16px);

    /* 复杂计算使用CSS变量缓存 */
    --computed-width: calc(100% - var(--sidebar-width, 250px));
    width: var(--computed-width);
}
```

### 浏览器兼容性

```css
/* 渐进增强方案 */
.element {
    /* 传统方式作为后备 */
    color: #007bff;
    padding: 16px;

    /* 支持CSS变量的浏览器使用变量 */
    @supports (color: var(--test)) {
        color: var(--primary-color, #007bff);
        padding: var(--spacing-unit, 16px);
    }
}

/* 检测并添加类名 */
if (window.CSS && CSS.supports && CSS.supports('color', 'var(--test)')) {
    document.documentElement.classList.add('css-variables');
} else {
    document.documentElement.classList.add('no-css-variables');
}

/* 使用类名提供后备样式 */
.no-css-variables .card {
    background-color: #ffffff; /* 固定颜色 */
    padding: 20px; /* 固定间距 */
}

.css-variables .card {
    background-color: var(--card-bg);
    padding: var(--card-padding);
}
```

## 最佳实践

### 命名约定要一致

```css
:root {
    /* 使用kebab-case */
    --primary-color: #007bff;
    --spacing-unit: 16px;
    --font-family-base: "Arial", sans-serif;
}
```

### 使用语义化名称

```css
/* 不好 */
--color1: #007bff;

/* 好 */
--primary-color: #007bff;
--brand-color-accent: #007bff;
```

### 设置合理的默认值

```css
.element {
    color: var(--text-color, #333);
    margin: var(--margin, 0);
}
```

### 避免在关键路径中使用复杂计算

```css
/* 预计算复杂值 */
:root {
    --complex-value: calc(100vw - var(--sidebar-width) - var(--margin) * 2);
}
```

### 文档化你的变量

```css
/**
 * CSS Custom Properties
 * 
 * Color Palette
 * --primary-color:     Brand primary color (#007bff)
 * --secondary-color:   Brand secondary color (#6c757d)
 * --success-color:     Success state color (#28a745)
 * --danger-color:      Error state color (#dc3545)
 * 
 * Spacing
 * --spacing-unit:      Base spacing unit (16px)
 * --spacing-xs:        Extra small spacing (4px)
 * --spacing-sm:        Small spacing (8px)
 * --spacing-md:        Medium spacing (16px)
 * --spacing-lg:        Large spacing (24px)
 * --spacing-xl:        Extra large spacing (32px)
 */
```
