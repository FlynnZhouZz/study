# useRef

## useRef的特点

useRef 可以在函数组件中存储可变值的方式。与useState的不同之处是，它不会引起组件的重新渲染。

1. 会返回一个可变的 ref 对象。
2. 可以保存任何可变值，类似于在 class 组件中使用实例变量。
3. 返回的 ref 对象在组件的整个生命周期中保持不变。
4. 并不会在每次组件渲染时都生成新的 ref 对象，因此可以用来保存一些不需要触发重新渲染的数据。
5. 可以用来引用 DOM 元素，用于获取或修改其属性。
6. 可以用来在函数组件之间传递数据。
7. 可以模拟实例变量，用于保存函数组件中的状态。

## 使用场景

### 存储定时器的 ID

```js
import React, { useState, useEffect, useRef } from 'react';

function App() {
  const [count, setCount] = useState(0);
  const intervalRef = useRef(null);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);

    return () => clearInterval(intervalRef.current);
  }, []);

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => clearInterval(intervalRef.current)}>
        Stop timer
      </button>
    </div>
  );
}

```

### 存储上一次的props或state

```js
import React, { useState, useEffect, useRef } from 'react';

function App() {
  const [count, setCount] = useState(0);
  const prevCountRef = useRef(null);

  useEffect(() => {
    prevCountRef.current = count;
  });

  const prevCount = prevCountRef.current;

  return (
    <div>
      <p>Current count: {count}</p>
      {prevCount && (
        <p>Previous count: {prevCount}</p>
      )}
      <button onClick={() => setCount(c => c + 1)}>
        Increase count
      </button>
    </div>
  );
}

```

### 存储dom元素的引用

```js
import React, { useRef } from 'react';

function App() {
  const inputRef = useRef(null);

  function handleFocus() {
    inputRef.current.style.backgroundColor = 'yellow';
  }

  function handleBlur() {
    inputRef.current.style.backgroundColor = 'white';
  }

  return (
    <>
      <input type="text" ref={inputRef} onFocus={handleFocus} onBlur={handleBlur} />
      <button onClick={() => inputRef.current.focus()}>
        Focus input
      </button>
    </>
  );
}

```

### 简单的组件间通信

```js

```