# 认识Gradle

Gradle 是一个现代化的开源构建自动化工具，专门用于：

- 自动化构建 Android 应用
- 依赖管理 第三方库
- 编译打包 APK/AAB 文件
- 任务编排 执行各种构建任务

## Gradle vs 其他构建工具

| 特性         | Gradle                 | Maven  | Ant        |
| ------------ | ---------------------- | ------ | ---------- |
| 构建脚本语言 | Groovy/Kotlin DSL      | XML    | XML        |
| 性能         | ⭐⭐⭐⭐⭐（增量构建） | ⭐⭐⭐ | ⭐⭐       |
| 灵活性       | ⭐⭐⭐⭐⭐             | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 学习曲线     | ⭐⭐⭐⭐               | ⭐⭐⭐ | ⭐⭐⭐⭐   |
| Android支持  | 官方首选               | 支持   | 已淘汰     |

## Android 项目中的 Gradle 文件

### 1. 文件结构概览
```text
项目根目录/
├── gradle/                    # Gradle包装器
│   └── wrapper/
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── build.gradle              # 项目级配置
├── settings.gradle           # 项目设置
├── gradlew                   # Unix启动脚本
├── gradlew.bat               # Windows启动脚本
└── app/                      # 模块目录
    └── build.gradle          # 模块级配置
```

### 2. 各文件作用说明

gradle-wrapper.properties - Gradle版本配置:
```properties
# 下载地址和版本配置
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-7.5-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

settings.gradle - 项目模块设置:
```gradle
// 包含哪些模块
include ':app'
include ':feature:home'      // 包含子模块
include ':library:network'

// 自定义仓库
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}
```

项目级 build.gradle - 全局配置:
```gradle
// Top-level build file
buildscript {
    ext {
        // 定义全局变量
        kotlin_version = '1.8.0'
        compileSdkVersion = 33
    }
    
    repositories {
        google()        // Google仓库
        mavenCentral()  // Maven中央仓库
    }
    
    dependencies {
        // Gradle插件
        classpath 'com.android.tools.build:gradle:7.4.0'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
}

// 所有模块通用配置
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

// 清理任务
task clean(type: Delete) {
    delete rootProject.buildDir
}
```

模块级 build.gradle - 模块具体配置:
```gradle
plugins {
    id 'com.android.application'  // Android应用插件
    id 'org.jetbrains.kotlin.android'  // Kotlin插件
}

android {
    namespace 'com.example.myapp'
    compileSdk 33  // 编译SDK版本
    
    defaultConfig {
        applicationId "com.example.myapp"
        minSdk 21      // 最低支持版本
        targetSdk 33   // 目标版本
        versionCode 1  // 版本号（数字）
        versionName "1.0"  // 版本名（字符串）
    }
    
    buildTypes {
        release {
            minifyEnabled true    // 开启代码混淆
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt')
        }
        debug {
            debuggable true
        }
    }
}

dependencies {
    // 依赖配置
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
}
```

## Gradle 核心概念

### 1. 依赖配置（Dependency Configurations）

```gradle
dependencies {
    // 1. implementation - 主代码依赖（推荐）
    implementation 'com.google.android.material:material:1.8.0'
    
    // 2. api - 暴露依赖给其他模块
    api 'com.squareup.retrofit2:retrofit:2.9.0'
    
    // 3. compileOnly - 仅编译时使用
    compileOnly 'org.projectlombok:lombok:1.18.24'
    
    // 4. runtimeOnly - 仅运行时使用
    runtimeOnly 'com.google.code.gson:gson:2.10'
    
    // 5. testImplementation - 测试代码依赖
    testImplementation 'junit:junit:4.13.2'
    
    // 6. androidTestImplementation - 仪器测试依赖
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
    
    // 7. kapt - Kotlin注解处理器
    kapt 'com.github.bumptech.glide:compiler:4.14.2'
    
    // 8. annotationProcessor - Java注解处理器
    annotationProcessor 'androidx.room:room-compiler:2.5.0'
}
```

### 2. 构建类型（Build Types）
```gradle
android {
    buildTypes {
        debug {
            // 调试版配置
            debuggable true
            minifyEnabled false
            applicationIdSuffix ".debug"
            versionNameSuffix "-DEBUG"
        }
        
        release {
            // 发布版配置
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt')
            signingConfig signingConfigs.release
        }
        
        // 自定义构建类型
        staging {
            initWith debug
            applicationIdSuffix ".staging"
            versionNameSuffix "-STAGING"
        }
    }
}
```

### 3. 产品风味（Product Flavors）
```gradle
android {
    flavorDimensions "version", "environment"
    
    productFlavors {
        free {
            dimension "version"
            applicationIdSuffix ".free"
            versionNameSuffix "-free"
        }
        
        paid {
            dimension "version"
            applicationIdSuffix ".paid"
            versionNameSuffix "-paid"
        }
        
        dev {
            dimension "environment"
            applicationIdSuffix ".dev"
            buildConfigField "String", "API_URL", '"https://dev.api.com"'
        }
        
        prod {
            dimension "environment"
            buildConfigField "String", "API_URL", '"https://api.com"'
        }
    }
}
```

### 4. 构建变体（Build Variants）
```text
构建变体 = 产品风味 × 构建类型

示例：
- freeDevDebug
- freeDevRelease
- paidProdDebug
- paidProdRelease
```

## 常用 Gradle 命令

基本命令：
```bash
# 查看所有任务
./gradlew tasks

# 清理构建
./gradlew clean

# 构建项目
./gradlew build

# 只编译不打包
./gradlew assemble

# 安装应用到设备
./gradlew installDebug
```

测试相关：
```bash
# 运行单元测试
./gradlew test

# 运行Android测试
./gradlew connectedAndroidTest

# 运行特定测试类
./gradlew test --tests "*ExampleUnitTest"
```

依赖管理：
```bash
# 查看依赖树
./gradlew app:dependencies

# 查看特定配置的依赖
./gradlew app:dependencies --configuration implementation

# 刷新依赖缓存
./gradlew --refresh-dependencies
```

分析和检查:
```bash
# Lint代码检查
./gradlew lint

# 检查依赖更新
./gradlew dependencyUpdates

# 分析APK大小
./gradlew analyzeDebugApk
```

## 依赖管理详解

### 1. 依赖格式
```gradle
dependencies {
    // 格式：group:name:version
    implementation 'androidx.appcompat:appcompat:1.6.1'
    //      ↑           ↑        ↑         ↑
    // 配置名称       组织名    模块名     版本号
}
```

### 2. 版本控制方式

```gradle
implementation 'com.squareup.retrofit2:retrofit:2.9.0'      // 固定版本
implementation 'com.squareup.okhttp3:okhttp:4.+'           // 4.x最新版
implementation 'androidx.core:core-ktx:[1.6.0,1.9.0]'      // 版本范围
implementation 'androidx.activity:activity-ktx:1.7.0-alpha02' // 预览版
```

### 3. 本地依赖
```gradle
dependencies {
    // 本地jar文件
    implementation files('libs/my-library.jar')
    implementation fileTree(dir: 'libs', include: ['*.jar'])
    
    // 本地aar文件
    implementation files('libs/my-library.aar')
    
    // 本地模块依赖
    implementation project(':library:network')
    implementation project(path: ':feature:home')
}
```

## 高级配置示例

### 1. 签名配置
```gradle
android {
    signingConfigs {
        debug {
            storeFile file('debug.keystore')
            storePassword 'android'
            keyAlias 'androiddebugkey'
            keyPassword 'android'
        }
        
        release {
            storeFile file('release.keystore')
            storePassword System.getenv('STORE_PASSWORD')
            keyAlias System.getenv('KEY_ALIAS')
            keyPassword System.getenv('KEY_PASSWORD')
        }
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

### 2. 多渠道打包
```gradle
android {
    // 动态配置应用名称和图标
    productFlavors {
        googleplay {
            manifestPlaceholders = [
                app_name: "@string/app_name_google",
                app_icon: "@mipmap/ic_launcher_google"
            ]
        }
        
        huawei {
            manifestPlaceholders = [
                app_name: "@string/app_name_huawei",
                app_icon: "@mipmap/ic_launcher_huawei"
            ]
        }
    }
}
```

### 3. 构建优化
```gradle
android {
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }
    
    kotlinOptions {
        jvmTarget = '11'
        freeCompilerArgs += ['-Xopt-in=kotlin.RequiresOptIn']
    }
    
    buildFeatures {
        viewBinding true
        dataBinding true
        compose true
    }
    
    // 启用资源缩减
    buildTypes {
        release {
            crunchPngs true  // 压缩PNG
            shrinkResources true  // 移除未使用资源
        }
    }
}
```

## Gradle 构建生命周期

```text
初始化阶段（Initialization）
     ↓
配置阶段（Configuration）
     ↓
执行阶段（Execution）
```

生命周期示例:
```text
// 初始化脚本
settings.gradle
     ↓
// 配置阶段（解析所有build.gradle）
println '配置阶段开始'
     ↓
// 任务图生成
     ↓
// 执行阶段
task myTask {
    doFirst {
        println '任务执行 - doFirst'
    }
    
    doLast {
        println '任务执行 - doLast'
    }
}
```