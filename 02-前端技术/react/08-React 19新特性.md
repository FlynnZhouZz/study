# React 19 新特性

## React 19 概览

React 19 是一次重大更新，引入了许多开发者期待已久的特性：

### 主要新特性

-   React Compiler（React 编译器）
-   Actions API（服务端 Actions）
-   use() Hook（资源处理）
-   Document Metadata（文档元数据）
-   Asset Loading（资源加载优化）
-   Web Components 集成
-   新的 Hooks
-   性能优化改进

## React Compiler（React 编译器）

### 什么是 React Compiler

React Compiler 是一个构建时编译器，可以自动优化 React 组件的重新渲染。

```jsx
// 编译前 - 需要手动优化的代码
function MyComponent({ items }) {
    const [count, setCount] = useState(0);
    const filteredItems = items.filter(item => item.active);

    return (
        <div>
            <button onClick={() => setCount(count + 1)}>Count: {count}</button>
            <ItemList items={filteredItems} />
        </div>
    );
}

// 编译后 - React Compiler 自动优化
// 编译器会自动识别：
// 1. filteredItems 只依赖于 items
// 2. items 变化时才重新计算 filteredItems
// 3. count 变化时不重新计算 filteredItems
```

### 编译器优化示例

```jsx
// 示例1: 自动 memoization
function UserProfile({ user }) {
    // 编译器自动记忆化计算
    const fullName = `${user.firstName} ${user.lastName}`;
    const isAdult = user.age >= 18;

    return (
        <div>
            <h1>{fullName}</h1>
            <p>{isAdult ? "成年人" : "未成年人"}</p>
            <UserDetails user={user} />
        </div>
    );
}

// 编译器自动转换为类似这样：
// const fullName = useMemo(() => `${user.firstName} ${user.lastName}`, [user]);
// const isAdult = useMemo(() => user.age >= 18, [user]);

// 示例2: 自动 useCallback
function ProductList({ products, onSelect }) {
    const handleSelect = productId => {
        onSelect(productId);
    };

    // 编译器自动转换为：
    // const handleSelect = useCallback((productId) => {
    //   onSelect(productId);
    // }, [onSelect]);

    return (
        <ul>
            {products.map(product => (
                <ProductItem key={product.id} product={product} onSelect={handleSelect} />
            ))}
        </ul>
    );
}
```

### 编译器配置

```jsx
// next.config.js (Next.js 项目)
module.exports = {
    experimental: {
        reactCompiler: {
            compilationMode: "annotation", // or 'all'
            panicThreshold: "CRITICAL_ONLY",
        },
    },
};

// vite.config.js (Vite 项目)
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [
        react({
            babel: {
                plugins: [
                    [
                        "babel-plugin-react-compiler",
                        {
                            compilationMode: "annotation",
                            sources: filename => {
                                return filename.indexOf("node_modules") === -1;
                            },
                        },
                    ],
                ],
            },
        }),
    ],
});

// 手动控制优化
import { useMemo, useCallback } from "react";

// 使用 "use no memo" 指令禁用优化
function Component() {
    // $useMemo
    const value = computeExpensiveValue();

    // $useCallback
    const handler = () => {
        console.log("handler");
    };

    return <div />;
}
```

## Actions API（服务端 Actions）

### 基础使用

```jsx
// 服务端 Action (app/actions.js)
"use server";

export async function addToCart(productId, quantity) {
    // 可以直接访问数据库
    const cart = await db.cart.addItem(productId, quantity);

    // 重新验证数据
    revalidatePath("/cart");
    revalidateTag("cart");

    return cart;
}

export async function updateProfile(userId, data) {
    try {
        await db.users.update(userId, data);
        return { success: true };
    } catch (error) {
        return {
            success: false,
            error: error.message,
        };
    }
}

// 客户端组件使用 Action
("use client");

import { addToCart, updateProfile } from "@/app/actions";
import { useActionState, useOptimistic } from "react";

function AddToCartButton({ productId }) {
    // useActionState 处理 Action 状态
    const [state, formAction, isPending] = useActionState(
        addToCart,
        null,
        productId // 初始参数
    );

    return (
        <form action={formAction}>
            <input type="hidden" name="productId" value={productId} />
            <button type="submit" disabled={isPending}>
                {isPending ? "添加中..." : "加入购物车"}
            </button>
            {state?.error && <p className="error">{state.error}</p>}
        </form>
    );
}

// 表单 Action 示例
function ProfileForm({ userId, initialData }) {
    const [state, action, isPending] = useActionState(updateProfile, { success: false }, userId);

    return (
        <form action={action}>
            <input name="name" defaultValue={initialData.name} required />
            <input name="email" type="email" defaultValue={initialData.email} required />
            <button type="submit" disabled={isPending}>
                {isPending ? "保存中..." : "保存"}
            </button>
            {state.success && <p>保存成功！</p>}
            {state.error && <p className="error">{state.error}</p>}
        </form>
    );
}
```

### 乐观更新 (Optimistic Updates)

```jsx
import { useOptimistic, useActionState } from "react";

function LikeButton({ postId, initialLikes, hasLiked }) {
    const [optimisticLikes, addOptimisticLike] = useOptimistic(
        { likes: initialLikes, hasLiked },
        (state, newLike) => ({
            likes: state.likes + (newLike ? 1 : -1),
            hasLiked: newLike,
        })
    );

    const [state, action, isPending] = useActionState(
        async (prevState, formData) => {
            const shouldLike = !optimisticLikes.hasLiked;

            // 立即进行乐观更新
            addOptimisticLike(shouldLike);

            try {
                await toggleLike(postId);
                return { success: true };
            } catch (error) {
                // 发生错误时，乐观更新会被回滚
                return {
                    success: false,
                    error: error.message,
                };
            }
        },
        { success: false }
    );

    return (
        <form action={action}>
            <button
                type="submit"
                disabled={isPending}
                className={optimisticLikes.hasLiked ? "liked" : ""}
            >
                ❤️ {optimisticLikes.likes}
            </button>
        </form>
    );
}

// 购物车乐观更新示例
function CartItem({ item }) {
    const [optimisticQuantity, setOptimisticQuantity] = useOptimistic(
        item.quantity,
        (currentQuantity, newQuantity) => newQuantity
    );

    const updateQuantity = async newQuantity => {
        setOptimisticQuantity(newQuantity);

        try {
            await updateCartItem(item.id, newQuantity);
        } catch (error) {
            // 错误处理：显示通知，恢复原数量
            showNotification("更新失败");
            setOptimisticQuantity(item.quantity);
        }
    };

    return (
        <div className="cart-item">
            <span>{item.name}</span>
            <div className="quantity-controls">
                <button
                    onClick={() => updateQuantity(optimisticQuantity - 1)}
                    disabled={optimisticQuantity <= 1}
                >
                    -
                </button>
                <span>{optimisticQuantity}</span>
                <button
                    onClick={() => updateQuantity(optimisticQuantity + 1)}
                    disabled={optimisticQuantity >= item.stock}
                >
                    +
                </button>
            </div>
        </div>
    );
}
```

### 渐进式增强

```jsx
// 支持 JavaScript 禁用的情况
function SearchForm() {
    return (
        <form
            action="/api/search"
            method="GET"
            // JavaScript 可用时增强体验
            onSubmit={async e => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const query = formData.get("query");

                // 客户端搜索
                const results = await clientSearch(query);
                updateResults(results);
            }}
        >
            <input type="search" name="query" placeholder="搜索..." required />
            <button type="submit">搜索</button>
        </form>
    );
}

// 文件上传 Action
("use server");

export async function uploadFile(formData) {
    const file = formData.get("file");

    if (!file) {
        throw new Error("请选择文件");
    }

    // 保存到云存储
    const url = await saveToCloudStorage(file);

    // 保存到数据库
    await db.files.create({
        name: file.name,
        url,
        size: file.size,
        type: file.type,
    });

    return { url };
}

// 客户端文件上传
("use client");

function FileUpload() {
    const [state, action, isPending] = useActionState(uploadFile, null);
    const [progress, setProgress] = useState(0);

    const handleSubmit = async e => {
        e.preventDefault();
        const formData = new FormData(e.target);

        // 显示上传进度
        const xhr = new XMLHttpRequest();
        xhr.upload.addEventListener("progress", event => {
            if (event.lengthComputable) {
                const percent = Math.round((event.loaded / event.total) * 100);
                setProgress(percent);
            }
        });

        await action(formData);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" name="file" required />
            <button type="submit" disabled={isPending}>
                {isPending ? `上传中 ${progress}%` : "上传"}
            </button>
            {state?.url && (
                <div>
                    <p>上传成功！</p>
                    <a href={state.url} target="_blank">
                        查看文件
                    </a>
                </div>
            )}
        </form>
    );
}
```

## use() Hook（资源处理）

### 基础使用

```jsx
// 使用 Promise
function UserData({ userId }) {
    // use() 可以读取 Promise
    const user = use(fetchUser(userId));

    return (
        <div>
            <h1>{user.name}</h1>
            <p>{user.email}</p>
        </div>
    );
}

// 使用 Context
const ThemeContext = createContext("light");

function ThemeConsumer() {
    // use() 可以读取 Context
    const theme = use(ThemeContext);

    return <div className={`theme-${theme}`}>当前主题: {theme}</div>;
}

// 在循环中使用
function UserList({ userIds }) {
    return (
        <ul>
            {userIds.map(userId => (
                <Suspense key={userId} fallback={<li>加载中...</li>}>
                    <UserListItem userId={userId} />
                </Suspense>
            ))}
        </ul>
    );
}

function UserListItem({ userId }) {
    // 每个列表项都有自己的 Suspense 边界
    const user = use(fetchUser(userId));

    return <li>{user.name}</li>;
}
```

### 与 Suspense 结合

```jsx
// 异步数据获取组件
function AsyncData({ promise }) {
    try {
        const data = use(promise);
        return <DataDisplay data={data} />;
    } catch (error) {
        if (error.then) {
            // 仍在加载，抛出 Promise 让 Suspense 处理
            throw error;
        }
        // 其他错误
        throw error;
    }
}

// 完整示例
function UserDashboard({ userId }) {
    return (
        <div className="dashboard">
            <Suspense fallback={<ProfileSkeleton />}>
                <UserProfile userId={userId} />
            </Suspense>

            <Suspense fallback={<PostsSkeleton />}>
                <UserPosts userId={userId} />
            </Suspense>

            <Suspense fallback={<StatsSkeleton />}>
                <UserStats userId={userId} />
            </Suspense>
        </div>
    );
}

function UserProfile({ userId }) {
    // 并行获取多个资源
    const user = use(fetchUser(userId));
    const posts = use(fetchUserPosts(userId));
    const stats = use(fetchUserStats(userId));

    return (
        <div className="profile">
            <img src={user.avatar} alt={user.name} />
            <h1>{user.name}</h1>
            <p>帖子数: {posts.length}</p>
            <p>关注者: {stats.followers}</p>
        </div>
    );
}

// 错误边界处理
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    render() {
        if (this.state.hasError) {
            return this.props.fallback || <div>加载失败</div>;
        }
        return this.props.children;
    }
}

// 使用示例
function App() {
    return (
        <ErrorBoundary fallback={<ErrorMessage />}>
            <Suspense fallback={<LoadingSpinner />}>
                <UserDashboard userId="123" />
            </Suspense>
        </ErrorBoundary>
    );
}
```

### 条件渲染和循环

```jsx
// 条件渲染
function ConditionalData({ shouldFetch, query }) {
    if (!shouldFetch) {
        return <div>不需要获取数据</div>;
    }

    // 只有在 shouldFetch 为 true 时才获取数据
    const data = use(fetchData(query));
    return <DataDisplay data={data} />;
}

// 循环中使用 use()
function DataGrid({ ids }) {
    return (
        <div className="grid">
            {ids.map(id => (
                <Suspense key={id} fallback={<GridItemSkeleton />}>
                    <DataItem id={id} />
                </Suspense>
            ))}
        </div>
    );
}

function DataItem({ id }) {
    const data = use(fetchItem(id));
    return (
        <div className="grid-item">
            <h3>{data.title}</h3>
            <p>{data.description}</p>
        </div>
    );
}

// 避免瀑布流问题
function OptimizedDashboard({ userId }) {
    // 提前开始所有数据请求
    const userPromise = fetchUser(userId);
    const postsPromise = fetchUserPosts(userId);
    const statsPromise = fetchUserStats(userId);

    return (
        <div>
            <Suspense fallback={<div>加载用户信息...</div>}>
                <UserProfile
                    userPromise={userPromise}
                    postsPromise={postsPromise}
                    statsPromise={statsPromise}
                />
            </Suspense>
        </div>
    );
}

function UserProfile({ userPromise, postsPromise, statsPromise }) {
    // 并行读取所有 Promise
    const user = use(userPromise);
    const posts = use(postsPromise);
    const stats = use(statsPromise);

    return (
        <div>
            <h1>{user.name}</h1>
            <p>帖子数: {posts.length}</p>
            <p>关注者: {stats.followers}</p>
        </div>
    );
}
```

## Document Metadata（文档元数据）

### 内置元数据组件

```jsx
// 在任意组件中直接使用
function BlogPost({ post }) {
    return (
        <>
            {/* 自动注入到 <head> */}
            <title>{post.title} - 我的博客</title>
            <meta name="description" content={post.excerpt} />
            <meta name="keywords" content={post.tags.join(", ")} />
            <link rel="canonical" href={`https://example.com/posts/${post.slug}`} />

            {/* Open Graph 标签 */}
            <meta property="og:title" content={post.title} />
            <meta property="og:description" content={post.excerpt} />
            <meta property="og:image" content={post.featuredImage} />
            <meta property="og:type" content="article" />

            {/* Twitter 卡片 */}
            <meta name="twitter:card" content="summary_large_image" />
            <meta name="twitter:title" content={post.title} />
            <meta name="twitter:description" content={post.excerpt} />
            <meta name="twitter:image" content={post.featuredImage} />

            {/* 结构化数据 */}
            <script type="application/ld+json">
                {JSON.stringify({
                    "@context": "https://schema.org",
                    "@type": "BlogPosting",
                    headline: post.title,
                    description: post.excerpt,
                    image: post.featuredImage,
                    author: {
                        "@type": "Person",
                        name: post.author.name,
                    },
                })}
            </script>

            {/* 页面内容 */}
            <article>
                <h1>{post.title}</h1>
                <div dangerouslySetInnerHTML={{ __html: post.content }} />
            </article>
        </>
    );
}

// 动态更新元数据
function ProductPage({ productId }) {
    const product = use(fetchProduct(productId));

    return (
        <>
            <title>{product.name} - 在线商店</title>
            <meta name="description" content={product.description} />
            <meta property="og:title" content={product.name} />
            <meta property="og:price:amount" content={product.price} />
            <meta property="og:price:currency" content="CNY" />

            <div className="product-page">
                <ProductDetails product={product} />
                <RelatedProducts productId={productId} />
            </div>
        </>
    );
}

// 嵌套路由中的元数据
function AppLayout({ children }) {
    return (
        <>
            {/* 全局元数据 */}
            <title>我的应用</title>
            <meta charSet="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <link rel="icon" href="/favicon.ico" />

            {/* 布局内容 */}
            <header>网站头部</header>
            <main>{children}</main>
            <footer>网站底部</footer>
        </>
    );
}

function HomePage() {
    return (
        <>
            {/* 覆盖全局 title */}
            <title>首页 - 我的应用</title>
            <meta name="description" content="欢迎来到我的应用首页" />

            <div className="home">
                <HeroSection />
                <Features />
            </div>
        </>
    );
}
```

### 高级用法

```jsx
// 脚本和样式管理
function AnalyticsScript() {
    return (
        <>
            <script async src="https://analytics.example.com/script.js" />
            <script
                dangerouslySetInnerHTML={{
                    __html: `
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'GA_MEASUREMENT_ID');
        `,
                }}
            />
        </>
    );
}

// 条件元数据
function DynamicPage({ type }) {
    const metadata = {
        blog: {
            title: "博客文章",
            description: "阅读我们的博客文章",
            keywords: "博客,文章,阅读",
        },
        product: {
            title: "产品详情",
            description: "查看产品详情",
            keywords: "产品,购买,详情",
        },
        about: {
            title: "关于我们",
            description: "了解我们的故事",
            keywords: "关于,团队,历史",
        },
    };

    const meta = metadata[type] || metadata.blog;

    return (
        <>
            <title>{meta.title}</title>
            <meta name="description" content={meta.description} />
            <meta name="keywords" content={meta.keywords} />

            <PageContent type={type} />
        </>
    );
}

// 主题颜色和 PWA 支持
function PWAConfig() {
    return (
        <>
            {/* PWA 配置 */}
            <link rel="manifest" href="/manifest.json" />
            <meta name="theme-color" content="#3b82f6" />
            <meta name="apple-mobile-web-app-capable" content="yes" />
            <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
            <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

            {/* 深色模式支持 */}
            <meta name="color-scheme" content="light dark" />
            <meta name="supported-color-schemes" content="light dark" />
        </>
    );
}

// 响应式元数据
function ResponsiveMeta() {
    return (
        <>
            {/* 响应式设计 */}
            <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5" />

            {/* 移动端特定配置 */}
            <meta name="format-detection" content="telephone=no" />
            <meta name="mobile-web-app-capable" content="yes" />

            {/* 平板设备优化 */}
            <meta name="apple-mobile-web-app-capable" content="yes" />
            <meta name="apple-mobile-web-app-status-bar-style" content="black" />
        </>
    );
}
```

## Asset Loading（资源加载优化）

### 预加载和预连接

```jsx
function OptimizedPage() {
    return (
        <>
            {/* 预加载关键资源 */}
            <link
                rel="preload"
                href="/fonts/inter.woff2"
                as="font"
                type="font/woff2"
                crossOrigin="anonymous"
            />
            <link
                rel="preload"
                href="/hero-image.jpg"
                as="image"
                imagesrcset="..."
                imagesizes="..."
            />

            {/* 预连接到第三方域名 */}
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="dns-prefetch" href="https://api.example.com" />

            {/* 预获取可能需要的资源 */}
            <link rel="prefetch" href="/about" as="document" />
            <link rel="prefetch" href="/products.json" as="fetch" />

            {/* 页面内容 */}
            <HeroSection />
            <Features />
        </>
    );
}

// 动态资源加载
function ProductImage({ productId, priority = false }) {
    const imageUrl = `/products/${productId}.jpg`;

    return (
        <>
            {priority && <link rel="preload" href={imageUrl} as="image" />}
            <img
                src={imageUrl}
                alt="产品图片"
                loading={priority ? "eager" : "lazy"}
                decoding={priority ? "sync" : "async"}
            />
        </>
    );
}

// 字体加载优化
function FontOptimization() {
    return (
        <>
            {/* 字体预加载 */}
            <link
                rel="preload"
                href="/fonts/inter-regular.woff2"
                as="font"
                type="font/woff2"
                crossOrigin="anonymous"
            />

            {/* 字体显示策略 */}
            <style>
                {`
          @font-face {
            font-family: 'Inter';
            font-style: normal;
            font-weight: 400;
            font-display: swap;
            src: url('/fonts/inter-regular.woff2') format('woff2');
          }
          .font-loading {
            font-family: system-ui, sans-serif;
          }
          .font-loaded {
            font-family: 'Inter', system-ui, sans-serif;
          }
        `}
            </style>

            {/* 字体加载检测 */}
            <script
                dangerouslySetInnerHTML={{
                    __html: `
          document.fonts.load('1em Inter').then(() => {
            document.documentElement.classList.add('font-loaded');
            document.documentElement.classList.remove('font-loading');
          });
        `,
                }}
            />
        </>
    );
}
```

### 图片优化

```jsx
function OptimizedImage({ src, alt, ...props }) {
    const [isLoaded, setIsLoaded] = useState(false);

    return (
        <>
            {/* 预加载 LCP 图片 */}
            <link
                rel="preload"
                href={src}
                as="image"
                imagesrcset={`${src}?w=640 640w, ${src}?w=768 768w, ${src}?w=1024 1024w`}
                imagesizes="(max-width: 768px) 100vw, 50vw"
            />

            {/* 图片元素 */}
            <img
                src={src}
                alt={alt}
                loading="lazy"
                decoding="async"
                onLoad={() => setIsLoaded(true)}
                className={`image ${isLoaded ? "loaded" : "loading"}`}
                style={{
                    contentVisibility: "auto",
                    containIntrinsicSize: "400px 300px",
                }}
                {...props}
            />

            {/* 内联 LQIP (Low Quality Image Placeholder) */}
            <style>{`
        .image.loading {
          background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
          background-size: 200% 100%;
          animation: loading 1.5s infinite;
        }
        @keyframes loading {
          0% { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
      `}</style>
        </>
    );
}

// 响应式图片组件
function ResponsiveImage({ src, alt, sizes, srcSet, quality = 75, format = "webp" }) {
    const baseUrl = `https://images.example.com`;
    const params = new URLSearchParams({
        q: quality,
        fm: format,
        fit: "crop",
        crop: "faces",
    });

    const generateSrcSet = widths => {
        return widths.map(width => `${baseUrl}?w=${width}&${params} ${width}w`).join(", ");
    };

    return (
        <img
            src={`${baseUrl}?w=800&${params}`}
            alt={alt}
            srcSet={srcSet || generateSrcSet([320, 480, 640, 768, 1024, 1280])}
            sizes={sizes || "(max-width: 768px) 100vw, 50vw"}
            loading="lazy"
            decoding="async"
        />
    );
}
```

## Web Components 集成

### 直接使用 Web Components

```jsx
function WebComponentDemo() {
    const [count, setCount] = useState(0);

    useEffect(() => {
        // 监听 Web Component 事件
        const element = document.querySelector("my-counter");
        const handleCountChange = event => {
            setCount(event.detail.count);
        };

        element.addEventListener("count-change", handleCountChange);

        return () => {
            element.removeEventListener("count-change", handleCountChange);
        };
    }, []);

    return (
        <div>
            <h2>Web Components 集成</h2>

            {/* 直接使用自定义元素 */}
            <my-counter count={count} onCountChange={e => setCount(e.detail.count)} />

            <my-slider
                min="0"
                max="100"
                value="50"
                onSliderChange={e => console.log("Slider:", e.detail.value)}
            />

            {/* 传递复杂数据 */}
            <my-data-grid
                data={JSON.stringify([
                    { id: 1, name: "Alice" },
                    { id: 2, name: "Bob" },
                ])}
                columns={JSON.stringify(["id", "name"])}
            />
        </div>
    );
}

// 封装 Web Components 为 React 组件
function MyCounter({ count, onCountChange }) {
    const ref = useRef();

    useEffect(() => {
        const element = ref.current;
        if (!element) return;

        const handleCountChange = event => {
            onCountChange?.(event.detail.count);
        };

        element.addEventListener("count-change", handleCountChange);

        return () => {
            element.removeEventListener("count-change", handleCountChange);
        };
    }, [onCountChange]);

    useEffect(() => {
        if (ref.current) {
            ref.current.count = count;
        }
    }, [count]);

    return <my-counter ref={ref} />;
}

// 使用封装的组件
function App() {
    const [count, setCount] = useState(0);

    return (
        <div>
            <MyCounter count={count} onCountChange={setCount} />
            <p>React 状态: {count}</p>
        </div>
    );
}
```

### 双向绑定

```jsx
// Web Component 表单元素
function WebComponentForm() {
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        rating: 3,
    });

    const handleInput = field => event => {
        setFormData(prev => ({
            ...prev,
            [field]: event.detail.value,
        }));
    };

    return (
        <form>
            <my-input label="姓名" value={formData.name} onMyInput={handleInput("name")} required />

            <my-input
                type="email"
                label="邮箱"
                value={formData.email}
                onMyInput={handleInput("email")}
                required
            />

            <my-rating value={formData.rating} onRatingChange={handleInput("rating")} max={5} />

            <button type="submit">提交</button>
        </form>
    );
}

// 自定义元素工厂
function createWebComponentWrapper(TagName, { events = {}, props = {} } = {}) {
    return React.forwardRef(({ children, ...rest }, ref) => {
        const elementRef = useRef();

        // 合并 ref
        useImperativeHandle(ref, () => elementRef.current);

        // 处理事件
        useEffect(() => {
            const element = elementRef.current;
            if (!element) return;

            const listeners = [];

            Object.entries(events).forEach(([eventName, handler]) => {
                if (rest[handler]) {
                    const listener = event => rest[handler](event);
                    element.addEventListener(eventName, listener);
                    listeners.push([eventName, listener]);
                }
            });

            return () => {
                listeners.forEach(([eventName, listener]) => {
                    element.removeEventListener(eventName, listener);
                });
            };
        }, [rest]);

        // 处理属性
        useEffect(() => {
            const element = elementRef.current;
            if (!element) return;

            Object.entries(props).forEach(([propName, propValue]) => {
                if (rest[propName] !== undefined) {
                    element[propName] = rest[propName];
                }
            });
        }, [rest]);

        return React.createElement(
            TagName,
            {
                ref: elementRef,
                ...rest,
            },
            children
        );
    });
}

// 使用工厂创建组件
const MyRating = createWebComponentWrapper("my-rating", {
    events: {
        "rating-change": "onRatingChange",
    },
    props: ["value", "max", "readonly"],
});

// 使用
function RatingDemo() {
    const [rating, setRating] = useState(3);

    return (
        <div>
            <MyRating value={rating} onRatingChange={e => setRating(e.detail.value)} max={5} />
            <p>当前评分: {rating}</p>
        </div>
    );
}
```

## 新的 Hooks 和 API

### useFormStatus

```jsx
// 表单状态 Hook
function SubmitButton() {
    const { pending, data, method, action } = useFormStatus();

    return (
        <button type="submit" disabled={pending} aria-disabled={pending}>
            {pending ? (
                <>
                    <Spinner />
                    提交中...
                </>
            ) : (
                "提交表单"
            )}
        </button>
    );
}

// 完整表单示例
function ContactForm() {
    const formRef = useRef();
    const { pending, data } = useFormStatus();

    useEffect(() => {
        if (!pending && data) {
            // 表单提交完成
            console.log("表单数据:", Object.fromEntries(data));
            formRef.current?.reset();
        }
    }, [pending, data]);

    return (
        <form ref={formRef} action="/api/contact" method="POST">
            <input name="name" placeholder="姓名" required />
            <input name="email" type="email" placeholder="邮箱" required />
            <textarea name="message" placeholder="消息" rows={4} required />

            <SubmitButton />

            {pending && <div className="form-status">正在提交表单...</div>}
        </form>
    );
}

// 嵌套表单状态
function MultiStepForm() {
    const [step, setStep] = useState(1);
    const { pending } = useFormStatus();

    return (
        <form action="/api/multi-step" method="POST">
            {step === 1 && <Step1 onNext={() => setStep(2)} />}

            {step === 2 && <Step2 onPrev={() => setStep(1)} onNext={() => setStep(3)} />}

            {step === 3 && <Step3 onPrev={() => setStep(2)} pending={pending} />}
        </form>
    );
}

function Step3({ onPrev, pending }) {
    const { data } = useFormStatus();

    return (
        <div>
            <h3>确认信息</h3>
            {data && (
                <div className="review">
                    <p>姓名: {data.get("name")}</p>
                    <p>邮箱: {data.get("email")}</p>
                    {/* 其他字段 */}
                </div>
            )}

            <div className="form-actions">
                <button type="button" onClick={onPrev}>
                    上一步
                </button>
                <button type="submit" disabled={pending}>
                    {pending ? "提交中..." : "确认提交"}
                </button>
            </div>
        </div>
    );
}
```

### useFormState（已重命名为 useActionState）

```jsx
// 替代原来的 useFormState
function SearchForm() {
    const [state, formAction, isPending] = useActionState(
        async (prevState, formData) => {
            const query = formData.get("query");
            const results = await search(query);
            return { results, query };
        },
        { results: [], query: "" }
    );

    return (
        <div>
            <form action={formAction}>
                <input name="query" defaultValue={state.query} placeholder="搜索..." />
                <button type="submit" disabled={isPending}>
                    {isPending ? "搜索中..." : "搜索"}
                </button>
            </form>

            {state.results.length > 0 && <SearchResults results={state.results} />}
        </div>
    );
}
```

### useOptimistic（乐观更新）

```jsx
// 完整聊天应用示例
function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [optimisticMessages, addOptimisticMessage] = useOptimistic(
        messages,
        (state, newMessage) => [...state, { ...newMessage, sending: true }]
    );

    const sendMessage = async text => {
        const message = {
            id: Date.now().toString(),
            text,
            timestamp: new Date(),
            user: "me",
            sending: true,
        };

        // 立即显示消息
        addOptimisticMessage(message);

        try {
            // 发送到服务器
            const response = await fetch("/api/messages", {
                method: "POST",
                body: JSON.stringify({ text }),
            });

            const savedMessage = await response.json();

            // 更新实际消息（移除 sending 状态）
            setMessages(prev => prev.map(msg => (msg.id === message.id ? savedMessage : msg)));
        } catch (error) {
            // 发送失败，标记错误
            setMessages(prev =>
                prev.map(msg =>
                    msg.id === message.id ? { ...msg, sending: false, error: true } : msg
                )
            );
        }
    };

    return (
        <div className="chat">
            <MessageList messages={optimisticMessages} />
            <MessageInput onSend={sendMessage} />
        </div>
    );
}

// 消息列表组件
function MessageList({ messages }) {
    return (
        <div className="message-list">
            {messages.map(message => (
                <div
                    key={message.id}
                    className={`message ${message.user} ${message.sending ? "sending" : ""} ${
                        message.error ? "error" : ""
                    }`}
                >
                    <p>{message.text}</p>
                    <small>
                        {message.timestamp.toLocaleTimeString()}
                        {message.sending && " (发送中...)"}
                        {message.error && " (发送失败)"}
                    </small>
                </div>
            ))}
        </div>
    );
}
```

## 性能优化改进

### 编译时优化

```jsx
// React Compiler 自动优化
function OptimizedComponent({ data }) {
  // 编译器会自动记忆化这些计算
  const filteredData = data.filter(item => item.active);
  const sortedData = [...filteredData].sort((a, b) => b.priority - a.priority);
  const total = sortedData.reduce((sum, item) => sum + item.value, 0);

  // 编译器会自动包装事件处理函数
  const handleClick = (id) => {
    console.log('Clicked:', id);
  };

  return (
    <div>
      <h2>总数: {total}</h2>
      <ul>
        {sortedData.map(item => (
          <li key={item.id} onClick={() => handleClick(item.id)}>
            {item.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

// 编译器配置优化
// .react-compiler.json
{
  "compilationMode": "annotation",
  "sources": [
    "./src/**/*.{js,jsx,ts,tsx}",
    "!./src/**/*.test.{js,jsx,ts,tsx}",
    "!./src/**/*.spec.{js,jsx,ts,tsx}"
  ],
  "panicThreshold": "SOFT",
  "logLevel": "info",
  "optimizations": {
    "memoizeExpensiveValues": true,
    "hoistConstants": true,
    "inlineComponents": true
  }
}
```

### 运行时优化

```jsx
// 使用新的性能API
function PerformanceOptimizedComponent() {
    const [state, setState] = useState({});
    const [isPending, startTransition] = useTransition();

    const handleUpdate = newData => {
        // 使用 startTransition 标记非紧急更新
        startTransition(() => {
            setState(newData);
        });
    };

    // 使用 useDeferredValue 延迟更新
    const deferredState = useDeferredValue(state);

    // 使用 useMemoCache（实验性）进行缓存
    const cachedValue = useMemoCache(() => {
        return expensiveComputation(deferredState);
    }, [deferredState]);

    return (
        <div>
            <button onClick={() => handleUpdate({ count: Math.random() })}>更新状态</button>
            {isPending && <div>更新中...</div>}
            <ExpensiveComponent data={cachedValue} />
        </div>
    );
}

// 资源优先级控制
function ResourcePriority() {
    return (
        <>
            {/* 高优先级资源 */}
            <script src="/critical.js" priority="high" />
            <link rel="stylesheet" href="/critical.css" priority="high" />

            {/* 低优先级资源 */}
            <script src="/analytics.js" priority="low" />
            <link rel="stylesheet" href="/non-critical.css" priority="low" />

            {/* 惰性加载组件 */}
            <Suspense fallback={<Loading />}>
                <LazyComponent
                    loader={() => import("./HeavyComponent")}
                    priority="idle" // 空闲时加载
                />
            </Suspense>
        </>
    );
}

// 视图过渡 API 集成
function ViewTransitions() {
    const navigate = useNavigate();
    const [isTransitioning, startViewTransition] = useViewTransition();

    const handleNavigation = async path => {
        // 使用视图过渡
        await startViewTransition(() => {
            navigate(path);
        });
    };

    return (
        <div className={isTransitioning ? "transitioning" : ""}>
            <nav>
                <button onClick={() => handleNavigation("/")}>首页</button>
                <button onClick={() => handleNavigation("/about")}>关于</button>
            </nav>
        </div>
    );
}
```

## 迁移指南和兼容性

### 从 React 18 迁移

```jsx
// package.json 更新
{
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    // 更新相关库
    "react-router-dom": "^7.0.0", // 支持 React 19
    "@reduxjs/toolkit": "^2.0.0"  // 确保兼容
  }
}

// 1. 更新 React 版本
// npm install react@latest react-dom@latest

// 2. 检查弃用的 API
// - findDOMNode: 已弃用
// - unmountComponentAtNode: 已弃用
// - renderToString: 有新的替代方案

// 3. 更新 createRoot
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(<App />);

// 4. 处理 breaking changes
// - Strict Mode 行为变化
// - 事件系统改进
// - 生命周期调整
```

### 兼容性处理

```jsx
// 向后兼容组件
import { useState, useEffect, useLayoutEffect } from "react";

function CompatibleComponent() {
    const [isReady, setIsReady] = useState(false);

    // 检测 React 版本
    useEffect(() => {
        const version = React.version;
        console.log("React version:", version);

        if (version.startsWith("19")) {
            // 使用新特性
            setIsReady(true);
        } else {
            // 降级方案
            console.warn("Using fallback for older React version");
        }
    }, []);

    // 条件使用新 API
    const useEnhancedHook = () => {
        if (typeof use === "function") {
            // React 19+
            try {
                return use(resource);
            } catch (error) {
                // 处理错误
            }
        } else {
            // React 18 及以下
            const [data, setData] = useState(null);
            useEffect(() => {
                resource.then(setData);
            }, []);
            return data;
        }
    };

    if (!isReady) {
        return <div>加载中...</div>;
    }

    return (
        <div>
            {/* 使用新特性的代码 */}
            <NewFeatureComponent />
        </div>
    );
}

// 错误边界处理
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error("React 19 Error:", error);
        console.error("Error Info:", errorInfo);

        // 发送错误报告
        if (typeof reportError === "function") {
            reportError(error);
        }
    }

    render() {
        if (this.state.hasError) {
            return this.props.fallback || <div>出错了</div>;
        }
        return this.props.children;
    }
}

// 使用示例
function App() {
    return (
        <ErrorBoundary fallback={<ErrorScreen />}>
            <Suspense fallback={<Loading />}>
                <CompatibleComponent />
            </Suspense>
        </ErrorBoundary>
    );
}
```

## 总结

-   更好的性能 - React Compiler 自动优化
-   更简单的数据获取 - Actions API 和 use() Hook
-   更好的元数据管理 - 内置文档元数据组件
-   改进的资源加载 - 自动预加载和优化
-   更好的互操作性 - Web Components 集成
