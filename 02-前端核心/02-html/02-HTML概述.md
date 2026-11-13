[MDN HTML基础](https://developer.mozilla.org/zh-CN/docs/Learn/HTML/Introduction_to_HTML)

## 什么是 DOCTYPE， 有何作用？

`<!DOCTYPE>` 声明的目的是让浏览器能够正确地渲染页面。

### 常见的 DOCTYPE 声明
HTML 5
```
<!DOCTYPE html>
```
HTML 4.01 Strict
这个 DTD 包含所有 HTML 元素和属性，但不包括表象或过时的元素（如 font ）。框架集是不允许的。
```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
```
HTML 4.01 Transitional
这个 DTD 包含所有 HTML 元素和属性，包括表象或过时的元素（如 font ）。框架集是不允许的。
```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
```
HTML 4.01 Frameset
这个 DTD 与 HTML 4.01 Transitional 相同，但是允许使用框架集内容。
```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
```
XHTML 1.0 Strict
这个 DTD 包含所有 HTML 元素和属性，但不包括表象或过时的元素（如 font ）。框架集是不允许的。结构必须按标准格式的 XML 进行书写。
```
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
```

## 说说对 html 语义化的理解

HTML标签的语义化，简单来说，就是用正确的标签做正确的事情，给某块内容用上一个最恰当最合适的标签，使页面有良好的结构，页面元素有含义，无论是谁都能看懂这块内容是什么。
语义化的优点如下：

* 在没有CSS样式情况下也能够让页面呈现出清晰的结构
* 有利于SEO和搜索引擎建立良好的沟通，有助于爬虫抓取更多的有效信息，爬虫是依赖于标签来确定上下文和各个关键字的权重
* 方便团队开发和维护，语义化更具可读性，遵循W3C标准的团队都遵循这个标准，可以减少差异化

## src 和 href 的区别

src和href都是HTML中特定元素的属性，都可以用来引入外部的资源。两者区别如下：

* src：全称source，它通常用于img、video、audio、script元素，通过src指向请求外部资源的来源地址，指向的内容会嵌入到文档中当前标签所在位置，在请求src资源时，它会将资源下载并应用到文档内，比如说：js脚本、img图片、frame等元素。当浏览器解析到该元素时，会暂停其它资源下载，直到将该资源加载、编译、执行完毕。这也是为什么将js脚本放在底部而不是头部的原因。
* href：全称hyper reference，意味着超链接，指向网络资源，当浏览器识别到它指向的⽂件时，就会并⾏下载资源，不会停⽌对当前⽂档的处理，通常用于a、link元素。

## 什么是严格模式与混杂模式？

* 严格模式：是以浏览器支持的最高标准运行
* 混杂模式：页面以宽松向下兼容的方式显示，模拟老式浏览器的行为

## 前端页面有哪三层构成，分别是什么？

结构层、表示层、行为层

**结构层（structural layer）**
> 结构层类似于盖房子需要打地基以及房子的悬梁框架，它是由HTML超文本标记语言来创建的，也就是页面中的各种标签，在结构层中保存了用户可以看到的所有内容，比如说：一段文字、一张图片、一段视频等等

**表示层（presentation layer）**
> 表示层是由CSS负责创建，它的作用是如何显示有关内容，学名：层叠样式表，也就相当于装修房子，看你要什么风格的，田园的、中式的、地中海的，总之CSS都能办妥

**行为层（behaviorlayer）**
> 行为层表示网页内容跟用户之间产生交互性，简单来说就是用户操作了网页，网页给用户一个反馈，这是JavaScript和DOM主宰的领域

## iframe的作用以及优缺点

iframe也称作嵌入式框架，嵌入式框架和框架网页类似，它可以把一个网页的框架和内容嵌入到现有的网页中。

优点：
* 可以用来处理加载缓慢的内容，比如：广告

缺点：
* iframe会阻塞主页面的Onload事件
* iframe和主页面共享连接池，而浏览器对相同域的连接有限制，所以会影响页面的并行加载。但是可以通过JS动态给ifame添加src属性值来解决这个问题，当然也可以解决iframe会阻塞主页面的Onload事件的问题
* 会产生很多页面，不易管理
* 浏览器的后退按钮没有作用
* 无法被一些搜索引擎识别

## H5和HTML5区别

* H5是一个产品名词，包含了最新的HTML5、CSS3、ES6等新技术来制作的应用
* HTML5是一个技术名词，指的就是第五代HTML

## label的作用是什么？是怎么用的？

`label`元素不会向用户呈现任何特殊效果，但是，它为鼠标用户改进了可用性，当我们在label元素内点击文本时就会触发此控件。也就是说，当用户选择该标签时，浏览器就会自动将焦点转到和标签相关的表单控件上。最常用label的地方就是表单中的性别单选框了，当点击文字时也能够自动聚焦绑定的表单控件。

## 对于Web标准以及W3C的理解

`Web标准`简单来说可以分为结构、表现、行为。
`W3C`，全称：world wide web consortium是一个制定各种标准的非盈利性组织，也叫万维网联盟，标准包括HTML、CSS、ECMAScript等等，web标准的制定有很多好处。

## Quirks（怪癖）模式是什么？它和Standards（标准）有什么区别？

**Quirks模式：**
Quirks模式是一种宽松的渲染模式，它是为了与旧版本的HTML文档兼容而设计的。在Quirks模式下，浏览器的行为可能会有一些怪异之处，与标准模式不同。以下是Quirks模式的一些特点：

* 怪癖盒模型： 在Quirks模式下，浏览器使用怪癖盒模型来计算元素的宽度和高度。这意味着边距和填充会影响元素的实际大小。
* 浮动和定位： 浮动和定位的行为在Quirks模式下与标准模式不同，可能导致页面布局问题。
* 垂直对齐： 垂直对齐可能不一致，可能需要额外的样式来修复。
* 默认字体： 浏览器可能使用不同的默认字体，导致文本呈现不同。

Quirks模式示例:
如果没有指定文档类型或使用了旧的文档类型，浏览器将进入Quirks模式。这是一种兼容性模式，用于支持旧的HTML文档。

```html
<!-- 没有指定文档类型，将触发Quirks模式 -->
<html>
  <head>
    <title>Quirks模式示例</title>
  </head>
  <body>
    <!-- 页面内容 -->
  </body>
</html>
```

**Standards模式：**
Standards模式是一种更严格的渲染模式，它遵循HTML5和现代Web标准。在Standards模式下，浏览器按照标准规范解释和渲染HTML和CSS。以下是Standards模式的一些特点：

* 标准盒模型： 在Standards模式下，浏览器使用标准盒模型来计算元素的宽度和高度，边距和填充不会影响实际大小。
* 一致的浮动和定位： 浮动和定位的行为在Standards模式下更一致，更容易控制。
* 一致的垂直对齐： 垂直对齐行为更一致，不太可能出现不一致的问题。
* 一致的字体： 浏览器使用相同的默认字体，文本呈现更一致。

Standards模式示例:
如果使用了现代的文档类型声明，浏览器将进入Standards模式。这是一种更严格的模式，用于支持HTML5和现代Web标准。

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Standards模式示例</title>
  </head>
  <body>
    <!-- 页面内容 -->
  </body>
</html>
```

## 知道什么是微格式吗？谈谈理解，在前端构建中应该考虑微格式吗？

**官方定义**
> 微格式基于简单的标记约定，使您能够向web内容添加有意义的结构。
> 微格式的一个关键原则是赋予人类可读内容特权。这意味着您应该首先考虑内容设计的可读性和可访问性。
> 通过使用最合适的HTML元素并将结构化类名应用到标记中，您可以生成人类观众可以清楚理解的内容，并通过自动化程序和其他在线工具以结构化方式使用这些内容。
> 但关键是，你不应该不遗余力地制作这样的机器友好型标记——微格式可以轻松地将这种更高程度的结构集成到你的网站中，而无需学习复杂的新语言或格式。

微格式就是为了兼顾 HTML 文档的人机可读性，在标签中添加的语义注解。

> 所谓微格式，是建立在已有的、被广泛采用的标准基础之上的一组简单的、开放的数据格式。
具体表现是把语义嵌入到 HTML 中，以便有助于分离式开发，并通过制定一些简单的约定，来兼顾 HTML 文档的人机可读性，相当于对 Web 网页进行了语义注解。
采用微格式的 Web 页面，在 HTML 文档中给一些标签增加一些属性，这些属性对信息的语义结构进行注解，有助于处理 HTML 文档的软件，更好的理解该 HTML 文档。

## HTML5为什么只需要写<!DOCTYPE html>?

因为HTML5不基于SGML，所以不需要引用DTD。在HTML4中，<!DOCTYPE>声明引用DTD，因为HTML4基于SGML。DTD规定了标记语言的规则，这样浏览器才能正确的呈现内容。

## HTML5新增了哪些新特性？移除了哪些元素？

HTML5主要是关于图像、位置、存储、多任务等功能的增加：
* 语义化标签，如：article、footer、header、nav等
* 视频video、音频audio
* 画布canvas
* 表单控件，calemdar、date、time、email
* 地理
* 本地离线存储，localStorage长期存储数据，浏览器关闭后数据不丢失，sessionStorage的数据在浏览器关闭后自动删除
* 拖拽释放

移除的元素：
* 纯表现的元素：basefont、font、s、strike、tt、u、big、center
* 对可选用性产生负面影响的元素：frame、frameset、noframes

## 怎么处理HTML5新标签兼容问题？

* 实现标签被识别：通过document.createElement(tagName)方法可以让浏览器识别新的标签，浏览器支持新标签后。还可以为新标签添加CSS样式
* 用JavaScript解决：使用HTML5的shim框架，在head标签中调用以下代码

## 如何实现在一张图片上的某个区域做到点击事件

我们可以通过图片热区技术：

1. 插入一张图片，并设置好图像的有关参数，在<img>标记中设置参数usemap="#Map"，以表示对图像地图的引用。
2. 用<map>标记设定图像地图的作用区域，并取名：Map；
3. 分别用<area>标记针对相应位置互粉出多个矩形作用区域，并设定好链接参数href

```html
<body>
 <img src="./image.jpg" alt="" usemap="#Map" />
 　　<map name="Map" id="Map">
     <area alt="" title="" href="#" shape="poly" coords="65,71,98,58,114,90,108,112,79,130,56,116,38,100,41,76,52,53,83,34,110,33,139,46,141,75,145,101,127,115,113,133,85,132,82,131,159,117" />
     <area alt="" title="" href="#" shape="poly" coords="28,22,57,20,36,39,27,61" />
 </map>
</body>
```

## 你知道SEO中的TDK吗？

在SEO中，TDK其实就是title、description、keywords这三个标签，title表示标题标签，description是描述标签，keywords是关键词标签