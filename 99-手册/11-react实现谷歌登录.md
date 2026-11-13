# react实现谷歌登录

## 申请谷歌项目

省略

## 谷歌 Authentication 配置

路径： 谷歌项目 - Authentication

### 登录方法

添加Google登录方法

### 设置 - 已获授权的网域

添加域名：
- localhost
- 127.0.0.1
- example.local
- example.product

> 视情况而定，如果本地开发使用localhost或127.0.0.1需对应配置，如果使用虚拟域名，也是一样的。

## 谷歌 开发者账号 配置

[Google Cloud Console](https://console.cloud.google.com)，登录

导航菜单 - API和服务 - 凭证 - OAuth2.0 客户端ID - Web Client

### 配置 已获授权的 JavaScript 来源

- http://localhost
- http://127.0.0.1
- https://localhost
- https://127.0.0.1
- http://example.local
- http://example.product
- https://example.local
- https://example.product

> 同上，视情况配置

### 配置 已获授权的重定向 URI

- https://localhost:5173/__/auth/handler
- http://localhost:5173/__/auth/handler
- https://localhost:5173
- http://localhost:5173

> 同上，视情况配置

## React + Vite 配置

## 配置 本地ssl证书

生成本地ssl证书（MacOS）：
```bash
# 有，跳过
brew install mkcert

# 在项目根目录下执行

# 安装本地CA
mkcert -install

# 为localhost生成证书
mkcert localhost 127.0.0.1 ::1
```

### 配置 vite.config.ts

```js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import fs from 'fs';
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        host: true, // 监听所有地址
        port: 5173, // Vite默认端口，可修改
        strictPort: true, // 如果端口被占用，尝试其他端口
        https: {
            key: fs.readFileSync(path.resolve(__dirname, 'localhost+2-key.pem')),
            cert: fs.readFileSync(path.resolve(__dirname, 'localhost+2.pem')),
        },
        headers: {
            'Service-Worker-Allowed': '/',
        },
        // 代理配置（如果需要）
        // proxy: {
        //     '/api': {
        //         target: 'http://localhost:3000',
        //         changeOrigin: true,
        //     },
        // },
        proxy: {
            '/__/auth/': {
                target: 'https://your-project-id.firebaseapp.com',
                changeOrigin: true,
                secure: false, // 允许自签名证书
                ws: true,
                configure: (proxy) => {
                    proxy.on('error', (err) => {
                        console.log('Firebase auth proxy error:', err);
                    });
                },
            },
        },
    },

    resolve: {
        alias: {
            '@': '/src',
        },
    },
});

```

## 谷歌登录

```js
const PROD_AUTH_DOMAIN = '';
const firebaseAuthDomain = import.meta.env.DEV ? `${window.location.hostname}:5173` : PROD_AUTH_DOMAIN;

export const firebaseConfig = {
    apiKey: '',
    authDomain: firebaseAuthDomain,
    projectId: '',
    storageBucket: '',
    messagingSenderId: '',
    appId: '',
    measurementId: '',
};
```

```tsx
// App.tsx
export const app = initializeApp(firebaseConfig);
```

```tsx
// 关键代码
const handleContinueGoogle = useCallback(async () => {
    setIsLoading(true);
    try {
        const auth = getAuth();
        const provider = new GoogleAuthProvider();
        provider.addScope('email');
        provider.addScope('profile');

        // Web 端使用 signInWithPopup
        const result = await signInWithPopup(auth, provider);
        console.log('result', result);

        // const credential = GoogleAuthProvider.credentialFromResult(result);
        // const token = credential.accessToken;

        if (result.user) {
            const user = result.user;
            const userId = user.uid;
            const email = user.email || '';
            // TODO 待确认方案是否可行
            const isRegister = (result as any).additionalUserInfo?.isNewUser || false;

            // 持久化存储
            await Storage.set(storageKeys.userId, userId);
            await Storage.set(storageKeys.userEmail, email);
            await Storage.set(storageKeys.userInfo, user);
            await Storage.set(storageKeys.userToken, 'true');

            if (userInfo) {
                reportUserInfo(userId, { email }, userInfo).catch(() => {});
            }
            reportUserContactService(userId, { email }, false).catch(
                () => {},
            );

            setIsLoggedIn(true);
            const routePath = isRegister ? '/login-result' : '/';
            // 使用 replace 导航到首页，避免在历史中保留登录页
            navigate(routePath, { replace: true });
            if (!isRegister) {
                // 额外替换当前历史状态，减少因返回导致的老页面残留问题
                safeReplaceHistoryState({ loggedIn: true }, '', '/');
            }
        }
    } catch (error: any) {
        console.error('Google login failed:', error);
        toastError(error.message || 'Failed to sign in with Google.');
    } finally {
        setIsLoading(false);
    }
}, [navigate, setIsLoggedIn, userInfo]);
```