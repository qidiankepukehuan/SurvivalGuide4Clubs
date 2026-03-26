---
name: build-guide
description: |
  项目启动、预览和构建指南。帮助用户启动开发服务器、预览书籍效果，以及生成 PDF/EPUB 输出文件。
  当用户询问如何运行项目、如何预览、或如何生成输出文件时触发此 skill。使用此 skill whenever the user asks how to run the project, build the book, generate PDF, preview, or start the dev server.
---

# Build and Preview Guide

项目启动、预览和构建指南 skill。

## 用途

帮助用户启动开发服务器、预览书籍效果，以及生成 PDF/EPUB 输出文件。

## 使用方法

当用户询问如何运行项目、如何预览、或如何生成输出文件时使用此 skill。

## 前置要求

### Node.js 环境

确保已安装 Node.js（建议 v18+）：

```bash
node --version
```

如果未安装，请前往 [Node.js 官网](https://nodejs.org/) 下载安装。

### 安装依赖

```bash
npm install
```

## 开发服务器

### 启动预览服务器

```bash
npm run preview
```

这将启动一个本地服务器，通常在 `http://localhost:3000` 或 `http://localhost:8080`，可以在浏览器中实时预览书籍效果。

### 监听文件变化自动刷新

```bash
npm run dev
```

或

```bash
npm run watch
```

## 构建输出

### 生成 PDF

```bash
npm run build:pdf
```

或使用 Vivliostyle CLI：

```bash
npx vivliostyle build --format pdf -o 幻协生存指南.pdf
```

生成的 PDF 文件会保存在当前目录或指定的输出目录。

### 生成 EPUB

```bash
npm run build:epub
```

或：

```bash
npx vivliostyle build --format epub -o 幻协生存指南.epub
```

### 同时生成 PDF 和 EPUB

```bash
npm run build
```

## 常用命令汇总

| 命令 | 说明 |
|------|------|
| `npm install` | 安装项目依赖 |
| `npm run preview` | 启动预览服务器 |
| `npm run dev` | 开发模式（监听文件变化） |
| `npm run build` | 构建所有格式 |
| `npm run build:pdf` | 仅构建 PDF |
| `npm run build:epub` | 仅构建 EPUB |

## vivliostyle.config.js 配置说明

构建行为由 `vivliostyle.config.js` 控制，关键配置项：

```javascript
export default defineConfig({
  title: "幻协生存指南",           // 书名
  author: "探索不了一点宇宙编辑部", // 作者
  language: "zh",                // 语言
  size: "185mm,260mm",           // 页面尺寸
  theme: ["./theme/custom.css"],  // 样式文件
  cover: { src: "./draft/cover.png" }, // 封面图片
  entry: [
    "./draft/front-cover.html",  // 入口文件列表
    "./draft/toc.html",
    "./draft/posts/前言.md",
    // ... 其他文章
  ],
  output: [
    "./幻协生存指南.pdf",         // 输出文件配置
    "./幻协生存指南.epub",
  ],
});
```

## 添加新文章后的步骤

1. **确保文章已添加到配置**：在 `vivliostyle.config.js` 的 `entry` 数组中添加新文章路径
2. **运行预览**：使用 `npm run preview` 查看效果
3. **构建输出**：使用 `npm run build` 生成最终文件

## 常见问题

### 预览页面不更新

尝试清除浏览器缓存，或重启预览服务器（Ctrl+C 后重新运行）。

### 构建失败

- 检查 `vivliostyle.config.js` 中的路径是否正确
- 确认所有引用的文件存在
- 检查是否有语法错误

### 图片不显示

- 确认图片路径正确（应为相对路径 `../photos/...`）
- 确认图片文件存在

## 相关 Skills

- `convert-document`: 将 docx/doc/markdown 转换为标准格式
- `project-architecture`: 项目架构概览
- `article-edit`: 文章文字校对与编辑
