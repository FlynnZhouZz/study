# RN 开发过程中，有遇到什么棘手的问题？你是如何解决的？

## 1. 内存泄漏和性能问题

### 问题现象：

-   App 运行时间越长越卡顿
-   列表滚动卡顿，特别是图片多时
-   应用偶尔崩溃，日志显示 OOM

### 解决方案：

```jsx
import React, { useState, useCallback, useMemo, memo } from "react";
import { FlatList, View, Text, Image } from "react-native";
import FastImage from "react-native-fast-image";

// 使用 memo 包装列表项
const ListItem = memo(({ item }) => {
    return (
        <View style={styles.item}>
            <FastImage
                source={{ uri: item.image }}
                style={styles.image}
                resizeMode={FastImage.resizeMode.cover}
            />
            <Text>{item.title}</Text>
        </View>
    );
});

// 使用 useCallback 优化函数
const OptimizedList = ({ data }) => {
    const [visibleItems, setVisibleItems] = useState([]);

    // 使用 useCallback 避免每次渲染创建新函数
    const handleViewableItemsChanged = useCallback(({ viewableItems }) => {
        setVisibleItems(viewableItems.map(item => item.key));
    }, []);

    const viewabilityConfig = useMemo(
        () => ({
            itemVisiblePercentThreshold: 50,
        }),
        []
    );

    // 使用 useMemo 缓存计算结果
    const getItemLayout = useCallback(
        (_, index) => ({
            length: 100,
            offset: 100 * index,
            index,
        }),
        []
    );

    // 优化图片渲染
    const renderItem = useCallback(({ item }) => <ListItem item={item} />, []);

    return (
        <FlatList
            data={data}
            renderItem={renderItem}
            keyExtractor={item => item.id}
            initialNumToRender={10}
            maxToRenderPerBatch={5}
            windowSize={21}
            getItemLayout={getItemLayout}
            onViewableItemsChanged={handleViewableItemsChanged}
            viewabilityConfig={viewabilityConfig}
            removeClippedSubviews={true}
        />
    );
};

// 使用 InteractionManager 延迟非紧急任务
const HeavyComponent = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const task = InteractionManager.runAfterInteractions(() => {
            // 延迟执行耗时操作
            loadHeavyData().then(setData);
        });

        return () => task.cancel();
    }, []);

    return data ? <RenderData data={data} /> : <Loading />;
};
```

## 2. 原生模块兼容性问题

问题： iOS 和 Android 原生模块行为不一致

解决方案：

```jsx
/import React, { useEffect, useState } from 'react';
import { Platform, NativeModules } from 'react-native';

// 自定义 Hook 处理平台差异
const useDeviceInfo = () => {
  const [deviceInfo, setDeviceInfo] = useState({});

  useEffect(() => {
    const fetchDeviceInfo = async () => {
      if (Platform.OS === 'ios') {
        const info = await NativeModules.IOSDeviceModule.getInfo();
        setDeviceInfo({
          model: info.model,
          osVersion: info.systemVersion,
        });
      } else {
        const info = await NativeModules.AndroidDeviceModule.getInfo();
        setDeviceInfo({
          model: info.model,
          osVersion: info.version,
          manufacturer: info.manufacturer,
        });
      }
    };

    fetchDeviceInfo();
  }, []);

  return deviceInfo;
};

// 使用 Hook 的组件
const DeviceInfoDisplay = () => {
  const deviceInfo = useDeviceInfo();

  return (
    <View>
      <Text>Model: {deviceInfo.model}</Text>
      <Text>OS: {deviceInfo.osVersion}</Text>
    </View>
  );
};

// 带降级的原生模块 Hook
const useNativeCamera = () => {
  const [cameraAvailable, setCameraAvailable] = useState(true);

  const takePhoto = useCallback(async () => {
    try {
      if (cameraAvailable) {
        return await NativeModules.CameraModule.takePhoto();
      } else {
        return await takePhotoWithFallback();
      }
    } catch (error) {
      setCameraAvailable(false);
      return await takePhotoWithFallback();
    }
  }, [cameraAvailable]);

  return { takePhoto, cameraAvailable };
};
```

## 3. 热更新和版本管理

问题： CodePush 热更新后数据格式不兼容

解决方案：

```jsx
import React, { useEffect } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import CodePush from "react-native-code-push";

// 数据迁移 Hook
const useDataMigration = () => {
    useEffect(() => {
        const migrateData = async () => {
            const currentVersion = await AsyncStorage.getItem("app_version");
            const newVersion = "2.0.0";

            if (!currentVersion) {
                // 首次安装
                await initializeDefaultData();
            } else if (currentVersion < "1.5.0") {
                await migrateFromV1ToV2();
            }

            await AsyncStorage.setItem("app_version", newVersion);
        };

        migrateData();
    }, []);
};

// 组件中使用
const App = () => {
    useDataMigration();

    // CodePush 配置
    const [updateAvailable, setUpdateAvailable] = useState(false);

    useEffect(() => {
        checkForUpdates();
    }, []);

    const checkForUpdates = async () => {
        const update = await CodePush.checkForUpdate();
        setUpdateAvailable(!!update);
    };

    return (
        <View>{updateAvailable && <Button title="更新" onPress={() => CodePush.sync()} />}</View>
    );
};
```

## 4. 导航栈管理复杂

问题： 深层嵌套路由状态丢失

解决方案：

```jsx
import React, { useRef, useEffect } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import AsyncStorage from "@react-native-async-storage/async-storage";

const Stack = createStackNavigator();

// 自定义 Hook 管理导航状态
const useNavigationPersistence = () => {
    const [isReady, setIsReady] = useState(false);
    const [initialState, setInitialState] = useState();

    useEffect(() => {
        const restoreState = async () => {
            try {
                const savedStateString = await AsyncStorage.getItem("NAVIGATION_STATE");
                const state = savedStateString ? JSON.parse(savedStateString) : undefined;

                if (state !== undefined) {
                    setInitialState(state);
                }
            } finally {
                setIsReady(true);
            }
        };

        if (!isReady) {
            restoreState();
        }
    }, [isReady]);

    const onStateChange = useCallback(state => {
        AsyncStorage.setItem("NAVIGATION_STATE", JSON.stringify(state));
    }, []);

    return { isReady, initialState, onStateChange };
};

// 使用 Hook 的导航容器
const AppNavigator = () => {
    const { isReady, initialState, onStateChange } = useNavigationPersistence();

    if (!isReady) {
        return <LoadingScreen />;
    }

    return (
        <NavigationContainer initialState={initialState} onStateChange={onStateChange}>
            <Stack.Navigator>
                <Stack.Screen name="Home" component={HomeScreen} />
                <Stack.Screen name="Details" component={DetailsScreen} />
            </Stack.Navigator>
        </NavigationContainer>
    );
};
```

## 5. 动画性能问题

问题： 复杂动画卡顿，特别是 Android 上

解决方案：

```jsx
import React, { useRef } from "react";
import { Animated, Pressable } from "react-native";
import Lottie from "lottie-react-native";
import Animated, {
    useSharedValue,
    useAnimatedStyle,
    withSpring,
    withTiming,
} from "react-native-reanimated";

// 使用原生驱动的 Animated
const NativeDrivenAnimation = () => {
    const fadeAnim = useRef(new Animated.Value(0)).current;

    const fadeIn = () => {
        Animated.timing(fadeAnim, {
            toValue: 1,
            duration: 1000,
            useNativeDriver: true, // 关键：启用原生驱动
        }).start();
    };

    return (
        <Animated.View style={{ opacity: fadeAnim }}>
            <Pressable onPress={fadeIn}>
                <Text>Fade In</Text>
            </Pressable>
        </Animated.View>
    );
};

// 使用 Reanimated 2
const ReanimatedComponent = () => {
    const translateX = useSharedValue(0);

    const animatedStyle = useAnimatedStyle(() => ({
        transform: [{ translateX: translateX.value }],
    }));

    const handlePress = () => {
        translateX.value = withSpring(Math.random() * 100);
    };

    return (
        <Pressable onPress={handlePress}>
            <Animated.View style={[styles.box, animatedStyle]} />
        </Pressable>
    );
};

// Lottie 动画
const LottieAnimation = () => {
    const animationRef = useRef(null);

    useEffect(() => {
        if (animationRef.current) {
            animationRef.current.play();
        }
    }, []);

    return (
        <Lottie
            ref={animationRef}
            source={require("./animation.json")}
            autoPlay
            loop
            hardwareAccelerationAndroid
        />
    );
};
```

## 6. 多分辨率适配

问题： 不同屏幕尺寸显示不一致

解决方案：

```jsx
import React from "react";
import { Dimensions, StyleSheet, View, useWindowDimensions } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

// 响应式 Hook
const useResponsive = () => {
    const { width, height } = useWindowDimensions();

    const guidelineBaseWidth = 390;
    const guidelineBaseHeight = 844;

    const scale = size => (width / guidelineBaseWidth) * size;
    const verticalScale = size => (height / guidelineBaseHeight) * size;
    const moderateScale = (size, factor = 0.5) => size + (scale(size) - size) * factor;

    return { scale, verticalScale, moderateScale };
};

// 使用 Hook 的组件
const ResponsiveComponent = () => {
    const { moderateScale, verticalScale } = useResponsive();
    const insets = useSafeAreaInsets();

    return (
        <View
            style={{
                paddingTop: insets.top + verticalScale(20),
                paddingHorizontal: moderateScale(15),
            }}
        >
            <View
                style={{
                    width: moderateScale(100),
                    height: moderateScale(100),
                    marginBottom: verticalScale(10),
                }}
            />
        </View>
    );
};

// 或使用 StyleSheet
const createStyles = () => {
    const { width, height } = Dimensions.get("window");

    return StyleSheet.create({
        container: {
            paddingHorizontal: width * 0.05,
            paddingVertical: height * 0.02,
        },
        card: {
            width: width * 0.9,
            height: height * 0.2,
        },
    });
};
```

## 7. 第三方库冲突

问题： 多个库依赖不同版本的 React Native

解决方案：

```jsx
import React, { useState, useEffect } from "react";

// 动态导入 Hook
const useDynamicImport = (moduleName, fallback) => {
    const [module, setModule] = useState(null);

    useEffect(() => {
        let isMounted = true;

        const loadModule = async () => {
            try {
                const imported = await import(moduleName);
                if (isMounted) {
                    setModule(imported.default || imported);
                }
            } catch (error) {
                console.warn(`无法加载 ${moduleName}:`, error);
                if (isMounted && fallback) {
                    setModule(fallback);
                }
            }
        };

        loadModule();

        return () => {
            isMounted = false;
        };
    }, [moduleName, fallback]);

    return module;
};

// 使用示例
const ComponentWithOptionalLibrary = () => {
    const FancyChart = useDynamicImport(
        "react-native-fancy-charts",
        SimpleChart // 备用组件
    );

    if (!FancyChart) {
        return <Loading />;
    }

    return <FancyChart data={chartData} />;
};

// 条件渲染 Hook
const useConditionalFeature = (featureName, dependencies = []) => {
    const [isAvailable, setIsAvailable] = useState(false);

    useEffect(() => {
        const checkAvailability = async () => {
            try {
                await NativeModules[featureName].check();
                setIsAvailable(true);
            } catch {
                setIsAvailable(false);
            }
        };

        checkAvailability();
    }, dependencies);

    return isAvailable;
};
```

## 8. 调试困难

问题： 生产环境 bug 难以复现

解决方案：

```jsx
import React, { useEffect } from "react";
import { Alert, Platform } from "react-native";

// 错误边界 Hook（React 18+）
const useErrorHandler = errorCallback => {
    const [error, setError] = useState(null);

    useEffect(() => {
        const errorHandler = (error, errorInfo) => {
            setError(error);
            errorCallback?.(error, errorInfo);

            // 生产环境上报
            if (!__DEV__) {
                reportError(error);
            }
        };

        // 全局错误捕获
        ErrorUtils.setGlobalHandler(errorHandler);

        return () => {
            ErrorUtils.setGlobalHandler(null);
        };
    }, [errorCallback]);

    return { error, clearError: () => setError(null) };
};

// 使用示例
const AppWithErrorHandling = () => {
    const { error, clearError } = useErrorHandler((error, errorInfo) => {
        console.error("捕获错误:", error, errorInfo);
    });

    if (error) {
        return (
            <View>
                <Text>出错了</Text>
                <Button title="重试" onPress={clearError} />
            </View>
        );
    }

    return <MainApp />;
};

// 性能监控 Hook
const usePerformanceMonitor = () => {
    useEffect(() => {
        if (__DEV__) {
            const monitor = require("react-native-performance-monitor");
            monitor.start({
                captureScreenshots: true,
                logLevel: "debug",
            });

            return () => monitor.stop();
        }
    }, []);
};

// 在根组件使用
const App = () => {
    usePerformanceMonitor();
    return <AppWithErrorHandling />;
};
```

## 9. 打包和发布问题

问题： 包体积过大，启动速度慢

解决方案：

```jsx
import React, { lazy, Suspense } from "react";
import { View, ActivityIndicator } from "react-native";

// 代码分割
const HeavyComponent = lazy(() => import("./HeavyComponent"));

const OptimizedScreen = () => {
    return (
        <View>
            <Suspense fallback={<ActivityIndicator />}>
                <HeavyComponent />
            </Suspense>
        </View>
    );
};

// 按需加载 Hook
const useLazyComponent = (importFn, fallback = null) => {
    const [Component, setComponent] = useState(() => fallback);

    useEffect(() => {
        importFn().then(module => {
            setComponent(() => module.default || module);
        });
    }, [importFn]);

    return Component;
};

// 使用示例
const LazyComponent = () => {
    const ChartComponent = useLazyComponent(
        () => import("./ChartComponent"),
        () => <SimpleChart />
    );

    return <ChartComponent data={data} />;
};
```

## 10. 状态管理混乱

问题： 状态分散，难以维护

解决方案：

```jsx
import React, { useCallback } from "react";
import { useSelector, useDispatch } from "react-redux";
import { createSlice, configureStore } from "@reduxjs/toolkit";
import { useDispatch, useSelector, Provider } from "react-redux";
import {
    persistStore,
    persistReducer,
    FLUSH,
    REHYDRATE,
    PAUSE,
    PERSIST,
    PURGE,
    REGISTER,
} from "redux-persist";
import AsyncStorage from "@react-native-async-storage/async-storage";

// 创建 slice
const authSlice = createSlice({
    name: "auth",
    initialState: {
        user: null,
        token: null,
        isLoading: false,
    },
    reducers: {
        setUser: (state, action) => {
            state.user = action.payload;
        },
        setToken: (state, action) => {
            state.token = action.payload;
        },
        setLoading: (state, action) => {
            state.isLoading = action.payload;
        },
    },
});

// 自定义 Hook
const useAuth = () => {
    const dispatch = useDispatch();
    const { user, token, isLoading } = useSelector(state => state.auth);

    const login = useCallback(
        async credentials => {
            dispatch(authSlice.actions.setLoading(true));
            try {
                const response = await api.login(credentials);
                dispatch(authSlice.actions.setUser(response.user));
                dispatch(authSlice.actions.setToken(response.token));
            } finally {
                dispatch(authSlice.actions.setLoading(false));
            }
        },
        [dispatch]
    );

    const logout = useCallback(() => {
        dispatch(authSlice.actions.setUser(null));
        dispatch(authSlice.actions.setToken(null));
    }, [dispatch]);

    return {
        user,
        token,
        isLoading,
        login,
        logout,
    };
};

// 组件中使用
const LoginScreen = () => {
    const { login, isLoading } = useAuth();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async () => {
        await login({ email, password });
    };

    return (
        <View>
            <TextInput value={email} onChangeText={setEmail} />
            <TextInput value={password} onChangeText={setPassword} secureTextEntry />
            <Button
                title={isLoading ? "登录中..." : "登录"}
                onPress={handleLogin}
                disabled={isLoading}
            />
        </View>
    );
};
```

## 问题排查清单

遇到问题时，按此顺序排查：

### 1. 检查环境

```bash
npx react-native info
npx pod-install # iOS
./gradlew clean # Android
```

### 2. 清除缓存

```bash
watchman watch-del-all
rm -rf node_modules
rm -rf ios/Pods
npm cache clean --force
```

### 3. 最小化复现

```bash
npx react-native init TestApp --template react-native-template-typescript
# 逐步添加依赖，找到冲突点
```

### 4. 查看原生日志

```bash
# iOS
npx react-native log-ios

# Android
npx react-native log-android
```

## 经验总结

-   保持 RN 版本稳定 - 不盲目升级
-   测试覆盖要全面 - 特别是原生模块
-   监控不能少 - 集成 APM 工具
-   文档很重要 - 团队统一解决方案
-   备用方案必须有 - 关键功能要有降级策略
