## new操作符

### 构造函数 无返回值
```js
function Person(name, age) {
    this.name = name;
    this.age = age;
}
Person.prototype.sayName = function() {
    console.log(this.name);
};
const Person0 = new Person('张三', 20);
console.log(Person0); // Person { name: '张三', age: 20 }
Person0.sayName(); // 张三
```
### 在构造函数中显示加上返回值，并且返回值是一个原始类型

```js
function Person(name) {
    this.name = name;
    return { name }; // 返回值是一个原始类型
}
const Person1 = new Person('张三');
console.log(Person1.name); // 张三
```

### 在构造函数中显示加上返回值，并且返回值是一个对象

```js
function Person2(name) {
    this.name = name;
    console.log(this);
    return { age: 20 };
}
const Person02 = new Person2('张三');
console.log(Person02); // { age: 20 }
console.log(Person02.name); // undefined
```

1. 创建一个新的对象 obj；
2. 将对象与构建函数通过原型链连接起来；
3. 将构建函数中的this绑定到新建的对象上；
4. 根据构建函数返回类型作判断，如果是原始值则被忽略，如果是返回对象，需要正常处理。

### 手写new操作符

```js
function myNew(Func, ...args) {
    // 1、创建一个对象 obj
    const obj = {};
    // 2、将对象与构建函数通过原型链连接起来（其实就是 新对象原型指向构造函数原型对象）
    obj.__proto__ = Func.prototype;
    // 3、将构建函数中的this绑定到新建的对象上（将构建函数的this指向新对象）
    let result = Func.apply(obj, args);
    // 4、根据返回值判断
    return result instanceof Object ? result : obj;
}
```

