# VMWare虚拟机安装

MacOS 系统安装 VMWare Fusion 13虚拟机来运行Windows系统。

## 步骤

### 1. 下载Windows iso文件

[官方下载 Windows11](https://www.microsoft.com/zh-cn/software-download/windows11)

- 下载适用于 x64 设备的 Windows 11 磁盘映像 (ISO)
- 选择: Windows 专业中文版
- 开始下载：需等待几秒钟
- 选择产品语言：简体中文
- 确认：需等待几秒钟，出现下载链接
- 下载：文件很大，需要时间

### 2. 下载 VMWare Fusion 13

[官方指导文档](https://knowledge.broadcom.com/external/article/368734/download-desktop-hypervisor-workstation.html)

- 访问[broadcom官网](https://www.broadcom.com)
- 注册/登录：使用邮箱
- 登录成功，进入个人中心
- [free-downloads](https://support.broadcom.com/group/ecx/free-downloads)
- 找到 VMware Fusion 或者搜索
- 选择VMWare Fusion 13，选择最新版本
- 下载，安装

### 3. 设置虚拟机

- 启动虚拟机
- 将 ISO 文件拖拽到虚拟机界面
- 一直下一步
- 启动，点击回车
- 安装系统

#### 网络连接问题：
> 一般情况下，虚拟机会自动设置网络连接，共享mac ip地址。当你使用了VPN(如： clashx)时，可能因为vpn的虚拟网卡占用了虚拟机的网络资源，导致VMWare的NAT服务启动失败，从而报出 无法连接诶到vmnet8的错误

如何解决：

方法1：切换虚拟机网络模式（最简单的长期方案）
> 虚拟机设置 - 网络适配器 - 桥接模式网络连接 - 自动检测 - 成功后 勾选 连接网络适配器

方法2：为 VMware 设置 ClashX 规则（推荐）
> 检查 ClashX 的配置，将 VMware Fusion 或其相关进程（如 vmware-vmx）加入规则，让这些流量直连（Direct）。

#### 共享文件、不能全屏展示

>  VMware Tools没有安装

- 虚拟机菜单栏 - 虚拟机 - 安装 VMWare Tools
- 按照不找安装即可
- 重启系统，共享文件和支持全屏展示都没有问题了