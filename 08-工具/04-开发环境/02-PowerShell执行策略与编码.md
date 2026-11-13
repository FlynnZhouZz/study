# PowerShell 执行策略与编码设置

> Windows 上跑 npm / 脚本时最常遇到的两个问题：脚本被策略拦截，中文输出乱码。

## 一、执行策略（npm 报「无法加载文件，因为在此系统上禁止运行脚本」）

### 更改 PowerShell 执行策略

1. 以管理员身份打开 PowerShell

2. 查看当前的执行策略（可选）：

```powershell
Get-ExecutionPolicy
# Restricted（禁止）
```

3. 更改执行策略

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

- `-Scope CurrentUser` 只修改当前用户的策略，不影响系统其他部分，相对安全
- `RemoteSigned` 的含义：本地脚本可直接运行，从网络下载的脚本需要签名

4. 确认更改

> 系统会提示是否更改执行策略。输入 `Y` 然后回车。

5. 验证并测试

- 关闭所有 PowerShell 和 VS Code 窗口，重新打开一个新的 PowerShell 窗口
- 再次输入 `npm -v`，应该能正常显示版本号

## 二、默认编码改为 UTF-8（中文输出乱码）

### 1. 查看当前编码

```powershell
chcp
```

- `936` = GBK
- `65001` = UTF-8

### 2. 临时设置当前窗口

```powershell
chcp 65001
```

### 3. 永久生效（写入 profile）

打开 PowerShell 配置文件：

```powershell
notepad $PROFILE
```

如果提示路径不存在，先创建：

```powershell
New-Item -ItemType File -Path $PROFILE -Force
notepad $PROFILE
```

写入下面这段并保存：

```powershell
chcp 65001 > $null
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [System.Text.UTF8Encoding]::new()
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
```

重新打开 PowerShell，执行 `chcp` 验证是否变为 `65001`。

> 如果 VS Code 的集成终端仍乱码，检查 VS Code 设置里的 `terminal.integrated.defaultProfile.windows` 是否指向 PowerShell 7（`pwsh`）而非 Windows PowerShell 5.1。
