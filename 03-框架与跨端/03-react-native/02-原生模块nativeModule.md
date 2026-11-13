# RN 原生模块（Native Module）

> 只要 RN 没有封装某个平台能力，或者某段计算放在 JS 线程上会卡住交互，就该落到原生模块；判断标准是「需不需要平台 API」和「要不要离开 JS 线程」。

原生模块官方定位：

> 有时候 App 需要访问平台 API，但在 React Native 可能还没有相应的模块。或者你需要复用一些 Java 代码，而不想用 JavaScript 再重新实现一遍；又或者你需要实现某些高性能的、多线程的代码，譬如图片处理、数据库、或者一些高级扩展。我们把 React Native 设计为可以在其基础上编写真正的原生代码，并且可以访问平台所有的能力。

## 开发安卓原生模块流程

1. 编写原生模块的相关代码；
2. 暴露接口和数据交互；
3. 注册与导出 RN 原生模块。

下面按这三步走完整流程。

## 第一步：写模块类

新建 `android/app/src/main/java/com/yourapp/DeviceInfoModule.java`：

```java
package com.yourapp;

import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;
import com.facebook.react.bridge.Promise;
import com.facebook.react.bridge.WritableMap;
import com.facebook.react.bridge.Arguments;

public class DeviceInfoModule extends ReactContextBaseJavaModule {
    private final ReactApplicationContext context;

    public DeviceInfoModule(ReactApplicationContext ctx) {
        super(ctx);
        this.context = ctx;
    }

    // JS 里通过 NativeModules.DeviceInfo 访问，名字必须固定
    @Override
    public String getName() {
        return "DeviceInfo";
    }

    // 同步方法：JS 调用时立刻返回，不要做耗时操作
    @ReactMethod(isBlockingSynchronousMethod = true)
    public String getAppVersion() {
        try {
            return context.getPackageManager()
                .getPackageInfo(context.getPackageName(), 0).versionName;
        } catch (Exception e) {
            return "unknown";
        }
    }

    // 异步方法：返回 Promise，JS 侧 await 使用
    @ReactMethod
    public void getDeviceInfo(Promise promise) {
        try {
            WritableMap map = Arguments.createMap();
            map.putString("brand", android.os.Build.BRAND);
            map.putString("model", android.os.Build.MODEL);
            map.putInt("sdkInt", android.os.Build.VERSION.SDK_INT);
            promise.resolve(map);
        } catch (Exception e) {
            promise.reject("ERR_DEVICE_INFO", e);
        }
    }
}
```

三个要点：

- `getName()` 返回的名字就是 JS 侧 `NativeModules.X` 的 key，改名等于改接口
- 原生方法必须在**原生模块线程**执行，不能直接碰 UI；要改 UI 用 `UiThreadUtil.runOnUiThread`
- 同步方法会阻塞 JS 线程，只适合读常量这类瞬时操作；网络、文件、加解密一律用 Promise

## 第二步：用 Package 注册模块

```java
package com.yourapp;

import com.facebook.react.ReactPackage;
import com.facebook.react.bridge.NativeModule;
import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.uimanager.ViewManager;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class DeviceInfoPackage implements ReactPackage {
    @Override
    public List<NativeModule> createNativeModules(ReactApplicationContext ctx) {
        List<NativeModule> modules = new ArrayList<>();
        modules.add(new DeviceInfoModule(ctx));
        return modules;
    }

    @Override
    public List<ViewManager> createViewManagers(ReactApplicationContext ctx) {
        return Collections.emptyList();
    }
}
```

## 第三步：挂到 Application 上

RN 0.7x 之后 `MainApplication` 是 Kotlin 写的，在 `getPackages()` 里加：

```kotlin
override fun getPackages(): List<ReactPackage> =
    PackageList(this).packages.apply {
        add(DeviceInfoPackage())
    }
```

老版本（Java 写法）是在 `Arrays.asList(new MainReactPackage(), new DeviceInfoPackage())` 里加一项。

## JS 侧调用

```js
import { NativeModules, Platform } from 'react-native';

const { DeviceInfo } = NativeModules;

export async function getDeviceInfo() {
  if (Platform.OS !== 'android' || !DeviceInfo) {
    return null;   // iOS 未实现时必须降级，否则 undefined is not a function
  }
  return DeviceInfo.getDeviceInfo();   // Promise
}

export function getAppVersion() {
  return DeviceInfo?.getAppVersion() ?? '0.0.0';
}
```

配一份 TypeScript 声明，调用处才有类型提示：

```ts
// types/native.d.ts
declare module 'react-native' {
  interface NativeModulesStatic {
    DeviceInfo: {
      getAppVersion(): string;
      getDeviceInfo(): Promise<{ brand: string; model: string; sdkInt: number }>;
    };
  }
}
```

## 数据类型的对应关系

桥接层只认固定几种类型，传错会静默变成 `null`：

| JS | Android | iOS |
|---|---|---|
| `string` / `number` / `boolean` | `String` / `double` / `boolean` | `NSString` / `NSNumber` / `BOOL` |
| `Object` | `ReadableMap` / `WritableMap` | `NSDictionary` |
| `Array` | `ReadableArray` / `WritableArray` | `NSArray` |
| `null` | `null` | `NSNull` |

注意数字统一走 `double`，原生里想用 `int` 需要自己转换；返回 `undefined` 会变成 `null`。

## iOS 侧的对应写法

```objc
// DeviceInfo.m
#import <React/RCTBridgeModule.h>

@interface RCT_EXTERN_MODULE(DeviceInfo, NSObject)
RCT_EXTERN_METHOD(getDeviceInfo:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject)
@end
```

iOS 的模块名默认是类名，可以通过 `RCT_EXPORT_MODULE(DeviceInfo)` 指定。两端 `getName()` 必须一致，JS 侧才能共用一份调用代码。

## 常见误区

**很多人以为改完原生代码 reload JS 就生效**。原生代码改动必须重新 `npx react-native run-android` 编译安装，Metro 的热更新只能改 JS。

**很多人以为模块没注册是 RN 的 bug**。`NativeModules.Xxx` 为 `undefined` 时，九成是 Package 没加进 `getPackages()`，或者加了但没重新编译。

**很多人以为所有逻辑都该放原生**。桥接有序列化成本，频繁小数据往返（比如每帧调一次）比纯 JS 还慢。高频场景应该合并成一次调用，或者用 JSI 直接共享内存。

**很多人以为 `@ReactMethod` 能返回任意类型**。它只能是 `void`，返回值必须通过 Promise、Callback 或事件发回。想同步返回要显式加 `isBlockingSynchronousMethod = true`。

## 新架构下的变化

RN 0.7x 起支持新架构（Fabric + TurboModules）。TurboModule 不再依赖运行时桥接，而是用 Codegen 从 TS 类型声明生成原生接口，调用是 C++ JSI 直连，省掉 JSON 序列化。

迁移成本主要在：类型声明文件（`NativeXxx.ts` 里的 `TurboModuleRegistry.getEnforcing`）、codegen 配置（`package.json` 的 `codegenConfig`）、以及原生侧要继承 `NativeXxxSpec` 而不是 `ReactContextBaseJavaModule`。做新模块时如果项目已开新架构，直接按 TurboModule 写更划算。

## 关联阅读

- [Android 原生基础](../04-android/README.md)
- [查看 Maven 包的 Java 包名](./03-查看Maven包的Java包名.md)
- [03-框架与跨端 索引](../README.md)
