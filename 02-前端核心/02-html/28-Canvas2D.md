# Canvas 2D

`<canvas>` 是 HTML5 引入的用于通过 JavaScript 绘制图形的元素。

## 基础用法

### 1. 创建 Canvas

```html
<canvas id="myCanvas" width="800" height="600"> 您的浏览器不支持 Canvas </canvas>
```

### 2. 获取上下文

```js
const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d"); // 2D 绘图上下文
```

## 绘制基本图形

### 1. 矩形

```js
// 填充矩形
ctx.fillStyle = "red";
ctx.fillRect(10, 10, 100, 50);

// 描边矩形
ctx.strokeStyle = "blue";
ctx.lineWidth = 2;
ctx.strokeRect(150, 10, 100, 50);

// 清除矩形区域
ctx.clearRect(20, 20, 50, 20);
```

### 2. 路径和线条

```js
// 开始路径
ctx.beginPath();
ctx.moveTo(50, 50); // 起点
ctx.lineTo(150, 50); // 直线到
ctx.lineTo(100, 150); // 直线到
ctx.closePath(); // 闭合路径

// 样式和绘制
ctx.strokeStyle = "green";
ctx.lineWidth = 3;
ctx.stroke();

// 填充路径
ctx.fillStyle = "rgba(255, 0, 0, 0.5)";
ctx.fill();
```

### 3. 圆形和圆弧

```js
// 圆形
ctx.beginPath();
ctx.arc(200, 200, 50, 0, Math.PI * 2); // (x, y, 半径, 起始角, 结束角)
ctx.fillStyle = "orange";
ctx.fill();

// 圆弧
ctx.beginPath();
ctx.arc(300, 200, 50, 0, Math.PI, false); // 半圆
ctx.strokeStyle = "purple";
ctx.lineWidth = 4;
ctx.stroke();
```

## 样式和颜色

### 1. 颜色和渐变

```js
// 纯色
ctx.fillStyle = "#ff0000";
ctx.fillStyle = "rgb(255, 0, 0)";
ctx.fillStyle = "rgba(255, 0, 0, 0.5)";

// 线性渐变
const gradient = ctx.createLinearGradient(0, 0, 200, 0);
gradient.addColorStop(0, "red");
gradient.addColorStop(0.5, "yellow");
gradient.addColorStop(1, "green");
ctx.fillStyle = gradient;
ctx.fillRect(10, 10, 200, 100);

// 径向渐变
const radialGradient = ctx.createRadialGradient(150, 150, 10, 150, 150, 50);
radialGradient.addColorStop(0, "white");
radialGradient.addColorStop(1, "blue");
ctx.fillStyle = radialGradient;
ctx.fillRect(100, 100, 100, 100);
```

### 2. 线条样式

```js
ctx.lineWidth = 10;
ctx.lineCap = "round"; // butt, round, square
ctx.lineJoin = "round"; // bevel, round, miter
ctx.setLineDash([5, 15]); // 虚线模式
ctx.lineDashOffset = 0;

ctx.beginPath();
ctx.moveTo(50, 50);
ctx.lineTo(200, 50);
ctx.lineTo(200, 150);
ctx.stroke();
```

### 3. 阴影

```js
ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
ctx.shadowBlur = 10;
ctx.shadowOffsetX = 5;
ctx.shadowOffsetY = 5;

ctx.fillStyle = "red";
ctx.fillRect(50, 50, 100, 100);
```

## 文本绘制

### 1. 文本样式

```js
ctx.font = "bold 48px Arial";
ctx.fillStyle = "blue";
ctx.textAlign = "center"; // start, end, left, right, center
ctx.textBaseline = "middle"; // top, hanging, middle, alphabetic, ideographic, bottom

ctx.fillText("Hello Canvas", 400, 100);

// 描边文本
ctx.strokeStyle = "black";
ctx.lineWidth = 2;
ctx.strokeText("Stroke Text", 400, 200);
```

### 2. 文本测量

```js
const text = "Hello World";
ctx.font = "30px Arial";
const metrics = ctx.measureText(text);

console.log("文本宽度:", metrics.width);
console.log("字体宽度:", metrics.actualBoundingBoxLeft + metrics.actualBoundingBoxRight);
```

## 图像操作

### 1. 绘制图像

```js
const img = new Image();
img.onload = function () {
    // 基本绘制
    ctx.drawImage(img, 50, 50);

    // 缩放绘制
    ctx.drawImage(img, 200, 50, 100, 100);

    // 切片绘制
    ctx.drawImage(img, 10, 10, 50, 50, 350, 50, 100, 100);
};
img.src = "image.jpg";
```

### 2. 图像数据处理

```js
// 获取图像数据
const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
const data = imageData.data;

// 处理像素（反色效果）
for (let i = 0; i < data.length; i += 4) {
    data[i] = 255 - data[i]; // Red
    data[i + 1] = 255 - data[i + 1]; // Green
    data[i + 2] = 255 - data[i + 2]; // Blue
    // Alpha (data[i + 3]) 保持不变
}

// 放回处理后的数据
ctx.putImageData(imageData, 0, 0);
```

## 变换和合成

### 1. 坐标变换

```js
// 保存当前状态
ctx.save();

// 平移
ctx.translate(100, 100);

// 旋转 (弧度)
ctx.rotate(Math.PI / 4);

// 缩放
ctx.scale(1.5, 1.5);

// 绘制
ctx.fillStyle = "red";
ctx.fillRect(0, 0, 50, 50);

// 恢复状态
ctx.restore();
```

### 2. 变换矩阵

```js
// 自定义变换矩阵
ctx.transform(1, 0.5, -0.5, 1, 30, 10);
ctx.fillRect(0, 0, 100, 100);

// 重置变换
ctx.setTransform(1, 0, 0, 1, 0, 0);
```

### 3. 合成操作

```js
ctx.globalAlpha = 0.5; // 全局透明度

ctx.globalCompositeOperation = "source-over"; // 默认
// 其他模式: source-in, source-out, destination-over, etc.

ctx.fillStyle = "red";
ctx.fillRect(50, 50, 100, 100);

ctx.fillStyle = "blue";
ctx.fillRect(100, 100, 100, 100);
```

## 动画基础

### 1. 简单动画循环

```js
function animate() {
    // 清除画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 更新和绘制
    drawFrame();

    // 继续动画
    requestAnimationFrame(animate);
}

// 开始动画
animate();
```

### 2. 弹跳球示例

```html
<canvas id="bounceCanvas" width="600" height="400"></canvas>

<script>
    const canvas = document.getElementById("bounceCanvas");
    const ctx = canvas.getContext("2d");

    let x = 50,
        y = 50;
    let dx = 2,
        dy = 3;
    const radius = 20;

    function drawBall() {
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = "red";
        ctx.fill();
        ctx.closePath();
    }

    function update() {
        // 清除画布
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 边界检测
        if (x + dx > canvas.width - radius || x + dx < radius) {
            dx = -dx;
        }
        if (y + dy > canvas.height - radius || y + dy < radius) {
            dy = -dy;
        }

        // 更新位置
        x += dx;
        y += dy;

        // 绘制
        drawBall();
    }

    // 动画循环
    setInterval(update, 10);
</script>
```

## 高级特性

### 1. 离屏 Canvas

```js
// 创建离屏 canvas
const offscreenCanvas = document.createElement("canvas");
const offscreenCtx = offscreenCanvas.getContext("2d");
offscreenCanvas.width = 100;
offscreenCanvas.height = 100;

// 在离屏 canvas 上绘制
offscreenCtx.fillStyle = "blue";
offscreenCtx.fillRect(0, 0, 100, 100);

// 绘制到主 canvas
ctx.drawImage(offscreenCanvas, 0, 0);
```

### 2. 点击检测

```js
canvas.addEventListener("click", function (event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // 检查是否点击在圆形上
    if (ctx.isPointInPath(x, y)) {
        console.log("点击了圆形！");
    }
});
```

### 3. 保存为图像

```js
function saveCanvas() {
    // 获取数据 URL
    const dataURL = canvas.toDataURL("image/png");

    // 创建下载链接
    const link = document.createElement("a");
    link.download = "canvas-image.png";
    link.href = dataURL;
    link.click();
}
```

## 案例

### 粒子系统

```html
<canvas id="particleCanvas" width="800" height="600"></canvas>

<script>
    const canvas = document.getElementById("particleCanvas");
    const ctx = canvas.getContext("2d");

    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.vx = (Math.random() - 0.5) * 2;
            this.vy = (Math.random() - 0.5) * 2;
            this.radius = Math.random() * 3 + 1;
            this.color = `hsl(${Math.random() * 360}, 50%, 50%)`;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            // 边界检查
            if (this.x < 0 || this.x > canvas.width) this.vx = -this.vx;
            if (this.y < 0 || this.y > canvas.height) this.vy = -this.vy;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
        }
    }

    const particles = [];
    for (let i = 0; i < 100; i++) {
        particles.push(new Particle());
    }

    function animate() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.1)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });

        requestAnimationFrame(animate);
    }

    animate();
</script>
```

## 性能优化

```js
// 1. 避免在动画循环中创建新对象
// 坏
function draw() {
    const gradient = ctx.createLinearGradient(0, 0, 100, 100); // 每次创建
    // ...
}

// 好
const gradient = ctx.createLinearGradient(0, 0, 100, 100); // 预先创建
function draw() {
    // 使用预先创建的 gradient
}

// 2. 使用离屏 canvas 缓存复杂图形
const cacheCanvas = document.createElement("canvas");
const cacheCtx = cacheCanvas.getContext("2d");
// 在 cacheCanvas 上绘制复杂图形

// 3. 合理使用 clearRect
ctx.clearRect(0, 0, canvas.width, canvas.height); // 清除整个画布
// 或只清除变化区域
ctx.clearRect(x, y, width, height);
```

## 总结

Canvas 提供了强大的 2D 绘图能力：

核心概念：

-   上下文 (Context) - 绘图环境
-   路径 (Path) - 图形的基础
-   状态 (State) - 通过 save()/restore() 管理

主要功能：

-   基本图形绘制
-   文本渲染
-   图像处理
-   动画创建
-   像素级操作

应用场景：

-   数据可视化
-   游戏开发
-   图像编辑
-   特效动画
-   交互式图表

## 怎么解决canvas中获取跨域图片数据的问题？

当请求跨域图片数据，而未满足跨域请求资源的条件时。如果canvas使用未经跨域允许的图片的原始数据，这些是不可信的数据，可能会暴露页面的数据。

### 请求图片资源 - 同域

Request Headers带有cookie。图片数据是被canvas信任的。

### 请求图片资源 - 跨域

默认情况下，直接请求跨域图片。因为不符合跨域请求资源的条件，图片数据是不被canvas信任的。

为了解决图片跨域资源共享的问题，`<img>` 元素提供了支持的属性：`crossOrigin`，该属性一共有两个值可选：`anonymous` 和 `use-credentials`，下面列举了两者的使用场景，以及满足的条件。


| \ | `anonymous` | `use-credentials` |
| --- | --- | --- |
| 用途 | 匿名请求跨域图片资源，不会发送证书（比如cookie等） | 具名请求跨域图片资源，会携带证书数据 |
| Request Headers | `origin` | `origin、cookie` |
| Response headers | `Access-Control-Allow-Origin` | `Access-Control-Allow-Origin`、`Access-Control-Allow-Credentials` |
| 所需条件 |`Access-Control-Allow-Origin` 字段值需要包含请求域。  | `Access-Control-Allow-Origin` 字段值需要包含请求域，且不能为通配符 `*`。`Access-Control-Allow-Credentials` 字段值需要为 true，表明允许请求发送证书数据。 |

主要原因是：

- 如果使用跨域的资源画到`canvas`中，并且资源没有使用CORS去请求，`canvas`会被认为是被污染了, `canvas`可以正常展示，但是没办法使用`toDataURL()`或者`toBlob()`导出数据，见`Allowing cross-origin use of images and canvas`。 所以通过在`img`标签上设置`crossorigin`，启用`CORS`，属性值为`anonymous`，在`CORS`请求时不会发送认证信息,见HTML attribute: crossorigin。
- 在启用`CORS`请求跨域资源时，资源必须允许跨域，才能正常返回，最简单的方式设置响应头`Access-Control-Allow-Origin`
- 图片已经通过img标签加载过，浏览器默认会缓存下来，下次使用js方式再去请求，直接返回缓存的图片，如果缓存中的图片不是通过`CORS` 请求或者响应头中不存在`Access-Control-Allow-Origin`，都会导致报错。