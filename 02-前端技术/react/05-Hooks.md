# Hooks

Hooks 是 React 16.8 新增的特性，让你在不编写 class 的情况下使用 state 和其他 React 特性。

为什么需要 Hooks？

-   解决 class 组件中状态逻辑复用困难的问题
-   避免组件嵌套过深（render props、HOC）
-   解决 class 中 this 绑定问题
-   更好的逻辑分离和复用

## 基础 Hooks

### useState - 状态管理

```jsx
import { useState } from "react";

function Counter() {
    // 基本用法
    const [count, setCount] = useState(0);

    // 对象状态
    const [user, setUser] = useState({
        name: "张三",
        age: 25,
        email: "zhangsan@example.com",
    });

    // 数组状态
    const [items, setItems] = useState(["item1", "item2"]);

    // 函数式更新
    const increment = () => {
        setCount(prevCount => prevCount + 1);
    };

    // 更新对象状态
    const updateUserName = () => {
        setUser(prevUser => ({
            ...prevUser,
            name: "李四",
        }));
    };

    // 更新数组状态
    const addItem = () => {
        setItems(prevItems => [...prevItems, `item${prevItems.length + 1}`]);
    };

    // 惰性初始 state
    const expensiveInitialState = () => {
        console.log("惰性初始化，只执行一次");
        return 0;
    };
    const [lazyState, setLazyState] = useState(() => expensiveInitialState());

    return (
        <div>
            <h2>计数器: {count}</h2>
            <button onClick={increment}>增加</button>
            <button onClick={() => setCount(count - 1)}>减少</button>

            <h2>用户信息</h2>
            <p>姓名: {user.name}</p>
            <p>年龄: {user.age}</p>
            <button onClick={updateUserName}>修改姓名</button>

            <h2>项目列表</h2>
            <ul>
                {items.map((item, index) => (
                    <li key={index}>{item}</li>
                ))}
            </ul>
            <button onClick={addItem}>添加项目</button>
        </div>
    );
}
```

### useEffect - 副作用处理

```jsx
import { useState, useEffect } from "react";

function EffectDemo() {
    const [count, setCount] = useState(0);
    const [data, setData] = useState(null);
    const [windowSize, setWindowSize] = useState({
        width: window.innerWidth,
        height: window.innerHeight,
    });

    // 1. 无依赖数组 - 每次渲染后都执行
    useEffect(() => {
        console.log("无依赖数组 - 每次渲染后执行");
    });

    // 2. 空依赖数组 - 只在组件挂载时执行（模拟 componentDidMount）
    useEffect(() => {
        console.log("空依赖数组 - 组件挂载时执行一次");

        // 发起网络请求
        fetchData();

        // 设置定时器
        const timerId = setInterval(() => {
            console.log("定时器执行中...");
        }, 1000);

        // 清理函数（模拟 componentWillUnmount）
        return () => {
            console.log("清理定时器");
            clearInterval(timerId);
        };
    }, []);

    // 3. 有依赖数组 - 依赖变化时执行（模拟 componentDidUpdate）
    useEffect(() => {
        console.log(`count 变化: ${count}`);
        document.title = `计数: ${count}`;

        // 发送分析数据
        if (count > 0) {
            console.log(`计数增加到 ${count}`);
        }
    }, [count]); // 依赖 count，count 变化时执行

    // 4. 监听窗口大小变化
    useEffect(() => {
        const handleResize = () => {
            setWindowSize({
                width: window.innerWidth,
                height: window.innerHeight,
            });
        };

        window.addEventListener("resize", handleResize);

        return () => {
            window.removeEventListener("resize", handleResize);
        };
    }, []); // 空数组表示只添加一次监听

    // 5. 清理副作用示例
    useEffect(() => {
        const controller = new AbortController();
        const signal = controller.signal;

        fetch("/api/data", { signal })
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => {
                if (error.name !== "AbortError") {
                    console.error("请求失败:", error);
                }
            });

        return () => {
            controller.abort(); // 组件卸载时取消请求
        };
    }, []);

    const fetchData = async () => {
        try {
            const response = await fetch("https://api.example.com/data");
            const result = await response.json();
            setData(result);
        } catch (error) {
            console.error("获取数据失败:", error);
        }
    };

    return (
        <div>
            <h1>useEffect 示例</h1>
            <p>计数: {count}</p>
            <button onClick={() => setCount(count + 1)}>增加</button>

            <p>
                窗口大小: {windowSize.width} x {windowSize.height}
            </p>

            <div>
                <h2>数据:</h2>
                <pre>{JSON.stringify(data, null, 2)}</pre>
            </div>
        </div>
    );
}
```

### useContext - 上下文管理

```jsx
import { createContext, useContext, useState } from "react";

// 1. 创建 Context
const ThemeContext = createContext("light");
const UserContext = createContext(null);

// 2. 提供 Context 值
function App() {
    const [theme, setTheme] = useState("light");
    const [user, setUser] = useState({
        name: "张三",
        role: "admin",
    });

    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            <UserContext.Provider value={{ user, setUser }}>
                <Toolbar />
                <Profile />
            </UserContext.Provider>
        </ThemeContext.Provider>
    );
}

// 3. 使用 useContext 获取 Context
function Toolbar() {
    const { theme, setTheme } = useContext(ThemeContext);

    return (
        <div
            style={{
                padding: "20px",
                backgroundColor: theme === "dark" ? "#333" : "#fff",
                color: theme === "dark" ? "#fff" : "#333",
            }}
        >
            <h2>工具栏</h2>
            <p>当前主题: {theme}</p>
            <button onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>切换主题</button>
        </div>
    );
}

// 4. 使用多个 Context
function Profile() {
    const { theme } = useContext(ThemeContext);
    const { user, setUser } = useContext(UserContext);

    const updateUser = () => {
        setUser({
            ...user,
            name: user.name === "张三" ? "李四" : "张三",
        });
    };

    return (
        <div
            style={{
                padding: "20px",
                marginTop: "20px",
                backgroundColor: theme === "dark" ? "#222" : "#f0f0f0",
            }}
        >
            <h2>用户信息</h2>
            <p>姓名: {user.name}</p>
            <p>角色: {user.role}</p>
            <button onClick={updateUser}>切换用户</button>
        </div>
    );
}

// 5. 自定义 Context Hook
function useTheme() {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error("useTheme 必须在 ThemeProvider 内使用");
    }
    return context;
}

// 使用自定义 Hook
function ThemeButton() {
    const { theme, setTheme } = useTheme();

    return (
        <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            style={{
                backgroundColor: theme === "dark" ? "#666" : "#ddd",
            }}
        >
            {theme === "dark" ? "切换到亮色" : "切换到暗色"}
        </button>
    );
}
```

## 高级 Hooks

### useReducer - 复杂状态管理

```jsx
import { useReducer } from "react";

// 1. 定义 reducer 函数
const todoReducer = (state, action) => {
    switch (action.type) {
        case "ADD_TODO":
            return {
                ...state,
                todos: [
                    ...state.todos,
                    {
                        id: Date.now(),
                        text: action.text,
                        completed: false,
                    },
                ],
            };

        case "TOGGLE_TODO":
            return {
                ...state,
                todos: state.todos.map(todo =>
                    todo.id === action.id ? { ...todo, completed: !todo.completed } : todo
                ),
            };

        case "DELETE_TODO":
            return {
                ...state,
                todos: state.todos.filter(todo => todo.id !== action.id),
            };

        case "SET_FILTER":
            return {
                ...state,
                filter: action.filter,
            };

        default:
            return state;
    }
};

// 2. 初始状态
const initialState = {
    todos: [],
    filter: "all", // all, active, completed
};

// 3. 使用 useReducer
function TodoApp() {
    const [state, dispatch] = useReducer(todoReducer, initialState);
    const [inputValue, setInputValue] = useState("");

    // 获取过滤后的待办事项
    const filteredTodos = state.todos.filter(todo => {
        if (state.filter === "active") return !todo.completed;
        if (state.filter === "completed") return todo.completed;
        return true;
    });

    // 添加待办事项
    const handleAddTodo = () => {
        if (inputValue.trim()) {
            dispatch({ type: "ADD_TODO", text: inputValue });
            setInputValue("");
        }
    };

    // 切换完成状态
    const handleToggleTodo = id => {
        dispatch({ type: "TOGGLE_TODO", id });
    };

    // 删除待办事项
    const handleDeleteTodo = id => {
        dispatch({ type: "DELETE_TODO", id });
    };

    return (
        <div style={{ maxWidth: "500px", margin: "0 auto" }}>
            <h1>待办事项列表</h1>

            {/* 添加待办事项 */}
            <div style={{ marginBottom: "20px" }}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={e => setInputValue(e.target.value)}
                    onKeyPress={e => e.key === "Enter" && handleAddTodo()}
                    placeholder="输入待办事项..."
                    style={{ marginRight: "10px", padding: "5px" }}
                />
                <button onClick={handleAddTodo}>添加</button>
            </div>

            {/* 过滤器 */}
            <div style={{ marginBottom: "20px" }}>
                <button
                    onClick={() => dispatch({ type: "SET_FILTER", filter: "all" })}
                    style={{
                        marginRight: "10px",
                        fontWeight: state.filter === "all" ? "bold" : "normal",
                    }}
                >
                    全部
                </button>
                <button
                    onClick={() => dispatch({ type: "SET_FILTER", filter: "active" })}
                    style={{
                        marginRight: "10px",
                        fontWeight: state.filter === "active" ? "bold" : "normal",
                    }}
                >
                    未完成
                </button>
                <button
                    onClick={() => dispatch({ type: "SET_FILTER", filter: "completed" })}
                    style={{
                        fontWeight: state.filter === "completed" ? "bold" : "normal",
                    }}
                >
                    已完成
                </button>
            </div>

            {/* 待办事项列表 */}
            <ul style={{ listStyle: "none", padding: 0 }}>
                {filteredTodos.map(todo => (
                    <li
                        key={todo.id}
                        style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            padding: "10px",
                            marginBottom: "10px",
                            backgroundColor: "#f5f5f5",
                            borderRadius: "5px",
                            textDecoration: todo.completed ? "line-through" : "none",
                            opacity: todo.completed ? 0.6 : 1,
                        }}
                    >
                        <span
                            onClick={() => handleToggleTodo(todo.id)}
                            style={{ cursor: "pointer" }}
                        >
                            {todo.text}
                        </span>
                        <div>
                            <button
                                onClick={() => handleToggleTodo(todo.id)}
                                style={{ marginRight: "10px" }}
                            >
                                {todo.completed ? "标记未完成" : "标记完成"}
                            </button>
                            <button
                                onClick={() => handleDeleteTodo(todo.id)}
                                style={{ color: "red" }}
                            >
                                删除
                            </button>
                        </div>
                    </li>
                ))}
            </ul>

            {/* 统计信息 */}
            <div style={{ marginTop: "20px", padding: "10px", backgroundColor: "#e0e0e0" }}>
                <p>总计: {state.todos.length} 项</p>
                <p>未完成: {state.todos.filter(t => !t.completed).length} 项</p>
                <p>已完成: {state.todos.filter(t => t.completed).length} 项</p>
            </div>
        </div>
    );
}

// 4. 使用惰性初始化
function CounterWithLazyInit() {
    const init = initialCount => {
        console.log("惰性初始化 reducer");
        return { count: initialCount };
    };

    const [state, dispatch] = useReducer(
        (state, action) => {
            switch (action.type) {
                case "increment":
                    return { count: state.count + 1 };
                case "decrement":
                    return { count: state.count - 1 };
                case "reset":
                    return init(action.payload);
                default:
                    return state;
            }
        },
        0, // 初始值
        init // 初始化函数
    );

    return (
        <div>
            计数: {state.count}
            <button onClick={() => dispatch({ type: "increment" })}>+</button>
            <button onClick={() => dispatch({ type: "decrement" })}>-</button>
            <button onClick={() => dispatch({ type: "reset", payload: 0 })}>重置</button>
        </div>
    );
}
```

### useCallback - 记忆化回调函数

```jsx
import { useState, useCallback, memo } from "react";

// 使用 memo 包装的子组件
const ExpensiveChild = memo(({ onClick, data }) => {
    console.log("ExpensiveChild 渲染");

    return (
        <div style={{ padding: "20px", backgroundColor: "#f0f0f0", margin: "10px 0" }}>
            <h3>昂贵的子组件</h3>
            <p>数据: {data}</p>
            <button onClick={onClick}>子组件按钮</button>
        </div>
    );
});

function CallbackDemo() {
    const [count, setCount] = useState(0);
    const [text, setText] = useState("");

    // ❌ 问题：每次渲染都会创建新的函数，导致子组件不必要地重新渲染
    const badHandleClick = () => {
        console.log("点击处理", count);
    };

    // ✅ 正确：使用 useCallback 记忆函数
    const goodHandleClick = useCallback(() => {
        console.log("点击处理（记忆化）", count);
    }, [count]); // 依赖 count，count 变化时重新创建函数

    // 另一个示例：带参数的函数
    const handleItemClick = useCallback(
        itemId => {
            console.log("点击项目:", itemId, "计数:", count);
        },
        [count]
    ); // 依赖 count

    // 如果没有依赖，函数只会创建一次
    const stableFunction = useCallback(() => {
        console.log("这是一个稳定的函数，不会重新创建");
    }, []); // 空依赖数组

    return (
        <div style={{ padding: "20px" }}>
            <h1>useCallback 示例</h1>

            <div>
                <p>计数: {count}</p>
                <button onClick={() => setCount(count + 1)}>增加计数</button>
            </div>

            <div>
                <input
                    type="text"
                    value={text}
                    onChange={e => setText(e.target.value)}
                    placeholder="输入文字..."
                />
            </div>

            {/* 使用记忆化函数的子组件 */}
            <ExpensiveChild onClick={goodHandleClick} data={text} />

            {/* 另一个示例 */}
            <div style={{ marginTop: "20px" }}>
                <h3>项目列表</h3>
                {[1, 2, 3].map(itemId => (
                    <div
                        key={itemId}
                        onClick={() => handleItemClick(itemId)}
                        style={{
                            padding: "10px",
                            margin: "5px",
                            backgroundColor: "#e8e8e8",
                            cursor: "pointer",
                        }}
                    >
                        项目 {itemId}
                    </div>
                ))}
            </div>

            {/* 稳定函数的示例 */}
            <button onClick={stableFunction} style={{ marginTop: "20px" }}>
                调用稳定函数
            </button>
        </div>
    );
}
```

### useMemo - 记忆化计算结果

```jsx
import { useState, useMemo } from "react";

// 模拟昂贵的计算
const expensiveCalculation = num => {
    console.log("执行昂贵计算...");
    // 模拟耗时操作
    for (let i = 0; i < 1000000000; i++) {}
    return num * 2;
};

function MemoDemo() {
    const [count, setCount] = useState(0);
    const [text, setText] = useState("");
    const [list, setList] = useState([1, 2, 3, 4, 5]);

    // ❌ 问题：每次渲染都会重新计算
    const badComputedValue = expensiveCalculation(count);

    // ✅ 正确：使用 useMemo 记忆计算结果
    const goodComputedValue = useMemo(() => {
        return expensiveCalculation(count);
    }, [count]); // 只有 count 变化时才重新计算

    // 记忆化复杂的过滤和映射操作
    const filteredList = useMemo(() => {
        console.log("过滤列表...");
        return list.filter(item => item > 2).map(item => item * 10);
    }, [list]); // 依赖 list

    // 记忆化对象
    const userInfo = useMemo(() => {
        return {
            id: 1,
            name: "张三",
            age: count + 20,
            // 计算属性
            isAdult: count + 20 >= 18,
        };
    }, [count]);

    // 记忆化数组
    const options = useMemo(() => {
        return ["选项1", "选项2", "选项3", `选项${count}`];
    }, [count]);

    // 记忆化样式对象
    const dynamicStyle = useMemo(() => {
        return {
            padding: "20px",
            backgroundColor: count % 2 === 0 ? "#f0f0f0" : "#e0e0e0",
            color: count % 3 === 0 ? "red" : "black",
            transition: "all 0.3s ease",
        };
    }, [count]);

    // 记忆化函数 - 另一种选择（通常用 useCallback 更好）
    const memoizedFunction = useMemo(() => {
        return () => {
            console.log("记忆化函数被调用", count);
        };
    }, [count]);

    return (
        <div style={{ padding: "20px" }}>
            <h1>useMemo 示例</h1>

            <div>
                <p>计数: {count}</p>
                <button onClick={() => setCount(count + 1)}>增加计数</button>
            </div>

            <div>
                <input
                    type="text"
                    value={text}
                    onChange={e => setText(e.target.value)}
                    placeholder="输入文字..."
                />
            </div>

            <div>
                <h3>计算结果</h3>
                <p>使用 useMemo: {goodComputedValue}</p>
                <p>不使用 useMemo（控制台会看到频繁计算）: {badComputedValue}</p>
            </div>

            <div>
                <h3>过滤后的列表</h3>
                <ul>
                    {filteredList.map((item, index) => (
                        <li key={index}>{item}</li>
                    ))}
                </ul>
                <button onClick={() => setList([...list, list.length + 1])}>添加项目</button>
            </div>

            <div style={dynamicStyle}>
                <h3>用户信息（动态样式）</h3>
                <pre>{JSON.stringify(userInfo, null, 2)}</pre>
            </div>

            <div>
                <h3>选项列表</h3>
                <select>
                    {options.map((option, index) => (
                        <option key={index} value={option}>
                            {option}
                        </option>
                    ))}
                </select>
            </div>

            <button onClick={memoizedFunction} style={{ marginTop: "20px" }}>
                调用记忆化函数
            </button>
        </div>
    );
}
```

### useRef - 访问 DOM 和保存可变值

```jsx
import { useState, useRef, useEffect } from "react";

function RefDemo() {
    const [count, setCount] = useState(0);
    const inputRef = useRef(null);
    const previousCountRef = useRef();
    const renderCountRef = useRef(0);
    const intervalRef = useRef(null);

    // 1. 访问 DOM 元素
    const focusInput = () => {
        inputRef.current?.focus();
        inputRef.current?.select();
    };

    // 2. 保存上一次的值
    useEffect(() => {
        previousCountRef.current = count;
    }, [count]);

    // 3. 记录渲染次数
    renderCountRef.current += 1;

    // 4. 保存定时器 ID
    const startTimer = () => {
        if (intervalRef.current) return;

        intervalRef.current = setInterval(() => {
            setCount(prev => prev + 1);
        }, 1000);
    };

    const stopTimer = () => {
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }
    };

    // 5. 保存组件实例值（不会触发重新渲染）
    const saveData = () => {
        // 这不会触发重新渲染
        previousCountRef.current = count * 2;
        console.log("保存的数据:", previousCountRef.current);
    };

    // 6. 复杂的 DOM 操作
    const changeInputStyle = () => {
        if (inputRef.current) {
            inputRef.current.style.backgroundColor = "#ff0";
            inputRef.current.style.border = "2px solid red";
            inputRef.current.style.padding = "10px";
        }
    };

    // 7. 测量 DOM 元素
    const measureInput = () => {
        if (inputRef.current) {
            const rect = inputRef.current.getBoundingClientRect();
            console.log("输入框尺寸:", rect);
            alert(`宽度: ${rect.width}px, 高度: ${rect.height}px`);
        }
    };

    // 8. 组合使用多个 ref
    const divRefs = useRef([]);

    const highlightDiv = index => {
        divRefs.current[index].style.backgroundColor =
            divRefs.current[index].style.backgroundColor === "yellow" ? "white" : "yellow";
    };

    return (
        <div style={{ padding: "20px" }}>
            <h1>useRef 示例</h1>

            <div style={{ marginBottom: "20px" }}>
                <h3>计数: {count}</h3>
                <p>上一次计数: {previousCountRef.current}</p>
                <p>渲染次数: {renderCountRef.current}</p>
                <button onClick={() => setCount(count + 1)}>增加计数</button>
                <button onClick={saveData} style={{ marginLeft: "10px" }}>
                    保存数据（不触发渲染）
                </button>
            </div>

            <div style={{ marginBottom: "20px" }}>
                <h3>定时器控制</h3>
                <button onClick={startTimer}>开始定时器</button>
                <button onClick={stopTimer} style={{ marginLeft: "10px" }}>
                    停止定时器
                </button>
            </div>

            <div style={{ marginBottom: "20px" }}>
                <h3>DOM 操作</h3>
                <input
                    ref={inputRef}
                    type="text"
                    defaultValue="点击按钮聚焦我"
                    style={{ marginRight: "10px", padding: "5px" }}
                />
                <button onClick={focusInput}>聚焦输入框</button>
                <button onClick={changeInputStyle} style={{ marginLeft: "10px" }}>
                    改变样式
                </button>
                <button onClick={measureInput} style={{ marginLeft: "10px" }}>
                    测量尺寸
                </button>
            </div>

            <div style={{ marginBottom: "20px" }}>
                <h3>多个 ref 示例</h3>
                {[1, 2, 3].map((item, index) => (
                    <div
                        key={index}
                        ref={el => (divRefs.current[index] = el)}
                        style={{
                            padding: "10px",
                            margin: "5px",
                            border: "1px solid #ccc",
                            cursor: "pointer",
                        }}
                        onClick={() => highlightDiv(index)}
                    >
                        点击高亮 div {item}
                    </div>
                ))}
            </div>

            <div style={{ marginTop: "20px", padding: "10px", backgroundColor: "#f0f0f0" }}>
                <h4>useRef 特点总结：</h4>
                <ul>
                    <li>1. 返回的对象在整个组件生命周期中保持不变</li>
                    <li>2. 修改 .current 属性不会触发重新渲染</li>
                    <li>3. 常用于访问 DOM 元素、保存定时器 ID、存储可变值</li>
                    <li>4. 与 useState 不同，变化不会触发组件更新</li>
                </ul>
            </div>
        </div>
    );
}

// 9. 转发 ref（配合 forwardRef）
const FancyInput = React.forwardRef((props, ref) => {
    return <input ref={ref} className="fancy-input" {...props} />;
});

function ParentComponent() {
    const inputRef = useRef(null);

    const focusChildInput = () => {
        inputRef.current.focus();
        inputRef.current.style.border = "2px solid blue";
    };

    return (
        <div>
            <FancyInput ref={inputRef} />
            <button onClick={focusChildInput}>聚焦子组件输入框</button>
        </div>
    );
}
```

## 自定义 Hooks

### 创建自定义 Hook

```jsx
// 1. 自定义 Hook：获取窗口大小
import { useState, useEffect } from "react";

function useWindowSize() {
    const [windowSize, setWindowSize] = useState({
        width: window.innerWidth,
        height: window.innerHeight,
    });

    useEffect(() => {
        const handleResize = () => {
            setWindowSize({
                width: window.innerWidth,
                height: window.innerHeight,
            });
        };

        window.addEventListener("resize", handleResize);

        // 立即获取一次初始尺寸
        handleResize();

        return () => {
            window.removeEventListener("resize", handleResize);
        };
    }, []);

    return windowSize;
}

// 2. 自定义 Hook：倒计时
function useCountdown(initialTime) {
    const [timeLeft, setTimeLeft] = useState(initialTime);
    const [isRunning, setIsRunning] = useState(false);

    useEffect(() => {
        let timerId;

        if (isRunning && timeLeft > 0) {
            timerId = setTimeout(() => {
                setTimeLeft(timeLeft - 1);
            }, 1000);
        } else if (timeLeft === 0) {
            setIsRunning(false);
        }

        return () => {
            if (timerId) clearTimeout(timerId);
        };
    }, [isRunning, timeLeft]);

    const start = () => setIsRunning(true);
    const pause = () => setIsRunning(false);
    const reset = () => {
        setTimeLeft(initialTime);
        setIsRunning(false);
    };

    return {
        timeLeft,
        isRunning,
        start,
        pause,
        reset,
    };
}

// 3. 自定义 Hook：本地存储
function useLocalStorage(key, initialValue) {
    // 从 localStorage 获取初始值
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error("读取 localStorage 失败:", error);
            return initialValue;
        }
    });

    // 更新 localStorage 和状态
    const setValue = value => {
        try {
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error("写入 localStorage 失败:", error);
        }
    };

    // 移除 localStorage 项
    const removeValue = () => {
        try {
            window.localStorage.removeItem(key);
            setStoredValue(initialValue);
        } catch (error) {
            console.error("移除 localStorage 失败:", error);
        }
    };

    return [storedValue, setValue, removeValue];
}

// 4. 自定义 Hook：防抖
function useDebounce(value, delay) {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const timerId = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => {
            clearTimeout(timerId);
        };
    }, [value, delay]);

    return debouncedValue;
}

// 5. 自定义 Hook：API 请求
function useFetch(url, options = {}) {
    const [state, setState] = useState({
        data: null,
        loading: true,
        error: null,
    });

    useEffect(() => {
        const controller = new AbortController();

        const fetchData = async () => {
            try {
                setState(prev => ({ ...prev, loading: true }));

                const response = await fetch(url, {
                    ...options,
                    signal: controller.signal,
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                setState({ data, loading: false, error: null });
            } catch (error) {
                if (error.name !== "AbortError") {
                    setState({ data: null, loading: false, error: error.message });
                }
            }
        };

        fetchData();

        return () => {
            controller.abort();
        };
    }, [url]); // 依赖 url，url 变化时重新请求

    return state;
}

// 6. 使用自定义 Hooks 的组件
function CustomHooksDemo() {
    // 使用自定义 Hook：窗口大小
    const windowSize = useWindowSize();

    // 使用自定义 Hook：倒计时
    const countdown = useCountdown(10);

    // 使用自定义 Hook：本地存储
    const [name, setName, removeName] = useLocalStorage("username", "");

    // 使用自定义 Hook：防抖
    const [searchTerm, setSearchTerm] = useState("");
    const debouncedSearchTerm = useDebounce(searchTerm, 500);

    // 使用自定义 Hook：API 请求
    const { data, loading, error } = useFetch(
        debouncedSearchTerm ? `https://api.github.com/search/users?q=${debouncedSearchTerm}` : null
    );

    return (
        <div style={{ padding: "20px" }}>
            <h1>自定义 Hooks 示例</h1>

            {/* 窗口大小 */}
            <div style={{ padding: "10px", backgroundColor: "#f0f0f0", marginBottom: "20px" }}>
                <h3>窗口大小</h3>
                <p>
                    宽度: {windowSize.width}px, 高度: {windowSize.height}px
                </p>
            </div>

            {/* 倒计时 */}
            <div style={{ padding: "10px", backgroundColor: "#e8f4f8", marginBottom: "20px" }}>
                <h3>倒计时</h3>
                <p>剩余时间: {countdown.timeLeft}秒</p>
                <p>状态: {countdown.isRunning ? "运行中" : "已停止"}</p>
                <button
                    onClick={countdown.start}
                    disabled={countdown.isRunning || countdown.timeLeft === 0}
                >
                    开始
                </button>
                <button
                    onClick={countdown.pause}
                    disabled={!countdown.isRunning}
                    style={{ marginLeft: "10px" }}
                >
                    暂停
                </button>
                <button onClick={countdown.reset} style={{ marginLeft: "10px" }}>
                    重置
                </button>
            </div>

            {/* 本地存储 */}
            <div style={{ padding: "10px", backgroundColor: "#f8f8e8", marginBottom: "20px" }}>
                <h3>本地存储</h3>
                <input
                    type="text"
                    value={name}
                    onChange={e => setName(e.target.value)}
                    placeholder="输入用户名"
                    style={{ marginRight: "10px" }}
                />
                <button onClick={() => setName("")}>清空</button>
                <button onClick={removeName} style={{ marginLeft: "10px" }}>
                    移除存储
                </button>
                <p>存储的用户名: {name || "未设置"}</p>
            </div>

            {/* 防抖搜索 */}
            <div style={{ padding: "10px", backgroundColor: "#e8f8e8", marginBottom: "20px" }}>
                <h3>防抖搜索 GitHub 用户</h3>
                <input
                    type="text"
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                    placeholder="搜索 GitHub 用户..."
                />
                <p>搜索词: {searchTerm}</p>
                <p>防抖后: {debouncedSearchTerm}</p>
            </div>

            {/* API 请求结果 */}
            <div style={{ padding: "10px", backgroundColor: "#f0e8f8" }}>
                <h3>搜索结果</h3>
                {loading && <p>加载中...</p>}
                {error && <p style={{ color: "red" }}>错误: {error}</p>}
                {data && (
                    <div>
                        <p>找到 {data.total_count} 个用户</p>
                        <ul>
                            {data.items.slice(0, 5).map(user => (
                                <li key={user.id}>
                                    <img
                                        src={user.avatar_url}
                                        alt={user.login}
                                        width="30"
                                        style={{ verticalAlign: "middle", marginRight: "10px" }}
                                    />
                                    {user.login}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
}
```

## 其他内置 Hooks

### useImperativeHandle

```jsx
import { forwardRef, useImperativeHandle, useRef } from "react";

const FancyInput = forwardRef((props, ref) => {
    const inputRef = useRef();

    // 向父组件暴露特定的方法
    useImperativeHandle(ref, () => ({
        focus: () => {
            inputRef.current.focus();
        },
        setValue: value => {
            inputRef.current.value = value;
        },
        getValue: () => {
            return inputRef.current.value;
        },
        // 可以暴露任何自定义方法
        customMethod: () => {
            console.log("自定义方法被调用");
        },
    }));

    return <input ref={inputRef} {...props} />;
});

function Parent() {
    const fancyInputRef = useRef();

    const handleClick = () => {
        fancyInputRef.current.focus();
        fancyInputRef.current.setValue("Hello");
        console.log("当前值:", fancyInputRef.current.getValue());
        fancyInputRef.current.customMethod();
    };

    return (
        <div>
            <FancyInput ref={fancyInputRef} />
            <button onClick={handleClick}>操作输入框</button>
        </div>
    );
}
```

### useLayoutEffect

```jsx
import { useState, useLayoutEffect, useEffect, useRef } from "react";

function LayoutEffectDemo() {
    const [width, setWidth] = useState(0);
    const divRef = useRef();

    // useLayoutEffect 会在 DOM 更新后、浏览器绘制前同步执行
    useLayoutEffect(() => {
        console.log("useLayoutEffect 执行");

        // 测量 DOM 元素
        const newWidth = divRef.current.getBoundingClientRect().width;
        setWidth(newWidth);

        // 强制同步布局操作
        divRef.current.style.backgroundColor = "lightblue";

        // 清理函数
        return () => {
            console.log("useLayoutEffect 清理");
        };
    }, []);

    // useEffect 会在浏览器绘制后异步执行
    useEffect(() => {
        console.log("useEffect 执行");
        // 这里适合做数据获取、订阅等副作用
    }, []);

    return (
        <div>
            <h2>useLayoutEffect vs useEffect</h2>
            <div
                ref={divRef}
                style={{
                    padding: "20px",
                    border: "1px solid #ccc",
                    marginBottom: "10px",
                }}
            >
                这个 div 的宽度是: {width}px
            </div>
            <p>打开控制台查看执行顺序</p>
        </div>
    );
}
```

### useDebugValue

```jsx
import { useState, useEffect, useDebugValue } from "react";

// 自定义 Hook 使用 useDebugValue
function useFriendStatus(friendID) {
    const [isOnline, setIsOnline] = useState(null);

    // 在 React DevTools 中显示自定义标签
    useDebugValue(isOnline ? "在线" : "离线");

    useEffect(() => {
        // 模拟订阅好友状态
        const timer = setInterval(() => {
            setIsOnline(Math.random() > 0.5);
        }, 2000);

        return () => clearInterval(timer);
    }, [friendID]);

    return isOnline;
}

// 更复杂的示例
function useUser(userId) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // 延迟格式化调试值（避免昂贵的格式化操作影响性能）
    useDebugValue(user, user => (user ? `用户: ${user.name}` : "用户: 加载中..."));

    useEffect(() => {
        // 模拟 API 调用
        setTimeout(() => {
            setUser({
                id: userId,
                name: `用户${userId}`,
                email: `user${userId}@example.com`,
            });
            setLoading(false);
        }, 1000);
    }, [userId]);

    return { user, loading };
}

function DebugValueDemo() {
    const isOnline = useFriendStatus(1);
    const { user, loading } = useUser(1);

    return (
        <div>
            <h2>useDebugValue 示例</h2>
            <p>好友状态: {isOnline === null ? "加载中..." : isOnline ? "在线" : "离线"}</p>
            <p>用户信息: {loading ? "加载中..." : user.name}</p>
            <p>打开 React DevTools 查看 Hook 的调试值</p>
        </div>
    );
}
```

## Hooks 使用规则和最佳实践

### Hooks 使用规则

```jsx
// ❌ 错误：在条件语句中使用 Hook
function BadExample() {
    if (condition) {
        const [state, setState] = useState(0); // 错误！
    }

    // ❌ 错误：在循环中使用 Hook
    for (let i = 0; i < 10; i++) {
        const [value, setValue] = useState(i); // 错误！
    }

    // ❌ 错误：在嵌套函数中使用 Hook
    function nestedFunction() {
        const [value, setValue] = useState(0); // 错误！
    }

    return <div />;
}

// ✅ 正确：在顶层使用 Hook
function GoodExample({ condition }) {
    const [state, setState] = useState(0);
    const [value, setValue] = useState(0);

    // 可以在条件语句中使用 Hook 的返回值
    const conditionalValue = condition ? state : value;

    return <div />;
}
```

### 性能优化最佳实践

```jsx
function OptimizedComponent({ items, onItemClick }) {
    // 1. 使用 useMemo 记忆昂贵的计算
    const filteredItems = useMemo(() => {
        return items.filter(item => item.active);
    }, [items]);

    // 2. 使用 useCallback 记忆回调函数
    const handleClick = useCallback(
        itemId => {
            onItemClick(itemId);
        },
        [onItemClick]
    );

    // 3. 使用 useRef 保存不变量
    const renderCount = useRef(0);
    renderCount.current++;

    // 4. 拆分多个 useEffect
    useEffect(() => {
        // 只做一件事
        document.title = `渲染次数: ${renderCount.current}`;
    }, [renderCount.current]);

    // 5. 避免不必要的依赖
    useEffect(() => {
        const handleScroll = () => {
            console.log("滚动位置:", window.scrollY);
        };

        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []); // 空数组，只添加一次监听

    return (
        <div>
            {filteredItems.map(item => (
                <Item key={item.id} item={item} onClick={handleClick} />
            ))}
        </div>
    );
}
```

## 常见问题解决方案

### 无限循环问题

```jsx
function InfiniteLoopExample() {
    const [count, setCount] = useState(0);

    // ❌ 问题：每次渲染都更新状态，导致无限循环
    // useEffect(() => {
    //   setCount(count + 1); // 错误！
    // });

    // ✅ 解决方案1：添加正确的依赖
    useEffect(() => {
        console.log("count 变化:", count);
    }, [count]); // 指定依赖

    // ✅ 解决方案2：使用 useCallback 避免函数重复创建
    const fetchData = useCallback(async () => {
        const data = await getData(count);
        // 处理数据
    }, [count]); // 依赖 count

    // ✅ 解决方案3：使用 useRef 跟踪变化
    const mounted = useRef(false);
    useEffect(() => {
        if (mounted.current) {
            // 只在更新时执行，不在首次渲染时执行
            console.log("组件更新");
        } else {
            mounted.current = true;
        }
    });

    return <div>计数: {count}</div>;
}
```

### 依赖数组问题

```jsx
function DependencyArrayExample() {
    const [count, setCount] = useState(0);
    const [user, setUser] = useState({ name: "张三", age: 25 });

    // ❌ 问题：依赖数组不完整
    useEffect(() => {
        console.log("user 变化:", user.name);
    }, [user.name]); // 缺少 user.age 依赖（如果 user 对象变化）

    // ✅ 解决方案1：依赖完整的对象
    useEffect(() => {
        console.log("user 对象变化:", user);
    }, [user]); // 依赖整个 user 对象

    // ✅ 解决方案2：使用 useMemo 创建稳定对象
    const stableUser = useMemo(() => user, [user.name, user.age]);

    useEffect(() => {
        console.log("稳定 user 对象:", stableUser);
    }, [stableUser]);

    // ✅ 解决方案3：使用函数式更新避免依赖
    const increment = useCallback(() => {
        setCount(prevCount => prevCount + 1); // 不依赖 count
    }, []); // 空依赖数组

    return <div>示例</div>;
}
```

## 总结

### 核心要点

-   useState - 管理组件状态
-   useEffect - 处理副作用
-   useContext - 访问上下文
-   useReducer - 复杂状态管理
-   useCallback - 记忆化函数
-   useMemo - 记忆化值
-   useRef - 访问 DOM/保存可变值
-   自定义 Hooks - 逻辑复用

### 最佳实践：

-   只在 React 函数组件或自定义 Hook 中调用 Hook
-   只在最顶层使用 Hook
-   使用 ESLint 插件检查规则
-   合理使用依赖数组
-   避免不必要的重新渲染
