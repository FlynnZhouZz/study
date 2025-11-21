# 部署SPA项目，配置Nginx代理，解决跨域问题

## 解决方法

```nginx
server {
    # ... 其他配置 ...
    # location / {
    #     try_files $uri $uri/ /index.html;
    # }
    
    location /api/ {
        proxy_pass https://api.upay7777.com/api/;
    }
    location /adm/ {
        proxy_pass https://api.upay7777.com/adm/;
    }
}
```