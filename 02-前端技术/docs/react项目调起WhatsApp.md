# react项目调起WhatsApp

说明：
> 需兼容在webview中也能调起WhatsApp并制定客服人员和预发信息


## 注意事项

iOS 的 WKWebView 对 URL Scheme 唤起有以下严格限制：

### 最严格的限制：WKWebView 只允许在直接用户交互（如点击事件）中同步调用 URL Scheme。

```js
// ✅ 允许 - 在点击事件处理器中直接调用
button.addEventListener('click', () => {
    window.location.href = 'whatsapp://send?phone=123456';
});

// ✅ 允许 - 使用 window.open
button.addEventListener('click', () => {
    window.open('whatsapp://send?phone=123456');
});

// ❌ 不允许 - 异步调用会被阻止
button.addEventListener('click', () => {
    setTimeout(() => {
        window.location.href = 'whatsapp://send?phone=123456'; // 会被阻止
    }, 100);
});

// ❌ 不允许 - 不在用户手势上下文中
window.onload = () => {
    window.location.href = 'whatsapp://send?phone=123456'; // 会被阻止
};
```

### 在 WKWebView 中，通过 iframe 加载自定义 Scheme 会受到严格限制：

```js
// ❌ 通常会被阻止
const iframe = document.createElement('iframe');
iframe.src = 'whatsapp://send?phone=123456';
document.body.appendChild(iframe);

// ✅ 可能的变通方案（但有时也会被阻止）
button.addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src = 'whatsapp://send?phone=123456';
    document.body.appendChild(iframe);
    
    setTimeout(() => {
        document.body.removeChild(iframe);
    }, 100);
});
```

### WKWebView 对 URL Scheme 调用有短暂的时间窗口（大约 1-2 秒），超出后会被阻止：

```js
// ❌ 超时太长会被阻止
button.addEventListener('click', () => {
    // 用户交互...
    // 一些其他操作...
    setTimeout(() => {
        // 如果距离点击事件超过约1-2秒，会被阻止
        window.location.href = 'whatsapp://send?phone=123456';
    }, 3000); // 太长了！
});
```

### WKWebView 默认阻止通过 window.open() 打开非 http/https 链接：

```js
// ❌ 可能会被阻止
window.open('whatsapp://send?phone=123456');

// ✅ 有时需要特殊配置
const webView = WKWebView()
webView.configuration.preferences.javaScriptCanOpenWindowsAutomatically = true
```