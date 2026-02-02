# 申请Gmail App Password

[官方文档](https://support.google.com/accounts/answer/185833?hl=zh-Hans&sjid=11159932005849407105-NC)

在后端 .env 中使用：
SMTP_USER=your.account@gmail.com
SMTP_PASS=生成的_app_password_
SMTP 主机通常：SMTP_HOST=smtp.gmail.com，端口：SMTP_PORT=587，SMTP_SECURE=false（使用 STARTTLS）。

## 注意与限制

App Password 只在开启两步验证后可用；若你使用 Google Workspace（公司/学校账号），管理员必须允许生成 App Password（或启用相应设置）。
App Password 等同于应用专用凭证，生产环境也要妥善保管（放在环境变量 / 密钥管理，而非代码仓库）。
Gmail SMTP 有发送速率限制，若月发送量较大（例如你计划持续 10k/月），建议使用 SES / Mailgun / SendGrid 等专业发送服务以提高送达率和稳定性。
若要撤销某个 App Password，可回到同一页面撤销（Recommended for rotation/revocation）。

## 
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=true
SMTP_USER=cn.foxfly@gmail.com
SMTP_PASS=iukosrjywuzahebp