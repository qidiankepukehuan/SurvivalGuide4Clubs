# 幻协生存指南 (SurvivalGuide4Club)

## 简介

本仓库用于构建《幻协生存指南》PDF/EPUB出版物，一本面向高校科幻社团的经验手册。

内容以 Markdown 编写，使用 Vivliostyle 进行排版，最终输出为 PDF/EPUB 书籍。

## 目录结构

```
SurvivalGuide4Club/
├── .github/workflows/      # GitHub Actions 配置
├── draft/                  # 内容源文件
│   ├── posts/              # 文章 Markdown 文件
│   ├── photos/             # 文章配图
│   ├── fonts/              # 字体文件
│   ├── front-cover.html    # 封面
│   ├── back-cover.html     # 封底
│   └── toc.html            # 目录页
├── theme/                  # 样式文件
│   ├── custom.css          # 正文样式
│   ├── cover.css           # 封面样式
│   └── toc.css             # 目录样式
├── vivliostyle.config.js   # 构建配置
├── package.json            # 项目配置
└── README.md
```

## 技术栈

- [Vivliostyle CLI](https://github.com/vivliostyle/vivliostyle-cli) - CSS排版引擎
- Markdown - 内容格式
- pnpm - 包管理
- Chrome/Chromium - PDF生成

### 字体

字体文件位于 `draft/fonts/` 目录：
- **思源黑体 (Source Han Sans SC)** - 标题
- **思源宋体 (Source Han Serif SC)** - 正文
- **霞鹜文楷 (LXGW WenKai)** - 引用和脚注
- **得意黑 (Smiley Sans)** - 装饰性元素

## 快速开始

### 环境要求

- Node.js (ES Module)
- pnpm
- Chrome/Chromium

### 安装依赖

```bash
pnpm install
```

### 构建

```bash
pnpm build           # 默认构建
pnpm build:pdf       # 构建 PDF
pnpm build:epub      # 构建 EPUB
pnpm build:all       # 构建 PDF 和 EPUB
```

### 预览效果

```bash
pnpm preview
```

构建产物输出到项目根目录：`幻协生存指南.pdf`、`幻协生存指南.epub`

## 添加新文章

1. 在 `draft/posts/` 目录下创建新的 Markdown 文件
2. 在 `vivliostyle.config.js` 的 `entry` 数组中添加文章路径
3. 运行 `pnpm build` 构建预览

### 内容格式

文章头部需包含 front matter：

```markdown
---
title: 文章标题
author: 作者名
date: 2026-01-01
categories:
  - 分类名称
---
```

正文内容紧跟在 front matter 之后。

如需保持一致的排版样式，建议使用以下 HTML 结构：

```html
<section class="article">
  <header class="article-head">
    <p class="article-author">文 / 作者名 (院校)</p>
    <h1 class="article-title">文章标题</h1>
  </header>

  <div class="article-body">
    <!-- 正文内容 -->
  </div>
</section>
```

## 配置文件说明

### vivliostyle.config.js

主要配置项：

- `title` - 书籍标题
- `author` - 作者/编辑部
- `language` - 语言 (zh-CN)
- `size` - 纸张尺寸 (185mm x 260mm)
- `theme` - 样式文件路径
- `entry` - 文章入口文件列表
- `cover` - 封面图片路径

## 发布流程

打 tag 后会自动构建并上传到 GitHub Release：

```bash
git tag v1.0.0
git push origin v1.0.0
```

## 联系方式

- GitHub: https://github.com/qidiankepukehuan/SurvivalGuide4Clubs
- Email: tslbydyzbjb@qidian.space

## 特别鸣谢

本项目的编写、编辑与排版工作，得到了众多机构、组织及个人的支持与帮助。

**技术支持**
- 感谢 [Vivliostyle 开源社区](https://vivliostyle.org/) 为本项目提供排版技术支持

**字体支持**
- 感谢以下开源字体项目：思源黑体、思源宋体、霞鹜文楷、得意黑

**经验支持**
- 感谢高校幻协负责人联盟群在内容交流与经验共享方面提供的支持
- 感谢河流及[中文科幻数据库](https://csfdb.cn/)在资料整理与信息检索方面给予的帮助
- 感谢全国高校科幻社团在文章、经验与实践案例方面提供的支持

---

MIT License
