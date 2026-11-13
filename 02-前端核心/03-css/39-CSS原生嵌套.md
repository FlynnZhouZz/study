# CSS 原生嵌套（CSS Nesting）

## 基本语法

```css
/* 传统写法 */
.parent {
  color: red;
}

.parent .child {
  color: blue;
}

.parent:hover {
  color: green;
}

/* 使用嵌套写法 */
.parent {
  color: red;
  
  .child {
    color: blue;
  }
  
  &:hover {
    color: green;
  }
}
```

## 浏览器支持情况

当前支持状态（2024）

- Chrome 120+ ✅ 完全支持
- Firefox 117+ ✅ 完全支持
- Safari 17.2+ ✅ 完全支持
- Edge 120+ ✅ 完全支持
- Opera 106+ ✅ 完全支持

## 完整的嵌套语法

### 基本嵌套

```css
/* 元素嵌套 */
.card {
  padding: 20px;
  
  .header {
    font-size: 24px;
    
    .title {
      color: #333;
      
      span {
        font-weight: bold;
      }
    }
  }
  
  .content {
    margin-top: 10px;
    
    p {
      line-height: 1.6;
    }
  }
}
```

### 使用 `&` 符号（父选择器引用）

```css
/* 伪类和伪元素 */
.button {
  background: blue;
  color: white;
  
  &:hover {
    background: darkblue;
  }
  
  &:active {
    transform: scale(0.98);
  }
  
  &:focus {
    outline: 2px solid orange;
  }
  
  &::before {
    content: "→ ";
  }
}

/* 连接类名 */
.btn {
  &-primary {
    background: blue;
  }
  
  &-secondary {
    background: gray;
  }
  
  &-large {
    padding: 15px 30px;
    font-size: 18px;
  }
}
```

### 媒体查询嵌套

```css
.container {
  width: 100%;
  padding: 20px;
  
  @media (min-width: 768px) {
    max-width: 750px;
    margin: 0 auto;
    
    .sidebar {
      width: 250px;
      float: left;
    }
    
    .content {
      margin-left: 270px;
    }
  }
  
  @media (min-width: 1200px) {
    max-width: 1140px;
  }
}
```

### 特性查询嵌套

```css
/* 检查 Grid 支持 */
.grid {
  display: flex;
  flex-wrap: wrap;
  
  @supports (display: grid) {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    
    & > .item {
      margin: 0;
    }
  }
}
```

### 复杂选择器嵌套

```css
/* 相邻兄弟选择器 */
h1 {
  color: #333;
  
  + p {
    margin-top: 10px;
    color: #666;
  }
}

/* 通用兄弟选择器 */
h2 {
  color: #222;
  
  ~ p {
    font-style: italic;
  }
}

/* 属性选择器嵌套 */
input {
  border: 1px solid #ccc;
  
  &[type="text"] {
    width: 200px;
  }
  
  &[type="checkbox"] {
    width: 20px;
    height: 20px;
  }
}
```

## 与 `Sass`/`Less` 嵌套的区别

### 相似之处

```css
/* Sass 和 CSS 原生嵌套看起来相似 */
.card {
  .title {
    color: red;
  }
}
```

### `&` 符号的必须性（重要区别！）

```css
/* ✅ CSS 原生嵌套：必须使用 & 来连接选择器 */
.component {
  &__part {
    color: red;
  }
}

/* ❌ 这会出错（在 CSS 中） */
.component {
  __part {  /* 无效！需要 & */
    color: red;
  }
}

/* ✅ 这样可以 */
.component {
  .part {  /* 有效：空格表示后代 */
    color: red;
  }
}
```

### 嵌套规则的位置

```css
/* CSS 原生嵌套：嵌套必须放在前面 */
.card {
  color: black;  /* 属性 */
  
  .title {       /* 嵌套规则必须放在所有属性之后 */
    color: red;
  }
}
.card1 {
  /* ❌ 这样会无效 */
  .title {
    color: red;
  }
  
  color: black;  /* 错误：属性不能在嵌套规则之后 */
}

/* Sass 允许更灵活的顺序 */
```

### `@`规则嵌套

```css
/* CSS 原生支持嵌套的 @规则 */
.container {
  @media (min-width: 768px) {
    padding: 40px;
    
    .item {
      width: 50%;
    }
  }
}

/* 不支持所有 @规则嵌套 */
.container {
  @keyframes slide {  /* 这个可能有问题 */
    from { opacity: 0; }
    to { opacity: 1; }
  }
}
```

## 注意事项

- 不要过度嵌套（保持深度在3层以内）

- 注意选择器特异性

```css
/* 嵌套会增加特异性 */
#header {
  .nav { /* 特异性: 1,1,0 */
    color: blue;
  }
}

/* 可能覆盖不了这个 */
.nav { /* 特异性: 0,1,0 */
  color: red; /* 这个不会生效 */
}
```

- 性能考虑
    - 深层嵌套可能影响性能
    - 浏览器从右向左解析选择器

## 最佳实践

- 使用 BEM 命名约定结合嵌套
- 将嵌套深度限制在3-4层
- 使用 `PostCSS` 处理兼容性（如果需要支持旧浏览器）
- 利用现代构建工具（Vite、Parcel等）自动处理

## 向后兼容方案

### 使用 PostCSS

```json
// package.json
{
  "devDependencies": {
    "postcss": "^8.0.0",
    "postcss-preset-env": "^8.0.0"
  },
  "postcss": {
    "plugins": {
      "postcss-preset-env": {
        "stage": 1,
        "features": {
          "nesting-rules": true
        }
      }
    }
  }
}
```

### 降级编译示例

```css
/* 你写的现代 CSS（使用嵌套） */
.card {
  padding: 20px;
  
  & .title {
    color: red;
  }
  
  &:hover {
    background: blue;
  }
}

/* PostCSS 会编译成 */
.card {
  padding: 20px;
}

.card .title {
  color: red;
}

.card:hover {
  background: blue;
}
```
