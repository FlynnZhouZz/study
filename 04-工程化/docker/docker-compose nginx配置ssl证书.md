# docker-compose nginx配置ssl证书

## 环境

1. windows10 专业版
2. docker-compose

## 思路

1. 生成自有ssl证书
2. docker对应网站配置ssl证书

## 生成自有ssl证书

### 安装openssl工具

**1、下载工具**
[openssl win64/win32](https://slproweb.com/products/Win32OpenSSL.html)

![openssl下载截图](assets/openssl_exe.png.png)

**2、安装工具**

建议傻瓜式安装，记住安装路径即可（路径: `C:\Program Files\OpenSSL-Win64`）<br />
如果选择非系统盘（C盘），请记住安装路径和勾选非系统盘选项

**3、校验安装是否完毕**

打开安装目录名，选择里面的`bin`目录打开命令行工具，输入`openssl version`，如正常显示版本即表示安装成功。

**4、配置环境变量**

我的电脑右键 - 属性 - 高级系统设置 - 高级/环境变量 - 系统变量 - 双击`Path` - 新建环境变量，将openssl安装的bin目录填写进去，确认即可

> 如果再安装/配置之前已经打开了命令行窗口或者powershell工具，需重启窗口再执行openssl命令

### 使用openssl工具生成自有证书

**1、生成证书**

进入lnmp的nginx目录，新建cert目录。
使用命令行工具，进入cert目录，执行如下命令生成ssl证书

```shell
openssl req -newkey rsa:2048 -nodes -keyout rsa_private.key -x509 -days 3650 -out cert.crt -subj "/C=CN/ST=GD/L=SZ/O=vihoo/OU=dev/CN=saas_api.com/emailAddress=123@qq.com"
```

解读：
1. `-days 3650`: 天数，这里是10年
2. `-subj`中的`CN`填写自己对应的域名或ip地址
3. `emailAddress`: 邮箱，不一定需要填写真实邮箱

### 配置nginx

**1、修改`docker-compose.yml`的nginx配置**

重要的修改点：
```yml
#映射端口
ports:
    - '80:80'
    - '81:80'
    - '443:443'
volumes:
    # ssl证书
    - ./nginx/cert:/etc/nginx/ssl
environment:
    - NGINX_HOST=saas_api.com
    - NGINX_EMAIL=admin@saas_api.com
```


**2、修改对应网站的vhost文件**
以`nginx/vhost/vhost_saas_api.conf`文件为例

重要修改点
```conf
listen       443 ssl;                        # 监听端口

ssl_certificate /etc/nginx/ssl/cert.crt;    # 对应的crt证书路径
ssl_certificate_key /etc/nginx/ssl/rsa_private.key;     # 对应的私钥文件路径

ssl_session_cache shared:SSL:1m;
ssl_session_timeout  10m;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers on;
```

**3、重新编译即可**

执行如下命令重新docker

```shell
docker-compose up -d
```