# Docker 常用命令

> 容器出问题时，八成是镜像没重建、端口没映射、或者卷挂错了；先分清镜像和容器，命令就不是背下来的。

## 镜像与容器

| 概念 | 是什么 | 类比 |
|---|---|---|
| 镜像 image | 只读的分层文件系统 + 启动命令 | 类 / 安装包 |
| 容器 container | 镜像的一次运行实例，加了可写层 | 实例 / 进程 |
| 卷 volume | 由 Docker 管理的持久化存储 | 外接硬盘 |
| 网络 network | 容器之间的通信域 | 虚拟交换机 |

容器删了可写层就没了，数据要留下来必须挂卷或绑定宿主机目录。

## 日常编排命令

项目里有 `docker-compose.yml` 时优先用 compose，它会按依赖顺序启动、自动建网络、统一管理生命周期。

```bash
# 构建（有改动才重建镜像）
docker compose build
# 只重建某个服务
docker compose build api

# 后台启动
docker compose up -d
# 启动并强制重建（改了 Dockerfile 必须加这个才生效）
docker compose up -d --build

# 停止（保留容器，下次 start 能恢复）
docker compose stop

# 停止并删除容器与网络（卷默认保留）
docker compose down
# 连卷一起删，数据会丢，慎用
docker compose down -v

# 重启某个服务
docker compose restart api

# 看状态与日志
docker compose ps
docker compose logs -f --tail=100 api
```

老版本命令是 `docker-compose`（带连字符），Docker Desktop 新版只提供插件形式 `docker compose`。

## 容器操作

```bash
docker ps                      # 运行中的容器
docker ps -a                   # 包含已退出的（排查崩溃必看）
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 进入容器，容器名可以用前三位唯一前缀
docker exec -it api /bin/sh    # 很多精简镜像没有 bash，用 sh
docker exec -it api env        # 只想看环境变量，不必进交互

# 查看日志（容器已崩溃时用这个，不进容器）
docker logs --tail 200 -f api

# 查看容器详情：端口映射、挂载、网络、启动命令
docker inspect api --format '{{json .NetworkSettings.Ports}}'
docker inspect api --format '{{json .Mounts}}'

# 容器内进程与资源
docker top api
docker stats                   # 实时 CPU/内存/网络
```

## 镜像与清理

```bash
docker images                              # 本地镜像
docker image prune -f                      # 删除悬空镜像（<none>）
docker system df                           # 先看空间被谁占了，再决定删什么
docker system prune -a --volumes           # 清空一切未使用资源，会删卷，慎用
```

排查「磁盘满了」的正确顺序是 `docker system df` → 看是镜像、容器、卷还是构建缓存占的 → 再定向清理。直接 `prune -a` 在共享服务器上可能删掉别人正在用的镜像。

## 端口与网络

```bash
# -p 宿主机端口:容器端口
docker run -d --name web -p 8080:80 nginx

# 确认端口被谁占用（映射错了会「容器起来了但访问不了」）
lsof -i :8080
docker port web

# 同一 compose 网络内用服务名互相访问，不要写 localhost
# nginx.conf 里 proxy_pass http://api:3000; 而不是 127.0.0.1
```

`localhost` 在容器里指向容器自己，这是「容器内连不上数据库」最常见的原因。

## 一句话排查流程

容器起不来时按这个顺序，比反复改配置快：

```bash
docker compose ps                    # 状态是 Exit 还是 Up
docker compose logs --tail=200 api   # 看退出原因
docker inspect api --format '{{.State.ExitCode}}'   # 137 = 被 OOM kill，1 = 应用报错
docker run -it --entrypoint sh image:tag            # 绕过启动命令进容器看环境
```

退出码 137 通常是内存不够被 SIGKILL，不是代码异常；143 是收到 SIGTERM 正常退出。

## 常见误区

**很多人以为改了 Dockerfile 直接 `up -d` 就会生效**。不加 `--build` 时 compose 会复用已有镜像，改了等于没改。这是「为什么我的修改没生效」的第一大来源。

**很多人以为 `down` 会连数据一起删**。默认保留命名卷，`down -v` 才删。反过来，用 bind mount 挂宿主机目录时，删容器不会删宿主机文件。

**很多人以为 `docker ps` 看不到容器就是没启动**。已经崩溃退出的容器只在 `docker ps -a` 里，而且日志用 `docker logs` 仍能看到。

## 关联阅读

- [Docker Desktop 升级后 compose 命令丢失](./03-docker-compose突然不可用.md)
- [docker compose 配置 nginx SSL 证书](./02-docker-compose配置nginx证书.md)
- [04-工程化 索引](../README.md)
