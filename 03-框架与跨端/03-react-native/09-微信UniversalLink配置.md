# 微信开放平台配置Universal Link

## 准备工作
- 拥有一个 HTTPS 域名（带有有效 SSL 证书）
- 可以在该域名下部署 .well-known/apple-app-site-association 文件
- 已开通 Apple Developer 账号，并已在 Xcode 中配置好 Associated Domains

## 部署 apple-app-site-association 文件
```json
{
  "applinks": {
    "apps": [],
    "details": [
      {
        "appID": "你的TeamID.你的BundleID",
        "paths": ["*"]
      }
    ]
  }
}
```
TeamID 可在 Apple Developer → Membership 页面查看
BundleID: com.xin.yun

**上传路径固定**
```
https://yourdomain.com/.well-known/apple-app-site-association
```
> 不能带 .json 后缀
> MIME 类型必须是 application/json
> 文件内容必须是无 BOM 的纯 JSON

## 配置微信开放平台 Universal Link

1. 打开微信开放平台：https://open.weixin.qq.com
2. 登录后进入你的 App → 「移动应用」→ 「应用详情」
3. 找到「Universal Link 配置」，点击「配置」
4. 填入你已部署 .well-known/apple-app-site-association 文件的基础路径，如：
```
https://yourdomain.com/app/
// 注意末尾必须有 尾部 /。微信只识别一级目录以下的路径（不能只写根路径）。
```

## 在 iOS 项目中配置
在 Signing & Capabilities 中添加 Associated Domains
```
applinks:yourdomain.com
```
不要写 https://，不要写路径。 


在代码中注册 App：
```js
WeChat.registerApp('yourAppId', 'https://yourdomain.com/app/');
```

## 验证是否配置成功
在 Safari 中访问：
https://yourdomain.com/.well-known/apple-app-site-association
应直接返回 JSON，不跳转，不报错

用 Apple 官方验证工具：
https://branch.io/resources/aasa-validator/