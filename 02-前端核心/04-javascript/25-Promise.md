# Promise

ES6+

## 1. Promise 基础

### 创建 Promise

```js
// 1. 直接创建
const promise = new Promise((resolve, reject) => {
    // 异步操作
    setTimeout(() => {
        const success = Math.random() > 0.5;

        if (success) {
            resolve("操作成功！");
        } else {
            reject(new Error("操作失败！"));
        }
    }, 1000);
});

// 2. 使用 Promise 静态方法
const resolvedPromise = Promise.resolve("立即解决的值");
const rejectedPromise = Promise.reject(new Error("立即拒绝的原因"));
```

## 2. Promise 基本使用

```js
// 消费 Promise
const fetchData = () => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const data = { id: 1, name: "张三" };
            resolve(data);
        }, 1000);
    });
};

// then/catch 方法
fetchData()
    .then(data => {
        console.log("成功:", data);
        return data.name; // 返回新值，传递给下一个 then
    })
    .then(name => {
        console.log("姓名:", name);
    })
    .catch(error => {
        console.error("失败:", error);
    })
    .finally(() => {
        console.log("请求结束，无论成功失败都会执行");
    });

// then 接收两个参数
promise.then(
    value => console.log("成功:", value),
    error => console.error("失败:", error)
);
```

## 3. Promise 链式调用

```js
// 模拟异步操作
const login = (username, password) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (username && password) {
                resolve({ token: "abc123", userId: 1 });
            } else {
                reject(new Error("用户名或密码错误"));
            }
        }, 500);
    });
};

const getUserInfo = userId => {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve({ userId, name: "张三", age: 25 });
        }, 500);
    });
};

const getOrders = userId => {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve([
                { orderId: 1, amount: 100 },
                { orderId: 2, amount: 200 },
            ]);
        }, 500);
    });
};

// 链式调用
login("admin", "123456")
    .then(response => {
        console.log("登录成功:", response);
        return getUserInfo(response.userId);
    })
    .then(userInfo => {
        console.log("用户信息:", userInfo);
        return getOrders(userInfo.userId);
    })
    .then(orders => {
        console.log("订单列表:", orders);
    })
    .catch(error => {
        console.error("发生错误:", error);
    });
```

## 4. Promise 静态方法

### Promise.all()

```js
// 所有 Promise 都成功时才成功
const p1 = Promise.resolve("结果1");
const p2 = 42; // 非 Promise 值会自动转换
const p3 = new Promise(resolve => {
    setTimeout(() => resolve("结果3"), 1000);
});

Promise.all([p1, p2, p3])
    .then(values => {
        console.log(values); // ['结果1', 42, '结果3']
    })
    .catch(error => {
        // 任何一个失败就进入这里
        console.error(error);
    });

// 实际应用：并发请求
const urls = ["/api/user", "/api/posts", "/api/comments"];
const requests = urls.map(url => fetch(url));

Promise.all(requests)
    .then(responses => Promise.all(responses.map(res => res.json())))
    .then(data => {
        console.log("所有数据:", data);
    });
```

### Promise.allSettled()

```js
// 等待所有 Promise 完成（无论成功或失败）
const promises = [
    Promise.resolve("成功1"),
    Promise.reject(new Error("失败1")),
    Promise.resolve("成功2"),
];

Promise.allSettled(promises).then(results => {
    results.forEach((result, index) => {
        if (result.status === "fulfilled") {
            console.log(`Promise ${index}:`, result.value);
        } else {
            console.log(`Promise ${index}:`, result.reason);
        }
    });
});
```

### Promise.race()

```js
// 第一个完成的 Promise（无论成功失败）
const timeout = new Promise((_, reject) => {
    setTimeout(() => reject(new Error("请求超时")), 5000);
});

const fetchPromise = fetch("/api/data");

Promise.race([fetchPromise, timeout])
    .then(response => {
        console.log("数据获取成功");
    })
    .catch(error => {
        console.error("请求失败或超时:", error);
    });
```

### Promise.any()

```js
// 第一个成功的 Promise
const promises = [
    Promise.reject(new Error("失败1")),
    Promise.reject(new Error("失败2")),
    Promise.resolve("第一个成功的结果"),
];

Promise.any(promises)
    .then(value => {
        console.log("成功:", value); // '第一个成功的结果'
    })
    .catch(error => {
        console.error("所有Promise都失败了:", error);
    });
```

## 5. Promise 高级用法

### 错误处理最佳实践

```js
function apiCall() {
    return new Promise((resolve, reject) => {
        // 模拟API调用
        setTimeout(() => {
            const success = Math.random() > 0.3;
            if (success) {
                resolve({ data: "API返回的数据" });
            } else {
                reject(new Error("API调用失败"));
            }
        }, 1000);
    });
}

// 正确的错误处理方式
apiCall()
    .then(response => {
        // 处理成功响应
        console.log("成功:", response);
        // 可能会抛出错误
        if (!response.data) {
            throw new Error("数据格式错误");
        }
        return response.data;
    })
    .then(data => {
        // 进一步处理数据
        console.log("数据:", data);
    })
    .catch(error => {
        // 捕获所有错误
        console.error("捕获错误:", error);
        // 可以返回默认值或重新抛出
        if (error.message === "API调用失败") {
            return { data: "默认数据" };
        }
        throw error; // 重新抛出给上层
    });
```

### Promise 化回调函数

```js
// 将回调函数转换为 Promise
const readFile = filename => {
    return new Promise((resolve, reject) => {
        // 假设这是回调风格的函数
        fs.readFile(filename, (err, data) => {
            if (err) {
                reject(err);
            } else {
                resolve(data);
            }
        });
    });
};

// Node.js util.promisify 示例
const util = require("util");
const fs = require("fs");
const readFileAsync = util.promisify(fs.readFile);

// 自定义 promisify 函数
function promisify(fn) {
    return function (...args) {
        return new Promise((resolve, reject) => {
            fn(...args, (err, result) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(result);
                }
            });
        });
    };
}
```

### 顺序执行 Promise

```js
// 使用 async/await 顺序执行
async function sequentialOperations() {
    try {
        const result1 = await operation1();
        const result2 = await operation2(result1);
        const result3 = await operation3(result2);
        return result3;
    } catch (error) {
        console.error("执行失败:", error);
        throw error;
    }
}

// 使用 reduce 顺序执行
const operations = [op1, op2, op3, op4];

operations.reduce(async (previousPromise, nextOperation) => {
    await previousPromise;
    return nextOperation();
}, Promise.resolve());
```

## 6. 实际应用示例

### 用户注册流程

```js
class UserService {
    // 检查用户名是否可用
    checkUsername(username) {
        return new Promise(resolve => {
            setTimeout(() => {
                const isAvailable = username.length >= 3;
                resolve(isAvailable);
            }, 300);
        });
    }

    // 发送验证码
    sendVerificationCode(email) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (email.includes("@")) {
                    resolve("验证码已发送");
                } else {
                    reject(new Error("邮箱格式错误"));
                }
            }, 500);
        });
    }

    // 创建用户
    createUser(userData) {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve({
                    id: Date.now(),
                    ...userData,
                    createdAt: new Date(),
                });
            }, 800);
        });
    }

    // 完整的注册流程
    async register(userData) {
        try {
            // 并行检查
            const [usernameAvailable, codeSent] = await Promise.all([
                this.checkUsername(userData.username),
                this.sendVerificationCode(userData.email),
            ]);

            if (!usernameAvailable) {
                throw new Error("用户名不可用");
            }

            // 创建用户
            const user = await this.createUser(userData);

            // 发送欢迎邮件（不等待完成）
            this.sendWelcomeEmail(user.email).catch(console.error);

            return user;
        } catch (error) {
            console.error("注册失败:", error);
            throw error;
        }
    }

    sendWelcomeEmail(email) {
        return new Promise(resolve => {
            setTimeout(() => {
                console.log(`欢迎邮件已发送至: ${email}`);
                resolve();
            }, 1000);
        });
    }
}

// 使用示例
const userService = new UserService();
const userData = {
    username: "john_doe",
    email: "john@example.com",
    password: "secure123",
};

userService
    .register(userData)
    .then(user => {
        console.log("注册成功:", user);
    })
    .catch(error => {
        console.error("注册失败:", error.message);
    });
```

### 图片批量加载

```js
function loadImage(src) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = () => reject(new Error(`图片加载失败: ${src}`));
        img.src = src;
    });
}

async function loadMultipleImages(imageUrls) {
    try {
        // 创建所有图片的 Promise
        const imagePromises = imageUrls.map(url => loadImage(url));

        // 使用 allSettled 确保所有图片都尝试加载
        const results = await Promise.allSettled(imagePromises);

        const loadedImages = [];
        const failedUrls = [];

        results.forEach((result, index) => {
            if (result.status === "fulfilled") {
                loadedImages.push(result.value);
            } else {
                failedUrls.push(imageUrls[index]);
                console.error(`图片 ${imageUrls[index]} 加载失败`);
            }
        });

        return {
            images: loadedImages,
            failedUrls,
            total: imageUrls.length,
            successCount: loadedImages.length,
        };
    } catch (error) {
        console.error("图片批量加载失败:", error);
        throw error;
    }
}
```

## 7. 常见陷阱和最佳实践

### 陷阱 1：忘记返回 Promise

```js
// 错误示例
somePromise()
    .then(value => {
        anotherPromise(value); // 忘记 return
    })
    .then(result => {
        // result 会是 undefined
    });

// 正确示例
somePromise()
    .then(value => {
        return anotherPromise(value); // 记得 return
    })
    .then(result => {
        // 正确接收结果
    });
```

### 陷阱 2：未捕获错误

```js
// 错误示例：错误被"吞掉"
somePromise().then(() => {
    throw new Error("错误被忽略了吗？");
});

// 正确示例：总是添加 catch
somePromise()
    .then(() => {
        throw new Error("错误被捕获");
    })
    .catch(error => {
        console.error("捕获到错误:", error);
    });
```

### 陷阱 3：Promise 嵌套

```js
// 反模式：Promise 地狱
getUser().then(user => {
    getPosts(user.id).then(posts => {
        getComments(posts[0].id).then(comments => {
            // 深度嵌套...
        });
    });
});

// 改进：使用链式调用
getUser()
    .then(user => getPosts(user.id))
    .then(posts => getComments(posts[0].id))
    .then(comments => {
        // 扁平的结构
    });
```

## 最佳实践

-   总是返回 Promise：在 then 回调中总是返回 Promise 或值
-   使用 catch 处理错误：每个 Promise 链都应该有错误处理
-   避免嵌套：使用链式调用而不是嵌套
-   使用 async/await：让异步代码看起来像同步代码
-   合理使用 Promise 静态方法：根据场景选择 all、race、any 等
-   考虑性能：合理使用并发（Promise.all）和顺序执行
