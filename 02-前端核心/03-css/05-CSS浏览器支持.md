# CSS 浏览器支持

## 浏览器支持现状

### 主要浏览器引擎

```text
- Chrome/Edge (Blink)
- Firefox (Gecko)
- Safari (WebKit)
- Opera (Blink)
```

### 全球使用率（2024）

-   Chrome: ~65%
-   Safari: ~18%
-   Edge: ~5%
-   Firefox: ~3%
-   其他: ~9%

## 浏览器支持查询工具

-   Can I Use: [https://caniuse.com](https://caniuse.com)
-   MDN Browser Compatibility: [https://developer.mozilla.org](https://developer.mozilla.org)
-   CSS Tricks Browser Support: [https://css-tricks.com](https://css-tricks.com)

## 浏览器前缀指南

### 常用前缀

-   `-webkit`- (Chrome, Safari, Edge, Opera)
-   `-moz-` (Firefox)
-   `-ms-` (Internet Explorer)
-   `-o-` (旧版 Opera)

### 现代前缀使用策略

```css
/* 推荐写法：先写带前缀的，再写标准的 */
.gradient-bg {
    background: -webkit-linear-gradient(red, blue); /* Safari 5.1-6 */
    background: -o-linear-gradient(red, blue); /* Opera 11.1-12 */
    background: -moz-linear-gradient(red, blue); /* Firefox 3.6-15 */
    background: linear-gradient(red, blue); /* 标准语法 */
}

/* Flexbox 兼容性处理 */
.flex-container {
    display: -webkit-box; /* 2009版语法 */
    display: -moz-box;
    display: -ms-flexbox; /* 2011版语法 */
    display: -webkit-flex; /* 2012版语法 */
    display: flex; /* 标准语法 */
}
```

## 构建工具自动处理

### PostCSS + Autoprefixer 配置

```json
// package.json 或 .browserslistrc
{
    "browserslist": [
        "> 1%" /* 全球使用率>1%的浏览器 */,
        "last 2 versions" /* 每个浏览器的最后两个版本 */,
        "not ie <= 11" /* 排除IE11及以下 */,
        "not dead" /* 排除官方不再支持的浏览器 */
    ]
}
```

```js
// postcss.config.js
module.exports = {
    plugins: [
        require("autoprefixer")({
            grid: "autoplace", // 自动添加IE的grid前缀
        }),
    ],
};
```

### 实用的兼容性 Mixins（SCSS 示例）

```scss
// 兼容性Mixin
@mixin flexbox() {
    display: -webkit-box;
    display: -moz-box;
    display: -ms-flexbox;
    display: -webkit-flex;
    display: flex;
}

@mixin transition($property) {
    -webkit-transition: $property;
    -moz-transition: $property;
    -ms-transition: $property;
    -o-transition: $property;
    transition: $property;
}

@mixin gradient($from, $to) {
    background-color: $to; /* 备用 */
    background-image: -webkit-linear-gradient($from, $to);
    background-image: -moz-linear-gradient($from, $to);
    background-image: -o-linear-gradient($from, $to);
    background-image: linear-gradient($from, $to);
}

// 使用示例
.container {
    @include flexbox();
    @include transition(all 0.3s ease);
    @include gradient(#ff0000, #0000ff);
}
```

## 测试策略

### 在线测试工具

-   BrowserStack: 云测试平台
-   LambdaTest: 在线浏览器测试
-   CrossBrowserTesting: 跨浏览器测试

### 本地测试

```bash
# 安装多个浏览器版本
# Chrome: 使用chrome://flags
# Firefox: 使用多个Profile
# Safari: 需要macOS设备

# 使用虚拟机测试IE
# Windows虚拟机 + IE Developer Tools
```

### 自动化测试

```js
// 使用Jest + Puppeteer
const puppeteer = require("puppeteer");

async function testCSSSupport() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // 检查CSS特性支持
    const supportsGrid = await page.evaluate(() => {
        return CSS.supports("display", "grid");
    });

    console.log(`Supports CSS Grid: ${supportsGrid}`);
    await browser.close();
}
```

## 最佳实践建议

-   定义浏览器支持矩阵：明确支持哪些浏览器版本
-   渐进增强：为现代浏览器提供更好体验
-   优雅降级：确保基础功能在所有浏览器中可用
-   定期更新：关注 Can I Use 的数据更新
-   性能考虑：前缀不要过度使用，保持 CSS 简洁
-   文档记录：记录已知的浏览器兼容性问题

## 浏览器兼容性表格示例

| 特性              | Chrome | Firefox | Safari | Edge | IE     | iOS Safari |
| ----------------- | ------ | ------- | ------ | ---- | ------ | ---------- |
| Flexbox           | 29+    | 28+     | 9+     | 12+  | 11\*   | 9+         |
| CSS Grid          | 57+    | 52+     | 10.1+  | 16+  | 不支持 | 10.3+      |
| CSS Variables     | 49+    | 31+     | 9.1+   | 15+  | 不支持 | 9.3+       |
| :has()            | 105+   | 121+    | 15.4+  | 105+ | 不支持 | 15.4+      |
| Container Queries | 105+   | 110+    | 16+    | 105+ | 不支持 | 16+        |

*IE11 部分支持 Flexbox（2012 版语法）
