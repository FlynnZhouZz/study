# vue 解决跨域请求

在`vue.config.js`文件中的`devServer`配置请求代理

```js
devServer: {
    proxy: {
        '/uplod': {
            target: 'https://saas_api.com', // 请求的域名
            changeOrigin: true, // 是否改变请求源
            pathRewrite: {
                '^/uplod': '', // 重写 /uplod
            },
        },
    },
},
```

在`axios`中请求
```js
import axios from 'axios'

// 获取资源blob
export function getAssetsBlob(url) {
    return axios({
        url,
        method: 'get',
        responseType: 'blob',
        // baseURL: '/uplod',
    })
}

// 其它地方调用 示例
getAssetsBlob('/uplod/uploads/20240904/123.png');
```
