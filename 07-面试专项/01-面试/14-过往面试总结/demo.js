// @ts-nocheck
// 示例1
const example1 = () => {
    console.log('============ example1 =================');
    const tom = {
        size: 'big'
    };
    const mouse = {
        name: 'jerry',
        big: false
    };
    console.log(`A. mouse[tom.size]是 ${mouse[tom.size]}`);
    console.log(`B. mouse.tom.size]是 ${mouse?.tom?.size}`); // 此调用方式直接报错
    console.log(`C. mouse[tom['size']]]是 ${mouse[tom['size']]}`);
};
example1();

// 示例2
const example2 = () => {
    console.log('============ example2 =================');
    const shape = {
        radius: 10,
        diameter() {
            return this.radius * 2;
        },
        primeter: () => 2 * Math.PI * this.radius,
    };
    console.log(`shape.diameter是 ${shape.diameter()}`);
    console.log(`shape.primeter是 ${shape.primeter()}`);

};
example2();

// 示例3
const example3 = () => {
    console.log('============ example3 =================');
    window.identity = 'The Window';
    let object = {
        identity: 'My object',
        getIdentity() {
            return this.identity;
        },
    };
    (object.getIdentity)(); // 1
    (object.getIdentity = object.getIdentity)(); // 2
    console.log(`1是 ${(object.getIdentity)()}`);
    console.log(`2是 ${(object.getIdentity = object.getIdentity)()}`);
};
// 不能使用node命令执行，因为服务器端不存在window对象
// example3();

// 示例4
const example4 = () => {
    console.log('============ example4 =================');

    console.log('------- 写法1 -------');
    (function f(a, b){
        console.log(`声明函数 自调用a+b: ${a+b}`);
    }(1,2));
    (function (a, b){
        console.log(`匿名函数 自调用a+b: ${a+b}`);
    }(1,2));

    console.log('------- 写法2 -------');
    (function f(a, b){
        console.log(`声明函数 自调用a+b: ${a+b}`);
    })(1,2);
    (function (a, b){
        console.log(`匿名函数 自调用a+b: ${a+b}`);
    })(1,2);
    // 函数自调用的作用
    // 模仿一个私有作用域，防止你在全局或局部作用域中声明的变量，会被其他人不小心用同名的变量给覆盖掉。
    // 用匿名函数作为一个“容器”，“容器”内部可以访问外部的变量，而外部环境不能访问“容器”内部的变量，所以( function(){…} )()内部定义的变量不会和外部的变量发生冲突，俗称匿名包裹器或命名空间。
};
example4();

// 示例5
const example5 = () => {
    console.log('============ example5 =================');
    const time = new Date();
    console.log(time.getDate());
};
example5();


// 示例6
const example6 = () => {
    console.log('============ example6 =================');
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
};
example6();