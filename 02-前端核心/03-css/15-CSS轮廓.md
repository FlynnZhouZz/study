# CSS 轮廓

CSS 轮廓（Outline）是一个经常被忽视但非常有用的属性。轮廓看起来像边框，但在行为和用途上有重要区别。

## 什么是 CSS 轮廓（outline）？

outline 是绘制在元素外侧的一条线，不占空间。

使用场景：输入框聚焦、按钮聚焦、调试元素边界。

| 属性        | 是否占空间 | 位置                       | 是否影响布局 |
| ----------- | ---------- | -------------------------- | ------------ |
| **border**  | ✔ 占空间   | 在 padding 外、margin 内   | ✔ 影响布局   |
| **outline** | ✖ 不占空间 | 在 border 外（不挤占布局） | ✖ 不影响布局 |

## 轮廓的基本属性

### 1. `outline-width` - 轮廓宽度

设置轮廓线的粗细。

```css
button {
    outline-width: 2px; /* 固定值 */
    outline-width: thin; /* 细线 */
    outline-width: medium; /* 中等（默认）*/
    outline-width: thick; /* 粗线 */
}
```

### 2. `outline-style` - 轮廓样式

设置轮廓线的样式。

```css
input {
    outline-style: solid; /* 实线 */
    outline-style: dashed; /* 虚线 */
    outline-style: dotted; /* 点线 */
    outline-style: double; /* 双实线 */
    outline-style: groove; /* 3D凹槽 */
    outline-style: none; /* 无轮廓（谨慎使用！）*/
}
```

### 3. `outline-color` - 轮廓颜色

设置轮廓线的颜色。

```css
a {
    outline-color: red;
    outline-color: #ff0000;
    outline-color: invert; /* 颜色反转（确保对比度）*/
}
```

### 4. `outline-offset` - 轮廓偏移

设置轮廓与元素边框之间的间距

```css
button {
    border: 2px solid #333;
    outline: 2px solid #3498db;
    outline-offset: 4px; /* 轮廓向外偏移4px */
}

img:focus {
    outline: 3px dotted #e74c3c;
    outline-offset: -6px; /* 轮廓向内偏移6px */
}
```

### 5. ·:focus-visible· - 智能焦点

只在键盘焦点时显示轮廓，鼠标点击时不显示。

```css
/* 现代方法：只在键盘导航时显示轮廓 */
button:focus-visible {
    outline: 3px solid #3498db;
    outline-offset: 2px;
}

/* 鼠标点击时不显示轮廓 */
button:focus:not(:focus-visible) {
    outline: none;
}
```

### 轮廓的简写属性

```css
element {
    outline: 2px solid red; /* 宽度 样式 颜色 */
    outline: thick dashed #3498db; /* 任意顺序 */
    outline: none; /* 无轮廓 */
}
```

## 最佳实践

### 1. 焦点指示（最重要的用途）

为键盘导航用户提供视觉反馈。

```css
/* 良好的焦点样式 */
button:focus,
input:focus,
a:focus {
    outline: 2px solid #3498db;
    outline-offset: 2px; /* 增加轮廓与元素的间距 */
}

/* 更精美的焦点样式 */
.custom-focus:focus {
    outline: 3px dashed #e74c3c;
    outline-offset: 4px;
    background-color: #fffacd; /* 同时改变背景色 */
}
```

### 2. 调试布局

临时添加轮廓来查看元素边界。

```css
/* 调试所有元素 */
* {
    outline: 1px solid red;
}

/* 调试特定元素 */
.debug * {
    outline: 1px dashed blue;
}
```

### 3. 表单输入框焦点样式

```css
.form-input {
    width: 100%;
    padding: 12px;
    border: 2px solid #bdc3c7;
    border-radius: 6px;
    font-size: 16px;
    transition: all 0.3s ease;
}

.form-input:focus {
    border-color: #3498db;
    outline: none; /* 移除默认轮廓 */
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2); /* 用阴影代替轮廓 */
}

/* 错误状态的焦点 */
.form-input.error:focus {
    border-color: #e74c3c;
    box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.2);
}
```

### 4. 导航链接焦点样式

```css
.nav-link {
    display: block;
    padding: 10px 15px;
    color: #333;
    text-decoration: none;
    border-radius: 4px;
}

.nav-link:focus {
    outline: 2px dashed #3498db;
    outline-offset: -2px; /* 向内偏移 */
    background-color: #ecf0f1;
}

.nav-link:hover {
    background-color: #f8f9fa;
}
```

### 5. 自定义复选框焦点样式

```css
.custom-checkbox {
    width: 20px;
    height: 20px;
    border: 2px solid #bdc3c7;
    border-radius: 3px;
    display: inline-block;
    position: relative;
}

.custom-checkbox:focus {
    outline: 2px solid #3498db;
    outline-offset: 2px;
}

input[type="checkbox"]:checked + .custom-checkbox {
    background-color: #3498db;
    border-color: #3498db;
}
```

### 6. 图片焦点样式

```css
.thumbnail {
    border: 3px solid transparent;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.thumbnail:focus {
    outline: none; /* 移除默认轮廓 */
    border-color: #3498db;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* 为键盘用户提供备用轮廓 */
.thumbnail:focus-visible {
    outline: 3px dotted #3498db;
    outline-offset: 4px;
}
```

## 注意事项

### 1. 永远不要完全移除焦点轮廓！

```css
/* ❌ 危险的写法 - 破坏可访问性 */
button:focus {
    outline: none;
}

/* ✅ 安全的写法 - 提供替代焦点指示 */
button:focus {
    outline: none;
    background-color: #ffff99;
    border-color: #333;
}

/* ✅ 更好的写法 - 保留轮廓但美化它 */
button:focus {
    outline: 2px solid #3498db;
    outline-offset: 2px;
}
```

### 2. 轮廓的局限性

-   轮廓不受 border-radius 影响，总是矩形
-   轮廓不能分别设置各边
-   轮廓不影响布局，这可能既是优点也是缺点

### 3. 现代最佳实践

```css
/* 使用 :focus-visible 提供智能焦点 */
button {
    /* 基础样式 */
}

button:focus-visible {
    outline: 3px solid #3498db;
    outline-offset: 2px;
}

/* 回退方案，支持旧浏览器 */
@supports not selector(:focus-visible) {
    button:focus {
        outline: 3px solid #3498db;
        outline-offset: 2px;
    }
}
```
