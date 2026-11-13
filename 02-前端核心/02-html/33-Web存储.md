# Web 存储

## 核心的 Web 存储技术对比

现代 Web 开发中，主要有以下几种客户端存储技术：

| 特性           | Cookie                                           | localStorage                         | sessionStorage                           | IndexedDB                                  |
| -------------- | ------------------------------------------------ | ------------------------------------ | ---------------------------------------- | ------------------------------------------ |
| 引入时间       | 早期 (HTTP 1.0)                                  | HTML5                                | HTML5                                    | HTML5                                      |
| 数据生命周期   | 可设置过期时间，否则随会话结束                   | 永久存储，除非手动清除               | 仅限当前会话，关闭标签页即清除           | 永久存储，除非手动清除                     |
| 存储容量       | 约 4KB                                           | 约 5MB (因浏览器而异)                | 约 5MB (因浏览器而异)                    | 巨大 (通常 ≥250MB，甚至更多)               |
| 与服务器的交互 | 每次都会在 HTTP 请求头（Cookie）中携带，影响性能 | 仅存储在客户端，不参与服务器通信     | 仅存储在客户端，不参与服务器通信         | 仅存储在客户端，不参与服务器通信           |
| 数据类型       | 字符串                                           | 字符串                               | 字符串                                   | 任何 JavaScript 类型（对象、数组、文件等） |
| API 易用性     | 简单，但需自行处理字符串                         | 非常简单的键值对 API                 | 非常简单的键值对 API                     | 复杂，基于事务的异步 API                   |
| 主要用途       | 会话管理、用户标识、个性化                       | 长期持久化数据（如用户偏好、购物车） | 临时会话数据（如表单内容、单次浏览信息） | 存储大量结构化数据、离线 Web 应用          |

## 详细解析

### Cookie

Cookie 是最早的客户端存储解决方案，最初设计用于在客户端存储会话标识符，以便服务器能够识别用户状态。

特点：

-   自动传输：浏览器会自动将匹配的 Cookie 添加到每一个发给该域名的 HTTP 请求的 Cookie 头中。
-   容量极小：4KB 的限制意味着它只能存储非常少量的信息，如用户 ID、Token 等。
-   可设置过期时间：通过 max-age 或 expires 属性控制。
-   有域和路径限制：只能被设置它的域名及其子域名（取决于路径）访问。

基本操作：<be>
原生 JavaScript 操作 Cookie 比较繁琐，通常使用库或框架来处理。

```js
// 设置 Cookie
document.cookie = "username=John Doe; max-age=3600; path=/";

// 读取 Cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}
console.log(getCookie("username")); // 输出 "John Doe"
```

### localStorage

特点：

-   仅限客户端：数据不会自动发送到服务器，节省了带宽。
-   简单的同步 API：操作是同步的，会阻塞主线程，但对于存储小数据影响不大。
-   同源策略：数据只能被同源（协议、域名、端口一致）的页面访问。
-   用于长期存储，数据没有过期时间，即使关闭浏览器再打开，数据依然存在。

基本操作：

```js
// 存储数据
localStorage.setItem("theme", "dark");
localStorage.setItem("user", JSON.stringify({ name: "Alice", id: 1 })); // 存对象需转成字符串

// 读取数据
const theme = localStorage.getItem("theme"); // 'dark'
const user = JSON.parse(localStorage.getItem("user")); // { name: 'Alice', id: 1 }

// 删除单个数据
localStorage.removeItem("theme");

// 清空所有数据
localStorage.clear();

// 获取键名
const key = localStorage.key(0); // 获取第一个键名
```

### sessionStorage

特点：

-   仅限客户端：数据不会自动发送到服务器，节省了带宽。
-   简单的同步 API：操作是同步的，会阻塞主线程，但对于存储小数据影响不大。
-   同源策略：数据只能被同源（协议、域名、端口一致）的页面访问。
-   用于一次会话的临时存储。（数据在页面会话结束时（关闭标签页或浏览器）被清除。即使是同一个网站的同一个页面，打开新标签页也会创建一个新的 sessionStorage）

API 与 localStorage 完全相同，只是对象名换成了 sessionStorage。

```js
// 存储数据
sessionStorage.setItem("theme", "dark");
sessionStorage.setItem("user", JSON.stringify({ name: "Alice", id: 1 })); // 存对象需转成字符串

// 读取数据
const theme = sessionStorage.getItem("theme"); // 'dark'
const user = JSON.parse(sessionStorage.getItem("user")); // { name: 'Alice', id: 1 }

// 删除单个数据
sessionStorage.removeItem("theme");

// 清空所有数据
sessionStorage.clear();

// 获取键名
const key = sessionStorage.key(0); // 获取第一个键名
```

### IndexedDB

当需要存储大量结构化数据（如客户记录、产品目录）或进行复杂查询时，localStorage 就力不从心了。这时需要使用 IndexedDB。

特点：

-   非关系型数据库：它是一个基于 JavaScript 的面向对象数据库。
-   异步操作：所有操作都是异步的，不会阻塞用户界面。
-   支持事务：保证数据操作的原子性和一致性。
-   存储量大：允许存储文件、Blob 等复杂数据类型。
-   API 复杂：相比于 Web Storage，其 API 更底层和复杂。

基本操作示例（打开数据库并添加数据）：

```js
// 打开或创建数据库
const request = indexedDB.open("MyTestDB", 1); // 数据库名，版本号

request.onerror = event => {
    console.error("为什么我的 IndexedDB 出错啦！", event);
};
request.onsuccess = event => {
    const db = event.target.result;
    console.log("数据库打开成功！");
    // 在这里执行数据库操作
};

// 如果数据库版本升级（或第一次创建），会触发 onupgradeneeded 事件
request.onupgradeneeded = event => {
    const db = event.target.result;
    // 创建一个对象存储空间（类似于 SQL 的表），并定义主键
    const objectStore = db.createObjectStore("customers", { keyPath: "id", autoIncrement: true });
    // 创建索引
    objectStore.createIndex("name", "name", { unique: false });
};

// 在 onsuccess 中，添加一条数据
function addCustomer(db, customer) {
    // 创建一个读写事务
    const transaction = db.transaction(["customers"], "readwrite");
    // 获取对象存储空间
    const objectStore = transaction.objectStore("customers");
    // 添加数据
    const request = objectStore.add(customer);
    request.onsuccess = event => {
        console.log("数据已添加，ID：", event.target.result);
    };
}
```

## 如何选择？

### 1. 数据是否需要随每个请求发送给服务器？
- 是 -> 使用 Cookie (例如：认证 Token)。
- 否 -> 进入下一步。

### 2. 需要存储的数据量是否很小（< 5MB），且只是简单的键值对？
- 是 -> 进入下一步。
- 否 -> 使用 IndexedDB (例如：离线应用、大量用户数据)。

### 3.是否需要永久存储，在多个标签页和浏览器会话间共享？
- 是 -> 使用 localStorage (例如：用户主题偏好、语言设置)。
- 否 -> 使用 sessionStorage (例如：单页表单的暂存、防止刷新丢失)。

## 总结

- Cookie：用于服务器通信，容量小。
- Web Storage (localStorage/sessionStorage)：简单键值对，容量中等，用于客户端状态持久化。
- IndexedDB：客户端 NoSQL 数据库，容量大，功能强，用于复杂的离线应用。
