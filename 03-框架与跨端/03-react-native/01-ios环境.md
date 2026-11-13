# iOS 开发环境（RN 0.72）

> iOS 构建链是 Node → Ruby → CocoaPods → Xcode 四层，任何一层版本不匹配，报错都会指向下一层，看起来像 RN 的问题。

## 版本约束先对齐

RN 0.72 的 `Gemfile` 写的是 `ruby ">= 2.7.6"`。macOS 系统自带的 `/usr/bin/ruby` 是 2.6.x（原文记录的 2.6.10 就是它，不是 Homebrew 装的），所以直接用系统 Ruby 会在 `bundle install` 阶段被拦下。

| 组件 | 0.72 的要求 | 检查命令 |
|---|---|---|
| Node | >= 16（建议 18 LTS） | `node -v` |
| Ruby | >= 2.7.6 | `ruby -v` |
| CocoaPods | >= 1.11 | `pod --version` |
| Xcode | >= 14.3 | `xcodebuild -version` |
| Xcode CLT | 与 Xcode 同版本 | `xcode-select -p` |

原文记录的可用 Ruby 是 3.x 版本（写的是 3.4）。实际建议用 3.1/3.2，这是 CocoaPods 生态验证最充分的区间；3.3+ 偶尔会遇到 `ffi` 编译问题。

## 用 rbenv 管 Ruby 版本

系统 Ruby 不要动，用 rbenv 装一份项目专用的：

```bash
brew install rbenv ruby-build

# 写进 ~/.zshrc，否则新开终端找不到 rbenv 装的版本
eval "$(rbenv init - zsh)"

rbenv install 3.2.2
rbenv global 3.2.2        # 或进项目目录后 rbenv local 3.2.2
ruby -v                   # 确认输出 3.2.2，不是 2.6.x
```

关键点：`rbenv init` 必须写进 shell 配置，并且 `~/.rbenv/shims` 要排在 PATH 前面，否则 `which ruby` 仍指向 `/usr/bin/ruby`。这是「装了 3.2 但 bundle 还说版本低」的唯一原因。

`rbenv install -l` 看可装版本，`rbenv versions` 看已装版本，`rbenv local 3.2.2` 在当前目录写 `.ruby-version` 让版本跟着项目走。

## 安装依赖与 Pods

```bash
# 1. 装 bundle 与项目依赖（在 ios 同级的项目根目录）
gem install bundler
bundle install

# 2. 装 Pods（Ruby 依赖装完后才能跑）
cd ios && bundle exec pod install && cd ..
```

新版 RN 推荐用 `bundle exec pod install` 而不是裸 `pod install`，保证用的是 Gemfile 锁定的 CocoaPods 版本。换 Ruby 版本或改了 `Podfile` 之后，先删 `Pods/` 与 `Podfile.lock` 再装。

Xcode 首次打开项目后，还要在 Settings → Locations 里把 Command Line Tools 设成对应的 Xcode，否则 `xcodebuild` 找不到 SDK。

## 常见报错对照

| 报错 | 真实原因 | 处理 |
|---|---|---|
| `Your Ruby version is 2.6.10, but your Gemfile specified >= 2.7.6` | 用了系统 Ruby | rbenv 切换 + 检查 PATH |
| `Unable to find a specification for 'FBLazyVector'` | Pods 源没同步 | `pod repo update`，或删 `Pods/` 重装 |
| `Command PhaseScriptExecution failed` + `node: command not found` | Xcode 的构建环境读不到 nvm 的 node | 在 Build Phase 里显式写 node 绝对路径，或用 `.xcode.env` 指定 |
| `building for iOS Simulator, but linking in object file built for iOS` | Apple Silicon 上架构不匹配 | Podfile 加 `EXCLUDED_ARCHS[sdk=iphonesimulator*] = arm64`（旧库）或升级库 |
| `sandbox: rsync ... deny file-write-create` | Xcode 15 与旧 RN 的脚本沙箱冲突 | Build Settings 里把 `ENABLE_USER_SCRIPT_SANDBOXING` 设为 NO |
| `The simulator ... is not installed` | 模拟器运行时缺失 | Xcode → Settings → Platforms 下载对应 iOS 版本 |

`.xcode.env` 是 0.7x 引入的机制，用来把 node 路径钉住，避免 Xcode 的 GUI 环境拿不到 nvm/fnm 的 PATH：

```bash
# ios/.xcode.env
export NODE_BINARY=$(command -v node)
```

## 缓存清了再说的三件事

环境问题里有一半是旧缓存：

```bash
watchman watch-del-all                      # Metro 的文件监听缓存
rm -rf node_modules && yarn install
cd ios && rm -rf Pods Podfile.lock && bundle exec pod install && cd ..
rm -rf ~/Library/Developer/Xcode/DerivedData  # Xcode 编译缓存
```

最后一项清了之后第一次编译会慢几分钟，但能解决「代码改了行为没变」这种玄学问题。

## 常见误区

**很多人以为报 Ruby 版本错就要重装系统 Ruby**。系统 Ruby 被 SIP 保护，动它会影响其他工具，正确做法是 rbenv + 项目内 `.ruby-version`。

**很多人以为 `pod install` 失败是网络问题**。国内访问 CDN 确实慢，但更常见的是 Ruby 版本不对导致 cocoapods 装在了另一个 gem 环境里，`which pod` 和 `which ruby` 不在同一目录就能确认。

**很多人以为模拟器跑通就等于真机能跑**。真机还要签名证书与 Provisioning Profile，Apple Silicon 上的模拟器架构问题也和真机完全不同。

## 关联阅读

- [iOS 证书配置](./07-iOS证书配置.md)
- [上架 App Store](./10-上架AppStore.md)
- [原生模块 NativeModule](./02-原生模块nativeModule.md)
- [03-框架与跨端 索引](../README.md)
