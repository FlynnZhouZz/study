# 框架 `<iframe>`

`<iframe>`（内联框架）用于在网页中嵌入另一个网页。

## 基本语法

### 最简单的使用
```html
<iframe src="https://example.com"></iframe>
```

### 带尺寸和边框
```html
<iframe 
    src="embedded-page.html"
    width="800"
    height="600"
    frameborder="0">
</iframe>
```

## 核心属性详解

### 1. src - 嵌入页面地址
```html
<!-- 外部网站 -->
<iframe src="https://www.wikipedia.org"></iframe>

<!-- 相对路径 -->
<iframe src="local-page.html"></iframe>

<!-- 绝对路径 -->
<iframe src="/pages/embedded.html"></iframe>

<!-- 空框架 -->
<iframe src="about:blank"></iframe>
```

### 2. width 和 height - 尺寸控制
```html
<!-- 固定像素 -->
<iframe src="content.html" width="300" height="200"></iframe>

<!-- 百分比 -->
<iframe src="content.html" width="100%" height="500"></iframe>

<!-- 通过 CSS 控制 -->
<iframe src="content.html" style="width: 100%; height: 400px;"></iframe>
```

### 3. name - 框架名称
```html
<!-- 命名框架 -->
<iframe src="default.html" name="contentFrame"></iframe>

<!-- 链接目标指向该框架 -->
<a href="page1.html" target="contentFrame">在框架中打开</a>
<a href="page2.html" target="contentFrame">另一个页面</a>
```

### 4. srcdoc - 内联 HTML 内容
```html
<iframe srcdoc="
    <!DOCTYPE html>
    <html>
    <head><title>内嵌内容</title></head>
    <body>
        <h1>Hello World!</h1>
        <p>这是直接嵌入的HTML内容</p>
    </body>
    </html>
"></iframe>
```

### 5. sandbox - 安全沙箱
```html
<!-- 最严格的沙箱 -->
<iframe src="untrusted.html" sandbox></iframe>

<!-- 允许特定功能 -->
<iframe src="content.html" sandbox="allow-scripts allow-forms"></iframe>

<!-- 常用沙箱配置 -->
<iframe src="content.html" sandbox="allow-scripts allow-same-origin allow-forms"></iframe>
```

沙箱属性值：

- allow-forms - 允许表单提交
- allow-scripts - 允许执行脚本
- allow-same-origin - 允许同源访问
- allow-popups - 允许弹出窗口
- allow-top-navigation - 允许导航顶级页面

### 6. allow - 功能策略
```html
<!-- 允许全屏 -->
<iframe src="video.html" allow="fullscreen"></iframe>

<!-- 允许支付请求 -->
<iframe src="payment.html" allow="payment"></iframe>

<!-- 多个权限 -->
<iframe src="app.html" allow="camera; microphone; geolocation"></iframe>
```

### 7. loading - 加载行为
```html
<!-- 延迟加载 -->
<iframe src="heavy-content.html" loading="lazy"></iframe>

<!-- 立即加载 -->
<iframe src="important-content.html" loading="eager"></iframe>
```

## 实际应用场景

### 1. 嵌入第三方服务
```html
<!-- 嵌入 YouTube 视频 -->
<iframe 
    width="560" 
    height="315" 
    src="https://www.youtube.com/embed/视频ID" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen>
</iframe>

<!-- 嵌入 Google 地图 -->
<iframe
    src="https://www.google.com/maps/embed?pb=地图参数"
    width="600"
    height="450"
    style="border:0;"
    allowfullscreen=""
    loading="lazy">
</iframe>

<!-- 嵌入在线文档 -->
<iframe
    src="https://docs.google.com/document/d/文档ID/preview"
    width="100%"
    height="600"
    frameborder="0">
</iframe>
```

### 2. 创建多页面应用
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .sidebar { float: left; width: 200px; }
        .content { margin-left: 220px; }
        iframe { border: 1px solid #ccc; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h3>导航菜单</h3>
        <ul>
            <li><a href="home.html" target="mainFrame">首页</a></li>
            <li><a href="about.html" target="mainFrame">关于我们</a></li>
            <li><a href="services.html" target="mainFrame">服务</a></li>
            <li><a href="contact.html" target="mainFrame">联系我们</a></li>
        </ul>
    </div>
    
    <div class="content">
        <iframe 
            src="home.html"
            name="mainFrame"
            width="100%"
            height="600"
            frameborder="0">
        </iframe>
    </div>
</body>
</html>
```

### 3. 动态内容加载
```html
<!DOCTYPE html>
<html>
<head>
    <script>
        function loadPage(url) {
            document.getElementById('contentFrame').src = url;
        }
        
        function showCustomContent() {
            const iframe = document.getElementById('contentFrame');
            iframe.srcdoc = `
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { 
                            font-family: Arial; 
                            padding: 20px; 
                            background: #f0f0f0;
                        }
                        h1 { color: #333; }
                    </style>
                </head>
                <body>
                    <h1>动态生成的内容</h1>
                    <p>当前时间: ${new Date().toLocaleString()}</p>
                    <button onclick="alert('来自iframe的消息!')">点击我</button>
                </body>
                </html>
            `;
        }
    </script>
</head>
<body>
    <button onclick="loadPage('page1.html')">加载页面1</button>
    <button onclick="loadPage('page2.html')">加载页面2</button>
    <button onclick="showCustomContent()">显示动态内容</button>
    
    <iframe 
        id="contentFrame"
        src="about:blank"
        width="100%"
        height="400"
        style="border: 1px solid #ddd; margin-top: 10px;">
    </iframe>
</body>
</html>
```

## JavaScript 交互

### 1. 访问 iframe 内容
```html
<!-- 主页面 -->
<iframe id="myFrame" src="child.html"></iframe>

<script>
    const iframe = document.getElementById('myFrame');
    
    // 等待 iframe 加载完成
    iframe.addEventListener('load', function() {
        try {
            // 访问 iframe 的文档
            const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
            const iframeWindow = iframe.contentWindow;
            
            // 修改 iframe 内容
            iframeDoc.body.style.backgroundColor = 'lightblue';
            
            // 调用 iframe 中的函数
            iframeWindow.someFunctionInIframe();
            
        } catch (e) {
            console.log('同源策略限制:', e);
        }
    });
</script>
```

### 2. 跨文档消息传递
```html
<!-- 主页面 -->
<iframe id="childFrame" src="child.html"></iframe>

<script>
    const iframe = document.getElementById('childFrame');
    
    // 向 iframe 发送消息
    function sendToIframe(message) {
        iframe.contentWindow.postMessage(message, '*');
    }
    
    // 接收来自 iframe 的消息
    window.addEventListener('message', function(event) {
        console.log('收到消息:', event.data);
        
        // 验证来源（可选）
        if (event.origin !== 'https://expected-domain.com') return;
        
        // 处理消息
        if (event.data.type === 'userAction') {
            handleUserAction(event.data.payload);
        }
    });
</script>

<!-- child.html (iframe 内容) -->
<script>
    // 向父页面发送消息
    function sendToParent(message) {
        window.parent.postMessage(message, '*');
    }
    
    // 接收父页面消息
    window.addEventListener('message', function(event) {
        console.log('iframe收到:', event.data);
    });
    
    // 示例：发送用户操作
    document.getElementById('someButton').addEventListener('click', function() {
        sendToParent({
            type: 'userAction',
            payload: { action: 'buttonClick', value: 'hello' }
        });
    });
</script>
```

## 响应式 iframe

### 1. 保持宽高比
```html
<style>
    .responsive-iframe-container {
        position: relative;
        width: 100%;
        height: 0;
        padding-bottom: 56.25%; /* 16:9 宽高比 */
    }
    
    .responsive-iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
    }
</style>

<div class="responsive-iframe-container">
    <iframe 
        class="responsive-iframe"
        src="https://www.youtube.com/embed/视频ID"
        allowfullscreen>
    </iframe>
</div>
```

### 2. 多种宽高比
```html
<style>
    /* 16:9 (视频) */
    .aspect-16-9 { padding-bottom: 56.25%; }
    
    /* 4:3 (传统屏幕) */
    .aspect-4-3 { padding-bottom: 75%; }
    
    /* 1:1 (正方形) */
    .aspect-1-1 { padding-bottom: 100%; }
    
    /* 21:9 (超宽屏) */
    .aspect-21-9 { padding-bottom: 42.85%; }
</style>

<div class="responsive-iframe-container aspect-16-9">
    <iframe src="video.html" class="responsive-iframe"></iframe>
</div>
```

## 安全最佳实践

### 1. 安全的 iframe 配置
```html
<!-- 推荐的安全配置 -->
<iframe
    src="https://trusted-domain.com/content"
    sandbox="allow-scripts allow-same-origin allow-forms"
    allow="fullscreen"
    referrerpolicy="no-referrer"
    loading="lazy"
    title="安全嵌入内容">
</iframe>
```

### 2. 防止点击劫持
```html
<!-- 在嵌入的页面中添加 -->
<style>
    /* 防止在 iframe 中显示 */
    body {
        header: X-Frame-Options: DENY;
    }
</style>

<script>
    // 或者通过 JavaScript
    if (window !== window.top) {
        window.top.location = window.location;
    }
</script>
```

## 错误处理

### 1. 加载失败处理
```html
<iframe 
    src="https://example.com/might-fail"
    onerror="handleIframeError(this)">
</iframe>

<script>
    function handleIframeError(iframe) {
        console.error('iframe 加载失败');
        iframe.srcdoc = `
            <html>
            <body style="text-align: center; padding: 20px;">
                <h3>内容加载失败</h3>
                <p>请检查网络连接或稍后重试</p>
                <button onclick="window.location.reload()">重新加载</button>
            </body>
            </html>
        `;
    }
</script>
```

## 性能优化

### 1. 延迟加载
```html
<!-- 视口外 iframe 延迟加载 -->
<iframe 
    src="heavy-content.html" 
    loading="lazy"
    width="600" 
    height="400">
</iframe>
```

### 2. 按需加载
```html
<button onclick="loadIframe()">点击加载内容</button>
<div id="iframeContainer"></div>

<script>
    function loadIframe() {
        const container = document.getElementById('iframeContainer');
        container.innerHTML = `
            <iframe 
                src="heavy-content.html"
                width="100%"
                height="400"
                onload="console.log('iframe加载完成')">
            </iframe>
        `;
    }
</script>
```

## iframe 优缺点

### 优点

- 隔离第三方内容
- 嵌入外部服务
- 创建微前端架构
- 内容沙箱化

### 缺点

- 安全风险（使用 sandbox）
- 性能影响
- SEO 考虑
- 移动端兼容性
