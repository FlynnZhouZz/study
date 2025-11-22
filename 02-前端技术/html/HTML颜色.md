# HTML颜色

## 颜色表示方法

### 1. 颜色名称 (Color Names)

HTML 支持 140 种标准颜色名称。

```html
<!-- 基本颜色 -->
<p style="color: red;">红色文本</p>
<p style="color: blue;">蓝色文本</p>
<p style="color: green;">绿色文本</p>

<!-- 更多颜色名称 -->
<div style="background-color: coral;">珊瑚色背景</div>
<span style="color: darkcyan;">深青色文本</span>
<button style="background-color: goldenrod;">金菊色按钮</button>
```

常用颜色名称：

red, green, blue, black, white

gray, silver, maroon, purple

fuchsia, lime, olive, yellow

navy, teal, aqua, orange

### 2. 十六进制颜色 (Hexadecimal)

```html
<!-- 6位十六进制 -->
<p style="color: #ff0000;">红色文本 (#ff0000)</p>
<div style="background-color: #00ff00;">绿色背景</div>

<!-- 3位简写 -->
<p style="color: #f00;">红色文本 (#f00)</p>
<span style="background-color: #0f0;">绿色背景</span>

<!-- 带透明度 8位十六进制 -->
<div style="background-color: #ff000080;">半透明红色</div>
```

格式说明：

- `#RRGGBB` - 红绿蓝各2位
- `#RGB` - 简写形式（每个字符重复一次）
- `#RRGGBBAA` - 带Alpha通道（透明度）

### 3. RGB 和 RGBA

使用十进制数值表示颜色。

```html
<!-- RGB -->
<p style="color: rgb(255, 0, 0);">红色文本</p>
<div style="background-color: rgb(0, 255, 0);">绿色背景</div>

<!-- 百分比 RGB -->
<span style="color: rgb(100%, 0%, 0%);">红色文本</span>

<!-- RGBA (带透明度) -->
<div style="background-color: rgba(255, 0, 0, 0.5);">半透明红色</div>
<button style="background-color: rgba(0, 255, 0, 0.3);">透明绿色按钮</button>
```

### 4. HSL 和 HSLA

使用色相、饱和度、亮度表示颜色。

```html
<!-- HSL -->
<p style="color: hsl(0, 100%, 50%);">红色文本</p>
<div style="background-color: hsl(120, 100%, 50%);">绿色背景</div>

<!-- HSLA (带透明度) -->
<span style="color: hsla(240, 100%, 50%, 0.7);">半透明蓝色</span>
<div style="background-color: hsla(60, 100%, 50%, 0.5);">半透明黄色</div>
```

HSL 参数：

- H (Hue)：色相 (0-360)
- S (Saturation)：饱和度 (0%-100%)
- L (Lightness)：亮度 (0%-100%)
- A (Alpha)：透明度 (0-1)
