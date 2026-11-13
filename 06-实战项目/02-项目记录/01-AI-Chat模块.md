# AI-Chat 模块技术文档

## 概述

AI 助手模块是网站全局浮动聊天组件，用户可点击右下角浮动按钮打开 AI 对话弹窗，咨询产品、方案和服务相关问题。

**当前状态**：前后端已完整对接，包含会话管理、打字机效果、Markdown 渲染、国际化等完整功能。

---

## 目录

- [文件结构](#文件结构)
- [组件详解](#组件详解)
  - [ChatButton — 浮动按钮](#1-chatbutton--浮动按钮)
  - [ChatModal — 聊天弹窗](#2-chatmodal--聊天弹窗)
  - [MessageList — 消息列表](#3-messagelist--消息列表)
  - [MessageItem — 消息项](#4-messageitem--消息项)
  - [ChatInput — 输入框](#5-chatinput--输入框)
- [Hooks](#hooks)
  - [useTypewriter — 打字机效果](#usetypewriter--打字机效果)
- [服务层](#服务层)
  - [ai-call.ts — AI 调用服务](#ai-callts--ai-调用服务)
  - [fingerprint.ts — 浏览器指纹](#fingerprintts--浏览器指纹)
  - [http.ts — HTTP 客户端](#httpts--http-客户端)
  - [system-prompt.ts — 系统提示词](#system-promptts--系统提示词)
  - [markdown-client.ts — Markdown 渲染](#markdown-clientts--markdown-渲染)
- [类型定义](#类型定义)
  - [ChatMessage — 消息类型](#chatmessagets--)
  - [AI Chat 组件 Props](#ai-chat-组件-props)
- [国际化文案](#国际化文案)
- [后端接口规范](#后端接口规范)
  - [POST /wxzg/ai-call](#post-wxzgai-call)
- [数据存储](#数据存储)
- [会话生命周期](#会话生命周期)
- [错误处理](#错误处理)

---

## 文件结构

```
src/
├── components/ai-chat/
│   ├── ChatButton.tsx         # 浮动按钮（可拖拽）
│   ├── ChatModal.tsx          # 聊天弹窗（核心业务逻辑）
│   ├── MessageList.tsx        # 消息列表容器（自动滚底）
│   ├── MessageItem.tsx        # 单条消息（用户/助手气泡 + Markdown）
│   └── ChatInput.tsx          # 输入框（文本区 + 发送按钮）
├── hooks/
│   └── useTypewriter.ts       # 打字机效果 Hook
├── services/
│   └── ai-call.ts             # AI API 调用 + 会话管理
├── types/
│   ├── chat.ts                # 聊天消息核心类型
│   └── ai-chat.ts             # 组件 Props 类型
├── lib/
│   ├── system-prompt.ts       # 系统提示词（中英文知识库 + 回复规则）
│   ├── fingerprint.ts         # 浏览器指纹（FingerprintJS）
│   ├── http.ts                # Axios 实例（base 60s 超时）
│   └── markdown-client.ts     # 浏览器端 Markdown → HTML 渲染器
└── app/[locale]/layout.tsx    # 根布局（第 69 行挂载 <ChatButton />）
```

静态资源：

```
public/assets/ai-chat/
├── avatar.svg       # AI 头像
├── close.svg        # 关闭按钮图标
├── sparkle.svg      # 建议问题图标
├── attachment.svg   # 附件按钮图标
├── send.svg         # 发送按钮（未激活）
└── send-active.svg  # 发送按钮（激活）
```

---

## 组件详解

### 1. ChatButton — 浮动按钮

**路径**：`src/components/ai-chat/ChatButton.tsx`  
**类型**：Client Component (`'use client'`)

页面右下角可拖拽的浮动 AI 助手按钮。

#### 功能细节

| 功能 | 实现 |
|------|------|
| **默认位置** | `fixed right-0 top-[70%]`（视口右侧 70% 高度处） |
| **拖拽** | Pointer Events (`onPointerDown` / `onPointerMove` / `onPointerUp`) + `setPointerCapture` |
| **点击判断** | 移动超过 3px 阈值才标记为拖拽，否则触发打开弹窗 |
| **位置约束** | `clamp()` 限制在视口边界内 |
| **键盘** | `Enter` / `Space` 键可打开弹窗 |
| **图标** | `/assets/74.svg`，56×56 (移动端) / 70×70 (sm+) |

#### DragState 类型

```typescript
interface DragState {
    offsetX: number;   // 指针相对按钮左上角的 x 偏移
    offsetY: number;   // 指针相对按钮左上角的 y 偏移
    startX: number;    // 按下时的 clientX
    startY: number;    // 按下时的 clientY
    moved: boolean;    // 是否真正拖拽（>3px 阈值）
}
```

---

### 2. ChatModal — 聊天弹窗

**路径**：`src/components/ai-chat/ChatModal.tsx`  
**类型**：Client Component (`'use client'`)  
**Props**：`ChatModalProps` — `{ open: boolean; onClose: () => void }`

核心聊天容器，管理完整对话生命周期。

#### 主要功能

##### a) 动画控制

使用 `mounted` + `visible` 双状态实现 300ms 缩放淡入淡出：

1. `open = true`：先 `setMounted(true)` 挂载 DOM，两帧 RAF 后 `setVisible(true)` 触发 CSS transition
2. `open = false`：先 `setVisible(false)` 触发退出动画，300ms 后 `setMounted(false)` 卸载 DOM

##### b) 消息持久化

| 项目 | 说明 |
|------|------|
| **存储键** | `localStorage` → `wxzg_chat_messages` |
| **格式** | `{ date: "YYYY-MM-DD", messages: ChatMessage[] }` |
| **跨天清空** | 加载时检查日期，不同天则清空旧消息 |
| **保存时机** | 通过 `messagesFingerprint`（消息 id + content 长度 + status 的字符串摘要）监听变化 |
| **加载时机** | `open` 变为 `true` 时从 localStorage 恢复 |

##### c) 消息发送流程

```
handleSend(content)
  │
  ├─ 防重入检查 (sendingRef)
  ├─ 创建 user 消息 + assistant 占位消息 (status: 'sending')
  ├─ 追加到消息列表
  ├─ 调用 callAi({ prompt, knowledgeBase: getSystemPrompt(locale) })
  │
  ├─ code === 200 成功
  │   ├─ 切换 status → 'typing'
  │   ├─ 设置 typingText → 启动 useTypewriter
  │   └─ 打字机逐字更新 content
  │
  ├─ 业务错误码
  │   ├─ rate_limit_exceeded  → t('errorRateLimit')
  │   ├─ too_many_requests    → t('errorTooMany')
  │   ├─ invalid_fingerprint  → t('errorFingerprint')
  │   └─ 其他                 → t('errorGeneric')
  │   └─ status → 'error'
  │
  └─ 网络异常 (catch)
      └─ status → 'error', content → t('errorNetwork')
```

##### d) 打字机效果

- 使用 `useTypewriter(typingText, { speed: 15 })` hook
- `visibleText` 变化 → 实时更新消息 content（逐字渲染）
- `done = true` → `status` 切换为 `'done'`

##### e) 欢迎界面（无消息时）

- 头像 (`/assets/ai-chat/avatar.svg`)
- 问候语 + 副标题（来自国际化）
- 3 条建议问题按钮（来自 `t.raw('suggestions')`），点击直接发送

##### f) 其他细节

| 功能 | 实现 |
|------|------|
| **Escape 关闭** | `keydown` 监听 |
| **滚动锁定** | `mounted` 时 `body.style.overflow = 'hidden'` |
| **Portal** | `createPortal` → `document.body` |
| **背景装饰** | 3 个彩色模糊圆形（蓝/紫/紫）|
| **免责声明** | 底部固定显示 `t('disclaimer')` |
| **弹窗尺寸** | 高 `min(580px, calc(100vh-64px))`，宽 `min(438px, calc(100vw-32px))`，圆角 24px |

---

### 3. MessageList — 消息列表

**路径**：`src/components/ai-chat/MessageList.tsx`  
**Props**：`MessageListProps` — `{ messages: ChatMessage[] }`

- 渲染所有消息，每条通过 `MessageItem` 组件渲染
- 自动滚底：`messages` 变化时 `scrollIntoView({ behavior: 'instant' })`（用 instant 避免打字机高频更新时抖动）

---

### 4. MessageItem — 消息项

**路径**：`src/components/ai-chat/MessageItem.tsx`  
**Props**：`MessageItemProps` — `{ message: ChatMessage }`

根据 `role` 和 `status` 渲染不同样式：

| role | status | 样式 | 内容 |
|------|--------|------|------|
| `user` | — | 右对齐，蓝色气泡 `#175EFC`，白色文字 | 纯文本 |
| `assistant` | `sending` | 左对齐，灰色背景 `#F5F5F5` | 三点加载动画（`animate-pulse`） |
| `assistant` | `typing` / `done` | 左对齐，灰色背景 `#F5F5F5` | Markdown 渲染的 HTML |
| `assistant` | `error` | 左对齐，粉色背景 `#FFF0F0`，红色文字 `#CC3333` | 错误纯文本 |

Markdown 渲染通过 `useMemo` + `renderMarkdown(markdown-client.ts)` 实现，支持标题、段落、列表、加粗、链接、代码块、引用、表格。

---

### 5. ChatInput — 输入框

**路径**：`src/components/ai-chat/ChatInput.tsx`  
**Props**：`ChatInputProps` — `{ onSend: (content: string) => void }`

- `<textarea>` 多行输入，2 行高度
- `Enter` 发送，`Shift+Enter` 换行
- 发送按钮：有内容时显示激活图标 (`send-active.svg`)，无内容时灰色 (`send.svg`) + `disabled`
- 附件按钮（占位，当前未实现附件功能）

---

## Hooks

### useTypewriter — 打字机效果

**路径**：`src/hooks/useTypewriter.ts`

```typescript
function useTypewriter(
    fullText: string,
    options?: { speed?: number; enabled?: boolean }
): {
    visibleText: string;   // 当前可见文本（逐字递增）
    done: boolean;         // 是否输出完毕
    skip: () => void;      // 跳至末尾
}
```

- 使用 `setInterval` 每 15ms 输出一个字符
- `fullText` 变化时自动重置
- `enabled = false` 时直接显示全部文本

---

## 服务层

### ai-call.ts — AI 调用服务

**路径**：`src/services/ai-call.ts`

核心 API 调用层，封装会话管理逻辑。

#### 类型定义

```typescript
interface AiCallParams {
    prompt: string;
    knowledgeBase?: string;    // 仅首次创建会话时发送
    model?: string;
    temperature?: number;
    max_tokens?: number;
}

interface AiCallResult {
    result: string;            // AI 回复文本
    model: string;             // 使用的模型
    session_id?: string;       // 会话 ID
}

interface AiError {
    error: string;             // 错误码
}

interface AiCallResponse {
    code: number;              // 业务状态码（200 成功）
    data: AiCallResult | null;
    msg: string;
}
```

#### 会话管理

| 存储键 | `localStorage` → `wxzg_chat_session` |
|--------|--------------------------------------|
| **格式** | `{ date: "YYYY-MM-DD", sessionId: string | null, knowledgeBaseSent: boolean }` |

**模块级变量**（跨组件实例共享，刷新后从 localStorage 恢复）：

```typescript
let sessionId: string | null;
let knowledgeBaseSent: boolean;
```

**会话流程**：

```
首次调用               后续调用             会话失效
─────────            ─────────            ─────────
发送 knowledge_base   携带 session_id      error: session_not_found
  ↓                    ↓                    ↓
后端创建会话          后端续接对话          resetSession()
  ↓                    ↓                    ↓
返回 session_id       knowledge_base       下次调用自动重建
  ↓                   （后端已有）
本地保存
```

跨天自动重置：日期变化时清除 `wxzg_chat_session`。

#### 请求详情

```
POST /wxzg/ai-call
Headers:
  x-device-fingerprint: <浏览器指纹>
  Content-Type: application/json
Body:
  {
    prompt: string,                    // 必填，用户输入
    knowledge_base?: string,           // 仅首轮
    session_id?: string,               // 续接时携带
    model?: string,
    temperature?: number,
    max_tokens?: number
  }

validateStatus: () => true  // 不按 HTTP 状态码抛异常，统一由业务 code 字段判断
```

---

### fingerprint.ts — 浏览器指纹

**路径**：`src/lib/fingerprint.ts`

- 使用 `@fingerprintjs/fingerprintjs`（动态 import，避免 SSR 报错）
- 单例模式：首次调用时加载并缓存 `visitorId`
- SSR 安全：`typeof window === 'undefined'` 时返回空字符串

```typescript
export async function getFingerprint(): Promise<string>
```

---

### http.ts — HTTP 客户端

**路径**：`src/lib/http.ts`

```typescript
export const http = axios.create({
    timeout: 60_000,  // AI 接口响应较慢，60 秒超时
});
```

经过 `next.config.ts` rewrites 代理，前端请求同源地址无需配置 baseURL。

---

### system-prompt.ts — 系统提示词

**路径**：`src/lib/system-prompt.ts`

包含中英文两套知识库 + 回复规则，作为 `knowledge_base` 参数发送给后端（仅首轮）。

```typescript
export function getSystemPrompt(locale: string): string
// locale === 'zh' → 中文知识库
// 其他 → 英文知识库
```

**知识库内容**（压缩版，原始出处 `public/docs/knowledge-base.md`）：

- 公司概况
- 8 款核心产品表
- 定制开发能力
- AI 应用
- 公司优势
- 合作模式
- 技术栈
- FAQ 精选（10 条）

**回复规则**（8 条）：

1. 专业顾问口吻，结合业务场景说明
2. 开发需求 → 引导描述业务场景
3. 复杂项目 → 引导加 WhatsApp
4. 需求模糊 → 标准引导语
5. 报价 → 引导提供项目信息
6. 试用 → 标准 SaaS 可试用，定制可看演示
7. 无法回答 / 要求人工 → 引导联系客服
8. 非业务问题 → 礼貌拒绝并引导

---

### markdown-client.ts — Markdown 渲染

**路径**：`src/lib/markdown-client.ts`

浏览器端 Markdown → HTML 渲染器，使用 `marked` 库 + 自定义 `Renderer`。

支持元素及对应 Tailwind 样式：

| 元素 | 样式 |
|------|------|
| h1 | `text-base font-bold text-[#002555]` |
| h2 | `text-sm font-bold text-[#1B2740]` |
| h3 | `text-sm font-semibold text-[#1B2740]` |
| p | `text-[14px] leading-relaxed text-[#333]` |
| ul | `list-disc pl-5` |
| ol | `list-decimal pl-5` |
| strong | `font-semibold text-[#1B2740]` |
| a | `text-[#175EFC] underline` + `target="_blank"` |
| code | `bg-[#F0F4FA] rounded text-[13px] text-[#175EFC]` |
| pre | `bg-[#F5F7FA] rounded-lg p-3` |
| blockquote | `border-l-4 border-[#175EFC] italic` |
| table | 带边框 + 表头背景色 |

```typescript
export function renderMarkdown(md: string): string
```

---

## 类型定义

### chat.ts — 核心消息类型

**路径**：`src/types/chat.ts`

```typescript
type ChatRole = 'assistant' | 'user';

type ChatMessageStatus = 'sending' | 'typing' | 'done' | 'error';

interface ChatMessage {
    content: string;
    id: string;
    role: ChatRole;
    /** 仅 assistant 消息有效 */
    status?: ChatMessageStatus;
}
```

**状态流转**：

```
sending  →  typing  →  done       （正常流程）
sending  →  error                  （异常流程）
```

### AI Chat 组件 Props

**路径**：`src/types/ai-chat.ts`

```typescript
interface FloatingPosition { x: number; y: number }
interface DragState { offsetX: number; offsetY: number; startX: number; startY: number; moved: boolean }
interface ChatModalProps { onClose: () => void; open: boolean }
interface MessageListProps { messages: ChatMessage[] }
interface MessageItemProps { message: ChatMessage }
interface ChatInputProps { onSend: (content: string) => void }
```

---

## 国际化文案

**命名空间**：`aiChat`

| 键 | 中文 | 英文 |
|----|------|------|
| `openButton` | AI 助手 | AI Assistant |
| `title` | AI 助手 | AI Assistant |
| `headerTitle` | 万象自构 AI 助理 | WXZG AI Assistant |
| `greeting` | 你好，我是万象自构AI助理 | Hello, I'm the WXZG AI Assistant |
| `subtitle` | 可以帮你快速了解产品、方案与服务 | I can help you quickly learn about our products, solutions, and services |
| `suggestions[0]` | 如何免费试用万象自构的产品？ | How can I try WXZG products for free? |
| `suggestions[1]` | 万象自构有哪些方面的产品，适合哪些业务场景？ | What products does WXZG offer and what scenarios do they suit? |
| `suggestions[2]` | 如何联系销售团队？ | How can I contact the sales team? |
| `inputLabel` | 消息 | Message |
| `inputPlaceholder` | 请将您想了解的问题告诉我 | Tell me what you'd like to know |
| `send` | 发送 | Send |
| `closeButton` | 关闭 | Close |
| `attachmentButton` | 添加附件 | Add attachment |
| `disclaimer` | 内容由 AI 生成，仅供参考… | Content is AI-generated for reference only… |
| `errorRateLimit` | 今日使用次数已达上限… | You've reached today's usage limit… |
| `errorTooMany` | 请求过于频繁… | Too many requests… |
| `errorFingerprint` | 设备验证失败… | Unable to verify device… |
| `errorNetwork` | 网络异常… | Network error… |
| `errorGeneric` | 服务异常… | Something went wrong… |
| `roles.assistant` | 助手 | Assistant |
| `roles.user` | 你 | You |

---

## 后端接口规范

### POST /wxzg/ai-call

#### 请求

```
POST /wxzg/ai-call
Content-Type: application/json
X-Device-Fingerprint: <visitorId>
```

**请求体**：

```json
{
    "prompt": "string（必填，用户输入的问题）",
    "knowledge_base": "string（可选，知识库内容，仅首次请求携带，用于创建会话）",
    "session_id": "string（可选，会话 ID，续接对话时携带）",
    "model": "string（可选，模型名称）",
    "temperature": "number（可选，温度参数）",
    "max_tokens": "number（可选，最大 token 数）"
}
```

**首次调用示例**（创建会话）：

```json
{
    "prompt": "万象自构有哪些产品？",
    "knowledge_base": "【万象自构 - 知识库】\n\n## 公司概况\n..."
}
```

**后续调用示例**（续接会话）：

```json
{
    "prompt": "能定制开发吗？",
    "session_id": "sess_abc123"
}
```

#### 成功响应

```json
{
    "code": 200,
    "msg": "success",
    "data": {
        "result": "您好！万象自构目前有 8 款核心产品...",
        "model": "gpt-4o",
        "session_id": "sess_abc123"
    }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | number | 业务状态码，200 表示成功 |
| `msg` | string | 状态文本 |
| `data.result` | string | AI 生成的回复文本（Markdown 格式） |
| `data.model` | string | 实际使用的模型名称 |
| `data.session_id` | string | 会话 ID，前端需保存用于后续请求 |

#### 错误响应

```json
{
    "code": 429,
    "msg": "rate limit exceeded",
    "data": {
        "error": "rate_limit_exceeded"
    }
}
```

**错误码映射**：

| data.error | code | 含义 | 前端处理 |
|------------|------|------|----------|
| `rate_limit_exceeded` | 429 | 今日使用次数达上限 | 显示错误提示，明天恢复 |
| `too_many_requests` | 429 | 请求频率过高 | 显示错误提示，稍后重试 |
| `invalid_fingerprint` | 403 | 设备指纹验证失败 | 显示错误提示，建议刷新 |
| `session_not_found` | 404 | 会话不存在或已过期 | 前端静默重置会话，下次自动重建 |
| 其他 | 500 | 服务端异常 | 显示通用错误提示 |

#### 后端需要实现的关键逻辑

1. **会话创建**（首次调用）
   - 收到 `knowledge_base` → 创建新会话
   - 将 `knowledge_base` 作为 system message 注入对话上下文
   - 生成并返回 `session_id`

2. **会话续接**（后续调用）
   - 收到 `session_id` → 查找已有会话
   - 自动注入已存储的 system message（无需前端重复发送 `knowledge_base`）
   - 将 user prompt 追加到对话历史，调用 LLM 生成回复
   - 返回更新后的对话结果，同时返回 `session_id`

3. **会话过期处理**
   - 会话不存在或过期时，返回 `code !== 200` + `data.error: "session_not_found"`
   - 前端收到此错误后自动重置状态，下次调用重新创建会话

4. **设备指纹验证**
   - 读取请求头 `x-device-fingerprint`
   - 可用于频率限制、风控等

5. **频率限制**
   - 按设备指纹或 IP 实现每日使用次数限制
   - 超限时返回 `rate_limit_exceeded`
   - 短时间高频请求返回 `too_many_requests`

6. **跨天重置**
   - 按自然日重置使用次数计数
   - 会话在当天有效，跨天后可能需要重新创建（根据会话过期策略决定）

---

## 数据存储

### localStorage 键一览

| 键 | 格式 | 用途 | 过期策略 |
|----|------|------|----------|
| `wxzg_chat_messages` | `{ date, messages: ChatMessage[] }` | 当天聊天记录 | 跨天清空 |
| `wxzg_chat_session` | `{ date, sessionId, knowledgeBaseSent }` | 会话状态 | 跨天清空 |

### Cookie

无 Cookie 写入（当前不涉及非必要 Cookie）。

---

## 会话生命周期

```
用户打开弹窗
  │
  ├─ 从 localStorage 恢复当天消息（如有）
  │
  ├─ 用户发送第一条消息
  │   └─ POST /wxzg/ai-call
  │       body: { prompt, knowledge_base: <系统提示词> }
  │       → 后端创建会话 → 返回 session_id
  │
  ├─ 用户发送后续消息
  │   └─ POST /wxzg/ai-call
  │       body: { prompt, session_id }
  │       → 后端续接会话，自动注入 system message
  │
  ├─ session_not_found
  │   └─ resetSession() → 下次调用自动重建
  │
  └─ 次日打开
      └─ 跨天检测 → 清除消息 + 重置会话
```

---

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 网络断开 | catch → 显示 `errorNetwork` 提示 |
| API 返回业务错误 | 根据 `data.error` 映射到对应提示文案 |
| localStorage 读写失败 | try/catch 静默失败，不影响功能 |
| 指纹获取失败 | `getFingerprint()` 返回空字符串，不阻塞请求 |
| 并发发送 | `sendingRef` 防重入 |
| Markdown 解析异常 | `renderMarkdown` 空字符串检查 |
