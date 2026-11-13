# PowerShell 策略问题

## 更改 PowerShell 执行策略

1. 以管理员身份打开 PowerShell

2. 查看当前的执行策略（可选）：

```bash
Get-ExecutionPolicy
# Restricted（禁止）
```

3. 更改执行策略

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

- `-Scope CurrentUser` 参数表示只修改当前用户的策略，无需担心影响系统其他部分，非常安全

4. 确认更改

    > 系统会提示你是否要更改执行策略。输入 Y（代表“是”）然后按回车键确认

5. 验证并测试

- 关闭所有 PowerShell 和 VS Code 窗口，重新打开一个新的 PowerShell 窗口。
- 再次输入 npm -v，现在应该就能正常显示 npm 的版本号了。
