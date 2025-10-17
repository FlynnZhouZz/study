# Uniapp 面试

## uniapp页面间通信

1. URL 传参
页面 A：通过 uni.navigateTo 跳转页面并传递参数。
页面 B：在 onLoad 生命周期中接收参数。

2. 全局变量
在 App.vue 中定义全局变量。
在其他页面中通过 getApp().globalData 访问全局变量。
```js
// App.vue：
<script>
export default {
  globalData: {
    userInfo: null
  },
  onLaunch() {
    // 初始化全局变量
    this.globalData.userInfo = { name: 'John', age: 25 };
  }
};
</script>
```
```js
const app = getApp();
console.log(app.globalData.userInfo); // 输出: { name: 'John', age: 25 }
```

## 3. 状态管理Vuex/Pinia