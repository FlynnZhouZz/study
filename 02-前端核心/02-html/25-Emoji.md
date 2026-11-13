# Emoji （表情符号）

## Emoji 基本概念

-   Emoji 是 Unicode 字符，本质上就是特殊字符
-   可以直接放在 HTML 里显示，无需图片
-   现代浏览器、操作系统都支持 Emoji

示例：
😀 😁 😂 🤣 🥰 😎 🐱 🐶 🍕 🎉

## 在 HTML 中直接使用 Emoji

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <title>Emoji 示例</title>
    </head>
    <body>
        <p>直接写 Emoji：😀 😎 🎉 🐶 🐱</p>
    </body>
</html>
```

## 用 Unicode 编码显示 Emoji

### 方法 1：十六进制 `&#x`

```html
<p>笑脸：&#x1F600;</p>
```

### 方法 2：十进制 `&#`

```html
<p>笑脸：&#128512;</p>
```

### 方法 3: 使用 CSS `::before` 或 `::after` 伪元素

```css
.warning::before {
    content: "\26A0\FE0F"; /* 使用十六进制码点，注意前面要加反斜杠 \ */
    margin-right: 5px;
}
.email::after {
    content: " ✉️"; /* 也可以直接粘贴 */
}
```

### 方法 4：使用 JavaScript

你可以通过 JavaScript 动态地插入或操作 Emoji。

示例省略

## Emoji 与 CSS

可以直接改变字体大小、颜色（对一些系统字体有效）：

```html
<p style="font-size:50px;">😎</p>
<p style="color:red;">❤️</p>
```

> 注意：Emoji 本身颜色和渲染由操作系统决定，有些系统无法改变内部颜色，只能变大小。

### 兼容性

-   支持现代浏览器（Chrome, Firefox, Edge, Safari）
-   老旧浏览器/系统可能显示方块或问号
-   iOS / Android 默认有完整 Emoji 字体支持

## Emoji 表情如何获取，实体如何查询

### 1. 使用在线 Emoji 表

| 网站 | 功能|
| -- | -- |
| [Emojipedia](https://emojipedia.org/) | 官方式 Emoji 百科，全 Unicode、实体、编码、含义 |
| [Unicode Table](https://unicode-table.com/) | 可查 Unicode 字符、HTML 实体  |
| [Get Emoji](https://getemoji.com/) | 直接复制 Emoji 到剪贴板 |

### 2. 在操作系统直接复制

- Windows: Win + . （点号） → 弹出 Emoji 面板 → 复制
- Mac: Control + Command + Space → Emoji 面板 → 复制
- Linux: 部分桌面环境右键菜单或复制网站 Emoji