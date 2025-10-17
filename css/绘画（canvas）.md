
<canvas>是一个可以使用脚本 (通常为JavaScript) 来绘制图形的 HTML 元素。2D 图像渲染标准之一。

## 绘制图形
## 使用样式和颜色
## 绘制文本
## 使用图像
## 变形
## 合成和剪辑
## 基本动画
## 高级动画
## 像素处理
## 优化canvas


## 怎么解决canvas中获取跨域图片数据的问题？

当请求跨域图片数据，而未满足跨域请求资源的条件时。如果canvas使用未经跨域允许的图片的原始数据，这些是不可信的数据，可能会暴露页面的数据。

### 请求图片资源 - 同域

Request Headers带有cookie。图片数据是被canvas信任的。

### 请求图片资源 - 跨域
默认情况下，直接请求跨域图片。因为不符合跨域请求资源的条件，图片数据是不被canvas信任的。

为了解决图片跨域资源共享的问题，`<img>` 元素提供了支持的属性：`crossOrigin`，该属性一共有两个值可选：`anonymous` 和 `use-credentials`，下面列举了两者的使用场景，以及满足的条件。


| \ | anonymous | use-credentials |
| --- | --- | --- |
| 用途 | 匿名请求跨域图片资源，不会发送证书（比如cookie等） | 具名请求跨域图片资源，会携带证书数据 |
| Request Headers | origin | origin、cookie |
| Response headers | Access-Control-Allow-Origin | Access-Control-Allow-Origin、Access-Control-Allow-Credentials |
| 所需条件 |Access-Control-Allow-Origin 字段值需要包含请求域。  | Access-Control-Allow-Origin 字段值需要包含请求域，且不能为通配符 `*`。Access-Control-Allow-Credentials 字段值需要为 true，表明允许请求发送证书数据。 |

主要原因是：

* 如果使用跨域的资源画到canvas中，并且资源没有使用CORS去请求，canvas会被认为是被污染了, canvas可以正常展示，但是没办法使用toDataURL()或者toBlob()导出数据，见Allowing cross-origin use of images and canvas。 所以通过在img标签上设置crossorigin，启用CORS，属性值为anonymous，在CORS请求时不会发送认证信息,见HTML attribute: crossorigin。
* 在启用CORS请求跨域资源时，资源必须允许跨域，才能正常返回，最简单的方式设置响应头Access-Control-Allow-Origin
* 图片已经通过img标签加载过，浏览器默认会缓存下来，下次使用js方式再去请求，直接返回缓存的图片，如果缓存中的图片不是通过CORS 请求或者响应头中不存在Access-Control-Allow-Origin，都会导致报错。