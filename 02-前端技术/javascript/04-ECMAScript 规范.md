# ECMAScript 规范

## 什么是 ECMAScript？

ECMAScript（简称 ES） 是 JavaScript 语言的官方标准规范，定义了语言的语法、类型、语句、关键字、保留字、操作符、对象等核心特性。

### 关键关系图：

```text
ECMAScript（标准规范）
       ↓
JavaScript（具体实现）   ← 由浏览器/Node.js等实现
       ↓
TypeScript           ← ES超集，添加类型系统
       ↓
Babel等工具          ← 将新语法转换为旧版本
```

## ECMAScript 版本演进时间线

| 版本   | 年份 | 代号 | 重大特性                           | 现状         |
| ------ | ---- | ---- | ---------------------------------- | ------------ |
| ES1    | 1997 | -    | 基础语法、类型、对象               | 已淘汰       |
| ES2    | 1998 | -    | 小修订，与 ISO 标准对齐            | 已淘汰       |
| ES3    | 1999 | -    | 正则表达式、异常处理               | 极少使用     |
| ES4    | 放弃 | -    | 激进改革（未发布）                 | -            |
| ES5    | 2009 | ES5  | strict mode、JSON、数组方法        | 广泛支持     |
| ES2015 | 2015 | ES6  | 类、模块、箭头函数、Promise        | 现代 JS 基石 |
| ES2016 | 2016 | ES7  | 指数运算符、Array.includes()       | 成熟         |
| ES2017 | 2017 | ES8  | async/await、Object.values()       | 成熟         |
| ES2018 | 2018 | ES9  | 异步迭代、Rest/Spread 对象         | 成熟         |
| ES2019 | 2019 | ES10 | Array.flat()、Object.fromEntries() | 成熟         |
| ES2020 | 2020 | ES11 | 可选链、空值合并、BigInt           | 广泛支持     |
| ES2021 | 2021 | ES12 | 逻辑赋值、String.replaceAll()      | 广泛支持     |
| ES2022 | 2022 | ES13 | 类字段、顶层 await、.at()方法      | 现代环境支持 |
| ES2023 | 2023 | ES14 | 数组查找方向、Hashbang 语法        | 逐步支持     |
| ES2024 | 2024 | ES15 | 数组分组、RegExp 扩展              | 最新标准     |

## ECMAScript 规范核心结构

### 1. 语言类型系统

```js
// ECMAScript 类型体系
类型分类：
├── 原始类型 (Primitive Types)
│   ├── Undefined
│   ├── Null
│   ├── Boolean
│   ├── Number
│   ├── BigInt          // ES2020新增
│   ├── String
│   └── Symbol          // ES2015新增
│
└── 对象类型 (Object Types)
    ├── Object
    ├── Function
    ├── Array
    ├── Date
    ├── RegExp
    ├── Error
    ├── Map/Set/WeakMap/WeakSet  // ES2015
    ├── Promise                  // ES2015
    ├── Proxy/Reflect            // ES2015
    ├── ArrayBuffer/TypedArray   // ES2015
    └── 其他内置对象...
```

类型转换规则（规范第 7 章定义）：

```js
// 抽象操作（规范内部概念，开发者不可直接调用）
ToString(argument)        // 转换为字符串
ToNumber(argument)        // 转换为数字
ToBoolean(argument)       // 转换为布尔值
ToPrimitive(argument)     // 转换为原始值
ToObject(argument)        // 转换为对象

// 实际转换示例
null == undefined         // true （规范9.1节）
[] == ![]                 // true （诡异但符合规范）
```

### 2. 执行上下文与作用域

```js
// 规范中的执行上下文结构
ExecutionContext = {
  LexicalEnvironment: {     // 词法环境
    EnvironmentRecord: {    // 环境记录
      // 标识符绑定
      [[OuterEnv]]: null | <父环境>  // 作用域链
    }
  },
  VariableEnvironment: { }, // 变量环境（var声明）
  ThisBinding: <值>        // this绑定
}

// 实际代码体现
function outer() {
  var x = 10;              // 进入VariableEnvironment
  let y = 20;              // 进入LexicalEnvironment

  function inner() {
    console.log(x, y);     // 通过作用域链查找
  }

  return inner;
}
```

### 3. 对象模型与原型链

```js
// 规范中的对象内部方法
对象内部槽位 = {
  [[Prototype]]: null | 对象,      // 原型链
  [[Extensible]]: true | false,    // 是否可扩展
  [[Get]](P, Receiver),            // 属性访问
  [[Set]](P, V, Receiver),         // 属性设置
  [[OwnPropertyKeys]]()            // 自有属性键
}

// 原型链查找算法（规范9.1.8.1）
function Get(O, P) {
  // 1. 转换为对象
  // 2. 在对象自身上查找属性
  // 3. 如果未找到，检查原型链
  // 4. 返回找到的值或undefined
}

// 实际原型链
const obj = {};
obj.__proto__ === Object.prototype;      // true
Object.getPrototypeOf(obj) === obj.__proto__; // true
```

## 重要版本特性详解

### ES5（2009）- 现代 JS 基础

```js
// 1. 严格模式
"use strict";
x = 10; // ReferenceError （非严格模式创建全局变量）

// 2. JSON支持
JSON.parse('{"x":1}');
JSON.stringify({ x: 1 });

// 3. 数组方法
[1, 2, 3].forEach(item => console.log(item));
[1, 2, 3].map(x => x * 2);
[1, 2, 3].filter(x => x > 1);
[1, 2, 3].reduce((sum, x) => sum + x, 0);

// 4. 属性描述符
Object.defineProperty(obj, "key", {
    value: "static",
    writable: false, // 不可写
    enumerable: false, // 不可枚举
    configurable: false, // 不可配置
});
```

### ES2015（ES6）- 革命性更新

```js
// 1. 块级作用域
{
    let x = 1; // 块级作用域
    const y = 2; // 常量
}
// x, y 不可访问

// 2. 箭头函数
const add = (a, b) => a + b;
const obj = {
    value: 10,
    getValue: () => this.value, // this指向外层
    getValue2() {
        return this.value;
    }, // 传统方法
};

// 3. 类语法
class Person {
    #privateField = "secret"; // 私有字段（ES2022正式化）

    constructor(name) {
        this.name = name;
    }

    greet() {
        return `Hello, ${this.name}`;
    }

    static create(name) {
        return new Person(name);
    }
}

class Student extends Person {
    constructor(name, grade) {
        super(name);
        this.grade = grade;
    }
}

// 4. 模块系统
// math.js
export const PI = 3.14159;
export function square(x) {
    return x * x;
}
export default class Calculator {}

// app.js
import Calculator, { PI, square } from "./math.js";

// 5. Promise
const fetchData = () =>
    new Promise((resolve, reject) => {
        setTimeout(() => resolve("data"), 1000);
    });

fetchData()
    .then(data => console.log(data))
    .catch(error => console.error(error));

// 6. 解构赋值
const [a, b] = [1, 2];
const { x, y } = { x: 1, y: 2 };
const { z = 3 } = {}; // 默认值

// 7. 模板字符串
const name = "Alice";
const greeting = `Hello, ${name}!
This is a multi-line string.`;

// 8. Symbol
const sym = Symbol("unique");
const obj = { [sym]: "value" };

// 9. 迭代器与生成器
function* idGenerator() {
    let id = 0;
    while (true) {
        yield id++;
    }
}
const gen = idGenerator();
gen.next().value; // 0
```

### ES2017 - async/await

```js
// 异步函数（语法糖，基于Promise）
async function fetchUser(id) {
    try {
        const response = await fetch(`/api/users/${id}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Fetch failed:", error);
        throw error;
    }
}

// 并行请求
async function fetchAll() {
    const [user, posts] = await Promise.all([fetchUser(1), fetchPosts(1)]);
    return { user, posts };
}

// 规范中的异步执行顺序
async function example() {
    console.log(1);
    await Promise.resolve();
    console.log(2);
    // 微任务队列插入点
}
console.log(3);
example();
console.log(4);
// 输出: 3, 1, 4, 2
```

### ES2020+ 重要特性

```js
// 1. 可选链操作符
const street = user?.address?.street;
const result = obj.method?.();

// 2. 空值合并运算符
const value = input ?? "default"; // 仅当null/undefined时用默认值

// 3. BigInt
const big = 9007199254740991n; // 超过Number.MAX_SAFE_INTEGER
const bigger = big + 1n;

// 4. 全局对象统一
// 浏览器: window, Node.js: global, 统一访问:
globalThis.setTimeout(() => {}, 1000);

// 5. Promise.allSettled
const promises = [Promise.resolve(1), Promise.reject("error")];
Promise.allSettled(promises).then(results => {
    // [{status: "fulfilled", value: 1}, {status: "rejected", reason: "error"}]
});

// 6. 动态导入
const module = await import("./module.js");
if (condition) {
    const utils = await import("./utils.js");
}

// 7. 私有类字段（ES2022正式化）
class Counter {
    #count = 0; // 真正的私有

    increment() {
        this.#count++;
    }

    getCount() {
        return this.#count;
    }
}

// 8. 顶层await（ES2022）
// 模块中可以直接使用await
const data = await fetchData();
export { data };
```

## ECMAScript 标准制定流程

### TC39 提案阶段

```text
阶段0: Strawman（草案） → 阶段1: Proposal（提案）
       ↓                           ↓
阶段2: Draft（草案规范） → 阶段3: Candidate（候选）
       ↓                           ↓
阶段4: Finished（完成）  → 纳入下一版ECMAScript
```

### 实际提案示例：装饰器

```js
// 阶段3提案（2024年更新）
// 旧语法（已废弃）
@decorator
class MyClass {}

// 新语法提案
class MyClass {
    @decorator accessor myField = 1;

    @decorator
    myMethod() {}
}

// 装饰器实现示例
function logged(target, context) {
    return function (...args) {
        console.log(`调用 ${context.name}`, args);
        return target.call(this, ...args);
    };
}

class Calculator {
    @logged
    add(a, b) {
        return a + b;
    }
}
```

## 浏览器/引擎实现差异

### 1. JavaScript 引擎对照表

| 引擎            | 浏览器/环境           | ECMAScript 兼容性    |
| --------------- | --------------------- | -------------------- |
| V8              | Chrome, Node.js, Edge | 最新特性支持最好     |
| SpiderMonkey    | Firefox               | 紧跟标准，实现质量高 |
| JavaScriptCore  | Safari                | 较保守，但符合标准   |
| Chakra (已弃用) | 旧版 Edge             | 已被 V8 取代         |

### 2. 兼容性检查代码

```js
// 特性检测（而非浏览器检测）
function supportsES2020() {
    try {
        // 检查可选链
        eval("const obj = {}; obj?.property");

        // 检查空值合并
        eval('null ?? "default"');

        // 检查Promise.allSettled
        if (!Promise.allSettled) return false;

        // 检查BigInt
        if (typeof BigInt === "undefined") return false;

        return true;
    } catch {
        return false;
    }
}

// 使用polyfill策略
if (typeof Promise.allSettled === "undefined") {
    Promise.allSettled = function (promises) {
        return Promise.all(
            promises.map(p =>
                p.then(
                    value => ({ status: "fulfilled", value }),
                    reason => ({ status: "rejected", reason })
                )
            )
        );
    };
}
```

## Babel 编译示例

```js
// 源代码（ES2022+）
class User {
    #password = "secret";

    static async create(data) {
        const user = new User();
        await user.#validate(data);
        return user;
    }

    async #validate(data) {
        // 私有方法
    }
}

const name = user?.profile?.name ?? "Anonymous";

// Babel转译后（ES5兼容）
("use strict");

function _classPrivateFieldInitSpec(obj, privateMap, value) {
    // 私有字段polyfill
}

function _checkPrivateRedeclaration(obj, privateCollection) {
    // 私有成员检查
}

var User = /*#__PURE__*/ (function () {
    function User() {
        _classPrivateFieldInitSpec(this, _password, {
            writable: true,
            value: "secret",
        });
    }

    User.create = function create(data) {
        return Promise.resolve().then(function () {
            var user = new User();
            return _validate.call(user, data).then(function () {
                return user;
            });
        });
    };

    var _password = new WeakMap();

    var _validate = /*#__PURE__*/ (function () {
        function _validate(data) {
            return Promise.resolve();
        }
        return _validate;
    })();

    return User;
})();

var name =
    (user == null ? void 0 : user.profile == null ? void 0 : user.profile.name) ?? "Anonymous";
```

## 学习与实践建议

### 1. 学习路径

初学者：ES5 基础 → ES6 核心 → 现代特性 <br>
进阶者：阅读 ES 规范 → 理解引擎实现 → 性能优化 <br>
专家级：参与 TC39 提案 → 开发 Babel 插件 → 引擎开发 <br>

### 2. 生产环境策略

```js
// package.json配置示例
{
  "browserslist": [
    "> 1%",            // 全球使用率>1%的浏览器
    "last 2 versions", // 最近两个版本
    "not dead"         // 未废弃的浏览器
  ],
  "devDependencies": {
    "@babel/core": "^7.0.0",
    "@babel/preset-env": "^7.0.0", // 智能polyfill
    "core-js": "^3.0.0"            // 标准库polyfill
  }
}

// .babelrc配置
{
  "presets": [
    ["@babel/preset-env", {
      "useBuiltIns": "usage",  // 按需引入polyfill
      "corejs": 3,
      "targets": {
        "chrome": "58",
        "ie": "11"             // 明确IE支持
      }
    }]
  ]
}
```

### 3. 资源推荐

-   规范文档: [ECMA-262 标准](https://tc39.es/ecma262)
-   提案状态: [TC39 GitHub](https://github.com/tc39/proposals)
-   兼容性表: [Can I Use](https://caniuse.com)
-   测试工具: [ES6 兼容性表](https://kangax.github.io)
-   学习资源: [MDN JavaScript](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript)
