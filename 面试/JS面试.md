# JS面试

## 目录

1. 变量与作用域
var、let、const 的区别：
    var：函数作用域，存在变量提升。
    let 和 const：块级作用域，不存在变量提升，const 用于声明常量。

作用域链：理解全局作用域、函数作用域和块级作用域。

闭包：函数与其词法环境的结合，常见用途（如数据封装、柯里化）。

2. 数据类型
基本类型：string、number、boolean、null、undefined、symbol、bigint。

引用类型：object、array、function。

类型检测：
    typeof：检测基本类型。
    instanceof：检测引用类型。
    Object.prototype.toString.call()：精确检测类型。

3. 原型与继承
原型链：每个对象都有一个 __proto__ 属性指向其原型对象。

构造函数与 prototype：构造函数通过 prototype 共享方法和属性。

继承方式：
    原型链继承。
    构造函数继承。
    组合继承。
    寄生组合继承（最优）。

4. 异步编程
回调函数：简单但容易导致回调地狱。

Promise：
    三种状态：pending、fulfilled、rejected。
    方法：then、catch、finally。
    Promise.all、Promise.race。

Async/Await：基于 Promise 的语法糖，使异步代码更易读。

5. 事件循环（Event Loop）
宏任务与微任务：
    宏任务：setTimeout、setInterval、I/O。
    微任务：Promise.then、MutationObserver。
    执行顺序：同步代码 → 微任务 → 宏任务。

二、进阶概念
1. ES6+ 新特性
    箭头函数：() => {}，没有自己的 this，继承外层 this。
    解构赋值：const { a, b } = obj。
    模板字符串：`Hello, ${name}`。
    模块化：import 和 export。
    默认参数：function(a = 1, b = 2) {}。
    展开运算符：...。

2. 函数式编程
    纯函数：相同的输入总是得到相同的输出，无副作用。
    高阶函数：接收函数作为参数或返回函数。
    柯里化：将多参数函数转换为单参数函数链。

3. 性能优化
防抖与节流：
    防抖：多次触发只执行最后一次。
    节流：一段时间内只执行一次。
垃圾回收：标记清除、引用计数。
内存泄漏：常见原因（如未清除的定时器、闭包）。

三、常见面试题
1. 基础题
null 和 undefined 的区别：
    null 表示空值，undefined 表示未定义。

== 和 === 的区别：
    == 会进行类型转换，=== 不会。

如何判断数组：
    Array.isArray(arr) 或 Object.prototype.toString.call(arr) === '[object Array]'。

2. 进阶题
实现一个 Promise：
    包含 resolve、reject、then 方法。

手写防抖和节流：
    防抖：debounce(fn, delay)。
    节流：throttle(fn, delay)。

实现深拷贝：
    递归遍历对象，处理基本类型和引用类型。

3. 算法题
数组去重：
    使用 Set 或 filter 实现。

两数之和：
    使用哈希表优化查找。

反转链表：
    迭代或递归实现。


## 浏览器输入链接，点击回车到页面展示，中间都发生了什么？

1. URL 解析
输入处理：
    浏览器会检查输入的内容是否是有效的 URL。
    如果不是 URL，浏览器会将其作为搜索查询，跳转到默认搜索引擎。

解析 URL：
    浏览器解析 URL 的协议（如 http、https）、域名、端口、路径和查询参数。

2. DNS 查询
查找域名对应的 IP 地址：
    浏览器检查本地缓存（如浏览器缓存、操作系统缓存）是否有该域名的 IP 地址。
    如果缓存中没有，浏览器会向 DNS 服务器发送查询请求，递归查找域名对应的 IP 地址。

DNS 解析过程：
    本地 DNS 缓存。
    向根域名服务器查询。
    向顶级域名服务器（如 .com）查询。
    向权威域名服务器查询。

3. 建立 TCP 连接
三次握手：
    浏览器通过 IP 地址和端口号与服务器建立 TCP 连接。

三次握手过程：
    客户端发送 SYN 包。
    服务器回复 SYN-ACK 包。
    客户端发送 ACK 包，连接建立。

4. 发送 HTTP 请求
构建请求：
    浏览器构建 HTTP 请求报文，包括请求行（如 GET /index.html HTTP/1.1）、请求头（如 User-Agent、Accept）和请求体（如 POST 请求的数据）。

发送请求：
    通过 TCP 连接将请求发送到服务器。

5. 服务器处理请求
接收请求：
    服务器接收请求并解析。

处理请求：
    根据请求路径和参数，服务器执行相应的逻辑（如读取文件、查询数据库）。

生成响应：
    服务器生成 HTTP 响应报文，包括状态行（如 HTTP/1.1 200 OK）、响应头（如 Content-Type、Content-Length）和响应体（如 HTML 内容）。

6. 接收 HTTP 响应
接收数据：
    浏览器接收服务器返回的 HTTP 响应。

解析响应：
    浏览器根据响应头中的 Content-Type 判断响应内容的类型（如 text/html、application/json）。

7. 渲染页面
1. 解析 HTML
构建 DOM 树：
    浏览器解析 HTML 文件，构建 DOM（文档对象模型）树。

遇到外部资源：
    如果 HTML 中包含外部资源（如 CSS、JS、图片），浏览器会发起额外的请求来加载这些资源。

2. 解析 CSS
构建 CSSOM 树：
    浏览器解析 CSS 文件，构建 CSSOM（CSS 对象模型）树。

3. 构建渲染树
合并 DOM 和 CSSOM：
    浏览器将 DOM 树和 CSSOM 树合并为渲染树（Render Tree）。

4. 布局（Layout）
计算布局：
    浏览器计算渲染树中每个节点的几何信息（如位置、大小）。

5. 绘制（Paint）
绘制页面：
    浏览器将渲染树中的节点绘制到屏幕上。

6. 合成（Composite）
图层合成：
    浏览器将多个图层合成为最终的页面图像。

8. 执行 JavaScript
解析和执行 JS：
    如果页面中包含 JavaScript 代码，浏览器会解析并执行。

事件驱动：
    JavaScript 可以监听用户交互事件（如点击、滚动），并动态更新页面内容。

9. 页面加载完成
触发 DOMContentLoaded 事件：
    当 HTML 文档完全加载和解析完成时触发。

触发 load 事件：
    当页面所有资源（如图片、样式表）加载完成后触发。

## 谈谈你对原型链的理解

1. 原型链的基本概念
1.1 原型（Prototype）
    每个 JavaScript 对象（除 null 外）都有一个内部属性 [[Prototype]]（在代码中可以通过 __proto__ 访问），指向它的原型对象。
    原型对象也是一个普通对象，它也有自己的原型，形成一条链式结构，这就是 原型链。

1.2 构造函数（Constructor）
    构造函数是用来创建对象的函数。通过 new 关键字调用构造函数时，会创建一个新对象，并将该对象的 [[Prototype]] 指向构造函数的 prototype 属性。
    构造函数的 prototype 属性是一个对象，包含共享的属性和方法。

1.3 原型链的作用
    当访问一个对象的属性或方法时，如果对象本身没有该属性或方法，JavaScript 会沿着原型链向上查找，直到找到该属性或方法，或者到达原型链的顶端（null）。

2. 原型链的组成
2.1 对象的原型链
    每个对象都有一个 __proto__ 属性，指向它的原型对象。
    原型对象也有自己的 __proto__，形成一条链，直到 Object.prototype，其 __proto__ 为 null。

2.2 构造函数的原型
    构造函数的 prototype 属性指向一个对象，该对象是实例化对象的原型。
```javascript
function Person() {}
const person = new Person();
console.log(person.__proto__ === Person.prototype); // true
```

2.3 原型链的顶端
    所有对象的原型链最终都会指向 Object.prototype，而 Object.prototype 的 __proto__ 为 null。
```javascript
console.log(Person.prototype.__proto__ === Object.prototype); // true
console.log(Object.prototype.__proto__); // null
```

3. 原型链的查找机制
当访问一个对象的属性或方法时，JavaScript 会按照以下顺序查找：
    对象本身。
    对象的原型（__proto__）。
    原型的原型（__proto__.__proto__）。
    直到找到属性或方法，或者到达 null（未找到）。

```javascript
function Person(name) {
  this.name = name;
}

Person.prototype.sayHello = function() {
  console.log(`Hello, ${this.name}`);
};

const person = new Person('Alice');

console.log(person.name); // Alice（来自对象本身）
person.sayHello(); // Hello, Alice（来自原型）
console.log(person.toString()); // [object Object]（来自 Object.prototype）
```

4. 原型链与继承
4.1 原型链继承
通过将子类的原型指向父类的实例，实现继承。

```javascript
function Parent() {
  this.name = 'Parent';
}
Parent.prototype.sayHello = function() {
  console.log(`Hello, ${this.name}`);
};

function Child() {
  this.name = 'Child';
}
Child.prototype = new Parent(); // 继承

const child = new Child();
child.sayHello(); // Hello, Child
```

4.2 构造函数继承
在子类构造函数中调用父类构造函数，继承父类的实例属性。

```javascript
function Parent(name) {
  this.name = name;
}

function Child(name) {
  Parent.call(this, name); // 继承实例属性
}

const child = new Child('Child');
console.log(child.name); // Child
```

4.3 组合继承
结合原型链继承和构造函数继承，解决原型链继承中引用属性共享的问题。

```javascript
function Parent(name) {
  this.name = name;
}
Parent.prototype.sayHello = function() {
  console.log(`Hello, ${this.name}`);
};

function Child(name) {
  Parent.call(this, name); // 继承实例属性
}
Child.prototype = new Parent(); // 继承原型方法

const child = new Child('Child');
child.sayHello(); // Hello, Child
```

4.4 寄生组合继承（最优）
通过 Object.create 实现原型链继承，避免调用父类构造函数。

```javascript
function Parent(name) {
  this.name = name;
}
Parent.prototype.sayHello = function() {
  console.log(`Hello, ${this.name}`);
};

function Child(name) {
  Parent.call(this, name); // 继承实例属性
}
Child.prototype = Object.create(Parent.prototype); // 继承原型方法
Child.prototype.constructor = Child; // 修复构造函数指向

const child = new Child('Child');
child.sayHello(); // Hello, Child
```

5. 原型链的应用场景
    共享方法：将方法定义在原型上，所有实例共享，节省内存。
    实现继承：通过原型链实现对象之间的继承关系。
    扩展内置对象：通过修改原型，扩展内置对象的功能（如为 Array 添加新方法）。

6. 原型链的注意事项
    性能问题：过长的原型链会增加属性查找时间。
    共享引用属性：如果原型对象包含引用类型属性，所有实例会共享该属性。
    修改原型：动态修改原型会影响所有实例。


## 谈谈你对闭包的理解

1. 闭包的定义
闭包是指一个函数能够记住并访问它的词法作用域，即使这个函数在其词法作用域之外执行。

```javascript
function outer() {
  const name = 'Alice';
  function inner() {
    console.log(name); // 访问外部函数的变量
  }
  return inner;
}

const innerFunc = outer();
innerFunc(); // 输出: Alice
```

inner 函数形成了闭包，它可以访问 outer 函数的变量 name，即使 outer 函数已经执行完毕。

2. 闭包的形成条件
    函数嵌套：一个函数内部定义了另一个函数。
    内部函数引用外部函数的变量：内部函数使用了外部函数的变量。
    内部函数在外部函数之外被调用：内部函数在其词法作用域之外执行。


3. 闭包的作用
3.1 数据封装
闭包可以创建私有变量，避免全局污染。

```javascript
function createCounter() {
  let count = 0;
  return function() {
    count++;
    console.log(count);
  };
}

const counter = createCounter();
counter(); // 输出: 1
counter(); // 输出: 2
```
count 变量被封装在闭包中，外部无法直接访问。

3.2 函数柯里化
柯里化是将多参数函数转换为单参数函数链的过程，闭包可以用于实现柯里化。

```javascript
function add(a) {
  return function(b) {
    return a + b;
  };
}

const add5 = add(5);
console.log(add5(3)); // 输出: 8
```

3.3 回调函数
闭包常用于回调函数中，保留上下文信息。

```javascript
setTimeout(function() {
  console.log('Hello after 1 second');
}, 1000);
```

4. 闭包与内存管理
4.1 内存泄漏
闭包会导致外部函数的变量无法被垃圾回收，从而可能引发内存泄漏。

```javascript
function createHeavyClosure() {
  const largeArray = new Array(1000000).fill('data');
  return function() {
    console.log(largeArray.length);
  };
}

const heavyFunc = createHeavyClosure();
// largeArray 无法被回收，即使 heavyFunc 不再使用
```

4.2 解决方法
在不需要闭包时，手动解除引用。

```javascript
heavyFunc = null; // 解除引用，允许垃圾回收
```

5. 闭包的应用场景
5.1 模块化
使用闭包实现模块化，隐藏内部实现细节。

```javascript
const module = (function() {
  const privateVar = '私有变量';
  function privateMethod() {
    console.log(privateVar);
  }
  return {
    publicMethod: function() {
      privateMethod();
    }
  };
})();

module.publicMethod(); // 输出: 私有变量
```

5.2 延迟执行
使用闭包实现延迟执行函数。

```javascript
function delay(message, time) {
  return function() {
    setTimeout(function() {
      console.log(message);
    }, time);
  };
}

const delayedHello = delay('Hello after 2 seconds', 2000);
delayedHello();
```

5.3 缓存
使用闭包实现缓存功能。

```javascript
function createCache() {
  const cache = {};
  return function(key, value) {
    if (value !== undefined) {
      cache[key] = value;
    }
    return cache[key];
  };
}

const cacheFunc = createCache();
cacheFunc('name', 'Alice');
console.log(cacheFunc('name')); // 输出: Alice
```

6. 闭包的注意事项
性能问题：
> 闭包会保留外部函数的变量，可能导致内存占用过高。

变量共享：
> 多个闭包共享同一个外部函数的变量时，可能会产生意外的行为。

```javascript
for (var i = 1; i <= 3; i++) {
  setTimeout(function() {
    console.log(i); // 输出: 4, 4, 4
  }, 1000);
}
```
解决方法：使用 let 或立即执行函数（IIFE）。

```javascript
for (let i = 1; i <= 3; i++) {
  setTimeout(function() {
    console.log(i); // 输出: 1, 2, 3
  }, 1000);
}
```

## 事件循环（Event Loop）
```js
new Promise((resolve, reject) => {resolve()}).then(() => {
    console.log('a')
    setTimeout(() => {
        console.log('b')
    });
});
setTimeout(() => {
    console.log('c')
    new Promise(() => {
        console.log('d')
    });
});
new Promise(() => console.log('e'))
```

e、a、c、d、b

解析：
1. new Promise(() => console.log('e')):
> Promise 构造函数，console.log('e') 会立即执行，因此 e 是第一个输出。

2. new Promise((resolve, reject) => { resolve() }):
> 这个 Promise 会立即 resolve，因此它的 .then() 回调会被放入微任务队列，等待当前同步代码执行完毕后执行。
> 在 .then() 回调中，console.log('a') 会立即执行，输出 a。
> 接着，setTimeout(() => { console.log('b') }) 会被放入宏任务队列，等待执行。

3. setTimeout(() => { console.log('c') ... }):
> 这个 setTimeout 会被放入宏任务队列，等待执行。
> 当它执行时，console.log('c') 会输出 c。
> 接着，new Promise(() => { console.log('d') }) 会立即执行，输出 d。

4. setTimeout(() => { console.log('b') }):
> 这个 setTimeout 是在 .then() 回调中被放入宏任务队列的，因此它会在当前宏任务执行完毕后执行。
> 当它执行时，console.log('b') 会输出 b。

执行顺序总结：
1. 同步代码：
e（立即输出）。

2. 微任务队列：
a（.then() 回调执行）。

3. 宏任务队列：
c 和 d（第一个 setTimeout 执行）。
b（第二个 setTimeout 执行）。


总结：
微任务：优先级高，会在当前同步代码执行完毕后立即执行，且会一次性执行完所有微任务。
宏任务：优先级低，每次事件循环只执行一个宏任务，然后检查微任务队列。
事件循环：同步代码 → 微任务队列 → 宏任务队列

常见的微任务：
> Promise.then()、Promise.catch()、Promise.finally() 的回调。
> MutationObserver 的回调。
> queueMicrotask() 添加的任务。

常见的宏任务：
> setTimeout、setInterval 的回调。
> setImmediate（Node.js 环境）。
> requestAnimationFrame（浏览器环境）。
> I/O 操作（如文件读取、网络请求等）。
> UI 渲染（浏览器环境）。

## 重绘与重排

1. 重绘（Repaint）
定义：当元素的外观发生变化（如颜色、背景、边框等），但不影响布局时，浏览器会重新绘制元素。

触发条件：
    修改颜色（color、background-color 等）。
    修改边框样式（border-style、border-color 等）。
    修改可见性（visibility）。
    修改阴影（box-shadow）。

性能影响：重绘的性能开销比重排小，但仍需避免频繁触发。

2. 重排（Reflow）
定义：当元素的几何属性发生变化（如尺寸、位置、布局等），浏览器需要重新计算布局并重新绘制页面。

触发条件：
    修改元素的尺寸（width、height、padding、margin 等）。
    添加或删除 DOM 元素。
    修改页面内容（如文字变化）。
    修改窗口大小（resize 事件）。
    获取某些布局属性（如 offsetTop、offsetWidth 等），因为浏览器需要重新计算布局。

性能影响：重排的性能开销较大，因为它会导致整个或部分页面重新布局。

3. 重绘与重排的关系
    重排一定会触发重绘，因为布局变化后需要重新绘制。
    重绘不一定触发重排，因为外观变化不一定影响布局。

4. 如何优化重绘与重排
减少重排：
    避免频繁操作 DOM，尽量一次性修改。
    使用 DocumentFragment 或离线 DOM（display: none）进行批量操作。
    使用 CSS transform 和 opacity 实现动画，因为它们不会触发重排。
    避免在循环中读取布局属性（如 offsetTop），因为这会强制触发重排。
    使用 flexbox 或 grid 布局，它们的性能优于传统布局。

减少重绘：
    避免频繁修改样式，尽量通过修改类名来批量更新样式。
    使用 will-change 属性提示浏览器优化某些元素。
    使用 requestAnimationFrame 优化动画，避免不必要的重绘。

## var、let、const 的区别

1. 作用域
1.1 var
    函数作用域：var 声明的变量在函数内部有效。
    如果在函数外声明，则为全局变量。

1.2 let
    块级作用域：let 声明的变量在块（如 {}）内部有效。

1.3 const
    块级作用域：与 let 相同，const 声明的变量在块内部有效。

2. 变量提升
2.1 var
    会提升：var 声明的变量会被提升到函数或全局作用域的顶部，但赋值不会提升。

2.2 let 和 const
    不会提升：let 和 const 声明的变量不会被提升，存在“暂时性死区”（Temporal Dead Zone, TDZ）。

3. 重复声明
3.1 var
    允许重复声明：可以多次声明同一个变量。

3.2 let 和 const
    不允许重复声明：在同一作用域内，不能重复声明同一个变量。

4. 可变性
4.1 var 和 let
    可变：可以重新赋值。

4.2 const
    不可变：声明时必须初始化，且不能重新赋值。
    注意：如果 const 声明的是对象或数组，对象或数组内部的属性或元素可以修改。

5. 全局作用域下的行为
5.1 var
    在全局作用域下声明时，会成为全局对象（如 window）的属性。

5.2 let 和 const
    在全局作用域下声明时，不会成为全局对象的属性。

## 作用域链：理解全局作用域、函数作用域和块级作用域。

1. 作用域（Scope）
作用域是指变量和函数的可访问范围。JavaScript 中有三种主要的作用域：
    全局作用域。
    函数作用域。
    块级作用域。

2. 全局作用域
定义：
    全局作用域是 JavaScript 中最外层的作用域。
    在全局作用域中声明的变量和函数可以在代码的任何地方访问。

特点：
    全局变量会挂载到全局对象（如浏览器中的 window 对象）上。
    过多的全局变量可能导致命名冲突和代码污染。

3. 函数作用域
定义：
    函数作用域是指在函数内部声明的变量和函数，只能在函数内部访问。
    使用 var 声明的变量具有函数作用域。

特点：
    函数作用域内的变量在函数外部不可访问。
    函数作用域可以嵌套，形成作用域链。

4. 块级作用域
定义：
    块级作用域是指在 {} 块内部声明的变量，只能在块内部访问。
    使用 let 和 const 声明的变量具有块级作用域。

特点：
    块级作用域内的变量在块外部不可访问。
    块级作用域可以避免变量污染和意外覆盖。

5. 作用域链
定义：
    作用域链是指 JavaScript 在查找变量时，从当前作用域开始，逐级向上查找，直到全局作用域的过程。
    作用域链的形成是基于函数的嵌套关系。

特点：
    内部作用域可以访问外部作用域的变量，但外部作用域不能访问内部作用域的变量。
    作用域链的顶端是全局作用域。

6. 作用域链的查找过程
当访问一个变量时，JavaScript 会按照以下顺序查找：
    当前作用域：查找当前函数或块内部是否有该变量。
    外部作用域：如果当前作用域没有，则向上一层作用域查找。
    全局作用域：如果所有外部作用域都没有，则查找全局作用域。
    未找到：如果全局作用域也没有，则抛出 ReferenceError。

7. 作用域链与闭包
    闭包 是函数与其词法作用域的结合。
    闭包可以访问其外部函数的变量，即使外部函数已经执行完毕。
```js
function outer() {
  var outerVar = '外部变量';
  return function inner() {
    console.log(outerVar);
  };
}

const innerFunc = outer();
innerFunc(); // 输出: 外部变量
```

## 数据类型

1. 基本类型：string、number、boolean、null、undefined、symbol、bigint。
    string: 文本
    number: 整数或浮点数
    boolean: 表示逻辑值，true 或 false
    null: 表示一个空值或不存在的对象。
    undefined: 表示变量已声明但未赋值。
    symbol: 表示唯一的、不可变的值，通常用于对象属性的键。
    bigint: 表示任意精度的整数。

2. 引用类型：object、array、function。
    object: 表示键值对的集合
    array: 表示有序的元素集合
    function: 表示可执行的代码块

3. 基本类型与引用类型的区别

3.1 存储方式
    基本类型：值直接存储在栈内存中。
    引用类型：值存储在堆内存中，栈内存中存储的是堆内存地址的引用。

3.2 赋值行为
    基本类型：赋值是值的拷贝。
    引用类型：赋值是引用的拷贝（指向同一个对象）。

3.3 比较方式
    基本类型：比较的是值。
    引用类型：比较的是引用（内存地址）。

3.4 可变性
    基本类型：不可变（值不能被修改）。
    引用类型：可变（对象属性可以被修改）。

```js
// 基本类型
let str = 'hello';
str[0] = 'H'; // 无效
console.log(str); // hello

// 引用类型
let obj = { name: 'Alice' };
obj.name = 'Bob';
console.log(obj.name); // Bob
```

4. 类型检测
4.1 typeof
    用于检测基本类型（除 null 外）和函数。
```js
console.log(typeof 'hello'); // string
console.log(typeof 42); // number
console.log(typeof true); // boolean
console.log(typeof undefined); // undefined
console.log(typeof Symbol('id')); // symbol
console.log(typeof 123n); // bigint
console.log(typeof null); // object（历史遗留问题）
console.log(typeof {}); // object
console.log(typeof []); // object
console.log(typeof function() {}); // function
```

4.2 instanceof
用于检测引用类型（对象、数组、函数等）。
```js
console.log([] instanceof Array); // true
console.log({} instanceof Object); // true
console.log(function() {} instanceof Function); // true
```

4.3 Object.prototype.toString.call()
精确检测数据类型。
```js
console.log(Object.prototype.toString.call('hello')); // [object String]
console.log(Object.prototype.toString.call(42)); // [object Number]
console.log(Object.prototype.toString.call(true)); // [object Boolean]
console.log(Object.prototype.toString.call(null)); // [object Null]
console.log(Object.prototype.toString.call(undefined)); // [object Undefined]
console.log(Object.prototype.toString.call(Symbol('id'))); // [object Symbol]
console.log(Object.prototype.toString.call(123n)); // [object BigInt]
console.log(Object.prototype.toString.call({})); // [object Object]
console.log(Object.prototype.toString.call([])); // [object Array]
console.log(Object.prototype.toString.call(function() {})); // [object Function]
```

## 异步编程

异步编程的必要性
    单线程模型：JavaScript 是单线程的，同一时间只能执行一个任务。
    耗时操作：如果同步执行耗时操作（如网络请求），会导致页面卡顿或无响应。
    异步机制：通过异步编程，可以将耗时操作放到后台执行，主线程继续处理其他任务。

1. 回调函数：简单但容易导致回调地狱。

定义：
    将函数作为参数传递给另一个函数，在异步操作完成后调用。
缺点：
    回调地狱（Callback Hell）：多层嵌套回调导致代码难以维护。
    错误处理困难：需要手动处理错误。

2 Promise
定义：
    Promise 是一个表示异步操作最终完成或失败的对象。

状态：
    pending：初始状态。
    fulfilled：操作成功完成。
    rejected：操作失败。

方法：
    then：处理成功状态。
    catch：处理失败状态。
    finally：无论成功或失败都会执行。
```js
function fetchData() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const data = 'Hello, World!';
      resolve(data);
    }, 1000);
  });
}

fetchData()
  .then((data) => {
    console.log(data); // 1秒后输出: Hello, World!
  })
  .catch((error) => {
    console.error(error);
  });
```

优点：
    链式调用，避免回调地狱。
    更好的错误处理机制。

3 Async/Await
定义：async/await 是基于 Promise 的语法糖，使异步代码看起来像同步代码。
用法：
    async：声明一个异步函数。
    await：等待 Promise 完成，并返回结果。

优点：
    代码更简洁，易于阅读。
    错误处理更直观。

4. 常见的异步操作
    setTimeout：延迟执行。
    setInterval：周期性执行。
    使用 fetch 或 XMLHttpRequest 发起网络请求。
    使用 fs 模块进行文件操作。

5. 异步编程的最佳实践

避免回调地狱：
    使用 Promise 或 async/await 替代嵌套回调。

错误处理：
    使用 try/catch 或 .catch() 捕获异步错误。

并发控制：
    使用 Promise.all 处理多个异步任务。
```js
async function fetchAllData() {
  const [data1, data2] = await Promise.all([fetchData1(), fetchData2()]);
  console.log(data1, data2);
}
```

性能优化：
    避免不必要的异步操作。
    使用缓存减少重复请求。

## ES6+ 新特性
箭头函数：() => {}，没有自己的 this，继承外层 this。
解构赋值：const { a, b } = obj。
模板字符串：`Hello, ${name}`。
模块化：import 和 export。
默认参数：function(a = 1, b = 2) {}。
展开运算符：...。


## 箭头函数

箭头函数使用 => 符号定义，语法比普通函数更简洁。


1. 箭头函数的特点

1.1 箭头函数没有自己的 this，它会捕获其所在上下文的 this 值。
```js
const obj = {
  name: 'Alice',
  greet: function() {
    setTimeout(() => {
      console.log(`Hello, ${this.name}`);
    }, 1000);
  }
};

obj.greet(); // 1秒后输出: Hello, Alice
```
> 普通函数中的 this 指向 setTimeout 的调用者（通常是 window），而箭头函数中的 this 指向 obj。

1.2 没有 arguments 对象
箭头函数没有自己的 arguments 对象，它会捕获其所在上下文的 arguments。
```js
const showArgs = () => {
  console.log(arguments); // 报错: arguments 未定义
};

function regularFunction() {
  const showArgs = () => {
    console.log(arguments); // 捕获外部函数的 arguments
  };
  showArgs();
}

regularFunction(1, 2, 3); // 输出: [1, 2, 3]
```

1.3 不能作为构造函数
箭头函数不能使用 new 关键字调用，因为它没有 [[Construct]] 内部方法。

```js
const Person = () => {};
const p = new Person(); // 报错: Person is not a constructor
```

1.4 没有 prototype 属性
箭头函数没有 prototype 属性，因此不能用于定义类或构造函数。

```js
const Person = () => {};
console.log(Person.prototype); // undefined
```

3. 箭头函数的适用场景

3.1 简化回调函数
箭头函数非常适合用于简化回调函数。

```js
const numbers = [1, 2, 3, 4, 5];
const squares = numbers.map(x => x * x);
console.log(squares); // [1, 4, 9, 16, 25]
```

3.2 绑定上下文
当需要保留外部上下文的 this 时，箭头函数非常有用。

```js
const obj = {
  name: 'Alice',
  greet: function() {
    setTimeout(() => {
      console.log(`Hello, ${this.name}`);
    }, 1000);
  }
};

obj.greet(); // 1秒后输出: Hello, Alice
```

3.3 函数式编程
箭头函数简洁的语法非常适合函数式编程风格。

```js
const add = (a, b) => a + b;
const multiply = (a, b) => a * b;
const result = multiply(add(2, 3), 4); // 20
```

4. 箭头函数的注意事项
4.1 不适合定义对象方法：

如果对象方法需要使用 this，普通函数更合适。

```js
const obj = {
  name: 'Alice',
  greet: () => {
    console.log(`Hello, ${this.name}`); // this 指向全局对象
  }
};

obj.greet(); // 输出: Hello, undefined
```

4.2 不适合定义原型方法：

箭头函数没有 prototype，不能用于定义原型方法。

```js
function Person(name) {
  this.name = name;
}

Person.prototype.greet = () => {
  console.log(`Hello, ${this.name}`); // this 指向全局对象
};

const p = new Person('Alice');
p.greet(); // 输出: Hello, undefined
```

4.3 不适合动态上下文：

如果函数需要动态绑定 this（如事件处理函数），普通函数更合适。

```js
const button = document.querySelector('button');
button.addEventListener('click', () => {
  console.log(this); // this 指向全局对象
});

button.addEventListener('click', function() {
  console.log(this); // this 指向 button 元素
});
```

## 函数式编程

1. 函数式编程的核心概念
1.1 纯函数（Pure Function）
定义：纯函数是指相同的输入始终得到相同的输出，且没有副作用（如修改外部状态、I/O 操作等）。
特点：
    不依赖外部状态。
    不修改外部状态。

```js
// 纯函数
function add(a, b) {
  return a + b;
}

// 非纯函数（依赖外部状态）
let count = 0;
function increment() {
  return ++count;
}
```

1.2 不可变数据（Immutable Data）
定义：数据一旦创建就不能被修改，任何修改都会生成一个新的数据。
优点：
    避免意外的数据修改。
    更容易追踪数据变化。

```js
const numbers = [1, 2, 3];
const newNumbers = numbers.concat(4); // 生成新数组
console.log(numbers); // [1, 2, 3]
console.log(newNumbers); // [1, 2, 3, 4]
```

1.3 高阶函数（Higher-Order Function）
定义：高阶函数是指接受函数作为参数或返回函数的函数。

```js
// 接受函数作为参数
function map(array, fn) {
  return array.map(fn);
}

// 返回函数
function add(a) {
  return function(b) {
    return a + b;
  };
}
```

1.4 函数组合（Function Composition）
定义：将多个函数组合成一个新的函数，前一个函数的输出作为后一个函数的输入。

```js
const add = (a, b) => a + b;
const square = x => x * x;

const addAndSquare = (a, b) => square(add(a, b));
console.log(addAndSquare(2, 3)); // 25
```

1.5 柯里化（Currying）
定义：将多参数函数转换为一系列单参数函数的过程。

```js
const add = a => b => a + b;
const add5 = add(5);
console.log(add5(3)); // 8
```

2. 函数式编程的优势
可维护性：
    纯函数和不可变数据使代码更易于理解和测试。

可复用性：
    高阶函数和函数组合提高了代码的复用性。

并发安全：
    纯函数没有副作用，适合并发环境。

声明式风格：
    代码更简洁，更关注“做什么”而不是“怎么做”。


3. 函数式编程的实践
3.1 使用纯函数
避免副作用，确保函数的行为可预测。
```js
// 非纯函数
let total = 0;
function addToTotal(amount) {
  total += amount;
  return total;
}

// 纯函数
function add(a, b) {
  return a + b;
}
```

3.2 使用不可变数据
使用 const 声明变量，避免直接修改数据。

```js
const numbers = [1, 2, 3];
const newNumbers = [...numbers, 4]; // 使用扩展运算符生成新数组
```

3.3 使用高阶函数
使用 map、filter、reduce 等函数处理数组。

```js
const numbers = [1, 2, 3, 4, 5];
const squares = numbers.map(x => x * x);
const evens = numbers.filter(x => x % 2 === 0);
const sum = numbers.reduce((acc, x) => acc + x, 0);
```

3.4 函数组合
使用工具库（如 lodash、ramda）或自定义函数组合工具。

```js
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);

const add = (a, b) => a + b;
const square = x => x * x;

const addAndSquare = compose(square, add);
console.log(addAndSquare(2, 3)); // 25
```

3.5 柯里化
使用工具库或自定义柯里化函数。

```js
const curry = fn => (...args) =>
  args.length >= fn.length ? fn(...args) : curry(fn.bind(null, ...args));

const add = curry((a, b) => a + b);
const add5 = add(5);
console.log(add5(3)); // 8
```

4. 函数式编程的工具库
    Lodash：提供了丰富的函数式编程工具函数。
    Ramda：专注于函数式编程的工具库，支持自动柯里化。
    Immutable.js：提供了不可变数据结构的实现。

## 防抖与节流

防抖：多次触发只执行最后一次。
节流：一段时间内只执行一次。

1. 防抖（Debounce）
1.1 定义
防抖是指在一定时间内，如果事件被多次触发，只执行最后一次触发的函数调用。如果在规定时间内事件再次触发，则重新计时。

1.2 适用场景
    输入框实时搜索（用户停止输入后再触发搜索）。
    窗口大小调整（用户停止调整后再触发计算）。
    按钮点击防止多次提交。

1.3 实现
```js
function debounce(fn, delay) {
  let timer = null;
  return function(...args) {
    if (timer) {
      clearTimeout(timer);
    }
    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}
```
```js
const input = document.querySelector('input');

function onInput(event) {
  console.log('输入内容:', event.target.value);
}

const debouncedInput = debounce(onInput, 300);
input.addEventListener('input', debouncedInput);
```

2. 节流（Throttle）
2.1 定义
节流是指在一定时间内，无论事件触发多少次，只执行一次函数调用。类似于控制函数的执行频率。

2.2 适用场景
    滚动事件（每隔一段时间触发一次）。
    鼠标移动事件（每隔一段时间触发一次）。
    高频点击事件（防止用户快速点击）。

2.3 实现
```js
function throttle(fn, delay) {
  let lastTime = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastTime >= delay) {
      fn.apply(this, args);
      lastTime = now;
    }
  };
}
```
```js
window.addEventListener('scroll', throttle(() => {
  console.log('滚动事件触发');
}, 300));
```

4. 进阶实现
4.1 防抖的立即执行版本
```js
function debounce(fn, delay, immediate = false) {
  let timer = null;
  return function(...args) {
    if (timer) {
      clearTimeout(timer);
    }
    if (immediate && !timer) {
      fn.apply(this, args);
    }
    timer = setTimeout(() => {
      if (!immediate) {
        fn.apply(this, args);
      }
      timer = null;
    }, delay);
  };
}
```

4.2 节流的定时器版本
```js
function throttle(fn, delay) {
  let timer = null;
  return function(...args) {
    if (!timer) {
      timer = setTimeout(() => {
        fn.apply(this, args);
        timer = null;
      }, delay);
    }
  };
}
```

## 垃圾回收

1. 垃圾回收的基本概念
1.1 什么是垃圾回收？
    垃圾回收是指自动管理内存分配和释放的过程。
    JavaScript 引擎（如 V8）会自动跟踪内存的使用情况，并在适当的时候回收不再使用的内存。

1.2 为什么需要垃圾回收？
    手动管理内存容易出错（如忘记释放内存导致内存泄漏，或过早释放内存导致程序崩溃）。
    垃圾回收可以减轻开发者的负担，提高代码的健壮性。

2. 垃圾回收的算法
JavaScript 引擎通常使用以下两种主要的垃圾回收算法：

2.1 标记-清除算法（Mark-and-Sweep）
步骤：
    标记：从根对象（如全局对象、当前调用栈）出发，标记所有可达的对象。
    清除：遍历堆内存，清除未被标记的对象。

优点：
    解决了循环引用的问题。

缺点：
    可能会导致内存碎片。

2.2 引用计数算法（Reference Counting）
原理：每个对象维护一个引用计数，当引用计数为 0 时，对象被回收。

优点：
    实时性高，对象不再被引用时立即回收。

缺点：
    无法处理循环引用的问题。

## 内存泄漏

1. 内存泄漏的常见原因

1.1 未清除的定时器： setInterval 或 setTimeout 未清除，导致回调函数持续引用外部变量。
1.2 未移除的事件监听器：事件监听器未移除，导致 DOM 元素和回调函数无法被回收。
1.3 闭包导致的引用：闭包会捕获外部函数的变量，导致这些变量无法被回收。
```js
function createClosure() {
  const largeArray = new Array(1000000).fill('data');
  return function() {
    console.log(largeArray.length);
  };
}

const closure = createClosure();

// largeArray 无法被回收，即使 closure 不再使用
```
解决方法：在不需要时解除引用。
```js
closure = null; // 解除引用
```

1.4 意外的全局变量：未使用 var、let 或 const 声明的变量会成为全局变量，直到页面关闭才会被释放。
> 解决方法：始终使用 var、let 或 const 声明变量。

1.5 未清理的 DOM 引用：保存了 DOM 元素的引用，即使 DOM 元素被移除，仍然无法被回收。
```js
const elements = [];
function addElement() {
  const element = document.createElement('div');
  document.body.appendChild(element);
  elements.push(element); // 保存 DOM 引用
}

function removeElement() {
  document.body.removeChild(elements[0]); // 移除 DOM 元素
}

// 即使 DOM 元素被移除，elements 数组仍然引用它
```
解决方法：在不需要时清除 DOM 引用。
```js
elements.length = 0; // 清除 DOM 引用
```

2. 内存泄漏的检测与调试
2.1 Chrome DevTools
Memory 面板：
    使用 Heap Snapshot 查看内存快照，分析内存使用情况。
    使用 Allocation Timeline 跟踪内存分配，查找内存泄漏。

Performance 面板：
    分析内存使用情况，查找内存泄漏。

2.2 Node.js 内存分析
使用 --inspect 参数：
    启动 Node.js 应用时添加 --inspect 参数，使用 Chrome DevTools 调试。

使用 v8 模块：
    使用 v8.getHeapStatistics() 获取堆内存统计信息。

3. 避免内存泄漏的最佳实践
及时清除定时器和事件监听器：
    使用 clearInterval、clearTimeout 和 removeEventListener。

避免意外的全局变量：
    始终使用 var、let 或 const 声明变量。

解除不再使用的引用：
    将不再使用的对象或变量设置为 null。

使用弱引用：
    使用 WeakMap 或 WeakSet 存储临时数据，避免阻止垃圾回收。

定期检查内存使用情况：
    使用工具（如 Chrome DevTools）分析内存使用情况，及时发现内存泄漏。

## 浅拷贝和深拷贝

1. 浅拷贝（Shallow Copy）
1.1 定义
    浅拷贝是指创建一个新对象，新对象的属性值是原对象属性值的引用。如果属性值是基本类型，则直接复制值；如果属性值是引用类型（如对象、数组），则复制引用。

1.2 特点
    只复制对象的第一层属性。
    嵌套对象仍然是共享的（修改嵌套对象会影响原对象）。

1.3 实现方式
1.3.1 使用 Object.assign
```js
const obj = { a: 1, b: { c: 2 } };
const shallowCopy = Object.assign({}, obj);

shallowCopy.b.c = 3;
console.log(obj.b.c); // 3（原对象被修改）
```

1.3.2 使用扩展运算符（Spread Operator）
```js
const obj = { a: 1, b: { c: 2 } };
const shallowCopy = { ...obj };

shallowCopy.b.c = 3;
console.log(obj.b.c); // 3（原对象被修改）
```

1.3.3 数组的浅拷贝
```js
const arr = [1, 2, { a: 3 }];
const shallowCopy = arr.slice(); // 或使用 [...arr]

shallowCopy[2].a = 4;
console.log(arr[2].a); // 4（原数组被修改）
```

2. 深拷贝（Deep Copy）
2.1 定义
    深拷贝是指创建一个新对象，递归地复制原对象的所有属性。新对象和原对象完全独立，修改新对象不会影响原对象。

2.2 特点
    复制对象的所有层级属性。
    嵌套对象也是独立的（修改嵌套对象不会影响原对象）。

2.3 实现方式
2.3.1 使用 JSON.parse 和 JSON.stringify
优点：简单易用。

缺点：
    无法复制函数、undefined、Symbol 等特殊类型。
    无法处理循环引用。

```js
const obj = { a: 1, b: { c: 2 } };
const deepCopy = JSON.parse(JSON.stringify(obj));

deepCopy.b.c = 3;
console.log(obj.b.c); // 2（原对象未被修改）
```

2.3.2 递归实现深拷贝
优点：可以处理所有数据类型，包括函数、undefined、Symbol 等。

缺点：需要手动处理循环引用。

```js
function deepCopy(obj, cache = new WeakMap()) {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }
  if (cache.has(obj)) {
    return cache.get(obj);
  }
  const result = Array.isArray(obj) ? [] : {};
  cache.set(obj, result);
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      result[key] = deepCopy(obj[key], cache);
    }
  }
  return result;
}

const obj = { a: 1, b: { c: 2 } };
const deepCopy = deepCopy(obj);

deepCopy.b.c = 3;
console.log(obj.b.c); // 2（原对象未被修改）
```

2.3.3 使用工具库
Lodash：提供了 _.cloneDeep 方法。

```js
const _ = require('lodash');
const obj = { a: 1, b: { c: 2 } };
const deepCopy = _.cloneDeep(obj);

deepCopy.b.c = 3;
console.log(obj.b.c); // 2（原对象未被修改）
```

4. 选择浅拷贝还是深拷贝？
浅拷贝：
    适用于简单对象，且不需要复制嵌套对象。
    性能较高，适合频繁复制的场景。

深拷贝：
    适用于复杂对象，且需要完全独立的副本。
    性能较低，但可以避免嵌套对象共享的问题。

## 算法题：数组去重

1. 使用 Set
优点：
    代码简洁，性能较好。

缺点：
    无法处理对象类型的元素（因为 Set 使用严格相等 === 判断唯一性）。

```js
function uniqueArray(arr) {
  return [...new Set(arr)];
}
const arr = [1, 2, 2, 3, 4, 4, 5];
const result = uniqueArray(arr);
console.log(result); // [1, 2, 3, 4, 5]
```

2. 使用 filter 和 indexOf
优点：
    兼容性好，支持 ES5。

缺点：
    性能较差（indexOf 的时间复杂度为 O(n)）。

```js
function uniqueArray(arr) {
  return arr.filter((item, index) => arr.indexOf(item) === index);
}
const arr = [1, 2, 2, 3, 4, 4, 5];
const result = uniqueArray(arr);
console.log(result); // [1, 2, 3, 4, 5]
```

3. 使用 reduce
优点：
    代码灵活，可以处理复杂逻辑。

缺点：
    性能较差（includes 的时间复杂度为 O(n)）。

```js
function uniqueArray(arr) {
  return arr.reduce((acc, item) => {
    if (!acc.includes(item)) {
      acc.push(item);
    }
    return acc;
  }, []);
}
const arr = [1, 2, 2, 3, 4, 4, 5];
const result = uniqueArray(arr);
console.log(result); // [1, 2, 3, 4, 5]
```

4. 使用 for 循环
优点：
    性能较好（Set 的查找时间复杂度为 O(1)）。

缺点：
    代码稍显冗长。

```js
function uniqueArray(arr) {
  const result = [];
  const seen = new Set();
  for (const item of arr) {
    if (!seen.has(item)) {
      seen.add(item);
      result.push(item);
    }
  }
  return result;
}
const arr = [1, 2, 2, 3, 4, 4, 5];
const result = uniqueArray(arr);
console.log(result); // [1, 2, 3, 4, 5]
```

5. 处理对象类型的去重
如果数组中包含对象类型的元素，可以使用 JSON.stringify 将对象转换为字符串进行去重。

优点：
    支持对象类型的去重。

缺点：
    性能较差（JSON.stringify 的时间复杂度较高）。

```js
function uniqueArray(arr) {
  const seen = new Set();
  return arr.filter((item) => {
    const str = JSON.stringify(item);
    return seen.has(str) ? false : seen.add(str);
  });
}
const arr = [{ a: 1 }, { a: 1 }, { b: 2 }];
const result = uniqueArray(arr);
console.log(result); // [{ a: 1 }, { b: 2 }]
```

## 算法题：两数之和

问题：给定一个整数数组 nums 和一个目标值 target，在数组中找出和为目标值的两个整数，并返回它们的下标。

1. 问题描述
输入：一个整数数组 nums 和一个目标值 target。
输出：两个整数的下标，使得它们的和等于 target。
假设：每种输入只会对应一个答案，且同一个元素不能使用两次。

示例：
```js
const nums = [2, 7, 11, 15];
const target = 9;
// 输出: [0, 1]，因为 nums[0] + nums[1] = 2 + 7 = 9
```

2. 暴力解法

思路：使用双重循环遍历数组，检查每对元素的和是否等于 target。
```js
function twoSum(nums, target) {
  for (let i = 0; i < nums.length; i++) {
    for (let j = i + 1; j < nums.length; j++) {
      if (nums[i] + nums[j] === target) {
        return [i, j];
      }
    }
  }
  return [];
}
```

复杂度分析
    时间复杂度：O(n²)，其中 n 是数组长度。
    空间复杂度：O(1)。

3. 哈希表优化
3.1 思路
    使用哈希表（对象或 Map）存储数组元素及其下标。
    遍历数组，检查 target - nums[i] 是否在哈希表中：
        如果存在，则返回当前下标和哈希表中的下标。
        如果不存在，则将当前元素及其下标存入哈希表。
```js
function twoSum(nums, target) {
  const map = new Map();
  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];
    if (map.has(complement)) {
      return [map.get(complement), i];
    }
    map.set(nums[i], i);
  }
  return [];
}
```

复杂度分析
    时间复杂度：O(n)，只需遍历数组一次。
    空间复杂度：O(n)，哈希表存储最多 n 个元素。

4. 双指针法（适用于有序数组）
4.1 思路
如果数组是有序的，可以使用双指针法：
    初始化两个指针，分别指向数组的开头和结尾。
    计算两个指针指向元素的和：
        如果和等于 target，返回两个指针的下标。

        如果和小于 target，左指针右移。

        如果和大于 target，右指针左移。
```js
function twoSum(nums, target) {
  let left = 0;
  let right = nums.length - 1;
  while (left < right) {
    const sum = nums[left] + nums[right];
    if (sum === target) {
      return [left, right];
    } else if (sum < target) {
      left++;
    } else {
      right--;
    }
  }
  return [];
}
```

复杂度分析
    时间复杂度：O(n)，只需遍历数组一次。
    空间复杂度：O(1)。


## 算法题：反转链表

问题：给定一个单链表的头节点，反转链表并返回反转后的头节点。

1. 问题描述
输入：一个单链表的头节点 head。
输出：反转后的链表的头节点。

```js
输入: 1 -> 2 -> 3 -> 4 -> 5 -> null
输出: 5 -> 4 -> 3 -> 2 -> 1 -> null
```

2. 迭代法
2.1 思路
使用三个指针：
    prev：指向当前节点的前一个节点，初始为 null。
    curr：指向当前节点，初始为 head。
    next：指向当前节点的下一个节点。
    遍历链表，逐个反转节点的指向。
```js
function reverseList(head) {
  let prev = null;
  let curr = head;
  while (curr !== null) {
    const next = curr.next; // 保存下一个节点
    curr.next = prev; // 反转当前节点的指向
    prev = curr; // 移动 prev 指针
    curr = next; // 移动 curr 指针
  }
  return prev; // 返回反转后的头节点
}
```

复杂度分析
    时间复杂度：O(n)，其中 n 是链表的长度。
    空间复杂度：O(1)。

3. 递归法
3.1 思路
递归地反转链表：
    递归到链表的最后一个节点，将其作为新的头节点。
    在回溯过程中，逐个反转节点的指向。
```js
function reverseList(head) {
  if (head === null || head.next === null) {
    return head; // 递归终止条件
  }
  const newHead = reverseList(head.next); // 递归反转剩余链表
  head.next.next = head; // 反转当前节点的指向
  head.next = null; // 断开当前节点的原指向
  return newHead; // 返回新的头节点
}
```
复杂度分析
    时间复杂度：O(n)，其中 n 是链表的长度。
    空间复杂度：O(n)，递归调用栈的深度。

## 