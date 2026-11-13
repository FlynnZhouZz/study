# 设置本地使用https访问

在`vue.config.js`文件中更改`devServer`对应参数即可

```js
devServer: {
    // development server port 8000
    port: 8210,
    host: 'saas.com',
    https: true,
},
```
