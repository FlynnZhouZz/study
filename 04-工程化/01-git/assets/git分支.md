# git分支

## 查看所有分支
```shell
git branch -a
```

- -a 显示 本地 + 远程 所有分支。
- 当前分支前会标有 *。

## 切换到已有分支
```shell
git checkout <分支名>
# Git 2.23+ 推荐
git switch <分支名>
```

## 创建并切换到新分支
```shell
git checkout -b <新分支名>
# 或
git switch -c <新分支名>
```

## 切换到远程分支
```shell
git checkout --track origin/<远程分支名>
# 或
git switch -t origin/<远程分支名>
```

## 删除本地分支
```shell
git branch -d <分支名>      # 安全删除（已合并的分支）
git branch -D <分支名>      # 强制删除（未合并的分支）
```
## 删除远程分支
```shell
git push origin --delete <远程分支名>
# 或
git push origin :<远程分支名>  # 旧语法
```

## 清理已合并的分支
```shell
git branch --merged | grep -v "main\|master\|*" | xargs git branch -d
```
> 删除所有 已合并到当前分支 的本地分支（排除 main/master 和当前分支）。
