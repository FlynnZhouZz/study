# bind、apply、call的区别

call(),apply(),bind()都是用来重定义this这个对象的。

示例代码

```js
let name = '123';
function fn(...args) {
    console.log(this.name, args);
}
let obj = {
    name: '张三',
};
```

## apply

### 参数
apply接受两个参数，
第一个参数是this的指向，
第二个参数是函数接受的参数，以数组的形式传入

> 改变this指向后原函数会立即执行，且此方法只是临时改变this指向一次
> 当第一个参数为null、undefined的时候，默认指向window(在浏览器中)

```js
fn.apply(obj, [1, 2]); // this会变成传入的obj，传入的参数必须是一个数组；
fn(1, 2); //  this指向window

fn.apply(null, [1, 2]); // this指向window
fn.apply(undefined, [1, 2]); // this指向window
```

## call

### 参数

call方法的第一个参数也是this的指向，后面传入的是一个参数列表

> 改变this指向后原函数会立即执行，且此方法只是临时改变this指向一次
> 当第一个参数为null、undefined的时候，默认指向window(在浏览器中)

```js
fn.call(obj, 1, 2);
fn(1, 2);

fn.call(null, [1, 2]); // this指向window
fn.call(undefined, [1, 2]); // this指向window
```

## bind

### 参数

第一参数也是this的指向，
后面传入的也是一个参数列表(但是这个参数列表可以分多次传入)

> 改变this指向后不会立即执行，而是返回一个永久改变this指向的函数

```js
const bindFn = fn.bind(obj, 1, 2); // this 也会变成传入的obj，bind不是立即执行的，需要执行一次
bindFn(1, 2); // this指向obj
fn(1, 2); // this指向window
```

## 小结

- 三者都可以改变函数的this对象指向
- 三者第一个参数都是this要指向的对象，如果没有这个参数或参数为undefined或null，则默认指向全局window
- 三者都可以传参，但是apply是数组，而call是参数列表，且apply和call是一次性传入参数，而bind可以分为多次传入
- bind是返回绑定this之后的函数，不立即执行；apply、call 则是立即执行

## apply实现bind步骤

```js
Function.prototype.myBind = function (context) {
    // 判断调用对象是否为函数
    if (typeof this !== 'function') {
        throw new TypeError('Error');
    }

    // 获取参数
    const args = [...arguments].slice(1),
    fn = this;

    return function Fn () {
        // 根据调用方式，传入不同绑定值 
        return fn.apply(this instanceof Fn ? fn(...arguments) : context, args.concat(...arguments));
    }
};


// 测试
function fn(...args) {
    console.log(this.name, args);
}
let obj = {
    name: '张三',
};

const bindFn = fn.myBind(obj); // this 也会变成传入的obj，bind不是立即执行的，需要执行一次
bindFn(1, 2); // this指向obj
fn(1, 2); // this指向window
```