# React面试

## 菜单
1. 基础知识
JSX：理解JSX语法及其与JavaScript的关系。

组件：掌握函数组件和类组件的编写与区别。

Props和State：熟悉Props和State的使用及其区别。

生命周期方法：了解类组件的生命周期方法，如componentDidMount、componentDidUpdate等。

Hooks：掌握常用Hooks，如useState、useEffect、useContext等。

2. 核心概念
虚拟DOM：理解虚拟DOM的工作原理及其优势。

组件通信：掌握父子组件、兄弟组件之间的通信方式。

条件渲染：熟悉条件渲染的实现方法。

列表和Keys：了解如何渲染列表及Keys的作用。

3. 高级特性
Context API：掌握Context API的使用场景及实现。

Refs：了解Refs的使用及其适用场景。

高阶组件（HOC）：理解HOC的概念及应用。

Render Props：熟悉Render Props模式及其使用。

4. 状态管理
Redux：掌握Redux的核心概念，如Store、Action、Reducer等。

MobX：了解MobX的基本用法。

React状态管理库：熟悉如Recoil、Zustand等现代状态管理工具。

5. 性能优化
React.memo：掌握React.memo的使用及其优化效果。

useMemo和useCallback：理解useMemo和useCallback的作用及使用场景。

懒加载：熟悉React.lazy和Suspense实现组件懒加载。

6. 路由
React Router：掌握React Router的基本用法，如路由配置、嵌套路由等。

7. 测试
单元测试：熟悉使用Jest和React Testing Library进行单元测试。

端到端测试：了解Cypress等工具进行端到端测试。

8. 项目经验
项目准备：回顾并总结自己做过的React项目，准备介绍项目背景、技术栈及解决方案。

问题解决：准备项目中遇到的挑战及解决方法。

9. 编码练习
LeetCode/CodeSandbox：通过LeetCode或CodeSandbox练习React相关题目，熟悉常见问题及解决方案。

10. 面试题准备
常见问题：准备常见React面试题，如虚拟DOM、Hooks、组件通信等。

行为问题：准备行为面试问题，如团队合作、问题解决等。

11. 最新动态
React最新特性：关注React的最新版本及特性，如并发模式、Server Components等。

## 理解JSX语法及其与JavaScript的关系。

JSX 是一种语法糖，它允许你在 JavaScript 中直接编写类似 HTML 的代码。
JSX 并不是直接由浏览器执行的，它需要通过工具（如 Babel）编译成标准的 JavaScript 代码。编译后的 JSX 会变成 React.createElement() 的调用。

###  JSX 的特点

1. 嵌入表达式：可以使用花括号 {} 嵌入任何 JavaScript 表达式
2. JSX 中的属性使用驼峰命名法（camelCase）
3. 自闭合标签：JSX 支持自闭合标签，例如 <img />、<input />
4. 多行 JSX：如果 JSX 跨越多行，建议用括号 () 包裹，以避免自动分号插入的问题
5. JSX 是一个表达式： JSX 本身是一个表达式，编译后会返回一个 JavaScript 对象。因此，你可以将 JSX 赋值给变量、作为函数返回值，或在条件语句中使用。

### JSX 的本质

JSX 的本质是 React.createElement() 的语法糖。它的作用是让开发者以更直观的方式描述 UI 结构，而不需要手动编写繁琐的 React.createElement() 调用。

### JSX 的限制

1. 必须有一个根元素。在 React 16 及以上版本中，可以使用 Fragment 来避免额外的 DOM 元素
2. 属性名不能使用 JavaScript 保留字

### 为什么使用 JSX？

直观性：JSX 的语法类似 HTML，更容易理解和编写。
表达能力：JSX 允许嵌入 JavaScript 表达式，使得动态内容的生成更加方便。
类型安全：结合 TypeScript 使用时，JSX 可以提供更好的类型检查。

### JSX 的编译工具

Babel 的 @babel/preset-react 插件负责将 JSX 转换为 React.createElement() 调用。

## 熟悉条件渲染的实现方法

1. 使用 if 语句
2. 使用三元运算符 (? :)
3. 使用逻辑与运算符 (&&)
4. 使用 switch 语句
5. 使用变量存储 JSX
6. 使用立即执行函数 (IIFE)
7. 使用高阶组件 (HOC)
8. 使用 React.Fragment 包裹多个条件渲染。适用场景：当需要返回多个并列的元素时。、
9. 使用 children 属性

## 了解如何渲染列表及Keys的作用

渲染列表：
> 通过 map() 方法将数组数据映射为 JSX 元素列表。

Keys 的作用：
> Keys 是 React 用于识别列表中每个元素的唯一标识符

（1）帮助 React 识别元素的变化
（2）提高性能
（3）避免渲染错误

如何选择 Key:
1. 唯一性：Key 应该在列表中唯一，通常使用数据的唯一标识符（如 id）。
2. 稳定性：Key 不应该随时间或渲染顺序变化。

## 掌握Context API的使用场景及实现

Context API 是 React 提供的一种跨组件传递数据的机制，用于解决组件树中多层组件之间共享数据的繁琐问题。它适用于全局数据（如主题、用户信息、语言偏好等）的传递，避免了通过 props 逐层传递的麻烦。

### Context API 的使用场景

主题切换：在应用中实现深色模式/浅色模式的切换。

用户信息：在多个组件中共享当前登录用户的信息。

语言偏好：实现多语言支持。

全局状态管理：替代简单的 Redux 场景，避免引入额外的状态管理库。

## 了解Refs的使用及其适用场景

Refs 是 React 提供的一种访问 DOM 元素或组件实例的方式。它们通常用于直接操作 DOM 或存储可变值，而不触发组件的重新渲染。

Refs 的适用场景

1. 访问 DOM 元素
2. Refs 可以存储可变值，且不会触发组件的重新渲染。
3. 访问子组件的实例
4. 集成第三方 DOM 库

forwardRef：转发 Refs
> 如果需要在函数组件中访问子组件的 DOM 元素，可以使用 forwardRef。

## 理解HOC的概念及应用

高阶组件（Higher-Order Component，HOC） 是 React 中用于复用组件逻辑的一种高级技术。HOC 是一个函数，它接收一个组件并返回一个新的组件。通过 HOC，可以将通用的逻辑抽象出来，应用到多个组件中。

HOC 的常见应用场景

1. 数据获取: 通过 HOC 封装数据获取逻辑，避免在每个组件中重复编写相同的代码。
2. 权限校验: 通过 HOC 封装权限校验逻辑，确保只有具备权限的用户才能访问某些组件。
3. 日志记录: 通过 HOC 封装日志记录逻辑，记录组件的生命周期事件或用户交互。

## 熟悉Render Props模式及其使用

Render Props 是 React 中一种复用组件逻辑的模式。它的核心思想是通过一个函数 prop（通常命名为 render 或 children）将组件的渲染逻辑交给父组件控制。Render Props 模式可以替代高阶组件（HOC），在某些场景下更具灵活性和可读性。

<!-- 使用 render prop -->
```jsx
class MouseTracker extends React.Component {
  state = { x: 0, y: 0 };

  handleMouseMove = (event) => {
    this.setState({ x: event.clientX, y: event.clientY });
  };

  render() {
    return (
      <div style={{ height: '100vh' }} onMouseMove={this.handleMouseMove}>
        {this.props.render(this.state)}
      </div>
    );
  }
}

// 使用 Render Props
function App() {
  return (
    <MouseTracker
      render={({ x, y }) => (
        <div>
          <h1>Move the mouse around!</h1>
          <p>
            The current mouse position is ({x}, {y})
          </p>
        </div>
      )}
    />
  );
}
```

<!-- 使用 children prop -->
```jsx
class MouseTracker extends React.Component {
  state = { x: 0, y: 0 };

  handleMouseMove = (event) => {
    this.setState({ x: event.clientX, y: event.clientY });
  };

  render() {
    return (
      <div style={{ height: '100vh' }} onMouseMove={this.handleMouseMove}>
        {this.props.children(this.state)}
      </div>
    );
  }
}

// 使用 Render Props
function App() {
  return (
    <MouseTracker>
      {({ x, y }) => (
        <div>
          <h1>Move the mouse around!</h1>
          <p>
            The current mouse position is ({x}, {y})
          </p>
        </div>
      )}
    </MouseTracker>
  );
}
```

### 常用逻辑

1. 数据获取
2. 表单管理
3. 复用逻辑

### Render Props 与 HOC 的对比

Render Props：通过函数 prop 将渲染逻辑交给父组件，更灵活。

HOC：通过函数包装组件，复用逻辑，但可能导致命名冲突和静态方法丢失。

## 掌握Redux的核心概念，如Store、Action、Reducer等。

### Store

定义：Store 是 Redux 中存储应用状态的地方。

特点：
1. 整个应用只有一个 Store。
2. Store 是不可变的，只能通过 Action 和 Reducer 更新。

创建 Store：使用 createStore 函数创建 Store。

```js
import { createStore } from 'redux';

const store = createStore(rootReducer);
```

### Action

定义：Action 是一个普通的 JavaScript 对象，用于描述状态的变化。

结构：
1. type：表示 Action 的类型（通常是字符串常量）。
2. payload：携带的数据（可选）。

创建 Action：通常通过 Action 创建函数（Action Creator）生成。

```js
// Action 类型
const ADD_TODO = 'ADD_TODO';

// Action 创建函数
function addTodo(text) {
  return {
    type: ADD_TODO,
    payload: text,
  };
}
```

### Reducer
定义：Reducer 是一个纯函数，用于根据 Action 更新状态。

特点：

1. 接收当前状态和 Action 作为参数。
2. 返回新的状态（不能直接修改原状态）。

创建 Reducer：通常使用 switch 语句处理不同的 Action 类型。

```js
const initialState = {
  todos: [],
};

function todoReducer(state = initialState, action) {
  switch (action.type) {
    case 'ADD_TODO':
      return {
        ...state,
        todos: [...state.todos, action.payload],
      };
    default:
      return state;
  }
}
```

### Dispatch

定义：Dispatch 是 Store 的一个方法，用于发送 Action。

作用：触发状态更新。

```js
store.dispatch(addTodo('Learn Redux'));
```

### Redux 的工作流程
触发 Action：通过 dispatch 方法发送一个 Action。

调用 Reducer：Store 调用 Reducer，传入当前状态和 Action。

更新状态：Reducer 根据 Action 返回新的状态。

通知订阅者：Store 更新状态后，通知所有订阅了 Store 的组件。

### Redux 的使用步骤

1. 安装 Redux

2. 创建 Action 和 Reducer
```js
// Action 类型
const ADD_TODO = 'ADD_TODO';

// Action 创建函数
function addTodo(text) {
  return {
    type: ADD_TODO,
    payload: text,
  };
}

// Reducer
const initialState = {
  todos: [],
};

function todoReducer(state = initialState, action) {
  switch (action.type) {
    case ADD_TODO:
      return {
        ...state,
        todos: [...state.todos, action.payload],
      };
    default:
      return state;
  }
}
```

3. 创建 Store
```js
import { createStore } from 'redux';

const store = createStore(todoReducer);
```

4. 订阅store
```js
store.subscribe(() => {
  console.log('State updated:', store.getState());
});
```

5. 触发 Action
```js
store.dispatch(addTodo('Learn Redux'));
store.dispatch(addTodo('Build a project'));
```

###  Redux 的中间件

1. redux-thunk: 用于处理异步 Action
2. redux-logger: 用于记录 Redux 状态变化的中间件

### Redux 与 React 的结合

1. 安装 react-redux

2. 使用 Provider: Provider 是一个组件，用于将 Store 传递给整个应用。

3. 使用 useSelector 和 useDispatch
> useSelector 用于从 Store 中获取状态，useDispatch 用于发送 Action。

```js
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';

function TodoApp() {
  const todos = useSelector((state) => state.todos);
  const dispatch = useDispatch();

  return (
    <div>
      <ul>
        {todos.map((todo, index) => (
          <li key={index}>{todo}</li>
        ))}
      </ul>
      <button onClick={() => dispatch(addTodo('New Todo'))}>Add Todo</button>
    </div>
  );
}
```

## redux toolkit

Redux Toolkit（RTK） 是 Redux 官方推荐的工具集，旨在简化 Redux 的使用。

### Redux Toolkit 的核心概念

configureStore：简化 Store 的创建。

createSlice：自动生成 Action 和 Reducer。

createAsyncThunk：处理异步操作。

createEntityAdapter：管理标准化状态。

### Redux Toolkit 的使用步骤

1. 安装 Redux Toolkit

2. 创建 Slice: createSlice 用于定义 Reducer 和 Action。
```js
import { createSlice } from '@reduxjs/toolkit';

const todoSlice = createSlice({
  name: 'todos', // Slice 的名称
  initialState: [], // 初始状态
  reducers: {
    addTodo: (state, action) => {
      state.push(action.payload); // 直接修改状态（Immer 支持）
    },
    removeTodo: (state, action) => {
      return state.filter((todo) => todo.id !== action.payload);
    },
  },
});

// 导出 Action 创建函数
export const { addTodo, removeTodo } = todoSlice.actions;

// 导出 Reducer
export default todoSlice.reducer;
```

3. 创建 Store: 使用 configureStore 创建 Store。
```js
import { configureStore } from '@reduxjs/toolkit';
import todoReducer from './todoSlice';

const store = configureStore({
  reducer: {
    todos: todoReducer,
  },
});

export default store;
```

4. 在 React 中使用

使用 react-redux 的 Provider、useSelector 和 useDispatch。

### 处理异步操作

使用 createAsyncThunk 处理异步操作。

### 管理标准化状态

使用 createEntityAdapter 管理标准化状态（如列表数据）。

## 熟悉React.lazy和Suspense实现组件懒加载

React.lazy 和 Suspense 是 React 提供的用于实现组件懒加载（Lazy Loading）的功能。懒加载可以帮助减少应用的初始加载时间，只有在需要时才加载某些组件，从而提升性能。

### React.lazy 和 Suspense 的概念

React.lazy：用于动态加载组件。
Suspense：用于在组件加载过程中显示加载指示器（如加载动画）。

### 实现组件懒加载的步骤

（1）使用 React.lazy 动态加载组件
React.lazy 接收一个返回 import() 的函数，动态加载组件。
```js
const LazyComponent = React.lazy(() => import('./LazyComponent'));
```

（2）使用 Suspense 包裹懒加载组件
Suspense 组件用于在懒加载组件加载过程中显示回退内容（如加载动画）。
```js
import React, { Suspense } from 'react';

const LazyComponent = React.lazy(() => import('./LazyComponent'));

function App() {
  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}>
        <LazyComponent />
      </Suspense>
    </div>
  );
}
```

## 掌握React Router的基本用法，如路由配置、嵌套路由等

### 基本路由配置

使用 BrowserRouter、Routes 和 Route 组件配置路由。

```js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

function Home() {
  return <div>Home Page</div>;
}

function About() {
  return <div>About Page</div>;
}

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
}

export default App;
```

### 嵌套路由

```js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Outlet } from 'react-router-dom';

function Home() {
  return <div>Home Page</div>;
}

function About() {
  return (
    <div>
      <h1>About Page</h1>
      <nav>
        <Link to="team">Team</Link>
        <Link to="history">History</Link>
      </nav>
      <Outlet /> {/* 子路由的渲染位置 */}
    </div>
  );
}

function Team() {
  return <div>Team Page</div>;
}

function History() {
  return <div>History Page</div>;
}

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />}>
          <Route path="team" element={<Team />} />
          <Route path="history" element={<History />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
```

### 动态路由
```js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useParams } from 'react-router-dom';

function User() {
  const { userId } = useParams(); // 获取动态路由参数
  return <div>User ID: {userId}</div>;
}

function App() {
  return (
    <Router>
      <nav>
        <Link to="/user/1">User 1</Link>
        <Link to="/user/2">User 2</Link>
      </nav>
      <Routes>
        <Route path="/user/:userId" element={<User />} />
      </Routes>
    </Router>
  );
}

export default App;
```

### 重定向
```js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

function Home() {
  return <div>Home Page</div>;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/old-path" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
```

### 编程式导航

使用 useNavigate Hook 实现编程式导航。

```js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  const goToAbout = () => {
    navigate('/about');
  };

  return (
    <div>
      <h1>Home Page</h1>
      <button onClick={goToAbout}>Go to About</button>
    </div>
  );
}

function About() {
  return <div>About Page</div>;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
}

export default App;
```