# UI_UX_pro_max的使用

[UI UX Pro Max](https://ui-ux-pro-max-skill.nextlevelbuilder.io)

UI UX Pro Max 的使用方式很特别，它不是一个可以双击打开的软件，而是一个需要安装在你的AI编程助手（比如 Cursor、Claude Code）里的“技能包”。装上它之后，你的AI助手就像瞬间拥有了专业设计师的经验，生成的界面会好看和规范很多。

## 1、安装与集成

1/ 安装 CLI 工具：打开终端，运行以下命令进行全局安装
```bash
npm install -g uipro-cli
```

2/ 进入你的项目：用 cd 命令进入你的前端项目根目录（确保里面有 package.json 文件

3/ 为你的AI助手初始化：根据你使用的AI编程助手，运行对应的初始化命令。这个命令会在项目里生成一些配置文件，把“设计智库”接入进去
```bash
# cursor
uipro init --ai cursor

# Claude Code
uipro init --ai claude

# GitHub Copilot
uipro init --ai copilot

# trae
uipro init --ai trae

# Windsurf
uipro init --ai windsurf

# 支持所有助手
uipro init --ai all
```

## 2、与AI对话，生成专业设计

- 在 Cursor 中：在聊天框里，用斜杠命令开头，比如 `/ui-ux-pro-max 帮我设计一个SaaS产品的数据看板`
- 在 Claude Code 或其它助手中：直接说出你的需求，AI会自动判断是否启用这个技能。你也可以主动提示它，比如 `请使用 UI UX Pro Max 技能，为我创建一个医疗健康App的个人资料页面，技术栈是React Native`
- 在trae中，必须切换到SOLO模式。