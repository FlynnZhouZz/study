## 申请 Google Translate API Key

1. 注册并登录 [Google Cloud](https://cloud.google.com) 账号

2. 创建项目

- 控制台(右上角) -> 控制台左上角点击“选择项目” -> “新建项目”，填写名称并创建。

3. 启用 Cloud Translation API

- 进入项目后，左侧菜单“API 和服务” -> “库”。
- 搜索“Cloud Translation API”或“翻译”。
- 点击进入，点“启用”。
- 创建 API 密钥

4. 创建凭据

- 左侧菜单“API 和服务” -> “凭据”。
- 点击“创建凭据” -> 选择“API 密钥”。
- 生成后可复制该 key。
- 安全设置（可选）

5. 建议设置

- “应用限制”（如 HTTP referrer，仅允许你的网站域名访问）。
- 设置“API 限制”，只允许 Cloud Translation API。

6. 费用说明

需绑定信用卡，超出免费额度会自动扣费。<br>
Google Translate API 按调用量计费：
- 免费额度：通常每月500,000字符。
- 超过后：每100万字符 20美元

7. 使用方法

将 key 填入 .env 文件的 VITE_GOOGLE_TRANSLATE_KEY。<br>
代码中会自动读取，无需手动传递。

8. 设置配额

- 进入 [Google Cloud Console](https://console.cloud.google.com)
- 导航到 IAM 与管理 → 配额
- 搜索 “Cloud Translation API”
- 找到 “Characters per day”（每日字符数）等指标 (使用浏览器搜索)
- 点击 “编辑配额”，将限额设置为 50万字符/天（或更低）
    - 注意：每月50万免费额度 ≈ 每日约1.67万字符，建议设置略低于此值以保安全
- 找到“Characters per minute”（每分钟字符数）。配额 100

如需详细图文教程，可访问 [Google translate 官方文档](https://cloud.google.com/translate/docs/setup)：
