# docker常用命令

```bash
# 构建
docker-compose build

# 后台运行
docker-compose up -d

# 停止
docker-compose stop

# 停止并删除
docker-compose down

# 重启
docker-compose restart

# 查看容器列表
docker ps

# 进入容器
docker exec -it xxx(容器名，可以是前三位) /bin/bash
```
