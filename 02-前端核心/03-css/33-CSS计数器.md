# CSS 计数器

CSS 计数器是一种 通过 CSS 对元素进行自动编号的机制。

-   适合用于列表、章节标题、序号等场景
-   无需在 HTML 中手动添加数字
-   纯 CSS 就可以实现递增编号

## 基本用法

CSS 计数器主要使用三个属性：

| 属性                | 说明                                    |
| ------------------- | --------------------------------------- |
| `counter-reset`     | 初始化计数器                            |
| `counter-increment` | 递增计数器                              |
| `content`           | 在 `::before` 或 `::after` 中显示计数器 |

## 基本计数器

### 1. 简单数字计数器

```html
<h2>Introduction</h2>
<p>This is the introduction section.</p>

<h2>Methods</h2>
<p>This is the methods section.</p>

<h2>Results</h2>
<p>This is the results section.</p>
```

```css
/* 初始化计数器 */
body {
    counter-reset: section; /* 创建名为 section 的计数器 */
}

/* 每次遇到 h2 时递增计数器 */
h2 {
    counter-increment: section; /* 递增 section 计数器 */
}

/* 在 h2 前显示计数器 */
h2::before {
    content: "Section " counter(section) ": ";
    color: #3182ce;
    font-weight: bold;
}
```

效果：

```text
Section 1: Introduction
This is the introduction section.

Section 2: Methods
This is the methods section.

Section 3: Results
This is the results section.
```

### 2. 自定义起始值和步长

```css
body {
    counter-reset: chapter 5; /* 从 5 开始计数 */
}

h1 {
    counter-increment: chapter 2; /* 每次递增 2 */
}

h1::before {
    content: "Chapter " counter(chapter) ": ";
}
```

## 嵌套计数器

嵌套计数器非常适合多级列表和目录结构。

### 1. 多级章节编号

```html
<div class="part">Getting Started</div>
<div class="chapter">Introduction</div>
<div class="section">Overview</div>
<div class="section">Requirements</div>

<div class="chapter">Installation</div>
<div class="section">Step by Step</div>
<div class="section">Troubleshooting</div>

<div class="part">Advanced Topics</div>
<div class="chapter">Configuration</div>
```

```css
/* 初始化各级计数器 */
body {
    counter-reset: part chapter section;
}

.part {
    counter-reset: chapter; /* 遇到 part 时重置 chapter */
    counter-increment: part;
}

.part::before {
    content: "Part " counter(part) ": ";
    font-size: 1.5em;
    color: #e53e3e;
}

.chapter {
    counter-reset: section; /* 遇到 chapter 时重置 section */
    counter-increment: chapter;
    margin-left: 20px;
}

.chapter::before {
    content: counter(part) "." counter(chapter) " ";
    font-weight: bold;
    color: #3182ce;
}

.section {
    counter-increment: section;
    margin-left: 40px;
}

.section::before {
    content: counter(part) "." counter(chapter) "." counter(section) " ";
    color: #38a169;
}
```

效果：

```text
Part 1: Getting Started
1.1 Introduction
1.1.1 Overview
1.1.2 Requirements
1.2 Installation
1.2.1 Step by Step
1.2.2 Troubleshooting

Part 2: Advanced Topics
2.1 Configuration
```

### 2. 使用 counters() 自动处理嵌套

```html
<ol>
    <li>
        First item
        <ol>
            <li>
                Nested item
                <ol>
                    <li>Deep nested</li>
                    <li>Another deep</li>
                </ol>
            </li>
            <li>Second nested</li>
        </ol>
    </li>
    <li>Second item</li>
</ol>
```

```css
ol {
    counter-reset: nested-list;
    list-style: none;
    padding-left: 0;
}

li {
    counter-increment: nested-list;
}

li::before {
    content: counters(nested-list, ".") ". ";
    color: #3182ce;
    font-weight: bold;
    margin-right: 8px;
}
```

效果：

```text
1. First item
   1.1. Nested item
      1.1.1. Deep nested
      1.1.2. Another deep
   1.2. Second nested
2. Second item
```

## 计数器样式

你可以为计数器指定不同的显示样式：

### 1. 数字格式

```css
.roman::before {
    content: counter(section, upper-roman) ". ";
}

.alpha::before {
    content: counter(section, lower-alpha) ". ";
}

.leading-zero::before {
    content: counter(section, decimal-leading-zero) ". ";
}
```

可用样式：

-   `decimal` - 数字 1, 2, 3...（默认）
-   `decimal-leading-zero` - 01, 02, 03...
-   `lower-roman` - i, ii, iii, iv...
-   `upper-roman` - I, II, III, IV...
-   `lower-alpha` - a, b, c, d...
-   `upper-alpha` - A, B, C, D...
-   `lower-greek` - α, β, γ, δ...
-   `disc` - •
-   `circle` - ◦
-   `square` - ▪

### 2. 复杂样式示例

```css
.fancy-counter {
    counter-reset: fancy;
}

.fancy-item {
    counter-increment: fancy;
    margin-bottom: 10px;
    padding-left: 40px;
    position: relative;
}

.fancy-item::before {
    content: counter(fancy);
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 30px;
    height: 30px;
    background: #3182ce;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 14px;
}
```

## 实用场景示例

### 场景 1：常见问题 FAQ 编号

```html
<div class="faq-container">
    <div class="faq-item">
        <div class="faq-question">How do I reset my password?</div>
        <div class="faq-answer">Click on "Forgot Password" on the login page.</div>
    </div>
    <div class="faq-item">
        <div class="faq-question">Where can I find documentation?</div>
        <div class="faq-answer">Visit our documentation portal at docs.example.com.</div>
    </div>
</div>
```

```css
.faq-container {
    counter-reset: faq;
}

.faq-item {
    counter-increment: faq;
    margin-bottom: 20px;
    padding: 20px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    background: #f7fafc;
}

.faq-question::before {
    content: "Q" counter(faq) ": ";
    font-weight: bold;
    color: #3182ce;
}

.faq-answer::before {
    content: "A" counter(faq) ": ";
    font-weight: bold;
    color: #38a169;
}
```

### 场景 2：步骤指示器

```html
<div class="steps">
    <div class="step completed">Cart</div>
    <div class="step active">Information</div>
    <div class="step">Shipping</div>
    <div class="step">Payment</div>
</div>
```

```css
.steps {
    counter-reset: step;
    display: flex;
    justify-content: space-between;
    position: relative;
    margin: 40px 0;
}

.steps::before {
    content: "";
    position: absolute;
    top: 15px;
    left: 0;
    width: 100%;
    height: 2px;
    background: #e2e8f0;
    z-index: 1;
}

.step {
    counter-increment: step;
    position: relative;
    z-index: 2;
    text-align: center;
    flex: 1;
}

.step::before {
    content: counter(step);
    width: 32px;
    height: 32px;
    background: #e2e8f0;
    color: #718096;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 8px;
    font-weight: bold;
    transition: all 0.3s ease;
}

.step.active::before {
    background: #3182ce;
    color: white;
}

.step.completed::before {
    background: #38a169;
    color: white;
}
```

### 场景 3：图片画廊计数器

```css
.gallery {
    counter-reset: photo;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    padding: 20px;
}

.photo {
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.photo::before {
    content: "Photo " counter(photo);
    counter-increment: photo;
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}

.photo img {
    width: 100%;
    height: 150px;
    object-fit: cover;
    display: block;
}
```

### 场景 4：价格表特性标记

```html
<div class="feature-list">
    <div class="feature-item included">Unlimited Projects</div>
    <div class="feature-item included">Team Collaboration</div>
    <div class="feature-item included">Advanced Analytics</div>
    <div class="feature-item excluded">Priority Support</div>
    <div class="feature-item excluded">Custom Domain</div>
</div>
```

```css
.feature-list {
    counter-reset: feature;
}

.feature-item {
    counter-increment: feature;
    padding: 12px 0;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
}

.feature-item::before {
    content: counter(feature);
    width: 24px;
    height: 24px;
    background: #3182ce;
    color: white;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    margin-right: 12px;
    flex-shrink: 0;
}

.feature-item.included::before {
    background: #38a169;
    content: "✓";
}

.feature-item.excluded::before {
    background: #e53e3e;
    content: "✕";
}
```

## 高级技巧

### 1. 多计数器组合

```css
.document {
    counter-reset: figure table;
}

.figure {
    counter-increment: figure;
    margin: 20px 0;
    text-align: center;
}

.figure::before {
    content: "Figure " counter(figure);
    font-weight: bold;
    display: block;
    margin-bottom: 8px;
}

.table {
    counter-increment: table;
    margin: 20px 0;
}

.table::before {
    content: "Table " counter(table);
    font-weight: bold;
    display: block;
    margin-bottom: 8px;
}

.caption::after {
    content: " (" counter(figure) ")";
    font-style: italic;
    color: #666;
}
```

### 2. 条件计数器

```css
/* 只为特定类别的项目计数 */
.todo-list {
    counter-reset: todo;
}

.todo-item.important {
    counter-increment: todo;
}

.todo-item.important::before {
    content: "!" counter(todo) " ";
    color: #e53e3e;
    font-weight: bold;
}
```

### 3. 动画计数器

```css
.animated-counter {
    counter-reset: count 0;
    animation: count-up 5s forwards;
}

.animated-counter::before {
    content: counter(count);
}

@keyframes count-up {
    to {
        counter-increment: count 100;
    }
}
```

## 浏览器兼容性提示

```css
/* 为不支持计数器的浏览器提供备用方案 */
.fallback-content {
    display: none;
}

@supports not (counter-increment: fallback) {
    .counter-element::before {
        content: none;
    }

    .fallback-content {
        display: inline;
    }
}
```
