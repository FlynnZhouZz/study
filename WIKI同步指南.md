# 个人 Wiki 操作指南

本文档说明如何把本地笔记仓库（本仓库）通过 `benji-cli` 同步到正式环境知蛛网 Wiki。所有命令均在本仓库根目录执行。

## 一、原理与前置条件

- 同步模型：本地 Git 仓库是唯一内容真源，CLI 扫描 Markdown 后推送，知蛛网按「仓库 → 书籍 → 页面」展示。
- 正式环境地址：服务端 `https://server.benj.cn`（接口前缀 `/zhizhu`），门户 `https://zhizhu.benj.cn`。
- 本地要求：
  - Node.js >= 18。
  - 已全局安装 CLI：`npm i -g benji-cli`，`benji --version` 应为 `0.2.2` 或更高。
  - 本仓库必须是 Git 仓库（存在 `.git`）。
  - 正式环境存在可密码登录的账号（手机号 + 密码）。
- 服务端要求：正式环境已部署仓库型 Wiki 接口（`POST /zhizhu/wiki/sync/push`、`GET /zhizhu/wiki/sync/pull`），且数据库迁移已执行。

## 二、操作步骤

### 1. 进入仓库并确认状态

```bash
cd /Users/foxfly/Desktop/study/study
git status
```

推送前工作区应无未预期改动，避免把草稿或不相关内容一起发布。

### 2. 初始化配置

```bash
benji wiki init
```

执行后会在仓库根目录生成 `wiki.config.json`，并向 `.gitignore` 追加 `.wiki-token`、`.wiki-sync/`。

说明：

- 只扫描含 Markdown 的目录，每个一级目录为一个同步根目录，二级目录默认作为一本书。
- 重复执行不会覆盖已有配置，只增量补充新发现的目录。
- `server` 默认写入 `https://server.benj.cn`，无需手动指定。
- `repoKey`（如 `study-8b4a6ebe`）由 init 生成并固定，用于标识该仓库，不要修改。

### 3. 确认可见性

打开 `wiki.config.json`，检查每一处 `visibility`：

| 取值 | 含义 |
| --- | --- |
| `public` | 任何人可在门户阅读 |
| `login` | 登录用户可阅读 |
| `private` | 仅自己在个人中心可见，门户不展示 |

注意两点：

1. 需要同时把根目录（`roots[].visibility`）和书籍（`books[].visibility`）设为 `public`，任一层为 `private` 都会挡住展示。
2. 仓库整体可见性由配置推导：只要有任意一个根目录或书籍为 `public`，仓库即为公开。

全部公开时，用编辑器的全局替换把 `"visibility": "private"` 全部替换为 `"visibility": "public"` 即可。

### 4. 登录正式环境

```bash
benji wiki login
```

按提示输入正式环境的手机号与密码。成功后：

- 凭据写入仓库根目录 `.wiki-token`，有效期 24 小时，过期重新登录即可。
- `.wiki-token` 与 `.wiki-sync/` 已在 `.gitignore` 中，不要提交。

如需免交互（密码会留在 shell 历史，不建议）：

```bash
benji wiki login --phone 13800000000 --password '你的密码'
```

### 5. 预览待推送内容

```bash
benji wiki status
benji wiki sync push --dry-run
```

- `status` 查看仓库标识、服务器、登录状态、本地页面数与待推送/待拉取数量。
- `--dry-run` 只列出新增、修改、删除，不提交到服务器。

首次推送时全部页面都是 `new`，具体数量以命令实际输出为准。

### 6. 执行推送

```bash
benji wiki sync push
```

推送过程会：

1. 按页面路径计算内容 hash，只提交新增、修改、删除的页面。
2. 上传页面中引用的图片（`png/jpg/jpeg/gif/webp/svg`）到 `workspace/upload`，并按内容 hash 缓存，源 Markdown 不做改写。
3. 提交书籍与目录配置（含可见性）。
4. 成功后写入 `.wiki-sync/manifest.json` 与基线快照，供下次增量对比。

正常输出示例：

```text
[benji] 待推送 319 项：新增 319，修改 0，删除 0
[benji] 推送完成：新增 319，更新 0，删除 0，冲突 0，跳过 0
```

耗时与页面数量和图片数量相关；若中途中断，修正后直接重跑 `benji wiki sync push`，服务端按 `repo_id + path` 幂等 upsert。

### 7. 验证结果

| 验证项 | 地址/方式 |
| --- | --- |
| 工作台封面列表 | `https://zhizhu.benj.cn/workspace/wiki`（需登录） |
| 个人主页 Wiki | `https://zhizhu.benj.cn/{你的identifier}/wiki` |
| 书籍首页 | `https://zhizhu.benj.cn/{你的identifier}/wiki/{书籍目录名}` |
| 页面详情 | `https://zhizhu.benj.cn/{你的identifier}/wiki/{书籍目录名}/{页面slug}` |
| 公开目录树接口 | `GET https://server.benj.cn/zhizhu/bloggers/{你的identifier}/wiki/tree` |

`identifier` 是账号标识（个人主页根路径），`书籍目录名` 即 `wiki.config.json` 中的书籍 `path`（如 `01-计算机网络`），URL 中使用时需要百分号编码。

### 8. 日常增量同步

```bash
cd /Users/foxfly/Desktop/study/study
benji wiki status          # 确认待推送/待拉取
benji wiki sync push       # 本地改动推送到线上
benji wiki sync pull       # 拉取线上编辑写回本地，并自动 git commit
benji wiki sync            # 等价于先 pull 再 push
```

## 三、内容约定

| 约定 | 说明 |
| --- | --- |
| 仓库介绍页 | 仓库根目录的 `README.md` 作为整个 Wiki 的介绍页，展示在个人主页 Wiki 首页顶部，不进入书籍列表；frontmatter 规则与书籍 README 一致 |
| 书籍落地页 | 书籍目录下的 `README.md` 作为该书首页；没有时展示页面卡片列表 |
| 深层 README | 书籍目录以下更深层的 `README.md` 按普通页面上传 |
| 页面顺序 | frontmatter 的 `order` 优先，未填写时按文件名自然排序 |
| 页面标题 | frontmatter 的 `title`，未填写时用文件名 |
| 不公开页面 | frontmatter 设置 `draft: true`，不在公开页展示 |
| 自定义 slug | frontmatter 的 `slug` |
| SEO | frontmatter 的 `seoTitle`、`seoDescription` |
| 图片 | 放在书目录的 `assets/` 下，Markdown 使用仓库相对路径引用 |

frontmatter 示例：

```markdown
---
title: HTTP 协议
order: 3
summary: HTTP 报文、缓存与连接管理
seoTitle: HTTP 协议详解
seoDescription: HTTP 报文结构、缓存策略与连接管理要点
draft: false
slug: http
---
```

## 四、常见问题

| 现象 | 原因与处理 |
| --- | --- |
| `未找到登录凭据` | 未执行 `benji wiki login`，或 `.wiki-token` 已过期（24 小时），重新登录 |
| 推送返回 401 / 签名错误 | 凭据过期或本地与服务器时间偏差过大；重新 `login`，并校准系统时间 |
| 推送提示存在未解决的冲突标记 | 文件内残留 `<<<<<<<` / `>>>>>>>`，处理冲突后再推送 |
| 推送提示页面冲突 | 线上已修改过该页，先执行 `benji wiki sync pull`，合并后再推送 |
| 页面已推送但门户看不到 | 检查根目录与书籍两级 `visibility` 是否均为 `public`；检查 `draft` 是否为 `true` |
| 修改 `visibility` 后线上不变 | CLI 仅在存在页面差异时才发起推送；任意修改一篇 Markdown 内容后重新 `sync push` 即可提交书籍配置 |
| 图片不显示 | 图片需位于书目录 `assets/` 下且为受支持格式，引用路径必须是仓库相对路径；推送日志会提示缺失资源 |
| 本地删除文件后线上仍在 | 需要执行一次 `sync push`，删除会同步到服务端 |
| 整本书不再需要 | 在 `wiki.config.json` 的 `exclude` 中加入该目录路径前缀后重新推送，未出现在推送内容中的书会自动下线 |
| 提交了 `.wiki-token` | 立即从 Git 历史移除并重新登录；该文件与 `.wiki-sync/` 不应入库 |

## 五、首次推送建议检查清单

1. `benji --version` 为 0.2.2 及以上。
2. 正式环境服务端 Wiki 接口与迁移已就绪。
3. `wiki.config.json` 中 `repoKey` 生成后保持不变。
4. 根目录与书籍的 `visibility` 符合预期。
5. 所有图片已放在书目录 `assets/` 下。
6. `git status` 中只有预期改动。
7. 已执行 `--dry-run` 预览并核对数量。

## 六、可见性调整与下线

- **改可见性**：修改 `wiki.config.json` 对应字段，并让至少一篇 Markdown 产生内容差异后执行 `benji wiki sync push`。
- **单篇下线**：在 frontmatter 中加 `draft: true` 后推送。
- **整库下线**：把所有根目录与书籍改为 `private`，触发一次页面变更后推送。
- **删除书籍**：在 `exclude` 中加入路径前缀，推送后该书从线上移除。

以上操作都不会删除本地笔记文件。

## 七、安全与注意事项

1. `.wiki-token` 等同账号凭据，不要提交、不要外发。
2. 不要在 Markdown 中写入密码、密钥、内网地址等敏感信息；一旦推送，公开可读用户即可访问。
3. 推送前先 `git status` / `git diff` 确认内容，避免误传草稿目录。
4. 正式环境数据只由同步接口写入，不要手工改数据库。
