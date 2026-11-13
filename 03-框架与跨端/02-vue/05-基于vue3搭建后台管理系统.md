# 基于vue3+vite+ts+elementplus+pinia+axios搭建后台管理系统

## 创建项目
```shell
npm init vite@latest YOURPROJECTNAME --template vue-ts
```

## ESLint 代码检测

> ESLint 可组装的JavaScript和JSX检查工具，目标是保证代码的一致性和避免错误。

### ESLint 安装

#### ESLint 插件安装

vscode 插件市场搜索 ESLint 插件并安装

#### ESLint 依赖安装

```shell
npx eslint --init
```

> 会自动生成`eslint.config.js`文件

#### ESLint 忽略配置(.eslintignore)（可选）

> 在根目录下新建`.eslintignore`文件，添加忽略文件

```
dist
node_modules
public
.husky
.vscode
.idea
*.sh
*.md

src/assets

.eslintrc.cjs
.prettierrc.cjs
.stylelintrc.cjs
```

## Prettier 代码格式化

### 安装 Prettier 插件

> VSCode 插件市场搜索 Prettier - Code formatter 插件安装

### 格式化忽略配置( .prettierignore)

> 根目录下新建 `.prettierignore`文件，添加配置
```
dist
node_modules
public
.husky
.vscode
.idea
*.sh
*.md

src/assets
```

### Prettier 保存自动格式化

VSCode 的 settings.json 配置:

```
{
  "editor.formatOnSave": true, // 保存格式化文件
  "editor.defaultFormatter": "esbenp.prettier-vscode" // 指定 prettier 为所有文件默认格式化器
}
```

## 设置端口和本地访问域名

```ts
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
    server: {
        port: 5175,
        host: 'saas_ads.com',
    },
});
```

> 需要更改本地host文件
> windows: `C:\Windows\System32\drivers\etc\hosts`
> macos: `/etc/hosts`

```shell
127.0.0.1		saas_ads.com
```

--------------------------------- 分割线 ---------------------------------

## 环境变量

Vite 环境变量主要是为了区分开发、测试、生产等环境的变量

[Vite 环境变量配置官方文档](https://cn.vite.dev/guide/env-and-mode.html)

### env配置文件

项目根目录新建 `.env.development`、`.env.production`

```env
# .env.development
# 变量必须以 VITE_ 为前缀才能暴露给外部读取
VITE_APP_TITLE = 'saas-ads'
VITE_APP_PORT = 5175
VITE_APP_BASE_API = '/api'
```

```env
# .env.production
VITE_APP_TITLE = 'saas-ads'
VITE_APP_PORT = 5175
VITE_APP_BASE_API = '/api'
```

### 环境变量智能提示

新建 `src/types/env.d.ts` 文件存放环境变量TS类型声明

```ts
// src/types/env.d.ts
interface ImportMetaEnv {
    /**
     * 应用标题
     */
    VITE_APP_TITLE: string;
    /**
     * 应用端口
     */
    VITE_APP_PORT: number;
    /**
     * API基础路径(反向代理)
     */
    VITE_APP_BASE_API: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}
```

### 使用

1、在html中使用
```html
<title>%VITE_APP_TITLE%</title>
```

2、在`vite.config.ts`中使用
```ts
import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd(), "");
    return {
        server: {
            port: Number(env.VITE_APP_PORT),
            host: "saas_ads.com",
            proxy: {
                [env.VITE_APP_BASE_API]: {
                    target: "https://saas_api.com",
                    changeOrigin: true,
                    rewrite: path => path.replace(/^\/api/, ""),
                },
            },
        },
    };
});
```

2、在`*.ts`中使用
```ts
console.log(import.meta.env.VITE_APP_TITLE);
```

--------------------------------- 分割线 ---------------------------------

## 跨域

> 本地开发环境通过 Vite 配置反向代理解决浏览器跨域问题，生产环境则是通过 nginx 配置反向代理 。

看上一节内容


--------------------------------- 分割线 ---------------------------------

## src 路径别名配置

相对路径别名配置，使用 @ 代替 src

### 安装 @types/node

```shell
yarn add 安装 @types/node -D
```

### 修改 vite.config.ts

```ts
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, './src'),
        },
    },
    server: {
        port: 5175,
    },
});
```

### 修改 tsconfig.json

> 如果有 `tsconfig.app.json`文件，建议放至`tsconfig.app.json`文件中。

```json
// tsconfig.json
{
    "compilerOptions": {
        "baseUrl": ".",
        "paths": {
            "@/*": ["./src/*"]
        }
    }
}
```

--------------------------------- 分割线 ---------------------------------

## 集成 Pinia

[Pinia官方文档](https://pinia.vuejs.org/zh)

### 安装Pinia依赖

```shell
yarn add pinia
```

### 引入 pinia

新建`src/store`目录并新建 `index.ts`文件

```ts
// src/store/index.ts
import { createPinia } from 'pinia';

// 这里导入store/modules下的状态文件
// import useStoreCounter from './modules/counter';
// ...

const pinia = createPinia();

// 这里导出
// export { useStoreCounter };
export default pinia;
```

#### main.ts引入store

```ts
// src/main.ts
import { createApp } from 'vue';

import App from './App.vue';
import store from '@/store';

import './style.css';

const app = createApp(App);
app.use(store);

app.mount('#app');
```

### 定义store

这里定义一个官网上的 计数器 为例

```ts
// src/store/counter.ts
import { ref, computed } from "vue";
import { defineStore } from "pinia";

export default defineStore("counter", () => {
    // ref变量 → state 属性
    const count = ref(0);
    // computed计算属性 → getters
    const double = computed(() => {
        return count.value * 2;
    });
    // function函数 → actions
    function increment() {
        count.value++;
    }

    return { count, double, increment };
});
```

在 `src/store/index.ts`中导出 `useStoreCounter`

使用 `useStoreCounter`

```vue
<script setup lang="ts">
import { useStoreCounter } from "@/store";
const counterStore = useStoreCounter();
</script>

<template>
    <button @click="counterStore.increment">count++</button>
    <div>数字： {{ counterStore.count }}</div>
    <div>加倍：{{ counterStore.double }}</div>
</template>
```

--------------------------------- 分割线 ---------------------------------

## 集成 Element Plus

### 安装 Element Plus 依赖 和 unplugin-vue-components unplugin-auto-import

```shell
yarn add element-plus
yarn add unplugin-vue-components unplugin-auto-import -D
```

### 引用样式
```ts
// main.ts
import 'element-plus/dist/index.css';
```

### 配置 vite.config.ts

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// Element Plus
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";

export default defineConfig({
    plugins: [
        vue(),
        // 自动导入 Element Plus API
        AutoImport({
            resolvers: [ElementPlusResolver()],
        }),
        // 自动导入 Element Plus 组件
        Components({
            resolvers: [ElementPlusResolver()],
        }),
    ],
});
```

### 配置 TypeScript 支持

> 如果有 `tsconfig.app.json`文件，建议放至`tsconfig.app.json`文件中。

```json
// tsconfig.json
{
    "compilerOptions": {
        "types": ["element-plus/global"] // 添加 Element Plus 的类型支持
    }
}
```

### 使用 Element Plus 组件

```vue
<template>
    <el-button type="primary">Primary Button</el-button>
</template>
```

### 自定义主题

#### 安装 sass 依赖

```shell
yarn add sass -D
```

#### 修改 vite.config.ts

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers';

export default defineConfig({
    plugins: [
        vue(),
        AutoImport({
            resolvers: [ElementPlusResolver()],
        }),
        Components({
            resolvers: [ElementPlusResolver({ importStyle: 'sass' })], // 使用 sass
        }),
    ],
    css: {
        preprocessorOptions: {
            scss: {
                additionalData: `@use "@/styles/element/index.scss" as *;`, // 自定义主题文件路径
            },
        },
    },
});
```

### 创建自定义主题文件

```scss
// src/styles/element/index.scss
@forward "element-plus/theme-chalk/src/common/var.scss" with (
  $colors: (
    "primary": (
      "base": #409eff,
    ),
  )
);

// If you just import on demand, you can ignore the following content.
// 如果你想导入所有样式:
// tips: 我导入了，可报@use死循环了，最终还是注释掉了
// @use "element-plus/theme-chalk/src/index.scss" as *;
```

### 报 ESLint `找不到名称“ElMessage”。`错误

> 即使你按照上面的配置都正确，编辑器可能还是会报这个 TS 错误。
> 解决方法：手动声明全局 element-plus 组件/api 类型

```js
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";

/** @type {import('eslint').Linter.Config[]} */
export default [
   {
        globals: {
            "ElMessage": "readonly"
        }
    }
];
```
```ts
// src/types/element-plus.d.ts
export {};
declare global {
    const ElMessage: typeof import("element-plus")["ElMessage"];
    const ElMessageBox: typeof import("element-plus")["ElMessageBox"];
    const ElLoading: typeof import("element-plus")["ElLoading"];
    // ...
}
```
```json
// src/tsconfig.app.json
{
    "include": ["src/types/*.d.ts"],
}
```

--------------------------------- 分割线 ---------------------------------

## 集成 sass

### 安装 sass 依赖

```shell
yarn add sass -D
```

### 创建全局样式文件 main.scss

> 优化建议：
> 创建项目时,有默认的`src/style.css`，在`main.ts`文件中引用了。可以将`styles.css`样式，选择需要的复制到`src/styles/main.scss`文件中，删除`style.css`也它的引用

```scss
// src/styles/main.scss
$primary-color: #409eff;

body {
  font-family: Arial, sans-serif;
  background-color: $primary-color;
}

.container {
  padding: 20px;
  color: white;
}
```

### 全局引入 main.scss

一般情况下，修改 `main.ts`

```ts
import '@/styles/main.scss';
```

--------------------------------- 分割线 ---------------------------------

## 集成 vite-plugin-svg-icons 使用Iconfont 第三方图标库实现本地图标

### 安装依赖

```shell
yarn add vite-plugin-svg-icons -D
```

###  配置 Vite

```ts
// vite.config.ts
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// vite-plugin-svg-icons
import { createSvgIconsPlugin } from "vite-plugin-svg-icons";

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        // vite-plugin-svg-icons
        createSvgIconsPlugin({
            // 指定需要缓存的图标文件夹
            iconDirs: [path.resolve(process.cwd(), "src/assets/icons")],
            // 指定symbolId格式
            symbolId: "icon-[dir]-[name]",
        }),
    ],
});

```

### 创建 SVG 图标组件

```vue
<!-- src/components/SvgIcon.vue -->
<template>
    <svg aria-hidden="true" class="svg-icon">
        <use :xlink:href="symbolId" />
    </svg>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
    name: {
        type: String,
        required: true,
    },
});

const symbolId = computed(() => `#icon-${props.name}`);
</script>

<style scoped>
.svg-icon {
    width: 1em;
    height: 1em;
    vertical-align: -0.15em;
    fill: currentColor;
    overflow: hidden;
}
</style>
```

### 使用 Iconfont 图标

你可以从 Iconfont 下载 SVG 图标，并将其放入 src/assets/icons 目录中。然后，你可以通过 SvgIcon 组件来使用这些图标。

例如，假设你下载了一个名为 home.svg 的图标，你可以这样使用它：

```vue
<template>
  <div>
    <SvgIcon name="home" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import SvgIcon from '@/components/SvgIcon.vue';

export default defineComponent({
  components: {
    SvgIcon,
  },
});
</script>
```

### 自动导入 SVG 图标
```ts
// main.ts
import { createApp } from 'vue';
import App from './App.vue';
import 'virtual:svg-icons-register'; // 自动导入 SVG 图标

const app = createApp(App);
app.mount('#app');
```

使用：

```vue
<template>
  <div>
    <SvgIcon name="home" />
  </div>
</template>
```

### 为 TypeScript 添加类型声明

```ts
// src/vite-env.d.ts
/// <reference types="vite-plugin-svg-icons/client" />
```

--------------------------------- 分割线 ---------------------------------

## 集成 Axios

### 安装依赖

```shell
yarn add axios
```

### Axios 工具类封装

```ts
// src/utils/request.ts
import axios, { type InternalAxiosRequestConfig, type AxiosResponse } from "axios";

// 创建 axios 实例
const service = axios.create({
    baseURL: import.meta.env.VITE_APP_BASE_API,
    timeout: 50000,
    headers: { "Content-Type": "application/json;charset=utf-8" },
});

// 请求拦截器
service.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        // const userStore = useUserStoreHook();
        // if (userStore.token) {
        //     config.headers.Authorization = userStore.token;
        // }
        return config;
    },
    (error: unknown) => {
        return Promise.reject(error);
    }
);

// 响应拦截器
service.interceptors.response.use(
    (response: AxiosResponse) => {
        const { msg } = response.data;
        // const { code, msg } = response.data;
        // if (code === "00000") {
        //     return response.data;
        // }

        // ElMessage.error(msg || "系统出错");
        return Promise.reject(new Error(msg || "Error"));
    },
    (error: any) => {
        if (error.response.data) {
            // const { code, msg } = error.response.data;
            // token 过期，跳转登录页
            // if (code === "A0230") {
            //     ElMessageBox.confirm("当前页面已失效，请重新登录", "提示", {
            //         confirmButtonText: "确定",
            //         type: "warning",
            //     }).then(() => {
            //         localStorage.clear(); // @vueuse/core 自动导入
            //         window.location.href = "/";
            //     });
            // } else {
            //     ElMessage.error(msg || "系统出错");
            // }
        }
        return Promise.reject(error.message);
    }
);

// 导出 axios 实例
export default service;
```

### 使用示例

```ts
// src/api/auth.ts
import request from "@/utils/request";
import type { AxiosPromise } from "axios";
import { LoginData, LoginResult } from "./types";

/**
 * 登录API
 *
 * @param data {LoginData}
 * @returns
 */
export function loginApi(data: LoginData): AxiosPromise<LoginResult> {
    return request({
        url: "/api/v1/auth/login",
        method: "post",
        params: data,
    });
}
```

--------------------------------- 分割线 ---------------------------------

## 集成 vue-router (静态) 及 layout布局

### 安装 vue-router 依赖
```shell
yarn add vue-router
```

### 项目结构
```
src/
├── assets/
├── components/
├── layouts/          // 布局组件
│   └── MainLayout.vue
├── router/           // 路由配置
│   └── index.ts
├── views/            // 页面组件
│   ├── Dashboard.vue
│   ├── Login.vue
│   ├── UserManagement.vue
│   └── Settings.vue
├── App.vue
└── main.ts
```

### 创建布局组件

```vue
<!-- src/layouts/MainLayout.vue -->
<template>
    <div class="main-layout">
        <header>
            <h1>Admin System</h1>
            <nav>
                <router-link to="/dashboard">Dashboard</router-link> |
                <router-link to="/user-management">User Management</router-link> |
                <router-link to="/settings">Settings</router-link> |
                <button @click="handleLogout">Logout</button>
            </nav>
        </header>

        <aside>
            <ul>
                <li><router-link to="/dashboard">Dashboard</router-link></li>
                <li><router-link to="/user-management">User Management</router-link></li>
                <li><router-link to="/settings">Settings</router-link></li>
            </ul>
        </aside>

        <main>
            <router-view />
        </main>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRouter } from "vue-router";

export default defineComponent({
    name: "MainLayout",
    setup() {
        const router = useRouter();

        const handleLogout = () => {
            localStorage.removeItem("isAuthenticated"); // 清除登录状态
            router.push("/login"); // 跳转到登录页
        };

        return {
            handleLogout,
        };
    },
});
</script>

<style scoped>
.main-layout {
    display: flex;
    flex-direction: column;
    height: 100vh;
}

header {
    background-color: #333;
    color: white;
    padding: 1rem;
    text-align: center;
}

aside {
    width: 200px;
    background-color: #f4f4f4;
    padding: 1rem;
}

main {
    flex: 1;
    padding: 1rem;
}

nav a {
    color: white;
    margin: 0 10px;
    text-decoration: none;
}

aside ul {
    list-style: none;
    padding: 0;
}

aside li {
    margin: 10px 0;
}

aside a {
    text-decoration: none;
    color: #333;
}
</style>
```

### 创建页面组件

#### Dashboard.vue

```vue
<template>
    <div>
        <h2>Dashboard</h2>
        <p>Welcome to the Dashboard!</p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "Dashboard",
});
</script>

```

#### Login.vue

```vue
<template>
    <div class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
            <div>
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required />
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";

export default defineComponent({
    name: "Login",
    setup() {
        const username = ref("");
        const password = ref("");
        const router = useRouter();

        const handleLogin = () => {
            // 模拟登录逻辑
            if (username.value === "admin" && password.value === "123456") {
                localStorage.setItem("isAuthenticated", "true"); // 存储登录状态
                router.push("/dashboard"); // 跳转到后台首页
            } else {
                alert("Invalid username or password");
            }
        };

        return {
            username,
            password,
            handleLogin,
        };
    },
});
</script>

<style scoped>
.login-container {
    max-width: 400px;
    margin: 100px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    text-align: center;
}

form div {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
}

button {
    padding: 10px 20px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background-color: #369f6e;
}
</style>
```

#### Settings.vue

```vue
<!-- src/views/Settings.vue -->
<template>
    <div>
        <h2>Settings</h2>
        <p>Configure system settings here.</p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "Settings",
});
</script>
```


#### UserManagement.vue

```vue
<!-- src/views/UserManagement.vue -->
<template>
    <div>
        <h2>User Management</h2>
        <p>Manage users here.</p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "UserManagement",
});
</script>
```

###  配置路由
```ts
// src/router/index.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import MainLayout from "@/layouts/MainLayout.vue";
import Dashboard from "@/views/Dashboard.vue";
import UserManagement from "@/views/UserManagement.vue";
import Settings from "@/views/Settings.vue";
import Login from "@/views/Login.vue";

const routes: Array<RouteRecordRaw> = [
    {
        path: "/login",
        component: Login,
    },
    {
        path: "/",
        component: MainLayout,
        meta: { requiresAuth: true }, // 需要登录才能访问
        children: [
            {
                path: "dashboard",
                component: Dashboard,
            },
            {
                path: "user-management",
                component: UserManagement,
            },
            {
                path: "settings",
                component: Settings,
            },
            {
                path: "", // 默认重定向到 Dashboard
                redirect: "/dashboard",
            },
        ],
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
    // 刷新时，滚动条位置还原
    scrollBehavior: () => ({ left: 0, top: 0 }),
});

// 路由守卫：检查用户是否已登录
router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";

    if (to.meta.requiresAuth && !isAuthenticated) {
        next("/login"); // 如果未登录，跳转到登录页
    } else {
        next(); // 否则继续导航
    }
});

export default router;
```

### 修改 App.vue
```vue
<template>
    <router-view />
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "App",
});
</script>

```

### 修改 main.ts
```ts
import { createApp } from 'vue';

import App from '@/App.vue';
import router from '@/router';

const app = createApp(App);

app.use(router);

app.mount('#app');
```

--------------------------------- 分割线 ---------------------------------

## 动态路由

<!-- TODO -->

--------------------------------- 分割线 ---------------------------------

## 按钮权限

<!-- TODO -->

--------------------------------- 分割线 ---------------------------------

## 国际化

### 安装 vue-i18n 依赖
```shell
yarn add vue-i18n
```

### Element Plus 国际化

#### 更改 App.vue
```vue
<template>
    <el-config-provider :locale="appStore.locale">
        <router-view />
    </el-config-provider>
</template>

<script lang="ts" setup>
import { ElConfigProvider } from "element-plus";
import { useStoreApp } from "@/store";
const appStore = useStoreApp();
</script>
```

#### 新建 `src/store/app.ts`
```ts
// src/store/app.ts
import { computed } from 'vue';
import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";
import { useI18n } from 'vue-i18n';

import { defaultSettings } from "@/config"; // 自定定制默认配置文件

// 导入 Element Plus 中英文语言包
import zhCn from "element-plus/es/locale/lang/zh-cn";
import en from "element-plus/es/locale/lang/en";

// setup
export default defineStore("app", () => {
    const { locale: i18nLocale } = useI18n();

    // 默认 zh-cn
    const language = useStorage("language", defaultSettings.language);

    /**
     * 根据语言标识读取对应的语言包
     */
    const locale = computed(() => {
        if (language?.value == "en") {
            return en;
        } else {
            return zhCn;
        }
    });

    /**
     * 切换语言
     */
    function changeLanguage(val: string) {
        language.value = val;
        i18nLocale.value = val;
    }

    return {
        language,
        locale,
        changeLanguage,
    };
});
```

### 本地国际化

#### 新建 locales 相关文件

```json
// src/locales/en.json
{
    "message": {
        "hello": "Hello"
    }
}
```

```json
// src/locales/zh-cn.json
{
    "message": {
        "hello": "你好"
    }
}
```

```ts
// src/locales/index.ts
import { createI18n } from "vue-i18n";
import { useStorage } from "@vueuse/core";

import { defaultSettings } from "@/config";

import en from "@/locales/en.json";
import zhCN from "@/locales/zh-cn.json";

const language = useStorage("language", defaultSettings.language);

const i18n = createI18n({
    legacy: false, // 设置为 false 启用 Composition API 风格的 i18n
    locale: language.value, // 默认语言
    messages: {
        en,
        "zh-cn": zhCN,
    },
});

// 全局 $t 工具函数，在脚本中使用这个
export const t = (key: string, values?: Record<string, unknown>) => {
    return values ? i18n.global.t(key, values) : i18n.global.t(key);
};

export default i18n;
```

#### 更改 main.ts
```ts
// src/main.ts
import { createApp } from 'vue';
import i18n from "@/locales";

import App from '@/App.vue';

const app = createApp(App);

app.use(i18n );
// 将 t 函数挂载到全局属性
app.config.globalProperties.$t = i18n.global.t;

app.mount('#app');
```

#### 切换语言组件
```vue
<!-- src/components/LanguageSwitch.vue -->
<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useStoreApp } from "@/store";

const appStore = useStoreApp();
const { locale } = useI18n();

function handleLanguageChange(lang: string) {
    locale.value = lang;
    appStore.changeLanguage(lang);
    if (lang == "en") {
        ElMessage.success("Switch Language Successful!");
    } else {
        ElMessage.success("切换语言成功！");
    }
}
</script>

<template>
    <el-dropdown trigger="click" @command="handleLanguageChange">
        <div>
            <el-button size="small" circle style="background-color: transparent;">
                <template #icon>
                    <svg-icon name="language" style="color: white;" />
                </template>
            </el-button>
        </div>
        <template #dropdown>
            <el-dropdown-menu>
                <el-dropdown-item :disabled="appStore.language === 'zh-cn'" command="zh-cn">
                    中文
                </el-dropdown-item>
                <el-dropdown-item :disabled="appStore.language === 'en'" command="en">
                    English
                </el-dropdown-item>
            </el-dropdown-menu>
        </template>
    </el-dropdown>
</template>
```

#### 在模板中使用国际化
```vue
<div>{{ $t('message.hello') }}</div>
```

#### 在脚本中使用国际化
```ts
import { t } from '@/locales';

console.log(t('message.hello'))
```

--------------------------------- 分割线 ---------------------------------

## 暗黑模式

### Element Plus 暗黑模式变量
```ts
// src/main.ts
import 'element-plus/theme-chalk/dark/css-vars.css'
```

### 切换暗黑模式组件
```vue
<!-- src/components/ThemeSwtich.vue -->
<script setup lang="ts">
import { useDark, useToggle } from "@vueuse/core";

/**
 * 暗黑模式
 */
const isDark = useDark();
const toggleDark = () => useToggle(isDark);
</script>

<template>
    <el-switch
        v-model="isDark"
        @change="toggleDark"
        inline-prompt
        size="large"
        style="
            --el-switch-on-color: rgba(101, 117, 133, 0.16);
            --el-switch-off-color: rgba(142, 150, 170, 0.14);
        "
    >
        <template #active-action>
            <span class="switchCircle dark">
                <svg-icon name="moon" :width="12" />
            </span>
        </template>
        <template #inactive-action>
            <span class="switchCircle">
                <svg-icon name="sunny" style="color: black" />
            </span>
        </template>
    </el-switch>
</template>

<style scoped lang="scss">
:deep(.el-switch__core .el-switch__action) {
    background-color: transparent !important;
}
.switchCircle {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    overflow: hidden;
    background-color: white;
    &.dark {
        background-color: black;
    }
}
</style>
```

### 自定义组件 暗黑模式

1/ 新建 `src/styles/dark.scss`
```scss
$drakColor: #141414;

html.dark {
    background-color: $drakColor;
    color: white;
    /* 修改自定义元素的样式 */
    .body {
        background-color: $drakColor;
    }
    header {
        background-color: $drakColor;
        a {
            color: white;
        }
    }
}
```

2/ 在 `main.ts`的`Element Plus` 的样式之后导入它
```ts
import 'element-plus/theme-chalk/dark/css-vars.css'; // Element Plus 暗黑模式
import '@/styles/dark.scss'; // 自定义组件 暗黑模式样式
```

--------------------------------- 分割线 ---------------------------------

## wangEditor 富文本 封装

[官方文档](https://www.wangeditor.com/)

### 安装依赖
```shell
yarn add @wangeditor/editor @wangeditor/editor-for-vue
```

### wangEditor 组件封装
```vue
<!-- src/components/Editor.vue -->
<template>
    <div style="border: 1px solid #ccc">
        <!-- 工具栏 -->
        <Toolbar
            :editor="editorRef"
            :defaultConfig="toolbarConfig"
            style="border-bottom: 1px solid #ccc"
            :mode="mode"
        />
        <!-- 编辑器 -->
        <Editor
            :defaultConfig="editorConfig"
            v-model="defaultHtml"
            @onChange="handleChange"
            style="height: 500px; overflow-y: hidden"
            :mode="mode"
            @onCreated="handleCreated"
        />
    </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, ref, shallowRef } from 'vue';
import { useVModel } from '@vueuse/core';
import { Editor, Toolbar } from "@wangeditor/editor-for-vue";

// API 引用
// import { uploadFileApi } from "@/api/file";

const props = defineProps({
    modelValue: {
        type: [String],
        default: "",
    },
});

const emit = defineEmits(["update:modelValue"]);

const defaultHtml = useVModel(props, "modelValue", emit);

const editorRef = shallowRef(); // 编辑器实例，必须用 shallowRef
const mode = ref("default"); // 编辑器模式
const toolbarConfig = ref({}); // 工具条配置
// 编辑器配置
const editorConfig = ref({
    placeholder: "请输入内容...",
    MENU_CONF: {
        uploadImage: {
            // 自定义图片上传
            async customUpload(file: any, insertFn: any) {
                // TODO: 自定义上传图片
                // uploadFileApi(file).then(response => {
                //     const url = response.data.url;
                //     insertFn(url);
                // });
            },
        },
    },
});

const handleCreated = (editor: any) => {
    editorRef.value = editor; // 记录 editor 实例，重要！
};

function handleChange(editor: any) {
    emit("update:modelValue", editor.getHtml());
}

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
    const editor = editorRef.value;
    if (editor == null) return;
    editor.destroy();
});
</script>

<style src="@wangeditor/editor/dist/css/style.css"></style>
```

### 使用Editor
```vue
<script setup lang="ts">
import Editor from '@/components/Editor.vue';
const value = ref('初始内容');
</script>

<template>
    <div class="app-container">
        <editor v-model="value" style="height: 600px" />
    </div>
</template>
```

--------------------------------- 分割线 ---------------------------------

## Echarts 图表

[官方文档](https://echarts.apache.org/examples/zh/index.html)


### 安装依赖
```shell
yarn add echarts
```

### echarts 组件封装
```vue
<!-- src/components/echarts/index.vue -->
<template>
    <div :id="id" :class="className" :style="{ height, width }" />
</template>

<script setup lang="ts">
import { onMounted, type PropType } from 'vue';
import * as echarts from "echarts";
import type { EChartsOption } from 'echarts';

const props = defineProps({
    id: {
        type: String,
        default: "barChart",
    },
    className: {
        type: String,
        default: "",
    },
    width: {
        type: String,
        default: "200px",
        required: true,
    },
    height: {
        type: String,
        default: "200px",
        required: true,
    },
    options: {
        type: Object as PropType<EChartsOption>,
        default: {},
        required: true,
    },
});

onMounted(() => {
    // 图表初始化
    const chart = echarts.init(document.getElementById(props.id) as HTMLDivElement);
    chart.setOption(props.options);

    // 大小自适应
    window.addEventListener("resize", () => {
        chart.resize();
    });
});
</script>
```

```vue
<!-- src/components/echarts/BarChart.vue -->
<template>
    <el-card>
        <template #header> 线 + 柱混合图 </template>
        <Echarts id="barChart" width="600px" height="600px" :options="options" />
    </el-card>
</template>

<script setup lang="ts">
import * as echarts from "echarts";
import type { EChartsOption } from 'echarts';

import Echarts from "./index.vue";

const options: EChartsOption = {
    grid: {
        left: "2%",
        right: "2%",
        bottom: "10%",
        containLabel: true,
    },
    tooltip: {
        trigger: "axis",
        axisPointer: {
            type: "cross",
            crossStyle: {
                color: "#999",
            },
        },
    },
    legend: {
        left: "center",
        top: "bottom",
        data: ["收入", "毛利润", "收入增长率", "利润增长率"],
        textStyle: {
            color: "#999",
        },
    },
    xAxis: [
        {
            type: "category",
            data: ["浙江", "北京", "上海", "广东", "深圳"],
            axisPointer: {
                type: "shadow",
            },
        },
    ],
    yAxis: [
        {
            type: "value",
            min: 0,
            max: 10000,
            interval: 2000,
            axisLabel: {
                formatter: "{value} ",
            },
        },
        {
            type: "value",
            min: 0,
            max: 100,
            interval: 20,
            axisLabel: {
                formatter: "{value}%",
            },
        },
    ],
    series: [
        {
            name: "收入",
            type: "bar",
            data: [7000, 7100, 7200, 7300, 7400],
            barWidth: 20,
            itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: "#83bff6" },
                    { offset: 0.5, color: "#188df0" },
                    { offset: 1, color: "#188df0" },
                ]),
            },
        },
        {
            name: "毛利润",
            type: "bar",
            data: [8000, 8200, 8400, 8600, 8800],
            barWidth: 20,
            itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: "#25d73c" },
                    { offset: 0.5, color: "#1bc23d" },
                    { offset: 1, color: "#179e61" },
                ]),
            },
        },
        {
            name: "收入增长率",
            type: "line",
            yAxisIndex: 1,
            data: [60, 65, 70, 75, 80],
            itemStyle: {
                color: "#67C23A",
            },
        },
        {
            name: "利润增长率",
            type: "line",
            yAxisIndex: 1,
            data: [70, 75, 80, 85, 90],
            itemStyle: {
                color: "#409EFF",
            },
        },
    ],
};
</script>
```

### 使用
```vue
<template>
    <div>
        <BarChart />
    </div>
</template>
<script lang="ts" setup>
import BarChart from '@/components/echarts/BarChart.vue';
</script>
```

--------------------------------- 分割线 ---------------------------------

## 错误合集

### `src/main.ts`的`import 'virtual:svg-icons-register'; // 自动导入 SVG 图标`报`找不到模块“virtual:svg-icons-register”或其相应的类型声明`

> 解决方法：
> 修改`tsconfig.app.json`
```json
"compilerOptions": {
    "noUncheckedSideEffectImports": false,
},
```

### `src/main.ts`的`import store from '@/store';`报`找不到模块“@/store”或其相应的类型声明`

> 解决方法：
> 修改`src/main.ts`
```ts
import store from '@/store/index';
```
--------------------------------- 分割线 ---------------------------------
