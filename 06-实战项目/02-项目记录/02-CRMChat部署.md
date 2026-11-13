# CRMChat 部署

> CRMChat（PHP 客服系统）跑在本机 `20108` 端口，前面挂 Nginx 做反向代理，并把 `/api_node/` 转发到 Node 服务。
>
> 这段配置解决三件事：① Node 接口与 PHP 应用同域，避免跨域；② WebSocket 升级头透传（客服需要长连接）；③ 静态资源短缓存、动态请求不缓存。

## 反向代理配置

```nginx
location ^~ /api_node/ {
    proxy_pass https://mail.go168.site/;
    proxy_ssl_server_name on;
    proxy_http_version 1.1;
    
    proxy_set_header Host mail.go168.site;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    proxy_buffering off;
    proxy_cache off;
}

location ^~ /
{
    proxy_pass http://127.0.0.1:20108;
    proxy_http_version 1.1;
    proxy_read_timeout 360s;   
    proxy_redirect off; 
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    # 站点有ssl一定要配置这个，要不然request->domain()无法获取到https而是http
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header REMOTE-HOST $remote_addr;
    
    add_header X-Cache $upstream_cache_status;
    #Set Nginx Cache

    set $static_fileHSrC8vxS 0;
    if ( $uri ~* "\.(gif|png|jpg|css|js|woff|woff2)$" )
    {
        set $static_fileHSrC8vxS 1;
        expires 1m;
    }
    if ( $static_fileHSrC8vxS = 0 )
    {
        add_header Cache-Control no-cache;
    }
}
```