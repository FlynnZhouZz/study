# React 18 新特性

> 18 的核心不是新 API，是把渲染变成可中断的并发任务；`useTransition` 只是把这个能力交到你手里的开关。

## 并发渲染（Concurrent Rendering）

16/17 的渲染是同步递归：一旦开始 render，就必须一路走完才能回到浏览器，任务长了就掉帧。18 引入 Fiber 的双缓冲与时间切片后，render 阶段可以被更高优先级的任务打断——**打断的是 render，commit 仍然是一次性同步完成的**，因为 DOM 改到一半回滚代价太大。

| 维度 | React 17 | React 18 |
|---|---|---|
| 渲染方式 | 同步递归，不可中断 | 可中断的并发渲染 |
| 更新优先级 | 全部同级 | 按 lane 分优先级（用户输入 > 过渡更新） |
| 批量更新范围 | 仅 React 事件回调内 | 所有场景（含 setTimeout、Promise、原生事件） |
| 水合 | 同步，阻塞 | 可选择性地随时中断（配合 Suspense） |

并发特性是**可选的**：不用 `createRoot`、不用新 API，应用行为与 17 基本一致。

## Render API：createRoot 与 hydrateRoot

`ReactDOM.render` 在 18 中被标记为 legacy，调用会打印警告；并发特性只在 `createRoot` 下可用。

```jsx
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
// 卸载用 root.unmount()，而不是 ReactDOM.unmountComponentAtNode
```

SSR 场景对应 `hydrateRoot`：

```jsx
import { hydrateRoot } from 'react-dom/client';

hydrateRoot(document.getElementById('root'), <App />);
```

**注意**：`createRoot` 下 `StrictMode` 会在开发环境对组件做两次挂载（mount → unmount → mount），用来暴露副作用没清理干净的问题。很多人以为这是 bug，实际上它是在提前暴露你在 `useEffect` 里漏了 cleanup。

## 自动批处理（Automatic Batching）

17 只在 React 事件处理器里批处理 `setState`，18 扩展到所有场景：

```jsx
// React 17：setTimeout 里两次 setState 触发两次渲染
// React 18：同样只渲染一次
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
}, 0);
```

需要强制同步刷新时用 `flushSync`，但它会破坏批处理、引发额外布局计算，只在「拿到 DOM 立刻测量」这类场景使用：

```jsx
import { flushSync } from 'react-dom';

flushSync(() => setCount(c => c + 1));
// 此时 DOM 已更新，可以 measure
```

## 并发 Hooks

**useTransition**：把一次更新标记为「过渡」，让用户输入优先。

```jsx
const [isPending, startTransition] = useTransition();
const [keyword, setKeyword] = useState('');

function onChange(e) {
  setKeyword(e.target.value);          // 紧急：输入框必须立刻响应
  startTransition(() => {
    setList(filterLargeList(e.target.value)); // 非紧急：可以被打断
  });
}
```

**useDeferredValue**：拿不到 setState 时（比如值来自 props），用它的延迟副本：

```jsx
const deferredKeyword = useDeferredValue(keyword);
const list = useMemo(() => filterLargeList(deferredKeyword), [deferredKeyword]);
```

两者的区别：`useTransition` 控制的是「这次更新能不能等」，`useDeferredValue` 控制的是「这个值能不能用旧版本」。前者能拿到 `isPending`，后者不能。

## Suspense 与流式 SSR

18 的 `Suspense` 支持在数据层使用（配合支持 Suspense 的数据源）：

```jsx
<Suspense fallback={<Skeleton />}>
  <Comments />   {/* 内部 throw promise 时展示 fallback */}
</Suspense>
```

服务端可以用 `renderToPipeableStream` 边渲染边推送，让首屏先到、慢的部分后到。

## 其他 API 变化

| API | 用途 | 备注 |
|---|---|---|
| `useId` | 生成 SSR 安全的唯一 id | 用于 `label htmlFor`、`aria-*`，不能当列表 key |
| `useSyncExternalStore` | 订阅外部 store | 让非 React 状态源在并发下不撕裂，Redux 8 用它重写 |
| `useInsertionEffect` | 供 CSS-in-JS 注入样式 | 早于 `useLayoutEffect`，业务代码基本用不到 |
| `startTransition`（顶层导出） | 非 Hook 版本 | 在组件外调用时使用 |

`useId` 的一个真实用途：SSR 时 `Math.random()` 会导致服务端与客户端 id 不一致而水合失败，`useId` 生成的是基于树位置的稳定值。

## 常见误区

**很多人以为升级到 18 就自动变快**。实际上并发渲染只在用了 `startTransition` / `useDeferredValue` / Suspense 的场景才生效，普通 `setState` 的渲染路径没有变快，甚至因为 lane 调度多了一点开销。

**很多人以为 `startTransition` 里的更新一定不阻塞输入**。如果过渡更新本身的计算（比如 render 里有同步的重计算）超过一帧，主线程依然会被占住，该拆的计算还得拆。

**很多人以为 React 18 支持了「服务端组件」**。RSC 是 React 19 与 Next.js App Router 的范畴，18 只有流式 SSR 与选择性水合。

## 面试怎么答

**Q：18 的并发渲染和 Vue 的响应式更新，本质区别是什么？**
A：Vue 靠依赖追踪精确知道谁变了，更新粒度更细；React 靠重新执行函数组件得到新虚拟树再 diff。18 的并发是在「必须重新执行」这个前提下，把执行过程切成可中断的片段，用优先级决定先执行谁。所以 React 需要 `memo`/`useMemo` 人工控制重算范围，Vue 不需要。

**Q：为什么 commit 阶段不能中断？**
A：commit 会真实修改 DOM、触发 layout 与 paint，还要执行 `useLayoutEffect`。如果中途被打断，DOM 会停留在与新状态不一致的中间态，且已执行的生命周期无法回滚。所以 React 只把可丢弃的 render 阶段做成可中断。

**Q：自动批处理会带来什么坑？**
A：原来依赖「每次 setState 后 DOM 已更新」的代码会失效，比如在两次 setState 之间读 `ref.current` 的高度。跨组件通信中也有影响——子组件的 effect 不再紧随某个 setState 触发。

## 关联阅读

- [React 19 新特性](./08-React19新特性.md)
- [Fiber 架构](./11-Fiber架构.md)
- [useCallback 闭包陷阱](./09-useCallback闭包陷阱.md)
- [常用性能优化操作](./10-常用性能优化操作.md)
