# HTML 头部

`<head>` 元素是 HTML 文档的“大脑”和“元信息中心”，它包含了所有不会直接显示在网页正文中的信息。这些信息是为浏览器、搜索引擎和其他网络服务提供的指令和数据。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <!-- 所有的元信息、标题、链接和脚本都放在这里 -->
    
    <!-- 1. 字符编码声明 -->
    <meta charset="UTF-8">
    
    <!-- 2. 视口设置 (针对移动设备) -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- 3. 网页标题 -->
    <title>我的网站 - 首页</title>
    
    <!-- 4. 网页描述 -->
    <meta name="description" content="这是一个关于前端技术和网页设计的精彩网站。">
    
    <!-- 5. 引入CSS样式表 -->
    <link rel="stylesheet" href="styles.css">
    
    <!-- 6. 网站图标 -->
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    
    <!-- 其他元标签、预连接、脚本等 -->
</head>
<body>
    <!-- 网页的可见内容在这里 -->
</body>
</html>
```

## 各部分详解

1. 字符编码 `<meta charset="UTF-8">`

- 作用：告诉浏览器使用哪种字符编码来解析页面。
- 重要性：必须放在 `<head>` 的最前面，避免出现乱码。`UTF-8` 是国际通用的编码，支持几乎所有语言的字符。

2. 视口设置 `<meta name="viewport" ...>`

- 作用：控制网页在移动设备上的布局和缩放。
- 重要性：响应式网页设计的基石。没有它，移动设备会按照桌面宽度渲染页面，导致用户需要手动缩放。
- `width=device-width`：让视口宽度等于设备宽度。
- `initial-scale=1.0`：设置页面的初始缩放级别为 1。

3. 网页标题 `<title>`

- 作用：定义浏览器标签页上显示的标题，也是搜索引擎结果列表中的主要标题。
- 重要性：对 SEO（搜索引擎优化）和用户体验至关重要。应简洁、描述性强且包含关键词。

4. 网页描述 `<meta name="description" ...>`

- 作用：提供一段关于网页内容的简短描述。
- 重要性：搜索引擎常常在搜索结果中显示这段描述。虽然不直接影响排名，但好的描述能提高点击率。

5. 引入外部资源 `<link>`
```html
<!-- 引入css -->
<link rel="stylesheet" href="styles/main.css">

<!-- 引入网站图标Favicon -->
<link rel="icon" href="images/favicon.ico">
<!-- 对于现代浏览器，推荐使用 PNG 或 SVG -->
<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32x32.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
```

6. 其他常用 `<meta>` 标签
```html
<!-- 作者和信息 -->
<meta name="author" content="你的名字">
<meta name="keywords" content="关键词1, 关键词2, 关键词3"> <!-- 对现代SEO影响很小，可省略 -->

<!-- 控制搜索引擎索引 -->
<meta name="robots" content="index, follow"> <!-- 默认值，允许收录和跟踪链接 -->
<meta name="robots" content="noindex, nofollow"> <!-- 禁止收录和跟踪链接 -->
```

7. 引入 JavaScript

最佳实践：通常把 `<script>` 标签放在 `<body>` 的末尾，以避免阻塞页面渲染。但如果脚本对渲染至关重要，或者使用 async/defer 属性，也可以放在 `<head>` 中。
```html
<!-- 放在 head 中，但使用 defer 使其不阻塞渲染 -->
<script src="script.js" defer></script>
```

8. Open Graph 协议 (用于社交媒体分享)
```html
<meta property="og:title" content="我的网站 - 首页">
<meta property="og:description" content="这是一个关于前端技术和网页设计的精彩网站。">
<meta property="og:image" content="https://example.com/images/og-image.jpg">
<meta property="og:url" content="https://example.com">
```

9. 预连接和预加载 (优化性能)
```html
<!-- 预连接，提前建立与重要第三方域的连接 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- 预加载关键资源 -->
<link rel="preload" href="critical-font.woff2" as="font" type="font/woff2" crossorigin>
```

10. 规范化链接 (Canonical URL)
```html
<link rel="canonical" href="https://example.com/standard-version-of-this-page">
```

11. 为文档设定主语言
```html
<html lang="zh-CN">
  …
</html>
```