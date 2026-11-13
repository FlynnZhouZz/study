# HTML 语言代码

## 什么是 HTML 语言代码

-   HTML 提供 lang 属性来指定文档或元素的语言
-   语言代码基于 ISO 639-1 / ISO 639-2
-   有助于：
    -   浏览器选择正确字体、拼写检查
    -   搜索引擎优化（SEO）
    -   辅助工具（屏幕阅读器）读出正确语言

## HTML 中使用 lang 属性

```html
<html lang="zh-CN">
    <head>
        <meta charset="UTF-8" />
        <title>语言示例</title>
    </head>
    <body>
        <p>这是中文段落。</p>
        <p lang="en">This is an English paragraph.</p>
        <p lang="ja">これは日本語の段落です。</p>
    </body>
</html>
```

说明：

- `<html lang="zh-CN">` → 整个页面默认中文（简体）
- `<p lang="en">` → 单独段落为英文
- `<p lang="ja">` → 单独段落为日文

## 常用 HTML 语言代码

| 语言 | ISO 639-1 | 常用地区（ISO 3166-1） | HTML 示例 |
| -- | -- | -- | -- |
| 中文（简体） | zh | CN（中国大陆）  | `<html lang="zh-CN">` |
| 中文（繁体） | zh | TW（台湾）、HK（香港）、MO（澳门）、SG（新加坡）、Hans（简体通用）、Hant（繁体通用） | `<html lang="zh-TW">` |
| 英文（美国） | en | US  | `<p lang="en-US">Hello</p>`  |
| 英文（英国） | en | GB  | `<p lang="en-GB">Hello</p>`  |
| 日文 | ja | JP（日本） | `<p lang="ja">こんにちは</p>` |
| 韩文 | ko | KR（韩国） | `<p lang="ko">안녕하세요</p>` |
| 法文 | fr | FR（法国）、CA（加拿大）   | `<p lang="fr-FR">Bonjour</p>`   |
| 德文 | de | DE（德国）、AT（奥地利）、CH（瑞士）   | `<p lang="de-DE">Guten Tag</p>` |
| 西班牙文   | es | ES（西班牙）、MX（墨西哥）、AR（阿根廷） | `<p lang="es-ES">Hola</p>`   |
| 意大利文   | it | IT（意大利）   | `<p lang="it-IT">Ciao</p>`   |
| 葡萄牙文（巴西）  | pt | BR  | `<p lang="pt-BR">Olá</p>`    |
| 葡萄牙文（葡萄牙） | pt | PT  | `<p lang="pt-PT">Olá</p>`    |
| 俄文 | ru | RU（俄罗斯）   | `<p lang="ru-RU">Привет</p>` |
| 阿拉伯文   | ar | AE（阿联酋）、SA（沙特）   | `<p lang="ar-SA">مرحبا</p>`  |
| 印地语    | hi | IN（印度） | `<p lang="hi-IN">नमस्ते</p>` |
