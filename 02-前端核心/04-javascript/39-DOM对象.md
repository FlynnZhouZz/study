# DOM 对象（文档对象模型）

## DOM 基础概念

### 1. DOM 树结构

```js
// DOM 将 HTML 文档表示为树形结构
/*
document
├── <html>
│   ├── <head>
│   │   ├── <title>Document</title>
│   │   └── <meta charset="UTF-8">
│   └── <body>
│       ├── <h1 id="title">Hello</h1>
│       ├── <div class="container">
│       │   ├── <p>Paragraph 1</p>
│       │   └── <p>Paragraph 2</p>
│       └── <script src="app.js"></script>
*/

// 节点类型常量
console.log(Node.ELEMENT_NODE); // 1 - 元素节点
console.log(Node.ATTRIBUTE_NODE); // 2 - 属性节点
console.log(Node.TEXT_NODE); // 3 - 文本节点
console.log(Node.COMMENT_NODE); // 8 - 注释节点
console.log(Node.DOCUMENT_NODE); // 9 - 文档节点
console.log(Node.DOCUMENT_TYPE_NODE); // 10 - 文档类型节点
```

### 2. 获取 DOM 节点

```js
// 1. 通过 ID 获取（返回单个元素）
const title = document.getElementById("title");

// 2. 通过类名获取（返回 HTMLCollection）
const containers = document.getElementsByClassName("container");

// 3. 通过标签名获取（返回 HTMLCollection）
const paragraphs = document.getElementsByTagName("p");

// 4. 通过 name 属性获取（返回 NodeList）
const inputs = document.getElementsByName("username");

// 5. 使用 CSS 选择器（返回单个元素）
const firstPara = document.querySelector(".container p:first-child");

// 6. 使用 CSS 选择器（返回 NodeList）
const allParas = document.querySelectorAll(".container p");

// 7. 获取特殊元素
console.log(document.documentElement); // <html> 元素
console.log(document.head); // <head> 元素
console.log(document.body); // <body> 元素
console.log(document.forms); // 所有表单
console.log(document.images); // 所有图片
console.log(document.links); // 所有链接
console.log(document.scripts); // 所有脚本

// 8. 遍历 DOM
const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT, null, false);

let node;
while ((node = walker.nextNode())) {
    console.log(node.tagName);
}
```

## 节点操作

### 1. 创建节点

```js
// 创建元素节点
const div = document.createElement("div");
const span = document.createElement("span");

// 创建文本节点
const text = document.createTextNode("Hello World");

// 创建注释节点
const comment = document.createComment("This is a comment");

// 创建文档片段（性能优化）
const fragment = document.createDocumentFragment();

// 克隆节点
const original = document.getElementById("original");
const clone = original.cloneNode(true); // true 表示深度克隆

// 创建属性节点（不常用）
const attr = document.createAttribute("data-custom");
attr.value = "value";
div.setAttributeNode(attr);
```

### 2. 插入节点

```js
const parent = document.getElementById("parent");
const child = document.createElement("div");
const reference = document.getElementById("reference");

// 1. appendChild - 追加到末尾
parent.appendChild(child);

// 2. insertBefore - 插入到指定位置
parent.insertBefore(child, reference);

// 3. insertAdjacentElement - 灵活插入
reference.insertAdjacentElement("beforebegin", child); // 前面
reference.insertAdjacentElement("afterbegin", child); // 内部开始
reference.insertAdjacentElement("beforeend", child); // 内部结束
reference.insertAdjacentElement("afterend", child); // 后面

// 4. insertAdjacentHTML - 插入 HTML 字符串
parent.insertAdjacentHTML("beforeend", "<div>New</div>");

// 5. insertAdjacentText - 插入文本
parent.insertAdjacentText("beforeend", "Some text");

// 6. replaceChild - 替换节点
const newChild = document.createElement("span");
parent.replaceChild(newChild, child);

// 7. 使用 DocumentFragment 批量插入（性能优化）
for (let i = 0; i < 1000; i++) {
    const item = document.createElement("div");
    item.textContent = `Item ${i}`;
    fragment.appendChild(item);
}
parent.appendChild(fragment);
```

### 3. 删除和替换节点

```js
const parent = document.getElementById("parent");
const child = document.getElementById("child");

// 1. removeChild - 移除子节点
parent.removeChild(child);

// 2. remove - 移除自身（现代API）
child.remove();

// 3. replaceChild - 替换节点
const newChild = document.createElement("div");
parent.replaceChild(newChild, child);

// 4. replaceWith - 替换自身（现代API）
child.replaceWith(newChild);

// 5. 清空所有子节点
while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
}

// 更高效的方式
parent.innerHTML = "";

// 或使用 textContent（保留元素）
parent.textContent = "";
```

### 4. 节点关系

```js
const element = document.getElementById("target");

// 父节点关系
console.log("父节点:", element.parentNode);
console.log("父元素:", element.parentElement);

// 子节点关系
console.log("第一个子节点:", element.firstChild);
console.log("最后一个子节点:", element.lastChild);
console.log("所有子节点:", element.childNodes);
console.log("子元素数量:", element.childElementCount);
console.log("子元素:", element.children);

// 兄弟节点关系
console.log("上一个兄弟节点:", element.previousSibling);
console.log("下一个兄弟节点:", element.nextSibling);
console.log("上一个兄弟元素:", element.previousElementSibling);
console.log("下一个兄弟元素:", element.nextElementSibling);

// 检查节点关系
const child = element.firstChild;
console.log("是否包含节点:", element.contains(child));
console.log("节点比较位置:", element.compareDocumentPosition(child));

// 遍历子节点
const children = element.children;
for (let i = 0; i < children.length; i++) {
    console.log("子元素:", children[i]);
}

// 使用 for...of（需要转换为数组）
for (const child of Array.from(element.children)) {
    console.log("子元素:", child);
}

// 查找最近的祖先元素
const closest = element.closest(".container");
console.log("最近的容器:", closest);
```

## 元素属性和内容

### 1. 属性操作

```js
const element = document.getElementById("myElement");

// 1. 标准属性操作
element.id = "newId";
element.className = "class1 class2";
element.title = "Tooltip text";

// 2. 通用属性方法
element.setAttribute("data-custom", "value");
console.log("获取属性:", element.getAttribute("data-custom"));
console.log("是否有属性:", element.hasAttribute("data-custom"));
element.removeAttribute("data-custom");

// 3. dataset 操作（data-* 属性）
element.dataset.userId = "123";
element.dataset.userRole = "admin";
console.log("所有data属性:", element.dataset);

// 4. classList 操作
element.classList.add("active", "highlight");
element.classList.remove("inactive");
element.classList.toggle("visible");
console.log("是否包含class:", element.classList.contains("active"));
element.classList.replace("old", "new");

// 5. style 操作
element.style.color = "red";
element.style.backgroundColor = "#f0f0f0";
element.style.setProperty("--custom-var", "value");
console.log("计算样式:", window.getComputedStyle(element).color);

// 6. 特殊属性
element.innerHTML = "<span>HTML内容</span>";
element.textContent = "纯文本内容";
element.outerHTML = "<div>替换整个元素</div>";
element.value = "表单值"; // 表单元素
element.checked = true; // 复选框/单选框

// 7. 获取所有属性
const attributes = element.attributes;
for (let i = 0; i < attributes.length; i++) {
    console.log(attributes[i].name, "=", attributes[i].value);
}
```

### 2. 内容操作

```js
const container = document.getElementById("container");

// 1. innerHTML - 获取/设置 HTML
console.log("HTML内容:", container.innerHTML);
container.innerHTML = "<div>New content</div>";

// 注意：innerHTML 会重新解析，有性能和安全问题
// 对于纯文本，使用 textContent 更好

// 2. textContent - 获取/设置文本
console.log("文本内容:", container.textContent);
container.textContent = "纯文本内容";

// 3. innerText - 获取/设置可见文本（考虑样式）
console.log("可见文本:", container.innerText);
container.innerText = "可见文本";

// 4. outerHTML - 包含元素本身的 HTML
console.log("外部HTML:", container.outerHTML);

// 5. 安全的内容插入
function safeHTML(html) {
    const div = document.createElement("div");
    div.textContent = html; // 自动转义
    return div.innerHTML;
}

// 或使用 textContent 避免 XSS
container.textContent = '<script>alert("xss")</script>';

// 6. 使用模板
const template = document.createElement("template");
template.innerHTML = "<div>Safe HTML</div>";
container.appendChild(template.content.cloneNode(true));
```

### 3. 表单元素操作

```js
const form = document.forms[0];
const input = document.getElementById("username");
const select = document.getElementById("country");
const checkbox = document.getElementById("agree");

// 1. 表单值
console.log("输入值:", input.value);
console.log("选中值:", select.value);
console.log("是否选中:", checkbox.checked);

// 2. 表单选项（select）
select.options[0].selected = true;
const selectedOption = select.options[select.selectedIndex];

// 3. 多选 select
const multiSelect = document.getElementById("multi");
const selectedValues = Array.from(multiSelect.selectedOptions).map(option => option.value);

// 4. 文件输入
const fileInput = document.getElementById("file");
console.log("文件:", fileInput.files[0]);

// 5. 表单验证
input.checkValidity(); // 检查约束验证
input.reportValidity(); // 显示验证消息
console.log("验证消息:", input.validationMessage);
console.log("有效性:", input.validity);

// 6. 自定义验证
input.setCustomValidity("自定义错误消息");
input.setCustomValidity(""); // 清除错误

// 7. 表单数据
const formData = new FormData(form);
for (const [key, value] of formData) {
    console.log(key, ":", value);
}

// 8. 表单重置
form.reset(); // 重置为默认值
form.submit(); // 提交表单
```

## 事件系统

### 1. 事件监听

```js
const button = document.getElementById("myButton");

// 1. 传统方式
button.onclick = function (event) {
    console.log("点击了按钮");
    // 只能有一个处理函数
};

// 2. addEventListener（推荐）
button.addEventListener("click", function (event) {
    console.log("点击事件 - 匿名函数");
});

// 命名函数（便于移除）
function handleClick(event) {
    console.log("点击事件", event.target, event.currentTarget);
}

button.addEventListener("click", handleClick);

// 3. 事件选项
button.addEventListener("click", handleClick, {
    capture: false, // 冒泡阶段
    once: true, // 只执行一次
    passive: true, // 不会调用 preventDefault()
    signal: abortSignal, // 可取消监听
});

// 4. 移除事件监听
button.removeEventListener("click", handleClick);

// 5. 使用 AbortSignal
const controller = new AbortController();
button.addEventListener("click", handleClick, {
    signal: controller.signal,
});
controller.abort(); // 移除所有通过此 signal 注册的监听器

// 6. 事件委托
document.addEventListener("click", function (event) {
    if (event.target.matches(".item")) {
        console.log("点击了项目:", event.target);
    }
});
```

### 2. 事件对象

```js
function handleEvent(event) {
    // 事件类型
    console.log("事件类型:", event.type);

    // 目标元素
    console.log("目标元素:", event.target);
    console.log("当前目标:", event.currentTarget);

    // 事件阶段
    console.log("事件阶段:", event.eventPhase); // 1:捕获 2:目标 3:冒泡

    // 鼠标事件
    if (event instanceof MouseEvent) {
        console.log("客户端坐标:", event.clientX, event.clientY);
        console.log("页面坐标:", event.pageX, event.pageY);
        console.log("屏幕坐标:", event.screenX, event.screenY);
        console.log("按下的按钮:", event.button);
        console.log("修饰键:", event.ctrlKey, event.shiftKey, event.altKey);
    }

    // 键盘事件
    if (event instanceof KeyboardEvent) {
        console.log("键码:", event.keyCode);
        console.log("键:", event.key);
        console.log("代码:", event.code);
    }

    // 触摸事件
    if (event instanceof TouchEvent) {
        console.log("触摸点:", event.touches.length);
    }

    // 阻止默认行为
    event.preventDefault();

    // 停止传播
    event.stopPropagation();
    event.stopImmediatePropagation(); // 阻止其他监听器

    // 时间戳
    console.log("时间戳:", event.timeStamp);

    // 是否可信任
    console.log("是否用户触发:", event.isTrusted);
}
```

### 3. 自定义事件

```js
// 1. 创建自定义事件
const event = new Event("custom");
const customEvent = new CustomEvent("custom", {
    detail: { message: "Hello" },
    bubbles: true,
    cancelable: true,
});

// 2. 触发事件
const element = document.getElementById("myElement");
element.dispatchEvent(customEvent);

// 3. 监听自定义事件
element.addEventListener("custom", function (event) {
    console.log("自定义事件:", event.detail.message);
});

// 4. 创建事件目标
class MyEmitter extends EventTarget {
    emit(data) {
        this.dispatchEvent(new CustomEvent("message", { detail: data }));
    }
}

const emitter = new MyEmitter();
emitter.addEventListener("message", event => {
    console.log("收到消息:", event.detail);
});

emitter.emit({ text: "Hello World" });

// 5. 合成事件（模拟真实事件）
const clickEvent = new MouseEvent("click", {
    bubbles: true,
    cancelable: true,
    view: window,
    clientX: 100,
    clientY: 100,
});

button.dispatchEvent(clickEvent);
```

### 4. 常用事件类型

```js
// 鼠标事件
element.addEventListener("click", handleClick);
element.addEventListener("dblclick", handleDoubleClick);
element.addEventListener("mousedown", handleMouseDown);
element.addEventListener("mouseup", handleMouseUp);
element.addEventListener("mousemove", handleMouseMove);
element.addEventListener("mouseenter", handleMouseEnter);
element.addEventListener("mouseleave", handleMouseLeave);
element.addEventListener("mouseover", handleMouseOver);
element.addEventListener("mouseout", handleMouseOut);
element.addEventListener("contextmenu", handleContextMenu);

// 键盘事件
element.addEventListener("keydown", handleKeyDown);
element.addEventListener("keyup", handleKeyUp);
element.addEventListener("keypress", handleKeyPress);

// 表单事件
form.addEventListener("submit", handleSubmit);
form.addEventListener("reset", handleReset);
input.addEventListener("change", handleChange);
input.addEventListener("input", handleInput);
input.addEventListener("focus", handleFocus);
input.addEventListener("blur", handleBlur);

// 窗口事件
window.addEventListener("load", handleLoad);
window.addEventListener("DOMContentLoaded", handleDOMContentLoaded);
window.addEventListener("resize", handleResize);
window.addEventListener("scroll", handleScroll);
window.addEventListener("hashchange", handleHashChange);

// 触摸事件
element.addEventListener("touchstart", handleTouchStart);
element.addEventListener("touchmove", handleTouchMove);
element.addEventListener("touchend", handleTouchEnd);
element.addEventListener("touchcancel", handleTouchCancel);

// 媒体事件
video.addEventListener("play", handlePlay);
video.addEventListener("pause", handlePause);
video.addEventListener("ended", handleEnded);
video.addEventListener("timeupdate", handleTimeUpdate);

// 拖放事件
draggable.addEventListener("dragstart", handleDragStart);
dropzone.addEventListener("dragover", handleDragOver);
dropzone.addEventListener("drop", handleDrop);
```

## 样式和类操作

### 1. classList 操作

```js
const element = document.getElementById("myElement");

// 1. 添加类
element.classList.add("active", "highlighted");

// 2. 移除类
element.classList.remove("inactive");

// 3. 切换类
element.classList.toggle("visible");
element.classList.toggle("visible", true); // 强制添加
element.classList.toggle("visible", false); // 强制移除

// 4. 检查类
if (element.classList.contains("active")) {
    console.log("元素有 active 类");
}

// 5. 替换类
element.classList.replace("old-class", "new-class");

// 6. 遍历类
for (const className of element.classList) {
    console.log("类名:", className);
}

// 7. 获取类数组
const classes = Array.from(element.classList);

// 8. 批量操作
function updateClasses(element, toAdd, toRemove) {
    element.classList.remove(...toRemove);
    element.classList.add(...toAdd);
}

// 9. 条件添加类
function addClassIf(condition, className) {
    if (condition) {
        element.classList.add(className);
    } else {
        element.classList.remove(className);
    }
}

// 10. 类名切换动画
element.classList.add("fade-in");
setTimeout(() => {
    element.classList.remove("fade-in");
    element.classList.add("fade-out");
}, 1000);
```

### 2. style 操作

```js
const element = document.getElementById("myElement");

// 1. 直接设置样式
element.style.color = "red";
element.style.backgroundColor = "#f0f0f0";
element.style.fontSize = "16px";

// 2. 使用 setProperty（支持CSS变量）
element.style.setProperty("--primary-color", "#007bff");
element.style.setProperty("background-color", "blue", "important");

// 3. 获取样式
console.log("内联颜色:", element.style.color);

// 4. 移除样式
element.style.removeProperty("color");

// 5. 批量设置样式
Object.assign(element.style, {
    color: "white",
    backgroundColor: "black",
    padding: "10px",
});

// 6. 获取计算样式（最终应用的样式）
const computed = window.getComputedStyle(element);
console.log("实际颜色:", computed.color);
console.log("实际宽度:", computed.width);

// 7. 检查样式支持
if ("backgroundClip" in element.style) {
    element.style.backgroundClip = "text";
}

// 8. 设置 CSS 文本
element.style.cssText = "color: red; background: blue;";

// 9. 添加 CSS 类来应用样式
element.classList.add("styled-element");

// 10. 动态样式表
const style = document.createElement("style");
style.textContent = `
    .dynamic {
        color: var(--dynamic-color, red);
        transition: all 0.3s;
    }
`;
document.head.appendChild(style);
```

### 3. CSS 变量操作

```js
// 1. 设置 CSS 变量
const root = document.documentElement;

// 在根元素设置
root.style.setProperty("--primary-color", "#007bff");
root.style.setProperty("--spacing-unit", "8px");

// 在特定元素设置
const element = document.getElementById("myElement");
element.style.setProperty("--local-color", "#ff0000");

// 2. 获取 CSS 变量
const primaryColor = getComputedStyle(root).getPropertyValue("--primary-color").trim();

// 3. 删除 CSS 变量
root.style.removeProperty("--primary-color");

// 4. 监听 CSS 变量变化
const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        if (mutation.type === "attributes" && mutation.attributeName === "style") {
            const newValue = getComputedStyle(root).getPropertyValue("--primary-color");
            console.log("CSS变量变化:", newValue);
        }
    });
});

observer.observe(root, {
    attributes: true,
    attributeFilter: ["style"],
});

// 5. CSS 变量工具类
class CSSVariables {
    constructor(element = document.documentElement) {
        this.element = element;
    }

    set(variable, value) {
        this.element.style.setProperty(`--${variable}`, value);
        return this;
    }

    get(variable) {
        return getComputedStyle(this.element).getPropertyValue(`--${variable}`).trim();
    }

    remove(variable) {
        this.element.style.removeProperty(`--${variable}`);
        return this;
    }

    setMultiple(variables) {
        Object.entries(variables).forEach(([key, value]) => {
            this.set(key, value);
        });
        return this;
    }
}

// 使用
const cssVars = new CSSVariables();
cssVars.set("primary-color", "#007bff").set("secondary-color", "#6c757d");

console.log("主色:", cssVars.get("primary-color"));
```

## DOM 尺寸和位置

### 1. 元素尺寸

```js
const element = document.getElementById("myElement");

// 1. 偏移尺寸（包含边框、内边距、滚动条）
console.log("偏移宽度:", element.offsetWidth);
console.log("偏移高度:", element.offsetHeight);
console.log("偏移左边:", element.offsetLeft);
console.log("偏移顶部:", element.offsetTop);
console.log("偏移父元素:", element.offsetParent);

// 2. 客户端尺寸（包含内边距，不包含边框、滚动条）
console.log("客户端宽度:", element.clientWidth);
console.log("客户端高度:", element.clientHeight);
console.log("客户端左边:", element.clientLeft); // 左边框宽度
console.log("客户端顶部:", element.clientTop); // 上边框宽度

// 3. 滚动尺寸
console.log("滚动宽度:", element.scrollWidth);
console.log("滚动高度:", element.scrollHeight);
console.log("滚动左边:", element.scrollLeft);
console.log("滚动顶部:", element.scrollTop);

// 4. 获取边界矩形
const rect = element.getBoundingClientRect();
console.log("边界矩形:", {
    x: rect.x,
    y: rect.y,
    width: rect.width,
    height: rect.height,
    top: rect.top,
    right: rect.right,
    bottom: rect.bottom,
    left: rect.left,
});

// 5. 获取多个元素的边界
const rects = element.getClientRects();
console.log("多个边界矩形:", rects);

// 6. 检查元素是否在视口中
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= window.innerHeight &&
        rect.right <= window.innerWidth
    );
}

// 7. 获取计算样式尺寸
const style = window.getComputedStyle(element);
console.log("样式宽度:", style.width);
console.log("样式高度:", style.height);
console.log("内边距:", style.padding);
console.log("边框:", style.borderWidth);

// 8. 实际内容尺寸
function getContentSize(element) {
    const style = window.getComputedStyle(element);
    const width =
        element.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    const height =
        element.clientHeight - parseFloat(style.paddingTop) - parseFloat(style.paddingBottom);
    return { width, height };
}
```

### 2. 窗口和文档尺寸

```js
// 1. 窗口尺寸
console.log("窗口宽度:", window.innerWidth);
console.log("窗口高度:", window.innerHeight);
console.log("视口宽度:", document.documentElement.clientWidth);
console.log("视口高度:", document.documentElement.clientHeight);

// 2. 屏幕尺寸
console.log("屏幕宽度:", screen.width);
console.log("屏幕高度:", screen.height);
console.log("可用宽度:", screen.availWidth);
console.log("可用高度:", screen.availHeight);

// 3. 文档尺寸
console.log("文档宽度:", document.documentElement.scrollWidth);
console.log("文档高度:", document.documentElement.scrollHeight);
console.log("文档滚动位置X:", window.pageXOffset || document.documentElement.scrollLeft);
console.log("文档滚动位置Y:", window.pageYOffset || document.documentElement.scrollTop);

// 4. 元素相对于文档的位置
function getElementPosition(element) {
    const rect = element.getBoundingClientRect();
    return {
        x: rect.left + window.pageXOffset,
        y: rect.top + window.pageYOffset,
        width: rect.width,
        height: rect.height,
    };
}

// 5. 检查元素是否可见
function isElementVisible(element) {
    const style = window.getComputedStyle(element);
    if (style.display === "none" || style.visibility === "hidden" || style.opacity === "0") {
        return false;
    }

    const rect = element.getBoundingClientRect();
    return !(rect.width === 0 || rect.height === 0);
}

// 6. 获取鼠标位置
document.addEventListener("mousemove", event => {
    console.log("页面位置:", event.pageX, event.pageY);
    console.log("客户端位置:", event.clientX, event.clientY);
    console.log("屏幕位置:", event.screenX, event.screenY);
});

// 7. 转换坐标
function pageToClient(x, y) {
    return {
        x: x - window.pageXOffset,
        y: y - window.pageYOffset,
    };
}

function clientToPage(x, y) {
    return {
        x: x + window.pageXOffset,
        y: y + window.pageYOffset,
    };
}
```

### 3. 滚动控制

```js
const element = document.getElementById("scrollable");

// 1. 滚动到位置
element.scrollTo(0, 100);
element.scrollTo({
    top: 100,
    left: 0,
    behavior: "smooth", // 'auto' 或 'smooth'
});

// 2. 相对滚动
element.scrollBy(0, 50);
element.scrollBy({
    top: 50,
    behavior: "smooth",
});

// 3. 滚动到元素
const target = document.getElementById("target");
target.scrollIntoView();
target.scrollIntoView({
    behavior: "smooth",
    block: "start", // 'start', 'center', 'end', 'nearest'
    inline: "nearest",
});

// 4. 监听滚动事件
element.addEventListener("scroll", event => {
    console.log("滚动位置:", element.scrollTop);
});

// 防抖的滚动监听
function debouncedScroll(callback, delay = 100) {
    let timeout;
    return function (event) {
        clearTimeout(timeout);
        timeout = setTimeout(() => callback(event), delay);
    };
}

element.addEventListener(
    "scroll",
    debouncedScroll(event => {
        console.log("滚动结束");
    })
);

// 5. 滚动方向检测
let lastScrollTop = 0;
element.addEventListener("scroll", () => {
    const scrollTop = element.scrollTop;
    const direction = scrollTop > lastScrollTop ? "down" : "up";
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    console.log("滚动方向:", direction);
});

// 6. 虚拟滚动（大数据量优化）
class VirtualScroller {
    constructor(container, itemHeight, totalItems, renderItem) {
        this.container = container;
        this.itemHeight = itemHeight;
        this.totalItems = totalItems;
        this.renderItem = renderItem;
        this.visibleItems = Math.ceil(container.clientHeight / itemHeight);
        this.startIndex = 0;
        this.endIndex = this.startIndex + this.visibleItems;

        this.init();
    }

    init() {
        // 设置容器高度
        this.container.style.height = `${this.totalItems * this.itemHeight}px`;

        // 创建视口
        this.viewport = document.createElement("div");
        this.viewport.style.position = "relative";
        this.viewport.style.height = "100%";
        this.container.appendChild(this.viewport);

        // 监听滚动
        this.container.addEventListener("scroll", () => {
            this.update();
        });

        this.update();
    }

    update() {
        const scrollTop = this.container.scrollTop;
        this.startIndex = Math.floor(scrollTop / this.itemHeight);
        this.endIndex = Math.min(
            this.startIndex + this.visibleItems + 2, // 缓冲
            this.totalItems
        );

        this.render();
    }

    render() {
        // 清空视口
        this.viewport.innerHTML = "";

        // 渲染可见项
        for (let i = this.startIndex; i < this.endIndex; i++) {
            const item = this.renderItem(i);
            item.style.position = "absolute";
            item.style.top = `${i * this.itemHeight}px`;
            item.style.width = "100%";
            item.style.height = `${this.itemHeight}px`;
            this.viewport.appendChild(item);
        }
    }
}
```

## DOM 性能优化

### 1. 批量操作

```js
// 1. 使用 DocumentFragment
function appendManyItems(items) {
    const fragment = document.createDocumentFragment();

    items.forEach(item => {
        const div = document.createElement("div");
        div.textContent = item;
        fragment.appendChild(div);
    });

    container.appendChild(fragment);
}

// 2. 使用 innerHTML（小心XSS）
function appendManyHTML(items) {
    const html = items.map(item => `<div>${item}</div>`).join("");
    container.innerHTML += html;
}

// 3. 使用 insertAdjacentHTML
function appendAdjacent(items) {
    const html = items.map(item => `<div>${item}</div>`).join("");
    container.insertAdjacentHTML("beforeend", html);
}

// 4. 隐藏元素进行批量操作
function batchUpdate(element, operations) {
    // 隐藏元素
    element.style.display = "none";

    // 执行操作
    operations.forEach(op => op());

    // 显示元素
    element.style.display = "";
}

// 5. 使用 requestAnimationFrame
function smoothAppend(items, index = 0) {
    if (index >= items.length) return;

    requestAnimationFrame(() => {
        const div = document.createElement("div");
        div.textContent = items[index];
        container.appendChild(div);

        smoothAppend(items, index + 1);
    });
}

// 6. 防抖和节流
const debouncedUpdate = debounce(updateDOM, 100);
const throttledUpdate = throttle(updateDOM, 100);

window.addEventListener("resize", debouncedUpdate);
window.addEventListener("scroll", throttledUpdate);
```

### 2. 事件优化

```js
// 1. 事件委托
document.getElementById("list").addEventListener("click", function (event) {
    if (event.target.classList.contains("item")) {
        handleItemClick(event.target);
    }
});

// 2. 使用 passive 事件监听器
document.addEventListener("touchstart", handleTouch, { passive: true });
document.addEventListener("wheel", handleWheel, { passive: true });

// 3. 使用 once 选项
button.addEventListener("click", handleClick, { once: true });

// 4. 使用 AbortSignal 管理事件
const controller = new AbortController();
const signal = controller.signal;

element.addEventListener("click", handleClick, { signal });
element.addEventListener("mouseover", handleMouseOver, { signal });

// 稍后取消所有事件
controller.abort();

// 5. 节流滚动事件
let ticking = false;
window.addEventListener("scroll", () => {
    if (!ticking) {
        requestAnimationFrame(() => {
            handleScroll();
            ticking = false;
        });
        ticking = true;
    }
});

// 6.  IntersectionObserver 替代滚动检测
const observer = new IntersectionObserver(
    entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                console.log("元素进入视口:", entry.target);
            }
        });
    },
    {
        threshold: 0.1,
        rootMargin: "50px",
    }
);

observer.observe(element);
```

### 3. 内存管理

```js
class DOMManager {
    constructor() {
        this.elements = new WeakMap();
        this.eventListeners = new Map();
        this.observers = new Set();
    }

    // 跟踪元素
    trackElement(element, data = {}) {
        this.elements.set(element, {
            created: Date.now(),
            ...data,
        });
        return element;
    }

    // 安全添加事件
    addEventListener(element, type, handler, options) {
        element.addEventListener(type, handler, options);

        const key = `${type}-${handler.name || "anonymous"}`;
        if (!this.eventListeners.has(element)) {
            this.eventListeners.set(element, new Map());
        }
        this.eventListeners.get(element).set(key, { type, handler, options });
    }

    // 安全移除事件
    removeEventListeners(element, type = null) {
        if (!this.eventListeners.has(element)) return;

        const listeners = this.eventListeners.get(element);
        for (const [key, { type: listenerType, handler, options }] of listeners) {
            if (!type || listenerType === type) {
                element.removeEventListener(listenerType, handler, options);
                listeners.delete(key);
            }
        }

        if (listeners.size === 0) {
            this.eventListeners.delete(element);
        }
    }

    // 添加观察者
    addObserver(observer) {
        this.observers.add(observer);
    }

    // 清理所有资源
    cleanup() {
        // 移除所有事件监听器
        for (const [element, listeners] of this.eventListeners) {
            for (const { type, handler, options } of listeners.values()) {
                element.removeEventListener(type, handler, options);
            }
        }
        this.eventListeners.clear();

        // 断开所有观察者
        for (const observer of this.observers) {
            observer.disconnect();
        }
        this.observers.clear();

        // 移除所有跟踪的元素
        this.elements = new WeakMap();

        // 强制垃圾回收（如果可用）
        if (typeof gc === "function") {
            gc();
        }
    }

    // 检查内存泄漏
    checkMemoryLeaks() {
        const realElements = new Set();

        // 收集实际存在的元素
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_ELEMENT,
            null,
            false
        );

        let node;
        while ((node = walker.nextNode())) {
            realElements.add(node);
        }

        // 检查跟踪的元素是否还在DOM中
        let leaks = 0;
        for (const element of this.elements) {
            if (!realElements.has(element)) {
                console.warn("检测到可能的内存泄漏:", element);
                leaks++;
            }
        }

        return leaks;
    }
}

// 使用
const manager = new DOMManager();
const element = manager.trackElement(document.createElement("div"), { type: "dynamic" });

manager.addEventListener(element, "click", () => {
    console.log("点击");
});

// 清理时
// manager.cleanup();
```

## 现代 DOM API

### 1. IntersectionObserver

```js
// 1. 基础使用
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        console.log("是否相交:", entry.isIntersecting);
        console.log("相交比例:", entry.intersectionRatio);
        console.log("边界矩形:", entry.boundingClientRect);
        console.log("根边界:", entry.rootBounds);
        console.log("目标:", entry.target);

        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
        } else {
            entry.target.classList.remove("visible");
        }
    });
});

// 观察元素
observer.observe(element);

// 2. 配置选项
const options = {
    root: document.querySelector("#scrollArea"), // 默认为视口
    rootMargin: "0px 0px -100px 0px", // 类似 CSS margin
    threshold: [0, 0.25, 0.5, 0.75, 1], // 触发阈值的数组
};

const detailedObserver = new IntersectionObserver(callback, options);

// 3. 懒加载图片
const lazyImages = document.querySelectorAll("img[data-src]");
const imageObserver = new IntersectionObserver(
    entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove("lazy");
                imageObserver.unobserve(img);
            }
        });
    },
    {
        rootMargin: "50px 0px",
        threshold: 0.01,
    }
);

lazyImages.forEach(img => imageObserver.observe(img));

// 4. 无限滚动
const sentinel = document.createElement("div");
sentinel.id = "sentinel";
container.appendChild(sentinel);

const infiniteObserver = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
        loadMoreItems();
    }
});

infiniteObserver.observe(sentinel);

// 5. 广告可见性检测
const adObserver = new IntersectionObserver(
    entries => {
        entries.forEach(entry => {
            if (entry.isIntersectionRatio >= 0.5) {
                console.log("广告至少50%可见");
                recordAdView(entry.target);
            }
        });
    },
    {
        threshold: [0, 0.25, 0.5, 0.75, 1],
    }
);

adObserver.observe(adElement);

// 6. 暂停观察
observer.unobserve(element);
observer.disconnect();
```

### 2. MutationObserver

```js
// 1. 监听 DOM 变化
const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        console.log("变化类型:", mutation.type);

        switch (mutation.type) {
            case "attributes":
                console.log(
                    "属性变化:",
                    mutation.attributeName,
                    mutation.target,
                    mutation.oldValue
                );
                break;

            case "childList":
                console.log("子节点变化:");
                mutation.addedNodes.forEach(node => {
                    console.log("添加:", node);
                });
                mutation.removedNodes.forEach(node => {
                    console.log("移除:", node);
                });
                break;

            case "characterData":
                console.log("文本变化:", mutation.target, mutation.oldValue);
                break;
        }
    });
});

// 2. 开始观察
observer.observe(element, {
    attributes: true,
    attributeOldValue: true,
    attributeFilter: ["class", "style"], // 只观察特定属性
    childList: true,
    subtree: true, // 观察所有后代
    characterData: true,
    characterDataOldValue: true,
});

// 3. 停止观察
observer.disconnect();

// 4. 获取所有记录
const records = observer.takeRecords();
console.log("未处理的变更:", records);

// 5. 实际应用：动态内容监听
class ContentMonitor {
    constructor(selector, callback) {
        this.selector = selector;
        this.callback = callback;
        this.observer = null;
        this.init();
    }

    init() {
        // 初始检查
        this.checkElements();

        // 监听 DOM 变化
        this.observer = new MutationObserver(() => {
            this.checkElements();
        });

        this.observer.observe(document.body, {
            childList: true,
            subtree: true,
        });
    }

    checkElements() {
        const elements = document.querySelectorAll(this.selector);
        elements.forEach(element => {
            if (!element.dataset.monitored) {
                element.dataset.monitored = "true";
                this.callback(element);
            }
        });
    }

    destroy() {
        if (this.observer) {
            this.observer.disconnect();
        }
    }
}

// 使用
const monitor = new ContentMonitor(".dynamic-item", element => {
    console.log("新动态项目:", element);
});
```

### 3. ResizeObserver

```js
// 1. 监听元素尺寸变化
const resizeObserver = new ResizeObserver(entries => {
    for (const entry of entries) {
        console.log("元素尺寸变化:", entry.target);
        console.log("内容矩形:", entry.contentRect);
        console.log("边框尺寸:", entry.borderBoxSize);
        console.log("内容尺寸:", entry.contentBoxSize);

        const { width, height } = entry.contentRect;
        entry.target.style.setProperty("--element-width", `${width}px`);
        entry.target.style.setProperty("--element-height", `${height}px`);
    }
});

// 观察元素
resizeObserver.observe(element);

// 2. 响应式设计
const responsiveObserver = new ResizeObserver(entries => {
    const entry = entries[0];
    const width = entry.contentRect.width;

    if (width < 768) {
        entry.target.classList.add("mobile");
        entry.target.classList.remove("tablet", "desktop");
    } else if (width < 1024) {
        entry.target.classList.add("tablet");
        entry.target.classList.remove("mobile", "desktop");
    } else {
        entry.target.classList.add("desktop");
        entry.target.classList.remove("mobile", "tablet");
    }
});

responsiveObserver.observe(container);

// 3. 图表重绘
class ResponsiveChart {
    constructor(container) {
        this.container = container;
        this.chart = null;
        this.observer = new ResizeObserver(() => this.redraw());
        this.observer.observe(container);
        this.initChart();
    }

    initChart() {
        // 初始化图表
        this.chart = {
            /* 图表实例 */
        };
        this.redraw();
    }

    redraw() {
        const { width, height } = this.container.getBoundingClientRect();
        // 根据新尺寸重绘图表
        console.log("重绘图表，新尺寸:", width, "x", height);
    }

    destroy() {
        this.observer.disconnect();
        // 清理图表
    }
}

// 4. 防抖的尺寸监听
function createDebouncedResizeObserver(callback, delay = 100) {
    let timeout;

    return new ResizeObserver(entries => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            callback(entries);
        }, delay);
    });
}

const debouncedObserver = createDebouncedResizeObserver(entries => {
    console.log("尺寸稳定后的变化:", entries);
});

debouncedObserver.observe(element);

// 5. 停止观察
resizeObserver.unobserve(element);
resizeObserver.disconnect();
```

## 最佳实践总结

### 1. 性能最佳实践

```js
// 1. 批量 DOM 操作
function updateList(items) {
    // ❌ 不好：多次重排
    items.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        list.appendChild(li);
    });

    // ✅ 好：使用 DocumentFragment
    const fragment = document.createDocumentFragment();
    items.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        fragment.appendChild(li);
    });
    list.appendChild(fragment);

    // ✅ 好：使用 innerHTML（注意XSS）
    const html = items.map(item => `<li>${escapeHTML(item)}</li>`).join("");
    list.innerHTML = html;
}

// 2. 事件委托
// ❌ 不好：为每个按钮添加监听器
document.querySelectorAll(".btn").forEach(btn => {
    btn.addEventListener("click", handleClick);
});

// ✅ 好：事件委托
document.addEventListener("click", event => {
    if (event.target.matches(".btn")) {
        handleClick(event);
    }
});

// 3. 使用现代 API
// ❌ 不好：使用 scroll 事件检测可见性
window.addEventListener("scroll", () => {
    const rect = element.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
        console.log("元素可见");
    }
});

// ✅ 好：使用 IntersectionObserver
const observer = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
        console.log("元素可见");
    }
});
observer.observe(element);

// 4. 避免强制同步布局
function updateWidths() {
    // ❌ 不好：强制同步布局
    const width = element.offsetWidth;
    element.style.width = width + 10 + "px";
    const newWidth = element.offsetWidth; // 强制重排

    // ✅ 好：批量读取和写入
    const width = element.offsetWidth;
    const newWidth = width + 10;
    element.style.width = newWidth + "px";
}

// 5. 使用 CSS 类而不是内联样式
// ❌ 不好：直接修改样式
element.style.display = "block";
element.style.opacity = "1";
element.style.transform = "translateY(0)";

// ✅ 好：使用 CSS 类
element.classList.add("visible");

// CSS:
// .visible {
//     display: block;
//     opacity: 1;
//     transform: translateY(0);
//     transition: all 0.3s ease;
// }
```

### 2. 安全最佳实践

```js
// 1. 防止 XSS
function safeHTML(html) {
    const div = document.createElement("div");
    div.textContent = html; // 自动转义
    return div.innerHTML;
}

// 或使用 textContent
element.textContent = userInput;

// 2. 验证和清理
function sanitizeHTML(html) {
    const template = document.createElement("template");
    template.innerHTML = html;

    // 移除危险元素
    template.content.querySelectorAll("script, style").forEach(el => {
        el.remove();
    });

    // 移除危险属性
    template.content.querySelectorAll("*").forEach(el => {
        el.removeAttribute("onclick");
        el.removeAttribute("onload");
        // 移除其他危险属性
    });

    return template.innerHTML;
}

// 3. 使用 Content Security Policy (CSP)
// 在 HTML 中添加：
// <meta http-equiv="Content-Security-Policy" content="default-src 'self'">

// 4. 安全的动态脚本加载
function loadScript(src, integrity) {
    return new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = src;

        if (integrity) {
            script.integrity = integrity;
            script.crossOrigin = "anonymous";
        }

        script.onload = resolve;
        script.onerror = reject;

        document.head.appendChild(script);
    });
}

// 5. 安全的 iframe 嵌入
function createSafeIframe(src) {
    const iframe = document.createElement("iframe");
    iframe.sandbox = "allow-same-origin allow-scripts allow-forms";
    iframe.src = src;
    iframe.referrerPolicy = "no-referrer";
    iframe.loading = "lazy";
    return iframe;
}
```

### 3. 可维护性最佳实践

```js
// 1. 使用组件模式
class MyComponent {
    constructor(config) {
        this.config = config;
        this.element = null;
        this.init();
    }

    init() {
        this.createElement();
        this.bindEvents();
        this.render();
    }

    createElement() {
        this.element = document.createElement("div");
        this.element.className = "my-component";
    }

    bindEvents() {
        this.element.addEventListener("click", this.handleClick.bind(this));
    }

    handleClick(event) {
        // 事件处理
    }

    render() {
        this.element.innerHTML = `
            <div class="title">${this.config.title}</div>
            <div class="content">${this.config.content}</div>
        `;
    }

    mount(container) {
        container.appendChild(this.element);
    }

    destroy() {
        this.element.remove();
        // 清理事件监听器等其他资源
    }
}

// 使用
const component = new MyComponent({
    title: "Hello",
    content: "World",
});
component.mount(document.body);

// 2. 使用数据属性
<button data-action="save" data-id="123">
    保存
</button>;

document.addEventListener("click", event => {
    const button = event.target.closest("[data-action]");
    if (button) {
        const action = button.dataset.action;
        const id = button.dataset.id;

        switch (action) {
            case "save":
                saveItem(id);
                break;
            case "delete":
                deleteItem(id);
                break;
        }
    }
});

// 3. 分离关注点
// HTML 负责结构
// CSS 负责样式
// JavaScript 负责行为

// 4. 使用自定义事件
class DataTable {
    constructor(element) {
        this.element = element;
        this.init();
    }

    init() {
        this.element.addEventListener("click", event => {
            if (event.target.matches(".row")) {
                const id = event.target.dataset.id;
                this.element.dispatchEvent(
                    new CustomEvent("rowclick", {
                        detail: { id },
                        bubbles: true,
                    })
                );
            }
        });
    }
}

// 使用
const table = new DataTable(document.getElementById("table"));
table.element.addEventListener("rowclick", event => {
    console.log("行点击:", event.detail.id);
});

// 5. 错误处理
function safeDOMOperation(operation) {
    try {
        return operation();
    } catch (error) {
        console.error("DOM 操作失败:", error);
        // 优雅降级或显示错误消息
        return null;
    }
}

// 使用
safeDOMOperation(() => {
    document.getElementById("nonexistent").innerHTML = "test";
});
```

## 总结要点：

-   理解 DOM 树结构，掌握节点关系和操作
-   优先使用现代 API：querySelector、classList、dataset
-   注重性能：批量操作、事件委托、使用观察者
-   确保安全性：防止 XSS、验证输入、使用 CSP
-   保持可维护性：组件化、分离关注点、错误处理
-   利用现代浏览器特性：IntersectionObserver、MutationObserver、ResizeObserver
-   优化用户体验：虚拟滚动、懒加载、平滑动画
-   内存管理：及时清理事件监听器、观察者、引用
