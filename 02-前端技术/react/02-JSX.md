# JSX

JSX (JavaScript XML) 是 JavaScript 的语法扩展，允许在 JavaScript 中编写类似 HTML 的代码。

```js
// JSX 示例
const element = <h1>Hello, World!</h1>;
```

## JSX 基础语法

### 基本元素

```js
const element = <div>Hello React</div>;

const heading = <h1 className="title">Welcome</h1>;
```

### 嵌套元素

```js
const container = (
    <div>
        <h1>标题</h1>
        <p>段落内容</p>
        <ul>
            <li>项目1</li>
            <li>项目2</li>
        </ul>
    </div>
);
```

## JSX 中的 JavaScript 表达式

使用花括号 `{}` 嵌入 JavaScript 表达式：

```jsx
const name = "John";
const element = <h1>Hello, {name}!</h1>;

const user = {
    firstName: "张",
    lastName: "三",
};
const greeting = (
    <p>
        你好，{user.firstName}
        {user.lastName}
    </p>
);

// 表达式
const sum = <p>1 + 2 = {1 + 2}</p>;

// 函数调用
function formatName(user) {
    return `${user.firstName} ${user.lastName}`;
}
const formatted = <h2>{formatName(user)}</h2>;
```

## JSX 属性（Props）

### 字符串字面量

```jsx
const element = <div tabIndex="0"></div>;
const img = <img src="image.jpg" alt="描述" />;
```

### JavaScript 表达式

```jsx
const element = <img src={user.avatarUrl} />;
const isDisabled = true;
const button = <button disabled={isDisabled}>按钮</button>;
```

### 类名和样式

```jsx
// className 代替 class
const element = <div className="container active"></div>;

// style 接受对象
const style = {
    color: "red",
    backgroundColor: "yellow",
    fontSize: "20px", // 驼峰命名
};
const styledDiv = <div style={style}>样式文本</div>;

// 内联样式
const inlineElement = (
    <div
        style={{
            padding: "10px",
            margin: "20px",
            border: "1px solid #ccc",
        }}
    >
        内容
    </div>
);
```

## JSX 子元素

### 字符串子元素

```jsx
const element = <p>这是一个段落</p>;
```

### 嵌套元素

```js
const element = (
    <div>
        <h1>标题</h1>
        <p>段落</p>
    </div>
);
```

### 表达式作为子元素

```js
const element = <div>{"Hello " + "World"}</div>;
const today = <p>今天是：{new Date().toLocaleDateString()}</p>;
```

### 组件作为子元素

```js
function Welcome(props) {
    return <h1>Hello, {props.name}</h1>;
}

const app = (
    <div>
        <Welcome name="Alice" />
        <Welcome name="Bob" />
    </div>
);
```

## JSX 防止注入攻击

JSX 会自动转义内容，防止 XSS 攻击：

```jsx
const userInput = '<script>alert("xss")</script>';
const safeElement = <div>{userInput}</div>; // 会被转义，安全

// 如果需要渲染 HTML，使用 dangerouslySetInnerHTML
const dangerousHTML = { __html: "<b>加粗文本</b>" };
const dangerousElement = <div dangerouslySetInnerHTML={dangerousHTML} />;
```

## JSX 的特殊属性

```jsx
// htmlFor 代替 for
const label = <label htmlFor="name">姓名</label>;

// 事件处理（驼峰命名）
const button = <button onClick={handleClick}>点击</button>;

// 自定义属性（data-*）
const element = <div data-testid="test-element"></div>;

// 布尔属性
const input = <input type="checkbox" checked={true} readOnly />;
```

## 条件渲染

### if 语句

```jsx
function Greeting(props) {
    if (props.isLoggedIn) {
        return <h1>欢迎回来！</h1>;
    }
    return <h1>请先登录</h1>;
}
```

### 三元运算符

```jsx
const element = <div>{isLoggedIn ? <LogoutButton /> : <LoginButton />}</div>;
```

### 逻辑与运算符 (&&)

```jsx
const element = (
    <div>{unreadMessages.length > 0 && <h2>您有 {unreadMessages.length} 条未读消息</h2>}</div>
);
```

### 立即执行函数

```jsx
const element = (
    <div>
        {(() => {
            switch (status) {
                case "loading":
                    return <Spinner />;
                case "error":
                    return <Error />;
                default:
                    return <Content />;
            }
        })()}
    </div>
);
```

## 列表渲染

### map() 方法

```jsx
const numbers = [1, 2, 3, 4, 5];
const listItems = numbers.map(number => <li key={number.toString()}>{number}</li>);

const element = <ul>{listItems}</ul>;
```

### 复杂列表

```jsx
const products = [
    { id: 1, name: "iPhone", price: 6999 },
    { id: 2, name: "iPad", price: 2999 },
    { id: 3, name: "MacBook", price: 12999 },
];

const productList = (
    <ul>
        {products.map(product => (
            <li key={product.id}>
                {product.name} - ¥{product.price}
            </li>
        ))}
    </ul>
);
```

### 使用 Fragment 避免额外包裹

```js
import React, { Fragment } from "react";

const items = ["A", "B", "C"];
const list = (
    <Fragment>
        {items.map((item, index) => (
            <Fragment key={index}>
                <span>{item}</span>
                <br />
            </Fragment>
        ))}
    </Fragment>
);
```

## JSX 的本质

JSX 会被 Babel 转译为 React.createElement() 调用：

```jsx
// JSX
const element = <h1 className="greeting">Hello, world!</h1>;

// 转译后的 JavaScript
const element = React.createElement("h1", { className: "greeting" }, "Hello, world!");

// 最终创建的对象
const element = {
    type: "h1",
    props: {
        className: "greeting",
        children: "Hello, world!",
    },
};
```

## JSX 的 Fragment

用于返回多个元素而不添加额外 DOM 节点：

```jsx
import React, { Fragment } from "react";

// 方式1：使用 Fragment
function Component() {
    return (
        <Fragment>
            <td>单元格1</td>
            <td>单元格2</td>
        </Fragment>
    );
}

// 方式2：使用简写语法
function Component() {
    return (
        <>
            <td>单元格1</td>
            <td>单元格2</td>
        </>
    );
}
```

## JSX 注意事项

### 1. 必须有一个根元素

```jsx
// ❌ 错误
const element = (
  <h1>标题</h1>
  <p>内容</p>
);

// ✅ 正确
const element = (
  <div>
    <h1>标题</h1>
    <p>内容</p>
  </div>
);
```

### 2. 标签必须闭合

```jsx
// ❌ 错误
const img = <img src="...">
const input = <input type="text">

// ✅ 正确
const img = <img src="..." />;
const input = <input type="text" />;
```

### 3. 属性名使用驼峰命名

```jsx
// ❌ 错误
const div = <div class="container" tabindex="0"></div>;

// ✅ 正确
const div = <div className="container" tabIndex="0"></div>;
```

### 4. 保留关键字

```js
// ❌ 错误
const element = <div class="container"> // class 是 JavaScript 关键字

// ✅ 正确
const element = <div className="container"> // 使用 className
```

## JSX 实用技巧

### 条件属性

```jsx
const inputProps = {
    type: "text",
    value: username,
    ...(isRequired && { required: true }),
    ...(isDisabled && { disabled: true }),
};

const input = <input {...inputProps} />;
```

### 展开属性

```js
const props = {
    className: "container",
    id: "main",
};

const element = <div {...props}>内容</div>;
```

### 渲染函数/组件

```jsx
function renderContent(type) {
    const components = {
        text: () => <p>文本内容</p>,
        image: () => <img src="image.jpg" alt="" />,
        video: () => <video src="video.mp4" controls />,
    };

    return components[type] ? components[type]() : null;
}

const element = <div>{renderContent("image")}</div>;
```

### JSX 与 TypeScript

```js
// 定义 Props 类型
interface ButtonProps {
    text: string;
    onClick: () => void;
    disabled?: boolean; // 可选属性
}

const Button: React.FC<ButtonProps> = ({ text, onClick, disabled = false }) => (
    <button onClick={onClick} disabled={disabled}>
        {text}
    </button>
);

// 使用泛型组件
interface ListProps<T> {
    items: T[];
    renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
    return (
        <ul>
            {items.map((item, index) => (
                <li key={index}>{renderItem(item)}</li>
            ))}
        </ul>
    );
}
```
