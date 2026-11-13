# arguments 对象

arguments 是一个类数组对象，在函数内部自动可用，包含所有传递给函数的参数。

```js
function showArgs() {
    console.log(arguments);
    console.log(arguments.length);
    console.log(arguments[0]); // 第一个参数
    console.log(arguments[1]); // 第二个参数
}

showArgs("a", "b", "c");
// 输出：
// Arguments(3) ['a', 'b', 'c']
// 3
// 'a'
// 'b'

// arguments 只能在函数内部访问
console.log(arguments); // 在全局作用域报错：arguments is not defined
```

## arguments 的特性

```js
function demonstrateArguments() {
    // 1. 类数组对象
    console.log(typeof arguments); // 'object'
    console.log(Array.isArray(arguments)); // false

    // 2. 有 length 属性
    console.log("参数个数:", arguments.length);

    // 3. 可以通过索引访问
    for (let i = 0; i < arguments.length; i++) {
        console.log(`参数 ${i}:`, arguments[i]);
    }

    // 4. 有 callee 属性（指向当前函数）
    console.log("callee:", arguments.callee);

    // 5. 有 iterator 接口（ES6+）
    console.log(Symbol.iterator in arguments); // true

    // 6. 有 caller 属性（已废弃）
    // console.log(arguments.caller); // 严格模式下报错
}

demonstrateArguments(1, 2, 3, 4, 5);
```

## arguments 的转换与使用

### 1. 转换为数组

```js
function convertToArray() {
    // 方法1：Array.from（ES6）
    const arr1 = Array.from(arguments);
    console.log("Array.from:", arr1);

    // 方法2：扩展运算符（ES6）
    const arr2 = [...arguments];
    console.log("扩展运算符:", arr2);

    // 方法3：Array.prototype.slice.call
    const arr3 = Array.prototype.slice.call(arguments);
    console.log("slice.call:", arr3);

    // 方法4：遍历（最兼容）
    const arr4 = [];
    for (let i = 0; i < arguments.length; i++) {
        arr4.push(arguments[i]);
    }
    console.log("遍历创建:", arr4);

    // 方法5：Object.values
    const arr5 = Object.values(arguments);
    console.log("Object.values:", arr5);

    // 验证
    console.log(
        "都是数组吗?",
        Array.isArray(arr1),
        Array.isArray(arr2),
        Array.isArray(arr3),
        Array.isArray(arr4),
        Array.isArray(arr5)
    );
}

convertToArray("a", "b", "c", "d");
```

### 2. arguments 与剩余参数比较

```js
// 传统的 arguments 方式
function sumWithArguments() {
    let total = 0;
    for (let i = 0; i < arguments.length; i++) {
        total += arguments[i];
    }
    return total;
}

// ES6 剩余参数方式
function sumWithRest(...numbers) {
    return numbers.reduce((total, num) => total + num, 0);
}

// 比较
console.log(sumWithArguments(1, 2, 3, 4)); // 10
console.log(sumWithRest(1, 2, 3, 4)); // 10

// 关键区别
function compareMethods(regularParam, ...restParams) {
    console.log("常规参数:", regularParam); // 'first'
    console.log("剩余参数:", restParams); // ['second', 'third']
    console.log("arguments:", arguments); // Arguments(3) ['first', 'second', 'third']
    console.log("arguments[0]:", arguments[0]); // 'first'
}

compareMethods("first", "second", "third");

// 箭头函数没有自己的 arguments
const arrowFunc = () => {
    console.log("箭头函数arguments:", arguments); // 引用外层函数的arguments
};

function outer() {
    const inner = () => {
        console.log("inner arguments:", arguments); // 引用outer的arguments
    };
    inner();
}

outer("test"); // inner arguments: Arguments ['test']
```

## arguments.callee

### 1. callee 的基本使用

```js
// callee 引用当前正在执行的函数
function factorial(n) {
    if (n <= 1) return 1;
    return n * arguments.callee(n - 1); // 递归调用自身
}

console.log(factorial(5)); // 120

// 匿名函数的递归
const factorialAnon = function (n) {
    if (n <= 1) return 1;
    return n * arguments.callee(n - 1);
};

console.log(factorialAnon(5)); // 120
```

### 2. callee 的问题与替代方案

```js
// 问题1：在严格模式下禁用
function strictModeExample() {
    "use strict";
    // console.log(arguments.callee); // 报错：TypeError
}

// 问题2：优化问题，妨碍内联和尾调用优化

// 替代方案1：命名函数表达式
const factorial = function fact(n) {
    if (n <= 1) return 1;
    return n * fact(n - 1); // 使用函数名
};

// 替代方案2：使用函数声明
function factorialDecl(n) {
    if (n <= 1) return 1;
    return n * factorialDecl(n - 1);
}

// 替代方案3：Y组合子（函数式编程）
const Y = f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y)));
const factorialY = Y(f => n => n <= 1 ? 1 : n * f(n - 1));

console.log(factorialY(5)); // 120
```

## 实际应用场景

### 1. 创建灵活的构造函数

```js
// 模拟 Function.prototype.bind
function bind(fn, context) {
    // 获取绑定时除前两个参数外的所有参数
    const bindArgs = Array.prototype.slice.call(arguments, 2);

    return function () {
        // 获取调用时的参数
        const callArgs = Array.prototype.slice.call(arguments);

        // 合并参数并调用原函数
        const allArgs = bindArgs.concat(callArgs);
        return fn.apply(context, allArgs);
    };
}

// 使用示例
function greet(greeting, punctuation) {
    console.log(greeting + ", " + this.name + punctuation);
}

const person = { name: "John" };
const greetJohn = bind(greet, person, "Hello");
greetJohn("!"); // "Hello, John!"
```

### 2. 实现柯里化函数

```js
// 使用 arguments 实现柯里化
function curry(fn) {
    // 获取期望的参数个数
    const arity = fn.length;

    return function curried() {
        // 获取当前参数
        const args = Array.prototype.slice.call(arguments);

        if (args.length >= arity) {
            // 参数足够，直接调用
            return fn.apply(this, args);
        } else {
            // 参数不足，返回新函数
            return function () {
                const moreArgs = Array.prototype.slice.call(arguments);
                return curried.apply(this, args.concat(moreArgs));
            };
        }
    };
}

// 使用示例
function add(a, b, c) {
    return a + b + c;
}

const curriedAdd = curry(add);
console.log(curriedAdd(1)(2)(3)); // 6
console.log(curriedAdd(1, 2)(3)); // 6
console.log(curriedAdd(1)(2, 3)); // 6
```

### 3. 实现函数重载

```js
// 使用 arguments 模拟函数重载
function createElement() {
    // 根据参数个数和类型决定行为
    if (arguments.length === 1) {
        // 一个参数：可能是标签名或HTML字符串
        const arg = arguments[0];
        if (typeof arg === "string") {
            if (arg.startsWith("<")) {
                // HTML字符串
                return parseHTML(arg);
            } else {
                // 标签名
                return document.createElement(arg);
            }
        }
    } else if (arguments.length === 2) {
        // 两个参数：标签名和属性对象
        const [tagName, attributes] = arguments;
        const element = document.createElement(tagName);
        Object.assign(element, attributes);
        return element;
    } else if (arguments.length === 3) {
        // 三个参数：标签名、属性和子元素
        const [tagName, attributes, children] = arguments;
        const element = document.createElement(tagName);
        Object.assign(element, attributes);

        if (Array.isArray(children)) {
            children.forEach(child => element.appendChild(child));
        } else {
            element.appendChild(children);
        }

        return element;
    }

    throw new Error("Invalid arguments");
}

function parseHTML(html) {
    const template = document.createElement("template");
    template.innerHTML = html.trim();
    return template.content.firstChild;
}

// 使用
const div1 = createElement("div");
const div2 = createElement("div", { id: "myDiv", className: "container" });
const div3 = createElement("div", null, createElement("span", null, "Hello"));
const div4 = createElement('<div class="custom">HTML</div>');
```

### 4. 日志与调试工具

```js
// 创建灵活的日志函数
function debug() {
    // 检查环境
    if (process.env.NODE_ENV !== "development") return;

    // 获取调用者信息
    const stack = new Error().stack;
    const callerLine = stack.split("\n")[2];

    // 格式化参数
    const timestamp = new Date().toISOString();
    const args = Array.from(arguments).map(arg => {
        if (typeof arg === "object") {
            try {
                return JSON.stringify(arg, null, 2);
            } catch {
                return String(arg);
            }
        }
        return arg;
    });

    console.log(`[${timestamp}]`, ...args, "\n", callerLine.trim());
}

// 带有条件判断的断言
function assert(condition) {
    if (!condition) {
        const args = Array.from(arguments).slice(1);
        throw new Error("Assertion failed: " + args.join(" "));
    }
}

// 参数验证装饰器
function validateArgs(validatorFn) {
    return function (target, name, descriptor) {
        const original = descriptor.value;

        descriptor.value = function () {
            const args = Array.from(arguments);

            // 验证参数
            if (!validatorFn(args)) {
                throw new Error(`Invalid arguments for ${name}: ${args}`);
            }

            return original.apply(this, args);
        };

        return descriptor;
    };
}

// 使用示例
class Calculator {
    @validateArgs(args => args.every(arg => typeof arg === "number"))
    add(a, b) {
        return a + b;
    }
}
```

## arguments 与 ES6+ 特性的结合

### 1. arguments 与解构赋值

```js
function processUser() {
    // 从 arguments 中解构
    const [name, age, ...rest] = arguments;
    console.log("解构:", { name, age, rest });

    // 或者使用剩余参数（更推荐）
    return { name, age, rest };
}

processUser("John", 30, "developer", "male");

// 处理 arguments 的默认值
function withDefaults() {
    const args = Array.from(arguments);
    const [name = "Anonymous", age = 18, city = "Unknown"] = args;

    console.log(`Name: ${name}, Age: ${age}, City: ${city}`);
}

withDefaults(); // Name: Anonymous, Age: 18, City: Unknown
withDefaults("Alice"); // Name: Alice, Age: 18, City: Unknown
withDefaults("Bob", 25, "NYC"); // Name: Bob, Age: 25, City: NYC
```

### 2. arguments 与生成器函数

```js
// 生成器函数也有 arguments
function* argumentGenerator() {
    console.log("生成器 arguments:", arguments);

    for (let i = 0; i < arguments.length; i++) {
        yield arguments[i];
    }
}

const gen = argumentGenerator("a", "b", "c");
console.log([...gen]); // ['a', 'b', 'c']

// 生成器函数与剩余参数结合
function* combinedGenerator(prefix, ...items) {
    console.log("prefix:", prefix);
    console.log("arguments:", arguments);

    for (const item of items) {
        yield `${prefix}: ${item}`;
    }
}

const combined = combinedGenerator("Item", "A", "B", "C");
console.log([...combined]); // ['Item: A', 'Item: B', 'Item: C']
```

### 3. arguments 与异步函数

```js
async function asyncWithArguments() {
    // 异步函数也有 arguments
    console.log("异步函数 arguments:", arguments);

    // 将 arguments 转换为数组
    const args = Array.from(arguments);

    // 模拟异步操作
    return await Promise.all(
        args.map(arg => new Promise(resolve => setTimeout(() => resolve(`Processed: ${arg}`), 100)))
    );
}

asyncWithArguments("task1", "task2", "task3").then(results => console.log("结果:", results));

// 使用 arguments 创建灵活的异步函数包装器
function withRetry(asyncFn, maxRetries = 3) {
    return async function () {
        const args = arguments;
        let lastError;

        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                return await asyncFn.apply(this, args);
            } catch (error) {
                lastError = error;
                console.log(`尝试 ${attempt} 失败:`, error.message);

                if (attempt < maxRetries) {
                    // 指数退避
                    await new Promise(resolve =>
                        setTimeout(resolve, 100 * Math.pow(2, attempt - 1))
                    );
                }
            }
        }

        throw lastError;
    };
}

// 使用
const unreliableFetch = async function (url) {
    if (Math.random() > 0.5) throw new Error("Network error");
    return `Data from ${url}`;
};

const reliableFetch = withRetry(unreliableFetch, 3);
reliableFetch("https://api.example.com/data").then(console.log);
```

## 性能优化与陷阱

### 1. arguments 的性能问题

```js
// 性能对比测试
function testPerformance() {
    const iterations = 1000000;

    // 测试 arguments 转换的性能
    console.time("arguments 转换");
    for (let i = 0; i < iterations; i++) {
        const args = Array.from(arguments);
    }
    console.timeEnd("arguments 转换");

    // 测试剩余参数的性能
    console.time("剩余参数");
    function restFunc(...args) {
        for (let i = 0; i < iterations; i++) {
            const arr = args;
        }
    }
    restFunc(1, 2, 3);
    console.timeEnd("剩余参数");
}

testPerformance(1, 2, 3);

// 优化建议
function optimizedSum() {
    // 避免在循环中多次访问 arguments
    const args = arguments;
    let total = 0;

    // 缓存 length
    const len = args.length;
    for (let i = 0; i < len; i++) {
        total += args[i];
    }

    return total;
}

// 使用剩余参数（性能更好）
function betterSum(...numbers) {
    return numbers.reduce((total, num) => total + num, 0);
}
```

### 2. 严格模式下的限制

```js
// 非严格模式
function nonStrict() {
    // 可以修改 arguments
    arguments[0] = "modified";
    console.log("非严格模式:", arguments[0]);

    // 可以访问 callee
    console.log("callee:", arguments.callee);
}
nonStrict("original"); // modified

// 严格模式
function strict() {
    "use strict";

    // 不能修改 arguments
    try {
        arguments[0] = "modified";
    } catch (e) {
        console.log("严格模式不能修改 arguments");
    }

    // 不能访问 callee
    try {
        console.log(arguments.callee);
    } catch (e) {
        console.log("严格模式不能访问 callee");
    }

    // arguments 不会跟踪参数变化
    function test(param) {
        param = "changed";
        console.log("param:", param); // 'changed'
        console.log("arguments[0]:", arguments[0]); // 'original'（不是 'changed'）
    }
    test("original");
}
strict();
```

### 3. 常见陷阱

```js
// 陷阱1：arguments 与形参的同步
function syncProblem(a, b) {
    console.log("初始:", { a, b, arguments: [...arguments] });

    a = "changed a";
    arguments[1] = "changed b via arguments";

    console.log("修改后:", { a, b, arguments: [...arguments] });
    // 在非严格模式下，a 和 arguments[0] 不同步
    // 在非严格模式下，b 和 arguments[1] 同步
}

syncProblem("original a", "original b");

// 陷阱2：箭头函数没有 arguments
const arrow = () => {
    console.log("箭头函数 arguments:", arguments); // 引用外层
};

function outer() {
    const inner = () => {
        console.log("inner arguments:", arguments); // 使用outer的arguments
    };
    inner();
}

outer("test");

// 陷阱3：嵌套函数的 arguments
function outerFunc() {
    console.log("outer arguments:", arguments);

    function innerFunc() {
        console.log("inner arguments:", arguments); // 自己的arguments
    }

    innerFunc("inner arg");
}

outerFunc("outer arg");
```

## 现代替代方案

### 1. 剩余参数（Rest Parameters）

```js
// 完全替代 arguments
function modernFunction(first, second, ...rest) {
    console.log("第一个参数:", first);
    console.log("第二个参数:", second);
    console.log("剩余参数:", rest);
    console.log("剩余参数个数:", rest.length);

    // rest 是真正的数组
    console.log("是数组吗?", Array.isArray(rest));

    // 可以直接使用数组方法
    const total = rest.reduce((sum, num) => sum + num, 0);
    console.log("剩余参数总和:", total);

    return { first, second, rest };
}

modernFunction(1, 2, 3, 4, 5, 6);

// 与解构结合
function processConfig(...args) {
    const [name, options = {}, ...callbacks] = args;

    console.log("名称:", name);
    console.log("选项:", options);
    console.log("回调:", callbacks);

    // 调用所有回调
    callbacks.forEach(callback => callback(options));
}

processConfig(
    "我的应用",
    { theme: "dark", debug: true },
    opts => console.log("回调1:", opts),
    opts => console.log("回调2:", opts.theme)
);
```

### 2. 默认参数

```js
// 替代 arguments 的默认值处理
function withDefaultParams(name = "Anonymous", age = 18, city = "Unknown") {
    console.log(`姓名: ${name}, 年龄: ${age}, 城市: ${city}`);
}

withDefaultParams(); // 姓名: Anonymous, 年龄: 18, 城市: Unknown
withDefaultParams("John"); // 姓名: John, 年龄: 18, 城市: Unknown
withDefaultParams("Alice", 25); // 姓名: Alice, 年龄: 25, 城市: Unknown
withDefaultParams("Bob", 30, "NYC"); // 姓名: Bob, 年龄: 30, 城市: NYC

// 动态默认值
function dynamicDefault(date = new Date()) {
    console.log("调用时间:", date.toISOString());
}

dynamicDefault(); // 每次调用都生成新时间
```

### 3. 结构化参数对象

```js
// 使用配置对象替代多个参数
function createUser({ name, age = 18, email, isAdmin = false, preferences = {} } = {}) {
    console.log("创建用户:", { name, age, email, isAdmin, preferences });

    return {
        id: Date.now(),
        name,
        age,
        email,
        isAdmin,
        preferences,
        createdAt: new Date(),
    };
}

// 更清晰的调用方式
const user = createUser({
    name: "John",
    email: "john@example.com",
    age: 30,
    preferences: { theme: "dark" },
});

// 参数验证更简单
function validateUserConfig(config) {
    if (!config.name) throw new Error("Name is required");
    if (!config.email) throw new Error("Email is required");
    if (config.age && (config.age < 0 || config.age > 150)) {
        throw new Error("Invalid age");
    }
}
```

## 最佳实践总结

### 1. 什么时候使用 arguments

```js
// ✅ 适用场景
// 1. 需要支持动态参数的老代码
// 2. 编写库/框架，需要最大兼容性
// 3. 需要访问 callee 的场景（非严格模式）
// 4. 处理不确定数量的参数，且不能使用ES6+特性

// ❌ 避免使用
// 1. 新项目应使用剩余参数(...args)
// 2. 需要严格模式的项目
// 3. 需要优化性能的热点代码
// 4. 可以使用配置对象的情况

// 迁移指南
// 旧代码
function legacySum() {
    let total = 0;
    for (let i = 0; i < arguments.length; i++) {
        total += arguments[i];
    }
    return total;
}

// 新代码
function modernSum(...numbers) {
    return numbers.reduce((total, num) => total + num, 0);
}
```

### 2. 代码示例：兼容性封装

```js
// 封装一个兼容 arguments 和剩余参数的函数
function createFlexibleFunction(fn) {
    return function (...args) {
        // 如果函数期望使用 arguments，我们可以提供一个
        if (fn.length === 0) {
            // 创建一个类 arguments 对象
            const argumentsLike = {
                0: args[0],
                1: args[1],
                2: args[2],
                length: args.length,
                callee: fn,
                [Symbol.iterator]: function* () {
                    for (let i = 0; i < this.length; i++) {
                        yield this[i];
                    }
                },
            };

            // 设置数字索引属性
            for (let i = 0; i < args.length; i++) {
                argumentsLike[i] = args[i];
            }

            // 使用 Proxy 使其更像 arguments
            return new Proxy(argumentsLike, {
                get(target, prop) {
                    if (typeof prop === "string" && /^\d+$/.test(prop)) {
                        const index = parseInt(prop);
                        return index < target.length ? target[index] : undefined;
                    }
                    return target[prop];
                },
                set(target, prop, value) {
                    if (typeof prop === "string" && /^\d+$/.test(prop)) {
                        const index = parseInt(prop);
                        if (index < target.length) {
                            target[index] = value;
                            return true;
                        }
                    }
                    return false;
                },
            });
        }

        return fn(...args);
    };
}

// 使用
const legacyFunc = createFlexibleFunction(function () {
    console.log("参数个数:", arguments.length);
    console.log("第一个参数:", arguments[0]);
    return Array.from(arguments).join(", ");
});

console.log(legacyFunc(1, 2, 3, 4, 5));
```

### 3. 实用工具函数

```js
// 1. 安全的 arguments 转换
function safeArgumentsToArray(args) {
    try {
        return Array.from(args);
    } catch (e) {
        const arr = [];
        for (let i = 0; i < args.length; i++) {
            arr.push(args[i]);
        }
        return arr;
    }
}

// 2. 参数验证包装器
function validateArguments(validator) {
    return function (target, name, descriptor) {
        const original = descriptor.value;

        descriptor.value = function (...args) {
            // 创建 arguments 对象用于老代码
            const argumentsObj = {
                length: args.length,
                [Symbol.iterator]: function* () {
                    for (let i = 0; i < args.length; i++) {
                        yield args[i];
                    }
                },
            };

            for (let i = 0; i < args.length; i++) {
                argumentsObj[i] = args[i];
            }

            // 验证
            if (!validator(argumentsObj)) {
                throw new Error(`Invalid arguments for ${name}`);
            }

            return original.apply(this, args);
        };

        return descriptor;
    };
}

// 3. 参数日志装饰器
function logArguments() {
    return function (target, name, descriptor) {
        const original = descriptor.value;

        descriptor.value = function (...args) {
            console.group(`调用 ${name}`);
            console.log("参数:", args);
            console.log("参数个数:", args.length);

            try {
                const result = original.apply(this, args);
                console.log("结果:", result);
                console.groupEnd();
                return result;
            } catch (error) {
                console.error("错误:", error);
                console.groupEnd();
                throw error;
            }
        };

        return descriptor;
    };
}

// 使用示例
class MathUtils {
    @logArguments()
    @validateArguments(args => args.length >= 2 && args.every(arg => typeof arg === "number"))
    static sum(...numbers) {
        return numbers.reduce((a, b) => a + b, 0);
    }
}

console.log(MathUtils.sum(1, 2, 3, 4, 5)); // 会输出日志并验证参数
```

## 总结要点：

-   arguments 是类数组对象，在函数内部自动可用
-   ES6+ 推荐使用剩余参数，它更安全、性能更好
-   严格模式下 arguments 有限制，不能修改，不能访问 callee
-   箭头函数没有自己的 arguments，会引用外层函数的 arguments
-   现代开发中应优先使用剩余参数、默认参数和解构
-   了解 arguments 有助于维护老代码和面试准备
