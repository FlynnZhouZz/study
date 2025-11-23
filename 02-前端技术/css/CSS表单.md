# CSS 表单

CSS 表单样式（Form Styling），包括常用表单元素、样式属性、伪类和实战技巧，让表单既美观又易用。

## 常见表单元素

| 元素         | 描述                             |
| ------------ | -------------------------------- |
| `<input>`    | 文本框、密码框、复选框、单选框等 |
| `<textarea>` | 多行文本输入框                   |
| `<select>`   | 下拉列表                         |
| `<option>`   | 下拉列表选项                     |
| `<button>`   | 按钮                             |
| `<label>`    | 标签文字，通常和 input 绑定      |

## 常用伪类

| 伪类            | 描述             | 示例                                                            |
| --------------- | ---------------- | --------------------------------------------------------------- |
| `:focus`        | 聚焦时样式       | `input:focus { border-color: #4caf50; }`                        |
| `:hover`        | 鼠标悬停         | `button:hover { background-color: #45a049; }`                   |
| `:checked`      | 复选框或单选选中 | `input[type="checkbox"]:checked { background-color: #4caf50; }` |
| `:disabled`     | 禁用状态         | `input:disabled { background-color: #eee; }`                    |
| `::placeholder` | 占位符文字       | `input::placeholder { color: #aaa; }`                           |

## 基础表单元素样式

### 1. 输入框样式

```css
/* 基础输入框样式 */
.form-input {
    width: 100%;
    padding: 12px 16px;
    font-size: 16px; /* 防止iOS缩放 */
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    background-color: #fff;
    transition: all 0.3s ease;
    box-sizing: border-box;
}

.form-input:focus {
    outline: none;
    border-color: #4d90fe;
    box-shadow: 0 0 0 3px rgba(77, 144, 254, 0.2);
}

.form-input:hover {
    border-color: #c6c6c6;
}
```

### 2. 标签样式

```css
.form-label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #2d3748;
    font-size: 14px;
}

/* 必填字段标记 */
.required::after {
    content: " *";
    color: #e53e3e;
}
```

### 3. 按钮样式

```css
.form-button {
    width: 100%;
    padding: 14px 24px;
    background: #3182ce;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.form-button:hover {
    background: #2c5aa0;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(49, 130, 206, 0.3);
}

.form-button:active {
    transform: translateY(0);
}

.form-button:disabled {
    background: #a0aec0;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}
```

## 自定义表单控件

### 1. 自定义复选框

```css
.checkbox-label {
    display: flex;
    align-items: center;
    cursor: pointer;
    font-size: 14px;
}

.checkbox-input {
    display: none;
}

.checkbox-custom {
    width: 18px;
    height: 18px;
    border: 2px solid #cbd5e0;
    border-radius: 4px;
    margin-right: 8px;
    position: relative;
    transition: all 0.3s ease;
}

.checkbox-input:checked + .checkbox-custom {
    background: #3182ce;
    border-color: #3182ce;
}

.checkbox-input:checked + .checkbox-custom::after {
    content: "✓";
    position: absolute;
    color: white;
    font-size: 12px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.checkbox-input:focus + .checkbox-custom {
    box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.2);
}
```

### 2. 自定义单选按钮

```css
.radio-label {
    display: flex;
    align-items: center;
    cursor: pointer;
    margin-bottom: 12px;
}

.radio-input {
    display: none;
}

.radio-custom {
    width: 18px;
    height: 18px;
    border: 2px solid #cbd5e0;
    border-radius: 50%;
    margin-right: 8px;
    position: relative;
    transition: all 0.3s ease;
}

.radio-input:checked + .radio-custom {
    border-color: #3182ce;
}

.radio-input:checked + .radio-custom::after {
    content: "";
    position: absolute;
    width: 8px;
    height: 8px;
    background: #3182ce;
    border-radius: 50%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
```

### 3. 自定义选择框

```css
.select-wrapper {
    position: relative;
}

.select-wrapper::after {
    content: "▼";
    position: absolute;
    top: 50%;
    right: 16px;
    transform: translateY(-50%);
    color: #718096;
    pointer-events: none;
    font-size: 12px;
}

.form-select {
    width: 100%;
    padding: 12px 16px;
    font-size: 16px;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    background-color: #fff;
    appearance: none;
    cursor: pointer;
    transition: all 0.3s ease;
}

.form-select:focus {
    outline: none;
    border-color: #4d90fe;
    box-shadow: 0 0 0 3px rgba(77, 144, 254, 0.2);
}
```

## 表单验证样式

### 1. 实时验证反馈

```css
/* 有效状态 */
.form-input:valid {
    border-color: #38a169;
}

.form-input:valid:focus {
    box-shadow: 0 0 0 3px rgba(56, 161, 105, 0.2);
}

/* 无效状态 */
.form-input:invalid:not(:focus):not(:placeholder-shown) {
    border-color: #e53e3e;
}

/* 错误消息 */
.error-message {
    color: #e53e3e;
    font-size: 12px;
    margin-top: 4px;
    display: none;
}

.form-input:invalid:not(:focus):not(:placeholder-shown) + .error-message {
    display: block;
}

/* 成功消息 */
.success-message {
    color: #38a169;
    font-size: 12px;
    margin-top: 4px;
    display: none;
}

.form-input:valid:not(:placeholder-shown) + .success-message {
    display: block;
}
```

### 2. 自定义验证样式

```html
<div class="form-group">
    <label for="email" class="form-label">电子邮箱</label>
    <input type="email" id="email" class="form-input" placeholder="请输入邮箱地址" required />
    <div class="error-message">请输入有效的邮箱地址</div>
    <div class="success-message">邮箱格式正确</div>
</div>
```

## 高级表单样式

### 1. 浮动标签效果

```html
<div class="float-label-group">
    <input type="text" id="name" class="float-input" placeholder=" " />
    <label for="name" class="float-label">姓名</label>
</div>
```

```css
.float-label-group {
    position: relative;
    margin-bottom: 24px;
}

.float-input {
    width: 100%;
    padding: 18px 16px 8px;
    font-size: 16px;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    background: #fff;
    transition: all 0.3s ease;
}

.float-label {
    position: absolute;
    top: 18px;
    left: 16px;
    color: #718096;
    font-size: 16px;
    pointer-events: none;
    transition: all 0.3s ease;
}

.float-input:focus {
    outline: none;
    border-color: #4d90fe;
    padding-top: 22px;
    padding-bottom: 4px;
}

.float-input:focus + .float-label,
.float-input:not(:placeholder-shown) + .float-label {
    top: 6px;
    left: 16px;
    font-size: 12px;
    color: #4d90fe;
}
```

### 2. 搜索框样式

```css
.search-container {
    position: relative;
    max-width: 400px;
}

.search-input {
    width: 100%;
    padding: 12px 48px 12px 16px;
    border: 2px solid #e1e5e9;
    border-radius: 24px;
    font-size: 16px;
    transition: all 0.3s ease;
}

.search-input:focus {
    outline: none;
    border-color: #4d90fe;
    box-shadow: 0 0 0 3px rgba(77, 144, 254, 0.2);
}

.search-button {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    background: #3182ce;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.search-button:hover {
    background: #2c5aa0;
    transform: translateY(-50%) scale(1.05);
}
```

### 3. 文件上传样式

```css
.file-upload {
    position: relative;
    display: inline-block;
    width: 100%;
}

.file-input {
    position: absolute;
    left: -9999px;
}

.file-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    border: 2px dashed #cbd5e0;
    border-radius: 8px;
    background: #f7fafc;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
}

.file-label:hover {
    border-color: #3182ce;
    background: #edf2f7;
}

.file-label.drag-over {
    border-color: #3182ce;
    background: #ebf8ff;
}

.upload-icon {
    font-size: 48px;
    color: #cbd5e0;
    margin-bottom: 16px;
}

.file-label:hover .upload-icon {
    color: #3182ce;
}
```

## 响应式表单设计

```css
/* 移动端优先 */
.form-container {
    padding: 20px;
    margin: 20px;
}

.form-group {
    margin-bottom: 20px;
}

/* 平板 */
@media (min-width: 768px) {
    .form-container {
        padding: 40px;
        margin: 40px auto;
    }

    .form-row {
        display: flex;
        gap: 20px;
    }

    .form-row .form-group {
        flex: 1;
        margin-bottom: 0;
    }
}

/* 桌面端 */
@media (min-width: 1024px) {
    .form-container {
        max-width: 500px;
    }
}

/* 横屏移动设备 */
@media (max-height: 500px) and (orientation: landscape) {
    .form-container {
        margin: 10px auto;
        padding: 20px;
    }

    .form-group {
        margin-bottom: 15px;
    }
}
```

## 表单状态和交互

### 1. 加载状态

```css
.form-button.loading {
    position: relative;
    color: transparent;
}

.form-button.loading::after {
    content: "";
    position: absolute;
    width: 20px;
    height: 20px;
    top: 50%;
    left: 50%;
    margin: -10px 0 0 -10px;
    border: 2px solid #ffffff;
    border-radius: 50%;
    border-right-color: transparent;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}
```

### 2. 成功/错误状态

```css
.form-message {
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 14px;
}

.form-message.success {
    background: #f0fff4;
    border: 1px solid #9ae6b4;
    color: #276749;
}

.form-message.error {
    background: #fed7d7;
    border: 1px solid #feb2b2;
    color: #c53030;
}

.form-message.warning {
    background: #fffaf0;
    border: 1px solid #fbd38d;
    color: #dd6b20;
}
```
