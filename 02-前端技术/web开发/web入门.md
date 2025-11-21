# web入门

## 环境安装

### 1、安装代码编辑器

推荐：[Visual Studio Code（VS Code）](https://code.visualstudio.com) <br>
推荐理由：免费、轻量、功能强大，拥有及其丰富的插件生态系统 <br>
必要的插件（可选）： <br>
- Chinese (Simplified) Language Pack：中文汉化包。
- Live Server：一键启动一个本地开发服务器，代码修改后浏览器自动刷新。
- Prettier - Code formatter：代码自动化格式化工具，保持代码风格统一。
- Auto Rename Tag：自动修改配对的 HTML 标签。
- ESLint：代码质量检查工具，帮你发现潜在错误。
- JavaScript (ES6) code snippets：提供常用的 JavaScript 代码片段。

### 2、安装现代浏览器

推荐：[Google Chrome](https://www.google.com/chrome) (国内可能访问不了，可自行寻找资源下载) <br>
推荐理由：拥有强大的开发者工具，是前端调试的利器 <br>
学习使用开发者工具：
- 在网页上右键点击，选择“检查”或按 F12 即可打开。
- 学会使用 Elements 面板查看和修改 HTML/CSS
- 学会使用 Console 面板查看 JavaScript 输出和错误
- 学会使用 Sources 面板调试 JavaScript

### 3、安装 Node.js 和 npm


[Node官网](https://nodejs.org/zh-cn)<br>
这是现代前端开发的核心环境。npm (Node Package Manager) 会随着 Node.js 一起安装。<br>
强烈建议下载 LTS (长期支持版)，它更稳定。<br>
验证安装：<br>
```bash
# 在终端中执行以下命令。正确显示对应版本号即表示成功
node -v
npm -v
```

配置 npm（可选但推荐）：<br>
```bash
# 设置全局安装路径（避免使用系统权限）
mkdir ~/.npm-global
npm config set prefix ‘~/.npm-global'

# 将新路径添加到系统环境变量 PATH 中（具体方法请根据你的操作系统搜索）
# 例如，在 ~/.bashrc 或 ~/.zshrc 文件中添加：export PATH=~/.npm-global/bin:$PATH

# 更换淘宝镜像源（国内用户推荐，大幅加速下载）
npm config set registry https://registry.npmmirror.com/
```

yarn安装（可选）：<br>
```bash
npm install -g yarn
# 验证安装
yarn -v
```
yarn基础使用：
```bash
# 初始化新项目（会创建 package.json）
yarn init
# 或者使用默认配置快速初始化
yarn init -y

# 包管理

# 安装所有依赖（类似于 npm install）
yarn install
# 或简写
yarn

# 添加生产依赖
yarn add [package-name]
# 例如：yarn add vue

# 添加开发依赖
yarn add [package-name] --dev
# 或简写
yarn add -D [package-name]
# 例如：yarn add -D typescript

# 全局安装
yarn global add [package-name]

# 移除包
yarn remove [package-name]

# 更新包
yarn upgrade [package-name]

# 更新所有包
yarn upgrade
```

Yarn 与 npm 命令对比
| 功能 | npm 命令 | Yarn 命令 |
| -- | -- | -- |
| 初始化项目 | npm init | yarn init |
| 安装所有依赖 | npm install | yarn install 或 yarn |
| 安装生产依赖 | npm install [package] | yarn add [package] |
| 安装开发依赖 | npm install --save-dev [package] | yarn add --dev [package] |
| 全局安装 | npm install -g [package] | yarn global add [package] |
| 卸载包 | npm uninstall [package] | yarn remove [package] |
| 更新包 | npm update [package] | yarn upgrade [package] |
| 运行脚本 | npm run [script] | yarn run [script] |

### 4、安装git

[Git官网](https://git-scm.com)<br>
Git 是分布式版本控制系统，用于代码的版本管理和团队协作。GitHub/GitLab 是基于 Git 的代码托管平台。

验证安装：<br>
```bash
git --version
```

基本全局配置：<br>
安装后，你需要设置你的用户名和邮箱，这样你的提交才会带有标识。
> 不一定需要真名和真实邮箱，但是为了有效标识，建议使用笔名和常用邮箱
```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱@example.com"
```

## 网页、网站、Web 服务器和搜索引擎的区别

### 网页（Web Page）
> 一份能够显示在 Web 浏览器上的文档，也常就被叫作“page”（页面）。这样的文档是使用 HTML 语言编写的。

### 网站（Web Site）
> 一个由许多网页组合在一起的集合，其中的网页常常以各种方式相互连接，通常称为“site”（站点）。

### Web 服务器（Web Server）
> 一个在互联网上托管网站的计算机。

### 搜索引擎（Search Engine）
> 搜索引擎是帮助你查找其他网页的网络服务，例如 Google、Bing、Yahoo、DuckDuckGo或百度。通常通过 Web 浏览器（例如，你可以直接在 Firefox、Chrome 等浏览器的地址栏中进行搜索引擎搜索）或通过网页（例如 bing.com 或 duckduckgo.com）访问搜索引擎。

## Web 是如何工作的：基础

当你访问网络时，从你的第一次交互（例如，在浏览器中输入网址（URL）并按下回车 Enter/Return）到操作结果呈现给你（例如，网站出现在你的浏览器中）之间，发生了很多事情：

1. 浏览器从存储资源的 Web 服务器中请求你想要访问的资源（例如，一个网页、一些数据、或图片或视频）。这些请求（以及产生的响应）是通过一种名为 HTTP（超文本传输协议）的技术来实现的，它使用动词语言（如 GET）来描述应该进行的操作。
2. 如果请求成功，Web 服务器会将包含所需资源的 HTTP 响应发送回 Web 浏览器。
3. 在某些情况下，请求的资源将触发更多 HTTP 请求，这将导致更多响应。例如：
> - 当网站加载时，最初会请求网站的首页主索引 HTML 文件。<br>
> - 当浏览器接收到该文件后会尝试解析，这个过程中可能找到发出更多请求的指令。如上所述，这些指令可能是用于嵌入的文件，例如图片、样式信息、脚本等。
4. 当所有资源请求完成后，Web 浏览器将按照要求解析和渲染它们，然后再将结果显示给用户。

## 代码编辑器的基本功能

1. 打开和编辑文件
2. 语法高亮
3. 代码补全/建议
4. 调试帮助
5. 搜索和替换
6. 使用扩展增强代码编辑器