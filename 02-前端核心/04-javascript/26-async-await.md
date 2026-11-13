# async/await

## 基本概念

1. async 函数

-   总是返回一个 Promise
-   可以使用 await 关键字

2. await 表达式

-   只能在 async 函数内部使用
-   暂停 async 函数的执行，等待 Promise 解决

## 基本用法

### 1. async 函数声明

```js
// 函数声明
async function getData() {
    return "Hello async";
}

// 函数表达式
const getData = async function () {
    return "Hello async";
};

// 箭头函数
const getData = async () => {
    return "Hello async";
};

// 对象方法
const obj = {
    async fetchData() {
        return "data";
    },
};

// 类方法
class ApiClient {
    async request() {
        return "response";
    }
}
```

### 2. await 使用

```js
async function example() {
    // 等待一个 Promise
    const result = await Promise.resolve(42);
    console.log(result); // 42

    // 等待多个独立的 Promise（顺序执行）
    const data1 = await fetchData1();
    const data2 = await fetchData2();

    // 并行执行（推荐）
    const [data1, data2] = await Promise.all([fetchData1(), fetchData2()]);
}
```

## 错误处理

### 1. try...catch

```js
async function fetchWithRetry(url, retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.log(`Attempt ${i + 1} failed:`, error.message);
            if (i === retries - 1) throw error;
            await wait(1000 * (i + 1)); // 指数退避
        }
    }
}

function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
```

### 2. 结合 .catch()

```js
// 方法1：async 函数返回 Promise，可以用 .catch()
async function getUser() {
    const response = await fetch("/api/user");
    return response.json();
}

getUser()
    .then(user => console.log(user))
    .catch(error => console.error("Error:", error));

// 方法2：立即执行函数
(async () => {
    try {
        const user = await getUser();
        console.log(user);
    } catch (error) {
        console.error("Error:", error);
    }
})();
```

## 进阶用法

### 1. 并发控制

```js
// 使用 for...of 顺序执行
async function processItems(items) {
    const results = [];
    for (const item of items) {
        const result = await processItem(item);
        results.push(result);
    }
    return results;
}

// 并行执行，控制并发数
async function parallelWithLimit(items, concurrency = 3) {
    const results = [];
    const executing = [];

    for (const item of items) {
        const p = processItem(item).then(result => {
            results.push(result);
        });
        executing.push(p);

        if (executing.length >= concurrency) {
            await Promise.race(executing);
        }
    }

    await Promise.all(executing);
    return results;
}

// 使用 async-pool 库的简化实现
async function asyncPool(poolLimit, array, iteratorFn) {
    const ret = [];
    const executing = new Set();

    for (const item of array) {
        const p = Promise.resolve().then(() => iteratorFn(item));
        ret.push(p);
        executing.add(p);

        const clean = () => executing.delete(p);
        p.then(clean).catch(clean);

        if (executing.size >= poolLimit) {
            await Promise.race(executing);
        }
    }

    return Promise.all(ret);
}
```

### 2. 取消操作

```js
// 使用 AbortController
function createCancellableFetch() {
    const controller = new AbortController();

    async function fetchWithCancel(url) {
        try {
            const response = await fetch(url, {
                signal: controller.signal,
            });
            return await response.json();
        } catch (error) {
            if (error.name === "AbortError") {
                console.log("Fetch aborted");
                return null;
            }
            throw error;
        }
    }

    function cancel() {
        controller.abort();
    }

    return { fetch: fetchWithCancel, cancel };
}

// 使用示例
const { fetch, cancel } = createCancellableFetch();

// 开始请求
const promise = fetch("https://api.example.com/data");

// 5秒后取消
setTimeout(() => cancel(), 5000);
```

### 3. 超时处理

```js
// 为 Promise 添加超时
function withTimeout(promise, timeout) {
    let timer;
    const timeoutPromise = new Promise((_, reject) => {
        timer = setTimeout(() => {
            reject(new Error(`Timeout after ${timeout}ms`));
        }, timeout);
    });

    return Promise.race([promise, timeoutPromise]).finally(() => clearTimeout(timer));
}

// 使用示例
async function fetchWithTimeout(url, timeout = 5000) {
    try {
        const response = await withTimeout(fetch(url), timeout);
        return await response.json();
    } catch (error) {
        if (error.message.includes("Timeout")) {
            console.log("Request timed out");
        }
        throw error;
    }
}
```

## 常见模式

### 1. 重试模式

```js
async function retry(fn, retries = 3, delay = 1000) {
    for (let i = 0; i < retries; i++) {
        try {
            return await fn();
        } catch (error) {
            if (i === retries - 1) throw error;

            console.log(`Retry ${i + 1} after ${delay}ms`);
            await new Promise(resolve => setTimeout(resolve, delay));

            // 指数退避
            delay *= 2;
        }
    }
}

// 使用示例
async function unstableApiCall() {
    const response = await fetch("https://api.example.com");
    if (Math.random() > 0.7) throw new Error("Random failure");
    return response.json();
}

// 最多重试3次
const result = await retry(unstableApiCall, 3, 1000);
```

### 2. 缓存模式

```js
function createCachedAsync(fn, ttl = 60000) {
    // 默认缓存1分钟
    const cache = new Map();

    return async function (...args) {
        const key = JSON.stringify(args);
        const cached = cache.get(key);

        if (cached) {
            const [value, timestamp] = cached;
            if (Date.now() - timestamp < ttl) {
                console.log("Cache hit");
                return value;
            }
        }

        console.log("Cache miss");
        const result = await fn(...args);
        cache.set(key, [result, Date.now()]);
        return result;
    };
}

// 使用示例
const cachedFetch = createCachedAsync(async url => {
    const response = await fetch(url);
    return response.json();
});

// 第一次调用会实际请求
const data1 = await cachedFetch("https://api.example.com/data");

// 60秒内再次调用，返回缓存
const data2 = await cachedFetch("https://api.example.com/data");
```

### 3. 批量处理

```js
class BatchProcessor {
    constructor(batchSize = 10, delay = 100) {
        this.batchSize = batchSize;
        this.delay = delay;
        this.queue = [];
        this.timer = null;
    }

    add(task) {
        return new Promise((resolve, reject) => {
            this.queue.push({ task, resolve, reject });

            if (!this.timer) {
                this.timer = setTimeout(() => this.process(), this.delay);
            }

            if (this.queue.length >= this.batchSize) {
                clearTimeout(this.timer);
                this.process();
            }
        });
    }

    async process() {
        if (this.queue.length === 0) return;

        const batch = this.queue.splice(0, this.batchSize);
        clearTimeout(this.timer);
        this.timer = null;

        try {
            const results = await Promise.all(batch.map(item => item.task()));

            batch.forEach((item, index) => {
                item.resolve(results[index]);
            });
        } catch (error) {
            batch.forEach(item => {
                item.reject(error);
            });
        }

        // 如果还有剩余，继续处理
        if (this.queue.length > 0) {
            this.timer = setTimeout(() => this.process(), this.delay);
        }
    }
}

// 使用示例
const batchProcessor = new BatchProcessor(5, 50);

async function simulateApi(id) {
    await new Promise(resolve => setTimeout(resolve, Math.random() * 100));
    return `Result ${id}`;
}

// 添加100个任务，但会批量处理
const promises = [];
for (let i = 0; i < 100; i++) {
    promises.push(batchProcessor.add(() => simulateApi(i)));
}

const results = await Promise.all(promises);
```

## 性能优化

### 1. 避免不必要的 await

```js
// ❌ 不好：顺序执行，时间更长
async function slow() {
    const user = await fetchUser();
    const posts = await fetchPosts();
    const comments = await fetchComments();
    return { user, posts, comments }; // 总时间 = t1 + t2 + t3
}

// ✅ 好：并行执行
async function fast() {
    const [user, posts, comments] = await Promise.all([fetchUser(), fetchPosts(), fetchComments()]);
    return { user, posts, comments }; // 总时间 = max(t1, t2, t3)
}
```

### 2. 提前 await

```js
// ❌ 不好：在循环中 await
async function processAll(items) {
    const results = [];
    for (const item of items) {
        // 每次循环都等待
        const result = await processItem(item);
        results.push(result);
    }
    return results;
}

// ✅ 好：收集所有 Promise，然后一次性 await
async function processAllBetter(items) {
    const promises = items.map(item => processItem(item));
    return await Promise.all(promises);
}

// ✅ 或者分批处理
async function processInBatches(items, batchSize = 10) {
    const results = [];
    for (let i = 0; i < items.length; i += batchSize) {
        const batch = items.slice(i, i + batchSize);
        const batchPromises = batch.map(item => processItem(item));
        const batchResults = await Promise.all(batchPromises);
        results.push(...batchResults);
    }
    return results;
}
```

### 3. 使用 async generator

```js
// 流式处理大数据集
async function* asyncGenerator(dataSource) {
    let page = 1;

    while (true) {
        const data = await fetchPage(dataSource, page);
        if (data.length === 0) break;

        for (const item of data) {
            yield item;
        }

        page++;
    }
}

// 使用 async generator
async function processLargeDataset() {
    const generator = asyncGenerator("https://api.example.com/items");

    for await (const item of generator) {
        await processItem(item);

        // 可以随时中断
        if (shouldStop()) break;
    }
}
```

## 调试技巧

### 1. 调试异步调用栈

```js
// 使用 async_hooks（Node.js）
const async_hooks = require("async_hooks");

// 或使用 source-map 和错误追踪
async function debugAsync(fn) {
    const originalPrepareStackTrace = Error.prepareStackTrace;

    Error.prepareStackTrace = (error, stack) => {
        return stack.map(frame => {
            return {
                file: frame.getFileName(),
                line: frame.getLineNumber(),
                column: frame.getColumnNumber(),
                function: frame.getFunctionName(),
            };
        });
    };

    try {
        return await fn();
    } catch (error) {
        console.log("Async call stack:", error.stack);
        throw error;
    } finally {
        Error.prepareStackTrace = originalPrepareStackTrace;
    }
}
```

### 2. 监控异步操作

```js
class AsyncMonitor {
    constructor() {
        this.active = new Map();
        this.completed = [];
    }

    track(name, promise) {
        const id = Symbol(name);
        const start = Date.now();

        this.active.set(id, { name, start });

        const cleanup = () => {
            const duration = Date.now() - start;
            this.active.delete(id);
            this.completed.push({ name, duration });

            // 只保留最近100条记录
            if (this.completed.length > 100) {
                this.completed.shift();
            }
        };

        promise.then(cleanup, cleanup);
        return promise;
    }

    getStats() {
        return {
            active: Array.from(this.active.values()),
            recent: this.completed.slice(-10),
        };
    }
}

// 使用示例
const monitor = new AsyncMonitor();

async function monitoredFetch(url) {
    return monitor.track(`fetch:${url}`, fetch(url));
}
```

## 最佳实践总结

-   总是使用 try...catch 或 .catch() 处理错误
-   并行执行 独立的异步操作
-   合理控制并发，避免资源耗尽
-   添加超时 防止无限等待
-   考虑实现重试逻辑 处理暂时性错误
-   避免在循环中使用 await，尽量使用 Promise.all
-   使用 async/await 替代复杂的 Promise 链
-   在适当的地方添加缓存 提高性能
-   考虑使用第三方库 处理复杂场景：
    -   `p-limit` - 并发控制
    -   `p-retry` - 重试逻辑
    -   `p-timeout` - 超时处理
    -   `p-map` / `p-filter` - 异步数组操作
-   注意内存泄漏：及时清理不再需要的异步操作引用
