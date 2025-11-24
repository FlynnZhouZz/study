# macOS M1 芯片 如何安装 py 和 tkinter

## 方法 1：使用官方 Python 安装包（推荐）

### 1. 下载 Python

```bash
# 访问官网下载：https://www.python.org/downloads/
# 选择 macOS 64-bit universal2 installer
# 或直接使用命令行下载
curl -O https://www.python.org/ftp/python/3.11.5/python-3.11.5-macos11.pkg
```

### 2. 安装 Python

-   双击下载的 .pkg 文件
-   按照安装向导完成安装
-   重要：确保勾选 "Install tkinter" 选项

### 3. 验证安装

```bash
python3 --version
pip3 --version
```

## 方法 2：使用 Homebrew（最推荐）

### 1. 安装 Homebrew

> 已安装请跳过此步骤

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. 安装 Python

```bash
# 更新 Homebrew
brew update

# 安装 Python（包含 tkinter）
brew install python-tk

# 或者单独安装
brew install python
```

### 3. 验证安装

```bash
python3 --version
```

## 验证 tkinter 安装

创建一个测试文件 `test_tkinter.py`：

```py
import tkinter as tk
from tkinter import ttk, messagebox

def test_tkinter():
    try:
        # 创建窗口
        root = tk.Tk()
        root.title("macOS M1 tkinter 测试")
        root.geometry("300x200")

        # 添加组件
        label = ttk.Label(root, text="✅ tkinter 安装成功！", font=("Arial", 14))
        label.pack(pady=20)

        def show_info():
            messagebox.showinfo("系统信息", f"Python: {tk.TkVersion}\nTcl/Tk: {tk.TclVersion}")

        info_btn = ttk.Button(root, text="显示版本", command=show_info)
        info_btn.pack(pady=10)

        quit_btn = ttk.Button(root, text="退出", command=root.quit)
        quit_btn.pack(pady=5)

        root.mainloop()

    except ImportError as e:
        print(f"❌ tkinter 导入失败: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")

if __name__ == "__main__":
    test_tkinter()
```

运行测试：

```bash
python3 test_tkinter.py
```

## 在 vscode 的虚拟环境(venv)中配置使用

### 1. 创建虚拟环境

方法 A：使用 VSCode 内置功能：

-   打开 VSCode
-   按 Cmd+Shift+P 打开命令面板
-   输入 "Python: Create Environment"
-   选择 "Venv"
-   选择 Python 3.14.0 解释器
-   选择依赖文件（requirements.txt 或手动选择）

方法 B：命令行创建

```bash
# 导航到项目目录
cd your-project-folder

# 创建虚拟环境
python3.14 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 验证 Python 版本
python --version
```
