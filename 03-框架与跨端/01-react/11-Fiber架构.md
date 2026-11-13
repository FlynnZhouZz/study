# Firbe 架构

Fiber 是 React 16+ 的核心重构，是一个增量式渲染引擎，使 React 支持：

-   可中断的渲染过程
-   优先级调度
-   更好的错误处理
-   异步渲染能力

## Fiber 的核心特性

### 1. 可中断的渲染

```jsx
// Fiber 之前：递归渲染（不可中断）
function render(element, container) {
    // 深度优先遍历，一旦开始不能中断
}

// Fiber 之后：链表结构（可中断）
class FiberNode {
    constructor(tag, pendingProps, key, mode) {
        this.tag = tag; // 组件类型
        this.key = key; // key
        this.elementType = null; // 元素类型
        this.stateNode = null; // 对应的真实DOM/Fiber
        this.return = null; // 父Fiber
        this.child = null; // 第一个子Fiber
        this.sibling = null; // 兄弟Fiber
        this.pendingProps = pendingProps;
        this.memoizedProps = null;
        this.memoizedState = null;
        this.updateQueue = null; // 更新队列
        this.mode = mode;
        this.effectTag = NoEffect;
        this.nextEffect = null; // 下一个有副作用的Fiber
        this.alternate = null; // 连接当前和workInProgress
    }
}
```

### 2. 双缓冲机制

```jsx
// current tree（当前显示） ↔ workInProgress tree（正在构建）
let workInProgress = null;
let current = null;

function performUnitOfWork(fiber) {
    // 开始构建 workInProgress tree
    // 完成后与 current tree 交换
}
```

## Fiber 工作流程

### 阶段 1：Reconciliation（协调阶段）

```jsx
// Fiber 的调度循环
function workLoop(deadline) {
    let shouldYield = false;

    while (nextUnitOfWork && !shouldYield) {
        nextUnitOfWork = performUnitOfWork(nextUnitOfWork);
        shouldYield = deadline.timeRemaining() < 1; // 检查剩余时间
    }

    if (!nextUnitOfWork && workInProgressRoot) {
        commitRoot(); // 提交到DOM
    }

    requestIdleCallback(workLoop); // 浏览器空闲时继续
}
```

### 阶段 2：Commit（提交阶段）

```jsx
function commitRoot() {
    // 不可中断，一次性完成DOM更新
    commitBeforeMutationEffects();
    commitMutationEffects();
    commitLayoutEffects();
}
```

## Fiber 的实际影响

### 1. Concurrent Mode（并发模式）

```jsx
// 启用并发特性
import { unstable_createRoot as createRoot } from "react-dom";

const root = createRoot(document.getElementById("root"));
root.render(<App />);

// 或使用新的 API
import { createRoot } from "react-dom/client";

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<App />);
```

### 2. Suspense 数据获取

```jsx
// 异步组件加载
const ProfilePage = React.lazy(() => import("./ProfilePage"));

function App() {
    return (
        <Suspense fallback={<Spinner />}>
            <ProfilePage />
        </Suspense>
    );
}

// 异步数据获取
function ProfileDetails() {
    const resource = fetchProfileData();
    return (
        <Suspense fallback={<h2>Loading profile...</h2>}>
            <ProfileTimeline resource={resource} />
        </Suspense>
    );
}
```

### 3. 优先级调度

```jsx
// 不同优先级的更新
import {
    unstable_runWithPriority,
    unstable_NormalPriority,
    unstable_UserBlockingPriority,
} from "scheduler";

// 用户交互（高优先级）
function handleClick() {
    unstable_runWithPriority(unstable_UserBlockingPriority, () => {
        setState(newState);
    });
}

// 数据加载（低优先级）
function loadData() {
    unstable_runWithPriority(unstable_NormalPriority, () => {
        setState(newState);
    });
}
```

## Fiber 的性能优化

### 时间切片（Time Slicing）

```jsx
// 长列表渲染优化
function LongList() {
  const items = useMemo(() => /* 大量数据 */, []);

  return (
    <div>
      {items.map(item => (
        // 每个 Item 的渲染可能会被中断
        <ListItem key={item.id} item={item} />
      ))}
    </div>
  );
}
```

### 过渡更新（Transitions）

```jsx
import { startTransition, useTransition } from "react";

// 标记非紧急更新
function App() {
    const [isPending, startTransition] = useTransition();
    const [tab, setTab] = useState("home");

    function selectTab(nextTab) {
        startTransition(() => {
            setTab(nextTab); // 非紧急更新
        });
    }

    return (
        <>
            {isPending && <Spinner />}
            <TabButton onClick={() => selectTab("home")}>Home</TabButton>
            <TabButton onClick={() => selectTab("about")}>About</TabButton>
            <TabContent tab={tab} />
        </>
    );
}
```

## 错误边界（Error Boundaries）

```jsx
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        // 记录错误
        logErrorToService(error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return <FallbackUI />;
        }

        return this.props.children;
    }
}

// 使用
<ErrorBoundary>
    <MyComponent />
</ErrorBoundary>;
```

## Fiber 调试工具

```jsx
// 1. React DevTools 中的 Fiber 树
// 2. 性能分析
import { unstable_trace as trace } from "scheduler/tracing";

trace("my event", performance.now(), () => {
    // 更新操作
});

// 3. 使用 Profiler API
<Profiler id="App" onRender={onRenderCallback}>
    <App />
</Profiler>;
```

## 实际应用示例

```jsx
// 优化大型应用渲染
function OptimizedApp() {
    const [input, setInput] = useState("");
    const [results, setResults] = useState([]);

    // 用户输入：紧急更新
    const handleInputChange = e => {
        setInput(e.target.value); // 同步更新

        // 搜索：非紧急更新
        startTransition(() => {
            const newResults = performSearch(e.target.value);
            setResults(newResults);
        });
    };

    return (
        <div>
            <input value={input} onChange={handleInputChange} />
            <Suspense fallback={<Loading />}>
                <SearchResults results={results} />
            </Suspense>
        </div>
    );
}
```
