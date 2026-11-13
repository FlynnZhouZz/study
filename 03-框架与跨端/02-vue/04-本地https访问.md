# Vue 本地开发启用 https

> 有些浏览器能力只在安全上下文里可用；本地用 http 调试时它们全部失效，看起来像代码写错了。

## 什么情况下非开 https 不可

浏览器把 `http://localhost` 视为安全上下文，但把 `http://saas.com`、`http://192.168.1.10` 视为不安全。以下 API 在非安全上下文里直接不可用或抛错：

| API | 现象 |
|---|---|
| `navigator.clipboard` | `undefined`，复制按钮静默失效 |
| `navigator.geolocation` | 回调直接 error，code 1 |
| `mediaDevices.getUserMedia` | 摄像头、麦克风 `permission denied` |
| `Service Worker` | 注册报错，PWA 无法调试 |
| `crypto.subtle` | `undefined`，加密库初始化失败 |
| 部分 Cookie 属性 | `Secure` 标记的 Cookie 不写入 |

另外有些场景本来就必须走 https：对接微信网页授权、OAuth 回调地址要求 https、后端接口强制 TLS。

## 开启方式

### Vue CLI（webpack）

在 `vue.config.js` 里改 `devServer`：

```js
devServer: {
    // development server port 8000
    port: 8210,
    host: 'saas.com',
    https: true,
},
```

`https: true` 会让 dev-server 用自签证书启动。浏览器第一次访问会提示「不安全」，点「继续前往」即可；接口请求若是 https 但证书自签，Node 侧可能报 `UNABLE_TO_VERIFY_LEAF_SIGNATURE`，需要设 `NODE_TLS_REJECT_UNAUTHORIZED=0`（仅本地）。

### Vite

```js
// vite.config.js
import basicSsl from '@vitejs/plugin-basic-ssl';

export default {
  server: {
    host: 'saas.com',
    port: 8210,
    https: true,          // 或用 basicSsl() 插件自动生成证书
  },
};
```

```bash
npm i -D @vitejs/plugin-basic-ssl
```

### 用受信任的证书（推荐）

`https: true` 的自签证书每次都会告警，而且某些 SDK（微信 JS-SDK、支付）只接受受信任证书。用 mkcert 生成一份本机信任的证书更省事：

```bash
brew install mkcert
mkcert -install                # 把根证书装进系统钥匙串
mkcert saas.com localhost 127.0.0.1
```

得到 `saas.com+2.pem` 与 `saas.com+2-key.pem` 后指给 dev-server：

```js
// vite.config.js
server: {
  https: {
    key: fs.readFileSync('./certs/saas.com+2-key.pem'),
    cert: fs.readFileSync('./certs/saas.com+2.pem'),
  },
}
```

## host 写域名，先改 hosts

`host: 'saas.com'` 这类配置依赖本机把域名解析到 127.0.0.1，否则 dev-server 起不来或访问不到：

```bash
# /etc/hosts
127.0.0.1  saas.com
```

改完 `sudo dscacheutil -flushcache`（macOS）或 `ipconfig /flushdns`（Windows）刷新 DNS 缓存。

用局域网 IP 给手机调试时反过来：`host: '0.0.0.0'` 监听所有网卡，手机访问 `https://192.168.x.x:8210`，此时证书的 SAN 必须包含这个 IP（mkcert 时一并生成）。

## 为什么 host 不能乱写

dev-server 的 `allowedHosts`（Vite 5+ 默认只允许 localhost 和 IP）会拦截陌生 Host 头，出现：

```
Blocked request. This host ("saas.com") is not allowed.
```

解法是把它加进白名单：

```js
server: {
  host: 'saas.com',
  allowedHosts: ['saas.com', '.saas.com'],
}
```

这也是「配置了 https 却打不开页面」的常见原因——不是证书问题，是 Host 校验。

## 常见误区

**很多人以为 https 只影响页面本身**。页面是 https 时，它发出的 http 请求会被当作混合内容（mixed content）拦掉，所以后端接口、图片、WebSocket 都得跟着上 https，或者至少走同域代理。

**很多人以为 `https: true` 就够微信授权用了**。微信要求的是受信任证书 + 备案域名，自签证书会被拒，必须用 mkcert 或真实证书。

**很多人以为 dev-server 的 https 会影响构建产物**。它只作用于本地开发服务器，生产环境的 TLS 由 Nginx/网关终结，和这份配置无关。

## 关联阅读

- [Vue 解决跨域请求](./01-vue解决跨域请求.md)
- [基于 vue3 搭建后台管理系统](./05-基于vue3搭建后台管理系统.md)
- [03-框架与跨端 索引](../README.md)
