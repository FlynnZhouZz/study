# git标签

## 查看标签
```shell
git tag              # 列出所有本地标签
git show <标签名>    # 查看标签详情
```
## 创建标签

**附注标签（Annotated Tag）**
```shell
git tag -a <标签名> -m "标签描述" [commit-hash]
# 示例
git tag -a v1.0.0 -m "正式发布版本 1.0.0"
```

**轻量标签（Lightweight Tag）**
```shell
git tag <标签名> [commit-hash]
# 示例
git tag v1.0.0          # 对当前提交打标签
git tag v1.0.0 abc1234  # 对指定提交（abc1234）打标签
```

## 推送标签到远端仓库
```shell
git push origin <标签名>
# 推送所有本地标签
git push origin --tags
# 示例
git push origin v1.0.0
```

## 删除标签
```shell
# 删除本地标签
git tag -d <标签名>
# 删除远端标签
git push origin --delete <标签名>
# 或
git push origin :refs/tags/<标签名>
# 示例
```

## 拉取远端标签
```shell
git fetch --tags
```
