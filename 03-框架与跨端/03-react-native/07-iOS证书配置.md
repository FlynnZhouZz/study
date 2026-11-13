# RN如何生成/配置iOS的开发者证书和生产证书

## 准备工作
- Apple 开发者账号（年费 $99）
- Mac 电脑（必须使用 Xcode）
- React Native 项目（已初始化 iOS 目录）

## 生成证书的完整流程

### 1、创建 App ID

- 登录 [Apple Developer 后台](https://developer.apple.com)
- 进入 Certificates, Identifiers & Profiles
- 选择 Identifiers > App IDs，点击 + 创建：
    Description：填写应用描述（如 MyApp Prod）
    Bundle ID：必须与 Xcode 中的 Bundle Identifier 完全一致（如 com.company.appname）
    勾选所需能力（如 Push Notifications）

> 需管理员和所属者权限

### 2、生成证书签名请求（CSR）

在 Mac 上生成 CSR 文件：

- 打开 钥匙串访问（Keychain Access）
- 顶部菜单选择 钥匙串访问 > 证书助理 > 从证书颁发机构请求证书...
- 填写信息：
    用户电子邮件：开发者账号邮箱
    常用名称：建议写你的名字（如 John Doe）
    选择 保存到磁盘，生成 .certSigningRequest 文件

### 3、创建开发证书（Development）

- 在 Apple Developer 后台进入 Certificates > +
- 选择 iOS App Development > 继续
- 上传刚才生成的 .certSigningRequest 文件
- 生成后下载证书（.cer 文件），双击安装到钥匙串

### 4、创建生产证书（Distribution）

- 同上步骤，但选择 Apple Distribution（用于 App Store 或 Ad Hoc）
- services视情况勾选，一般勾选push相关服务
- 下载并安装 .cer 文件

## 在 React Native 项目中配置

### 方式1：使用 Xcode 自动管理（推荐）

- 打开 Xcode，进入项目设置
```shell
cd ios && open YourProject.xcworkspace
```

- 选择 Targets > Signing & Capabilities：
    勾选 Automatically manage signing
    选择你的 Team（开发者账号）
    确保 Bundle ID 与 Apple 后台一致

> 登录开发者账号，建议登录有管理权限的开发者账号

### 方式2：手动配置

- 创建 Provisioning Profile：
    开发环境：选择 iOS Development，关联证书和 App ID
    生产环境：选择 App Store 或 Ad Hoc

- 下载 .mobileprovision 文件，双击安装
- 在 Xcode 中手动选择证书和 Profile：
    Signing (Debug)：开发证书
    Signing (Release)：生产证书

## 验证证书是否生效

看能否正常打包开发/生产包

## 在 Apple Developer 后台 添加设备 UDID

- [Apple Developer 后台](https://developer.apple.com)
- 进入 Devices > +
- 填写设备名称和 UDID
- 保存后，需 重新生成 Provisioning Profile 才能生效


## 从 .cer 和 mac 钥匙串导出 .p12

### 找到你的开发者证书或发布证书

- 打开 钥匙串访问.app：
    进入：应用程序 > 实用工具 > 钥匙串访问
- 选择左上角：
    钥匙串：登录
    分类：我的证书

- 找到你的 Apple 证书（名称类似于 Apple Distribution: 你的公司名）

### 右键导出证书为 .p12
- 右键点击该证书，选择 导出
- 格式选择：个人信息交换 (.p12)
- 设置一个导出密码（EAS 构建时需要）

> 如果你没看到导出选项，说明这个证书没有关联私钥（你是从别人那里拿的 .cer 而不是用自己的私钥生成的）


### 获取设备UDID

推荐方法：
- [蒲公英 获取UDID](https://www.pgyer.com/tools/udid)
- 使用iPhone设备的浏览器扫码，下载描述文件并安装
- 获取UDID

方法 1：通过 Mac 上的 Finder 或 iTunes（macOS Catalina 10.15 及更高版本）
- 使用 USB 线连接 iPhone/iPad 到 Mac
- 打开 Finder（macOS Catalina 10.15+）或 iTunes（旧版 macOS）
- 选择你的设备（在 Finder 侧边栏或 iTunes 左上角）
- 点击设备名称或序列号：
    在设备信息页面，点击 序列号 会切换显示 UDID
    右键点击 UDID 并选择 拷贝 以复制

方法 2：通过 Xcode 获取
- 连接设备到 Mac
- 打开 Xcode，进入顶部菜单：
    Window > Devices and Simulators

- 选择已连接的设备，在右侧信息面板中找到 Identifier（即 UDID）
    右键点击 UDID 选择 Copy

## 注意事项

- 每次证书过期（1年有效期）需重新生成

## 配置ios
将相关证书放到`certificate/ios/`目录下，记得配置git忽略

> development:device  ad-hoc分发包
> production  正式分发包
### eas.json
```json
{
    "cli": {
        "version": ">= 3.15.1",
        "appVersionSource": "local"
    },
    "build": {
        "development": {
            "extends": "production",
            "distribution": "internal",
            "android": {
                "gradleCommand": ":app:assembleDebug"
            },
            "ios": {
                "buildConfiguration": "Debug",
                "simulator": true
            }
        },
        "development:device": {
            "extends": "development",
            "distribution": "internal",
            "ios": {
                "buildConfiguration": "Release",
                "simulator": false,
                "credentialsSource": "local"
            }
        },
        "preview": {
            "extends": "production",
            "distribution": "internal",
            "ios": {
                "simulator": true
            },
            "android": {
                "buildType": "apk"
            }
        },
        "preview:device": {
            "extends": "preview",
            "ios": {
                "simulator": false
            }
        },
        "production": {
            "android": {
                "buildType": "apk",
                "credentialsSource": "local"
            },
            "ios": {
                "credentialsSource": "local",
                "autoIncrement": true
            }
        }
    },
    "submit": {
        "production": {}
    }
}

```

### credentials.json配置
> 打不同（开发/生产）iOS包，选择不同的证书


**证书和描述文件对照关系**

打包测试分发包，使用如下对照文件
> ios_distribution.p12 - adhoc.mobileprovision

打包正式分发包，使用如下对照文件
> ios_distribution.p12 - prod.mobileprovision


```json
{
    "android": {
        "keystore": {
            "keystorePath": "./certificate/keystore.jks",
            "keystorePassword": "xinyun2024",
            "keyAlias": "cjxy",
            "keyPassword": "xinyun2024"
        }
    },
    "ios": {
        "provisioningProfilePath": "certificate/ios/profile.mobileprovision",
        "distributionCertificate": {
            "path": "certificate/ios/dist.p12",
            "password": "DISTRIBUTION_CERTIFICATE_PASSWORD"
        }
    }
}

```

## 本地安装并配置 Fastlane

> 使用本地证书，不需要此步骤

安装 Fastlane
```shell
# 使用 RubyGems 安装（需 Ruby 环境）
gem install fastlane -NV

# 或通过 Homebrew（macOS）
brew install fastlane
```

验证安装
```shell
fastlane --version
```

初始化 Fastlane
```shell
cd ios && fastlane init
```

配置 Fastlane
```ruby
lane :build_for_eas do
  setup_ci
  sync_code_signing(type: "appstore")  # 如果是 App Store 分发
  # 或其他自定义步骤
end
```


## 比对证书和描述文件是否一致

```shell
# 查看描述文件SHA1
security cms -D -i xyapp_dev.mobileprovision > profile.plist

plutil -extract DeveloperCertificates.0 xml1 profile.plist -o - | \
awk '/<data>/{flag=1;next}/<\/data>/{flag=0}flag' | \
tr -d '\n ' | base64 -d > cert.der

openssl x509 -inform DER -in cert.der -noout -fingerprint
> SHA1 Fingerprint=A9:EE:A8:00:24:3F:DF:9F:57:B9:84:83:13:F4:A1:C6:55:E2:DD:DB

# 查看p12文件SHA1
openssl pkcs12 -in ios_development.p12 -nokeys -nodes -legacy -out cert.pem
openssl x509 -in cert.pem -noout -fingerprint
> SHA1 Fingerprint=A9:EE:A8:00:24:3F:DF:9F:57:B9:84:83:13:F4:A1:C6:55:E2:DD:DB
```
