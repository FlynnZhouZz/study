## 申请 Google Translate API Key

步骤如下：

注册 Google Cloud 账号
访问 https://cloud.google.com/，用 Google 账号注册并登录。

创建项目
控制台左上角点击“选择项目” → “新建项目”，填写名称并创建。

启用 Cloud Translation API

进入项目后，左侧菜单“API 和服务” → “库”。
搜索“Cloud Translation API”或“翻译”。
点击进入，点“启用”。
创建 API 密钥

左侧菜单“API 和服务” → “凭据”。
点击“创建凭据” → 选择“API 密钥”。
生成后可复制该 key。
安全设置（可选）

建议设置“应用限制”（如 HTTP referrer，仅允许你的网站域名访问）。
设置“API 限制”，只允许 Cloud Translation API。
费用说明

Google Translate API 按调用量计费，有免费额度（通常每月500,000字符）。
需绑定信用卡，超出免费额度会自动扣费。
使用方法

将 key 填入 .env 文件的 VITE_GOOGLE_TRANSLATE_KEY。
代码中会自动读取，无需手动传递。
如需详细图文教程，可访问 Google 官方文档：
https://cloud.google.com/translate/docs/setup