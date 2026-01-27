# node+express实现gmail发送邮件

## 准备工作

[Gmail](https://mail.google.com)

### 设置 POP/IMAP

路径: 登录 - 设置（右上角设置icon） - 查看所有设置 - 转发和POP/IMAP - 启动POP和IMAP

### 申请Google App Password

[申请Google App Password](./申请Gmail%20App%20Password.md)

## 开发

核心库：
```json
{
    "scripts": {
        "start": "node index.js"
    },
    "dependencies": {
        "cors": "^2.8.5",
        "dotenv": "^17.2.3",
        "express": "^4.18.2",
        "express-rate-limit": "^6.7.0",
        "firebase-admin": "^11.10.0",
        "helmet": "^7.0.0",
        "morgan": "^1.10.0",
        "nodemailer": "^6.9.3"
    }
}
```

核心接口：
```js
const app = express();
// 兼容 CommonJS / ESM 导出：部分环境下 `helmet` 导出为 { default: fn }
const _helmetFactory = typeof helmet === 'function' ? helmet : (helmet && typeof helmet.default === 'function' ? helmet.default : null);
if (_helmetFactory) {
    app.use(_helmetFactory());
} else {
    console.warn('helmet middleware is not callable in this environment; skipping helmet()');
}
app.use(cors());
app.use(express.json());
app.use(morgan('combined'));

// 全局基础限流（按 IP）
const limiter = rateLimit({
    windowMs: 60 * 1000,
    max: 60, // 限制每个 IP 地址每分钟最多请求 60 次
});
app.use(limiter);

/**
 * @param {crypto.BinaryLike} code
 */
function hashCode(code) {
    return crypto.createHash('sha256').update(code).digest('hex');
}

// POST /send-otp { email }
app.post('/send-otp', async (req, res) => {
    try {
        const email = (req.body.email || '').toString().trim().toLowerCase();
        if (!email) return res.status(400).json({ ok: false, error: 'missing email' });

        // 每邮箱重发保护：使用以 email 为 id 的单文档记录，避免复合索引需求
        const minIntervalMs = (Number(MIN_RESEND_INTERVAL_SECONDS) || 60) * 1000;
        const recentCutoff = Date.now() - minIntervalMs;
        const emailDocId = encodeURIComponent(email);
        const docRef = db.collection('email_otps').doc(emailDocId);

        // 生成 OTP
        const code = Math.floor(100000 + Math.random() * 900000).toString();
        const codeHash = hashCode(code);
        const ttlMs = (Number(OTP_TTL_MINUTES) || 5) * 60 * 1000;
        const expiresAt = Date.now() + ttlMs;

        // 使用事务原子检查并写入，避免并发请求导致竞态
        try {
            await db.runTransaction(async (tx) => {
                const snap = await tx.get(docRef);
                if (snap.exists) {
                    const d = snap.data();
                    let createdAtMs = null;
                    if (d && d.createdAt && typeof d.createdAt.toMillis === 'function') {
                        createdAtMs = d.createdAt.toMillis();
                    } else if (d && d.createdAt && typeof d.createdAt === 'number') {
                        createdAtMs = d.createdAt;
                    }
                    if (createdAtMs && createdAtMs >= recentCutoff) {
                        const e = new Error('resend_too_soon_tx');
                        e.code = 'RESEND_TOO_SOON';
                        throw e;
                    }
                }
                tx.set(docRef, {
                    email,
                    codeHash,
                    expiresAt,
                    createdAt: admin.firestore.FieldValue.serverTimestamp(),
                });
            });
        } catch (txErr) {
            if (txErr && txErr.code === 'RESEND_TOO_SOON') {
                return res.status(429).json({ ok: false, error: 'resend_too_soon' });
            }
            console.error('Transaction error when writing OTP:', txErr);
            return res.status(500).json({ ok: false, error: 'internal_error' });
        }

        // 发送邮件
        const textBody = `Your verification code is ${code}. It expires in ${OTP_TTL_MINUTES} minutes.`;
        const htmlBody = `<p>Your verification code is <strong>${code}</strong>. It expires in ${OTP_TTL_MINUTES} minutes.</p>`;

        // 使用 nodemailer 通过 SMTP 发送邮件（例如 Gmail）。需要 SMTP_USER 和 SMTP_PASS（对 Gmail 建议使用 App Password）。
        const SMTP_HOST = process.env.SMTP_HOST || 'smtp.gmail.com';
        const SMTP_PORT = Number(process.env.SMTP_PORT) || 587;
        const SMTP_SECURE = (process.env.SMTP_SECURE || 'false') === 'true';
        const SMTP_USER = process.env.SMTP_USER;
        const SMTP_PASS = process.env.SMTP_PASS;

        if (!SMTP_USER || !SMTP_PASS) {
            console.error('No SMTP credentials configured (SMTP_USER/SMTP_PASS missing)');
            return res.status(500).json({ ok: false, error: 'no_smtp_credentials' });
        }

        // 在文件顶端或此处读取 env
        const DEV_SMTP_IP = process.env.DEV_SMTP_IP || '142.250.101.109';

        // 选择 host：开发环境用 IP，生产用 SMTP_HOST（域名）
        const hostToUse = process.env.NODE_ENV === 'production' ? SMTP_HOST : DEV_SMTP_IP;

        // 创建 transporter，并启用调试日志以便排查连接问题
        const transporterOptions = {
            host: hostToUse,
            port: SMTP_PORT,
            secure: SMTP_SECURE,
            auth: {
                user: SMTP_USER,
                pass: SMTP_PASS,
            },
            // logger: true,
            // debug: true,
            // 关键：必须设置servername用于TLS证书验证
            tls: {
                servername: SMTP_HOST,
                rejectUnauthorized: true
            },
            // 在一些本地/测试环境中，可能需要短期放宽 TLS 验证，生产环境不要改为 false
            // tls: { rejectUnauthorized: process.env.SMTP_TLS_REJECT_UNAUTHORIZED !== 'false' },
        };
        const transporter = nodemailer.createTransport(transporterOptions);

        // 在发送前 verify 一次连接可达性，这会返回更明确的失败原因（例如 ENOTFOUND/ECONNREFUSED/ECONNRESET）
        try {
            await transporter.verify();
        } catch (verifyErr) {
            console.error('SMTP verify failed:', verifyErr && verifyErr.code, verifyErr && verifyErr.message);
            return res.status(502).json({ ok: false, error: 'smtp_verify_failed', detail: verifyErr && verifyErr.message });
        }

        try {
            await transporter.sendMail({
                from: SMTP_USER,
                to: email,
                subject: 'Your verification code',
                text: textBody,
                html: htmlBody,
            });
        } catch (sendErr) {
            // 捕获并返回详细的错误码与信息，便于定位网络/认证问题
            console.error('transporter.sendMail error', sendErr && sendErr.code, sendErr && sendErr.message);
            if (sendErr && (sendErr.code === 'ECONNRESET' || sendErr.code === 'ESOCKET')) {
                console.error('Detected connection reset during SMTP send — check SMTP_HOST/PORT/SECURE and network/firewall');
            }
            return res.status(502).json({ ok: false, error: 'smtp_send_failed', detail: sendErr && sendErr.message });
        }

        return res.json({ ok: true });
    } catch (err) {
        console.error('send-otp error', err);
        return res.status(500).json({ ok: false, error: 'internal_error' });
    }
});

// POST /verify-otp { email, code }
app.post('/verify-otp', async (req, res) => {
    try {
        const email = (req.body.email || '').toString().trim().toLowerCase();
        const code = (req.body.code || '').toString().trim();
        if (!email || !code) return res.status(400).json({ ok: false, error: 'missing_params' });

        const codeHash = hashCode(code);
        const emailDocId = encodeURIComponent(email);
        const docRef = db.collection('email_otps').doc(emailDocId);
        const snap = await docRef.get();
        if (!snap.exists) return res.status(400).json({ ok: false, error: 'invalid_code' });

        const data = snap.data();
        if (!data) return res.status(400).json({ ok: false, error: 'invalid_code' });
        if (data.codeHash !== codeHash) {
            return res.status(400).json({ ok: false, error: 'invalid_code' });
        }

        // expiresAt 存的是 epoch ms
        if (data.expiresAt && data.expiresAt >= Date.now()) {
            try { await docRef.delete(); } catch (e) { }
            return res.json({ ok: true });
        }

        try { await docRef.delete(); } catch (e) { }
        return res.status(400).json({ ok: false, error: 'expired' });
    } catch (err) {
        console.error('verify-otp error', err);
        return res.status(500).json({ ok: false, error: 'internal_error' });
    }
});

app.listen(PORT, () => {
    console.log(`Email OTP backend listening on port ${PORT}`);
});
```

### 前端调用示例（fetch）：

```js
// 发送验证码
await fetch('https://your-backend/send-otp', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com' })
});

// 验证验证码
const res = await fetch('https://your-backend/verify-otp', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com', code: '123456' })
});
const json = await res.json();
```