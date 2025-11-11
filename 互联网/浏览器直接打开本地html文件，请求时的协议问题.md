# 浏览器直接打开本地html文件，请求时的协议问题

当你在本地直接打开HTML文件（file://协议）时，浏览器处于安全限制不会发送Cookie。

## 解决方案

使用 Node.js http-server

```bash
# 全局安装
npm install -g http-server

# 在项目目录 运行
http-server -p 8000
```

## 其他注意事项

1/ 使用`featch`请求，需配置`credentials: 'include',`，如：
```js
fetch(`${host}/api/index/login`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(generateSignPayload({
        username: username,
        password: password,
        code: code
    }))
})
```

2/ http-server服务打开，需使用请求域名访问页面，保证同源策略。
> 如你接口请求的域名是`http://example.com`，那么你访问页面的路径应该也是`http://example.com/index.html`
> 如何设置访问域名和接口请求域名相同呢？1. 确保接口请求服务是在本地。2. 修改本地host文件，127.0.0.1 -> example.com

3/ 如何检测请求是否携带Cookie
> 查看Headers中的Request Headers中是否有Cookie字段