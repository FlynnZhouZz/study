# App 推送通道申请及费用

> 对应后端 `push` 配置中的 APNs、华为、小米、vivo、OPPO、Firebase 推送。面向中国大陆 App 开发和上架场景。各厂商后台、审核条件和限额可能调整，最终以控制台和官方协议为准。

## 总体结论

| 推送通道 | 主要设备 | 是否单独收费 | 主要前置条件 |
| --- | --- | --- | --- |
| APNs | iPhone、iPad、macOS 等 Apple 设备 | 不单独收推送费 | 需要有效的 Apple Developer Program 账号 |
| 华为 Push Kit | 华为、荣耀旧 HMS 机型、HarmonyOS/HMS 生态 | 通常不单独收推送费 | 华为开发者账号、应用、Push Kit 开通 |
| 小米推送 | 小米、Redmi、部分 HyperOS/MIUI 设备 | 基础服务目前免费 | 小米开发者账号、应用、推送服务启用 |
| vivo 推送 | vivo、iQOO 设备 | 通常不单独收推送费 | vivo 开发者账号、应用、推送服务申请通过 |
| OPPO PUSH | OPPO、一加、realme 部分机型 | 通常不单独收推送费 | OPPO 企业开发者账号、应用、PUSH 权限开通 |
| Firebase FCM | 海外 Android、Google Play 设备、Web、部分 iOS 场景 | FCM 本身免费 | Firebase 项目、Android 应用、服务账号 JSON |

实际开发里，推送本身多数不收费；真正可能产生费用的是 Apple 开发者账号、各平台企业认证/上架材料、云服务器、第三方聚合推送服务、短信兜底、运营推广和合规整改。

## 是否需要企业资料

需要区分两个阶段：

- 开发者账号认证/应用创建阶段：国内厂商通常会要求个人或企业实名认证。公司 App 建议使用企业开发者账号，通常要准备营业执照、统一社会信用代码、法人/经办人信息、联系人手机号和邮箱等资料。
- 推送服务开通阶段：多数情况下不会重新收一整套企业资料，而是基于已经认证的开发者账号、已创建的应用、包名和应用审核状态开通推送权限。部分平台可能要求补充推送用途、隐私合规说明、应用截图或上架状态。

| 通道 | 是否需要企业资料 | 说明 |
| --- | --- | --- |
| APNs | 公司账号需要；个人账号不需要企业资料 | Apple 个人账号只做个人身份验证；组织账号需要 D-U-N-S、公司网站、公司域名邮箱和法律授权 |
| 华为 Push Kit | 公司 App 建议企业认证 | 需要华为开发者实名认证；创建应用、上架和开通 Push Kit 时会基于账号主体和应用信息审核 |
| 小米推送 | 通常需要企业实名认证 | 小米推送官方接入流程包含“通过企业实名认证成为小米开发者” |
| vivo 推送 | 公司 App 建议企业认证 | vivo 开放平台需要开发者认证，推送服务可能结合应用状态、包名和合规资料审核 |
| OPPO PUSH | 通常需要企业开发者账号 | OPPO PUSH 权限申请一般基于已认证开发者和已创建应用，企业资料不完整会影响开通 |
| Firebase FCM | 不强制中国企业资料 | 需要 Google/Firebase 项目和服务账号；若上架 Google Play，则另有 Google Play 开发者身份验证要求 |

国内商业 App 如果要覆盖主流安卓厂商，建议提前准备企业主体资料，而不是只准备技术参数。

常见资料：

- 营业执照。
- 统一社会信用代码。
- 企业名称、注册地址、办公地址。
- 法人信息或经办人信息。
- 联系人姓名、手机号、邮箱。
- 公司官网、隐私政策 URL、用户协议 URL。
- App 包名、应用名称、应用图标、应用截图。
- 软著、ICP备案、App 备案等资料，视平台和类目要求提供。
- 加固包、签名证书 SHA-256、隐私合规整改说明，视平台审核要求提供。

## 配置字段对应关系

```yaml
push:
  contentDetailOn: true
  pushPoolSize: 100
  apns:
    dev: false
    topic: ""
    password: ""
    cert: ""
  hms:
    packageName: ""
    appID: ""
    appSecret: ""
  mi:
    packageName: ""
    appID: ""
    appSecret: ""
    channelID: ""
  vivo:
    packageName: ""
    appID: ""
    appKey: ""
    appSecret: ""
  oppo:
    packageName: ""
    appID: ""
    appKey: ""
    appSecret: ""
    masterSecret: ""
  firebase:
    jsonPath: ""
    projectId: ""
    packageName: ""
```

| 字段 | 从哪里获取 | 说明 |
| --- | --- | --- |
| `contentDetailOn` | 自己配置 | 是否在通知栏展示消息详情；涉及隐私内容时建议谨慎开启 |
| `pushPoolSize` | 自己配置 | 后端推送并发池大小，不是厂商平台参数；过大可能触发限流 |
| `packageName` | Android 项目/各厂商应用后台 | 必须与 APK/AAB 包名一致，例如 `com.company.app` |
| `apns.topic` | Apple Developer / Xcode | 通常是 iOS Bundle ID，例如 `com.company.app` |
| `apns.cert` | Apple Developer 证书后台 | APNs `.p12` 证书路径，也可改造为 APNs Auth Key 方式 |
| `apns.password` | 导出 `.p12` 时设置 | 服务器读取证书时使用 |
| `hms.appID` / `hms.appSecret` | AppGallery Connect | 华为应用的 App ID 和 Client Secret/App Secret |
| `mi.appID` / `mi.appSecret` | 小米推送运营平台 | 小米应用启用推送后查看 |
| `mi.channelID` | 小米推送运营平台 | 通知渠道 ID，和客户端通知渠道保持一致 |
| `vivo.appID` / `vivo.appKey` / `vivo.appSecret` | vivo 开放平台推送服务 | 应用推送服务申请通过后查看 |
| `oppo.appID` / `oppo.appKey` / `oppo.appSecret` / `oppo.masterSecret` | OPPO PUSH 运营平台 | PUSH 权限通过后在应用配置中查看 |
| `firebase.jsonPath` | Firebase / Google Cloud | 服务账号 JSON 文件路径，注意不要提交到 Git |
| `firebase.projectId` | Firebase 项目设置 | Firebase Project ID |

## APNs 申请和费用

### 费用

- APNs 不按推送量单独收费。
- 需要 Apple Developer Program 会员资格，国内常见为 688 元/年，详见 [iOS 开发者账号申请流程及费用](./iOS开发者账号申请流程及费用.md)。

### 申请步骤

1. 登录 [Apple Developer](https://developer.apple.com/account/)。
2. 进入 Certificates, Identifiers & Profiles。
3. 在 Identifiers 中找到 App ID，确认 Bundle ID 与 iOS 工程一致。
4. 开启 Push Notifications 能力。
5. 创建 APNs 证书：
   - 证书方式：创建 Apple Push Notification service SSL 证书，下载 `.cer` 后导出 `.p12`。
   - 推荐长期方式：创建 APNs Auth Key，使用 Key ID、Team ID、Bundle ID 进行鉴权；如果当前后端只支持 `.p12`，先按证书方式配置。
6. 在服务器配置：
   - `topic`：Bundle ID。
   - `cert`：`.p12` 文件路径。
   - `password`：导出 `.p12` 时设置的密码。
   - `dev`：测试环境为 `true`，生产环境为 `false`。

### 注意事项

- 开发环境和生产环境 token 不通用，`dev` 配错会导致推送失败。
- APNs 证书和应用 Bundle ID 绑定，换包名、转移 App 或换团队后要重新检查证书。
- `.p12` 文件属于敏感凭据，不要放进公开仓库。

## 华为 Push Kit 申请和费用

### 费用

- 华为 Push Kit 通常不单独收推送费。
- 华为 HMS Core 大部分服务免费，部分服务有免费额度或按量计费；Push Kit 是否产生额外费用以 AppGallery Connect 和服务价格页为准。

### 申请步骤

1. 注册并登录 [华为开发者联盟](https://developer.huawei.com/consumer/cn/)。
2. 完成开发者实名认证，企业应用建议使用企业开发者账号。
3. 进入 AppGallery Connect，创建项目和应用。
4. 填写 Android 包名，配置 SHA-256 证书指纹。
5. 在“项目设置 > API 管理”中启用 Push Kit。
6. 在应用或项目配置中获取：
   - `packageName`
   - `appID`
   - `appSecret` 或 Client Secret
7. Android 客户端集成 HMS Push SDK，服务端按华为 Push Kit API 发送消息。

### 注意事项

- 华为通道主要覆盖安装了 HMS Core 的设备。
- App ID、Client ID、Client Secret 名称在不同版本控制台中可能略有差异，按后端 SDK 要求填入。
- 如果接入消息回执，要在 AppGallery Connect 配置回执地址。

## 小米推送申请和费用

### 费用

- 小米官方 FAQ 说明，小米推送基础服务目前免费。
- 可能存在消息分类、频控、每日限额、运营消息审核等规则，超出或违规不一定是收费问题，更多是限流或权限问题。

### 申请步骤

1. 注册并登录 [小米澎湃 OS 开发者平台](https://dev.mi.com/)。
2. 完成开发者认证。
3. 在控制台创建应用，填写包名。
4. 进入消息推送/推送运营平台，为应用启用推送服务。
5. 阅读并同意小米推送相关协议。
6. 获取：
   - `packageName`
   - `appID`
   - `appKey`
   - `appSecret`
   - `channelID`
7. Android 客户端集成 Mi Push SDK，服务端使用 AppSecret 调用小米推送 API。

### 注意事项

- `channelID` 要与客户端 Android 通知渠道匹配，否则可能影响通知展示样式或分类。
- 小米对通知消息分类、营销消息、私信消息等有管理规则，运营类推送要避免高频骚扰。
- 国行小米设备通常优先走小米系统通道，海外设备可考虑 FCM。

## vivo 推送申请和费用

### 费用

- vivo 推送通常不单独收推送费。
- 正式推送通常受应用状态、推送权限和每日额度限制；不同类别消息、运营消息可能需要审核。

### 申请步骤

1. 注册并登录 [vivo 开放平台](https://dev.vivo.com.cn/)。
2. 完成开发者认证，企业应用建议使用企业账号。
3. 创建应用并填写包名。
4. 在管理中心申请推送服务。
5. 按要求提交应用信息、隐私合规资料、推送用途等。
6. 审核通过后，在推送服务后台获取：
   - `packageName`
   - `appID`
   - `appKey`
   - `appSecret`
7. Android 客户端集成 vivo Push SDK，服务端使用 AppID、AppKey、AppSecret 获取鉴权 token 后发送。

### 注意事项

- vivo 正式推送权限通常要求应用审核通过或满足平台要求；未通过时可能只能测试推送。
- vivo 服务端接口一般要求时间戳和签名，服务器时间要准确。
- 建议配置回执地址，方便统计到达、点击和失败原因。

## OPPO PUSH 申请和费用

### 费用

- OPPO PUSH 通常不单独收推送费。
- 需要 OPPO 企业开发者账号；如果账号认证、应用上架、软著或合规材料需要代理，会产生外部服务费用。

### 申请步骤

1. 注册并登录 [OPPO 开放平台](https://open.oppomobile.com/)。
2. 完成企业开发者认证。
3. 创建应用并填写包名。
4. 在“应用服务/开发服务/推送服务”中申请 OPPO PUSH 权限。
5. 权限通过后进入 OPPO PUSH 运营平台。
6. 在配置管理或应用配置中获取：
   - `packageName`
   - `appID`
   - `appKey`
   - `appSecret`
   - `masterSecret`
7. Android 客户端集成 OPPO Push SDK，服务端使用 AppKey、MasterSecret 等参数签名发送。

### 注意事项

- OPPO PUSH 使用 `MasterSecret` 参与服务端签名，泄露后风险很高。
- 申请权限时可能要求应用已创建、包名一致、企业资质完整。
- OPPO、一加、realme 的覆盖范围和系统版本有关，实际到达情况要用真机测试。

## Firebase FCM 申请和费用

### 费用

- Firebase Cloud Messaging 本身属于 Firebase 免费产品。
- 如果同时使用 Firebase Functions、Firestore、Storage、Authentication 短信验证等能力，可能产生费用；不要把 FCM 免费理解成整个 Firebase 项目都免费。

### 申请步骤

1. 登录 [Firebase Console](https://console.firebase.google.com/)。
2. 创建 Firebase 项目。
3. 添加 Android 应用，填写包名。
4. 下载 `google-services.json` 给 Android 客户端使用。
5. 在 Google Cloud 或 Firebase 项目设置中创建服务账号密钥，下载服务账号 JSON。
6. 在服务器配置：
   - `jsonPath`：服务账号 JSON 路径。
   - `projectId`：Firebase Project ID。
   - `packageName`：Android 包名。
7. Android 客户端集成 Firebase Messaging SDK，服务端通过 Firebase Admin SDK 或 HTTP v1 API 发送消息。

### 注意事项

- FCM 在海外 Android 设备上更常用；中国大陆国行 Android 设备通常不能稳定依赖 FCM。
- iOS 也可以通过 FCM 转发到 APNs，但仍然需要配置 Apple APNs 凭据。
- 服务账号 JSON 是高敏感凭据，不要提交到 Git。

## 国内 Android 推荐接入策略

国内 Android 没有统一可用的系统推送通道，通常需要多厂商推送组合：

| 设备 | 推荐通道 |
| --- | --- |
| 华为/HarmonyOS/HMS | 华为 Push Kit |
| 小米/Redmi | 小米推送 |
| vivo/iQOO | vivo 推送 |
| OPPO/一加/realme | OPPO PUSH |
| 海外 Android/Google Play 设备 | Firebase FCM |
| 其它设备 | 第三方聚合推送或应用保活兜底，但要注意合规 |

如果不想自己维护多厂商 SDK 和服务端签名，可以选择极光、个推、友盟、腾讯云移动推送、阿里云移动推送等聚合服务。聚合推送通常会有免费版、MAU 阶梯、厂商通道增强、数据统计和 SLA 套餐，费用按服务商报价。

## 安全和合规注意事项

- 所有 `appSecret`、`masterSecret`、APNs `.p12`、Firebase JSON 都只能放在服务端，不能写进 App 客户端。
- 不要把推送密钥提交到 Git；建议放入环境变量、配置中心或密钥管理服务。
- 推送内容涉及手机号、订单、验证码、聊天内容时，建议关闭通知详情或只展示摘要。
- 营销推送要提供退订/关闭入口，避免高频打扰。
- 国内应用市场会检查隐私政策中是否说明推送 SDK 收集的设备信息、网络信息、应用信息等。
- 客户端要处理用户关闭通知权限、系统省电限制、厂商消息分类和通知渠道。

## 费用预算建议

| 场景 | 推送直接费用 | 可能的间接费用 |
| --- | --- | --- |
| 只做 iOS 推送 | APNs 不单独收费 | Apple Developer Program 年费 |
| 国内 Android 多厂商直连 | 厂商推送通常不单独收费 | 各厂商账号认证、上架材料、软著、开发和维护成本 |
| 海外 Android FCM | FCM 本身免费 | Firebase 其它服务、Google Play 账号、服务器 |
| 使用聚合推送服务 | 取决于服务商套餐 | MAU、消息量、厂商通道增强、数据统计、SLA |

## 官方链接

- [Apple APNs 远程通知服务端配置](https://developer.apple.com/documentation/usernotifications/setting-up-a-remote-notification-server)
- [Apple 证书概览](https://developer.apple.com/cn/help/account/certificates/certificates-overview/)
- [华为 Push Kit](https://developer.huawei.com/consumer/cn/hms/huawei-pushkit)
- [华为 HMS Core 服务价格](https://developer.huawei.com/consumer/cn/hms/price/)
- [小米推送服务](https://dev.mi.com/xiaomihyperos/ability/mipush)
- [小米推送常见问题](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=1545)
- [vivo 开放平台](https://dev.vivo.com.cn/)
- [vivo PUSH 开放平台 API 文档](https://swsdl.vivo.com.cn/appstore/developer/uploadfile/20190129/20190129110835218.pdf)
- [OPPO PUSH](https://developers.oppomobile.com/newservice/capability?pagename=push)
- [OPPO PUSH 服务开启指南](https://open.oppomobile.com/bbs/forum.php?mod=viewthread&tid=1906)
- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)
- [Firebase 价格](https://firebase.google.com/pricing)
