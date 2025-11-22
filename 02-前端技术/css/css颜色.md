# css颜色

## CSS 变量管理颜色

```html
<style>
    :root {
        --primary-color: #3498db;
        --secondary-color: #2ecc71;
        --accent-color: #e74c3c;
        --text-color: #2c3e50;
        --bg-color: #ecf0f1;
        --shadow-color: rgba(0, 0, 0, 0.1);
    }
    
    .modern-card {
        background: white;
        color: var(--text-color);
        padding: 20px;
        margin: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 10px var(--shadow-color);
        border-left: 4px solid var(--primary-color);
    }
    
    .modern-button {
        background: var(--primary-color);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: background 0.3s;
    }
    
    .modern-button:hover {
        background: #2980b9;
    }
</style>

<div class="modern-card">
    <h3>现代卡片设计</h3>
    <p>使用 CSS 变量统一管理颜色</p>
    <button class="modern-button">主要按钮</button>
</div>
```

## 透明度和混合模式

```html
<style>
    .blend-mode-example {
        width: 300px;
        height: 200px;
        background: 
            linear-gradient(45deg, #ff6b6b, #4ecdc4),
            url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="%233498db"/></svg>');
        background-blend-mode: overlay;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
</style>

<div class="blend-mode-example">
    背景混合模式效果
</div>
```

## 最佳实践

### 1. 颜色命名规范
```css
/* 好的命名 */
:root {
    --color-primary: #3498db;
    --color-success: #2ecc71;
    --color-warning: #f39c12;
    --color-danger: #e74c3c;
    --color-text: #2c3e50;
    --color-background: #ecf0f1;
}

/* 避免魔法数字 */
.button {
    background: var(--color-primary); /* 好 */
    background: #3498db; /* 避免 */
}
```

### 2. 响应式颜色方案
```css
@media (prefers-color-scheme: dark) {
    :root {
        --color-text: #ecf0f1;
        --color-background: #2c3e50;
    }
}

@media (prefers-contrast: high) {
    :root {
        --color-primary: #0066cc;
        --color-text: #000000;
    }
}
```