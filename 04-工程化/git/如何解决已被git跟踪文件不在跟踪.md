# 如何解决已被git跟踪文件不在跟踪

## 问题描述

在项目中，一开始有某个文件（如: .DS_Store）被git跟踪提交过，但后续我想使git不在跟踪这个文件。可当我在`.gitignore`中配置这个文件之后，git还是会跟踪这个文件的变化。

## 解决方法

1. 检查哪些 .DS_Store 还在 git 跟踪中:

```bash
# 这条命令会列出所有被 git 跟踪的 .DS_Store 文件。
git ls-files | grep .DS_Store
```

2. 只对这些文件执行移除:

```bash
git rm --cached 路径/到/.DS_Store
```

也可以批量处理

```bash
git ls-files | grep .DS_Store | xargs git rm --cached
```

3. 提交

```bash
git commit -m "remove: tracked .DS_Store files"
```

这样就不会再有 .DS_Store 被 git 监听到变化了。之后新生成的 .DS_Store 会被 .gitignore 忽略，不再进入 git 跟踪。
