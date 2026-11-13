# mac 按照了桌面docker，之前可以正常使用docer-compose 可最近使用不了了

报错：
`zsh: command not found: docker-compose`

因为桌面docker包中不再包含docker-compose.
查看路径：`Application/Contents/Resource/bin`

解决方法
```shell
sudo ln -sf /Applications/Docker.app/Contents/Resources/cli-plugins/docker-compose /usr/local/bin/docker-compose
```