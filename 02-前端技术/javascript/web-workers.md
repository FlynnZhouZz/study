# HTML5 Web Workers

Web Workers 是一项强大的浏览器功能，它允许在 Web 应用程序的后台线程中运行 JavaScript 代码，而不会阻塞主线程（通常是 UI 线程）。

## 什么是 Web Workers？为什么需要它？

核心问题：JavaScript 是单线程的

浏览器中，JavaScript 运行在单个线程（主线程）上。这个线程负责处理一切：渲染 UI、响应用户交互（点击、滚动）、执行 JavaScript 逻辑等。如果有一个计算密集型任务（例如循环处理大量数据、复杂的图像处理），它会阻塞主线程，导致页面卡顿、无响应，用户体验极差。

Web Workers 的解决方案

Web Workers 允许开发者创建一个在后台运行的“Worker 线程”。你可以将一些繁重的计算任务交给 Worker 去处理。在此期间，主线程可以继续保持响应，处理用户交互和页面渲染。当 Worker 完成任务后，再通过消息机制将结果返回给主线程。

## Web Workers 的核心特性

1. 真正的多线程： Worker 运行在独立的全局上下文中，与主线程并行执行。
2. 不阻塞主线程： 在 Worker 中执行耗时任务不会影响页面的响应性。
3. 通信机制： Worker 和主线程之间通过消息传递进行通信，使用 postMessage 方法和 onmessage 事件处理器。数据是复制的，而不是共享的（但可以使用 Transferable Objects 来转移所有权，提高性能）。
4. 安全限制：
    - 同源策略： Worker 脚本必须与主脚本同源。
    - DOM 限制： Worker 无法直接访问 DOM。它不能操作 document、window 或 parent 对象。这是为了保持线程安全。
    - 全局对象： Worker 内部全局对象是 DedicatedWorkerGlobalScope 或 SharedWorkerGlobalScope，而不是 Window。

## 案例

> 运行后，页面不会卡住 —— 因为计算在 Worker 的后台线程进行。

index.html:

```html
<!DOCTYPE html>
<html>
    <body>
        <button onclick="startWorker()">开始计算</button>
        <p id="result"></p>

        <script>
            let worker;

            function startWorker() {
                // 创建 Worker
                worker = new Worker("worker.js");

                // 接收 Worker 发送的消息
                worker.onmessage = function (event) {
                    document.getElementById("result").innerText = "后台计算结果：" + event.data;
                };

                // 发送消息给 Worker（可选）
                worker.postMessage("start");
            }
        </script>
    </body>
</html>
```

worker.js:

```js
// 接收主线程的消息
onmessage = function (event) {
    // 模拟耗时任务（累加 1~1e8）
    let sum = 0;
    for (let i = 0; i < 100000000; i++) {
        sum += i;
    }

    // 把结果发送给主线程
    postMessage(sum);
};
```

## 知识点

### 1. Worker 无法访问 DOM

Worker 处于独立线程，没有 window / document：
- 不能修改 DOM
- 不能访问 document
- 不能 alert()

但它可以：
- 访问定时器（setTimeout）
- 访问 XMLHttpRequest / fetch
- 导入脚本 importScripts()

### 2. 主线程与 Worker 的通信

主线程 → Worker：
```js
worker.postMessage("hello");

```

Worker → 主线程：
```js
postMessage({ count: 100 });
```

主线程接收：
```js
worker.onmessage = (e) => console.log(e.data);
```

Worker 接收：
```js
onmessage = (e) => console.log(e.data);
```

主线程终止：
```js
worker.terminate();
```

Worker 自己终止：
```js
close();
```

## 什么时候要用 Web Worker？

- 大量循环计算（数学计算、解析 JSON、大列表处理）
- 图像处理（像素处理、Canvas 图片转换）
- 加密 / 解密
- 解压 zip 文件
- 数据库查询（IndexedDB）
- AI 模型本地推理（TensorFlow.js）

只要任务可能卡住 UI，就应该丢到 Worker。




