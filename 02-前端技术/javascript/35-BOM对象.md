# BOM 对象（浏览器对象模型）

## window 对象

### 1. window 对象的属性

```js
// window 是全局对象，在浏览器中是顶级对象

// 1. 窗口尺寸和滚动
console.log("窗口宽度:", window.innerWidth);
console.log("窗口高度:", window.innerHeight);
console.log("屏幕宽度:", window.screen.width);
console.log("屏幕高度:", window.screen.height);
console.log("设备像素比:", window.devicePixelRatio);

// 2. 窗口位置
console.log("屏幕左侧:", window.screenX || window.screenLeft);
console.log("屏幕顶部:", window.screenY || window.screenTop);

// 3. 滚动位置
console.log("水平滚动:", window.pageXOffset || window.scrollX);
console.log("垂直滚动:", window.pageYOffset || window.scrollY);

// 4. 其他属性
console.log("窗口名称:", window.name);
console.log("窗口是否关闭:", window.closed);
console.log("是否全屏:", window.fullScreen);
console.log("窗口打开者:", window.opener);
console.log("父窗口:", window.parent);
console.log("顶层窗口:", window.top);
console.log("框架数量:", window.length);
```

### 2. window 对象的方法

```js
// 1. 对话框
window.alert("警告消息");
const confirmed = window.confirm("确定要删除吗？");
const input = window.prompt("请输入姓名:", "张三");

// 2. 窗口操作
// 打开新窗口
const newWindow = window.open("https://www.example.com", "_blank", "width=400,height=300");

// 关闭窗口
if (newWindow && !newWindow.closed) {
    newWindow.close();
}

// 3. 定时器
const timeoutId = window.setTimeout(() => {
    console.log("3秒后执行");
}, 3000);

const intervalId = window.setInterval(() => {
    console.log("每秒执行一次");
}, 1000);

// 取消定时器
clearTimeout(timeoutId);
clearInterval(intervalId);

// 立即执行（微任务）
const immediateId = window.setImmediate
    ? window.setImmediate(() => {
          console.log("立即执行");
      })
    : setTimeout(() => {
          console.log("setImmediate polyfill");
      }, 0);

// 4. 滚动控制
window.scrollTo(0, 100); // 滚动到指定位置
window.scrollBy(0, 50); // 相对滚动
window.scroll({ top: 0, behavior: "smooth" }); // 平滑滚动

// 5. 其他方法
window.focus(); // 窗口获取焦点
window.blur(); // 窗口失去焦点
window.print(); // 打印页面
window.stop(); // 停止加载
window.find("text"); // 在页面中查找文本
```

### 3. 窗口事件

```js
// 监听窗口事件
window.addEventListener("load", () => {
    console.log("页面完全加载完成");
});

window.addEventListener("DOMContentLoaded", () => {
    console.log("DOM加载完成，无需等待样式表和图像");
});

window.addEventListener("resize", () => {
    console.log("窗口大小改变:", window.innerWidth, window.innerHeight);
});

window.addEventListener("scroll", () => {
    console.log("页面滚动:", window.pageYOffset);
});

window.addEventListener("beforeunload", event => {
    // 页面关闭前提示
    event.preventDefault();
    event.returnValue = ""; // 必须设置，Chrome 需要
    return "确定要离开吗？未保存的更改可能会丢失。";
});

window.addEventListener("unload", () => {
    // 页面卸载时清理
    console.log("页面即将卸载");
});

window.addEventListener("online", () => {
    console.log("网络已连接");
});

window.addEventListener("offline", () => {
    console.log("网络已断开");
});

window.addEventListener("hashchange", () => {
    console.log("hash改变:", window.location.hash);
});

// 存储事件（跨标签页通信）
window.addEventListener("storage", event => {
    console.log("存储变更:", event.key, event.newValue, event.oldValue);
});
```

## location 对象

### 1. location 属性

```js
// 获取当前 URL 信息
console.log("完整URL:", location.href);
console.log("协议:", location.protocol); // http: 或 https:
console.log("主机名:", location.hostname); // www.example.com
console.log("主机:", location.host); // www.example.com:8080
console.log("端口:", location.port);
console.log("路径:", location.pathname); // /path/to/page
console.log("查询参数:", location.search); // ?key=value
console.log("hash:", location.hash); // #section
console.log("来源:", location.origin); // http://www.example.com:8080

// 解析查询参数
function getQueryParams() {
    const params = {};
    const search = location.search.substring(1);

    if (search) {
        const pairs = search.split("&");
        pairs.forEach(pair => {
            const [key, value] = pair.split("=");
            if (key) {
                params[decodeURIComponent(key)] = decodeURIComponent(value || "");
            }
        });
    }

    return params;
}

// 示例 URL: https://www.example.com:8080/path/to/page?name=John&age=30#section1
```

### 2. location 方法

```js
// 1. 页面导航
location.assign("https://www.example.com/new-page"); // 记录到历史记录
location.replace("https://www.example.com/new-page"); // 不记录历史记录
location.reload(); // 重新加载
location.reload(true); // 强制从服务器重新加载

// 2. URL 操作
// 修改部分URL
location.hash = "#new-section"; // 修改hash
location.search = "?new=query"; // 修改查询参数
location.pathname = "/new-path"; // 修改路径

// 3. 解析URL
const url = new URL("https://www.example.com:8080/path?query=1#hash");
console.log("URL对象:", url);

// 安全的URL跳转
function safeRedirect(url) {
    // 验证URL
    try {
        const parsed = new URL(url, window.location.origin);

        // 只允许同源或可信域名
        const allowedDomains = ["example.com", "trusted-site.com"];
        const hostname = parsed.hostname;

        if (allowedDomains.some(domain => hostname.endsWith(domain))) {
            location.href = parsed.toString();
        } else {
            console.error("不允许跳转到该域名:", hostname);
        }
    } catch (error) {
        console.error("无效的URL:", error);
    }
}
```

### 3. URLSearchParams API

```js
// 现代API处理查询参数
const params = new URLSearchParams(location.search);

// 基本操作
params.set("page", "1");
params.set("sort", "desc");
params.delete("oldParam");
console.log("是否有page参数:", params.has("page"));
console.log("获取page值:", params.get("page"));
console.log("所有参数:", params.toString());

// 遍历
for (const [key, value] of params) {
    console.log(key, ":", value);
}

params.forEach((value, key) => {
    console.log(key, "->", value);
});

// 获取所有值
console.log("所有page值:", params.getAll("page"));

// 构建URL
const url = new URL("https://api.example.com/data");
url.search = params.toString();
console.log("构建的URL:", url.toString());

// 实用函数
function updateQueryParam(key, value) {
    const params = new URLSearchParams(location.search);

    if (value === null || value === undefined) {
        params.delete(key);
    } else {
        params.set(key, value);
    }

    // 更新URL（不刷新页面）
    const newUrl = `${location.pathname}?${params.toString()}${location.hash}`;
    history.pushState(null, "", newUrl);
}

function getQueryParam(key) {
    const params = new URLSearchParams(location.search);
    return params.get(key);
}
```

## navigator 对象

### 1. 浏览器和系统信息

```js
// 浏览器信息
console.log("用户代理:", navigator.userAgent);
console.log("应用名称:", navigator.appName);
console.log("应用版本:", navigator.appVersion);
console.log("平台:", navigator.platform);
console.log("语言:", navigator.language);
console.log("用户语言:", navigator.languages); // 用户偏好的语言数组

// 浏览器能力检测
console.log("Cookie启用:", navigator.cookieEnabled);
console.log("Java启用:", navigator.javaEnabled());
console.log("PDF查看器:", navigator.pdfViewerEnabled);
console.log("是否在线:", navigator.onLine);

// 硬件信息
console.log("CPU核心数:", navigator.hardwareConcurrency);
console.log("设备内存:", navigator.deviceMemory, "GB"); // Chrome
console.log("最大触摸点数:", navigator.maxTouchPoints);

// 地理位置
if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
        position => {
            console.log("纬度:", position.coords.latitude);
            console.log("经度:", position.coords.longitude);
            console.log("精度:", position.coords.accuracy);
        },
        error => {
            console.error("获取位置失败:", error.message);
        },
        {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0,
        }
    );
}

// 持续监听位置变化
const watchId = navigator.geolocation.watchPosition(
    position => console.log("位置更新:", position.coords),
    error => console.error("位置监听错误:", error)
);

// 停止监听
// navigator.geolocation.clearWatch(watchId);
```

### 2. 媒体设备

```js
// 获取媒体设备
async function getMediaDevices() {
    try {
        // 请求权限
        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
            video: true,
        });

        // 获取设备列表
        const devices = await navigator.mediaDevices.enumerateDevices();

        devices.forEach(device => {
            console.log(`${device.kind}: ${device.label} (${device.deviceId})`);
        });

        // 按类别筛选
        const cameras = devices.filter(d => d.kind === "videoinput");
        const microphones = devices.filter(d => d.kind === "audioinput");

        console.log("摄像头数量:", cameras.length);
        console.log("麦克风数量:", microphones.length);

        // 停止媒体流
        stream.getTracks().forEach(track => track.stop());
    } catch (error) {
        console.error("访问媒体设备失败:", error);
    }
}

// 设备变化监听
navigator.mediaDevices.addEventListener("devicechange", async () => {
    console.log("设备列表已更改");
    const devices = await navigator.mediaDevices.enumerateDevices();
    console.log("新设备列表:", devices);
});
```

### 3. 其他 navigator API

```js
// 剪贴板 API
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        console.log("复制成功");
    } catch (error) {
        console.error("复制失败:", error);
        // 降级方案
        const textarea = document.createElement("textarea");
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
    }
}

async function pasteFromClipboard() {
    try {
        const text = await navigator.clipboard.readText();
        console.log("粘贴的内容:", text);
        return text;
    } catch (error) {
        console.error("读取剪贴板失败:", error);
        return null;
    }
}

// 网络信息 API
if ("connection" in navigator) {
    const connection = navigator.connection;

    console.log("网络类型:", connection.effectiveType); // 4g, 3g, 2g
    console.log("下行速度:", connection.downlink, "Mbps");
    console.log("往返时间:", connection.rtt, "ms");
    console.log("是否开启数据保护模式:", connection.saveData);

    connection.addEventListener("change", () => {
        console.log("网络连接改变:", connection.effectiveType);
    });
}

// 震动 API
function vibrate() {
    if ("vibrate" in navigator) {
        // 震动200ms
        navigator.vibrate(200);

        // 模式震动：震动200ms，暂停100ms，再震动300ms
        // navigator.vibrate([200, 100, 300]);

        // 停止震动
        // navigator.vibrate(0);
    }
}

// 电池状态 API
async function getBatteryInfo() {
    if ("getBattery" in navigator) {
        try {
            const battery = await navigator.getBattery();

            console.log("电量:", battery.level * 100 + "%");
            console.log("正在充电:", battery.charging);
            console.log("充满时间:", battery.chargingTime);
            console.log("剩余时间:", battery.dischargingTime);

            battery.addEventListener("chargingchange", () => {
                console.log("充电状态改变:", battery.charging);
            });

            battery.addEventListener("levelchange", () => {
                console.log("电量改变:", battery.level * 100 + "%");
            });
        } catch (error) {
            console.error("获取电池信息失败:", error);
        }
    }
}
```

## history 对象

### 1. history 基本操作

```js
// 历史记录信息
console.log("历史记录长度:", history.length);
console.log("当前状态:", history.state);

// 导航方法
history.back(); // 后退一步
history.forward(); // 前进一步
history.go(-2); // 后退两步
history.go(1); // 前进一步
history.go(0); // 刷新当前页

// 添加历史记录
history.pushState({ page: 1 }, "Page 1", "/page1");
history.pushState({ page: 2 }, "Page 2", "/page2");
history.replaceState({ page: 3 }, "Page 3", "/page3"); // 替换当前记录

// 监听历史记录变化
window.addEventListener("popstate", event => {
    console.log("位置变化:", event.state);
    console.log("当前URL:", location.href);

    // 根据 state 更新页面
    if (event.state) {
        loadPage(event.state.page);
    }
});

// 实用函数：安全的 pushState
function safePushState(state, title, url) {
    try {
        // 验证 state 大小（防止性能问题）
        const stateStr = JSON.stringify(state);
        if (stateStr.length > 16000) {
            // 16KB限制
            console.warn("State 太大，可能会影响性能");
        }

        // 验证 URL
        const base = location.origin;
        const fullUrl = new URL(url, base).toString();

        history.pushState(state, title, fullUrl);
        return true;
    } catch (error) {
        console.error("pushState 失败:", error);
        return false;
    }
}
```

### 2. SPA 路由实现

```js
class Router {
    constructor(routes) {
        this.routes = routes;
        this.currentPath = location.pathname;
        this.init();
    }

    init() {
        // 监听浏览器前进后退
        window.addEventListener("popstate", this.handlePopState.bind(this));

        // 监听链接点击
        document.addEventListener("click", this.handleLinkClick.bind(this));

        // 初始加载
        this.navigate(location.pathname, false);
    }

    handlePopState(event) {
        const path = location.pathname;
        this.navigate(path, false);
    }

    handleLinkClick(event) {
        const link = event.target.closest("a[data-router]");
        if (link) {
            event.preventDefault();
            const href = link.getAttribute("href");
            this.navigate(href);
        }
    }

    navigate(path, pushState = true) {
        // 查找匹配的路由
        const route = this.findRoute(path);

        if (route) {
            // 更新页面内容
            this.render(route);

            // 更新URL
            if (pushState && path !== this.currentPath) {
                history.pushState({ path }, "", path);
            }

            this.currentPath = path;
        } else {
            this.navigate("/404");
        }
    }

    findRoute(path) {
        return this.routes.find(route => {
            if (typeof route.path === "string") {
                return route.path === path;
            } else if (route.path instanceof RegExp) {
                return route.path.test(path);
            }
            return false;
        });
    }

    render(route) {
        // 这里应该是实际的渲染逻辑
        console.log("渲染路由:", route.path);
        document.title = route.title || "My App";

        // 触发路由变化事件
        window.dispatchEvent(
            new CustomEvent("routechange", {
                detail: { route },
            })
        );
    }
}

// 使用示例
const router = new Router([
    { path: "/", title: "首页" },
    { path: "/about", title: "关于我们" },
    { path: "/contact", title: "联系我们" },
    { path: "/user/:id", title: "用户详情" },
    { path: /^\/post\/\d+$/, title: "文章详情" },
    { path: "/404", title: "页面不存在" },
]);
```

## screen 对象

### 1. 屏幕信息

```js
// 屏幕尺寸和分辨率
console.log("屏幕宽度:", screen.width);
console.log("屏幕高度:", screen.height);
console.log("可用宽度:", screen.availWidth); // 减去任务栏等
console.log("可用高度:", screen.availHeight);
console.log("色彩深度:", screen.colorDepth, "位");
console.log("像素深度:", screen.pixelDepth, "位");

// 方向检测
if ("orientation" in screen) {
    console.log("屏幕方向:", screen.orientation.type);
    console.log("旋转角度:", screen.orientation.angle);

    // 监听方向变化
    screen.orientation.addEventListener("change", () => {
        console.log("方向改变:", screen.orientation.type);
    });
}

// 多显示器支持
if ("getScreenDetails" in window) {
    async function getScreensInfo() {
        try {
            const screenDetails = await window.getScreenDetails();

            console.log("屏幕数量:", screenDetails.screens.length);

            screenDetails.screens.forEach((screen, index) => {
                console.log(`屏幕 ${index}:`, {
                    width: screen.width,
                    height: screen.height,
                    left: screen.left,
                    top: screen.top,
                    isPrimary: screen.isPrimary,
                    label: screen.label,
                });
            });

            // 监听屏幕变化
            screenDetails.addEventListener("screenschange", () => {
                console.log("屏幕配置已更改");
            });
        } catch (error) {
            console.error("获取屏幕信息失败:", error);
        }
    }

    getScreensInfo();
}
```

### 2. 响应式设计辅助

```js
// 根据屏幕特性调整布局
function adaptToScreen() {
    const breakpoints = {
        mobile: 768,
        tablet: 1024,
        desktop: 1200,
    };

    // 检测设备类型
    const isMobile = screen.width <= breakpoints.mobile;
    const isTablet = screen.width > breakpoints.mobile && screen.width <= breakpoints.tablet;
    const isDesktop = screen.width > breakpoints.tablet;

    // 检测横竖屏
    const isPortrait = window.matchMedia("(orientation: portrait)").matches;
    const isLandscape = window.matchMedia("(orientation: landscape)").matches;

    // 检测像素密度
    const isHighDensity = window.devicePixelRatio >= 2;
    const isRetina = window.devicePixelRatio >= 3;

    // 根据检测结果调整
    document.documentElement.className = [
        isMobile ? "mobile" : "",
        isTablet ? "tablet" : "",
        isDesktop ? "desktop" : "",
        isPortrait ? "portrait" : "",
        isLandscape ? "landscape" : "",
        isHighDensity ? "high-dpi" : "",
        isRetina ? "retina" : "",
    ]
        .filter(Boolean)
        .join(" ");

    // 设置视口缩放
    if (isMobile) {
        const viewport = document.querySelector('meta[name="viewport"]');
        if (viewport) {
            viewport.content =
                "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no";
        }
    }
}

// 监听屏幕变化
window.addEventListener("resize", adaptToScreen);
screen.orientation?.addEventListener("change", adaptToScreen);

// 初始调用
adaptToScreen();
```

## document 对象

### 1. 文档信息

```js
// 文档基本信息
console.log("文档标题:", document.title);
console.log("字符集:", document.characterSet);
console.log("文档类型:", document.doctype);
console.log("文档URI:", document.documentURI);
console.log("文档域:", document.domain);
console.t.log("上次修改:", document.lastModified);
console.log("根元素:", document.documentElement);
console.log("头部:", document.head);
console.log("主体:", document.body);

// 文档状态
console.log("就绪状态:", document.readyState);
console.log("是否隐藏:", document.hidden);
console.log("可见性:", document.visibilityState);

// 文档位置
console.log("滚动位置X:", document.documentElement.scrollLeft || document.body.scrollLeft);
console.log("滚动位置Y:", document.documentElement.scrollTop || document.body.scrollTop);
console.log("滚动宽度:", document.documentElement.scrollWidth);
console.log("滚动高度:", document.documentElement.scrollHeight);
console.log("可视宽度:", document.documentElement.clientWidth);
console.log("可视高度:", document.documentElement.clientHeight);

// 文档事件
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM 加载完成");
});

document.addEventListener("readystatechange", () => {
    console.log("就绪状态改变:", document.readyState);
});

document.addEventListener("visibilitychange", () => {
    console.log("可见性改变:", document.visibilityState);

    if (document.visibilityState === "visible") {
        // 页面可见时恢复操作
        resumeActivity();
    } else if (document.visibilityState === "hidden") {
        // 页面隐藏时暂停操作
        pauseActivity();
    }
});
```

### 2. 文档操作

```js
// 创建元素
const div = document.createElement("div");
const text = document.createTextNode("Hello World");
const comment = document.createComment("这是一个注释");
const fragment = document.createDocumentFragment();

// 插入元素
document.body.appendChild(div);
document.body.insertBefore(div, document.body.firstChild);
document.body.replaceChild(newDiv, oldDiv);

// 查询元素
const byId = document.getElementById("myId");
const byClass = document.getElementsByClassName("myClass");
const byTag = document.getElementsByTagName("div");
const byName = document.getElementsByName("username");
const querySingle = document.querySelector(".container .item");
const queryAll = document.querySelectorAll(".item");

// 样式操作
document.body.style.backgroundColor = "#f0f0f0";
document.documentElement.style.setProperty("--primary-color", "#007bff");

// 类名操作
document.body.classList.add("dark-mode");
document.body.classList.remove("light-mode");
document.body.classList.toggle("active");
console.log("是否包含class:", document.body.classList.contains("dark-mode"));

// 属性操作
document.body.setAttribute("data-theme", "dark");
const theme = document.body.getAttribute("data-theme");
document.body.hasAttribute("data-theme");
document.body.removeAttribute("data-theme");

// 写入内容
document.write("<h1>Hello World</h1>");
document.writeln("<p>Line with newline</p>");
```

## BOM 综合应用

### 1. 页面性能监控

```js
class PerformanceMonitor {
    constructor() {
        this.metrics = {};
        this.init();
    }

    init() {
        if ("performance" in window) {
            this.collectNavigationTiming();
            this.collectResourceTiming();
            this.setupPerformanceObserver();
        }
    }

    collectNavigationTiming() {
        const timing = performance.timing;

        this.metrics = {
            // DNS 查询
            dnsLookup: timing.domainLookupEnd - timing.domainLookupStart,

            // TCP 连接
            tcpConnect: timing.connectEnd - timing.connectStart,

            // 请求响应
            requestResponse: timing.responseEnd - timing.requestStart,

            // DOM 处理
            domProcessing: timing.domComplete - timing.domLoading,

            // 页面加载
            pageLoad: timing.loadEventEnd - timing.navigationStart,

            // 白屏时间
            firstPaint: timing.responseEnd - timing.navigationStart,

            // 可交互时间
            timeToInteractive: timing.domInteractive - timing.navigationStart,
        };

        console.log("页面性能指标:", this.metrics);
    }

    collectResourceTiming() {
        const resources = performance.getEntriesByType("resource");

        resources.forEach(resource => {
            console.log(`${resource.name}:`, {
                duration: resource.duration,
                type: resource.initiatorType,
                size: resource.transferSize,
            });
        });
    }

    setupPerformanceObserver() {
        // 监听长任务（阻塞UI超过50ms的任务）
        const longTaskObserver = new PerformanceObserver(list => {
            list.getEntries().forEach(entry => {
                console.log("长任务检测:", {
                    duration: entry.duration,
                    startTime: entry.startTime,
                });
            });
        });

        longTaskObserver.observe({ entryTypes: ["longtask"] });

        // 监听布局偏移（CLS）
        const layoutShiftObserver = new PerformanceObserver(list => {
            list.getEntries().forEach(entry => {
                if (!entry.hadRecentInput) {
                    console.log("布局偏移:", {
                        value: entry.value,
                        sources: entry.sources,
                    });
                }
            });
        });

        layoutShiftObserver.observe({ entryTypes: ["layout-shift"] });

        // 监听最大内容绘制（LCP）
        const largestContentfulPaintObserver = new PerformanceObserver(list => {
            const entries = list.getEntries();
            const lastEntry = entries[entries.length - 1];
            console.log("最大内容绘制时间:", lastEntry.startTime);
        });

        largestContentfulPaintObserver.observe({
            entryTypes: ["largest-contentful-paint"],
        });
    }

    getMetrics() {
        return this.metrics;
    }
}

// 使用
const monitor = new PerformanceMonitor();
```

### 2. 浏览器存储管理

```js
class StorageManager {
    constructor() {
        this.storageTypes = ["localStorage", "sessionStorage", "indexedDB", "cookies"];
        this.init();
    }

    init() {
        // 检测存储可用性
        this.checkStorageAvailability();

        // 监听存储变化
        window.addEventListener("storage", this.handleStorageChange.bind(this));
    }

    checkStorageAvailability() {
        const tests = {
            localStorage: () => {
                try {
                    localStorage.setItem("test", "test");
                    localStorage.removeItem("test");
                    return true;
                } catch (e) {
                    return false;
                }
            },
            sessionStorage: () => {
                try {
                    sessionStorage.setItem("test", "test");
                    sessionStorage.removeItem("test");
                    return true;
                } catch (e) {
                    return false;
                }
            },
            cookies: () => navigator.cookieEnabled,
            indexedDB: () => "indexedDB" in window,
        };

        const results = {};
        for (const [type, test] of Object.entries(tests)) {
            results[type] = test();
        }

        console.log("存储支持情况:", results);
        return results;
    }

    // LocalStorage 增强
    setLocalStorage(key, value, options = {}) {
        const item = {
            value,
            timestamp: Date.now(),
            ttl: options.ttl, // 生存时间（毫秒）
            version: options.version || "1.0",
        };

        localStorage.setItem(key, JSON.stringify(item));

        if (options.expires) {
            this.setExpiration(key, options.expires);
        }
    }

    getLocalStorage(key) {
        const itemStr = localStorage.getItem(key);
        if (!itemStr) return null;

        try {
            const item = JSON.parse(itemStr);

            // 检查是否过期
            if (item.ttl && Date.now() > item.timestamp + item.ttl) {
                localStorage.removeItem(key);
                return null;
            }

            return item.value;
        } catch (e) {
            console.error("解析存储数据失败:", e);
            return null;
        }
    }

    setExpiration(key, expires) {
        const expirationKey = `${key}_expires`;
        const expirationTime = Date.now() + expires;
        localStorage.setItem(expirationKey, expirationTime.toString());
    }

    // 清理过期数据
    cleanup() {
        const now = Date.now();
        const toRemove = [];

        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.endsWith("_expires")) {
                const expirationTime = parseInt(localStorage.getItem(key));
                if (now > expirationTime) {
                    const dataKey = key.replace("_expires", "");
                    toRemove.push(dataKey, key);
                }
            }
        }

        toRemove.forEach(key => localStorage.removeItem(key));
        console.log(`清理了 ${toRemove.length / 2} 个过期项目`);
    }

    handleStorageChange(event) {
        console.log("存储变更事件:", {
            key: event.key,
            oldValue: event.oldValue,
            newValue: event.newValue,
            url: event.url,
            storageArea: event.storageArea,
        });

        // 跨标签页通信
        if (event.key === "broadcast") {
            try {
                const message = JSON.parse(event.newValue);
                this.handleBroadcastMessage(message);
            } catch (e) {
                console.error("解析广播消息失败:", e);
            }
        }
    }

    broadcast(message) {
        const broadcastData = {
            ...message,
            timestamp: Date.now(),
            sender: window.name || "unknown",
        };

        localStorage.setItem("broadcast", JSON.stringify(broadcastData));
        localStorage.removeItem("broadcast"); // 立即删除，触发事件
    }

    handleBroadcastMessage(message) {
        console.log("收到广播消息:", message);

        // 处理不同类型的消息
        switch (message.type) {
            case "auth":
                // 认证状态变化
                break;
            case "data":
                // 数据更新
                break;
            case "sync":
                // 同步请求
                break;
        }
    }
}

// 使用
const storageManager = new StorageManager();
```

### 3. 跨窗口通信

```js
class CrossWindowCommunication {
    constructor() {
        this.channels = new Map();
        this.init();
    }

    init() {
        // 监听消息
        window.addEventListener("message", this.handleMessage.bind(this));

        // 监听存储事件（同源）
        window.addEventListener("storage", this.handleStorage.bind(this));

        // 监听页面可见性
        document.addEventListener("visibilitychange", () => {
            if (document.visibilityState === "visible") {
                this.syncState();
            }
        });
    }

    // 使用 postMessage
    openChannel(targetWindow, targetOrigin = "*", channelName = "default") {
        const channel = {
            target: targetWindow,
            origin: targetOrigin,
            listeners: new Set(),
        };

        this.channels.set(channelName, channel);
        return channel;
    }

    sendMessage(channelName, message, transfer = []) {
        const channel = this.channels.get(channelName);
        if (!channel) {
            throw new Error(`Channel ${channelName} not found`);
        }

        const fullMessage = {
            type: "cross-window-message",
            channel: channelName,
            data: message,
            timestamp: Date.now(),
            source: window.location.origin,
        };

        channel.target.postMessage(fullMessage, channel.origin, transfer);
    }

    onMessage(channelName, callback) {
        const channel = this.channels.get(channelName);
        if (channel) {
            channel.listeners.add(callback);
        }
    }

    handleMessage(event) {
        // 验证来源
        if (event.data.type !== "cross-window-message") return;

        // 安全性检查
        if (event.origin !== window.location.origin) {
            console.warn("拒绝来自不同源的消息:", event.origin);
            return;
        }

        const { channel, data } = event.data;
        const channelObj = this.channels.get(channel);

        if (channelObj) {
            channelObj.listeners.forEach(listener => {
                try {
                    listener(data, event);
                } catch (error) {
                    console.error("消息处理错误:", error);
                }
            });
        }
    }

    // 使用 BroadcastChannel API（现代浏览器）
    setupBroadcastChannel(channelName = "app-channel") {
        if ("BroadcastChannel" in window) {
            const bc = new BroadcastChannel(channelName);

            bc.onmessage = event => {
                console.log("BroadcastChannel 消息:", event.data);
                this.handleBroadcastMessage(event.data);
            };

            return bc;
        } else {
            // 降级方案：使用 localStorage
            console.log("BroadcastChannel 不支持，使用降级方案");
            return null;
        }
    }

    // 使用 SharedWorker（复杂跨窗口通信）
    setupSharedWorker() {
        if ("SharedWorker" in window) {
            const worker = new SharedWorker("shared-worker.js");

            worker.port.onmessage = event => {
                console.log("SharedWorker 消息:", event.data);
                this.handleWorkerMessage(event.data);
            };

            // 连接到 worker
            worker.port.start();

            return worker;
        }
        return null;
    }

    // 页面间同步状态
    syncState() {
        // 从主窗口获取最新状态
        if (window.opener && !window.opener.closed) {
            this.sendMessage("main", { type: "sync-request" });
        }

        // 从其他标签页获取状态
        localStorage.setItem("sync-request", Date.now().toString());
    }

    handleStorage(event) {
        if (event.key === "sync-request" && event.newValue) {
            // 响应同步请求
            const state = this.getCurrentState();
            localStorage.setItem(
                "sync-response",
                JSON.stringify({
                    state,
                    timestamp: Date.now(),
                })
            );
        }

        if (event.key === "sync-response" && event.newValue) {
            // 处理同步响应
            try {
                const response = JSON.parse(event.newValue);
                this.applyState(response.state);
            } catch (e) {
                console.error("解析同步响应失败:", e);
            }
        }
    }

    getCurrentState() {
        // 获取当前应用状态
        return {
            user: this.getUserState(),
            data: this.getDataState(),
            ui: this.getUIState(),
        };
    }

    applyState(state) {
        // 应用从其他窗口获取的状态
        console.log("应用同步状态:", state);
        // 实际应用中这里会更新应用状态
    }

    getUserState() {
        return {
            /* 用户状态 */
        };
    }

    getDataState() {
        return {
            /* 数据状态 */
        };
    }

    getUIState() {
        return {
            /* UI状态 */
        };
    }
}

// 使用示例
const communicator = new CrossWindowCommunication();

// 与父窗口通信
if (window.opener) {
    const channel = communicator.openChannel(window.opener, window.location.origin, "parent-child");
    communicator.onMessage("parent-child", data => {
        console.log("收到父窗口消息:", data);
    });

    // 发送消息到父窗口
    communicator.sendMessage("parent-child", { action: "ready" });
}

// 与 iframe 通信
const iframe = document.getElementById("myIframe");
const iframeChannel = communicator.openChannel(
    iframe.contentWindow,
    "https://allowed-origin.com",
    "iframe-comm"
);
```

## 最佳实践总结

### 1. 安全注意事项

```js
// 1. 验证来源
function validateOrigin(allowedOrigins = []) {
    return function (event) {
        const origin = event.origin || event.originalEvent.origin;
        if (!allowedOrigins.includes(origin)) {
            console.error("拒绝来自未授权源的消息:", origin);
            return false;
        }
        return true;
    };
}

// 2. 防止点击劫持
if (self === top) {
    // 正常页面
    document.documentElement.style.display = "block";
} else {
    // 在iframe中
    if (location.hostname !== "trusted-domain.com") {
        top.location = self.location; // 跳出框架
    }
}

// 添加X-Frame-Options
// 服务器端设置：X-Frame-Options: SAMEORIGIN

// 3. 安全的窗口打开
function safeWindowOpen(url, target, features) {
    // 验证URL
    try {
        const parsedUrl = new URL(url, window.location.origin);

        // 防止使用危险协议
        const dangerousProtocols = ["javascript:", "data:", "vbscript:"];
        if (dangerousProtocols.some(proto => parsedUrl.protocol.startsWith(proto))) {
            throw new Error("危险协议被阻止");
        }

        // 限制特征
        const safeFeatures = "noopener,noreferrer," + (features || "");

        const newWindow = window.open(parsedUrl.toString(), target, safeFeatures);

        if (newWindow) {
            // 限制对新窗口的访问
            newWindow.opener = null;
        }

        return newWindow;
    } catch (error) {
        console.error("安全打开窗口失败:", error);
        return null;
    }
}

// 4. 防止历史记录操纵
function safeHistoryPush(state, title, url) {
    // 限制历史记录数量
    if (history.length > 50) {
        console.warn("历史记录过多，可能会影响性能");
    }

    // 验证状态大小
    if (JSON.stringify(state).length > 16000) {
        throw new Error("状态数据太大");
    }

    history.pushState(state, title, url);
}

// 5. 安全的URL操作
function safeURLUpdate(param, value) {
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);

    if (value === null || value === undefined) {
        params.delete(param);
    } else {
        params.set(param, value);
    }

    url.search = params.toString();

    // 使用 replaceState 避免过多历史记录
    history.replaceState({}, "", url.toString());
}
```

### 2. 性能优化

```js
// 1. 防抖和节流
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function (...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => (inThrottle = false), limit);
        }
    };
}

// 使用
window.addEventListener(
    "resize",
    debounce(() => {
        console.log("调整大小完成");
    }, 250)
);

window.addEventListener(
    "scroll",
    throttle(() => {
        console.log("滚动中...");
    }, 100)
);

// 2. 智能事件监听
class SmartEventListener {
    constructor() {
        this.listeners = new Map();
        this.intersectionObserver = null;
        this.visibilityObserver = null;
    }

    // 智能滚动监听
    addScrollListener(element, callback, options = {}) {
        const { threshold = 0.1, rootMargin = "0px", once = false } = options;

        if (!this.intersectionObserver) {
            this.intersectionObserver = new IntersectionObserver(
                this.handleIntersection.bind(this),
                { threshold, rootMargin }
            );
        }

        const listener = { callback, once };
        this.listeners.set(element, listener);
        this.intersectionObserver.observe(element);
    }

    handleIntersection(entries) {
        entries.forEach(entry => {
            const listener = this.listeners.get(entry.target);
            if (listener && entry.isIntersecting) {
                listener.callback(entry);

                if (listener.once) {
                    this.intersectionObserver.unobserve(entry.target);
                    this.listeners.delete(entry.target);
                }
            }
        });
    }

    // 智能可见性监听
    addVisibilityListener(element, callback, options = {}) {
        if (!this.visibilityObserver) {
            this.visibilityObserver = new IntersectionObserver(this.handleVisibility.bind(this), {
                threshold: Array.from({ length: 101 }, (_, i) => i / 100),
            });
        }

        const listener = { callback, lastVisibility: 0 };
        this.listeners.set(element, listener);
        this.visibilityObserver.observe(element);
    }

    handleVisibility(entries) {
        entries.forEach(entry => {
            const listener = this.listeners.get(entry.target);
            if (listener) {
                const visibility = entry.intersectionRatio;
                if (Math.abs(visibility - listener.lastVisibility) > 0.1) {
                    listener.callback(visibility, entry);
                    listener.lastVisibility = visibility;
                }
            }
        });
    }

    cleanup() {
        if (this.intersectionObserver) {
            this.intersectionObserver.disconnect();
        }
        if (this.visibilityObserver) {
            this.visibilityObserver.disconnect();
        }
        this.listeners.clear();
    }
}

// 3. 内存管理
class MemoryManager {
    constructor() {
        this.references = new WeakMap();
        this.eventListeners = new Map();
        this.timers = new Set();
    }

    // 跟踪对象引用
    track(obj, tag) {
        this.references.set(obj, {
            tag,
            created: Date.now(),
            size: this.estimateSize(obj),
        });
    }

    // 清理事件监听器
    addEventListener(target, type, handler, options) {
        target.addEventListener(type, handler, options);

        const key = `${type}-${handler.toString().slice(0, 50)}`;
        if (!this.eventListeners.has(target)) {
            this.eventListeners.set(target, new Map());
        }
        this.eventListeners.get(target).set(key, { type, handler, options });
    }

    // 清理定时器
    addTimer(timerId) {
        this.timers.add(timerId);
    }

    // 清理所有资源
    cleanup() {
        // 清理事件监听器
        for (const [target, listeners] of this.eventListeners) {
            for (const { type, handler, options } of listeners.values()) {
                target.removeEventListener(type, handler, options);
            }
        }
        this.eventListeners.clear();

        // 清理定时器
        for (const timerId of this.timers) {
            clearTimeout(timerId);
            clearInterval(timerId);
        }
        this.timers.clear();

        // 强制垃圾回收（如果可用）
        if (window.gc) {
            window.gc();
        }
    }

    estimateSize(obj) {
        // 粗略估计对象大小
        const str = JSON.stringify(obj);
        return str ? str.length * 2 : 0; // 假设 UTF-16
    }
}
```

### 3. 兼容性处理

```js
// BOM 特性检测和 polyfill
class BOMCompat {
    constructor() {
        this.features = this.detectFeatures();
        this.applyPolyfills();
    }

    detectFeatures() {
        return {
            // 窗口特性
            requestIdleCallback: "requestIdleCallback" in window,
            requestAnimationFrame: "requestAnimationFrame" in window,
            matchMedia: "matchMedia" in window,

            // 导航特性
            pushState: "pushState" in history,
            replaceState: "replaceState" in history,

            // 存储特性
            localStorage: "localStorage" in window,
            sessionStorage: "sessionStorage" in window,
            indexedDB: "indexedDB" in window,

            // 网络特性
            navigator: {
                geolocation: "geolocation" in navigator,
                connection: "connection" in navigator,
                serviceWorker: "serviceWorker" in navigator,
                clipboard: "clipboard" in navigator,
            },

            // 其他特性
            IntersectionObserver: "IntersectionObserver" in window,
            MutationObserver: "MutationObserver" in window,
            PerformanceObserver: "PerformanceObserver" in window,
        };
    }

    applyPolyfills() {
        // requestIdleCallback polyfill
        if (!this.features.requestIdleCallback) {
            window.requestIdleCallback = function (callback) {
                return setTimeout(() => {
                    const start = Date.now();
                    callback({
                        didTimeout: false,
                        timeRemaining: () => Math.max(0, 50 - (Date.now() - start)),
                    });
                }, 1);
            };

            window.cancelIdleCallback = function (id) {
                clearTimeout(id);
            };
        }

        // 其他 polyfills...
        console.log("应用特性检测结果:", this.features);
    }

    // 安全的特性使用
    safeMatchMedia(query) {
        if (this.features.matchMedia) {
            return window.matchMedia(query);
        } else {
            // 简单降级
            return {
                matches: false,
                addListener: () => {},
                removeListener: () => {},
            };
        }
    }

    safeGeolocation(options) {
        return new Promise((resolve, reject) => {
            if (this.features.navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(resolve, reject, options);
            } else {
                reject(new Error("Geolocation not supported"));
            }
        });
    }

    // 特性使用建议
    getRecommendations() {
        const recommendations = [];

        if (!this.features.pushState) {
            recommendations.push("考虑为旧浏览器添加 HTML5 History API polyfill");
        }

        if (!this.features.localStorage) {
            recommendations.push("需要为不支持 localStorage 的浏览器提供替代存储方案");
        }

        if (!this.features.navigator.connection) {
            recommendations.push("无法检测网络状态，考虑降级处理");
        }

        return recommendations;
    }
}

// 使用
const compat = new BOMCompat();
console.log("浏览器支持情况:", compat.features);
console.log("建议:", compat.getRecommendations());
```

## 总结要点：

-   window 是全局对象，控制浏览器窗口和页面
-   location 操作 URL，注意安全性
-   navigator 提供浏览器和环境信息
-   history 管理浏览历史，支持 SPA
-   screen 提供屏幕信息，用于响应式设计
-   document 代表页面文档，是 DOM 的入口
-   注意安全性：验证来源、防止劫持
-   考虑性能：使用防抖节流、智能事件监听
-   处理兼容性：特性检测和 polyfill
-   现代 BOM API：Clipboard、Geolocation、MediaDevices 等
