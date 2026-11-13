# tkinter 编写的程序如何打包成桌面软件

## 打包之前或者开发时注意事项

### 资源路径的写法

1/ `config.py`

```py
import os
import sys

# 判断是否被 PyInstaller 打包
if getattr(sys, "frozen", False):
    # PyInstaller 打包后
    BASE_DIR = sys._MEIPASS
else:
    # 源码运行
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 资源目录
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(ASSETS_DIR, "data")

# 错误写法，此写法在开发阶段有效，打包后无效
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# ASSETS_DIR = os.path.join(BASE_DIR, "assets")
# DATA_DIR = os.path.join(BASE_DIR, "assets/data")
```

2/ 使用

```py
candidate = os.path.join(ASSETS_DIR, f"{idx+1}.jpg")
```

## 打包到 Windows（.exe）

### 使用 PyInstaller

PyInstaller 是最常用的工具，支持 Tkinter、PIL、pandas 等大部分库。

1/ 安装 pyinstaller

```bash
pip install pyinstaller
```

2/ 打包命令

ps: 记得切换至py程序根目录

```bash
pyinstaller --onefile --windowed --add-data "assets;assets" main.py

python -m PyInstaller --onefile --windowed -i faicon.ico -n "锻件图卡计算器" --add-data "assets:assets" main.py
pyinstaller --onefile --add-data "assets;assets" main.py
pyinstaller --onefile --windowed --add-data "assets;assets" main.py
pyinstaller --onefile --windowed -i faicon.ico -n "锻件图卡计算器" --add-data "assets:assets" main.py
```

解释：
- `--onefile` → 打包成单个可执行文件。
- `--windowed` → 不显示控制台（适合 GUI 程序）。
- `--add-data "assets;assets"` → 如果使用了 图片、字体或其他资源文件，需要在打包时指定：Windows 路径用分号 `;` 分隔，mac/Linux 用冒号 `:`  "源路径;目标路径"
- `-i` → 设置应用图标
- `-n` → 设置应用名称

3/ 生成结果

- 打包完成后，在 dist/ 目录下会生成 main.exe。
- 所有依赖会被打包进去。

## 打包到 macOS（.app）

### 1/ 使用 PyInstaller

PyInstaller 同样支持 macOS，但要在 mac 上打包 mac.app，不能在 Windows 上生成。

1/ 安装 PyInstaller

```bash
pip3 install pyinstaller
```

2/ 打包命令

ps: 记得切换至py程序根目录

```bash
pyinstaller --onefile --windowed --add-data "assets:assets" main.py
```

生成的 .app 会在 dist/ 下，比如：`dist/main.app`

注意事项:
- macOS 需要在 本机打包（因为跨平台打包 .app 很难）。
- 如果使用了图片、资源文件，也需要 --add-data "assets:assets"。

### 2/ py2app

macOS 专用打包工具。

1/ 安装 PyInstaller

```bash
pip3 install py2app
```

2/ 创建 `setup.py`

```py
from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'PIL', 'pandas'],  # 需要的库
    'iconfile': 'icon.icns',  # 可选图标
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

3/ 打包命令

```bash
python3 setup.py py2app
```

打包完成后，应用在 `dist/` 下。
