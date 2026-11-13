# CSS 动画

CSS 动画允许元素在一段时间内从一个状态平滑地过渡到另一个或多个状态，不需要 JavaScript。

CSS 动画由两部分组成：

-   `@keyframes` —— 定义动画过程
-   `animation` 属性 —— 控制动画的播放方式

## `@keyframes` 规则

定义动画的关键帧序列。

```css
/* 基础语法 */
@keyframes animation-name {
    from {
        /* 起始状态 */
    }
    to {
        /* 结束状态 */
    }
}

/* 百分比语法 推荐 */
@keyframes animation-name {
    0% {
        /* 状态 */
    }
    50% {
        /* 状态 */
    }
    100% {
        /* 状态 */
    }
}

/* 示例 */
@keyframes slideIn {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes bounce {
    0%,
    20%,
    50%,
    80%,
    100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-30px);
    }
    60% {
        transform: translateY(-15px);
    }
}

@keyframes colorChange {
    0% {
        background-color: red;
    }
    33% {
        background-color: yellow;
    }
    66% {
        background-color: blue;
    }
    100% {
        background-color: green;
    }
}
```

## `Animation` 属性

简写语法：

```css
.element {
    animation: name duration timing-function delay iteration-count direction fill-mode play-state;
}
```

```css
/* 简写 */
.box {
    animation: move 2s ease-in-out 0s infinite alternate;
}

/* 单个属性写法 */
.box {
    animation-name: move;
    animation-duration: 2s;
    animation-timing-function: ease;
    animation-delay: 0s;
    animation-iteration-count: infinite;
    animation-direction: alternate;
    animation-fill-mode: both;
    animation-play-state: running;
}
```

### 详细属性

#### `animation-name`

指定要使用的`@keyframes`名称。

```css
animation-name: slideIn;
```

#### `animation-duration`

动画完成一个周期所需时间。

```css
animation-duration: 2s; /* 2秒 */
animation-duration: 500ms; /* 500毫秒 */
```

#### `animation-timing-function`

动画的速度曲线。

```css
animation-timing-function: ease; /* 默认 */
animation-timing-function: linear; /* 匀速 */
animation-timing-function: ease-in; /* 慢开始 */
animation-timing-function: ease-out; /* 慢结束 */
animation-timing-function: ease-in-out; /* 慢开始和结束 */
animation-timing-function: cubic-bezier(0.1, 0.7, 1, 0.1); /* 自定义 */
animation-timing-function: steps(4, jump-start); /* 步进动画 */
```

#### `animation-delay`

动画开始前的延迟时间。

```css
animation-delay: 1s; /* 延迟1秒 */
animation-delay: -1s; /* 从第1秒开始 */
```

#### `animation-iteration-count`

动画播放次数。

```css
animation-iteration-count: 1; /* 播放1次 */
animation-iteration-count: 3; /* 播放3次 */
animation-iteration-count: infinite; /* 无限循环 */
```

#### `animation-direction`

动画是否反向播放。

```css
animation-direction: normal; /* 正常播放 */
animation-direction: reverse; /* 反向播放 */
animation-direction: alternate; /* 奇数次正向，偶数次反向 */
animation-direction: alternate-reverse; /* 奇数次反向，偶数次正向 */
```

#### `animation-fill-mode`

动画执行前后如何应用样式。

```css
animation-fill-mode: none; /* 默认，动画前后不应用任何样式 */
animation-fill-mode: forwards; /* 动画结束后保持最后一帧的样式 */
animation-fill-mode: backwards; /* 动画开始前应用第一帧的样式 */
animation-fill-mode: both; /* 同时应用forwards和backwards */
```

#### `animation-play-state`

控制动画的播放状态。

```css
animation-play-state: running; /* 正在播放 */
animation-play-state: paused; /* 暂停播放 */
```

## 完整示例

### 示例 1：基础动画

```css
/* 定义动画 */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 应用动画 */
.element {
    animation: fadeInUp 1s ease-out 0.5s both;
}

/* 分开写法 */
.element {
    animation-name: fadeInUp;
    animation-duration: 1s;
    animation-timing-function: ease-out;
    animation-delay: 0.5s;
    animation-fill-mode: both;
}
```

### 示例 2：复杂动画序列

```css
@keyframes loading {
    0% {
        transform: rotate(0deg);
        width: 50px;
        height: 50px;
    }
    25% {
        background-color: #ff6b6b;
        border-radius: 50%;
    }
    50% {
        transform: rotate(180deg);
        width: 80px;
        height: 80px;
    }
    75% {
        background-color: #4ecdc4;
        border-radius: 10%;
    }
    100% {
        transform: rotate(360deg);
        width: 50px;
        height: 50px;
    }
}

.loader {
    animation: loading 2s ease-in-out infinite alternate;
}
```

### 示例 3：多个动画组合

```css
@keyframes move {
    0% {
        left: 0;
    }
    100% {
        left: calc(100% - 50px);
    }
}

@keyframes color {
    0%,
    100% {
        background-color: red;
    }
    50% {
        background-color: blue;
    }
}

.box {
    position: relative;
    width: 50px;
    height: 50px;
    animation: move 3s linear infinite, color 1.5s ease-in-out infinite;
}
```

## 性能优化技巧

### 1. 优先使用`transform`和`opacity`

```css
/* 性能好 */
@keyframes good-animation {
    to {
        transform: translateX(100px);
        opacity: 0.5;
    }
}

/* 性能差 */
@keyframes bad-animation {
    to {
        margin-left: 100px;
        width: 200px;
    }
}
```

### 2. 使用`will-change`优化

```css
.element {
    will-change: transform, opacity;
    animation: myAnimation 1s;
}
```

### 3. 适当使用硬件加速

```css
.element {
    transform: translateZ(0); /* 触发GPU加速 */
    animation: myAnimation 1s;
}
```

## JavaScript 控制

```js
// 开始/暂停动画
const element = document.querySelector(".element");

// 开始动画
element.style.animationPlayState = "running";

// 暂停动画
element.style.animationPlayState = "paused";

// 监听动画事件
element.addEventListener("animationstart", e => {
    console.log("动画开始");
});

element.addEventListener("animationend", e => {
    console.log("动画结束");
});

element.addEventListener("animationiteration", e => {
    console.log("动画循环一次");
});

// 动态添加动画
element.style.animation = "fadeIn 1s forwards";

// 重置动画
element.style.animation = "none";
void element.offsetWidth; // 触发重排
element.style.animation = "fadeIn 1s forwards";
```

## 与 CSS Transition 的区别

| 特性     | CSS Transition                   | CSS Animation              |
| -------- | -------------------------------- | -------------------------- |
| 触发方式 | 需要状态变化（hover、active 等） | 可以自动播放               |
| 复杂度   | 简单，两个状态之间               | 复杂，多关键帧序列         |
| 控制度   | 有限，只能控制起点和终点         | 完全控制每一帧             |
| 循环播放 | 不可以                           | 可以（infinite）           |
| 方向控制 | 只能正向                         | 可以正向、反向、交替       |
| 暂停控制 | 有限                             | 完全控制（paused/running） |

## 实际应用场景

### 1. 加载动画

```css
@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.spinner {
    animation: spin 1s linear infinite;
}
```

### 2. 骨架屏动画

```css
@keyframes shimmer {
    0% {
        background-position: -200px 0;
    }
    100% {
        background-position: calc(200px + 100%) 0;
    }
}

.skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200px 100%;
    animation: shimmer 1.5s infinite linear;
}
```

### 打字机效果

```css
@keyframes typing {
    from {
        width: 0;
    }
    to {
        width: 100%;
    }
}

@keyframes blink {
    50% {
        border-color: transparent;
    }
}

.typewriter {
    overflow: hidden;
    border-right: 3px solid;
    white-space: nowrap;
    animation: typing 3.5s steps(40, end), blink 0.75s step-end infinite;
}
```

## 浏览器兼容性

```css
/* 前缀版本 */
@-webkit-keyframes fadeIn {
    /* Webkit browsers */
}
@keyframes fadeIn {
    /* Standard */
}

.element {
    -webkit-animation: fadeIn 1s; /* Chrome, Safari */
    animation: fadeIn 1s;
}
```

## 最佳实践

-   使用简写属性：提高可读性
-   设置 animation-fill-mode：避免动画闪动
-   考虑用户体验：动画不应影响操作
-   测试性能：复杂动画在移动设备上可能卡顿
-   提供暂停机制：尊重用户偏好
