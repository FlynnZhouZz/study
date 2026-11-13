# CSS 文本格式

## 1. `color` - 文本颜色

设置文本的前景色。

```css
p {
    color: red;
    color: #ff0000;
    color: rgb(255, 0, 0);
    color: rgba(255, 0, 0, 0.8); /* 带透明度 */
    color: hsl(0, 100%, 50%); /* 色相、饱和度、明度 */
}
```

## 2. `text-align` - 水平对齐

设置文本的水平对齐方式。

```css
p {
    text-align: left; /* 左对齐（默认） */
    text-align: right; /* 右对齐 */
    text-align: center; /* 居中对齐 */
    text-align: justify; /* 两端对齐 */
}
```

## 3. `vertical-align` - 垂直对齐

设置行内元素或表格单元格的垂直对齐方式。

```css
img {
    vertical-align: middle; /* 图片与文本中线对齐 */
}
span {
    vertical-align: super; /* 上标 */
    vertical-align: sub; /* 下标 */
    vertical-align: top; /* 顶部对齐 */
    vertical-align: bottom; /* 底部对齐 */
}
```

## 4. `text-decoration` - 文本装饰

简写属性，用于设置文本的装饰线。

```css
a {
    text-decoration: none; /* 去除链接下划线 */
}

h1 {
    text-decoration: overline; /* 上划线 */
    text-decoration: line-through; /* 删除线 */
    text-decoration: underline; /* 下划线 */
    text-decoration: underline wavy red; /* 波浪形红色下划线 */
}

/* 也可以拆分为更详细的属性 */
.fancy {
    text-decoration-line: underline;
    text-decoration-style: dashed;
    text-decoration-color: blue;
    text-decoration-thickness: 2px;
}
```

## 5. `text-transform` - 文本转换

控制文本的大小写。

```css
p {
    text-transform: capitalize; /* 每个单词首字母大写 */
    text-transform: uppercase; /* 全部大写 */
    text-transform: lowercase; /* 全部小写 */
    text-transform: none; /* 默认，原样显示 */
}
```

## 6. `text-shadow` - 文本阴影

为文本添加阴影效果。

```css
h1 {
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    /* 格式：水平偏移 垂直偏移 模糊半径 颜色 */
}

/* 多重阴影效果 */
.fancy-text {
    text-shadow: 1px 1px 0 #fff, 2px 2px 0 #999;
}
```

## 7. `font-family` - 字体家族

设置文本的字体系列。

```css
body {
    font-family: "Microsoft YaHei", Arial, sans-serif;
    /* 浏览器会从左到右依次查找可用的字体 */
}
```

更过详情内容，请看下文 [font-family 字体文件如何获取和配置](#font-family-字体文件如何获取和配置)

## 8. `font-size` - 字体大小

```css
p {
    font-size: 16px; /* 像素 */
    font-size: 1em; /* 相对于父元素 */
    font-size: 1rem; /* 相对于根元素(html) */
    font-size: 100%; /* 百分比 */
    font-size: larger; /* 相对大小 */
}
```

## 9. `font-weight` - 字体粗细

```css
p {
    font-weight: normal; /* 正常 */
    font-weight: bold; /* 粗体 */
    font-weight: 700; /* 数字值：100-900 */
    font-weight: lighter; /* 更细 */
}
```

## 10. `font-style` - 字体样式

```css
p {
    font-style: normal; /* 正常 */
    font-style: italic; /* 斜体 */
    font-style: oblique; /* 倾斜体 */
}
```

## 11. `line-height` - 行高

设置行间的距离（行高）。

```css
p {
    line-height: 1.6; /* 无单位数字，相对于当前字体大小 */
    line-height: 24px; /* 固定值 */
    line-height: 150%; /* 百分比 */
}
```

## 12. `letter-spacing` - 字符间距

```css
h1 {
    letter-spacing: 2px; /* 增加间距 */
    letter-spacing: -1px; /* 减少间距 */
}
```

## 13. `word-spacing` - 单词间距

```css
p {
    word-spacing: 5px; /* 增加单词间距 */
}
```

## 14. `text-indent` - 首行缩进

```css
p {
    text-indent: 2em; /* 首行缩进2个字符 */
    text-indent: 20px; /* 固定值缩进 */
}
```

## 15. `white-space` - 空白处理

控制元素中空白的处理方式。

```css
pre {
    white-space: pre; /* 保留所有空白和换行 */
}

.nowrap {
    white-space: nowrap; /* 文本不换行 */
}

.normal {
    white-space: normal; /* 默认，合并空白，自动换行 */
}
```

## 16. `word-wrap` / `overflow-wrap` - 单词换行

允许长单词或 URL 地址换行到下一行。

```css
p {
    word-wrap: break-word; /* 旧属性 */
    overflow-wrap: break-word; /* 新标准 */
}
```

## 17. `word-break` - 断行规则

指定怎样在单词内断行。

```css
p {
    word-break: normal; /* 默认断行规则 */
    word-break: break-all; /* 允许在任意字符间断行 */
    word-break: keep-all; /* 主要在空格或连字符处换行 */
}
```

## 18. `text-overflow` - 文本溢出

确定如何向用户发出未显示的溢出内容信号。

```css
.truncate {
    white-space: nowrap; /* 必须的 */
    overflow: hidden; /* 必须的 */
    text-overflow: ellipsis; /* 显示省略号 */
}

/* 多行省略号（-webkit） */
.truncate1 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2; /* 显示 2 行 */
    overflow: hidden;
}
```

## 字体简写属性

语法：

```css
font: [font-style] [font-variant] [font-weight] [font-size]/[line-height] [font-family];
```

示例：

```css
p {
    /* 完整写法 */
    font-style: italic;
    font-weight: bold;
    font-size: 16px;
    line-height: 1.5;
    font-family: Arial, sans-serif;

    /* 等效的简写写法 */
    font: italic bold 16px/1.5 Arial, sans-serif;
}

body {
    /* 更简洁的写法 */
    font: 14px/1.6 "Microsoft YaHei", sans-serif;
}
```

## 实用示例

### 示例 1：优美的段落排版

```css
.article {
    font-family: "Georgia", serif;
    font-size: 18px;
    line-height: 1.7;
    color: #333;
    text-align: justify;
    text-indent: 2em;
    word-spacing: 1px;
    margin-bottom: 1.5em;
}
```

### 示例 2：标题样式

```css
.heading {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #2c3e50;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}
```

### 示例 3：链接样式

```css
a {
    color: #3498db;
    text-decoration: none;
    transition: all 0.3s ease;
}

a:hover {
    color: #2980b9;
    text-decoration: underline;
}
```

### 示例 4：文字截断

```css
.card-title {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin: 0;
}
```

## `font-family` 字体文件如何获取和配置

### 字体文件去哪里获取

1. [Google Fonts](https://fonts.google.com): 众多字体/自动生成 CSS/可直接下载字体 ZIP
2. [字体天下](https://www.fonts.net.cn): 中文，部分免费
3. [justfont](https://justfont.com): 中文，部分免费
4. Adobe Fonts: 需 Adobe 账户，可商用。
5. 开源中文字体（高质量）
   | 字体 | 特点 |
   | -- | -- |
   | **思源黑体 Noto Sans CJK / Source Han Sans** | 免费最全、最标准 |
   | **思源宋体** | 中文非常专业 |
   | **阿里巴巴普惠体** | 免费商用、风格现代 |
   | **HarmonyOS Sans** | 华为字体，免费商用 |

### 字体格式说明

浏览器对字体格式支持不同，因此建议准备多种格式：

| 格式          | 说明                     | 推荐程度       |
| ------------- | ------------------------ | -------------- |
| **woff2**     | 最小、加载快、现代浏览器 | ⭐⭐⭐⭐⭐     |
| **woff**      | 兼容好（旧浏览器）       | ⭐⭐⭐⭐       |
| **ttf / otf** | 常用原始格式，体积大     | ⭐⭐⭐         |
| **eot**       | 旧版 IE 用               | ⭐（基本不用） |

最理想组合：woff2 + woff + ttf

### 字体文件如何配置？（@font-face）

假设你下载了字体文件放在：

```bash
/assets/fonts/
    MyFont.woff2
    MyFont.woff
    MyFont.ttf
```

写 `@font-face：`

```css
@font-face {
    font-family: "MyFont";
    src: url("/assets/fonts/MyFont.woff2") format("woff2"), url("/assets/fonts/MyFont.woff") format("woff"),
        url("/assets/fonts/MyFont.ttf") format("truetype");
    font-weight: normal;
    font-style: normal;
    font-display: swap;
}
```

说明：

-   `font-family: 'MyFont'` 是你自己取的名字
-   `font-display: swap;` 能避免字体加载中闪烁（FOIT）
-   需要多个格式保证兼容性

然后直接使用字体：

```css
body {
    font-family: "MyFont", sans-serif;
}
```

### 不同项目中如何配置

#### 1. 原生 HTML 项目（最简单）

把字体文件放在项目根目录或 assets 目录，CSS 写上面那段 `@font-face` 即可。

#### 2. Vue（包含 Vue2 / Vue3）

```bash
# 字体文件放在：
src/assets/fonts/MyFont.woff2
```

```css
/* @font-face 写法 */
@font-face {
    font-family: "MyFont";
    src: url("@/assets/fonts/MyFont.woff2") format("woff2");
}
```

```css
/* 使用 */
body {
    font-family: "MyFont";
}
```

#### 3. React / Web

放在 `public/fonts` 或 `src/assets/fonts`：

```css
/* src/index.css： */
@font-face {
    font-family: "MyFont";
    src: url("./assets/fonts/MyFont.woff2") format("woff2");
}
```

```css
/* App.css */
body {
    font-family: "MyFont";
}
```

#### 4. React Native / Expo

React Native 不支持 woff/woff2，只能使用 ttf！

```bash
# 字体文件放在：
/assets/fonts/MyFont.ttf
```

```js
// react-native.config.js
module.exports = {
    assets: ["./assets/fonts/"],
};
```

Expo 项目（你正在用的环境）更简单：

```js
// app.json
{
  "expo": {
    "assetBundlePatterns": ["**/*"]
  }
}
```

组件中加载：

```js
import * as Font from "expo-font";

await Font.loadAsync({
    MyFont: require("./assets/fonts/MyFont.ttf"),
});
```

使用：

```jsx
<Text style={{ fontFamily: "MyFont" }}>Hello</Text>
```

### 使用 CDN 字体（免下载）

```html
<link
    href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&display=swap"
    rel="stylesheet"
/>
```

使用：

```css
body {
    font-family: "Noto Sans", sans-serif;
}
```

### 最佳实践

1. 字体路径要正确：如果部署到子目录，路径必须是 绝对路径 或使用构建工具的资源管理。
2. 不要直接用 TTF 放生产，体积大：推荐：woff2 + woff
3. 字体名称必须与 @font-face 声明一致：区分大小写
4. 使用 font-display: swap; 提升性能：避免字体加载闪白或闪跳
