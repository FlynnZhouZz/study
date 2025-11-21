## 你有多少 RN 开发经验？做过哪些项目？

我大约有两年的RN开发经验，期间参与了专享app项目的开发，我自己也有一个用RN开发的app，是自己使用的。我熟悉RN的核心概念，如组件、状态管理、导航等，并能够熟练的使用Redux状态管理工具。

专享app，我主要负责开发客户管理及客户资料、新闻、直播等功能。

### RN集成直播

使用的是腾讯云的直播SDK。

#### 配置ios项目
使用 CocoaPods 安装腾讯云直播 SDK：
```bash
pod 'TXLiteAVSDK_Professional', '~> 版本号'

# 安装依赖
pod install
```

使用 Xcode 创建一个原生模块（如 TencentLiveModule），封装腾讯云直播 SDK 的功能。

在 TencentLiveModule.m 中实现推流、拉流等方法，并通过 RCT_EXPORT_METHOD 暴露给 RN。

在 React Native 项目中，通过 NativeModules 调用原生模块。

#### 配置android想
将腾讯云直播SDK的android版本.arr添加到android/app/libs目录中
在AndroidMainfest.xml中添加相机和麦克风权限
在build.gradle中添加依赖
```java
implementation fileTree(dir: 'libs', include: ['*.aar'])
```
在 android/app/src/main/java/com/yourapp 目录下创建原生模块（如 TencentLiveModule.java）。

使用 @ReactMethod 注解暴露推流、拉流等方法。

在 MainApplication.java 中注册模块：


#### 处理UI渲染

腾讯云直播 SDK 提供了原生的 UIView 或 SurfaceView 用于渲染视频流。你需要在原生模块中创建自定义视图，并通过 requireNativeComponent 将其暴露给 RN。

```objective-c
// TencentLiveViewManager.m
#import <React/RCTViewManager.h>
#import <TXLiteAVSDK_Professional/TXLiteAVSDK.h>

@interface TencentLiveViewManager : RCTViewManager
@end

@implementation TencentLiveViewManager

RCT_EXPORT_MODULE(TencentLiveView)

- (UIView *)view {
  return [[UIView alloc] init];
}

@end
```

```java
// TencentLiveViewManager.java
package com.yourapp;

import com.facebook.react.uimanager.SimpleViewManager;
import com.facebook.react.uimanager.ThemedReactContext;
import com.tencent.rtmp.ui.TXCloudVideoView;

public class TencentLiveViewManager extends SimpleViewManager<TXCloudVideoView> {
    @Override
    public String getName() {
        return "TencentLiveView";
    }

    @Override
    protected TXCloudVideoView createViewInstance(ThemedReactContext reactContext) {
        return new TXCloudVideoView(reactContext);
    }
}
```

<!-- RN 中使用 -->
```js
import { requireNativeComponent } from 'react-native';

const TencentLiveView = requireNativeComponent('TencentLiveView');

const LiveView = () => {
  return <TencentLiveView style={{ flex: 1 }} />;
};
```

### RN实现查看pdf

使用三方库：react-native-pdf/react-native-view-pdf

文件权限：如果加载本地文件，确保在 Android 和 iOS 上正确配置文件权限。

性能优化：对于大文件，注意内存管理和加载性能。
> 分块加载，axios分开下载文件
> react-native-pdf支持流式渲染
> 缓存，使用react-native-fs将文件缓存到本地
> 性能优化：避免内存泄漏、优化图片资源

错误处理：处理网络错误或文件加载失败的情况。

## RN 和 React 在架构上的主要区别？

React：

使用 虚拟 DOM 来优化 Web 应用的渲染性能。

通过 ReactDOM.render() 将组件渲染到浏览器的 DOM 中。

直接操作浏览器的 DOM API。

React Native：

使用 原生组件 而不是 DOM。

通过 React Native 的桥接机制将 JavaScript 组件映射到原生组件（如 View → UIView 或 android.view.View）。

不直接操作 DOM，而是通过原生 API 更新 UI。

## 如何在 RN 中管理状态？你倾向于使用 Redux、MobX 还是 Context API？

**Redux**
优点：
单一数据源：整个应用的状态存储在一个全局的 Store 中，易于调试和管理。

可预测性：通过纯函数（Reducer）更新状态，确保状态变化可预测。

强大的中间件支持：支持异步操作（如 redux-thunk、redux-saga）。

丰富的生态系统：有大量的插件和工具（如 Redux DevTools）。

缺点：
样板代码多：需要编写大量的 Action、Reducer 和 Store 配置代码。

学习曲线陡峭：对于初学者来说，理解 Redux 的概念和工作流程可能需要一些时间。

适用场景：
大型应用，需要复杂的状态管理。

需要强大的调试工具和中间件支持。

**MobX**
优点：
简洁易用：代码量少，学习曲线较低。

自动更新：通过 observable 和 observer 自动管理状态更新。

高性能：只更新依赖变化的组件，减少不必要的渲染。

缺点：
隐式依赖：状态的依赖关系是隐式的，可能导致调试困难。

生态系统较小：相比 Redux，插件和工具较少。

适用场景：
中小型应用，需要快速开发。

需要简洁的状态管理方案。

**Context API**
优点：
无需额外依赖：内置在 React 中，无需安装第三方库。

简单易用：适合小型应用或局部状态管理。

灵活性高：可以结合 useReducer 实现类似 Redux 的功能。

缺点：
性能问题：当状态变化频繁时，可能导致不必要的渲染。

不适合复杂场景：对于大型应用，管理多个 Context 可能变得复杂。

适用场景：
小型应用或局部状态管理。

需要快速实现状态共享。

**Recoil**：Facebook 推出的状态管理库，适合复杂的状态管理场景。

## 使用过哪些第三方库来处理网络请求、导航、状态管理等？

网络请求：axios、fetch
导航： React Navigation、React Native Navigation 
状态管理：redux、Mobx、context api

## axios原理

axios 是一个基于 Promise 的 HTTP 客户端，广泛用于浏览器和 Node.js 环境中。它的设计简洁、功能强大，支持请求和响应拦截、自动转换 JSON 数据、取消请求等特性。

### 核心设计
基于 Promise：所有请求都返回 Promise 对象，支持异步操作。

适配器模式：通过适配器（Adapter）支持浏览器和 Node.js 两种环境。

拦截器机制：支持请求和响应拦截，方便全局处理。

配置化：通过配置对象统一管理请求参数。

### 主要模块
axios 的源码结构清晰，主要包含以下模块：

（1）核心模块（Core）
Axios 类：核心类，封装了请求的逻辑。

请求配置：通过 config 对象管理请求参数（如 URL、方法、headers 等）。

请求发送：根据环境选择适配器发送请求。

（2）适配器（Adapter）
浏览器适配器：基于 XMLHttpRequest 实现。

Node.js 适配器：基于 http 或 https 模块实现。

（3）拦截器（Interceptors）
请求拦截器：在请求发送前对配置进行处理。

响应拦截器：在响应返回后对结果进行处理。

（4）取消请求（Cancel Token）
提供取消请求的机制，基于 CancelToken 实现。

### 工作原理
（1）创建请求配置
用户通过 axios(config) 或 axios.get(url, config) 等方式传入请求配置。

配置对象包括 url、method、headers、data 等参数。

（2）请求拦截器
在请求发送前，依次执行用户定义的请求拦截器。

拦截器可以对配置进行修改（如添加 token、修改 headers）。

（3）选择适配器
根据运行环境（浏览器或 Node.js）选择对应的适配器。

浏览器环境使用 XMLHttpRequest，Node.js 环境使用 http 或 https 模块。

（4）发送请求
适配器根据配置发送请求，并返回 Promise 对象。

在浏览器中，XMLHttpRequest 发送请求并监听 onload 和 onerror 事件。

在 Node.js 中，http 或 https 模块发送请求并监听 response 事件。

（5）响应拦截器
在响应返回后，依次执行用户定义的响应拦截器。

拦截器可以对响应数据进行处理（如格式化、错误处理）。

（6）返回结果
最终返回处理后的响应数据（如 JSON 数据）。

### 使用 CancelToken 实现请求取消。

## 如何减少 App 启动时间？

优化方向	具体措施
JavaScript 加载	代码拆分、预加载关键资源、减少 JavaScript 体积
原生启动	减少主线程负载、延迟加载非关键模块、优化原生代码
UI 渲染	减少初始渲染复杂度、使用占位符、优化图片加载
网络请求	缓存数据、预加载数据
打包和构建	移除未使用代码、优化 Metro 配置、使用 Hermes 引擎
监控和分析	使用性能监控工具、分析启动流程
其他优化	减少同步操作、优化字体加载、减少动画复杂度

## RN 如何进行动画优化？Animated 和 Reanimated 的区别？

1. Animated
Animated 是 React Native 内置的动画库，适用于大多数简单的动画场景。

特点：
基于 JavaScript：动画逻辑在 JavaScript 线程中执行。

简单易用：API 简单，适合实现基本的动画效果（如渐变、平移、缩放等）。

性能限制：由于动画在 JavaScript 线程中运行，复杂动画可能会导致性能问题（如卡顿、丢帧）。

优化建议：
启用原生驱动：通过 useNativeDriver: true 将动画逻辑转移到原生线程，提升性能。

避免复杂动画：对于复杂动画，考虑使用 Reanimated。

2. Reanimated
Reanimated 是一个高性能的动画库，专为解决 Animated 的性能问题而设计。

特点：
基于原生线程：动画逻辑在原生线程中执行，避免 JavaScript 线程的瓶颈。

高性能：适合实现复杂的动画效果（如手势驱动动画、物理动画等）。

灵活性强：提供更强大的 API，支持自定义动画逻辑。

优化建议：
使用 useSharedValue：将动画值存储在原生线程中，避免 JavaScript 线程的通信开销。

使用 withTiming 或 withSpring：实现平滑的动画效果。

结合手势库：使用 react-native-gesture-handler 实现手势驱动的动画。

## 如何进行离线存储？AsyncStorage 和 MMKV 有什么区别？

1. AsyncStorage
AsyncStorage 是 React Native 官方提供的轻量级、异步的键值对存储方案。

特点：
异步操作：所有操作都是异步的，避免阻塞主线程。

简单易用：API 简单，适合存储少量数据（如用户设置、令牌等）。

性能限制：不适合存储大量数据或频繁读写的场景。

无类型支持：存储的数据只能是字符串，需要手动序列化和反序列化。

2. MMKV
MMKV 是由微信团队开发的高性能键值对存储库，专为移动端优化。

特点：
高性能：基于内存映射文件（mmap）实现，读写速度极快。

同步/异步支持：支持同步和异步操作。

类型支持：支持多种数据类型（如字符串、数字、布尔值、对象等）。

大容量支持：适合存储大量数据。

跨平台：支持 iOS 和 Android。

1）SQLite
特点：

关系型数据库，适合存储结构化数据。

支持复杂的查询和事务操作。

适用场景：

需要存储结构化数据（如用户数据、订单数据）。

需要复杂查询和事务支持的场景。

推荐库：

react-native-sqlite-storage

watermelondb

## 如何实现推送通知（如 FCM、APNs）？

国外 安卓使用FCM，国内需要个推、极光推送或小米推送等

## 如何处理不同尺寸设备的 UI 适配？

1. 使用 Flexbox 布局
2. 使用百分比宽度和高度
3. 使用 Dimensions API
4. 使用 PixelRatio API
5. 使用 Platform API
6. 使用 react-native-responsive-screen 库
7. 使用 react-native-size-matters 库
8. 使用 SafeAreaView 适配刘海屏
9. 使用 useWindowDimensions Hook

## 你是否处理过深色模式（Dark Mode）

（1）使用 useColorScheme Hook
（2）使用 react-native-paper 或 react-navigation 的主题支持
（3）自定义主题管理: 通过 Context 或状态管理库（如 Redux）实现自定义主题切换。

## 无障碍（Accessibility）适配？

（1）无障碍属性
accessible：标记组件是否为无障碍元素。

accessibilityLabel：为组件提供描述性文本。

accessibilityRole：定义组件的角色（如按钮、文本等）。

accessibilityHint：提供额外的操作提示。

```js
import React from 'react';
import { View, Text, Button } from 'react-native';

const App = () => (
  <View>
    <Text
      accessible
      accessibilityLabel="Welcome text"
      accessibilityRole="text"
    >
      Welcome to the app!
    </Text>
    <Button
      title="Press Me"
      accessibilityLabel="Press this button to perform an action"
      accessibilityHint="Double tap to activate"
      onPress={() => alert('Button pressed')}
    />
  </View>
);

export default App;
```

（2）无障碍 API
AccessibilityInfo：用于检测屏幕阅读器状态。

setAccessibilityFocus：将焦点设置到指定组件。

```js
import React, { useEffect } from 'react';
import { View, Text, AccessibilityInfo } from 'react-native';

const App = () => {
  useEffect(() => {
    AccessibilityInfo.isScreenReaderEnabled().then((enabled) => {
      console.log('Screen reader enabled:', enabled);
    });
  }, []);

  return (
    <View>
      <Text accessible accessibilityLabel="Welcome text">
        Welcome to the app!
      </Text>
    </View>
  );
};

export default App;
```

（3）无障碍事件
onAccessibilityTap：当用户双击组件时触发。

onMagicTap：当用户双击屏幕时触发（iOS 专用）。

```js
import React from 'react';
import { View, Text } from 'react-native';

const App = () => (
  <View>
    <Text
      accessible
      accessibilityLabel="Double tap to greet"
      onAccessibilityTap={() => alert('Hello!')}
    >
      Double tap to greet
    </Text>
  </View>
);

export default App;
```

（4）无障碍测试工具
iOS VoiceOver：在 iOS 设备上测试无障碍功能。

Android TalkBack：在 Android 设备上测试无障碍功能。

React Native Debugger：检查无障碍属性和事件。

## 物流 App 可能需要定位功能，RN 如何处理高精度定位？如何在后台运行？

1. 高精度定位

（1）使用 react-native-geolocation-service
> react-native-geolocation-service 是一个第三方库，提供了更强大的定位功能，支持高精度定位。

（2）使用 react-native-maps
> 一个地图库，支持高精度定位和地图显示。

2. 后台运行

（1）使用 react-native-background-geolocation
> react-native-background-geolocation 是一个强大的库，支持在后台持续获取位置信息。

（2）使用 Headless JS（仅 Android）
> Headless JS 是 React Native 提供的一种机制，允许在后台运行 JavaScript 代码。


## RN 如何集成 Google Maps？

安装依赖`react-native-maps`

（2）配置 Google Maps API 密钥
在 Google Cloud Console 中创建项目并启用 Google Maps API。

获取 API 密钥。

Android 配置：
在 android/app/src/main/AndroidManifest.xml 中添加：
```xml
<meta-data
  android:name="com.google.android.geo.API_KEY"
  android:value="YOUR_GOOGLE_MAPS_API_KEY" />
```

iOS 配置：
在 ios/项目名称/AppDelegate.m 中添加：
```objective-c
#import <GoogleMaps/GoogleMaps.h>

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
  [GMSServices provideAPIKey:@"YOUR_GOOGLE_MAPS_API_KEY"];
  return YES;
}
```

## RN 如何集成 高德地图？

`react-native-amap3d`

（2）配置高德地图 API 密钥
在 高德开放平台 注册账号并创建应用。

获取 API 密钥。

Android 配置：
在 android/app/src/main/AndroidManifest.xml 中添加：
```xml
<meta-data
  android:name="com.amap.api.v2.apikey"
  android:value="YOUR_AMAP_API_KEY" />
```

iOS 配置：
在 ios/项目名称/AppDelegate.m 中添加：
```objective-c
#import <AMapFoundationKit/AMapFoundationKit.h>

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
  [AMapServices sharedServices].apiKey = @"YOUR_AMAP_API_KEY";
  return YES;
}
```

## 如何保证订单实时更新？使用 WebSocket 还是轮询？

1. WebSocket
WebSocket 是一种全双工通信协议，允许客户端和服务器之间建立持久连接，实现实时数据传输。

优点：
实时性高：数据可以立即从服务器推送到客户端。

效率高：避免了频繁的 HTTP 请求，减少了网络开销。

适合高频更新：适用于需要实时更新的场景（如订单状态、位置跟踪）。

缺点：
实现复杂：需要额外的服务器支持和客户端实现。

连接管理：需要处理连接断开和重连的逻辑。

服务器压力：大量并发连接可能增加服务器负载。

适用场景：
需要实时更新的场景（如订单状态、聊天、实时位置跟踪）。

2. 轮询（Polling）
轮询是通过客户端定期向服务器发送请求来获取最新数据的方式。

优点：
实现简单：只需定期发送 HTTP 请求。

兼容性好：适用于所有支持 HTTP 的环境。

服务器压力可控：可以通过调整轮询间隔控制请求频率。

缺点：
实时性差：数据更新有延迟，取决于轮询间隔。

效率低：频繁的 HTTP 请求增加了网络开销。

不适合高频更新：频繁轮询会增加服务器和客户端的负担。

适用场景：
数据更新频率较低的场景（如每日数据统计、定时任务）。

## 如何进行蓝牙打印（比如打印快递单）？

使用 react-native-ble-plx 库进行蓝牙通信。

2. 配置权限
Android
在 android/app/src/main/AndroidManifest.xml 中添加以下权限：
```xml
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

iOS
在 ios/项目名称/Info.plist 中添加以下权限：
```xml
<key>NSBluetoothAlwaysUsageDescription</key>
<string>我们需要访问蓝牙以连接打印机。</string>
<key>NSBluetoothPeripheralUsageDescription</key>
<string>我们需要访问蓝牙以连接打印机。</string>
```

3. 连接蓝牙打印机
（1）扫描蓝牙设备
（2）连接设备

4. 发送打印数据

（1）文本打印
将文本转换为打印机支持的格式（如 ESC/POS 指令）并发送。

（2）图片打印
将图片转换为打印机支持的格式（如位图）并发送。


## 如何处理离线任务（比如快递员断网后如何继续使用 App）？

1. 离线任务的核心需求
数据存储：在本地存储任务数据（如订单信息、快递单号）。

任务同步：在网络恢复后将本地数据同步到服务器。

用户体验：确保用户在网络中断时仍能正常使用 App。

2. 实现方案
（1）本地数据存储

SQLite：轻量级关系型数据库，适合存储结构化数据。

Realm：高性能对象存储数据库，支持离线同步。

AsyncStorage：简单的键值对存储，适合少量数据。


## 你如何组织 RN 项目的目录结构？

```
my-rn-app/
├── src/
│   ├── assets/               # 静态资源（图片、字体等）
│   ├── components/           # 通用组件
│   ├── config/               # 配置文件（如 API 地址、主题）
│   ├── constants/            # 常量（如路由名称、颜色）
│   ├── navigation/           # 导航配置
│   ├── views/              # 页面组件
│   ├── services/api/             # 服务层（如 API 请求、数据库）
│   ├── store/                # 状态管理（如 Redux、MobX）
│   ├── styles/                # 工具函数
│   ├── utils/                # 工具函数
│   ├── App.js                # 应用入口
│   └── index.js              # 项目入口
├── .eslintrc.js              # ESLint 配置
├── .prettierrc.js            # Prettier 配置
├── babel.config.js           # Babel 配置
├── metro.config.js           # Metro 配置
├── package.json              # 项目依赖
└── README.md                 # 项目说明
```

## 组件如何拆分，如何复用？

1. 组件拆分的原则
（1）单一职责原则
每个组件只负责一个功能或 UI 部分。例如，一个按钮组件只负责显示按钮和处理点击事件。

（2）高内聚低耦合
组件内部的逻辑和样式应紧密相关，而组件之间应尽量减少依赖。

（3）可复用性
将通用的 UI 部分提取为独立组件，以便在多个地方复用。

（4）可配置性
通过 props 使组件具有可配置性，适应不同的使用场景。

2. 组件的拆分方法
（1）按功能拆分
（2）按 UI 元素拆分
（3）按业务逻辑拆分

3. 组件的复用方法
（1）通过 props 实现复用
（2）通过 children 实现复用
（3）通过高阶组件（HOC）实现复用: 高阶组件是一个函数，接收一个组件并返回一个新的组件，用于复用逻辑。
（4）通过自定义 Hook 实现复用: 自定义 Hook 可以将逻辑提取到可复用的函数中。

## 使用了哪些设计模式？

（1）组件模式
容器组件与展示组件：

容器组件：负责逻辑处理和数据获取。

展示组件：负责 UI 渲染。

（2）高阶组件（HOC）
用途：复用组件逻辑。

（3）Render Props
用途：通过 props 传递渲染逻辑。

（4）Provider 模式
用途：通过 Context 共享全局状态。

## 有没有做过性能优化？

（1）减少重渲染
使用 React.memo：避免不必要的组件重渲染。
使用 useMemo 和 useCallback：缓存计算值和回调函数。

（2）优化列表渲染
使用 FlatList 或 SectionList：只渲染可见项，减少内存占用。

（3）图片优化
使用 react-native-fast-image：优化图片加载性能。

（4）减少 JavaScript 线程负载
启用 Hermes 引擎：提升 JavaScript 执行性能。

（5）优化动画
使用 useNativeDriver：将动画逻辑转移到原生线程。

（6）代码拆分和懒加载
使用 React.lazy 和 Suspense：按需加载组件。

（7）减少同步操作
避免在主线程执行耗时操作：如文件读写、数据库操作。

（8）使用性能监控工具
React Native Debugger：监控组件渲染性能。

Flipper：分析网络请求、日志和性能。

## RN 如何进行调试？用过哪些工具（如 Flipper、React DevTools）？

（1）React Native Debugger
功能：集成 Redux 调试、React DevTools 和 JavaScript 调试。

安装：

下载并安装 React Native Debugger。

使用：

在应用中启用调试模式（摇动设备或按 Ctrl+M）。

选择“Debug JS Remotely”。

打开 React Native Debugger，自动连接到应用。

4）Chrome 开发者工具
功能：调试 JavaScript 代码、查看网络请求、分析性能。

使用：

在应用中启用调试模式（摇动设备或按 Ctrl+M）。

选择“Debug JS Remotely”。

打开 Chrome 浏览器，访问 chrome://inspect，选择设备并点击“Inspect”。

（5）Xcode 和 Android Studio
功能：调试原生代码、查看日志、分析性能。

使用：

Xcode：打开项目，选择设备并运行，使用调试工具查看日志和性能。

Android Studio：打开项目，选择设备并运行，使用 Logcat 查看日志。

## RN 代码如何测试？使用过 Jest 或 Detox 吗？

1. 单元测试（Jest）
Jest 是 Facebook 开发的 JavaScript 测试框架，支持 React Native 的单元测试。

（1）安装 Jest
```shell
npm install --save-dev jest
```

（2）配置 Jest
在 package.json 中添加 Jest 配置：
```json
{
  "scripts": {
    "test": "jest"
  },
  "jest": {
    "preset": "react-native",
    "transformIgnorePatterns": [
      "node_modules/(?!(react-native|@react-native|react-native-vector-icons)/)"
    ]
  }
}
```

（3）编写单元测试
```js
// components/Button.js
import React from 'react';
import { TouchableOpacity, Text, StyleSheet } from 'react-native';

const Button = ({ title, onPress }) => (
  <TouchableOpacity style={styles.button} onPress={onPress}>
    <Text style={styles.text}>{title}</Text>
  </TouchableOpacity>
);

const styles = StyleSheet.create({
  button: {
    padding: 10,
    backgroundColor: 'blue',
    borderRadius: 5,
    alignItems: 'center',
  },
  text: {
    color: 'white',
    fontSize: 16,
  },
});

export default Button;
```

```js
// __tests__/Button.test.js
import React from 'react';
import { render } from '@testing-library/react-native';
import Button from '../components/Button';

test('Button renders correctly', () => {
  const { getByText } = render(<Button title="Submit" onPress={() => {}} />);
  expect(getByText('Submit')).toBeTruthy();
});
```

（4）运行测试
```shell
npm test
```

2. 端到端测试（Detox）
Detox 是一个用于 React Native 的端到端测试框架，模拟用户操作并验证应用行为。

（1）安装 Detox

```shell
npm install --save-dev detox
```

（2）配置 Detox
在 package.json 中添加 Detox 配置：
```json
{
  "scripts": {
    "test:e2e": "detox test"
  },
  "detox": {
    "configurations": {
      "ios.sim.debug": {
        "device": "iPhone 14",
        "app": "ios.debug"
      },
      "android.emu.debug": {
        "device": "Pixel_4_API_30",
        "app": "android.debug"
      }
    }
  }
}
```

在项目根目录创建 .detoxrc.json 文件：
```json
{
  "testRunner": "jest",
  "runnerConfig": "e2e/config.json",
  "configurations": {
    "ios.sim.debug": {
      "device": "iPhone 14",
      "app": "ios.debug"
    },
    "android.emu.debug": {
      "device": "Pixel_4_API_30",
      "app": "android.debug"
    }
  }
}
```

（3）编写端到端测试
```js
// e2e/firstTest.spec.js
describe('Example', () => {
  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should show welcome screen', async () => {
    await expect(element(by.text('Welcome'))).toBeVisible();
  });

  it('should show hello screen after tap', async () => {
    await element(by.id('hello_button')).tap();
    await expect(element(by.text('Hello!!!'))).toBeVisible();
  });
});
```

（4）运行端到端测试

```shell
detox build --configuration ios.sim.debug
detox test --configuration ios.sim.debug
```

```shell
detox build --configuration android.emu.debug
detox test --configuration android.emu.debug
```

## 如何抓取移动端网络请求并分析数据？

1. 使用 Flipper
2. 使用 React Native Debugger
3. 使用 Chrome 开发者工具
4. 使用 Charles Proxy
5. 使用 Wireshark

## RN App 如何打包并发布到 App Store 和 Google Play？

1. 发布到 App Store

（1）准备工作
- 注册 Apple Developer 账号：
    访问 Apple Developer 注册账号。

- 创建 App ID：
    在 Apple Developer 中创建唯一的 App ID。

- 创建证书和配置文件：
    生成开发证书和发布证书。
    创建 Provisioning Profile。

（2）配置 Xcode 项目
- 打开 ios/项目名称.xcworkspace。

- 设置 Bundle Identifier：
    在 General 选项卡中，设置 Bundle Identifier 为 App ID。

- 配置签名：
    在 Signing & Capabilities 选项卡中，选择 Team 并启用自动签名。

（3）打包应用
选择 Product -> Scheme -> Edit Scheme，将 Build Configuration 设置为 Release。

选择 Product -> Archive，生成 .xcarchive 文件。

（4）上传到 App Store Connect
打开 Xcode Organizer，选择生成的 .xcarchive 文件。

点击 Distribute App，选择 App Store Connect。

上传应用并填写元数据（如应用名称、描述、截图等）。

（5）提交审核
登录 App Store Connect。

选择应用，点击 Submit for Review。

等待 Apple 审核通过后，应用将发布到 App Store。

2. 发布到 Google Play

（1）准备工作
- 注册 Google Play Developer 账号：
    访问 Google Play Console 注册账号。

- 创建应用：
    在 Google Play Console 中创建应用并填写基本信息。


（2）配置 Android 项目
生成签名密钥：
```shell
keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
```

配置 android/app/build.gradle：
```java
android {
  ...
  signingConfigs {
    release {
      storeFile file('my-release-key.keystore')
      storePassword 'your_store_password'
      keyAlias 'your_key_alias'
      keyPassword 'your_key_password'
    }
  }
  buildTypes {
    release {
      ...
      signingConfig signingConfigs.release
    }
  }
}
```
（3）打包应用
生成 APK 文件：
```shell
cd android
./gradlew assembleRelease
```
生成的 APK 文件位于 android/app/build/outputs/apk/release/。

（4）上传到 Google Play Console
登录 Google Play Console。

选择应用，点击 Release -> Create New Release。

上传 APK 文件并填写元数据（如应用名称、描述、截图等）。

（5）提交审核
点击 Review Release，确认发布信息。

等待 Google 审核通过后，应用将发布到 Google Play。

## 如何做 CI/CD 以自动化构建和发布？

持续集成（CI）、持续交付（CD）

常用工具：
GitHub Actions

## OTA（Over-The-Air）更新如何实现？使用过 CodePush 吗？

OTA（Over-The-Air）更新是一种无需重新发布应用即可更新 JavaScript 代码和资源的机制。


## 你如何和后端/产品/UI 进行高效沟通？
1. 与后端沟通
（1）明确接口规范
（2）定期同步: 每日站会、技术讨论
（3）使用工具： postman

2. 与产品沟通
（1）理解需求
（2）参与需求评审
（3）反馈开发进度

3. 与 UI 设计师沟通
（1）理解设计稿
（2）确认交互细节
（3）反馈实现问题

4. 沟通工具
    面对面、OA

## 你如何学习和掌握新技术？最近关注的 RN 相关技术有哪些？

1. 学习和掌握新技术的方法

（1）明确学习目标
（2）系统学习
（3）实践项目
（4）总结
（5）持续学习

2. 最近关注的 React Native 相关技术
（1）React Native 新版本
React Native 0.70+：关注新版本的特性和改进，如 Hermes 引擎的优化、Fabric 渲染器的进展等。

2）状态管理
Recoil：探索 Recoil 在 React Native 中的应用，了解其与 Redux 的对比。
Zustand：学习 Zustand 的轻量级状态管理方案。

（3）性能优化
React Native Reanimated：深入研究 Reanimated 2，优化复杂动画性能。
Hermes 引擎：探索 Hermes 引擎的性能优势和使用场景。

（4）跨平台开发
React Native for Windows + macOS：关注 React Native 在桌面端的应用和发展。
Expo：学习 Expo 的最新功能，如 EAS（Expo Application Services）。

（5）测试和调试
Detox：深入研究 Detox 的端到端测试方案，提升测试覆盖率。
Flipper：探索 Flipper 的插件生态系统，优化调试体验。

（6）原生模块开发
TurboModules：学习 TurboModules 的实现原理，优化原生模块性能。
Codegen：了解 Codegen 的代码生成机制，简化原生模块开发。

（7）UI 组件库
React Native Paper：探索 React Native Paper 的最新组件和主题支持。
NativeBase：学习 NativeBase 3 的设计理念和使用方法。

## React Native如何实现跨平台开发？与原生开发相比有哪些优缺点？

1）基于 JavaScript 和 React
JavaScript：使用 JavaScript 编写业务逻辑。

React：使用 React 组件化开发 UI。

（2）桥接机制
JavaScript 与原生代码通信：通过桥接机制实现 JavaScript 与原生代码的通信。

原生模块：通过编写原生模块（Native Modules）访问平台特定功能。

（3）跨平台组件
核心组件：提供跨平台的核心组件（如 View、Text、Image）。

平台特定代码：通过 Platform API 或文件后缀（如 .ios.js、.android.js）实现平台特定代码。

（4）第三方库
社区支持：使用丰富的第三方库（如 react-navigation、react-native-maps）加速开发。

（1）优点
代码复用：
开发效率：
社区支持：

（2）缺点
性能限制：
平台差异
调试难度：

3. React Native 的适用场景
（1）适合场景
中小型应用：快速开发中小型应用，降低开发成本。

跨平台需求：需要同时支持 iOS 和 Android 的应用。

动态更新：需要频繁更新内容的应用（如新闻、电商）。

（2）不适合场景
高性能需求：需要高性能图形处理或复杂动画的应用（如游戏）。

平台特定功能：需要深度集成平台特定功能的应用（如 AR/VR）。

## 你对物流行业了解多少？快递员使用的App有哪些核心功能？

（1）物流环节
运输：包括陆运、海运、空运等多种运输方式。

仓储：货物的存储和管理，涉及库存管理、订单处理等。

配送：最后一公里的配送服务，直接面向客户。

（2）技术驱动
信息化：通过物流管理系统（TMS、WMS）实现物流信息的实时跟踪和管理。

自动化：自动化仓储设备（如 AGV、无人机）和智能分拣系统。

数据化：通过大数据分析优化物流路径和资源配置。

2. 快递员使用的 App 的核心功能

（1）订单管理
订单接收：实时接收并查看配送订单。

订单状态更新：更新订单状态（如已接单、配送中、已签收）。

订单筛选和排序：根据优先级、距离等条件筛选和排序订单。

（2）路线规划
智能导航：根据订单地址自动规划最优配送路线。

实时交通信息：提供实时交通信息，避开拥堵路段。

（3）扫码签收
二维码/条形码扫描：通过扫描包裹上的二维码或条形码确认签收。

电子签名：客户在 App 上签名确认收货。

（4）客户沟通
电话/短信通知：自动发送短信或拨打电话通知客户配送信息。

在线聊天：通过 App 与客户实时沟通。

（5）数据统计
配送统计：查看每日、每周、每月的配送数据（如订单数量、配送时长）。

绩效评估：根据配送效率和服务质量进行绩效评估。

（6）异常处理
异常订单上报：上报无法配送的订单（如地址错误、客户不在家）。

问题反馈：反馈配送过程中遇到的问题（如包裹损坏、客户投诉）。

（7）个人中心
个人信息管理：查看和更新个人信息（如联系方式、银行账户）。

通知公告：接收公司发布的通知和公告。

## 在网络不稳定的情况下，如何确保App正常运行？

1. 数据缓存与持久化
目标： 确保关键数据在无网或弱网情况下可用。

AsyncStorage / MMKV / SQLite
AsyncStorage（官方提供，适用于小数据存储）。
MMKV（比 AsyncStorage 速度快，适用于大数据存储）。
SQLite / WatermelonDB（适用于需要查询的本地数据库）。
场景：
快递员登录信息本地存储，即使无网也能进入 App。
缓存上次的订单列表、地图数据，让用户能继续操作。
图片/视频等大文件可用本地存储，上传失败后补传。

2. 离线任务队列
目标： 让 App 在无网络时仍然能提交数据，并在网络恢复时自动同步。

解决方案：

任务队列机制（类似消息队列）：在本地存储任务（订单状态变更、快递签收等），待网络恢复后批量上传。
使用库： react-native-queue 或 redux-offline。

3. 断网检测
目标： 及时发现网络状态变化，提示用户或采取措施。

4. 数据同步策略
目标： 避免网络恢复后数据冲突或丢失。

解决方案

版本控制：后端提供数据版本号，避免覆盖最新数据。
增量同步：只同步变化的数据，减少流量消耗。
乐观更新：先更新 UI，再与服务器同步，失败后回滚。

5. WebSocket + 轮询
目标： 确保实时数据更新，即使 WebSocket 断开，也能自动恢复。

6. 地图与导航
目标： 让快递员在无网或弱网情况下仍能查看地图。

使用离线地图

高德地图 / Google Maps 支持离线地图下载。
方案：提前缓存快递员常用区域的地图数据。

后台定位

react-native-background-geolocation 可以在后台持续记录位置，即使断网后仍然存储数据，并在恢复后上传。

7. UI 友好提示



## 如何确保App的数据安全，特别是用户隐私和订单信息？

1. 网络通信安全

(1) HTTPS + TLS 加密
使用 HTTPS：确保所有 API 请求都通过 HTTPS，而不是 HTTP。
强制 TLS 1.2+：
确保服务器和 App 仅支持 TLS 1.2 或更高版本，避免 TLS 1.0 和 1.1（已被淘汰）。
(2) API 签名和防重放攻击
HMAC（哈希消息认证码）：每个请求附带一个签名（如 SHA256(secret + timestamp + request_body)），服务器验证签名是否匹配。
防重放攻击：
在请求头加 timestamp，服务器拒绝超时请求（如 5分钟 以内）。
服务器检查 nonce（随机数），防止重复请求被伪造。

2. 身份验证和权限控制

3. 本地存储安全

(1) 避免存储敏感数据
不要存储 JWT 令牌在 AsyncStorage 中，因为它容易被反编译读取。
推荐存储方式：
iOS：使用 Keychain（react-native-keychain）。
Android：使用 Keystore（EncryptedSharedPreferences）。

(2) 数据加密存储
MMKV / SQLite 数据加密：
使用 AES 加密，确保本地存储的数据即使被盗取，也无法直接读取。
推荐库：
react-native-mmkv（支持 AES 加密）。
react-native-sqlite-storage（数据库加密）。

4. 防止逆向工程和代码注入

(1) 代码混淆
在 metro.config.js 启用 JS 代码混淆，防止攻击者轻易理解代码逻辑。
启用 ProGuard（Android），防止 Java 代码被反编译。
在 android/app/proguard-rules.pro 添加：
```java
-keep class com.facebook.** { *; }
-keep class expo.modules.** { *; }
```

(2) 防止调试和篡改
检测 Root（Android）/ Jailbreak（iOS），防止 App 运行在受攻击的设备上。
检测 Hook 工具（Frida、Xposed），防止恶意修改代码。

5. 订单数据安全

6. 日志与异常处理

## 你如何确保代码质量？是否参与过代码审查？

1. 代码规范
(1) 代码格式化
使用 ESLint + Prettier 自动格式化
    遵循 Airbnb / Standard 代码规范。
    结合 husky + lint-staged，在提交代码前自动检查格式。

(2) 统一编码风格
    变量命名：camelCase（小驼峰），常量 UPPER_CASE，类 PascalCase。
    组件命名：OrderListScreen.js 而不是 orderlist.js，确保结构清晰。

2. 代码模块化

(1) 组件化开发
(2) 代码拆分

3. 性能优化

4. 单元测试 + 端到端测试

5. 代码审查（Code Review）

(1) Code Review 机制
使用 GitHub/GitLab Merge Request 进行代码审查。
代码提交前，至少有 1-2 位同事 进行 Review。
代码 Review 重点关注：
    代码逻辑是否清晰？
    是否有性能问题？
    是否有未处理的异常？
    是否遵循了团队的编码规范？


## 在项目中是否进行过代码重构？如何确保重构不影响现有功能？

目标：识别代码中的坏味道（Code Smell），优化代码结构。

重构场景	问题	解决方案
代码重复	发现多个页面重复编写相似的 API 请求	抽取 useOrderData 自定义 Hook
组件耦合度高	UI 组件直接包含业务逻辑	UI 组件与逻辑层解耦（Presentational + Container 模式）
API 代码冗余	API 请求代码分散在各个组件中	统一封装 API 服务层（services/orderService.js）
组件性能低	组件无必要地重复渲染	使用 React.memo() 和 useCallback()
状态管理混乱	组件内部 state 过多，导致数据流混乱	统一管理状态（Pinia / Redux / Zustand）


