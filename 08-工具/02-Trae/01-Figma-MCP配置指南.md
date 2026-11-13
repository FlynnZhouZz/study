# Figma MCP 配置指南

> 状态：已确认
>
> 适用范围：TRAE / TRAE SOLO CN 中安装的 Figma AI Bridge MCP（`figma-developer-mcp`），用于 AI 代理直接拉取 Figma 设计稿节点数据与导出图片资源。

## 1. 背景

Figma 官方 API 域名（`api.figma.com`、`www.figma.com`）在国内网络环境下无法直连（DNS 解析超时）。MCP 服务器默认不走系统代理，导致 `get_figma_data` / `download_figma_images` 调用报错：

```
Error fetching file: Failed to make request to Figma API endpoint ...
Could not connect to the Figma API. If your network requires a proxy,
set the --proxy flag in your MCP server config or the FIGMA_PROXY
environment variable to your proxy URL (e.g. http://proxy:8080).
```

解决方式：在 MCP 配置中显式指定代理地址（本地 VPN 客户端监听端口）。

## 2. 配置文件位置

TRAE SOLO CN 的 MCP 配置文件：

```
C:\Users\<用户名>\AppData\Roaming\TRAE SOLO CN\User\mcp.json
```

> 若为 TRAE CN（非 SOLO 版本），对应路径一般在 `C:\Users\<用户名>\AppData\Roaming\Trae CN\User\` 下，文件名相同。

## 3. 完整配置示例（含代理）

```json
{
  "mcpServers": {
    "Figma AI Bridge": {
      "command": "npx",
      "args": [
        "-y",
        "figma-developer-mcp",
        "--stdio"
      ],
      "env": {
        "FIGMA_API_KEY": "<你的Figma个人访问令牌>",
        "FIGMA_PROXY": "http://127.0.0.1:7890"
      },
      "fromGalleryId": "GLips.Figma-Context-MCP"
    }
  }
}
```

字段说明：

| 字段 | 说明 |
| --- | --- |
| `command` / `args` | 通过 npx 启动 `figma-developer-mcp`，`--stdio` 为标准输入输出模式（TRAE MCP 默认通信方式），保持不动 |
| `FIGMA_API_KEY` | Figma 个人访问令牌，获取方式见第 5 节 |
| `FIGMA_PROXY` | 代理地址。`127.0.0.1:7890` 为 Clash 默认监听端口；其他客户端按实际端口填写（见第 4 节） |
| `fromGalleryId` | 表示该 MCP 从 TRAE MCP 市场安装，保留即可 |

### 3.1 代理配置的两种等价写法

**写法一：环境变量（推荐，改动最小）**

```json
"env": {
  "FIGMA_API_KEY": "<你的token>",
  "FIGMA_PROXY": "http://127.0.0.1:7890"
}
```

**写法二：启动参数**

```json
"args": [
  "-y",
  "figma-developer-mcp",
  "--stdio",
  "--proxy=http://127.0.0.1:7890"
]
```

两种方式二选一即可，不要重复配置。

## 4. 如何确定本地代理端口

打开 PowerShell 执行：

```powershell
netstat -ano | findstr "LISTENING" | findstr ":7890 :7891 :10808 :10809 :1080"
```

常见客户端默认端口：

| 客户端 | 默认 HTTP 代理端口 |
| --- | --- |
| Clash / Clash Verge / Mihomo | 7890 |
| V2rayN | 10808（socks）/ 10809（http） |
| Shadowsocks | 1080 |

验证代理是否可访问 Figma：

```powershell
curl.exe -I --max-time 10 -x http://127.0.0.1:7890 https://api.figma.com
```

返回 `HTTP/1.1 200 Connection established` 及 `302 Moved Temporarily` 即为连通正常。

## 5. Figma API Key 获取方式

1. 登录 Figma 网页版 → 左上角头像 → **Settings**
2. 切换到 **Security** 标签页
3. 找到 **Personal access tokens** → **Generate new token**
4. 填写名称（如 `trae-mcp`）、权限范围勾选 **File content: Read-only**
5. 生成后立即复制保存（只显示一次），填入配置的 `FIGMA_API_KEY`

> 注意：
> - Viewer（只读）账号的 API 有更严格的速率限制，可能遇到 429 限流（`Retry after xxxxx seconds`），属正常现象，等待解禁或换 Editor 协作者账号的 token。
> - Token 属于敏感凭据，不要提交到代码仓库或粘贴到公开场合；若已泄露，在上述同一页面 **Delete** 该 token 并重新生成。

## 6. 为什么界面上改不了配置

从 MCP 市场安装的服务（配置含 `fromGalleryId` 字段）在 TRAE 的 MCP 管理界面中字段为锁定状态，无法直接编辑。此时只能：

1. **完全退出 TRAE**（含系统托盘图标），避免进程占用文件或用旧配置回写覆盖；
2. 用记事本 / VSCode 直接编辑 `mcp.json`；
3. 保存后重新启动 TRAE，在 MCP 面板中重启该服务。

## 7. 配置完成后的验证

1. TRAE MCP 面板中 Figma AI Bridge 状态为已连接；
2. 让 AI 代理调用 `get_figma_data`，传入设计稿链接解析出的参数：
   - fileKey：链接中 `figma.com/design/<fileKey>/...` 部分（如 `Se7Xx7HG6COTuvaW0oeNC5`）
   - nodeId：链接中 `node-id=<id>` 参数，`-` 需替换为 `:`（如 `154-356` → `154:356`）
3. 能正常返回节点结构数据（layout、fills、字符样式等）即配置成功。

## 8. 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `Could not connect to the Figma API` | 未配置代理或代理端口错误 | 按第 3、4 节配置 `FIGMA_PROXY` |
| `Figma API rate limit hit (429)` | 触发 API 速率限制（常见于 Viewer 账号） | 等待提示的 Retry after 秒数后重试；或使用 Editor 权限账号 token |
| 改了 mcp.json 不生效 | TRAE 未完全退出，进程回写旧配置 | 托盘退出 TRAE 后再编辑，改完重启 |
| 界面上 MCP 配置字段为只读 | 市场安装（含 `fromGalleryId`） | 直接编辑配置文件，见第 6 节 |
| 代理端口不确定 | VPN 客户端各异 | 用第 4 节 netstat 命令探测 |
