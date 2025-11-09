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