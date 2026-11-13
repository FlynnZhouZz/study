# SVG

SVG (Scalable Vector Graphics)  是基于 XML 的矢量图形格式，可以在不失真的情况下无限缩放。

## SVG 基础

### 1. 基本结构

```html
<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  <!-- SVG 内容 -->
</svg>
```

### 2. 在 HTML 中使用 SVG

```html
<!-- 内联 SVG -->
<svg width="200" height="200">
  <circle cx="100" cy="100" r="50" fill="red"/>
</svg>

<!-- 作为图片引用 -->
<img src="image.svg" alt="SVG 图片">

<!-- 作为背景图片 -->
<div style="background: url('image.svg');"></div>

<!-- 使用 object 标签 -->
<object data="image.svg" type="image/svg+xml"></object>
```

## 基本图形元素

### 1. 矩形 `<rect>`

```html
<svg width="300" height="200">
  <!-- 基本矩形 -->
  <rect x="10" y="10" width="100" height="50" fill="blue"/>
  
  <!-- 圆角矩形 -->
  <rect x="150" y="10" width="100" height="50" rx="10" ry="10" fill="green"/>
  
  <!-- 带边框的矩形 -->
  <rect x="10" y="80" width="100" height="50" fill="none" stroke="red" stroke-width="3"/>
</svg>
```

### 2. 圆形 `<circle>`

```html
<svg width="300" height="200">
  <!-- 实心圆 -->
  <circle cx="80" cy="80" r="50" fill="red"/>
  
  <!-- 空心圆 -->
  <circle cx="200" cy="80" r="40" fill="none" stroke="blue" stroke-width="5"/>
</svg>
```

### 3. 椭圆 `<ellipse>`

```html
<svg width="300" height="200">
  <ellipse cx="150" cy="100" rx="80" ry="40" fill="orange"/>
  <ellipse cx="150" cy="100" rx="60" ry="30" fill="yellow"/>
</svg>
```

### 4. 线条 `<line>`

```html
<svg width="300" height="200">
  <!-- 水平线 -->
  <line x1="50" y1="50" x2="250" y2="50" stroke="black" stroke-width="2"/>
  
  <!-- 斜线 -->
  <line x1="50" y1="150" x2="250" y2="100" stroke="red" stroke-width="3"/>
  
  <!-- 虚线 -->
  <line x1="50" y1="180" x2="250" y2="180" stroke="blue" stroke-width="2" stroke-dasharray="5,5"/>
</svg>
```

### 5. 折线 `<polyline>`

```html
<svg width="300" height="200">
  <polyline points="50,50 100,100 150,50 200,100 250,50" 
            fill="none" 
            stroke="green" 
            stroke-width="3"/>
</svg>
```

### 6. 多边形 `<polygon>`

```html
<svg width="300" height="200">
  <!-- 三角形 -->
  <polygon points="150,50 100,150 200,150" fill="lightblue"/>
  
  <!-- 五角星 -->
  <polygon points="100,10 40,198 190,78 10,78 160,198" 
           fill="gold" 
           stroke="orange" 
           stroke-width="2"/>
</svg>
```

## 路径 `<path>`

### 路径 <path>

```html
<svg width="400" height="300">
  <!-- 复杂路径 -->
  <path d="M 100,100
           L 200,100
           L 150,50
           Z
           M 100,150
           C 100,150 150,200 200,150
           S 250,100 300,150"
        fill="none" 
        stroke="purple" 
        stroke-width="3"/>
</svg>
```

### 2. 路径命令详解

```html
<svg width="600" height="400" viewBox="0 0 600 400">
  <!-- M = moveto -->
  <path d="M 50,50" stroke="red" stroke-width="2"/>
  
  <!-- L = lineto -->
  <path d="M 100,50 L 150,100" stroke="blue" stroke-width="2"/>
  
  <!-- H = horizontal lineto -->
  <path d="M 200,50 H 250" stroke="green" stroke-width="2"/>
  
  <!-- V = vertical lineto -->
  <path d="M 300,50 V 100" stroke="orange" stroke-width="2"/>
  
  <!-- C = curveto (三次贝塞尔曲线) -->
  <path d="M 50,150 C 100,100 150,200 200,150" 
        fill="none" stroke="purple" stroke-width="2"/>
  
  <!-- Q = quadratic Bézier curve (二次贝塞尔曲线) -->
  <path d="M 250,150 Q 300,100 350,150" 
        fill="none" stroke="brown" stroke-width="2"/>
  
  <!-- A = elliptical arc (椭圆弧) -->
  <path d="M 400,150 A 50,30 0 0,1 500,150" 
        fill="none" stroke="teal" stroke-width="2"/>
  
  <!-- Z = closepath -->
  <path d="M 50,250 L 100,300 L 150,250 Z" 
        fill="lightgray" stroke="black" stroke-width="2"/>
</svg>
```

## 文本 `<text>`

### 1. 基本文本

```html
<svg width="400" height="200">
  <!-- 基本文本 -->
  <text x="50" y="50" font-family="Arial" font-size="24" fill="black">Hello SVG!</text>
  
  <!-- 带样式的文本 -->
  <text x="50" y="100" 
        font-family="Verdana" 
        font-size="30" 
        font-weight="bold" 
        fill="blue"
        text-decoration="underline">
    Styled Text
  </text>
  
  <!-- 旋转文本 -->
  <text x="200" y="150" 
        font-family="Arial" 
        font-size="20" 
        fill="red"
        transform="rotate(30 200,150)">
    Rotated Text
  </text>
</svg>
```

### 2. 文本路径

```html
<svg width="400" height="200">
  <defs>
    <path id="textPath" d="M 50,100 C 100,50 150,150 200,100 S 300,50 350,100" 
          fill="none" stroke="lightgray"/>
  </defs>
  
  <text>
    <textPath href="#textPath" 
              font-family="Arial" 
              font-size="16" 
              fill="darkblue">
      这是一段沿着曲线路径排列的文本
    </textPath>
  </text>
</svg>
```

## 样式和外观

### 1. 填充和描边

```html
<svg width="400" height="300">
  <!-- 渐变填充 -->
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:rgb(255,255,0);stop-opacity:1" />
      <stop offset="100%" style="stop-color:rgb(255,0,0);stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <rect x="50" y="50" width="100" height="100" fill="url(#grad1)"/>
  
  <!-- 图案填充 -->
  <defs>
    <pattern id="pattern1" patternUnits="userSpaceOnUse" width="20" height="20">
      <circle cx="10" cy="10" r="5" fill="blue"/>
    </pattern>
  </defs>
  
  <circle cx="250" cy="100" r="50" fill="url(#pattern1)"/>
  
  <!-- 多种描边样式 -->
  <rect x="50" y="200" width="100" height="50" 
        fill="none" 
        stroke="green" 
        stroke-width="5"
        stroke-dasharray="10,5"
        stroke-linecap="round"/>
</svg>
```

### 2. 渐变

```html
<svg width="400" height="300">
  <defs>
    <!-- 线性渐变 -->
    <linearGradient id="linearGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff0000"/>
      <stop offset="50%" stop-color="#00ff00"/>
      <stop offset="100%" stop-color="#0000ff"/>
    </linearGradient>
    
    <!-- 径向渐变 -->
    <radialGradient id="radialGrad" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" stop-color="white"/>
      <stop offset="100%" stop-color="blue"/>
    </radialGradient>
  </defs>
  
  <rect x="50" y="50" width="100" height="100" fill="url(#linearGrad)"/>
  <circle cx="250" cy="100" r="50" fill="url(#radialGrad)"/>
</svg>
```

## 滤镜效果

### 1. 常用滤镜

```html
<svg width="600" height="400">
  <defs>
    <!-- 高斯模糊 -->
    <filter id="blur">
      <feGaussianBlur in="SourceGraphic" stdDeviation="5"/>
    </filter>
    
    <!-- 投影 -->
    <filter id="shadow">
      <feDropShadow dx="5" dy="5" stdDeviation="3" flood-color="rgba(0,0,0,0.5)"/>
    </filter>
    
    <!-- 颜色矩阵 -->
    <filter id="saturate">
      <feColorMatrix type="saturate" values="0.2"/>
    </filter>
  </defs>
  
  <!-- 应用滤镜 -->
  <circle cx="100" cy="100" r="40" fill="red" filter="url(#blur)"/>
  <circle cx="250" cy="100" r="40" fill="blue" filter="url(#shadow)"/>
  <circle cx="400" cy="100" r="40" fill="green" filter="url(#saturate)"/>
</svg>
```

## 变换和动画

### 1. 变换操作

```html
<svg width="400" height="300">
  <!-- 原始位置 -->
  <rect x="50" y="50" width="50" height="50" fill="red" opacity="0.5"/>
  
  <!-- 平移 -->
  <rect x="50" y="50" width="50" height="50" fill="blue" opacity="0.5"
        transform="translate(100,0)"/>
  
  <!-- 旋转 -->
  <rect x="50" y="50" width="50" height="50" fill="green" opacity="0.5"
        transform="rotate(45 75,75)"/>
  
  <!-- 缩放 -->
  <rect x="50" y="50" width="50" height="50" fill="orange" opacity="0.5"
        transform="scale(1.5) translate(100,100)"/>
</svg>
```

### 2. SMIL 动画

```html
<svg width="400" height="300">
  <!-- 移动动画 -->
  <circle cx="50" cy="50" r="20" fill="red">
    <animate attributeName="cx" from="50" to="350" dur="3s" repeatCount="indefinite"/>
  </circle>
  
  <!-- 颜色动画 -->
  <rect x="50" y="100" width="100" height="50" fill="blue">
    <animate attributeName="fill" values="blue;green;red;blue" dur="4s" repeatCount="indefinite"/>
  </rect>
  
  <!-- 变换动画 -->
  <rect x="200" y="100" width="50" height="50" fill="purple">
    <animateTransform attributeName="transform" 
                      type="rotate"
                      from="0 225 125" 
                      to="360 225 125" 
                      dur="2s" 
                      repeatCount="indefinite"/>
  </rect>
</svg>
```

## 交互性

### 1. 鼠标交互

```html
<svg width="400" height="300">
  <style>
    .interactive:hover {
      fill: orange;
      stroke: red;
      stroke-width: 3;
      cursor: pointer;
    }
    
    .interactive:active {
      fill: red;
    }
  </style>
  
  <circle class="interactive" cx="100" cy="100" r="40" fill="blue"/>
  <rect class="interactive" x="200" y="60" width="80" height="80" fill="green"/>
</svg>
```

### 2. JavaScript 交互

```html
<svg width="400" height="300" id="interactiveSVG">
  <circle id="draggableCircle" cx="100" cy="100" r="30" fill="red" 
          style="cursor: move;"/>
  
  <rect id="colorChanger" x="200" y="80" width="60" height="60" fill="blue"
        style="cursor: pointer;"/>
</svg>

<script>
  // 拖拽功能
  const circle = document.getElementById('draggableCircle');
  let isDragging = false;
  
  circle.addEventListener('mousedown', () => isDragging = true);
  document.addEventListener('mousemove', (e) => {
    if (isDragging) {
      circle.setAttribute('cx', e.clientX);
      circle.setAttribute('cy', e.clientY);
    }
  });
  document.addEventListener('mouseup', () => isDragging = false);
  
  // 颜色切换
  const rect = document.getElementById('colorChanger');
  const colors = ['blue', 'green', 'red', 'purple', 'orange'];
  let colorIndex = 0;
  
  rect.addEventListener('click', () => {
    colorIndex = (colorIndex + 1) % colors.length;
    rect.setAttribute('fill', colors[colorIndex]);
  });
</script>
```

## 实用示例

### 1. 数据可视化图表

```html
<svg width="600" height="400" id="chart">
  <defs>
    <linearGradient id="barGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#4facfe"/>
      <stop offset="100%" stop-color="#00f2fe"/>
    </linearGradient>
  </defs>
  
  <!-- 坐标轴 -->
  <line x1="50" y1="350" x2="550" y2="350" stroke="black" stroke-width="2"/>
  <line x1="50" y1="350" x2="50" y2="50" stroke="black" stroke-width="2"/>
  
  <!-- 数据标签 -->
  <text x="300" y="390" text-anchor="middle" font-family="Arial" font-size="14">月份</text>
  <text x="20" y="200" text-anchor="middle" font-family="Arial" font-size="14" transform="rotate(-90 20,200)">销售额</text>
</svg>

<script>
  const data = [
    { month: '1月', value: 120 },
    { month: '2月', value: 200 },
    { month: '3月', value: 150 },
    { month: '4月', value: 300 },
    { month: '5月', value: 250 },
    { month: '6月', value: 400 }
  ];
  
  const chart = document.getElementById('chart');
  const maxValue = Math.max(...data.map(d => d.value));
  
  data.forEach((item, index) => {
    const barWidth = 40;
    const barSpacing = 20;
    const x = 80 + index * (barWidth + barSpacing);
    const height = (item.value / maxValue) * 250;
    const y = 350 - height;
    
    // 创建柱状图
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', x);
    rect.setAttribute('y', y);
    rect.setAttribute('width', barWidth);
    rect.setAttribute('height', height);
    rect.setAttribute('fill', 'url(#barGradient)');
    rect.setAttribute('rx', '3');
    
    // 添加数据标签
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', x + barWidth / 2);
    text.setAttribute('y', 370);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-family', 'Arial');
    text.setAttribute('font-size', '12');
    text.textContent = item.month;
    
    // 数值标签
    const valueText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    valueText.setAttribute('x', x + barWidth / 2);
    valueText.setAttribute('y', y - 5);
    valueText.setAttribute('text-anchor', 'middle');
    valueText.setAttribute('font-family', 'Arial');
    valueText.setAttribute('font-size', '10');
    valueText.textContent = item.value;
    
    chart.appendChild(rect);
    chart.appendChild(text);
    chart.appendChild(valueText);
  });
</script>
```

### 2. 图标系统

```html
<svg style="display: none;">
  <defs>
    <!-- 主页图标 -->
    <symbol id="home-icon" viewBox="0 0 24 24">
      <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" fill="currentColor"/>
    </symbol>
    
    <!-- 设置图标 -->
    <symbol id="settings-icon" viewBox="0 0 24 24">
      <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z" fill="currentColor"/>
    </symbol>
  </defs>
</svg>

<div class="icon-container">
  <svg class="icon" width="24" height="24">
    <use href="#home-icon"/>
  </svg>
  主页
  
  <svg class="icon" width="24" height="24">
    <use href="#settings-icon"/>
  </svg>
  设置
</div>

<style>
  .icon-container {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: Arial;
  }
  
  .icon {
    color: #666;
    transition: color 0.3s;
  }
  
  .icon:hover {
    color: #007bff;
  }
</style>
```

## 最佳实践

### 1. 性能优化

```html
<!-- 使用 symbol 和 use 重用元素 -->
<svg style="display: none;">
  <symbol id="reusable-shape">
    <path d="M10 10 H 90 V 90 H 10 Z" fill="blue"/>
  </symbol>
</svg>

<svg width="200" height="200">
  <use href="#reusable-shape" x="0" y="0"/>
  <use href="#reusable-shape" x="100" y="0" fill="red"/>
  <use href="#reusable-shape" x="0" y="100" fill="green"/>
  <use href="#reusable-shape" x="100" y="100" fill="yellow"/>
</svg>
```

### 2. 响应式 SVG

```html
<svg viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet" 
     style="width: 100%; height: auto;">
  <circle cx="50" cy="50" r="40" fill="blue"/>
</svg>
```

## 总结

SVG 的优势：
- 矢量图形 - 无限缩放不失真
- 文件体积小 - 适合网络传输
- 可编程性 - 支持 JavaScript 交互
- 可访问性 - 支持屏幕阅读器
- 动画支持 - 内置动画和过渡效果

应用场景：
- 数据可视化
- 用户界面图标
- 交互式图形
- 地图和图表
- logo 和品牌元素
