# URL

## 概述

URL（统一资源定位符）是因特网中的唯一资源的地址。它是浏览器用于检索已发布资源（例如 HTML 页面、CSS 文档、图像等）的关键机制之一。 <br>
理论上说，每个有效的 URL 都指向一个唯一的资源。

## 剖析 URL

例子：
`https://www.example.com:443/docs/tutorial/index.html?lang=zh&page=1#chapter1`

| 部分 | 例子 | 功能说明 |
| -- | -- | -- |
| 协议 | https:// | 规定使用哪种协议访问资源。常见的有 http、https（加密的HTTP）、ftp等。浏览器和服务器根据协议来通信。://是固定分隔符。 |
| 主机名 | www.example.com | 指定资源所在的服务器。通常是一个域名，也可以直接使用IP地址。 |
| 端口 | :443 | 指定连接到服务器上的哪个网络服务。https 的默认端口是 443，http 是 80。因为默认，所以这个部分通常被省略。 |
| 路径 | /docs/tutorial/index.html | 表示资源在服务器上的具体位置，就像电脑上的文件路径一样。它指向一个具体的页面、图片或文件。 |
| 查询参数 | ?lang=zh&page=1 | 在 ? 之后，用于向服务器提供额外参数。格式是 键=值，多个参数用 & 连接。例如，这个URL告诉服务器：需要中文版本，并且跳转到第一页。 |
| 锚点 | #chapter1 | 在 # 之后，它不会发送给服务器。其作用是让浏览器直接跳转到页面内的某个特定位置（如一个标题或章节）。 |

## 绝对URL和相对URL

### 绝对URL

绝对URL提供了资源的完整路径，包含了访问该资源所需的所有部分。

结构：`协议://主机名:端口/路径?查询参数#锚点`

示例： <br>
https://www.example.com/images/logo.png <br>
https://blog.example.com/articles/index.html <br>
//cdn.example.com/script.js (这是一种特殊的协议相对URL，它会继承当前页面的协议（HTTP或HTTPS），现在已不推荐使用)。

特点与用法：

独立性：它不依赖于任何上下文，可以在任何地方使用——无论是另一个网站、电子邮件、文档或二维码——都能准确定位到资源。

用于外部资源：当你的网站需要链接到另一个域名下的资源时，必须使用绝对URL。
```html
<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<a href="https://twitter.com/your_profile">关注我们</a>
```

### 相对URL

相对URL只提供了资源的部分路径，它需要与当前页面的基础URL结合起来，才能形成完整的地址。

基础URL（Base URL）：通常是当前正在浏览的网页的URL。

相对URL主要有以下几种形式：

1. 相对于根目录的相对URL

以 斜杠 / 开头。它表示从网站的根域名开始计算路径。

- 基础URL： https://www.example.com/shop/electronics/index.html
- 相对URL： /images/banner.jpg
- 解析结果： https://www.example.com/images/banner.jpg

2. 相对于当前目录的相对URL

不以斜杠开头。它表示从当前页面所在的目录开始计算路径。

- 基础URL： https://www.example.com/shop/electronics/index.html
- 相对URL： ./iphone14.html 或 iphone14.html (. 代表当前目录，通常可省略)
- 解析结果： https://www.example.com/shop/electronics/iphone14.html

3. 指向上级目录的相对URL

使用 ../ 来表示“向上移动一级目录”。

- 基础URL： https://www.example.com/shop/electronics/index.html
- 相对URL： ../furniture/sofas.html (先从中跳出/electronics/目录，再进入/furniture/目录)
- 解析结果： https://www.example.com/shop/furniture/sofas.html

## 语义 URL

语义URL，也称为语义化URL或友好URL，指的是其路径和结构能够清晰地向人类和机器（如搜索引擎）传达页面内容主题的URL。

简单来说，就是“一看就懂”的网址。

### 语义URL的特点与构成

一个良好的语义URL通常包含与页面内容相关的关键词，并使用易于理解的单词和逻辑结构。

| 非语义URL (不友好) | 语义URL (友好) |
| -- | -- |
| https://example.com/p?id=123&cat=5 | https://example.com/products/iphone-15 |
| https://example.com/blog/post.php?p=789 | https://example.com/blog/how-to-bake-a-cake |
| https://example.com/cgi-bin/article?lang=zh&id=456 | https://example.com/guides/web-design/semantic-urls |

- 非语义URL：使用了技术参数（id, cat, p），无法从中获取任何关于页面内容的信息。
- 语义URL：即使不看网页标题，你也能猜到第一个链接是关于“iPhone 15”的产品页，第二个是关于“如何烘焙蛋糕”的博客，第三个是关于“语义URL”的指南，并且位于“Web设计”分类下。

### 为什么语义URL如此重要？

1. 用户体验

可读性强、易于记忆和分享、可操作性强

2. 搜索引擎优化

- 关键词权重：URL本身是搜索引擎排名的一个因素。包含目标关键词的语义URL可以向搜索引擎清晰地传递页面主题。
- 点击率：在搜索结果中，一个清晰、描述性的URL比一堆乱码更能吸引用户点击，从而提高点击率，而高点击率是重要的排名信号。
- 结构化数据：像 .../category/subcategory/product 这样的层次结构，有助于搜索引擎理解网站的信息架构。

3. 可维护性与可访问性

- 开发与内容管理：对于开发者和内容管理者来说，清晰的URL结构使得网站内容组织一目了然，便于管理和维护。
- 辅助技术：对于使用屏幕阅读器的视障用户，听到一个描述性的URL比听到一串无意义的数字和字母要有用得多。

### 如何设计一个好的语义URL？

1. 使用描述性词语：在路径中使用能准确描述页面内容的英文单词或拼音。

- 好：/contact-us
- 差：/page1

2. 保持简洁明了：避免过长和冗余的词汇。只包含必要的关键词。

- 好：/cars/electric/tesla-model-3
- 差：/vehicles/cars/electric-cars/tesla/model-3-review-article

3. 使用连字符分隔单词：这是Web标准的最佳实践。避免使用下划线 _ 或空格 %20。

- 好：/my-favorite-books
- 差：/my_favorite_books 或 /my%20favorite%20books

4. 采用逻辑层次结构：像文件夹一样组织你的URL，体现从一般到具体的关系。

- 示例：/blog/2024/web-design-trends
- 这个结构清晰地表示：这是博客栏目下，2024年发布的，一篇关于网页设计趋势的文章。

5. 避免使用动态参数：尽量将 ?id=123&category=abc 这样的参数重写为友好的路径形式。这通常需要通过服务器的 URL重写 功能（如Apache的 mod_rewrite 或Nginx的 rewrite 规则）来实现。

6. 使用小写字母：统一使用小写字母可以避免因大小写混淆而导致的访问错误（有些服务器系统是大小写敏感的）。

### 技术实现：如何创建语义URL？

非语义URL通常是由动态网站（如PHP、Python、Java等）生成的。要将其变为语义URL，需要进行 URL重写。

原理：服务器端通过规则，将用户看到的“友好URL”在内部映射到处理该请求的真实脚本和参数。

示例（Apache的 .htaccess 文件）：
```apache
# 将 "example.com/product.php?id=123" 重写为 "example.com/product/123"
RewriteEngine On
RewriteRule ^product/([0-9]+)/?$ product.php?id=$1 [L]

# 更高级的例子：将 "example.com/articles/how-to-bake-a-cake" 映射到 "example.com/article.php?slug=how-to-bake-a-cake"
RewriteRule ^articles/([a-zA-Z0-9-]+)/?$ article.php?slug=$1 [L]
```

示例Nginx：

目标：<br>
将用户访问的友好URL：https://example.com/product/123<br>
在内部映射到：/product.php?id=123

```nginx
server {
    listen 80;
    server_name example.com;
    
    # 定义网站的根目录
    root /var/www/html;
    index index.php index.html index.htm;

    # 位置块用于匹配 product/ 后跟一个数字的URL
    location ~ ^/product/(\d+)/?$ {
        # 将请求重写到 product.php，并传递 id 参数
        # $1 代表前面正则表达式捕获的第一个分组，即 (\d+)
        try_files $uri $uri/ /product.php?id=$1;
    }

    # 处理PHP文件的配置
    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        # 非常重要：告诉PHP脚本实际要执行的文件名
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}
```

使用 try_files 实现「前端控制器」模式（最常用于现代框架）
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/laravel/public; # 注意：根目录指向了 public 文件夹
    index index.php index.html;

    # 处理所有请求
    location / {
        # 首先尝试将请求作为文件或目录处理；
        # 如果找不到，则重写URL，将请求发送到 index.php
        # $query_string 用于保留原始的GET参数
        try_files $uri $uri/ /index.php?$query_string;
    }

    # 处理PHP文件
    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_index index.php;
        # 防止执行不存在的PHP文件
        try_files $uri =404;
    }

    # 禁止访问 .htaccess 或其他隐藏文件
    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

现代Web框架（如 Django, Ruby on Rails, Laravel, Express.js 等）都内置了非常便捷的路由功能，可以让你轻松地定义出语义化的URL结构，而无需手动配置复杂的重写规则。