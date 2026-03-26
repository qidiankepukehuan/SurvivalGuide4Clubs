---
name: convert-document
description: |
  将 docx/doc/markdown 文件转换为项目标准文章格式的工具。将外部文档转换为符合本项目规范的标准化文章。
  当用户请求将文档转换为标准格式时触发此 skill。使用此 skill whenever the user wants to convert a docx/doc/markdown file to the project's standard article format.
---

# Convert Document to Standard Article Format

将 docx/doc/markdown 文件转换为项目标准文章格式的 skill。

## 用途

将外部文档（docx/doc/markdown）转换为符合本项目规范的标准化文章。

## 使用方法

当用户请求将文档转换为标准格式时，使用此 skill。

## 执行步骤

### 1. 收集文章信息

向用户询问以下信息（如果文档中无法提取）：

- **文章标题** (title)
- **作者名称** (author)
- **作者学校/单位** (school)
- **发布日期** (date)，格式：YYYY-MM-DD，如果不确定则用当前日期
- **分类** (categories)，默认：`["幻协生存指南"]`
- **标签** (tags)，可选
- **文章所属章节/系列**（如果有）

### 2. 处理源文件

1. 如果是 **docx/doc** 文件：
   - **优先**：使用 `document-skills:docx` skill 读取文件内容
   - 如果 docx skill 不可用或无法处理，再使用 Python 脚本 `convert_document.py` 提取内容和图片
   - 脚本会自动从 docx 中提取内嵌图片并保存到 `draft/photos/{文章标题}/`

2. 如果是 **markdown** 文件：
   - 读取文件内容
   - 处理图片路径（用户需要提供图片或告知图片位置）

### 3. 生成标准格式文章

生成的文件保存到 `draft/posts/{文章标题}.md`，格式如下：

```yaml
---
title: {文章标题}
author: {作者名}
date: {日期}
categories:
  - {分类}
tags:
  - {标签}
---
<section class="article">
<header class="article-head">
<p class="article-author">文 / {作者名} ({学校})</p>
<h1 class="article-title">{文章标题}</h1>
</header>

<div class="article-body">
{文章内容}
</div>
</section>
```

### 4. 分析与筛选正文内容

在将内容写入文章之前，必须对提取的内容进行分析和筛选，确保正文只包含有意义的内容。

#### 4.1 需要过滤的内容

以下内容应该**排除**：

1. **空白段落**：空行、空段落
2. **重复内容**：与标题重复的段落、连续重复的句子
3. **页眉页脚**：文档的页眉页脚内容
4. **噪声符号**：连续的横线、分页符、空白字符
5. **脚注尾注**：除非是重要引用，否则过滤
6. **乱码内容**：无法识别的字符、无意义的符号组合
7. **元信息**：如 "字数：XXX"、"第 X 页" 等文档元信息

#### 4.2 筛选流程

对提取的每个段落进行以下判断：

1. **检查是否为空**：跳过纯空白段落
2. **检查长度**：过短（<5字）且无意义的段落可跳过
3. **检查重复**：跳过与前文完全重复的段落
4. **检查类型**：识别是标题、正文、列表、引用还是其他

#### 4.3 保留的内容类型

确保保留以下有效内容：

- **正文段落**：完整的叙述文字
- **标题**：各层级标题
- **列表**：有序/无序列表项
- **引用**：引用的内容
- **图片说明**：图片的描述文字
- **重要注释**：关键的补充说明

#### 4.4 输出筛选后的内容

将筛选后的内容按正确顺序写入 `<div class="article-body">` 中，每个段落之间用空行分隔。

**示例筛选过程：**

```
原始内容（来自 docx）：
├── 标题：如何管理社团
├── （页眉：仅供参考）
├── 第一段：社团管理是一门艺术...
├──
├── （重复标题）
├── 第二段：人员分工很重要...
├── [脚注1]
├──
├── 分割线
└── 筛选后：
├── 第一段：社团管理是一门艺术...
├── 第二段：人员分工很重要...
```

### 5. 处理图片

1. 图片保存位置：`draft/photos/{文章标题}/`
2. 在文章内容中使用相对路径：`../photos/{文章标题}/{图片名}.{扩展名}`
3. 图片命名建议使用有意义的名称，如 `图1.webp`、`现场照片.webp` 等

### 6. 更新 vivliostyle.config.js

在 `vivliostyle.config.js` 的 `entry` 数组中添加新文章：

```javascript
entry: [
  "./draft/front-cover.html",
  "./draft/toc.html",
  // ... 其他文章
  "./draft/posts/{文章标题}.md",  // 添加这一行
],
```

## 所需工具

### 优先方案：使用 Claude 官方 docx 技能

**强烈推荐**：如果环境中已有 `document-skills:docx` skill，优先使用它来读取 docx 文件，无需安装 Python 环境。

```bash
# 调用 docx skill 读取文件
/document-skills:docx
```

### 备选方案：使用 Python 脚本

如果没有 docx skill，则使用 Python 脚本：

- **Python 3.8+**
- **python-docx** 库：用于读取 docx 文件
- **Pillow** 库：用于处理图片
- 如果没有环境，请使用 uv 创建虚拟环境：
  ```bash
  uv venv
  uv pip install python-docx Pillow
  ```

## 注意事项

- 如果用户在转换过程中没有提供所有信息，引导用户补充
- 日期格式必须为 `YYYY-MM-DD`
- 作者信息格式为 `文 / 作者名 (学校)`
- 图片路径使用相对路径 `../photos/{文章名}/...`
- 确保图片目录存在后再保存图片
