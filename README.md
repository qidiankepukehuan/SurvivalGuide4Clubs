# 📖 社团生存指南 LaTeX 自动构建系统

本仓库是 **《社团生存指南》** 的自动化 PDF 生成系统。
通过 **LaTeX** 进行内容排版，并结合 **Python 构建流水线**，实现 Markdown → LaTeX → PDF 的全自动化流程。
每次在 GitHub 打 TAG 时，系统会自动生成最新 PDF 并发布到 Releases，方便社团成员下载和分发。

---

## 📂 项目结构

```
.
├── latex/                 # LaTeX 输出目录及章节
├── markdown/              # Markdown 源文件及图片
│   ├── chapters           # Markdown 文件
│   └── photos             # 图片资源
├── themes/                # LaTeX 模板文件
├── out/                   # PDF 输出及中间文件
├── main.py                # 构建主程序
├── pyproject.toml         # Python 项目配置
├── uv.lock                # uv 构建锁文件
└── README.md
```

---

## ✨ 功能亮点

* 📝 **Markdown → LaTeX 转换**
  使用 `pypandoc` 将 Markdown 文件转换为 LaTeX 章节文件。

* 🖼️ **图片复制**
  自动将 Markdown 中的 `photos/` 复制到 LaTeX 目录，保证 PDF 中图片可引用。

* 🔄 **文本替换**
  可批量替换 LaTeX 文本，例如将所有 `\begin{figure}` 替换为 `\begin{figure}[H]`。

* 🎨 **主题文件整合**
  自动复制 `themes/` 中模板文件（如 `preamble.tex`、`cover.tex`）到 LaTeX 目录。

* 📑 **生成 main.tex**
  自动生成 `main.tex` 并插入所有章节。

* 🖨️ **PDF 构建**
  使用 `xelatex` 两轮编译生成最终 PDF。

* 🧹 **中间文件整理**
  将构建过程产生的中间文件移动到 `out/temp/`，保持输出目录整洁。

---

## ⚙️ 安装依赖

确保已安装：

* Python 3.13+
* LaTeX（支持 XeLaTeX）
* Pandoc

安装 Python 包依赖：

```bash
pip install -r requirements.txt
```

`requirements.txt` 可包含：

```
pypandoc
argparse
```

---

## 🚀 使用说明

在项目根目录运行：

```bash
python main.py
```

可选参数：

* `--skip-md`：跳过 Markdown → LaTeX 转换
* `--skip-pdf`：跳过 PDF 构建
* `--only-step STEP_NAME`：只执行指定步骤（如 `convert_markdown_to_latex`）

**示例**：

```bash
python main.py --skip-md
python main.py --only-step build_pdf
```

---

## 🔄 构建流程

1. 🧹 清理 `latex/` 目录
2. 📝 Markdown → LaTeX
3. 🖼️ 复制图片资源
4. 🔄 批量文本替换
5. 🎨 复制主题文件
6. 📑 生成 `main.tex`
7. 🖨️ 构建 PDF
8. 🧹 整理中间文件

流水线通过 **链式声明**完成，可根据需要跳过或单独执行某一步。

---

## 📤 输出文件

* `out/main.pdf`：最终生成的 PDF
* `out/temp/`：中间文件，包括 `.aux`、`.log` 等

---

## 🤖 自动化发布

在 GitHub Actions 中可配置每次打 TAG 自动运行构建脚本，并将 `main.pdf` 上传到 Releases，方便社团成员获取最新版本。

---

## 💡 贡献与维护

* 📝 Markdown 内容更新 → `markdown/` 文件夹
* 🖼️ 图片资源 → `markdown/photos/`
* 🎨 LaTeX 样式修改 → `themes/`

通过 `main.py` 统一构建 PDF，无需手动操作 LaTeX。
