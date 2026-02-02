# 申请Gmail App Password

[官方文档](https://support.google.com/accounts/answer/185833?hl=zh-Hans&sjid=11159932005849407105-NC)

在后端 .env 中使用： <br>
SMTP_USER=your.account@gmail.com <br>
SMTP_PASS=生成的_app_password_ <br>
SMTP 主机通常：SMTP_HOST=smtp.gmail.com，端口：SMTP_PORT=587，SMTP_SECURE=false（使用 STARTTLS）。 <br>

## 开通步骤

### 1、登录Google管理账号

[Google管理账号](https://myaccount.google.com)或者使用Google浏览器登录 - 右上角头像 - 管理Google账号

### 2、开启 两步验证

路径：管理Google账号 - 安全性与登录 - 两步验证 - 验证密码 - 开启两步验证

### 3、创建和管理应用专用密码

[创建和管理应用专用密码](https://myaccount.google.com/apppasswords) - 验证密码 - 创建应用专用密码 - 复制（只展示这一次，需复制安全保管）

## 注意与限制

App Password 只在开启两步验证后可用；若你使用 Google Workspace（公司/学校账号），管理员必须允许生成 App Password（或启用相应设置）。 <br>
App Password 等同于应用专用凭证，生产环境也要妥善保管（放在环境变量 / 密钥管理，而非代码仓库）。 <br>
Gmail SMTP 有发送速率限制，若月发送量较大（例如你计划持续 10k/月），建议使用 SES / Mailgun / SendGrid 等专业发送服务以提高送达率和稳定性。 <br>
若要撤销某个 App Password，可回到同一页面撤销（Recommended for rotation/revocation）。 <br>

## `.env`

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=true
SMTP_USER=example@gmail.com
SMTP_PASS=yourAppPwssword
```