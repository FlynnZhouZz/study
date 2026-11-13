# HTML 发展史

HTML（HyperText Markup Language）从简单的文档标记语言发展到现代 Web 开发的基石，经历了多个重要阶段。

## 一、前 Web 时代 (1989-1991)

### 诞生背景

- 1989年：Tim Berners-Lee 在 CERN 提出 Web 概念
- 目标：创建链接文档系统，方便科学家共享研究信息

### 第一版 HTML
```html
<!-- 最早的 HTML 文档示例 -->
<TITLE>我的第一个网页</TITLE>
<H1>欢迎来到万维网</H1>
<P>这是一个<A HREF="another.html">链接</A>到其他文档的例子。
```

## 二、HTML 2.0 (1995)

### 标准化进程
- 1995年11月：作为 RFC 1866 发布
- 首个官方标准：由 IETF 制定

### 主要特性
新增元素：`<form>, <input>, <select>, <textarea>`

```html
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<HTML>
<HEAD>
    <TITLE>HTML 2.0 示例</TITLE>
</HEAD>
<BODY>
    <H1>标题</H1>
    <P>段落文本</P>
    <UL>
        <LI>无序列表项</LI>
    </UL>
    <FORM ACTION="/submit" METHOD="POST">
        <INPUT TYPE="TEXT" NAME="username">
        <INPUT TYPE="SUBMIT" VALUE="提交">
    </FORM>
</BODY>
</HTML>
```

## 三、HTML 3.2 (1997)

### W3C 接管
- 1997年1月：W3C 发布 HTML 3.2
- 特性：引入表格、Applet、字体控制等

```html
<TABLE BORDER="1">
    <TR>
        <TD>单元格1</TD>
        <TD>单元格2</TD>
    </TR>
</TABLE>

<APPLET CODE="MyApplet.class" WIDTH="300" HEIGHT="200">
</APPLET>

<FONT FACE="Arial" SIZE="3" COLOR="red">红色文本</FONT>
```

## 四、HTML 4.01 (1999)

### 重要里程碑
- 1999年12月：发布 HTML 4.01
- 核心理念：分离结构与表现

### 三个变体
```html
<!-- 严格型 -->
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
    "http://www.w3.org/TR/html4/strict.dtd">

<!-- 过渡型 -->
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">

<!-- 框架集型 -->
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"
    "http://www.w3.org/TR/html4/frameset.dtd">
```

### 主要改进
```html
<!-- 引入 CSS -->
<LINK REL="stylesheet" TYPE="text/css" HREF="style.css">

<!-- 脚本支持 -->
<SCRIPT TYPE="text/javascript">
    function validateForm() {
        // JavaScript 代码
    }
</SCRIPT>

<!-- 框架 -->
<FRAMESET COLS="20%,80%">
    <FRAME SRC="menu.html">
    <FRAME SRC="content.html">
</FRAMESET>
```

## 五、XHTML 1.0 (2000)

### XML 化改革
- 2000年1月：基于 XML 的重新定义
- 目标：更严格、更规范

### 语法要求
```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>XHTML 示例</title>
</head>
<body>
    <!-- 所有标签必须小写 -->
    <p>这是一个段落</p>
    
    <!-- 所有属性必须加引号 -->
    <img src="image.jpg" alt="描述" />
    
    <!-- 所有标签必须闭合 -->
    <br />
    <hr />
    
    <!-- 正确嵌套 -->
    <p><strong>粗体文本</strong></p>
</body>
</html>
```

## 六、HTML5 (2008-2014)

### 现代 Web 标准
- 2008年：首次草案
- 2014年10月：HTML5 成为 W3C 推荐标准

### 革命性变化
```html
<!DOCTYPE html>  <!-- 简化的文档类型声明 -->
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>HTML5 网页</title>
</head>
<body>
    <!-- 语义化标签 -->
    <header>
        <nav>导航</nav>
    </header>
    
    <main>
        <article>
            <section>
                <h1>文章标题</h1>
                <p>内容...</p>
            </section>
        </article>
        
        <aside>侧边栏</aside>
    </main>
    
    <footer>页脚</footer>
    
    <!-- 多媒体 -->
    <video controls>
        <source src="movie.mp4" type="video/mp4">
    </video>
    
    <audio controls>
        <source src="audio.mp3" type="audio/mpeg">
    </audio>
    
    <!-- 新表单元素 -->
    <input type="email" placeholder="邮箱">
    <input type="date">
    <input type="range">
</body>
</html>
```

## 七、HTML5.1 和 HTML5.2

### 持续演进
- 2016年11月：HTML5.1 成为标准
- 2017年12月：HTML5.2 发布

### 新增特性
```html
<!-- 对话框 -->
<dialog id="myDialog">
    <p>这是一个对话框</p>
    <button onclick="myDialog.close()">关闭</button>
</dialog>

<!-- 详情元素 -->
<details>
    <summary>点击查看详情</summary>
    <p>这里是详细内容</p>
</details>

<!-- 主内容区域 -->
<main>
    <p>页面的主要内容</p>
</main>
```

## 八、HTML5.3 和未来

### 当前发展
- Living Standard：HTML 现在作为"活标准"持续更新
- 新特性不断加入

### 现代特性示例
```html
<!-- 图片懒加载 -->
<img src="image.jpg" loading="lazy" alt="示例">

<!-- 响应式图片 -->
<picture>
    <source media="(min-width: 800px)" srcset="large.jpg">
    <source media="(min-width: 400px)" srcset="medium.jpg">
    <img src="small.jpg" alt="响应式图片">
</picture>

<!-- 原生模态框 -->
<dialog open>
    <p>原生对话框！</p>
</dialog>
```

## 发展历程

| 版本 | 时间 | 主要特点 |
| -- | -- | -- |
| HTML 1.0 | 1991 | 基本文本和链接 |
| HTML 2.0 | 1995 | 首个官方标准，引入表单 |
| HTML 3.2 | 1997 | 表格、Applet、字体控制 |
| HTML 4.01 | 1999 | CSS 分离，框架，国际化 |
| XHTML 1.0 | 2000 | XML 语法，更严格规范 |
| HTML5 | 2014 | 语义化标签，多媒体，新API |
| HTML Living Standard | 至今 | 持续更新，新特性不断加入 |
