# RN面试

## React 组件的生命周期（如useEffect、componentDidMount等）

### 类组件的生命周期

- 初始化阶段：
    - constructor()，组件的构造函数，用于初始化组件的状态和绑定事件处理函数。
    - static getDerivedStateFromProps(),在组件实例化或接受到新的Props时调用，用于根据props更新state。
- 挂载阶段
    - render:渲染组件的UI。纯函数，不应该在这里执行副作用操作。
    - componentDidMount：组件挂载到DOM后调用。通常用于执行副作用操作。如数据获取、订阅事件等。
- 更新阶段：
    - static getDerivedStateFromProps: 在组件接收到新的props或state时调用，用于根据新的props或state更新组件的状态。
    - shouldComponentUpdate: 决定组件是否需要重新渲染。可以通过返回false来阻止不必要的渲染，优化性能。
    - render：重新渲染zujianUI。
    - getSnapshotBeforeUpdate: 在DOM更新之前调用，用于捕获更新前的DOM状态（如滚动位置）。
    - componentDidUpdate: 组件更新完成后调用，通常用于执行DOM操作或网络请求
- 卸载阶段：
    - componentWillUnmount：组件从DOM中卸载之前调用，用于清理操作，如取消网络请求，移除事件监听器等。
- 错误处理阶段：
    - static getDerivedStateFromError: 在子组件抛出错误时调用，用于更新state以显示错误信息
    - componentDidCatch: 在子组件抛出错误时调用，用于记录错误信息或执行副作用操作

### 函数组件的生命周期

React 16.8引入Hooks

- useEffect: 用于处理副作用，可以模拟componentDidMount/componentDidUpdate/componentWillUnmont
- useState: 用于管理组件的状态；
- useContext: 用于访问上下文；
- useMemo和UseCallback：用于优化性能

### RN生命周期

#### useContext使用示例：
<!-- MyContext.js -->
```jsx
import React from 'react';

// 创建 Context 对象
const MyContext = React.createContext();

export default MyContext;
```

<!-- App.js -->
```jsx
import React, { useState } from 'react';
import MyContext from './MyContext'; // 导入 Context
import ChildComponent from './ChildComponent'; // 导入子组件

function App() {
  const [user, setUser] = useState({ name: 'John', age: 30 });

  // 更新用户信息的函数
  const updateUser = () => {
    setUser({ name: 'Jane', age: 25 });
  };

  return (
    // 使用 Provider 提供 Context 的值
    <MyContext.Provider value={{ user, updateUser }}>
      <div>
        <h1>App Component</h1>
        <ChildComponent />
      </div>
    </MyContext.Provider>
  );
}

export default App;

```

<!-- ChildComponent.js -->
```jsx
import React, { useContext } from 'react';
import MyContext from './MyContext'; // 导入 Context

function ChildComponent() {
  // 使用 useContext 获取 Context 的值
  const { user, updateUser } = useContext(MyContext);

  return (
    <div>
      <h2>Child Component</h2>
      <p>Name: {user.name}</p>
      <p>Age: {user.age}</p>
      <button onClick={updateUser}>Update User</button>
    </div>
  );
}

export default ChildComponent;
```

#### useMemo和UseCallback的区别

`useMemo` 用于缓存计算结果，避免在每次渲染时都重新计算。它适用于需要复杂计算的场景。
```jsx
/**
 * 语法
 * 参数1：函数，返回需要缓存的值
 * 参数2：依赖项数组
 */
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
```

`useCallback` 用于缓存函数引用，避免在每次渲染时都创建新的函数。它适用于将函数作为 props 传递给子组件的场景。
```jsx
/**
 * 语法
 * 参数1：函数，返回需要缓存的函数
 * 参数2：依赖项数组
 */
const memoizedCallback = useCallback(() => {
  doSomething(a, b);
}, [a, b]);
```

<!-- 综合示例 -->
```jsx
import React, { useState, useMemo, useCallback } from 'react';

function App() {
  const [count, setCount] = useState(0);
  const [inputValue, setInputValue] = useState('');

  // 缓存计算结果
  const doubledCount = useMemo(() => {
    console.log('Calculating doubledCount...');
    return count * 2;
  }, [count]);

  // 缓存函数引用
  const increment = useCallback(() => {
    setCount(count + 1);
  }, [count]);

  return (
    <div>
      <p>Count: {count}</p>
      <p>Doubled Count: {doubledCount}</p>
      <button onClick={increment}>Increment</button>
      <input
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Type something..."
      />
    </div>
  );
}

export default App;
```

## 状态管理（State）和属性传递（Props）

### 状态管理（State）

> State 是组件内部管理的可变数据。它用于存储组件的动态信息，这些信息可能会随着时间的推移而改变。
> State 是私有的，只能由组件自身修改（通过 setState 或 useState）。

使用场景：
> 存储组件的动态数据（如表单输入、计数器、开关状态等）。
> 当数据变化需要触发组件重新渲染时。

使用：
```jsx
// 类组件
 constructor(props) {
    super(props);
    this.state = { count: 0 }; // 初始化状态
}
this.setState({ count: this.state.count + 1 }); // 更新状态
```
```jsx
// 函数组件
const [count, setCount] = useState(0); // 初始化状态

setCount(count + 1); // 更新状态
```
### 属性传递（Props）

> Props 是组件的输入参数，用于从父组件向子组件传递数据。
> Props 是只读的，子组件不能直接修改 Props。

使用场景：
> 在组件之间传递数据（如配置、事件处理函数等）。
> 当父组件需要控制子组件的行为或显示内容时。

## React 组件间通信

### 父组件 -> 子组件

通过Props传递

### 子组件 -> 父组件

通过回调函数

### 兄弟组件通信

兄弟组件之间没有直接的通信方式，需要通过共同的父组件来实现。

实现步骤：
> 将共享状态提升到父组件。
> 父组件通过 Props 将状态和更新状态的函数分别传递给两个子组件。

### 跨层级组件通信

当组件层级较深时，通过 Props 逐层传递数据会变得繁琐。可以使用 Context API 或 状态管理库（如 Redux、MobX）来实现跨层级组件通信。

### 全局状态管理

如 Redux、MobX、Recoil

```shell
npm install @reduxjs/toolkit react-redux
```
```jsx
// 创建store
import { configureStore, createSlice } from '@reduxjs/toolkit';

const dataSlice = createSlice({
  name: 'data',
  initialState: { value: '' },
  reducers: {
    setData: (state, action) => {
      state.value = action.payload;
    },
  },
});

const store = configureStore({
  reducer: {
    data: dataSlice.reducer,
  },
});

export const { setData } = dataSlice.actions;
export default store;
```
```jsx
// 组件中使用
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setData } from './store';

function ChildA() {
  const dispatch = useDispatch();

  const sendData = () => {
    dispatch(setData("Hello from Child A!"));
  };

  return <button onClick={sendData}>Send Data to Child B</button>;
}

function ChildB() {
  const data = useSelector((state) => state.data.value);

  return <p>Data from Child A: {data}</p>;
}

function ParentComponent() {
  return (
    <div>
      <ChildA />
      <ChildB />
    </div>
  );
}

export default ParentComponent;
```

### 事件总线（Event Bus）

事件总线是一种发布-订阅模式，适用于任意组件间的通信。可以通过第三方库（如 mitt）或自定义实现。

```shell
npm install mitt
```

```jsx
// 创建事件总线
import mitt from 'mitt';

const emitter = mitt();
export default emitter;
```

```jsx
// 在组件中使用
import React, { useEffect, useState } from 'react';
import emitter from './eventBus';

function ChildA() {
  const sendData = () => {
    emitter.emit('sendData', "Hello from Child A!");
  };

  return <button onClick={sendData}>Send Data to Child B</button>;
}

function ChildB() {
  const [data, setData] = useState("");

  useEffect(() => {
    const handler = (payload) => {
      setData(payload);
    };
    emitter.on('sendData', handler);

    return () => {
      emitter.off('sendData', handler);
    };
  }, []);

  return <p>Data from Child A: {data}</p>;
}

function ParentComponent() {
  return (
    <div>
      <ChildA />
      <ChildB />
    </div>
  );
}

export default ParentComponent;
```

## React 事件处理

### 基本事件处理

onClick、onChange

### 事件对象

React 的事件处理函数会接收一个合成事件对象（SyntheticEvent），它是浏览器原生事件的跨浏览器包装器。

### 传递参数

如果需要将额外参数传递给事件处理函数，可以使用箭头函数或 bind 方法。

### 手势事件

React 支持常见的手势事件，例如 onTouchStart、onTouchMove、onTouchEnd 等。
```jsx
function TouchArea() {
  const handleTouchStart = (event) => {
    console.log('Touch started:', event.touches);
  };

  const handleTouchEnd = (event) => {
    console.log('Touch ended:', event.touches);
  };

  return (
    <div
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      style={{ width: '100px', height: '100px', backgroundColor: 'lightblue' }}
    >
      Touch Me
    </div>
  );
}
```

### 自定义事件

React 支持自定义事件，可以通过 CustomEvent 或第三方库（如 EventEmitter）实现。

```jsx
function CustomEventExample() {
  const handleCustomEvent = (event) => {
    console.log('Custom event triggered:', event.detail);
  };

  useEffect(() => {
    const element = document.getElementById('custom-event-element');
    element.addEventListener('customEvent', handleCustomEvent);

    return () => {
      element.removeEventListener('customEvent', handleCustomEvent);
    };
  }, []);

  const triggerEvent = () => {
    const event = new CustomEvent('customEvent', { detail: { message: 'Hello!' } });
    const element = document.getElementById('custom-event-element');
    element.dispatchEvent(event);
  };

  return (
    <div>
      <div id="custom-event-element">Custom Event Element</div>
      <button onClick={triggerEvent}>Trigger Custom Event</button>
    </div>
  );
}
```

### 事件委托

React 默认使用事件委托机制，将所有事件绑定到根节点（root）上，而不是直接绑定到每个 DOM 元素。这可以提高性能并简化事件管理。

```jsx
function EventDelegation() {
  const handleClick = (event) => {
    if (event.target.tagName === 'BUTTON') {
      console.log('Button clicked:', event.target.textContent);
    }
  };

  return (
    <div onClick={handleClick}>
      <button>Button 1</button>
      <button>Button 2</button>
    </div>
  );
}
```

### 阻止默认行为和事件冒泡

可以通过事件对象的方法来阻止默认行为或事件冒泡。

```jsx
function Form() {
  const handleSubmit = (event) => {
    event.preventDefault(); // 阻止表单提交
    console.log('Form submitted');
  };

  const handleClick = (event) => {
    event.stopPropagation(); // 阻止事件冒泡
    console.log('Button clicked');
  };

  return (
    <form onSubmit={handleSubmit}>
      <button onClick={handleClick}>Submit</button>
    </form>
  );
}
```

## React Native和React的区别？

React Native 和 React 都是由 Facebook 开发的开源框架，但它们的目标平台和使用场景有所不同。

### 目标平台

react:
    用于构建 Web 应用。
    运行在浏览器环境中，生成的是标准的 HTML、CSS 和 JavaScript。
    适用于开发单页应用（SPA）或多页应用。
RN:
    用于构建 原生移动应用（iOS 和 Android）。
    运行在移动设备的原生环境中，生成的是原生组件（如 View、Text、Image 等）。
    适用于开发跨平台移动应用。

### 渲染机制

react:
    使用 虚拟 DOM 来高效地更新和渲染 Web 页面。
    最终渲染为浏览器可识别的 HTML 元素（如 <div>、<p> 等）。
RN:
    使用 原生组件 而不是 HTML 元素。
    通过 JavaScript 线程与原生线程通信，最终渲染为平台特定的原生 UI 组件（如 iOS 的 UIView 或 Android 的 View）。

### 组件和 API

react:
    使用标准的 Web 组件（如 <div>、<span>、<img> 等）。
    依赖于浏览器的 API（如 document、window 等）。
RN:
    使用专为移动端设计的组件（如 <View>、<Text>、<Image> 等）。
    提供移动端特有的 API（如访问相机、地理位置、设备传感器等）。

### 样式

react:
    使用 CSS 或 CSS-in-JS 来定义样式。
    支持所有标准的 CSS 特性（如伪类、媒体查询等）。
RN:
    使用 JavaScript 对象 来定义样式（类似于内联样式）。
    不支持所有 CSS 特性（如伪类、动画等），但有专门的 API 实现类似功能（如 StyleSheet、Animated）。

### 开发工具

react:
    使用浏览器的开发者工具（如 Chrome DevTools）进行调试。
    支持热重载（Hot Reloading）和快速刷新（Fast Refresh）。
RN:
    使用 React Native 自带的调试工具（如 React Native Debugger）。
    支持热重载和快速刷新。
    需要安装平台特定的开发工具（如 Xcode 或 Android Studio）。

### 生态系统

react:
    拥有庞大的 Web 开发生态系统（如 React Router、Redux、Next.js 等）。
    支持大量的第三方库和工具。
RN:
    拥有专门为移动端设计的生态系统（如 React Navigation、React Native Paper 等）。
    支持访问原生模块和 API，但部分 Web 库可能不兼容。

### 性能

react:
    性能依赖于浏览器的渲染引擎。
    虚拟 DOM 可以有效减少页面重绘，但在复杂应用中仍可能遇到性能瓶颈。
RN:
    性能接近原生应用，因为最终渲染的是原生组件。
    通过 JavaScript 线程与原生线程通信，可能会在某些场景下出现性能问题（如大量动画或复杂计算）。

### 代码复用

react:
    代码仅适用于 Web 平台。
    无法直接复用到移动端。
RN:
    代码可以在 iOS 和 Android 平台上复用。
    通过 React Native for Web 等工具，部分代码可以复用到 Web 平台。

### 适用场景

react:
    适用于构建 Web 应用、管理后台、静态网站等。
    适合需要快速迭代和跨浏览器兼容的项目。
RN:
    适用于构建跨平台移动应用。
    适合需要接近原生性能但又希望共享代码库的项目。

## 什么是虚拟DOM？

虚拟 DOM（Virtual DOM） 是 React 的核心概念之一，它是一种用于提高 Web 应用性能的技术。虚拟 DOM 通过在内存中维护一个轻量级的 DOM 副本，来减少直接操作真实 DOM 的开销。

虚拟 DOM 是一个 JavaScript 对象，它是真实 DOM 的轻量级副本。
它通过树结构（Tree Structure）来描述真实 DOM 的层次结构。
虚拟 DOM 的更新和操作比真实 DOM 更快，因为它不涉及浏览器的渲染和重绘过程。

### 虚拟 DOM 的工作原理

- 初始渲染
当组件首次渲染时，React 会创建一个虚拟 DOM 树，并将其与真实 DOM 同步。

- 状态更新
当组件的状态（State）或属性（Props）发生变化时，React 会创建一个新的虚拟 DOM 树。

- Diff 算法
React 使用 Diff 算法 比较新旧虚拟 DOM 树的差异（称为 Reconciliation）。
Diff 算法会找出需要更新的最小部分，而不是重新渲染整个 DOM 树。

- 批量更新
React 将差异应用到真实 DOM 上，这个过程称为 提交（Commit）。
React 会批量处理更新，以减少浏览器的重绘和回流次数。

### 虚拟 DOM 的优势

（1）性能优化
直接操作真实 DOM 是非常昂贵的，因为每次 DOM 更新都会触发浏览器的重绘和回流。
虚拟 DOM 通过在内存中操作轻量级的 JavaScript 对象，减少了直接操作真实 DOM 的次数。

（2）跨平台兼容
虚拟 DOM 是一个抽象层，可以用于不同的平台（如 Web、移动端、桌面端）。
例如，React Native 使用虚拟 DOM 来生成原生组件。

（3）简化开发
开发者只需关注状态和 UI 的关系，而不需要手动操作 DOM。
React 会自动处理 DOM 的更新和渲染。

### 虚拟 DOM 的局限性
（1）内存占用
虚拟 DOM 需要在内存中维护一个完整的 DOM 树副本，可能会占用较多的内存。

（2）不适合简单场景
对于非常简单的应用，虚拟 DOM 可能会引入不必要的复杂性。

（3）性能瓶颈
在极端复杂的场景下，虚拟 DOM 的 Diff 算法可能会成为性能瓶颈。

### 虚拟 DOM 的实现原理

- 创建虚拟 DOM
React 使用 React.createElement 方法创建虚拟 DOM 节点。
```js
const element = React.createElement('div', { className: 'container' }, 'Hello, World!');
```

- Diff 算法
React 的 Diff 算法基于以下假设：
    不同类型的元素：直接替换整个子树。
    相同类型的元素：只更新变化的属性。
    列表元素：通过 key 属性优化更新。

- 提交更新
React 将虚拟 DOM 的差异应用到真实 DOM 上。
```js
ReactDOM.render(element, document.getElementById('root'));
```

## RN是如何渲染UI的？
React Native（RN） 的 UI 渲染机制与传统的 Web 应用（如 React）有显著不同。React Native 的目标是构建原生移动应用，因此它的渲染方式更接近原生开发。

### React Native 的架构
（1）JavaScript 层
开发者编写的 React 组件和逻辑代码运行在 JavaScript 线程中。
使用 React 的虚拟 DOM 来描述 UI 结构。

（2）原生层
原生代码（Objective-C/Swift 或 Java/Kotlin）运行在主线程（UI 线程）中。
负责实际渲染 UI 和处理用户交互。

（3）桥接层（Bridge）
JavaScript 层和原生层通过 桥接层 进行通信。
桥接层负责将 JavaScript 的 UI 描述转换为原生组件，并将用户交互事件传递回 JavaScript 层。


### UI 渲染流程
（1）JavaScript 线程
开发者编写 React 组件，使用 JSX 描述 UI。
React 在 JavaScript 线程中生成虚拟 DOM 树。
虚拟 DOM 树通过桥接层序列化为 JSON 数据，并发送到原生层。

（2）原生层
原生层接收到 JSON 数据后，将其解析为原生组件树。
原生层根据组件树创建对应的原生视图（如 UIView 或 View）。
原生视图被渲染到屏幕上。

（3）用户交互
用户与屏幕上的原生视图交互（如点击、滑动等）。
原生层捕获用户事件，并通过桥接层将事件传递回 JavaScript 层。
JavaScript 层处理事件，并更新虚拟 DOM 树。
更新的虚拟 DOM 树再次通过桥接层发送到原生层，触发 UI 更新。

### React Native 的组件
React Native 提供了一系列核心组件，这些组件最终会被映射为原生组件：

### 样式系统
React Native 使用 JavaScript 对象来定义样式，而不是 CSS。样式对象最终会被转换为原生样式属性。

样式映射
flex 被映射为原生布局系统（如 iOS 的 Auto Layout 或 Android 的 FlexboxLayout）。
fontSize 被映射为原生文本大小属性。


### 渲染优化
（1）批量更新
React Native 会将多个 UI 更新批量处理，减少桥接层的通信次数。

（2）异步渲染
JavaScript 线程和原生线程是异步运行的，避免了阻塞 UI 线程。

（3）FlatList 和 SectionList
对于长列表，React Native 提供了 FlatList 和 SectionList，它们只渲染可见区域的内容，从而提高性能。

## 新架构（Fabric）
Fabric 是 React Native 的新架构，旨在解决现有架构（基于 Bridge）的性能瓶颈和开发体验问题。Fabric 的目标是提供更高效的渲染机制、更好的线程模型以及更紧密的原生集成

React Native 正在开发新的架构（称为 Fabric），旨在进一步提升性能和开发体验。Fabric 的主要改进包括：

（1）同步渲染
JavaScript 线程和原生线程可以直接通信，减少桥接层的延迟。

（2）更高效的 Diff 算法
新的 Diff 算法可以更快地计算 UI 更新。

（3）更好的原生模块支持
原生模块可以直接与 JavaScript 代码交互，减少桥接层的开销。

### 现有架构的问题
在现有的 React Native 架构中，JavaScript 线程和原生线程通过 Bridge 进行通信。这种设计存在以下问题：

（1）性能瓶颈
异步通信：JavaScript 线程和原生线程之间的通信是异步的，可能导致 UI 更新的延迟。
序列化开销：数据需要通过 Bridge 进行序列化和反序列化，增加了额外的开销。

（2）开发体验
调试困难：由于 JavaScript 和原生代码运行在不同的线程中，调试变得复杂。
原生模块集成复杂：开发原生模块需要处理跨线程通信，增加了开发难度。

### Fabric 的核心改进

（1）同步渲染
JavaScript 线程和原生线程可以直接通信，减少了 Bridge 的延迟。
UI 更新可以更快地反映到屏幕上。

（2）新的渲染器
Fabric 引入了新的渲染器，替代了现有的渲染机制。
新的渲染器支持更高效的 Diff 算法和批量更新。

（3）更紧密的原生集成
JavaScript 代码可以直接调用原生模块，无需通过 Bridge。
原生模块也可以直接调用 JavaScript 代码，提供了更灵活的开发方式。

（4）线程模型优化
Fabric 引入了新的线程模型，允许 JavaScript 代码和原生代码在同一个线程中运行。
这减少了线程切换的开销，提高了性能。

### Fabric 的架构
（1）JavaScript 层
开发者编写的 React 组件和逻辑代码仍然运行在 JavaScript 线程中。
使用 React 的虚拟 DOM 来描述 UI 结构。

（2）C++ 层
Fabric 引入了 C++ 层，作为 JavaScript 层和原生层之间的桥梁。
C++ 层负责处理 UI 更新的计算和调度。

（3）原生层
原生代码（Objective-C/Swift 或 Java/Kotlin）运行在主线程（UI 线程）中。
原生层负责实际渲染 UI 和处理用户交互。

### Fabric 的渲染流程
（1）JavaScript 线程
开发者编写 React 组件，使用 JSX 描述 UI。
React 在 JavaScript 线程中生成虚拟 DOM 树。
虚拟 DOM 树通过 C++ 层发送到原生层。

（2）C++ 层
C++ 层接收到虚拟 DOM 树后，计算 UI 更新的差异。
C++ 层将更新指令发送到原生层。

（3）原生层
原生层根据更新指令创建或更新原生视图。
原生视图被渲染到屏幕上。

（4）用户交互
用户与屏幕上的原生视图交互（如点击、滑动等）。
原生层捕获用户事件，并通过 C++ 层将事件传递回 JavaScript 层。
JavaScript 层处理事件，并更新虚拟 DOM 树。
更新的虚拟 DOM 树再次通过 C++ 层发送到原生层，触发 UI 更新。

### Fabric 的优势
（1）性能提升
同步渲染和新的线程模型减少了 UI 更新的延迟。
更高效的 Diff 算法和批量更新提高了渲染性能。

（2）开发体验改进
更紧密的原生集成简化了原生模块的开发。
调试工具和开发体验得到了显著改善。

（3）跨平台一致性
Fabric 提供了更一致的跨平台开发体验，减少了平台特定的差异。

## Hermes引擎

Hermes 是 Facebook 专门为 React Native 开发的一款开源 JavaScript 引擎，旨在提升 React Native 应用的启动性能、内存占用和运行效率。Hermes 从 React Native 0.60 版本开始作为可选引擎引入，并在后续版本中逐渐成为默认引擎。

### Hermes 的设计目标

更快的启动时间：通过预编译和优化 JavaScript 代码，减少应用启动时的解析和编译时间。

更低的内存占用：优化内存管理，减少 JavaScript 引擎的内存开销。

更好的性能：提供高效的 JavaScript 执行环境，提升应用的运行效率。

### Hermes 的核心特性
1）预编译（AOT - Ahead of Time）
Hermes 支持将 JavaScript 代码预编译为字节码（Bytecode），减少运行时的解析和编译开销。

预编译后的字节码可以直接在 Hermes 引擎中执行，显著提升启动速度。

（2）优化的字节码格式
Hermes 使用紧凑的字节码格式，减少代码体积，从而降低内存占用。

字节码格式针对移动设备进行了优化，执行效率更高。

（3）高效的内存管理
Hermes 实现了轻量级的内存管理机制，减少垃圾回收（GC）的开销。

通过增量垃圾回收和压缩内存分配，降低内存峰值和波动。

（4）支持 ES6+ 语法
Hermes 支持现代 JavaScript 语法（如 ES6、ES7 等），同时保持高效的执行性能。

（5）与 React Native 深度集成
Hermes 专为 React Native 设计，能够无缝集成到 React Native 的构建和运行环境中。

开发者可以轻松启用 Hermes，无需修改现有代码。

### Hermes 的性能优势
（1）启动时间优化
Hermes 通过预编译和字节码执行，显著减少了 JavaScript 代码的解析和编译时间。

在冷启动场景下，Hermes 可以将启动时间缩短 30% 以上。

（2）内存占用降低
Hermes 的字节码格式和内存管理机制减少了内存占用。

在低端设备上，Hermes 的内存占用比传统引擎（如 JavaScriptCore）低 20%-30%。

（3）运行效率提升
Hermes 的优化执行引擎提供了更高的运行效率，尤其是在复杂计算和频繁调用的场景下。

### Hermes 的局限性

调试工具支持有限：与 Chrome DevTools 的集成不如 JavaScriptCore 成熟。

兼容性问题：某些依赖特定 JavaScript 引擎特性的库可能需要调整。

## 如何实现代码复用？

### 跨平台组件
React Native 的核心优势之一是提供了一套跨平台的组件（如 <View>、<Text>、<Image> 等），这些组件在 iOS 和 Android 上具有相同的行为。

### 平台特定代码
- 使用 .ios.js 和 .android.js 后缀来区分平台特定代码。
- Platform 模块

### 抽象通用逻辑
将通用的业务逻辑抽象到独立的模块或工具函数中，以便在不同平台和组件中复用。

### 高阶组件（HOC）
高阶组件是一种复用组件逻辑的设计模式。通过将通用逻辑提取到高阶组件中，可以在多个组件中复用。

### 自定义 Hook
自定义 Hook 是一种复用逻辑的方式，特别适合处理状态和副作用。

### 组件库
将通用的 UI 组件封装成独立的组件库，以便在多个项目中复用。

## 如何优化React Native的性能？

### 减少重渲染
React.memo、useMemo、useCallback

### 优化列表渲染
使用 FlatList 或 SectionList
使用 getItemLayout：如果列表项的高度固定，可以使用 getItemLayout 属性来避免动态计算布局

### 减少 Bridge 通信
（1）批量更新
将多个状态更新合并为一个批量更新，减少 Bridge 通信次数。

（2）避免频繁更新
避免在短时间内频繁更新状态或触发事件。

### 优化图片加载
（1）使用合适的分辨率
加载适合屏幕分辨率的图片，避免加载过大图片。

（2）使用缓存
使用 react-native-fast-image 库来缓存图片。

### 使用 Hermes 引擎

### 减少主线程负担
主线程负责 UI 渲染，过多的计算会导致 UI 卡顿。以下方法可以减少主线程负担：

（1）使用 InteractionManager
InteractionManager 可以将任务延迟到动画或交互完成后执行。

（2）使用 Web Worker
将复杂的计算任务放到 Web Worker 中执行，避免阻塞主线程。

### 优化动画
（1）使用 useNativeDriver
将动画的 useNativeDriver 属性设置为 true，将动画交给原生线程处理。

（2）避免复杂动画
避免在低端设备上使用复杂的动画。

### 使用性能分析工具
（1）React DevTools
使用 React DevTools 分析组件的渲染性能。

（2）Flipper
使用 Flipper 分析应用的性能、网络请求和日志。

（3）Performance Monitor
在开发模式下，使用 Performance Monitor 监控应用的帧率和内存占用。

## 如何处理原生模块的集成？

在 React Native 中，原生模块 是连接 JavaScript 代码和原生平台（iOS 和 Android）功能的桥梁。通过原生模块，开发者可以访问平台特定的 API 或实现高性能的功能。

### 原生模块的使用场景
访问平台特定的 API（如相机、地理位置、传感器等）。

实现高性能的功能（如图像处理、复杂计算等）。

集成第三方原生库或 SDK。

### 创建原生模块的步骤

#### iOS 原生模块

1. 创建 Objective-C 或 Swift 类
在 Xcode 中创建一个新的类，继承自 NSObject 并实现 RCTBridgeModule 协议。

2. 导出模块
使用 RCT_EXPORT_MODULE 宏导出模块。

使用 RCT_EXPORT_METHOD 宏导出方法。

```objective-c
// MyNativeModule.h
#import <React/RCTBridgeModule.h>

@interface MyNativeModule : NSObject <RCTBridgeModule>
@end

// MyNativeModule.m
#import "MyNativeModule.h"
#import <React/RCTLog.h>

@implementation MyNativeModule

RCT_EXPORT_MODULE();

RCT_EXPORT_METHOD(showMessage:(NSString *)message) {
  RCTLogInfo(@"Showing message: %@", message);
  // 在这里实现原生功能
}

@end
```
```swift
// MyNativeModule.swift
import Foundation
import React

@objc(MyNativeModule)
class MyNativeModule: NSObject {
  @objc func showMessage(_ message: String) {
    print("Showing message: \(message)")
    // 在这里实现原生功能
  }
}
```

<!-- 在js中使用 -->
```js
import { NativeModules } from 'react-native';

const { MyNativeModule } = NativeModules;

MyNativeModule.showMessage('Hello from JavaScript!');
```

#### Android 原生模块
1. 创建 Java 或 Kotlin 类
在 Android 项目中创建一个新的类，继承自 ReactContextBaseJavaModule。

2. 导出模块
使用 @ReactModule 注解导出模块。

使用 @ReactMethod 注解导出方法。

```java
// MyNativeModule.java
package com.myapp;

import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;

public class MyNativeModule extends ReactContextBaseJavaModule {
  public MyNativeModule(ReactApplicationContext reactContext) {
    super(reactContext);
  }

  @Override
  public String getName() {
    return "MyNativeModule";
  }

  @ReactMethod
  public void showMessage(String message) {
    System.out.println("Showing message: " + message);
    // 在这里实现原生功能
  }
}
```
```kotlin
// MyNativeModule.kt
package com.myapp

import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.bridge.ReactContextBaseJavaModule
import com.facebook.react.bridge.ReactMethod

class MyNativeModule(reactContext: ReactApplicationContext) : ReactContextBaseJavaModule(reactContext) {
  override fun getName() = "MyNativeModule"

  @ReactMethod
  fun showMessage(message: String) {
    println("Showing message: $message")
    // 在这里实现原生功能
  }
}
```

3. 注册模块
在 MainApplication.java 或 MainApplication.kt 中注册模块。
```java
// MainApplication.java
import com.facebook.react.ReactPackage;
import com.facebook.react.shell.MainReactPackage;
import com.myapp.MyNativeModule;

import java.util.Arrays;
import java.util.List;

public class MainApplication extends Application implements ReactApplication {
  @Override
  protected List<ReactPackage> getPackages() {
    return Arrays.<ReactPackage>asList(
      new MainReactPackage(),
      new ReactPackage() {
        @Override
        public List<NativeModule> createNativeModules(ReactApplicationContext reactContext) {
          return Arrays.<NativeModule>asList(
            new MyNativeModule(reactContext)
          );
        }
      }
    );
  }
}
```

4. 在js中使用
```js
import { NativeModules } from 'react-native';

const { MyNativeModule } = NativeModules;

MyNativeModule.showMessage('Hello from JavaScript!');
```

### 处理回调

原生模块可以通过回调函数将结果返回给 JavaScript。

```objective-c
RCT_EXPORT_METHOD(getData:(RCTResponseSenderBlock)callback) {
  NSString *data = @"Some data from native";
  callback(@[data]);
}
```

```java
@ReactMethod
public void getData(Callback callback) {
  String data = "Some data from native";
  callback.invoke(data);
}
```
在 JavaScript 中使用
```js
MyNativeModule.getData((data) => {
  console.log('Data from native:', data);
});
```

### 处理 Promise
原生模块可以通过 Promise 返回异步结果。

```objective-c
RCT_EXPORT_METHOD(getData:(RCTPromiseResolveBlock)resolve reject:(RCTPromiseRejectBlock)reject) {
  NSString *data = @"Some data from native";
  resolve(data);
}
```

```java
@ReactMethod
public void getData(Promise promise) {
  String data = "Some data from native";
  promise.resolve(data);
}
```
在 JavaScript 中使用
```js
MyNativeModule.getData()
  .then((data) => {
    console.log('Data from native:', data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
```

### 处理事件

原生模块可以通过事件将数据发送到 JavaScript。

```objective-c
#import <React/RCTEventEmitter.h>

@interface MyNativeModule : RCTEventEmitter <RCTBridgeModule>
@end

@implementation MyNativeModule

RCT_EXPORT_MODULE();

- (NSArray<NSString *> *)supportedEvents {
  return @[@"MyEvent"];
}

RCT_EXPORT_METHOD(sendEvent) {
  [self sendEventWithName:@"MyEvent" body:@{@"message": @"Hello from native"}];
}

@end
```

```java
import com.facebook.react.modules.core.DeviceEventManagerModule;
import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;

public class MyNativeModule extends ReactContextBaseJavaModule {
  public MyNativeModule(ReactApplicationContext reactContext) {
    super(reactContext);
  }

  @Override
  public String getName() {
    return "MyNativeModule";
  }

  @ReactMethod
  public void sendEvent() {
    getReactApplicationContext()
      .getJSModule(DeviceEventManagerModule.RCTDeviceEventEmitter.class)
      .emit("MyEvent", "Hello from native");
  }
}
```

在 JavaScript 中使用
```js
import { NativeEventEmitter, NativeModules } from 'react-native';

const { MyNativeModule } = NativeModules;
const eventEmitter = new NativeEventEmitter(MyNativeModule);

eventEmitter.addListener('MyEvent', (event) => {
  console.log('Event from native:', event);
});

MyNativeModule.sendEvent();
```

## 常用插件和工具
导航：React Navigation（Stack、Tab、Drawer）

状态管理：Redux、MobX、Context API

网络请求：Axios、Fetch

本地存储：AsyncStorage

UI库：React Native Paper、NativeBase

动画：React Native Reanimated、Lottie

调试工具：React Native Debugger、Flipper

## 如何向面试官讲解我开发的RN接入原生模块的功能

### 项目背景

在我参与的一个 React Native 项目中，我们需要实现一个二维码扫描功能，并在扫描成功后触发设备震动，以提供更好的用户体验。由于 React Native 自带的 Camera 组件无法满足我们的性能需求，我们决定通过原生模块来实现这一功能

### 技术选型理由

性能需求：二维码扫描需要实时处理视频流，原生代码的性能更高。

功能扩展：React Native 的原生模块可以访问平台特定的 API，如 iOS 的 AVFoundation 和 Android 的 Camera2。

设备震动：React Native 没有直接提供设备震动的 API，需要通过原生模块实现。

### 实现步骤

### Android 实现

1. 创建 Java 类
在 Android 项目中创建一个新的 Java 类 QRCodeScannerModule。
```java
// QRCodeScannerModule.java
package com.myapp;

import android.content.Context;
import android.media.AudioManager;
import android.media.ToneGenerator;
import android.os.Vibrator;
import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;

public class QRCodeScannerModule extends ReactContextBaseJavaModule {
  private final ReactApplicationContext reactContext;

  public QRCodeScannerModule(ReactApplicationContext reactContext) {
    super(reactContext);
    this.reactContext = reactContext;
  }

  @Override
  public String getName() {
    return "QRCodeScannerModule";
  }

  @ReactMethod
  public void startScanning() {
    // 初始化摄像头并开始扫描
    // 这里省略摄像头初始化和二维码识别的代码
  }

  @ReactMethod
  public void vibrate() {
    Vibrator vibrator = (Vibrator) reactContext.getSystemService(Context.VIBRATOR_SERVICE);
    if (vibrator != null) {
      vibrator.vibrate(500); // 震动 500 毫秒
    }
  }
}
```

2. 注册模块
在 MainApplication.java 中注册模块。

```java
// MainApplication.java
import com.facebook.react.ReactPackage;
import com.facebook.react.shell.MainReactPackage;
import com.myapp.QRCodeScannerModule;

import java.util.Arrays;
import java.util.List;

public class MainApplication extends Application implements ReactApplication {
  @Override
  protected List<ReactPackage> getPackages() {
    return Arrays.<ReactPackage>asList(
      new MainReactPackage(),
      new ReactPackage() {
        @Override
        public List<NativeModule> createNativeModules(ReactApplicationContext reactContext) {
          return Arrays.<NativeModule>asList(
            new QRCodeScannerModule(reactContext)
          );
        }
      }
    );
  }
}
```

### iOS 实现

1. 创建 Objective-C 类
在 iOS 项目中创建一个新的 Objective-C 类 QRCodeScannerModule。

```objective-c
// QRCodeScannerModule.h
#import <React/RCTBridgeModule.h>
#import <AVFoundation/AVFoundation.h>

@interface QRCodeScannerModule : NSObject <RCTBridgeModule>
@end

// QRCodeScannerModule.m
#import "QRCodeScannerModule.h"
#import <AudioToolbox/AudioToolbox.h>

@implementation QRCodeScannerModule

RCT_EXPORT_MODULE();

RCT_EXPORT_METHOD(startScanning) {
  dispatch_async(dispatch_get_main_queue(), ^{
    // 初始化摄像头并开始扫描
    // 这里省略摄像头初始化和二维码识别的代码
  });
}

RCT_EXPORT_METHOD(vibrate) {
  AudioServicesPlaySystemSound(kSystemSoundID_Vibrate); // 触发震动
}

@end
```

### JavaScript 调用
```js
import { NativeModules } from 'react-native';

const { QRCodeScannerModule } = NativeModules;

function startScanning() {
  QRCodeScannerModule.startScanning();
}

function vibrate() {
  QRCodeScannerModule.vibrate();
}

// 使用示例
startScanning();

// 扫描成功后触发震动
function onScanSuccess() {
  vibrate();
}
```

### 可能追问的问题
如何解决原生模块的性能瓶颈？

答：避免在主线程中执行耗时操作，使用异步任务或线程池处理复杂逻辑。

如何处理 Android 和 iOS 的差异？

答：通过平台特定的代码（如 .android.js 和 .ios.js）或 Platform 模块动态区分平台。

如何确保原生模块的跨平台兼容性？

答：通过统一的 JavaScript API 封装平台特定的实现，确保调用方式一致。

## 项目中的挑战

### 列表滚动卡顿的问题
在开发过程中，遇到了长列表滚动卡顿的问题。通过分析发现是图片加载导致的性能瓶颈，最终使用react-native-fast-image插件优化了图片加载。

### 吸顶

吸顶效果的核心是通过监听滚动事件，动态调整目标组件的位置或样式，使其在滚动到指定位置时固定在顶部。

优化：
使用 useMemo 和 useCallback 缓存计算值和函数引用。

使用 scrollEventThrottle 控制滚动事件的触发频率。

使用 Animated.event 的 useNativeDriver 属性将动画交给原生线程处理。

## 如何实现一个自定义的Modal组件？

1. 自定义 Modal 组件的核心功能
一个自定义 Modal 组件通常需要实现以下功能：

显示/隐藏控制：通过 visible 属性控制 Modal 的显示和隐藏。

动画效果：通过动画实现 Modal 的淡入淡出或滑动效果。

遮罩层：在 Modal 下方显示一个半透明的遮罩层。

点击遮罩层关闭：点击遮罩层时关闭 Modal。

2. 实现步骤
（1）创建 Modal 组件
创建一个可复用的 CustomModal 组件，支持显示/隐藏控制和动画效果。

（2）使用 Animated 实现动画
使用 React Native 的 Animated API 实现 Modal 的动画效果。

（3）处理点击遮罩层关闭
通过 TouchableWithoutFeedback 组件实现点击遮罩层关闭 Modal 的功能。

## 如何处理RN中的内存泄漏问题？

在 React Native 应用中，内存泄漏 是一个常见的问题，尤其是在组件卸载后未正确清理资源（如事件监听器、定时器、订阅等）时。内存泄漏会导致应用性能下降，甚至崩溃。

### 内存泄漏的常见原因
未清理的事件监听器：组件卸载后，事件监听器仍然存在。

未清除的定时器：setTimeout 或 setInterval 未在组件卸载时清除。

未取消的订阅：如 Redux 的 store.subscribe 或第三方库的订阅。

未释放的引用：如闭包中引用了组件的状态或方法。

### 检测内存泄漏

Chrome DevTools：通过 React DevTools 和 Chrome 的内存分析工具检测内存泄漏。

Flipper：React Native 的调试工具，支持内存和性能分析。

Xcode Instruments（iOS）：用于检测 iOS 应用的内存泄漏。

Android Profiler（Android）：用于检测 Android 应用的内存泄漏。

### 解决内存泄漏的方法

（1）清理事件监听器
（2）清除定时器
（3）取消订阅
（4）避免闭包中的引用
（5）使用 useRef 存储可变值
（6）避免在卸载的组件中更新状态


## 如何实现一个无限滚动列表？

监听滚动事件：当用户滚动到列表底部时，触发加载更多数据的逻辑。

加载更多数据：从服务器或本地数据源获取更多数据，并将其追加到现有列表中。

显示加载指示器：在加载数据时，显示一个加载指示器（如 ActivityIndicator）。


## 如何使用RN实现一个实时聊天功能？

实时通信：使用 WebSocket 或第三方服务（如 Firebase、Socket.IO）实现实时消息传递。

消息存储：使用数据库（如 Firebase Firestore、MongoDB）存储聊天记录。

用户认证：使用认证服务（如 Firebase Authentication）管理用户登录和身份验证。


## RN 打包和上架

### Android 打包

1. 生成签名密钥
```shell
keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
```

2. 添加签名配置, 配置 Gradle `android/app/build.gradle`
```js
android {
    ...
    signingConfigs {
        release {
            storeFile file('my-release-key.keystore')
            storePassword 'your_store_password'
            keyAlias 'your_key_alias'
            keyPassword 'your_key_password'
        }
    }
    buildTypes {
        release {
            ...
            signingConfig signingConfigs.release
        }
    }
}
```

3. 打包 APK
```shell
cd android
./gradlew assembleRelease
```

> APK 文件会生成在 android/app/build/outputs/apk/release/ 目录下。

### ios 打包

1. 配置 Xcode 项目

打开 ios/YourProject.xcworkspace 文件。

在 Xcode 中，选择目标设备为 Generic iOS Device。

进入 Product > Scheme > Edit Scheme，确保 Build Configuration 为 Release。

2. 打包 IPA
在 Xcode 中，选择 Product > Archive。

打包完成后，Xcode 会自动打开 Organizer 窗口，显示生成的 .xcarchive 文件。

点击 Distribute App，选择 App Store Connect，然后按照提示导出 .ipa 文件。

## 上架应用

### 上架到 Google Play Store

1. 创建开发者账号
访问 Google Play Console，注册并支付一次性费用（25 美元）。

2. 创建应用
登录 Google Play Console，点击 Create App。

填写应用的基本信息（如名称、描述、分类等）。

3. 上传 APK
进入 Release Management > App Releases。

选择 Production，点击 Create Release。

上传打包好的 APK 文件。

4. 填写商店信息
进入 Store Presence > Store Listing，填写应用的详细信息（如截图、图标、描述等）。

进入 Pricing & Distribution，设置价格和分发范围。

5. 提交审核
检查所有信息无误后，点击 Submit 提交审核。

审核通过后，应用会自动发布到 Google Play Store。

### 上架到 Apple App Store

1. 创建开发者账号
访问 Apple Developer，注册并支付年费（99 美元）。

2. 创建应用
登录 App Store Connect，点击 My Apps。

点击 + 按钮，选择 New App，填写应用的基本信息。

3. 上传 IPA
安装并打开 Transporter。

将打包好的 .ipa 文件拖入 Transporter，点击 Deliver 上传。

4. 填写商店信息
在 App Store Connect 中，进入 App Information，填写应用的详细信息（如名称、描述、分类等）。

进入 Pricing and Availability，设置价格和分发范围。

5. 提交审核
进入 App Store > App Review，填写审核信息并提交。

审核通过后，应用会自动发布到 Apple App Store。