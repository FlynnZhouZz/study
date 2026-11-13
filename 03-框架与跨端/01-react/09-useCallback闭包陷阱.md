# useCallback 闭包陷阱

闭包陷阱指的是在 React 函数组件中，由于闭包的特性，回调函数或副作用函数捕获了旧的变量值，而不是最新的值。

## 常见场景

### 1. 经典计数器问题

```jsx
function Counter() {
    const [count, setCount] = useState(0);

    // ❌ 问题：点击按钮时，回调函数使用的是创建时的 count 值
    const increment = useCallback(() => {
        setCount(count + 1); // 总是使用初始的 count 值
    }, []); // 依赖数组为空，只创建一次

    return <button onClick={increment}>Count: {count}</button>;
}
```

### 2. 定时器中的闭包陷阱

```jsx
function Timer() {
    const [time, setTime] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            // ❌ 问题：总是输出 0，闭包捕获了初始值
            console.log(time);
            setTime(time + 1); // 只会从 0 加到 1，然后一直加 1
        }, 1000);

        return () => clearInterval(interval);
    }, []); // 依赖数组为空，effect 只运行一次

    return <div>Time: {time}</div>;
}
```

## 解决方案

### 方案 1：正确声明依赖

```jsx
function Counter() {
    const [count, setCount] = useState(0);

    // ✅ 正确：将 count 添加到依赖数组
    const increment = useCallback(() => {
        setCount(count + 1);
    }, [count]); // 依赖 count，count 变化时重新创建函数

    return <button onClick={increment}>Count: {count}</button>;
}
```

### 方案 2：使用函数式更新

```jsx
function Counter() {
    const [count, setCount] = useState(0);

    // ✅ 最佳实践：使用函数式更新，无需依赖 count
    const increment = useCallback(() => {
        setCount(prevCount => prevCount + 1);
    }, []); // 依赖数组可以为空

    return <button onClick={increment}>Count: {count}</button>;
}
```

### 方案 3：使用 ref 保存最新值

```jsx
function Timer() {
    const [time, setTime] = useState(0);
    const timeRef = useRef(time);

    // 同步 ref 和 state
    useEffect(() => {
        timeRef.current = time;
    }, [time]);

    useEffect(() => {
        const interval = setInterval(() => {
            // ✅ 正确：使用 ref 访问最新值
            console.log(timeRef.current);
            setTime(timeRef.current + 1);
        }, 1000);

        return () => clearInterval(interval);
    }, []); // 依赖数组可以为空

    return <div>Time: {time}</div>;
}
```

### 方案 4：自定义 hook 封装

```jsx
// 自定义 hook 解决闭包问题
function useLatestRef(value) {
    const ref = useRef(value);
    useEffect(() => {
        ref.current = value;
    }, [value]);
    return ref;
}

function Timer() {
    const [time, setTime] = useState(0);
    const timeRef = useLatestRef(time);

    useEffect(() => {
        const interval = setInterval(() => {
            console.log(timeRef.current);
            setTime(timeRef.current + 1);
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    return <div>Time: {time}</div>;
}
```

## 复杂场景示例

### 场景：表单提交

```jsx
function Form() {
    const [data, setData] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const dataRef = useRef(data);

    useEffect(() => {
        dataRef.current = data;
    }, [data]);

    // ✅ 使用 ref 或函数式更新
    const handleSubmit = useCallback(async () => {
        setIsSubmitting(true);
        try {
            // 可以安全访问最新的 data
            await submitData(dataRef.current);
        } catch (error) {
            console.error("提交失败:", error);
        } finally {
            setIsSubmitting(false);
        }
    }, []); // 不需要依赖 data

    return <form onSubmit={handleSubmit}>{/* 表单内容 */}</form>;
}
```

### 场景：事件监听器

```jsx
function ScrollComponent() {
    const [scrollY, setScrollY] = useState(0);
    const [isScrollingDown, setIsScrollingDown] = useState(false);

    const prevScrollYRef = useRef(0);

    const handleScroll = useCallback(() => {
        const currentScrollY = window.scrollY;
        setIsScrollingDown(currentScrollY > prevScrollYRef.current);
        prevScrollYRef.current = currentScrollY;
        setScrollY(currentScrollY);
    }, []);

    useEffect(() => {
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, [handleScroll]);

    return (
        <div>
            <div>滚动位置: {scrollY}</div>
            <div>{isScrollingDown ? "向下滚动" : "向上滚动"}</div>
        </div>
    );
}
```

## 最佳实践总结

1. 优先使用函数式更新：对于 setState，使用函数式更新可以避免依赖变化。`setCount(prev => prev + 1);`
2. 正确声明依赖：对于非函数式更新的场景，确保依赖数组包含所有用到的变量
3. 使用 ref 保存可变值：对于需要在回调中访问但不想触发重新渲染的值，使用 ref
4. 区分使用场景：

-   需要最新状态值：使用函数式更新或 ref
-   需要缓存函数避免子组件重渲染：使用 useCallback 并正确声明依赖
-   需要在卸载时清理：使用 useEffect 的清理函数

5. 避免过度优化：不是所有函数都需要 useCallback，只有确实需要保持引用稳定时才使用

## 调试技巧

1. 使用 React DevTools 检查组件重渲染
2. 使用 useWhyDidYouUpdate 自定义 hook 分析更新原因
3. 添加 console.log 检查闭包中的变量值

```jsx
// 调试 hook
function useWhyDidYouUpdate(name, props) {
    const previousProps = useRef();
    useEffect(() => {
        if (previousProps.current) {
            const allKeys = Object.keys({ ...previousProps.current, ...props });
            const changes = {};
            allKeys.forEach(key => {
                if (previousProps.current[key] !== props[key]) {
                    changes[key] = {
                        from: previousProps.current[key],
                        to: props[key],
                    };
                }
            });
            if (Object.keys(changes).length) {
                console.log("[why-did-you-update]", name, changes);
            }
        }
        previousProps.current = props;
    });
}
```

## 总结

理解闭包陷阱的关键是认识到：函数组件每次渲染都会创建一个新的闭包作用域，而 useCallback 可以帮助我们控制何时创建新的函数引用。
