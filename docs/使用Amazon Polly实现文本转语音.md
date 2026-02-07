# 使用Amazon Polly实现文本转语音

[Amazon Polly](https://ap-southeast-2.console.aws.amazon.com/polly/home?region=ap-southeast-2)

## 登录AWS控制台

具体查看 ![注册AWS账号](./注册AWS账号.md)

## 本地安装 AWSCLI

macOS:
```bash
# 使用 Homebrew
brew install awscli

# 或者使用安装包
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

Windows:
```bash

# 使用 MSI 安装包下载
https://awscli.amazonaws.com/AWSCLIV2.msi

# 或者使用 Chocolatey
choco install awscli
```

Linux:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install awscli -y

# 或使用官方安装脚本
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## 前期准备工作

### 1. 进入 Amazon Polly 产品详情

[Amazon Polly](https://ap-southeast-2.console.aws.amazon.com/polly/home?region=ap-southeast-2)
或者：在AWS控制台直接搜索 Amazon Polly

### 2. 引入SDK实现文本转语音

[console](https://ap-southeast-2.console.aws.amazon.com/polly/home/SynthesizeSpeech)
[polly document](https://docs.aws.amazon.com/polly/latest/dg/what-is.html)

> 说明：
> 如果有条件，建议选择后端SDK或者。
> 由于我后端项目的PHP版本是7.4，而AWS官方要求PHP最低版本是8.1。要升级PHP版本工作量太大，最怕的是影响现有功能的隐患。
> 选择AWS SDK for JavaScript v3 为了安全，配置很麻烦。
> 最终，我选择了 nodejs SDK

### 3. 使用 nodejs SDK 前的配置

#### 1. 创建 Amazon S3 存储桶

- 路径: Console → Amazon S3 → 存储桶 → 通用存储桶 → 创建存储桶
- 存储桶名称: 英文、数字、`-`符号
- 对象所有权: ACL 已禁用（推荐）
- 阻止所有公开访问
- 存储桶版本控制: 禁用
- 标签: 可选
- 默认加密: 使用 Amazon S3 托管密钥进行服务器端加密（SSE-S3）
- 存储桶密钥: 启用

配置存储桶策略：
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::polly1-bucket/*"
    }
  ]
}
```

配置跨院资源共享(CORS)：
```json
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "PUT",
            "POST",
            "DELETE",
            "HEAD"
        ],
        "AllowedOrigins": [
            "https://asw.go168.site",
            "http://localhost:8081"
        ],
        "ExposeHeaders": [
            "ETag"
        ],
        "MaxAgeSeconds": 3000
    }
]
```

#### 2. 创建IAM 用户并附加策略

- Console → IAM → 用户 → 创建用户
- 用户名: 推荐英文
- 向用户提供 AWS 管理控制台的访问权限 - 可选: 勾选
- 控制台密码: 自动生成密码
- 用户必须在下次登录时创建新密码 – 推荐: 勾选
- 下一步
- 权限选项: 直接附加策略

权限策略: 创建polly策略
- polly1-bucket为自己的存储桶名
- 策略编辑器: json (polly.json)
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"polly:StartSpeechSynthesisTask",
				"polly:SynthesizeSpeech"
			],
			"Resource": "*"
		},
		{
			"Effect": "Allow",
			"Action": [
				"s3:PutObject",
				"s3:GetObject"
			],
			"Resource": [
				"arn:aws:s3:::polly1-bucket/*"
			]
		},
		{
			"Effect": "Allow",
			"Action": [
				"s3:ListBucket"
			],
			"Resource": [
				"arn:aws:s3:::polly1-bucket"
			]
		}
	]
}
```
- 下一步
- 策略名称: 推荐英文
- 描述: 可选
- 创建策略按钮

策略编辑器: json (s3.json)
- polly1-bucket为自己的存储桶名
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"s3:ListBucket"
			],
			"Resource": [
				"arn:aws:s3:::polly1-bucket"
			]
		},
		{
			"Effect": "Allow",
			"Action": [
				"s3:GetObject",
				"s3:PutObject"
			],
			"Resource": [
				"arn:aws:s3:::polly1-bucket/*"
			]
		}
	]
}
```
- 下一步
- 策略名称: 推荐英文
- 描述: 可选
- 创建策略按钮

创建用户后，进入用户详情：<br>
权限策略：没有polly和s3存储桶权限，需添加权限
- 添加权限
- 创建内联策略

安全凭证:
- 访问密钥 - 创建访问密钥 - 本地代码 - 下一步 - 描述标签值 - 创建访问密钥 - 下载.csv文件
- 文件中就是Access key ID、Secret access key

## 后端代码

```js
require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { PollyClient, StartSpeechSynthesisTaskCommand } = require('@aws-sdk/client-polly');
const { S3Client, GetObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');
const url = require('url');

const app = express();
app.use(cors());
app.use(bodyParser.json({ limit: '1mb' }));

const REGION = process.env.AWS_REGION || 'us-east-1';
const S3_BUCKET = process.env.OUTPUT_S3_BUCKET;
const S3_KEY_PREFIX = process.env.OUTPUT_S3_KEY_PREFIX || 'polly';

if (!S3_BUCKET) {
    console.warn('Warning: OUTPUT_S3_BUCKET not set in env. Set OUTPUT_S3_BUCKET to enable S3 output.');
}

const pollyClient = new PollyClient({ region: REGION });
const s3Client = new S3Client({ region: REGION });

// POST /api/polly/start-task
// 请求体: { text: string, voiceId?: string, outputKeyPrefix?: string }
app.post('/api/polly/start-task', async (req, res) => {
    try {
        const { text, voiceId = 'Joanna', outputKeyPrefix, engine } = req.body || {};
        if (!text || typeof text !== 'string' || text.trim() === '') {
            return res.status(400).json({ ok: false, message: 'Missing text' });
        }

        if (!S3_BUCKET) {
            return res.status(500).json({ ok: false, message: 'Server not configured with OUTPUT_S3_BUCKET' });
        }

        const prefix = (outputKeyPrefix || S3_KEY_PREFIX).replace(/(^\/+|\/+$)/g, '');
        const timestamp = Date.now();
        const keyPrefix = `${prefix}/${timestamp}`;

        // Engine 可选：'standard' 或 'neural'。优先使用请求中指定，其次使用环境变量 POLLY_ENGINE，默认 'neural'
        const chosenEngine = (engine || process.env.POLLY_ENGINE || 'neural').toLowerCase();

        const input = {
            OutputFormat: 'mp3',
            OutputS3BucketName: S3_BUCKET,
            Text: text,
            VoiceId: voiceId,
            TextType: 'text',
            OutputS3KeyPrefix: keyPrefix,
            Engine: chosenEngine === 'standard' ? 'standard' : 'neural',
        };

        const cmd = new StartSpeechSynthesisTaskCommand(input);
        let resp;
        try {
            resp = await pollyClient.send(cmd);
        } catch (err) {
            // 如果因为 engine 不支持导致失败，尝试回退到 neural 并重试一次
            const msg = (err && err.message) || '';
            if (msg.includes('does not support the selected engine') && input.Engine !== 'neural') {
                try {
                    const fallbackInput = { ...input, Engine: 'neural' };
                    const fallbackCmd = new StartSpeechSynthesisTaskCommand(fallbackInput);
                    resp = await pollyClient.send(fallbackCmd);
                } catch (e2) {
                    throw e2;
                }
            } else {
                throw err;
            }
        }

        // resp.SynthesisTask 在任务完成或创建时可能包含 OutputUri
        const task = resp.SynthesisTask || null;

        let presignedUrl = null;
        if (task && task.OutputUri) {
            // 尝试从 OutputUri 中解析出 bucket 和 key，并创建预签名 GET 链接
            try {
                const parsed = url.parse(task.OutputUri);
                // path begins with /bucket/key or /{region}.amazonaws.com/bucket/key
                // attempt to find bucket/key: if host contains "s3" style or path contains bucket
                const pathParts = (parsed.pathname || '').split('/').filter(Boolean);
                // If first segment equals bucket name, key is rest
                let key = null;
                if (pathParts.length > 1 && pathParts[0] === S3_BUCKET) {
                    key = pathParts.slice(1).join('/');
                } else {
                    // 回退方案：如果知道 OutputS3KeyPrefix，则使用 prefix + filename 构建 key
                    // 尝试获取最后一段作为文件名
                    const filename = pathParts[pathParts.length - 1];
                    key = `${keyPrefix}/${filename}`;
                }

                if (key) {
                    const getCmd = new GetObjectCommand({ Bucket: S3_BUCKET, Key: key });
                    presignedUrl = await getSignedUrl(s3Client, getCmd, { expiresIn: 60 * 60 });
                }
            } catch (e) {
                // 忽略生成预签名时的错误
                console.warn('Presign failed', e && e.message);
            }
        }

        return res.json({ ok: true, task, presignedUrl });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ ok: false, error: err.message || String(err) });
    }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`imchat_backend listening on http://localhost:${PORT}`);
});
```

```env
AWS_REGION=
AWS_ACCESS_KEY_ID=AKIA********KW5X4N
AWS_SECRET_ACCESS_KEY=rIJu0rM********sotU0
OUTPUT_S3_BUCKET=po********ket
PORT=5000

# Optional: prefix for generated S3 keys
OUTPUT_S3_KEY_PREFIX=polly
```

```json
// pageage.json
{
  "name": "imchat_backend",
  "version": "0.1.0",
  "private": true,
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  },
  "dependencies": {
    "@aws-sdk/client-polly": "^3.0.0",
    "@aws-sdk/client-s3": "^3.0.0",
    "@aws-sdk/s3-request-presigner": "^3.0.0",
    "body-parser": "^1.20.0",
    "cors": "^2.8.5",
    "dotenv": "^16.0.0",
    "express": "^4.18.2"
  },
  "devDependencies": {
    "nodemon": "^2.0.22"
  }
}
```

## 前端调用


```js
const awsVoiceOptions = [
    { value: 'Danielle', label: 'Danielle（Female）' },
    { value: 'Gregory', label: 'Gregory（Male）' },
    { value: 'Ivy', label: 'Ivy（Female）' },
    { value: 'Joanna', label: 'Joanna（Female）' },
    { value: 'Kendra', label: 'Kendra（Female）' },
    { value: 'Kimberly', label: 'Kimberly（Female）' },
    { value: 'Salli', label: 'Salli（Female）' },
    { value: 'Joey', label: 'Joey（Male）' },
    { value: 'Justin', label: 'Justin（Male）' },
    { value: 'Kevin', label: 'Kevin（Male）' },
    { value: 'Matthew', label: 'Matthew（Male）' },
    { value: 'Ruth', label: 'Ruth（Female）' },
    { value: 'Stephen', label: 'Stephen（Male）' },
    { value: 'Patrick', label: 'Patrick（Male）' },
];
```
```js
async doGenerateSpeech() {
    this.loadingVoice = true;
    try {
        const backendBase = Setting.pollyBackendUrl.replace(/\/$/, '');
        const endpoint = `${backendBase}/api/polly/start-task`;

        const payload = {
            text: this.formData.text_en,
            voiceId: this.awsVoiceId || 'Joanna',
        };

        const resp = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const data = await resp.json().catch(() => null);
        if (!resp.ok || !data) {
            const msg = (data && (data.message || data.error)) || `后端调用失败：${resp.status}`;
            this.$Message.error(msg);
            return;
        }

        if (!data.ok) {
            this.$Message.error(data.message || data.error || '合成失败');
            return;
        }
    } catch (err) {
        this.$Message.error(err?.message || '生成语音失败');
        console.error('doGenerateSpeech error:', err);
    } finally {
        this.loadingVoice = false;
    }
}
```