# typeof 和 instanceof 的区别

## typeof 

typeof 操作符返回一个字符串，表示未经计算的操作数的类型

引用类型数据，用typeof来判断的话，除了function会被识别出来之外，其余的都输出object。

使用方法：
```js
// operand 表示对象或原始值表达式
typeof operand;
typeof(operand);
```

示例：
```js
// 返回类型举例
typeof 1; // 'number'
typeof '1'; // 'string'
typeof undefined; // 'undefined'
typeof true; // 'boolean'
typeof Symbol(); // 'symbol'
typeof null; // 'object'
typeof []; // 'object'
typeof {}; // 'object'
typeof console; // 'object'
typeof console.log; // 'function'
```

## instanceof

instanceof 运算符用于检测构造函数的 prototype 属性是否出现在某个实例对象的原型链上

> 顺着原型链去找，直到找到相同的原型对象，返回true，否则为false

```js
// object: 实例对象
// constructor: 构造函数
object instanceof  constructor
```

示例：
```js
let Car = function() {}; // 定义构造函数
let benz = new Car();
console.log(benz instanceof Car); // true

let car = new String('123');
console.log(car instanceof String); // true

let str = '123';
console.log(str instanceof String); //false
```

## 总结

typeof与instanceof都是判断数据类型的方法

- typeof会返回一个变量的基本类型，instanceof返回的是一个布尔值
- instanceof 可以准确地判断复杂引用数据类型，但是不能正确判断基础数据类型
- 而typeof 也存在弊端，它虽然可以判断基础数据类型（null 除外），但是引用数据类型中，除了function 类型以外，其他的也无法判断

## typeof 和 instanceof都有利弊，如何实现完美的类型判断

```js
function getType (obj) {
    let type = typeof obj;
    // 先进行typeof判断，如果是基础类型，直接返回
    if (type !== 'object') return type;
    // 对于typeof返回结果为object，再使用 Object.prototype.toString 进行判断
    return Object.prototype.toString.call(obj).replace(/^\[Object (\S+)\]$/, '$1');
}
```