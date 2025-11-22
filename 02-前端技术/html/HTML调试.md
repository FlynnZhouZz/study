# HTML调试

HTML 调试是前端开发中的重要技能，涉及多种工具和技巧来识别和修复问题。

## 一、浏览器开发者工具

### 1. 打开方式
- F12 或 Ctrl+Shift+I (Windows/Linux)
- Cmd+Opt+I (Mac)
- 右键 → "检查" 或 "审查元素"

### 2. 元素面板 (Elements)

查看和编辑 HTML 结构。

```html
<!-- 在 Elements 面板中可以看到 -->
<div class="container" id="main">
    <h1 data-testid="title">页面标题</h1>
    <p class="text">段落内容</p>
    <!-- 注释也会显示 -->
</div>
```

## 二、常见 HTML 错误及调试

- 标签未闭合
- 属性语法错误
- 嵌套错误

## 三、验证工具

### W3C 验证器
```html
<!-- 在 https://validator.w3.org/ 检查 -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>待验证的页面</title>
</head>
<body>
    <h1>页面标题</h1>
    <!-- 故意制造错误 -->
    <div><p>未闭合的段落
</body>
</html>
```

### 浏览器内置验证

```html
<form id="myForm">
    <input type="email" required placeholder="输入邮箱">
    <input type="submit" value="提交">
</form>

<script>
// 检查表单验证
const form = document.getElementById('myForm');
console.log('表单验证状态:', form.checkValidity());
</script>
```

## 高级调试技巧

### 1. 性能调试
```html
<script>
// 测量 DOM 加载时间
const startTime = performance.now();

document.addEventListener('DOMContentLoaded', () => {
    const loadTime = performance.now() - startTime;
    console.log(`DOM 加载时间: ${loadTime.toFixed(2)}ms`);
});

// 检查重绘和回流
const element = document.getElementById('myElement');
const rect = element.getBoundingClientRect();
console.log('元素位置:', rect);
</script>
```

### 2. 网络请求调试
```html
<script>
// 检查所有资源加载
window.addEventListener('load', () => {
    const resources = performance.getEntriesByType('resource');
    resources.forEach(resource => {
        console.log(`${resource.name}: ${resource.duration.toFixed(2)}ms`);
    });
});

// 图片加载监控
document.addEventListener('DOMContentLoaded', () => {
    const images = document.getElementsByTagName('img');
    Array.from(images).forEach(img => {
        img.addEventListener('load', () => {
            console.log(`图片加载成功: ${img.src}`);
        });
        img.addEventListener('error', () => {
            console.error(`图片加载失败: ${img.src}`);
        });
    });
});
</script>
```

### 3. 错误边界调试
```html
<div id="error-boundary">
    <!-- 可能出错的内容 -->
</div>

<script>
// 全局错误处理
window.addEventListener('error', (event) => {
    console.error('全局错误:', event.error);
    // 可以发送到错误监控服务
});

// 特定区域错误处理
const errorBoundary = document.getElementById('error-boundary');
try {
    // 可能出错的代码
    errorBoundary.innerHTML = '<script>undefinedFunction()</script>';
} catch (error) {
    console.error('边界错误:', error);
    errorBoundary.innerHTML = '<p>内容加载失败</p>';
}
</script>
```

## 实用调试工具推荐

### 1. 浏览器扩展

- Web Developer - 多功能开发工具
- HTML Validator - 实时HTML验证
- PerfectPixel - 像素级对比调试

### 2. 在线工具

- W3C Validator - HTML验证
- WebPageTest - 性能测试
- BrowserStack - 跨浏览器测试
