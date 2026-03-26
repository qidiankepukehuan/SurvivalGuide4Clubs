---
name: project-architecture
description: |
  项目架构概览。向用户介绍整个项目的结构、架构和工作流程，帮助用户理解如何贡献和维护这个项目。
  当用户询问项目结构、架构设计或如何参与项目时触发此 skill。使用此 skill whenever the user asks about the project structure, architecture, or how to contribute to the project.
---

# Project Architecture Overview

项目架构讲解 skill。

## 用途

向用户介绍整个项目的结构、架构和工作流程，帮助用户理解如何贡献和维护这个项目。

## 使用方法

当用户询问项目结构、架构设计或如何参与项目时使用此 skill。

## 项目结构

```
SurvivalGuide4Clubs/
├── .claude/                    # Claude Code 配置和 skills
│   └── skills/                 # 自定义 skills
│       ├── convert_document.md # 文档转换 skill
│       ├── convert_document.py # 转换脚本
│       ├── project-architecture.md
│       └── build-guide.md
├── vivliostyle.config.js       # Vivliostyle 构建配置
├── package.json                # Node.js 依赖配置
├── theme/                      # 样式主题目录
│   ├── custom.css             # 正文样式（双栏排版）
│   ├── cover.css               # 封面样式
│   └── toc.css                 # 目录样式
├── draft/                      # 稿件目录
│   ├── front-cover.html       # 封面页
│   ├── back-cover.html        # 封底页
│   ├── toc.html                # 目录页
│   ├── cover.png               # 封面图片
│   ├── posts/                  # 文章目录
│   │   ├── 前言.md
│   │   ├── 如何管理社团.md
│   │   └── ...
│   └── photos/                 # 图片资源
│       ├── 如何出摊/
│       └── 如何开展观星活动/
└── 输出文件/                    # 构建输出目录
    ├── 幻协生存指南.pdf
    └── 幻协生存指南.epub
```

## 技术栈

- **构建工具**: [Vivliostyle](https://vivliostyle.org/) - 支持 PDF/EPUB 生成
- **格式标准**: Markdown + HTML 混合格式
- **样式**: CSS（支持双栏排版、字体定制）
- **图片处理**: Python Pillow

## 文章格式规范

### 文件命名

- 文件名为中文标题：`前言.md`、`如何管理社团.md`
- 对应图片目录：`draft/photos/{文章标题}/`

### Front Matter (YAML)

```yaml
---
title: 文章标题
author: 作者名
date: 2026-01-17
categories:
  - 幻协生存指南
tags:
  - 标签1
  - 标签2
---
```

### HTML 包装结构

```html
<section class="article">
<header class="article-head">
<p class="article-author">文 / 作者名 (学校)</p>
<h1 class="article-title">文章标题</h1>
</header>

<div class="article-body>
...Markdown 内容...
</div>
</section>
```

### 内部链接

- 图片引用：`../photos/{文章名}/{图片名}.{扩展名}`
- 文章引用：`./posts/{文章名}.md`

## 样式系统

### 页面尺寸

- 尺寸：185mm × 260mm
- 页边距：上 18mm，下 20mm，左 16mm，右 16mm

### 排版规则

- 正文：双栏排版（column-count: 2），栏间距 5mm
- 字体：思源宋体（正文）、思源黑体（标题）
- 行距：1.8，首行缩进 2em

### 特殊样式

- 图片：自动编号，支持居中 (`.center` 类)
- 引用：霞鹜文楷字体
- 脚注：自动编号

## 工作流程

1. **撰写文章**：使用标准格式编写 Markdown
2. **添加图片**：放入对应 `draft/photos/{文章名}/` 目录
3. **更新配置**：在 `vivliostyle.config.js` 中添加文章入口
4. **构建输出**：生成 PDF/EPUB

## 配置文件说明

### vivliostyle.config.js

```javascript
export default defineConfig({
  title: "幻协生存指南",
  author: "探索不了一点宇宙编辑部",
  language: "zh",
  size: "185mm,260mm",
  theme: ["./theme/custom.css"],
  cover: { src: "./draft/cover.png" },
  entry: [
    "./draft/front-cover.html",
    "./draft/toc.html",
    "./draft/posts/前言.md",
    // ... 其他文章
  ],
});
```

## 相关 Skills

- `convert-document`: 将 docx/doc/markdown 转换为标准格式
- `build-guide`: 项目启动、预览、构建指南
- `article-edit`: 文章文字校对与编辑
