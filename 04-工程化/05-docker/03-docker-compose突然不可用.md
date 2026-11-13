# Docker Desktop 升级后 docker-compose 命令找不到

> Desktop 不再随包分发 compose v1 的可执行文件，命令名从 `docker-compose` 变成了 `docker compose`；补个软链接只是让旧脚本继续能跑。

## 现象

一直在用的命令突然失效，脚本、CI、Makefile 全线报错：

```
zsh: command not found: docker-compose
```

`docker ps` 却正常，说明 Docker 守护进程和 CLI 都在，只是 `docker-compose` 这个独立二进制没了。

## 原因

docker-compose 有两代：

| 版本 | 形态 | 调用方式 |
|---|---|---|
| v1 | 独立的 Python 程序 `docker-compose` | `docker-compose up -d` |
| v2 | Docker CLI 的插件，Go 重写 | `docker compose up -d`（中间是空格） |

Docker Desktop 从某个版本起只保留 v2 插件，不再把 v1 的 `docker-compose` 软链到 `/usr/local/bin`。旧命令自然就找不到了。

插件文件仍在包内，路径为：

```
/Applications/Docker.app/Contents/Resources/cli-plugins/docker-compose
```

（原文写的 `Application/Contents/Resource/bin` 是同一处的简写，实际目录是 `Resources/cli-plugins`。）

## 两种解决方式

**方式一：改用 v2 命令（推荐）**

```bash
docker compose version       # 确认插件可用
docker compose up -d         # 注意是空格，不是连字符
```

v2 兼容 v1 的 `docker-compose.yml` 格式，绝大多数项目直接换命令即可。少数差异点：`version:` 字段被废弃会打警告（可删）、`--compatibility` 参数行为不同、部分 v1 特有的环境变量插值语法收紧。

**方式二：补软链接，让旧命令继续能用**

```shell
sudo ln -sf /Applications/Docker.app/Contents/Resources/cli-plugins/docker-compose /usr/local/bin/docker-compose
```

这行把 v2 插件伪装成 v1 的独立命令。适合「项目里几十个脚本都写了 `docker-compose`，暂时不想一个个改」的场景。

`/usr/local/bin` 在 Apple Silicon 上可能不在 PATH 里（Homebrew 用的是 `/opt/homebrew/bin`），可以改到那个目录，或者先 `echo $PATH` 确认。

## 更省事的方式：用别名

软链接需要 sudo，改 shell 配置更轻：

```bash
# ~/.zshrc
alias docker-compose='docker compose'
```

缺点是只对交互式 shell 生效，CI 和脚本里跑不到。团队项目里还是改脚本更彻底。

## 验证

```bash
which docker-compose          # 指向 /usr/local/bin/docker-compose 即成功
docker-compose version        # 注意会显示 v2.x，这是正常的
docker compose version        # 两种写法都能用
```

如果 `docker-compose version` 报 `Cannot connect to the Docker daemon`，那是 Docker Desktop 没启动，和命令本身无关。

## 常见误区

**很多人以为软链接之后 v1 就回来了**。链接指向的是 v2 插件，行为、日志格式、部分参数都和真正的 v1 不同。遇到 `--compatibility` 相关的行为差异时，别怀疑链接，先看版本。

**很多人以为 `docker compose` 和 `docker-compose` 完全等价**。文件名、项目名推导规则、`COMPOSE_FILE` 环境变量的默认值都有细微差别。同一个目录下两者混用，可能起出两套容器。

**很多人以为升级 Docker Desktop 只影响 compose**。Desktop 4.x 之后还改过 `docker context` 的默认值、把 `docker scan` 换成了 `docker scout`，升级后最好扫一遍 CI 里的所有 docker 命令。

## 关联阅读

- [Docker 常用命令](./01-docker常用命令.md)
- [docker compose 配置 nginx SSL 证书](./02-docker-compose配置nginx证书.md)
- [04-工程化 索引](../README.md)
