#!/usr/bin/env python3
"""重建各知识目录的 README.md 索引。

用法:
    python3 00-路线/tools/gen-index.py

规则:
- 只处理 SCAN_DIRS 中列出的目录，其他目录（含手写 README）不动。
- 带数字前缀的文件按编号排序，编号即推荐阅读顺序。
- 无编号文件归入「专题补充」，按文件名排序。
- 已存在手写 README 的目录通过 SKIP 跳过。
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 目录 -> (标题, 一句话说明)
SCAN_DIRS = {
    "01-计算机基础/01-计算机网络": ("计算机网络", "HTTP、TCP/IP、互联网如何运作——所有前端问题的物理底座。"),
    "01-计算机基础/02-浏览器原理": ("浏览器原理", "从输入 URL 到像素上屏，渲染流水线是性能优化的理论依据。"),
    "02-前端核心/01-web开发": ("Web 开发基础", "Web 是什么、URL 与域名、命令行与服务端的基本认知。"),
    "02-前端核心/02-html": ("HTML", "结构与语义。先搞清元素在表达什么，再谈样式。"),
    "02-前端核心/03-css": ("CSS", "从盒模型到布局，再到动画与响应式。编号即阅读顺序。"),
    "02-前端核心/04-javascript": ("JavaScript 核心", "语言内核。重点在 08-11 的执行机制与 32-35 的闭包原型内存。"),
    "02-前端核心/05-typescript": ("TypeScript", "类型系统与类型体操。"),
    "03-框架与跨端/01-react": ("React", "组件、Hooks、状态管理、Fiber 架构与性能优化。"),
    "03-框架与跨端/02-vue": ("Vue", "Vue2/Vue3 工程实践与后台管理系统搭建。"),
    "03-框架与跨端/03-react-native": ("React Native", "环境、原生模块、性能、证书与上架。"),
    "03-框架与跨端/04-android": ("Android 原生", "为 RN 原生模块开发服务的 Android 基础。"),
    "04-工程化/01-git": ("Git", "分支、标签、常见报错与仓库清理。"),
    "04-工程化/05-docker": ("Docker", "常用命令、compose 与 nginx 证书配置。"),
    "04-工程化/04-部署": ("部署", "Nginx 单页应用配置与跨域代理。"),
    "04-工程化/06-性能优化": ("性能优化", "从体系到单项实战：先建立指标，再动手优化。"),
    "04-工程化/03-测试": ("测试", "单测、组件测试、端到端的分工与选型。"),
    "04-工程化/07-微前端/01-qiankun": ("微前端 · qiankun", "微前端架构原理与子应用接入实战。"),
    "05-后端与数据/01-nodejs": ("Node.js", "运行时环境与版本兼容问题。"),
    "05-后端与数据/02-php": ("PHP", "ThinkPHP 业务实践、邮件轮询与服务器排查。"),
    "05-后端与数据/03-python": ("Python", "环境安装与 tkinter 桌面程序打包。"),
    "05-后端与数据/04-架构设计": ("架构设计", "权限模型等通用设计范式。"),
    "05-后端与数据/05-运维/01-宝塔": ("宝塔面板", "面板环境下的服务排障记录。"),
    "07-面试专项/01-面试": ("面试题库", "按技术栈分类的高频题库，与知识层目录一一对应。"),
    "07-面试专项/04-真实面试经历": ("真实面试经历", "以日期+公司命名的面试复盘，是校准准备方向的真实信号。"),
    "07-面试专项/01-面试/12-react专项": ("React 专项", ""),
    "07-面试专项/01-面试/13-reactnative专项": ("React Native 专项", ""),
    "07-面试专项/01-面试/14-过往面试总结": ("过往面试总结", "历史面试题与现场记录。"),
    "08-工具/01-n8n": ("n8n", "可视化工作流自动化平台。"),
    "08-工具/02-Trae": ("Trae", "AI 编辑器与 MCP 配置。"),
    "08-工具/03-UI_UX_pro_max": ("UI UX Pro Max", "设计规范生成工具的使用。"),
    "08-工具/04-开发环境": ("开发环境", "本机环境搭建与终端配置问题，Windows 侧居多。"),
    "06-实战项目/02-项目记录": ("项目记录", "真实项目的设计与实施记录。读的时候看「为什么这么做」，而不是抄代码。"),
    "01-计算机基础/03-操作系统": ("操作系统", "进程线程、虚拟内存、IO 模型、文件系统——解释「为什么快」的底层依据。"),
    "01-计算机基础/04-数据结构与算法/01-基础数据结构": ("基础数据结构", "数组链表、栈队列、哈希表、树与堆。每篇配手写实现与常考题型。"),
    "01-计算机基础/04-数据结构与算法/02-高级算法": ("高级算法", "排序、二分、回溯、动态规划、双指针。先记模板，再刷题。"),
    "01-计算机基础/04-数据结构与算法/03-leetcode刷题": ("LeetCode 刷题", "按专题的刷题记录与模板沉淀。"),
    "04-工程化/02-构建工具/02-webpack": ("webpack", "核心概念、构建流程与产物体积优化的实操层内容。"),
    "04-工程化/02-构建工具/03-vite": ("vite", "预构建、插件体系与生产构建的分包策略。"),
    "07-面试专项/02-面试八股": ("面试八股", "跨技术栈的通用追问：网络、浏览器、工程化。回答层次比结论更重要。"),
    "07-面试专项/03-算法面试题": ("算法面试题", "前端高频手写题与场景设计题，含回答框架而不只是代码。"),
}

# 手写 README 的目录，生成器不覆盖
SKIP = {"06-实战项目", "98-杂项", "99-手册", "01-计算机基础", "02-前端核心", "03-框架与跨端",
        "04-工程化", "05-后端与数据", "07-面试专项", "08-工具", "00-路线"}


def read_meta(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    lines = [l.strip() for l in text.split("\n")]
    # 跳过 YAML frontmatter
    if lines and lines[0] == "---":
        for i, l in enumerate(lines[1:], 1):
            if l == "---":
                lines = lines[i + 1:]
                break
    in_code = False
    prose = []
    for l in lines:
        if l.startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            prose.append(l)
    title = ""
    for l in prose:
        if l.startswith("# "):
            title = re.sub(r"`", "", l[2:]).strip()
            break
    if not title:
        title = os.path.splitext(os.path.basename(path))[0]
        title = re.sub(r"^\d+[-_]", "", title)  # 去掉文件名里的顺序前缀
    desc = ""
    # 约定：H1 之后的第一段引用块即「一句话说明」，优先级高于正文首句
    head = [l for l in prose if not l.startswith("#")]
    for l in head[:6]:
        if l.startswith(">"):
            quote = re.sub(r"[`*\[\]<>]", "", l.lstrip(">").strip()).strip()
            if len(quote) >= 8:
                desc = quote[:48] + ("…" if len(quote) > 48 else "")
                break
    code_hint = re.compile(r"^(if|for|while|const|let|var|function|return|class|import|export|new|def|async)\b|[;{}]|//|console\.|=>")
    for l in ([] if desc else prose):
        if not l or l.startswith(("#", "![", "|", "```", ">", "-", "*", "<", "//", "/*")):
            continue
        if re.match(r"^\d+[.、)]\s", l):  # 有序列表项，不是摘要
            continue
        plain = re.sub(r"[`*\[\]!<>]", "", l).strip()
        if len(plain) < 8 or code_hint.search(plain) or plain.count("(") > 1:
            continue
        desc = plain[:48]
        if len(plain) > 48:
            desc += "…"
        break
    return title, desc, round(len(text.encode()) / 1024, 1)


def num_key(fn):
    m = re.match(r"^(\d+)[-_\s.]", fn)
    return (0, int(m.group(1))) if m else (1, 0)


def link(fn):
    return "./" + fn.replace(" ", "%20")


def build(dirpath, title, intro):
    full = os.path.join(ROOT, dirpath)
    files = [f for f in os.listdir(full) if f.endswith(".md") and f != "README.md"]
    if not files:
        return None
    numbered = sorted([f for f in files if num_key(f)[0] == 0], key=lambda f: (num_key(f)[1], f))
    extra = sorted([f for f in files if num_key(f)[0] == 1])
    total_kb = sum(read_meta(os.path.join(full, f))[2] for f in files)

    out = [f"# {title}", ""]
    if intro:
        out += [f"> {intro}", ""]
    out += [f"共 **{len(files)}** 篇，约 {total_kb:.0f} KB。", ""]

    rows = []
    for i, f in enumerate(numbered, 1):
        t, d, kb = read_meta(os.path.join(full, f))
        rows.append(f"| {i:02d} | [{t}]({link(f)}) | {d or '—'} |")
    if extra and rows:
        out += ["## 主线（按编号顺序阅读）", "", "| # | 文档 | 要点 |", "|---|------|------|"]
        out += rows + [""]
        out += ["## 专题补充", "", "| 文档 | 要点 |", "|------|------|"]
        for f in extra:
            t, d, kb = read_meta(os.path.join(full, f))
            out.append(f"| [{t}]({link(f)}) | {d or '—'} |")
    elif rows:
        out += ["| # | 文档 | 要点 |", "|---|------|------|"] + rows
    else:
        out += ["| 文档 | 要点 |", "|------|------|"]
        for f in extra:
            t, d, kb = read_meta(os.path.join(full, f))
            out.append(f"| [{t}]({link(f)}) | {d or '—'} |")
    out.append("")
    return "\n".join(out)


def main():
    n = 0
    for d, (title, intro) in SCAN_DIRS.items():
        if d in SKIP:
            continue
        content = build(d, title, intro)
        if content is None:
            continue
        p = os.path.join(ROOT, d, "README.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        n += 1
        print(f"  更新 {d}/README.md")
    print(f"完成，共 {n} 个目录索引。")


if __name__ == "__main__":
    main()
