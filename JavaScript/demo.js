
// @ts-nocheck
// 原型，原型链
const example1 = () => {
    console.log('============ example1 =================');
    function doSomething() { }
    console.log(doSomething.prototype);
};
example1();

// new操作符
const example2 = () => {
    console.log('============ example2 =================');
    console.log('--------------- 构造函数 无返回值 ---------------');
    function Person(name, age) {
        this.name = name;
        this.age = age;
    }
    Person.prototype.sayName = function () {
        console.log(this.name);
    };
    const Person0 = new Person('张三', 20);
    console.log(Person0); // Person { name: '张三', age: 20 }
    Person0.sayName(); // 张三
    console.log('--------------- 在构造函数中显示加上返回值，并且返回值是一个原始类型 ---------------');

    function Person1(name) {
        this.name = name;
        return 1;
    }
    const Person01 = new Person1('张三');
    console.log(Person01.name); // 张三

    console.log('--------------- 在构造函数中显示加上返回值，并且返回值是一个对象 ---------------');

    function Person2(name) {
        this.name = name;
        console.log(this);
        return { age: 20 };
    }
    const Person02 = new Person2('张三');
    console.log(Person02); // { age: 20 }
    console.log(Person02.name); // undefined

    console.log('--------------- 手写new操作符 ---------------');
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
    function testMyNew(name, age) {
        this.name = name;
        this.age = age;
    }
    testMyNew.prototype.sayName = function () {
        console.log(this.name);
    };
    const test1 = myNew(testMyNew, 'test', 10);
    console.log(test1);
    test1.sayName();
};
example2();

// bind、applu、call 
const example3 = () => {
    console.log('============ example3 =================');
    console.log('--------------- apply ---------------');
    let name = '123';
    function fn(...args) {
        console.log(this.name, args);
    }
    let obj = {
        name: '张三',
    };
    fn.apply(obj, [1, 2]); // this会变成传入的obj，传入的参数必须是一个数组；
    fn(1, 2); //  this指向window

    fn.apply(null, [1, 2]); // this指向window
    fn.apply(undefined, [1, 2]); // this指向window

    console.log('--------------- call ---------------');
    fn.call(obj, 1, 2);
    fn(1, 2);

    fn.call(null, [1, 2]); // this指向window
    fn.call(undefined, [1, 2]); // this指向window

    console.log('--------------- bind ---------------');
    const bindFn = fn.bind(obj); // this 也会变成传入的obj，bind不是立即执行的，需要执行一次
    bindFn(1, 2); // this指向obj
    fn(1, 2); // this指向window
};
example3();


// 手写bind
const example4 = () => {
    console.log('============ example4 =================');
    Function.prototype.myBind = function (context) {
        // 判断调用对象是否为函数
        if (typeof this !== 'function') {
            throw new TypeError('Error');
        }

        // 获取参数
        const args = [...arguments].slice(1),
            fn = this;

        return function Fn() {
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
};
example4();

// typeof instanceof 的区别
const example5 = () => {
    console.log('============ example5 =================');

    console.log('--------------- typeof ---------------');
    console.log(typeof 1); // 'number'
    console.log(typeof '1'); // 'string'
    console.log(typeof undefined); // 'undefined'
    console.log(typeof true); // 'boolean'
    console.log(typeof Symbol()); // 'symbol'
    console.log(typeof null); // 'object'
    console.log(typeof []); // 'object'
    console.log(typeof {}); // 'object'
    console.log(typeof console); // 'object'
    console.log(typeof console.log); // 'function'

    console.log('--------------- instanceof ---------------');
    let Car = function () { }; // 定义构造函数
    let benz = new Car();
    console.log(benz instanceof Car); // true

    let car = new String('123');
    console.log(car instanceof String); // true

    let str = '123';
    console.log(str instanceof String); //false

    console.log('--------------- 完美实现类型判断 ---------------');
    function getType (obj) {
        let type = typeof obj;
        // 先进行typeof判断，如果是基础类型，直接返回
        if (type !== 'object') return type;
        // 对于typeof返回结果为object，再使用 Object.prototype.toString 进行判断
        const _type = Object.prototype.toString.call(obj).replace(/^\[object (\S+)\]$/, '$1');
        return _type.toLowerCase();
    }

    console.log(getType(1));
    console.log(getType('1'));
    // console.log(getType(window)); // 需在浏览器中执行
    console.log(getType(null));
    console.log(getType(undefined));
    console.log(getType());
    console.log(getType(function() {}));
    console.log(getType(/123/g));
    console.log(getType([]));
    console.log(getType({}));
};
example5();