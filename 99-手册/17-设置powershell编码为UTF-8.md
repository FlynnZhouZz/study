# 设置powershell默认编码格式为UTF-8

查看当前powershell编码格式：
```bash
chcp 
```

- 936 = GBK
- 65001 = UTF-8

## 设置powershell默认编码格式为UTF-8

### 1、设置当前窗口编码格式为UTF-8
```bash
chcp 65001
```

### 3、设置powershell默认编码格式为UTF-8

1/ 打开 PowerShell 配置文件
```bash
notepad $PROFILE
```
如果提示路径不存在，先创建：
```bash
New-Item -ItemType File -Path $PROFILE -Force
notepad $PROFILE
```

2/ 写入下面这段
```text
chcp 65001 > $null
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [System.Text.UTF8Encoding]::new()
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
```

3/ 保存关闭并重新打开 PowerShell 验证
```bash
chcp
```