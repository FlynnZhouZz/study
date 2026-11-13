# redis启动失败

## 问题描述

在宝塔面板上安装redis软件，启动时报错`启动失败,pid文件不存在:/www/server/redis/redis.pid`

具体报错：

```bash
Starting redis server...
sudo: Account or password is expired, reset your password and try again
sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper
sudo: unable to change expired password: Authentication token manipulation error
Starting redis success!

# 翻译
正在启动 Redis 服务器...
sudo：帐户或密码已过期，请重置密码并重试
sudo：需要终端才能读取密码；请使用 -S 选项从标准输入读取密码，或配置 askpass 辅助程序
sudo：无法更改已过期的密码：身份验证令牌操作错误
Redis 启动成功！
```

## 原因分析

因为终端密码已过期，身份验证令牌失败导致。

## 解决方法 - 重置终端密码

需要当前密码才行

```bash
echo "newpassword" | sudo passwd --stdin $(whoami)

# 执行结果
[root@iZwz97x3mnk3ttqjq4xgzcZ ~]# echo "newpassword" | sudo passwd --stdin $(whoami)
sudo: Account or password is expired, reset your password and try again
Current password: 
New password: 
Retype new password: 
Changing password for user root.
passwd: all authentication tokens updated successfully.
```
