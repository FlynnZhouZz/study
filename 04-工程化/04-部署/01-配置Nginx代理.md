# Nginx 反向代理解决跨域

> 跨域是浏览器的同源策略在拦，代理让请求从「浏览器发往另一个域」变成「服务器发往另一个域」，浏览器那一关根本没走到。

## 为什么代理能解决跨域

同源策略只在浏览器里执行：页面在 `https://web.example.com`，请求 `https://api.example.com` 就是跨域，响应头没有 `Access-Control-Allow-Origin` 就被拦。而 Nginx 转发这条请求时，发起方是服务器进程，不存在同源概念。

于是让前端只请求同域路径 `/api/xxx`，Nginx 在服务端转给真实后端，浏览器看到的始终是同一个域。

比 CORS 头更彻底的地方：**不需要后端配合加响应头，也不需要处理预检（OPTIONS）**，老接口、第三方接口都能代理。

## 配置

```nginx
server {
    # ... 其他配置 ...

    # 前端静态资源 / history 路由兜底
    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass https://api.upay7777.com/api/;
    }
    location /adm/ {
        proxy_pass https://api.upay7777.com/adm/;
    }
}
```

## proxy_pass 结尾那个斜杠，是全篇最容易错的地方

`proxy_pass` 后面**有没有 URI 部分**，决定了路径怎么拼：

| 写法 | 请求 `/api/user` 实际转发到 |
|---|---|
| `proxy_pass https://host;` | `https://host/api/user` — 原样带过去 |
| `proxy_pass https://host/;` | `https://host/user` — 把 `location` 匹配到的 `/api/` 替换成 `/` |
| `proxy_pass https://host/api/;` | `https://host/api/user` — 替换成 `/api/`，结果与第一种相同但含义不同 |

口诀：**proxy_pass 一旦带了路径，location 匹配到的前缀就被它替换**。所以 `location /api/` 配 `proxy_pass https://host/` 会把 `/api` 吃掉，后端收到 `/user` 而不是 `/api/user`，表现就是 404。

第二种写法（转发到根）在 `location /api/` 下更常见，因为它能把前端前缀整段剥掉：

```nginx
location /api/ {
    proxy_pass https://api.upay7777.com/;   # /api/user -> /user
}
```

## 补上这几个头，否则后端会拿到错的来源

默认情况下 Nginx 转发时 `Host` 头会变成上游域名，后端拿不到客户端真实 IP，也无法判断来源。一组通用配置：

```nginx
location /api/ {
    proxy_pass https://api.upay7777.com/api/;

    proxy_set_header Host              $host;
    proxy_set_header X-Real-IP         $remote_addr;
    proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

`X-Forwarded-For` 会累加，后端取第一个非信任 IP 才是客户端真实地址。`Host` 传 `$host` 而不是写死上游域名，是为了让后端生成的重定向、Cookie domain 仍指向用户访问的域名。

## 这三个坑，配完才想起来

**Cookie 丢失**：后端 `Set-Cookie` 带了 `Domain=api.upay7777.com`，浏览器在 `web.example.com` 下不会保存。要么后端去掉 Domain（默认就是当前域），要么代理时改写：

```nginx
proxy_cookie_domain api.upay7777.com web.example.com;
```

**WebSocket 连不上**：`ws://` 升级需要显式透传 upgrade 头，否则握手失败，表现为连接 1 秒后断开：

```nginx
location /ws/ {
    proxy_pass http://127.0.0.1:7001/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade    $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 600s;    # 默认 60s，长连接会被掐断
}
```

**SSE / 流式响应被缓冲**：`proxy_buffering` 默认开，Nginx 会攒够一个 buffer 才下发，前端看到的就是「一次性吐出全部」而不是逐字输出。关掉它：

```nginx
location /stream/ {
    proxy_pass http://127.0.0.1:7001/;
    proxy_buffering off;
    proxy_cache off;
}
```

## 常见误区

**很多人以为代理之后就完全没有跨域问题了**。如果前端在代码里把 `baseURL` 写死成 `https://api.example.com`，请求根本不经过 Nginx，代理配了也没用。必须让请求走相对路径。

**很多人以为 `add_header` 可以随便加在 `location` 里**。`add_header` 有继承覆盖规则：子级一旦出现 `add_header`，父级的所有 `add_header` 全部失效。要加 CORS 头时得把需要的头在同一个层级写全。

**很多人以为改完 reload 就生效**。`nginx -t` 必须先过语法检查，再 `nginx -s reload`；配置语法错时 reload 会失败但旧进程继续按老配置跑，看起来「没生效」，实际是没重载成功。

## 验证方式

```bash
# 直接从服务器验证转发是否通
curl -I https://web.example.com/api/health

# 看真实转发目标（把响应头带出来）
curl -v https://web.example.com/api/user 2>&1 | grep -E "< HTTP|< location"

# 确认 Nginx 配置语法
nginx -t && nginx -s reload
```

## 关联阅读

- [刷新非首页报 404](./02-刷新非首页报404.md)
- [04-工程化 索引](../README.md)
