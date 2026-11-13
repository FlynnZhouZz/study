# HTML URL 编码

## 什么是 URL 编码

URL（Uniform Resource Locator）只能包含 ASCII 字符：

-   英文字母 `a-z A-Z`
-   数字 `0-9`
-   一些特殊符号：`- _ . ~`

其它字符（空格、中文、Emoji、特殊符号）必须 编码成 `%XX` 格式，称为 URL Encoding / Percent Encoding。

```text
空格 -> %20
中文“你” -> %E4%BD%A0
Emoji 😀 -> %F0%9F%98%80
```

## HTML/JS 中的编码函数

JS 提供 4 个常用函数：<br>
一条规则：URL 参数用 `encodeURIComponent`，整 URL 用 `encodeURI`

| 函数| 功能  | 示例 |
| -- | ---- | ---- |
| `encodeURI()`  | 编码整个 URL，不编码 `: / ? & = #` 等 | `encodeURI("https://example.com/搜索?q=你好")` → `"https://example.com/搜索?q=你好"`（部分未编码） |
| `encodeURIComponent()` | 编码 URL 参数，几乎编码所有非字母数字字符 | `encodeURIComponent("你好")` → `%E4%BD%A0` |
| `decodeURI()`  | 解码 `encodeURI()` 编码的 URL | `"https://example.com/%E6%90%9C%E7%B4%A2"` → `"https://example.com/搜索"` |
| `decodeURIComponent()` | 解码 `encodeURIComponent()` | `%E4%BD%A0%E5%A5%BD` → `"你好"` |

## 在线工具和手动查询

在线编码/解码工具：

- [URL Encoder/Decoder](https://www.url-encode-decode.com)
- [URL Decoder/Encoder](https://meyerweb.com/eric/tools/dencoder)

手动查询字符编码：

你可以使用任何编程语言或查看 ASCII 码表。例如在 JavaScript 控制台：

```js
// 获取字符的十六进制码
"!".charCodeAt(0).toString(16); // 输出 "21"
"你".charCodeAt(0).toString(16); // 输出 "4f60" (这是 Unicode 码点)
```
