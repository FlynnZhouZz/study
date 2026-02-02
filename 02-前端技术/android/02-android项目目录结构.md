# Android项目目录结构

## 整体结构

```text
MyApplication/                    # 项目根目录
├── app/                         # 主模块（主要开发目录）
├── gradle/                      # Gradle包装器文件
├── .gradle/                     # Gradle缓存（自动生成）
├── .idea/                       # IDE配置（自动生成）
├── build/                       # 构建输出（自动生成）
├── gradle/                      # Gradle相关
├── gradlew                      # Gradle包装器脚本（Unix）
├── gradlew.bat                  # Gradle包装器脚本（Windows）
├── build.gradle                 # 项目级构建配置
├── settings.gradle              # 项目设置文件
├── local.properties             # 本地环境配置（自动生成）
└── README.md                    # 项目说明文档
```

## 主模块（app/）详细结构

```text
app/
├── manifests/                   # Android清单文件
│   └── AndroidManifest.xml     # 应用配置清单
├── java/                       # Java/Kotlin源代码
│   ├── com.example.myapp/      # 包名目录
│   │   ├── MainActivity.kt     # 主Activity
│   │   ├── ui/                 # 界面相关
│   │   │   ├── fragments/      # Fragment类
│   │   │   ├── activities/     # Activity类
│   │   │   └── adapters/       # 适配器类
│   │   ├── data/               # 数据层
│   │   │   ├── models/         # 数据模型
│   │   │   ├── repositories/   # 数据仓库
│   │   │   └── databases/      # 数据库相关
│   │   ├── network/            # 网络相关
│   │   ├── utils/              # 工具类
│   │   └── di/                 # 依赖注入
│   └── (androidTest)           # Android测试代码
├── res/                        # 资源文件目录
│   ├── drawable/               # 图片资源（PNG、JPEG、WebP）
│   │   ├── ic_launcher.png     # 应用图标
│   │   ├── background.xml      # 背景选择器
│   │   └── vector/             # 矢量图形目录
│   ├── layout/                 # 布局文件
│   │   ├── activity_main.xml   # 主Activity布局
│   │   ├── item_list.xml       # 列表项布局
│   │   └── fragment_home.xml   # Fragment布局
│   ├── mipmap/                 # 应用图标（不同分辨率）
│   │   ├── ic_launcher.png     # 默认图标
│   │   ├── ic_launcher_round.png # 圆形图标
│   │   └── (hdpi, xhdpi, etc.)/ # 不同密度
│   ├── values/                 # 数值资源
│   │   ├── colors.xml          # 颜色定义
│   │   ├── strings.xml         # 字符串资源
│   │   ├── styles.xml          # 样式定义
│   │   ├── dimens.xml          # 尺寸定义
│   │   ├── themes.xml          # 主题定义
│   │   └── arrays.xml          # 数组定义
│   ├── anim/                   # 动画资源
│   │   ├── fade_in.xml         # 淡入动画
│   │   └── slide_up.xml        # 上滑动画
│   ├── menu/                   # 菜单资源
│   │   └── main_menu.xml       # 主菜单
│   ├── font/                   # 字体资源
│   │   └── roboto.ttf          # 自定义字体
│   ├── raw/                    # 原始资源文件
│   │   └── audio.mp3           # 音频文件
│   └── xml/                    # 其他XML配置
│       └── network_security_config.xml # 网络安全配置
├── assets/                     # 原始资源目录
│   ├── html/                   # HTML文件
│   ├── json/                   # JSON数据文件
│   └── fonts/                  # 字体文件（另一种方式）
├── (test)                      # 单元测试代码
├── build.gradle                # 模块级构建配置
└── proguard-rules.pro          # 混淆规则文件
```

## 关键文件详解

### 1. AndroidManifest.xml - 应用清单文件

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myapp">

    <!-- 应用权限声明 -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <!-- 应用配置 -->
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/AppTheme">

        <!-- Activity声明 -->
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Service声明 -->
        <service android:name=".MyService" />

        <!-- Broadcast Receiver声明 -->
        <receiver android:name=".MyReceiver" />
    </application>
</manifest>
```

### 2. build.gradle - 构建配置

```gradle
// 项目级 build.gradle
buildscript {
    ext {
        kotlin_version = '1.8.0'
        compileSdkVersion = 33
        minSdkVersion = 21
        targetSdkVersion = 33
    }

    repositories {
        google()
        mavenCentral()
    }

    dependencies {
        classpath 'com.android.tools.build:gradle:7.4.0'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
```

```gradle
// 模块级 build.gradle (app/build.gradle)
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'kotlin-kapt'  // Kotlin注解处理
}

android {
    namespace 'com.example.myapp'
    compileSdk 33

    defaultConfig {
        applicationId "com.example.myapp"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled true      // 开启混淆
            shrinkResources true    // 缩减资源
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
        debug {
            debuggable true
            applicationIdSuffix ".debug"  // 调试版后缀
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }

    kotlinOptions {
        jvmTarget = '11'
    }

    buildFeatures {
        viewBinding true      // 启用ViewBinding
        dataBinding true      // 启用DataBinding
        compose true          // 启用Jetpack Compose
    }
}

dependencies {
    // Kotlin
    implementation "org.jetbrains.kotlin:kotlin-stdlib:$kotlin_version"
    implementation 'androidx.core:core-ktx:1.9.0'

    // UI
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'

    // Architecture Components
    implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.0'
    implementation 'androidx.lifecycle:lifecycle-livedata-ktx:2.6.0'

    // Navigation
    implementation 'androidx.navigation:navigation-fragment-ktx:2.5.3'
    implementation 'androidx.navigation:navigation-ui-ktx:2.5.3'

    // Network
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.10.0'

    // Image Loading
    implementation 'com.github.bumptech.glide:glide:4.14.2'

    // Database
    implementation 'androidx.room:room-runtime:2.5.0'
    kapt 'androidx.room:room-compiler:2.5.0'

    // Test
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
```

### 3. 资源文件详解

colors.xml - 颜色定义:

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- 主色调 -->
    <color name="colorPrimary">#3F51B5</color>
    <color name="colorPrimaryDark">#303F9F</color>
    <color name="colorAccent">#FF4081</color>

    <!-- 文本颜色 -->
    <color name="text_primary">#212121</color>
    <color name="text_secondary">#757575</color>

    <!-- 背景色 -->
    <color name="background">#FFFFFF</color>
    <color name="surface">#F5F5F5</color>

    <!-- 语义颜色 -->
    <color name="success">#4CAF50</color>
    <color name="warning">#FF9800</color>
    <color name="error">#F44336</color>
</resources>
```

strings.xml - 字符串资源:

```xml
<resources>
    <!-- 应用名称 -->
    <string name="app_name">我的应用</string>

    <!-- 界面文本 -->
    <string name="welcome_message">欢迎使用！</string>
    <string name="login">登录</string>
    <string name="register">注册</string>

    <!-- 格式化字符串 -->
    <string name="welcome_user">你好，%1$s！</string>
    <string name="item_count">共 %d 个项目</string>

    <!-- 复数形式 -->
    <plurals name="item_plural">
        <item quantity="one">%d 个项目</item>
        <item quantity="other">%d 个项目</item>
    </plurals>
</resources>
```

styles.xml - 样式定义:

```xml
<resources>
    <!-- 基础主题 -->
    <style name="Theme.MyApplication" parent="Theme.MaterialComponents.DayNight.DarkActionBar">
        <item name="colorPrimary">@color/colorPrimary</item>
        <item name="colorPrimaryVariant">@color/colorPrimaryDark</item>
        <item name="colorOnPrimary">@android:color/white</item>

        <!-- 状态栏 -->
        <item name="android:statusBarColor" tools:targetApi="l">?attr/colorPrimaryVariant</item>

        <!-- 字体 -->
        <item name="android:fontFamily">@font/roboto</item>
    </style>

    <!-- 自定义Widget样式 -->
    <style name="Widget.MyApplication.Button" parent="Widget.MaterialComponents.Button">
        <item name="android:textSize">16sp</item>
        <item name="android:textColor">@android:color/white</item>
        <item name="cornerRadius">8dp</item>
    </style>

    <!-- 无ActionBar主题 -->
    <style name="Theme.MyApplication.NoActionBar">
        <item name="windowActionBar">false</item>
        <item name="windowNoTitle">true</item>
    </style>
</resources>
```

dimens.xml - 尺寸定义:

```xml
<resources>
    <!-- 通用尺寸 -->
    <dimen name="spacing_small">8dp</dimen>
    <dimen name="spacing_medium">16dp</dimen>
    <dimen name="spacing_large">24dp</dimen>

    <!-- 组件尺寸 -->
    <dimen name="button_height">48dp</dimen>
    <dimen name="button_corner_radius">4dp</dimen>

    <!-- 文本尺寸 -->
    <dimen name="text_size_small">12sp</dimen>
    <dimen name="text_size_medium">14sp</dimen>
    <dimen name="text_size_large">18sp</dimen>

    <!-- 图标尺寸 -->
    <dimen name="icon_size_small">24dp</dimen>
    <dimen name="icon_size_medium">32dp</dimen>
</resources>
```

## 代码包结构最佳实践

```text
com.example.myapp/
├── activities/                  # 所有Activity
├── fragments/                   # 所有Fragment
├── adapters/                    # 所有适配器
├── viewmodels/                  # 所有ViewModel
├── models/                      # 所有数据模型
├── repositories/                # 所有仓库
├── services/                    # 所有Service
├── utils/                       # 工具类
│   ├── extensions/              # 扩展函数
│   ├── helpers/                 # 辅助类
│   └── constants/               # 常量定义
└── interfaces/                  # 接口定义
```

## 资源文件命名规范

### 1. 布局文件命名

```text
activity_<模块名>.xml         # Activity布局
fragment_<模块名>.xml        # Fragment布局
item_<列表项类型>.xml        # 列表项布局
dialog_<对话框类型>.xml      # 对话框布局
layout_<组件名>.xml          # 公共布局组件
```

### 2. 图片资源命名

```text
ic_<用途>_<颜色>_<尺寸>.png   # 图标
bg_<用途>_<状态>.png         # 背景
img_<内容描述>.png           # 图片
vector_<图标名>.xml          # 矢量图标
```

### 3. 可绘制资源命名

```text
shape_<形状>_<颜色>.xml      # 形状
selector_<状态>.xml          # 状态选择器
layer_<层次>.xml             # 图层列表
```

## 配置文件说明

### 1. settings.gradle - 项目设置

```gradle
// 包含的模块
include ':app'
include ':library'          // 如果有库模块

// 自定义构建缓存位置
buildCache {
    local {
        directory = new File(rootDir, 'build-cache')
        removeUnusedEntriesAfterDays = 30
    }
}
```

### 2. local.properties - 本地配置

```properties
# SDK路径
sdk.dir=/Users/username/Library/Android/sdk
# NDK路径（如果需要）
ndk.dir=/Users/username/Library/Android/sdk/ndk/25.1.8937393
# CMake路径
cmake.dir=/Users/username/Library/Android/sdk/cmake/3.22.1
```

### 3. gradle.properties - Gradle配置

```properties
# 内存设置
org.gradle.jvmargs=-Xmx4096m -XX:MaxMetaspaceSize=1024m

# 并行构建
org.gradle.parallel=true
org.gradle.daemon=true

# 配置缓存
org.gradle.configurationcache=true

# 国内镜像（加速）
systemProp.http.proxyHost=mirrors.aliyun.com
systemProp.http.proxyPort=80
```
