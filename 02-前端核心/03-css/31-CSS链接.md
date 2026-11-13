# CSS 链接

CSS 链接指的是使用 CSS 来样式化 HTML 中的 `<a>`（锚点）元素。链接有其特殊之处，因为它们有多种不同的状态，我们可以为每种状态定义不同的样式。

## CSS 链接有 4 种状态（必须记住顺序）

| 状态        | 解释                 |
| ----------- | -------------------- |
| `a:link`    | 普通未访问过的链接   |
| `a:visited` | 用户访问过的链接     |
| `a:hover`   | 鼠标悬停在链接上     |
| `a:active`  | 鼠标按下（点击瞬间） |

### 定义样式的顺序：LVHA 法则

Link → Visited → Hover → Active

否则 hover 会被覆盖。

## 实用样式示例

### 示例 1：基础链接样式（去除默认下划线）

```css
a {
    color: #3498db; /* 设置一个好看的蓝色 */
    text-decoration: none; /* 去除默认下划线 */
    transition: color 0.3s ease; /* 为颜色变化添加平滑过渡 */
}

a:hover {
    color: #2980b9; /* 悬停时变为深蓝色 */
    text-decoration: underline; /* 悬停时显示下划线 */
}
```

### 示例 2：按钮式链接

```css
a.button {
    display: inline-block; /* 允许设置 padding 和 margin */
    padding: 10px 20px;
    background-color: #4caf50; /* 绿色背景 */
    color: white !important; /* 确保文字颜色为白色 */
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

a.button:hover {
    background-color: #45a049; /* 悬停时变深绿色 */
}

a.button:active {
    transform: translateY(2px); /* 点击时下沉效果 */
}
```

### 示例 3：现代简约链接

```css
a.modern {
    color: #2c3e50;
    text-decoration: none;
    position: relative; /* 为伪元素定位做准备 */
    padding-bottom: 2px; /* 为下划线留出空间 */
}

a.modern::after {
    content: "";
    position: absolute;
    width: 0;
    height: 2px;
    bottom: 0;
    left: 0;
    background-color: #e74c3c; /* 下划线颜色 */
    transition: width 0.3s ease; /* 宽度变化的过渡 */
}

a.modern:hover::after {
    width: 100%; /* 悬停时下划线从左侧展开到右侧 */
}

a.modern:hover {
    color: #e74c3c;
}
```

### 示例 4：面包屑导航链接

```css
.breadcrumb {
    font-size: 14px;
}

.breadcrumb a {
    color: #666;
    text-decoration: none;
}

.breadcrumb a:hover {
    color: #333;
    text-decoration: underline;
}

.breadcrumb a:not(:last-child)::after {
    content: " / ";
    color: #999;
    margin: 0 5px;
}
```

### 示例 5：带过渡动画的链接

```css
a {
    color: #333;
    text-decoration: none;
    transition: color 0.3s ease, border-color 0.3s;
}

a:hover {
    color: #ff5722;
    border-bottom: 1px solid #ff5722;
}
```

### 示例 6：禁用链接样式（不可点击）

```css
a.disabled {
    pointer-events: none;
    color: #aaa;
}
```

### 示例 7：图标 + 链接

```css
a.icon-link::before {
    content: "👉 ";
}
```

## 关于 :visited 状态的限制

出于用户隐私和安全考虑，现代浏览器严格限制了你能为已访问链接设置的样式。通常只能修改 color， background-color， border-color 等颜色相关属性，并且不能获取这些样式的计算值（以防止通过 JavaScript 探测用户的浏览历史）。
