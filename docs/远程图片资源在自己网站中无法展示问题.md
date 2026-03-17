# 远程图片资源在自己网站中无法展示问题

当远程图片资源（如阿里云oss服务）设置了防盗链，自己网站直接展示图片资源会加载错误。浏览器请求图片资源，会返回403 http状态。

## 解决方法

### 1、在全局HTML中设置Referrer Policy

在React项目的`public/index.html`文件的`<head>`标签内，添加以下`<meta>`标签：
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- 添加这行代码来解决图片403防盗链问题 -->
    <meta name="referrer" content="no-referrer" />
  </head>
  <body></body>
</html>
```

### 2、仅为特定图片设置referrerPolicy属性

在`<img>`标签上使用`referrerPolicy`属性。注意在React中，这个属性是驼峰式（camelCase）命名的 `referrerPolicy`，而不是全小写:
```js
function MyComponent() {
  return (
    <div>
      <h1>我的页面</h1>
      {/* 对于其他图片，正常加载，会发送Referer */}
      <img src="https://my-own-server.com/image.jpg" alt="My Image" />
      
      {/* 对于阿里云这个会报403的图片，设置不发送Referer */}
      <img 
        src="https://cbu01.alicdn.com/img/ibank/O1CN01AfYQDh21P41Rfmg4g_!!2214286236976-0-cib.jpg" 
        alt="Product Image"
        referrerPolicy="no-referrer" 
      />
    </div>
  );
}
```