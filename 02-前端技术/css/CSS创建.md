# CSS 创建

## 创建 CSS 的三种方法

### 1. 外部样式表（External CSS）— 最推荐方式

把 CSS 写在独立文件，如 style.css，再用 `<link>` 引入。

优点：
-   结构与样式分离，最易维护
-   多页面可复用
-   让 HTML 更干净
-   浏览器会缓存 CSS 文件，加速后续页面的加载速度。

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="style.css" />
    </head>
    <body>
        <h1>外部 CSS 示例</h1>
    </body>
</html>
```

```css
/* style.css */
h1 {
    color: blue;
    font-size: 30px;
}
```

### 2. 内部样式表（Internal CSS）— 写在 `<style>` 中

所有 CSS 写在当前 HTML 文件的 `<head>` 部分。

适用场景：

-   单页面小项目
-   小范围局部样式
-   临时测试

```html
<!DOCTYPE html>
<html>
    <head>
        <style>
            p {
                color: green;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <p>内部 CSS 示例</p>
    </body>
</html>
```

### 3. 内联样式（Inline CSS）— 写在标签上

把样式写进元素的 style 属性内。

缺点：
- 难维护、难复用
- 优先级过高（不利于大项目）

```html
<p style="color: red; font-size: 16px;">
  这是一个内联样式段落
</p>
```

## 样式表的层叠与优先级

当多种创建方式同时存在时，浏览器会根据 “层叠” 规则来决定最终应用哪个样式。其优先级顺序（从高到低）通常为：
- 内联样式 (style 属性) - 最高优先级
- 内部样式 (`<style>` 标签) 和 外部样式 (`<link> `引入) - 优先级相同
    - 谁写在后面，谁就覆盖前面的（遵循“后来者居上”原则）。
- 浏览器默认样式 - 最低优先级
