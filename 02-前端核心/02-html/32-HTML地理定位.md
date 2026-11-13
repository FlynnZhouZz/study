# HTML5 Geolocation（地理定位）

HTML5 Geolocation API 用于获得用户的地理位置。

```html
<button id="btn">获取位置</button>
<p id="out"></p>

<script>
    btn.onclick = () => {
        navigator.geolocation.getCurrentPosition(
            pos => {
                out.textContent = `纬度：${pos.coords.latitude}, 经度：${pos.coords.longitude}`;
            },
            err => {
                out.textContent = `定位失败：${err.message}`;
            }
        );
    };
</script>
```

## 详解

### 1. `navigator.geolocation`

浏览器提供的全局对象，用来做定位。 <br>
这是整个 API 的入口。

### 2. `getCurrentPosition()`：获取一次当前坐标

-   调用后浏览器会自动弹“是否允许访问位置”的权限框
-   用户点击“允许”后，会调用你传入的 successCallback
-   成功回调参数 pos 包含坐标

### 3. 从返回的数据中取经纬度

pos对象：
```json
{
  "coords": {
    "latitude": 35.689487,
    "longitude": 139.691711,
    "accuracy": 25,
    "altitude": null,
    "altitudeAccuracy": null,
    "heading": null,
    "speed": null
  },
  "timestamp": 1732310425123
}
```

- coords.latitude：纬度
- coords.longitude：经度
- coords.accuracy：经纬度误差（米）
- coords.altitude：海拔（可能为 null）
- coords.altitudeAccuracy：海拔误差（米）
- coords.heading：方向（度数）
- coords.speed：速度（米/秒）
- timestamp：时间戳（毫秒）

## 注意事项

### 1. 网页必须 https 或 localhost

否则浏览器会拒绝定位

### 2. 用户必须点击操作才能触发

比如按钮点击，否则有的浏览器会拦截。

### 3. 用户可能拒绝授权

可以加一个错误回调。
