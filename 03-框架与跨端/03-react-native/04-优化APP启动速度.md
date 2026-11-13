# 优化 APP 启动速度

## 启动流程分析与测量

### React Native 启动流程

```text
冷启动：
应用启动 → Android/iOS Native → React Native 初始化 → JS Bundle 加载 → JS 执行 → 渲染 → 首屏显示

热启动：
应用启动 → JS 已加载 → JS 执行 → 渲染 → 首屏显示
```

### 测量工具

```js
// 1. 使用 React Native Performance API
import { Performance } from 'react-native-performance';

// 标记关键时间点
Performance.mark('appLaunchStart');
Performance.mark('rnInitStart');
Performance.mark('jsBundleLoadStart');
Performance.mark('jsExecutionStart');
Performance.mark('firstRenderStart');
Performance.mark('firstPaint');

// 测量阶段耗时
Performance.measure('appLaunch', 'appLaunchStart', 'firstPaint');
Performance.measure('rnInit', 'rnInitStart', 'jsBundleLoadStart');
Performance.measure('jsBundleLoad', 'jsBundleLoadStart', 'jsExecutionStart');
Performance.measure('jsExecution', 'jsExecutionStart', 'firstRenderStart');
Performance.measure('firstRender', 'firstRenderStart', 'firstPaint');

// 获取测量结果
const measurements = Performance.getEntriesByType('measure');
measurements.forEach(({ name, duration }) => {
  console.log(`${name}: ${duration.toFixed(2)}ms`);
});

// 2. 自定义性能监控
class PerformanceMonitor {
  static timings = {};

  static start(key) {
    this.timings[key] = {
      startTime: Date.now(),
      startPerfTime: performance.now()
    };
  }

  static end(key) {
    if (this.timings[key]) {
      this.timings[key].endTime = Date.now();
      this.timings[key].endPerfTime = performance.now();
      this.timings[key].duration =
        this.timings[key].endPerfTime - this.timings[key].startPerfTime;

      console.log(`${key}耗时: ${this.timings[key].duration.toFixed(2)}ms`);
    }
  }

  static logAll() {
    Object.entries(this.timings).forEach(([key, timing]) => {
      if (timing.duration) {
        console.log(`🔥 ${key}: ${timing.duration.toFixed(2)}ms`);
      }
    });
  }
}

// 3. Android 测量 (MainApplication.java)
public class MainApplication extends Application {
  @Override
  public void onCreate() {
    super.onCreate();
    long startTime = System.currentTimeMillis();

    SoLoader.init(this, false);

    // React Native 初始化
    long rnStartTime = System.currentTimeMillis();
    initializeFlipper(this);
    long rnEndTime = System.currentTimeMillis();

    Log.d("Performance", "RN初始化耗时: " + (rnEndTime - rnStartTime) + "ms");
    Log.d("Performance", "App启动总耗时: " + (System.currentTimeMillis() - startTime) + "ms");
  }
}

// 4. iOS 测量 (AppDelegate.mm)
- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
  NSDate *startTime = [NSDate date];

  // React Native 初始化
  NSDate *rnStartTime = [NSDate date];
  RCTBridge *bridge = [[RCTBridge alloc] initWithDelegate:self launchOptions:launchOptions];
  NSDate *rnEndTime = [NSDate date];

  NSTimeInterval rnInitTime = [rnEndTime timeIntervalSinceDate:rnStartTime];
  NSLog(@"RN初始化耗时: %.2fms", rnInitTime * 1000);
  NSLog(@"App启动总耗时: %.2fms", [[NSDate date] timeIntervalSinceDate:startTime] * 1000);

  return YES;
}
```

## Native 层优化

### Android 优化

```java
// MainApplication.java - 优化版本
public class MainApplication extends Application implements ReactApplication {
  private final ReactNativeHost mReactNativeHost = new ReactNativeHost(this) {
    @Override
    public boolean getUseDeveloperSupport() {
      return BuildConfig.DEBUG;
    }

    @Override
    protected List<ReactPackage> getPackages() {
      @SuppressWarnings("UnnecessaryLocalVariable")
      List<ReactPackage> packages = new PackageList(this).getPackages();

      // 1. 预加载常用模块
      preloadModules();

      // 2. 延迟加载非必要模块
      packages.add(new LazyReactPackage() {
        @Override
        public List<ModuleSpec> getModules() {
          // 延迟加载的模块
          return Arrays.asList(
            ModuleSpec.nativeModuleSpec(
              AnalyticsModule.class,
              () -> new AnalyticsModule()
            )
          );
        }
      });

      return packages;
    }

    @Override
    protected String getJSMainModuleName() {
      return "index";
    }

    // 3. 使用 Hermes 引擎
    @Override
    protected String getJSBundleFile() {
      // 预加载的 bundle 文件
      return "assets://index.android.bundle";
    }

    @Override
    protected JSIModulePackage getJSIModulePackage() {
      return new JSIModulePackage() {
        @Override
        public List<JSIModuleSpec> getJSIModules(
          final ReactApplicationContext reactApplicationContext,
          final JavaScriptContextHolder jsContext
        ) {
          // 启用 TurboModules
          List<JSIModuleSpec> modules = new ArrayList<>();
          modules.add(
            new JSIModuleSpec() {
              @Override
              public JSIModuleType getJSIModuleType() {
                return JSIModuleType.TurboModuleManager;
              }

              @Override
              public JSIModuleProvider getJSIModuleProvider() {
                return new TurboModuleManagerProvider();
              }
            }
          );
          return modules;
        }
      };
    }
  };

  private void preloadModules() {
    // 在主线程空闲时预加载
    Handler mainHandler = new Handler(Looper.getMainLooper());
    mainHandler.postDelayed(() -> {
      // 预加载常用 native 模块
      AsyncTask.execute(() -> {
        try {
          // 提前实例化常用模块
          Class.forName("com.facebook.react.modules.core.DeviceEventManagerModule");
          Class.forName("com.facebook.react.modules.network.NetworkingModule");
        } catch (ClassNotFoundException e) {
          e.printStackTrace();
        }
      });
    }, 1000); // 延迟1秒执行
  }

  // 4. 减少启动时的 Activity 初始化
  @Override
  public void onCreate() {
    super.onCreate();

    // 延迟初始化非关键组件
    new Handler().postDelayed(() -> {
      // 初始化推送、统计等非关键服务
      initNonCriticalServices();
    }, 3000);

    // 启用并发 React Native 初始化
    SoLoader.init(this, false);

    // 预加载字体
    preloadFonts();

    // 内存优化
    trimMemory();
  }

  private void preloadFonts() {
    // 预加载常用字体
    Typeface typeface = Typeface.createFromAsset(getAssets(), "fonts/Roboto-Regular.ttf");
    // 缓存字体
  }

  private void trimMemory() {
    // 内存紧张时清理
    registerComponentCallbacks(new ComponentCallbacks2() {
      @Override
      public void onTrimMemory(int level) {
        if (level >= ComponentCallbacks2.TRIM_MEMORY_UI_HIDDEN) {
          // 清理缓存
          ImagePipelineFactory.getInstance().getImagePipeline().clearMemoryCaches();
        }
      }
    });
  }
}

// 5. 优化 MainActivity.java
public class MainActivity extends ReactActivity {
  private long launchStartTime;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    // 1. 设置启动主题（避免白屏）
    setTheme(R.style.AppTheme_Splash);

    launchStartTime = System.currentTimeMillis();

    super.onCreate(savedInstanceState);

    // 2. 优化窗口设置
    getWindow().setFlags(
      WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
      WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS
    );

    // 3. 减少布局层次
    if (getReactRootView() != null) {
      ViewGroup rootView = (ViewGroup) getReactRootView().getParent();
      if (rootView != null) {
        rootView.setBackground(null);
      }
    }

    // 4. 测量启动时间
    long launchEndTime = System.currentTimeMillis();
    Log.d("Performance", "Activity创建耗时: " + (launchEndTime - launchStartTime) + "ms");
  }

  @Override
  protected void onResume() {
    super.onResume();

    // 5. 延迟加载非关键UI
    new Handler().postDelayed(() -> {
      // 加载引导页、广告等
      loadNonCriticalUI();
    }, 1000);
  }
}

// 6. AndroidManifest.xml 优化
<!-- 启动主题设置 -->
<style name="AppTheme.Splash" parent="Theme.AppCompat.Light.NoActionBar">
  <item name="android:windowBackground">@drawable/splash_background</item>
  <item name="android:windowFullscreen">true</item>
  <item name="android:windowContentOverlay">@null</item>
  <item name="android:windowIsTranslucent">true</item>
</style>

<!-- 禁用不必要的权限检查 -->
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"
  android:maxSdkVersion="28" /> <!-- 仅限需要时使用 -->

<!-- 多进程配置（可选） -->
<service
  android:name=".MyService"
  android:process=":background" /> <!-- 后台进程 -->
```

### iOS 优化

```objective-c
// AppDelegate.mm - 优化版本
#import <React/RCTBridge.h>
#import <React/RCTBundleURLProvider.h>
#import <React/RCTRootView.h>
#import <React/RCTAppSetupUtils.h>

@implementation AppDelegate {
  NSDate *_launchStartTime;
  NSDate *_rnInitStartTime;
}

- (BOOL)application:(UIApplication *)application
    didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {

  _launchStartTime = [NSDate date];

  // 1. 设置启动图
  UIStoryboard *launchScreen = [UIStoryboard storyboardWithName:@"LaunchScreen" bundle:nil];
  UIViewController *launchScreenVC = [launchScreen instantiateInitialViewController];
  self.window.rootViewController = launchScreenVC;
  [self.window makeKeyAndVisible];

  // 2. 异步初始化 React Native
  dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
    _rnInitStartTime = [NSDate date];

    // 提前加载必要资源
    [self preloadResources];

    // 在主线程初始化 RN
    dispatch_async(dispatch_get_main_queue(), ^{
      [self initializeReactNative];
    });
  });

  // 3. 延迟初始化非关键服务
  [self performSelector:@selector(initializeNonCriticalServices)
             withObject:nil
             afterDelay:2.0];

  return YES;
}

- (void)initializeReactNative {
  RCTBridge *bridge = [self.reactDelegate createBridgeWithDelegate:self launchOptions:self.launchOptions];

  // 4. 使用预加载的 bundle
  NSURL *bundleURL = [self getBundleURL];

  // 5. 启用 TurboModules
  RCTAppSetupPrepareApp(application);

  RCTRootView *rootView = [self.reactDelegate createRootViewWithBridge:bridge
                             moduleName:@"YourAppName"
                             initialProperties:nil];

  // 6. 优化 RootView 配置
  rootView.backgroundColor = [UIColor clearColor];
  rootView.loadingView = nil; // 禁用默认 loading view

  UIViewController *rootViewController = [self.reactDelegate createRootViewController];
  rootViewController.view = rootView;

  // 7. 替换启动图
  [UIView transitionWithView:self.window
                    duration:0.3
                     options:UIViewAnimationOptionTransitionCrossDissolve
                  animations:^{
                    self.window.rootViewController = rootViewController;
                  }
                  completion:nil];

  // 8. 测量性能
  NSTimeInterval rnInitTime = [[NSDate date] timeIntervalSinceDate:_rnInitStartTime];
  NSTimeInterval totalTime = [[NSDate date] timeIntervalSinceDate:_launchStartTime];

  NSLog(@"🔥 RN初始化耗时: %.2fms", rnInitTime * 1000);
  NSLog(@"🔥 总启动耗时: %.2fms", totalTime * 1000);
}

- (NSURL *)getBundleURL {
  #if DEBUG
    return [[RCTBundleURLProvider sharedSettings] jsBundleURLForBundleRoot:@"index"];
  #else
    // 生产环境使用预加载的 bundle
    return [[NSBundle mainBundle] URLForResource:@"main" withExtension:@"jsbundle"];
  #endif
}

- (void)preloadResources {
  // 预加载字体
  UIFont *font = [UIFont fontWithName:@"Roboto-Regular" size:14];

  // 预加载图片到缓存
  UIImage *image = [UIImage imageNamed:@"splash"];

  // 初始化常用框架
  [SDWebImageManager sharedManager];
}

- (void)initializeNonCriticalServices {
  // 初始化推送、统计、广告等
  [PushNotificationManager setup];
  [AnalyticsManager start];
}

// 9. 内存优化
- (void)applicationDidReceiveMemoryWarning:(UIApplication *)application {
  // 清理图片缓存
  [[SDImageCache sharedImageCache] clearMemory];
  [[YYWebImageManager sharedManager].cache.memoryCache removeAllObjects];
}

// 10. 后台预加载
- (void)applicationDidEnterBackground:(UIApplication *)application {
  // 预加载下一个可能访问的 bundle
  dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_LOW, 0), ^{
    [self preloadNextBundle];
  });
}

@end

// Info.plist 配置
<!-- 禁用启动白屏 -->
<key>UIViewControllerBasedStatusBarAppearance</key>
<false/>

<!-- 启动图配置 -->
<key>UILaunchStoryboardName</key>
<string>LaunchScreen</string>

<!-- 后台任务 -->
<key>UIBackgroundModes</key>
<array>
  <string>fetch</string>
  <string>remote-notification</string>
</array>
```

## JavaScript 层优化

### Bundle 优化

```jsx
// metro.config.js - 优化配置
const { getDefaultConfig } = require('@react-native/metro-config');
const path = require('path');

const config = {
  transformer: {
    getTransformOptions: async () => ({
      transform: {
        experimentalImportSupport: false,
        inlineRequires: true, // 启用 inline requires
      },
    }),
    // 启用 Hermes 优化
    hermesParser: true,
    minifierConfig: {
      compress: {
        drop_console: true, // 生产环境移除 console
        drop_debugger: true,
        pure_funcs: ['console.log', 'console.info', 'console.debug'],
        passes: 3, // 多轮压缩
      },
      mangle: {
        toplevel: true,
      },
    },
  },
  resolver: {
    // 1. 优化模块解析
    resolverMainFields: ['react-native', 'browser', 'main'],
    // 2. 排除不必要的文件
    blockList: [
      /.*\/__tests__\/.*/,
      /.*\/__fixtures__\/.*/,
      /.*\/__mocks__\/.*/,
      /node_modules\/.*\/node_modules\/react-native\/.*/,
    ],
    // 3. 别名配置，减少查找时间
    alias: {
      'react-native$': 'react-native-web',
      '@components': path.resolve(__dirname, 'src/components'),
      '@utils': path.resolve(__dirname, 'src/utils'),
      '@assets': path.resolve(__dirname, 'src/assets'),
    },
    // 4. 启用加速解析
    unstable_enableSymlinks: true,
    unstable_enablePackageExports: true,
  },
  serializer: {
    // 5. 优化包大小
    getModulesRunBeforeMainModule: () => [
      require.resolve('./src/polyfills.js'),
    ],
    getPolyfills: () => [],
    // 6. 模块分组
    createModuleIdFactory: () => {
      return (path) => {
        // 根据路径创建优化的 moduleId
        const projectRootPath = __dirname;
        let moduleId = path.substr(projectRootPath.length + 1);

        // 常用模块给较小的 ID
        if (moduleId.includes('node_modules/react-native/')) {
          return 1;
        }
        if (moduleId.includes('node_modules/react/')) {
          return 2;
        }

        return moduleId;
      };
    },
  },
  // 7. 缓存配置
  cacheStores: [
    new (require('metro-cache')).FileStore({
      root: path.join(__dirname, 'node_modules', '.cache', 'metro'),
    }),
  ],
  cacheVersion: '1.0',
  maxWorkers: require('os').cpus().length, // 使用所有 CPU 核心
};

module.exports = config;

// package.json - Bundle 分析脚本
{
  "scripts": {
    "analyze-bundle": "react-native bundle --platform android --dev false --entry-file index.js --bundle-output /tmp/bundle.android.js --sourcemap-output /tmp/bundle.android.map --minify false",
    "visualize-bundle": "source-map-explorer /tmp/bundle.android.js /tmp/bundle.android.map --html > bundle-report.html"
  }
}

// bundle 分析工具
import { analyze } from '@bundle-analyzer/core';

async function analyzeBundle() {
  const report = await analyze({
    platform: 'android',
    minify: true,
    dev: false,
  });

  console.log('📦 Bundle 分析报告:');
  console.log('总大小:', report.totalSize);
  console.log('模块数量:', report.moduleCount);
  console.log('最大模块:', report.largestModules.slice(0, 5));
}
```

### 代码分割与延迟加载

```js
// 1. 动态导入（Code Splitting）
// App.js
import React, { Suspense, lazy } from "react";
import { View, ActivityIndicator } from "react-native";

// 延迟加载的组件
const HomeScreen = lazy(() => import("./screens/HomeScreen"));
const ProfileScreen = lazy(() => import("./screens/ProfileScreen"));
const SettingsScreen = lazy(() => import("./screens/SettingsScreen"));

// 按需加载的模块
const HeavyComponent = lazy(() =>
    Promise.all([
        import("./components/HeavyComponent"),
        new Promise(resolve => setTimeout(resolve, 100)), // 添加延迟避免阻塞
    ]).then(([module]) => module)
);

function App() {
    const [currentScreen, setCurrentScreen] = React.useState("home");

    const renderScreen = () => {
        switch (currentScreen) {
            case "home":
                return (
                    <Suspense fallback={<LoadingFallback />}>
                        <HomeScreen />
                    </Suspense>
                );
            case "profile":
                return (
                    <Suspense fallback={<LoadingFallback />}>
                        <ProfileScreen />
                    </Suspense>
                );
            case "settings":
                return (
                    <Suspense fallback={<LoadingFallback />}>
                        <SettingsScreen />
                    </Suspense>
                );
            default:
                return null;
        }
    };

    return (
        <View style={{ flex: 1 }}>
            {renderScreen()}
            <NavigationBar onNavigate={setCurrentScreen} />
        </View>
    );
}

function LoadingFallback() {
    return (
        <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
            <ActivityIndicator size="large" />
        </View>
    );
}

// 2. 预加载策略
class PreloadManager {
    static cache = new Map();

    static async preloadComponent(componentPath) {
        if (this.cache.has(componentPath)) {
            return this.cache.get(componentPath);
        }

        const promise = import(componentPath);
        this.cache.set(componentPath, promise);

        // 空闲时预加载
        if ("requestIdleCallback" in window) {
            requestIdleCallback(() => {
                promise.then(module => {
                    console.log(`预加载完成: ${componentPath}`);
                });
            });
        }

        return promise;
    }

    static preloadCriticalComponents() {
        // 预加载首屏需要的组件
        const criticalComponents = [
            "./components/Header",
            "./components/ProductList",
            "./components/CartButton",
        ];

        criticalComponents.forEach(component => {
            this.preloadComponent(component);
        });
    }

    static preloadOnInteraction(componentPath, triggerElement) {
        // 用户交互时预加载
        triggerElement.addEventListener(
            "touchstart",
            () => {
                this.preloadComponent(componentPath);
            },
            { once: true }
        );
    }
}

// 3. 路由级别的代码分割
// 使用 react-navigation 的 lazy 选项
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

const Tab = createBottomTabNavigator();

function MainTabs() {
    return (
        <Tab.Navigator
            screenOptions={{
                lazy: true, // 延迟加载非活动标签页
                lazyPreloadDistance: 1, // 预加载相邻页面
            }}
        >
            <Tab.Screen
                name="Home"
                component={lazy(() => import("./screens/HomeScreen"))}
                options={{ lazy: false }} // 首页不延迟加载
            />
            <Tab.Screen name="Search" component={lazy(() => import("./screens/SearchScreen"))} />
            <Tab.Screen name="Profile" component={lazy(() => import("./screens/ProfileScreen"))} />
        </Tab.Navigator>
    );
}

// 4. 条件导入
const loadAnalytics = () => {
    // 只在需要时加载分析 SDK
    if (__DEV__) {
        return Promise.resolve({ track: () => {} });
    }
    return import("@analytics/sdk").then(module => module.default);
};

const loadMaps = () => {
    // 根据用户位置决定是否加载地图
    if (userNeedsMaps) {
        return import("react-native-maps");
    }
    return Promise.resolve(null);
};

// 5. 模块初始化优化
class LazyModule {
    static instance = null;

    static async getInstance() {
        if (!this.instance) {
            // 延迟加载模块
            const module = await import("./heavy-module");
            this.instance = new module.default();

            // 空闲时初始化
            await this.instance.initialize();
        }
        return this.instance;
    }
}

// 使用
const heavyModule = await LazyModule.getInstance();
```

### 启动时的 JavaScript 优化

```js
// 1. 减少启动时的同步操作
// AppRegistry 注册优化
import { AppRegistry, LogBox } from "react-native";
import { name as appName } from "./app.json";
import { startPerformanceMonitoring } from "./performance";

// 禁用不必要的警告
LogBox.ignoreLogs(["Require cycle:", "VirtualizedLists should never be nested"]);

// 延迟注册服务
setTimeout(() => {
    // 注册推送、统计等
    registerServices();
}, 1000);

// 2. 优化 App 入口
import React, { useEffect } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { GestureHandlerRootView } from "react-native-gesture-handler";

function App() {
    useEffect(() => {
        // 启动性能监控
        startPerformanceMonitoring();

        // 预加载数据
        preloadInitialData();

        // 缓存清理
        clearOldCache();
    }, []);

    // 使用轻量级初始组件
    return (
        <GestureHandlerRootView style={{ flex: 1 }}>
            <SafeAreaProvider>
                <NavigationContainer
                    // 优化导航器
                    onReady={() => {
                        console.log("导航器准备就绪");
                        // 标记首屏完成
                        Performance.mark("navigationReady");
                    }}
                    fallback={<SplashScreen />}
                >
                    <RootNavigator />
                </NavigationContainer>
            </SafeAreaProvider>
        </GestureHandlerRootView>
    );
}

// 3. 首屏渲染优化
function HomeScreen() {
    const [isReady, setIsReady] = React.useState(false);
    const [initialData, setInitialData] = React.useState(null);

    React.useEffect(() => {
        // 并行加载数据
        const loadData = async () => {
            const [userData, products, config] = await Promise.all([
                fetchUserData(),
                fetchProducts(),
                fetchConfig(),
            ]);

            setInitialData({ userData, products, config });
            setIsReady(true);

            // 标记首屏完成
            Performance.mark("homeScreenReady");
        };

        loadData();

        // 预加载下一屏数据
        preloadNextScreenData();
    }, []);

    if (!isReady) {
        return <SkeletonScreen />;
    }

    return (
        <View style={{ flex: 1 }}>
            {/* 优先渲染可视区域 */}
            <View style={{ height: 300 }}>
                <HeroSection data={initialData} />
            </View>

            {/* 延迟渲染长列表 */}
            {isReady && (
                <ProductList
                    products={initialData.products}
                    initialNumToRender={5} // 减少初始渲染数量
                    maxToRenderPerBatch={10}
                    windowSize={5}
                />
            )}

            {/* 延迟加载非关键组件 */}
            <LazyFooter />
        </View>
    );
}

// 4. 骨架屏优化
function SkeletonScreen() {
    return (
        <View style={{ flex: 1, padding: 16 }}>
            {/* 头部骨架 */}
            <View
                style={{
                    height: 60,
                    backgroundColor: "#f0f0f0",
                    borderRadius: 8,
                    marginBottom: 16,
                }}
            />

            {/* 卡片骨架 */}
            {[1, 2, 3].map(i => (
                <View
                    key={i}
                    style={{
                        height: 100,
                        backgroundColor: "#f0f0f0",
                        borderRadius: 8,
                        marginBottom: 12,
                    }}
                />
            ))}
        </View>
    );
}

// 5. 优化数据获取
class DataLoader {
    static cache = new Map();
    static pendingRequests = new Map();

    static async load(key, fetcher, options = {}) {
        const { ttl = 300000, priority = "low" } = options;

        // 检查缓存
        if (this.cache.has(key)) {
            const cached = this.cache.get(key);
            if (Date.now() - cached.timestamp < ttl) {
                return cached.data;
            }
        }

        // 避免重复请求
        if (this.pendingRequests.has(key)) {
            return this.pendingRequests.get(key);
        }

        // 创建请求
        const request = fetcher()
            .then(data => {
                this.cache.set(key, { data, timestamp: Date.now() });
                this.pendingRequests.delete(key);
                return data;
            })
            .catch(error => {
                this.pendingRequests.delete(key);
                throw error;
            });

        this.pendingRequests.set(key, request);

        // 根据优先级调度
        if (priority === "high") {
            return request;
        } else {
            // 低优先级请求延迟执行
            return new Promise(resolve => {
                setTimeout(() => resolve(request), 100);
            });
        }
    }
}

// 6. 启动时 JavaScript 执行优化
// 避免在模块顶层执行耗时操作
// ❌ 不好 - 在顶层执行
import { heavyComputation } from "./utils";
const result = heavyComputation(); // 会阻塞启动

// ✅ 好 - 延迟执行
let cachedResult = null;
const getResult = () => {
    if (!cachedResult) {
        cachedResult = heavyComputation();
    }
    return cachedResult;
};

// ✅ 更好 - 异步执行
const getResultAsync = async () => {
    if (!cachedResult) {
        // 在空闲时计算
        if ("requestIdleCallback" in window) {
            await new Promise(resolve => {
                requestIdleCallback(() => {
                    cachedResult = heavyComputation();
                    resolve();
                });
            });
        } else {
            await new Promise(resolve => setTimeout(resolve, 0));
            cachedResult = heavyComputation();
        }
    }
    return cachedResult;
};
```

## 渲染优化

### 列表优化

```js
import React, { memo, useMemo, useCallback } from "react";
import { FlatList, View, Text, Image, useWindowDimensions } from "react-native";

// 1. 优化列表项组件
const ProductItem = memo(
    ({ item, onPress }) => {
        return (
            <View style={styles.itemContainer}>
                <Image
                    source={{ uri: item.image }}
                    style={styles.image}
                    resizeMode="cover"
                    fadeDuration={0} // 禁用淡入动画
                />
                <Text style={styles.title} numberOfLines={2}>
                    {item.name}
                </Text>
                <Text style={styles.price}>¥{item.price}</Text>
            </View>
        );
    },
    (prevProps, nextProps) => {
        // 自定义比较函数
        return (
            prevProps.item.id === nextProps.item.id && prevProps.item.price === nextProps.item.price
        );
    }
);

// 2. 优化 FlatList 配置
function ProductList({ products }) {
    const { width } = useWindowDimensions();

    // 计算列数
    const numColumns = useMemo(() => {
        return width > 768 ? 3 : width > 480 ? 2 : 1;
    }, [width]);

    // 计算 item 宽度
    const itemWidth = useMemo(() => {
        return (width - 32 - (numColumns - 1) * 8) / numColumns;
    }, [width, numColumns]);

    // 优化渲染函数
    const renderItem = useCallback(
        ({ item }) => <ProductItem item={item} style={{ width: itemWidth }} />,
        [itemWidth]
    );

    // 提取 key
    const keyExtractor = useCallback(item => item.id, []);

    // 获取 item 布局
    const getItemLayout = useCallback(
        (data, index) => ({
            length: itemWidth + 100, // item 高度 + 间距
            offset: (itemWidth + 100) * index,
            index,
        }),
        [itemWidth]
    );

    return (
        <FlatList
            data={products}
            renderItem={renderItem}
            keyExtractor={keyExtractor}
            getItemLayout={getItemLayout}
            numColumns={numColumns}
            key={numColumns} // 列数变化时重新创建列表
            // 性能优化参数
            initialNumToRender={6} // 初始渲染数量
            maxToRenderPerBatch={10} // 每批渲染数量
            updateCellsBatchingPeriod={50} // 批量更新周期
            windowSize={5} // 渲染窗口大小
            removeClippedSubviews={true} // 移除不可见子视图
            // 滚动性能
            decelerationRate="fast"
            showsVerticalScrollIndicator={false}
            // 内存优化
            onEndReachedThreshold={0.5}
            onEndReached={loadMore}
            // 空状态
            ListEmptyComponent={<EmptyState />}
            // 分隔线
            ItemSeparatorComponent={() => <View style={styles.separator} />}
        />
    );
}

// 3. 虚拟化长列表
import { RecyclerListView, DataProvider, LayoutProvider } from "recyclerlistview";

class OptimizedList extends React.Component {
    constructor(props) {
        super(props);

        const dataProvider = new DataProvider((r1, r2) => {
            return r1.id !== r2.id;
        });

        this.state = {
            dataProvider: dataProvider.cloneWithRows(props.data),
        };

        // 布局提供器
        this.layoutProvider = new LayoutProvider(
            index => {
                return this.state.dataProvider.getDataForIndex(index).type;
            },
            (type, dim) => {
                switch (type) {
                    case "header":
                        dim.width = this.props.width;
                        dim.height = 100;
                        break;
                    case "item":
                        dim.width = this.props.width;
                        dim.height = 80;
                        break;
                }
            }
        );
    }

    render() {
        return (
            <RecyclerListView
                layoutProvider={this.layoutProvider}
                dataProvider={this.state.dataProvider}
                rowRenderer={this.rowRenderer}
                initialRenderIndex={0}
                renderAheadOffset={500}
                optimizeForInsertDelete={true}
            />
        );
    }
}

// 4. 分页和无限滚动优化
function PaginatedList() {
    const [data, setData] = useState([]);
    const [page, setPage] = useState(1);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);

    const loadMore = useCallback(async () => {
        if (loading || !hasMore) return;

        setLoading(true);

        try {
            const newData = await fetchData(page);

            if (newData.length === 0) {
                setHasMore(false);
            } else {
                setData(prev => [...prev, ...newData]);
                setPage(prev => prev + 1);
            }
        } catch (error) {
            console.error("加载失败:", error);
        } finally {
            setLoading(false);
        }
    }, [page, loading, hasMore]);

    // 防抖加载
    const debouncedLoadMore = useMemo(() => debounce(loadMore, 300), [loadMore]);

    return (
        <FlatList
            data={data}
            onEndReached={debouncedLoadMore}
            onEndReachedThreshold={0.1}
            ListFooterComponent={loading ? <ActivityIndicator /> : !hasMore ? <NoMoreData /> : null}
        />
    );
}
```

### 图片优化

```jsx
import React from "react";
import FastImage from "react-native-fast-image";
import { Image } from "react-native";

// 1. 使用 FastImage
function OptimizedImage({ uri, style, priority = "normal" }) {
    return (
        <FastImage
            style={style}
            source={{
                uri,
                priority: FastImage.priority[priority], // high, normal, low
                cache: FastImage.cacheControl.immutable, // 缓存策略
            }}
            resizeMode={FastImage.resizeMode.cover}
            onLoadStart={() => {
                // 显示占位符
            }}
            onLoad={() => {
                // 加载完成
            }}
            onError={() => {
                // 显示错误图片
            }}
        />
    );
}

// 2. 图片预加载
class ImagePreloader {
    static preloadImages = new Set();

    static async preload(imageUrls) {
        const promises = imageUrls.map(
            url =>
                new Promise((resolve, reject) => {
                    if (this.preloadImages.has(url)) {
                        resolve();
                        return;
                    }

                    Image.prefetch(url)
                        .then(() => {
                            this.preloadImages.add(url);
                            resolve();
                        })
                        .catch(reject);
                })
        );

        return Promise.all(promises);
    }

    static preloadCriticalImages() {
        // 预加载首屏图片
        const criticalImages = [
            "https://example.com/hero.jpg",
            "https://example.com/logo.png",
            "https://example.com/banner.jpg",
        ];

        this.preload(criticalImages);
    }
}

// 3. 渐进式图片加载
function ProgressiveImage({ uri, thumbnailUri, style }) {
    const [loaded, setLoaded] = useState(false);

    return (
        <View style={[style, { overflow: "hidden" }]}>
            {/* 缩略图 */}
            <FastImage
                source={{ uri: thumbnailUri }}
                style={[StyleSheet.absoluteFill, { opacity: loaded ? 0 : 1 }]}
                resizeMode="cover"
            />

            {/* 高清图 */}
            <FastImage
                source={{ uri }}
                style={[StyleSheet.absoluteFill, { opacity: loaded ? 1 : 0 }]}
                resizeMode="cover"
                onLoad={() => {
                    setLoaded(true);
                }}
            />
        </View>
    );
}

// 4. 图片尺寸优化
function ResponsiveImage({ source, aspectRatio = 1, maxWidth = 500 }) {
    const [dimensions, setDimensions] = useState(null);

    useEffect(() => {
        if (source.uri) {
            Image.getSize(source.uri, (width, height) => {
                const aspectRatio = width / height;
                setDimensions({ width, height, aspectRatio });
            });
        }
    }, [source.uri]);

    const imageStyle = useMemo(() => {
        if (!dimensions) return { width: "100%", aspectRatio };

        const { width, height } = dimensions;
        const calculatedWidth = Math.min(width, maxWidth);
        const calculatedHeight = calculatedWidth / (width / height);

        return {
            width: calculatedWidth,
            height: calculatedHeight,
            maxWidth: "100%",
        };
    }, [dimensions, aspectRatio, maxWidth]);

    return <Image source={source} style={imageStyle} />;
}

// 5. 图片缓存策略
import { ImageCacheManager } from "react-native-cached-image";

class OptimizedImageCache {
    static async prefetchAndCache(urls) {
        // 预下载并缓存
        await ImageCacheManager.downloadAndCacheUrls(urls, {
            ttl: 60 * 60 * 24 * 7, // 缓存7天
            useQueryParamsInCacheKey: false,
        });
    }

    static async getCachedImage(url) {
        const cachedPath = await ImageCacheManager.getCachedImagePath(url);

        if (cachedPath) {
            return { uri: `file://${cachedPath}` };
        }

        // 下载并缓存
        const result = await ImageCacheManager.downloadAndCacheUrl(url);
        return { uri: `file://${result.path}` };
    }

    static clearOldCache() {
        // 清理过期缓存
        ImageCacheManager.clearCache({ ttl: 60 * 60 * 24 * 30 }); // 清理30天前的缓存
    }
}
```

## 内存与缓存优化

### 内存管理

```js
// 1. 内存监控
import { DeviceEventEmitter, NativeModules } from "react-native";

class MemoryMonitor {
    static startMonitoring() {
        // Android 内存警告
        DeviceEventEmitter.addListener("onTrimMemory", level => {
            console.log(`内存警告级别: ${level}`);
            this.handleLowMemory(level);
        });

        // iOS 内存警告
        DeviceEventEmitter.addListener("memoryWarning", () => {
            this.handleLowMemory();
        });

        // 定期检查内存使用
        setInterval(() => {
            this.checkMemoryUsage();
        }, 60000); // 每分钟检查一次
    }

    static handleLowMemory(level) {
        // 根据内存级别清理资源
        const actions = {
            TRIM_MEMORY_COMPLETE: () => this.cleanupEverything(),
            TRIM_MEMORY_MODERATE: () => this.cleanupHeavyResources(),
            TRIM_MEMORY_BACKGROUND: () => this.cleanupCaches(),
            TRIM_MEMORY_UI_HIDDEN: () => this.cleanupUIResources(),
        };

        if (actions[level]) {
            actions[level]();
        }
    }

    static cleanupEverything() {
        // 清理所有缓存
        ImageCacheManager.clearCache();
        AsyncStorage.clear();

        // 卸载非活动组件
        unmountInactiveComponents();

        // 减少图片质量
        reduceImageQuality();
    }

    static cleanupHeavyResources() {
        // 清理大资源
        clearLargeCaches();
        unloadHeavyModules();
    }

    static async checkMemoryUsage() {
        if (Platform.OS === "android") {
            const memoryInfo = await NativeModules.AndroidMemory.getMemoryInfo();

            if (memoryInfo.percent > 80) {
                // 内存使用超过80%，开始清理
                this.cleanupCaches();
            }
        }
    }
}

// 2. 图片内存优化
class ImageMemoryManager {
    static config = {
        maxMemoryCacheSize: 50 * 1024 * 1024, // 50MB
        maxDiskCacheSize: 200 * 1024 * 1024, // 200MB
    };

    static optimizeImageLoading() {
        // 监听列表滚动，卸载不可见图片
        DeviceEventEmitter.addListener("scrollStateChanged", isScrolling => {
            if (isScrolling) {
                this.pauseImageLoading();
            } else {
                this.resumeImageLoading();
            }
        });

        // 后台时减少缓存
        AppState.addEventListener("change", state => {
            if (state === "background") {
                this.reduceCacheSize();
            }
        });
    }

    static pauseImageLoading() {
        // 暂停图片加载
        Image.prefetch = () => Promise.resolve();
    }

    static reduceCacheSize() {
        // 减少缓存大小
        ImageCacheManager.clearCache({ size: this.config.maxMemoryCacheSize / 2 });
    }
}

// 3. 组件内存泄漏预防
function useMemorySafeState(initialValue) {
    const [state, setState] = useState(initialValue);
    const isMounted = useRef(true);

    useEffect(() => {
        return () => {
            isMounted.current = false;
        };
    }, []);

    const safeSetState = useCallback(value => {
        if (isMounted.current) {
            setState(value);
        }
    }, []);

    return [state, safeSetState];
}

// 4. 大数据列表内存优化
function VirtualizedList({ data }) {
    const [visibleRange, setVisibleRange] = useState({ start: 0, end: 10 });

    // 只渲染可见项
    const visibleData = useMemo(() => {
        return data.slice(visibleRange.start, visibleRange.end);
    }, [data, visibleRange]);

    const handleScroll = useThrottle(event => {
        const { contentOffset, layoutMeasurement } = event.nativeEvent;
        const startIndex = Math.floor(contentOffset.y / 100);
        const endIndex = Math.floor((contentOffset.y + layoutMeasurement.height) / 100) + 2;

        setVisibleRange({ start: startIndex, end: endIndex });
    }, 100);

    return (
        <FlatList
            data={visibleData}
            renderItem={renderItem}
            onScroll={handleScroll}
            initialNumToRender={5}
            windowSize={3}
        />
    );
}
```

### 缓存策略

```jsx
// 1. 智能缓存系统
class SmartCache {
    static cache = new Map();
    static timestamps = new Map();
    static accessCounts = new Map();

    static set(key, value, options = {}) {
        const { ttl = 3600000, maxSize = 100 } = options;

        // 清理过期缓存
        this.cleanupExpired();

        // 检查缓存大小
        if (this.cache.size >= maxSize) {
            this.evictLRU();
        }

        this.cache.set(key, value);
        this.timestamps.set(key, Date.now());
        this.accessCounts.set(key, 0);

        // 设置过期时间
        if (ttl > 0) {
            setTimeout(() => {
                this.delete(key);
            }, ttl);
        }
    }

    static get(key) {
        if (!this.cache.has(key)) {
            return null;
        }

        // 更新访问计数和时间
        this.accessCounts.set(key, (this.accessCounts.get(key) || 0) + 1);
        this.timestamps.set(key, Date.now());

        return this.cache.get(key);
    }

    static delete(key) {
        this.cache.delete(key);
        this.timestamps.delete(key);
        this.accessCounts.delete(key);
    }

    static cleanupExpired() {
        const now = Date.now();
        for (const [key, timestamp] of this.timestamps) {
            if (now - timestamp > 3600000) {
                // 1小时
                this.delete(key);
            }
        }
    }

    static evictLRU() {
        // 找到最近最少使用的项
        let lruKey = null;
        let minAccessCount = Infinity;
        let oldestTimestamp = Infinity;

        for (const [key, accessCount] of this.accessCounts) {
            const timestamp = this.timestamps.get(key);

            if (
                accessCount < minAccessCount ||
                (accessCount === minAccessCount && timestamp < oldestTimestamp)
            ) {
                minAccessCount = accessCount;
                oldestTimestamp = timestamp;
                lruKey = key;
            }
        }

        if (lruKey) {
            this.delete(lruKey);
        }
    }

    static clear() {
        this.cache.clear();
        this.timestamps.clear();
        this.accessCounts.clear();
    }
}

// 2. 离线缓存
import NetInfo from "@react-native-community/netinfo";
import AsyncStorage from "@react-native-async-storage/async-storage";

class OfflineCache {
    static async cacheRequest(url, data) {
        const cacheKey = `cache_${btoa(url)}`;
        const cacheData = {
            data,
            timestamp: Date.now(),
            url,
        };

        await AsyncStorage.setItem(cacheKey, JSON.stringify(cacheData));
    }

    static async getCachedResponse(url) {
        const cacheKey = `cache_${btoa(url)}`;
        const cached = await AsyncStorage.getItem(cacheKey);

        if (cached) {
            const cacheData = JSON.parse(cached);

            // 检查是否过期（5分钟）
            if (Date.now() - cacheData.timestamp < 300000) {
                return cacheData.data;
            }
        }

        return null;
    }

    static async syncWhenOnline() {
        const netInfo = await NetInfo.fetch();

        if (netInfo.isConnected) {
            // 同步离线时的修改
            await this.syncPendingChanges();
        }
    }
}

// 3. 图片缓存优化
import { CacheManager } from "react-native-expo-image-cache";

class ImageCacheOptimizer {
    static async prefetchImages(images) {
        // 使用低优先级预加载
        const lowPriorityQueue = images.map(async url => {
            if (await CacheManager.isCached(url)) {
                return;
            }

            // 延迟加载避免阻塞
            await new Promise(resolve => setTimeout(resolve, 100));
            return CacheManager.prefetch(url);
        });

        // 分批预加载
        const batchSize = 3;
        for (let i = 0; i < lowPriorityQueue.length; i += batchSize) {
            const batch = lowPriorityQueue.slice(i, i + batchSize);
            await Promise.all(batch);
        }
    }

    static async getCachedImagePath(url) {
        const cachedPath = await CacheManager.getCachedPath(url, {});

        if (cachedPath) {
            return cachedPath;
        }

        // 渐进式加载
        const promise = CacheManager.prefetch(url);

        // 先返回低质量版本
        return {
            uri: url,
            cache: "force-cache",
        };
    }

    static clearUnusedCache() {
        // 清理一周内未访问的缓存
        CacheManager.clearCache({ days: 7 });
    }
}
```

## 网络优化

### 请求优化

```jsx
// 1. 请求合并与批处理
class RequestBatcher {
    static pendingRequests = new Map();
    static batchTimer = null;

    static async batchRequest(key, requestFn, delay = 50) {
        if (!this.pendingRequests.has(key)) {
            this.pendingRequests.set(key, []);
        }

        return new Promise((resolve, reject) => {
            this.pendingRequests.get(key).push({ resolve, reject, requestFn });

            if (!this.batchTimer) {
                this.batchTimer = setTimeout(() => {
                    this.executeBatch(key);
                }, delay);
            }
        });
    }

    static async executeBatch(key) {
        const requests = this.pendingRequests.get(key) || [];
        this.pendingRequests.delete(key);
        this.batchTimer = null;

        if (requests.length === 0) return;

        try {
            // 合并请求
            const results = await Promise.all(requests.map(r => r.requestFn()));

            // 分发结果
            requests.forEach((request, index) => {
                request.resolve(results[index]);
            });
        } catch (error) {
            requests.forEach(request => {
                request.reject(error);
            });
        }
    }
}

// 使用示例
const fetchUserData = userId => {
    return RequestBatcher.batchRequest(`user_${userId}`, () => api.get(`/users/${userId}`));
};

// 2. 请求优先级
class PriorityQueue {
    constructor() {
        this.highPriority = [];
        this.normalPriority = [];
        this.lowPriority = [];
        this.isProcessing = false;
    }

    add(task, priority = "normal") {
        const queue = this[`${priority}Priority`];
        queue.push(task);

        if (!this.isProcessing) {
            this.process();
        }
    }

    async process() {
        if (this.isProcessing) return;

        this.isProcessing = true;

        while (
            this.highPriority.length > 0 ||
            this.normalPriority.length > 0 ||
            this.lowPriority.length > 0
        ) {
            let task;

            if (this.highPriority.length > 0) {
                task = this.highPriority.shift();
            } else if (this.normalPriority.length > 0) {
                task = this.normalPriority.shift();
            } else {
                task = this.lowPriority.shift();
            }

            try {
                await task();
            } catch (error) {
                console.error("Task failed:", error);
            }

            // 让出主线程
            await new Promise(resolve => setTimeout(resolve, 0));
        }

        this.isProcessing = false;
    }
}

// 3. 连接复用
import axios from "axios";

const apiClient = axios.create({
    baseURL: "https://api.example.com",
    timeout: 10000,
    maxRedirects: 5,
    maxContentLength: 50 * 1024 * 1024,

    // 连接池配置
    httpAgent: new http.Agent({
        keepAlive: true,
        maxSockets: 50,
        maxFreeSockets: 10,
        timeout: 60000,
    }),

    httpsAgent: new https.Agent({
        keepAlive: true,
        maxSockets: 50,
        maxFreeSockets: 10,
        timeout: 60000,
    }),
});

// 4. 请求缓存
class RequestCache {
    static cache = new Map();

    static async cachedRequest(url, options = {}) {
        const cacheKey = `${url}_${JSON.stringify(options)}`;
        const cacheConfig = {
            ttl: options.ttl || 300000, // 5分钟
            staleWhileRevalidate: options.staleWhileRevalidate || false,
        };

        // 检查缓存
        const cached = this.cache.get(cacheKey);
        if (cached && Date.now() - cached.timestamp < cacheConfig.ttl) {
            if (cacheConfig.staleWhileRevalidate) {
                // 后台更新缓存
                this.updateCacheInBackground(url, options, cacheKey);
            }
            return cached.data;
        }

        // 发起请求
        const response = await fetch(url, options);
        const data = await response.json();

        // 更新缓存
        this.cache.set(cacheKey, {
            data,
            timestamp: Date.now(),
        });

        return data;
    }

    static async updateCacheInBackground(url, options, cacheKey) {
        // 在后台更新缓存
        setTimeout(async () => {
            try {
                const response = await fetch(url, options);
                const data = await response.json();

                this.cache.set(cacheKey, {
                    data,
                    timestamp: Date.now(),
                });
            } catch (error) {
                console.error("Background cache update failed:", error);
            }
        }, 0);
    }
}
```

### 数据压缩与优化

```jsx
// 1. 响应数据压缩
import pako from "pako";

class ResponseCompressor {
    static async compress(data) {
        const jsonString = JSON.stringify(data);
        const compressed = pako.deflate(jsonString);
        return compressed;
    }

    static async decompress(compressedData) {
        const decompressed = pako.inflate(compressedData, { to: "string" });
        return JSON.parse(decompressed);
    }
}

// 2. 增量更新
class IncrementalUpdate {
    static async getUpdates(sinceTimestamp) {
        const response = await api.get("/updates", {
            params: { since: sinceTimestamp },
            headers: {
                Accept: "application/json",
                "Accept-Encoding": "gzip, deflate",
            },
        });

        // 应用增量更新
        this.applyUpdates(response.data);
    }

    static applyUpdates(updates) {
        updates.forEach(update => {
            switch (update.type) {
                case "add":
                    this.addItem(update.data);
                    break;
                case "update":
                    this.updateItem(update.id, update.changes);
                    break;
                case "delete":
                    this.deleteItem(update.id);
                    break;
            }
        });
    }
}

// 3. 数据分页优化
class PaginatedDataLoader {
    constructor(options = {}) {
        this.pageSize = options.pageSize || 20;
        this.prefetchPages = options.prefetchPages || 2;
        this.cache = new Map();
    }

    async loadPage(page) {
        // 检查缓存
        if (this.cache.has(page)) {
            return this.cache.get(page);
        }

        // 加载当前页
        const currentPage = await this.fetchPage(page);
        this.cache.set(page, currentPage);

        // 预加载后续页面
        this.prefetchPagesAhead(page);

        return currentPage;
    }

    async prefetchPagesAhead(currentPage) {
        for (let i = 1; i <= this.prefetchPages; i++) {
            const nextPage = currentPage + i;

            if (!this.cache.has(nextPage)) {
                this.fetchPage(nextPage).then(data => {
                    this.cache.set(nextPage, data);
                });
            }
        }
    }

    async fetchPage(page) {
        const response = await api.get("/items", {
            params: {
                page,
                pageSize: this.pageSize,
                fields: "id,name,image,price", // 只请求必要字段
            },
        });

        return response.data;
    }
}
```

## 启动流程优化方案

### 渐进式启动

```jsx
// 1. 阶段化启动
class ProgressiveStartup {
    static phases = [
        { name: "native_init", priority: 0 },
        { name: "js_load", priority: 0 },
        { name: "core_init", priority: 0 },
        { name: "ui_render", priority: 1 },
        { name: "data_load", priority: 2 },
        { name: "services_init", priority: 3 },
    ];

    static async start() {
        // 阶段1: 核心初始化
        await this.phase1();

        // 阶段2: 显示UI
        await this.phase2();

        // 阶段3: 加载数据
        await this.phase3();

        // 阶段4: 初始化服务
        await this.phase4();
    }

    static async phase1() {
        // 初始化必要核心模块
        Performance.mark("phase1_start");

        await Promise.all([this.initNavigation(), this.initStorage(), this.initNetworking()]);

        Performance.mark("phase1_end");
    }

    static async phase2() {
        // 显示首屏UI
        Performance.mark("phase2_start");

        await this.renderInitialUI();

        // 标记首屏完成
        Performance.measure("firstPaint", "appLaunchStart", "phase2_end");

        Performance.mark("phase2_end");
    }

    static async phase3() {
        // 加载首屏数据（低优先级）
        requestIdleCallback(async () => {
            Performance.mark("phase3_start");

            await Promise.all([this.loadInitialData(), this.prefetchNextScreen()]);

            Performance.mark("phase3_end");
        });
    }

    static async phase4() {
        // 初始化非关键服务
        setTimeout(async () => {
            Performance.mark("phase4_start");

            await Promise.all([
                this.initAnalytics(),
                this.initCrashReporting(),
                this.initPushNotifications(),
            ]);

            Performance.mark("phase4_end");
            Performance.measure("fullStartup", "appLaunchStart", "phase4_end");
        }, 3000);
    }
}

// 2. 可交互时间优化
function optimizeTimeToInteractive() {
    // 延迟非关键任务
    const nonCriticalTasks = [() => initAnalytics(), () => initThirdPartySDKs(), () => loadAds()];

    // 在主线程空闲时执行
    if ("requestIdleCallback" in window) {
        requestIdleCallback(() => {
            nonCriticalTasks.forEach(task => task());
        });
    } else {
        setTimeout(() => {
            nonCriticalTasks.forEach(task => task());
        }, 5000);
    }

    // 优化首屏渲染
    const criticalTasks = [
        () => renderHeroSection(),
        () => loadUserProfile(),
        () => renderNavigation(),
    ];

    // 立即执行关键任务
    criticalTasks.forEach(task => task());
}
```

### 预热策略

```jsx
// 1. 应用预热
class AppWarmup {
    static async warmup() {
        if (Platform.OS === "android") {
            // Android 后台服务预热
            this.warmupAndroid();
        } else if (Platform.OS === "ios") {
            // iOS 后台任务预热
            this.warmupIOS();
        }

        // 通用预热
        await this.commonWarmup();
    }

    static warmupAndroid() {
        // 使用 JobScheduler 预加载
        const JobScheduler = NativeModules.JobScheduler;

        JobScheduler.schedule({
            jobId: 1,
            persist: true,
            requiredNetwork: 0, // 不需要网络
            requiresCharging: false,
            requiresDeviceIdle: true,
        });
    }

    static async commonWarmup() {
        // 预热常用数据
        const warmupData = [
            { key: "config", url: "/api/config" },
            { key: "user", url: "/api/user/profile" },
            { key: "products", url: "/api/products/hot" },
        ];

        // 后台预加载
        warmupData.forEach(async ({ key, url }) => {
            try {
                const data = await api.get(url);
                CacheManager.set(key, data);
            } catch (error) {
                console.warn(`预热 ${key} 失败:`, error);
            }
        });

        // 预加载字体
        await Font.loadAsync({
            Roboto: require("./assets/fonts/Roboto.ttf"),
        });

        // 预加载图片
        await Image.prefetch("https://example.com/logo.png");
    }
}

// 2. 下次启动预热
class NextLaunchWarmup {
    static async prepareForNextLaunch() {
        // 在应用关闭时准备下次启动
        AppState.addEventListener("change", async state => {
            if (state === "background") {
                await this.prefetchForNextLaunch();
            }
        });
    }

    static async prefetchForNextLaunch() {
        // 预测用户可能访问的页面
        const predictedPages = this.predictNextPages();

        // 预加载数据
        predictedPages.forEach(async page => {
            await this.prefetchPageData(page);
        });

        // 预加载 JS Bundle
        await this.prefetchNextBundle();
    }

    static predictNextPages() {
        // 基于用户行为预测
        const userHistory = this.getUserHistory();
        const currentTime = new Date().getHours();

        if (currentTime >= 9 && currentTime <= 18) {
            return ["home", "products", "cart"];
        } else {
            return ["home", "profile", "settings"];
        }
    }
}
```

## 监控与分析

### 性能监控

```js
// 1. 全面性能监控
class PerformanceMonitor {
    static metrics = {
        coldStart: null,
        warmStart: null,
        jsLoadTime: null,
        tti: null, // Time to Interactive
        fcp: null, // First Contentful Paint
        lcp: null, // Largest Contentful Paint
    };

    static startMonitoring() {
        // 监听各阶段
        this.setupPerformanceObservers();

        // 自定义指标
        this.setupCustomMetrics();

        // 错误监控
        this.setupErrorMonitoring();
    }

    static setupPerformanceObservers() {
        if (typeof PerformanceObserver === "undefined") return;

        // 资源加载监控
        const resourceObserver = new PerformanceObserver(list => {
            list.getEntries().forEach(entry => {
                if (entry.duration > 1000) {
                    console.warn("慢资源加载:", entry.name, entry.duration);
                }
            });
        });

        resourceObserver.observe({ entryTypes: ["resource"] });

        // 长任务监控
        const longTaskObserver = new PerformanceObserver(list => {
            list.getEntries().forEach(entry => {
                if (entry.duration > 50) {
                    // 超过50ms
                    console.warn("长任务:", entry);
                    this.reportLongTask(entry);
                }
            });
        });

        longTaskObserver.observe({ entryTypes: ["longtask"] });
    }

    static setupCustomMetrics() {
        // 首屏时间
        const fcpObserver = new PerformanceObserver(list => {
            const entries = list.getEntries();
            const fcp = entries[entries.length - 1];

            this.metrics.fcp = fcp.startTime;
            this.reportMetric("fcp", fcp.startTime);
        });

        fcpObserver.observe({ entryTypes: ["paint"] });

        // 可交互时间
        let ttiDetected = false;
        const ttiObserver = new PerformanceObserver(list => {
            if (ttiDetected) return;

            const quietPeriod = this.detectQuietPeriod();
            if (quietPeriod) {
                ttiDetected = true;
                this.metrics.tti = Date.now() - performance.timing.navigationStart;
                this.reportMetric("tti", this.metrics.tti);
            }
        });
    }

    static reportMetric(name, value) {
        // 上报到监控系统
        fetch("https://monitoring.example.com/metrics", {
            method: "POST",
            body: JSON.stringify({ name, value, timestamp: Date.now() }),
        });
    }
}

// 2. 启动性能分析
class StartupAnalyzer {
    static async analyzeStartup() {
        const report = {
            platform: Platform.OS,
            version: Platform.Version,
            device: DeviceInfo.getModel(),
            timestamp: Date.now(),
            metrics: {},
        };

        // 收集各阶段时间
        const entries = performance.getEntriesByType("measure");
        entries.forEach(entry => {
            report.metrics[entry.name] = entry.duration;
        });

        // 收集资源信息
        const resources = performance.getEntriesByType("resource");
        report.resources = resources.map(res => ({
            name: res.name,
            duration: res.duration,
            size: res.transferSize,
        }));

        // 分析瓶颈
        report.bottlenecks = this.findBottlenecks(report);

        // 上报分析结果
        await this.uploadReport(report);

        return report;
    }

    static findBottlenecks(report) {
        const bottlenecks = [];

        // JS Bundle 加载时间过长
        if (report.metrics.jsBundleLoad > 2000) {
            bottlenecks.push({
                type: "js_bundle",
                severity: "high",
                suggestion: "考虑代码分割或预加载",
            });
        }

        // 首屏渲染时间过长
        if (report.metrics.firstRender > 1000) {
            bottlenecks.push({
                type: "first_render",
                severity: "high",
                suggestion: "优化首屏组件，使用骨架屏",
            });
        }

        return bottlenecks;
    }
}
```

## 工具与自动化

### 自动化优化工具

```js
// package.json 优化脚本
{
  "scripts": {
    "start:optimized": "react-native start --max-workers 4 --reset-cache",
    "bundle:prod": "react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res --minify true --sourcemap-output android-release.bundle.map",
    "analyze:size": "source-map-explorer android-release.bundle.map",
    "profile:android": "react-native run-android --variant=release --no-packager",
    "profile:ios": "react-native run-ios --configuration Release",
    "optimize:images": "node scripts/optimize-images.js",
    "check:performance": "node scripts/performance-check.js",
    "lint:performance": "eslint --rule 'react/no-unstable-nested-components: error'"
  }
}

// scripts/performance-check.js
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

class PerformanceChecker {
  static async runChecks() {
    console.log('🚀 开始性能检查...\n');

    // 1. 检查 Bundle 大小
    await this.checkBundleSize();

    // 2. 检查图片资源
    await this.checkImages();

    // 3. 检查依赖
    await this.checkDependencies();

    // 4. 生成报告
    await this.generateReport();
  }

  static async checkBundleSize() {
    console.log('📦 检查 Bundle 大小...');

    const bundlePath = path.join(__dirname, '../android/app/build/outputs/bundle/release/app.bundle');

    if (fs.existsSync(bundlePath)) {
      const stats = fs.statSync(bundlePath);
      const sizeMB = stats.size / 1024 / 1024;

      console.log(`Bundle 大小: ${sizeMB.toFixed(2)}MB`);

      if (sizeMB > 10) {
        console.warn('⚠️  Bundle 过大，建议优化');
      }
    }
  }

  static async checkImages() {
    console.log('🖼️  检查图片资源...');

    const imagesDir = path.join(__dirname, '../src/assets/images');

    if (fs.existsSync(imagesDir)) {
      const images = fs.readdirSync(imagesDir);

      images.forEach(image => {
        const imagePath = path.join(imagesDir, image);
        const stats = fs.statSync(imagePath);

        if (stats.size > 500 * 1024) { // 大于500KB
          console.warn(`⚠️  图片过大: ${image} (${(stats.size / 1024).toFixed(2)}KB)`);
        }
      });
    }
  }
}

// 运行检查
PerformanceChecker.runChecks();
```

## 最佳实践总结

### 优化清单

```md
## ✅ 必须做的优化

### Native 层

-   [ ] 使用 Hermes 引擎
-   [ ] 配置启动图/主题
-   [ ] 启用 TurboModules
-   [ ] 预加载关键资源
-   [ ] 延迟非关键服务初始化

### JavaScript 层

-   [ ] 启用 inline requires
-   [ ] 代码分割和懒加载
-   [ ] 优化 Bundle 配置
-   [ ] 减少启动时同步操作
-   [ ] 使用骨架屏

### 渲染优化

-   [ ] 优化列表组件配置
-   [ ] 图片懒加载和预加载
-   [ ] 减少组件重新渲染
-   [ ] 使用合适的缓存策略

### 网络优化

-   [ ] 请求合并与批处理
-   [ ] 数据压缩
-   [ ] 连接复用
-   [ ] 离线缓存

## ⚡ 高级优化

### 启动流程

-   [ ] 渐进式启动
-   [ ] 预热策略
-   [ ] 预测性预加载
-   [ ] 后台初始化

### 监控分析

-   [ ] 性能监控埋点
-   [ ] 崩溃监控
-   [ ] 用户行为分析
-   [ ] A/B 测试

### 工具自动化

-   [ ] 自动化性能检查
-   [ ] CI/CD 集成
-   [ ] 性能回归测试
```

### 关键指标

```js
// 目标指标
const TARGET_METRICS = {
    // Android 冷启动
    androidColdStart: {
        good: "< 2000ms", // 优秀
        acceptable: "< 4000ms", // 可接受
        poor: "> 4000ms", // 需要优化
    },

    // iOS 冷启动
    iosColdStart: {
        good: "< 1500ms",
        acceptable: "< 3000ms",
        poor: "> 3000ms",
    },

    // JS Bundle 加载
    jsBundleLoad: {
        good: "< 1000ms",
        acceptable: "< 2000ms",
        poor: "> 2000ms",
    },

    // 首屏时间
    firstPaint: {
        good: "< 1500ms",
        acceptable: "< 2500ms",
        poor: "> 2500ms",
    },

    // 可交互时间
    timeToInteractive: {
        good: "< 3000ms",
        acceptable: "< 5000ms",
        poor: "> 5000ms",
    },

    // Bundle 大小
    bundleSize: {
        good: "< 5MB",
        acceptable: "< 10MB",
        poor: "> 10MB",
    },
};
```

### 持续优化流程

```js
// 性能优化工作流
class PerformanceWorkflow {
  static async run() {
    // 1. 测量
    const baseline = await this.measureBaseline();

    // 2. 分析
    const bottlenecks = this.analyze(baseline);

    // 3. 优化
    const improvements = await this.implementOptimizations(bottlenecks);

    // 4. 验证
    const results = await this.measureAfterOptimization();

    // 5. 监控
    this.setupContinuousMonitoring();

    return { baseline, bottlenecks, improvements, results };
  }

  static async measureBaseline() {
    // 在不同设备上测量启动性能
    const devices = ['low-end', 'mid-range', 'high-end'];
    const measurements = {};

    for (const device of devices) {
      measurements[device] = await this.measureOnDevice(device);
    }

    return measurements;
  }

  static analyze(measurements) {
    // 使用规则引擎分析瓶颈
    const rules = [
      {
        condition: (m) => m.jsBundleLoad > 2000,
        action: '优化 Bundle 大小',
        priority: 'high',
      },
      {
        condition: (m) => m.firstPaint > 2500,
        action: '优化首屏渲染',
        priority: 'high',
      },
      {
        condition: (m) => m.tti > 5000,
        action: '减少同步任务',
        priority: 'medium',
      },
    ];

    const bottlenecks = [];

    rules.forEach(rule => {
      Object.values(measurements).forEach(m => {
        if (rule.condition(m)) {
          bottlenecks.push({
            action: rule.action,
            priority: rule.priority,
            metric: m,
          });
        }
      });
    });

    return bottlenecks;
  }
}

// 集成到开发流程
// .github/workflows/performance.yml
name: Performance Check

on:
  pull_request:
    branches: [main]

jobs:
  performance:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2

      - name: Install dependencies
        run: npm ci

      - name: Check bundle size
        run: npm run analyze:size

      - name: Run performance tests
        run: npm run check:performance

      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: performance-report
          path: reports/performance.json
```

## 总结

React Native 应用启动速度优化是一个系统工程，需要从 Native 层、JavaScript 层、网络层、渲染层等多个维度进行优化。

### 核心优化策略

-   测量先行 - 使用工具准确测量各阶段耗时
-   瓶颈定位 - 找到影响启动的关键因素
-   分层优化 - 从 Native 到 JS 逐层优化
-   持续监控 - 建立性能监控和预警机制

### 关键优化点

-   Native 层：Hermes、TurboModules、预加载
-   Bundle 优化：代码分割、懒加载、Tree Shaking
-   渲染优化：骨架屏、列表优化、图片懒加载
-   网络优化：请求合并、缓存策略、数据压缩
-   内存管理：智能缓存、内存监控、泄漏预防

### 成功标准

-   冷启动时间 < 2 秒（高端设备）
-   热启动时间 < 1 秒
-   Bundle 大小 < 5MB
-   首屏渲染 < 1.5 秒
-   可交互时间 < 3 秒
