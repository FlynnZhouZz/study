# nginx和php-fpm通信问题导致网站页面空白

## 问题描述

> 宝塔搭建的服务器，一开始部署项目使用的是nginx+php。刚把nginx改成Apache测试一下东西，测试完后切换回nginx。这时就出现，之前网站打不开了，都是php项目。直接访问html可以正常访问，可访问php文件就空白页面。

## 问题分析

> 能正常访问html文件，表示nginx配置没问题。不能访问php，表示nginx和php-fpm的通信有问题。

## 解决方法

1、查看对应网站的配置文件`/www/server/panel/vhost/nginx/***.conf`；
2、查看配置php-fpm的结点
```conf
include enable-php-81.conf;
```
3、查看`include enable-php-81.conf`文件配置，路径`/www/server/nginx/conf/enable-php-81.conf`
```conf
location ~ [^/]\.php(/|$)
{
    try_files $uri =404;
    fastcgi_pass  unix:/tmp/php-cgi-81.sock;
    fastcgi_index index.php;
    include fastcgi.conf;
    include pathinfo.conf;
}
```

`fastcgi.conf`
```conf
fastcgi_param  HTTP_HOST          $host;
```
发现里面缺少`include fastcgi_params;`配置，修改后
```conf
fastcgi_param  HTTP_HOST          $host;
include fastcgi_params;
```