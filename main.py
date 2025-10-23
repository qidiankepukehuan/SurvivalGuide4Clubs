#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
import subprocess
from pathlib import Path
import pypandoc
import argparse


class LatexBuilder:
    """LaTeX 构建流水线类（链式声明式构建）"""

    def __init__(self):
        # 路径配置
        self.MARKDOWN_DIR = Path("./markdown")
        self.THEME_DIR = Path("./themes")
        self.LATEX_DIR = Path("./latex")
        self.CHAPTERS_DIR = self.LATEX_DIR / "chapters"
        self.OUTPUT_DIR = Path("./out")
        self.TEMP_DIR = self.OUTPUT_DIR / "temp"
        self.TEMPLATE_PATH = self.THEME_DIR / "article.tex"

        for directory in [self.CHAPTERS_DIR, self.OUTPUT_DIR, self.TEMP_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

        # 构建队列
        self.pipeline = []
        self.args = None

    # =====================================================
    # 参数注入
    # =====================================================
    def set_args(self):
        """解析命令行参数并保存"""
        parser = argparse.ArgumentParser(description="LaTeX 构建流水线工具")
        parser.add_argument("--skip-md", action="store_true", help="跳过 Markdown → LaTeX 转换")
        parser.add_argument("--skip-pdf", action="store_true", help="跳过 PDF 构建")
        parser.add_argument("--only-step", type=str, default=None,
                            help="仅执行指定步骤（如：convert_markdown_to_latex）")
        self.args = parser.parse_args()
        return self

    # =====================================================
    # Step 注册器（用于链式声明）
    # =====================================================
    def _register(self, func):
        """注册步骤而非立即执行"""
        self.pipeline.append(func)
        return self

    # =====================================================
    # Step 0: 清理 LaTeX 目录
    # =====================================================
    def clean_latex_dir(self):
        return self._register(self._do_clean_latex_dir)

    def _do_clean_latex_dir(self):
        print("[STEP] 清理 latex 目录 ...")
        if self.LATEX_DIR.exists():
            for item in self.LATEX_DIR.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                    print(f"[INFO] 删除目录: {item}")
                elif item.is_file():
                    item.unlink()
                    print(f"[INFO] 删除文件: {item}")
        else:
            self.LATEX_DIR.mkdir(parents=True)
            print(f"[INFO] 已创建目录: {self.LATEX_DIR}")
        print("[DONE] LaTeX 目录清理完成。\n")

    # =====================================================
    # Step 1: Markdown → LaTeX
    # =====================================================
    def convert_markdown_to_latex(self):
        return self._register(self._do_convert_markdown_to_latex)

    def _do_convert_markdown_to_latex(self):
        if self.args and self.args.skip_md:
            print("[SKIP] 跳过 Markdown 转换。\n")
            return
        print("[STEP] 转换 Markdown → LaTeX ...")
        self.CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
        for md_file in sorted(self.MARKDOWN_DIR.glob("*.md")):
            file_id = md_file.stem
            output_tex = self.CHAPTERS_DIR / f"{file_id}.tex"
            print(f"[INFO] 转换: {md_file} → {output_tex}")
            pypandoc.convert_file(
                source_file=str(md_file),
                to="latex",
                format="markdown",
                outputfile=str(output_tex),
                extra_args=[
                    f"--template={self.TEMPLATE_PATH}",
                    "--standalone",
                    "--variable", "graphics-width=0.8\\textwidth",
                ],
            )
        print("[DONE] Markdown 转换完成。\n")

    # =====================================================
    # Step 2: 复制图片
    # =====================================================
    def copy_photos(self):
        return self._register(self._do_copy_photos)

    def _do_copy_photos(self):
        if self.args and self.args.skip_md:
            print("[SKIP] 跳过图片复制（因跳过 Markdown 转换）。\n")
            return
        print("[STEP] 复制图片资源 ...")
        src_photos = self.MARKDOWN_DIR / "photos"
        dst_photos = self.LATEX_DIR / "photos"
        if src_photos.exists():
            if dst_photos.exists():
                shutil.rmtree(dst_photos)
            shutil.copytree(src_photos, dst_photos)
            print(f"[INFO] 复制图片目录: {src_photos} → {dst_photos}")
        else:
            print("[WARN] 未找到 markdown/photos，跳过。")
        print("[DONE] 图片复制完成。\n")

    # =====================================================
    # Step 3: 替换文本
    # =====================================================
    def replace_in_tex(self, pattern, replacement):
        return self._register(lambda: self._do_replace_in_tex(pattern, replacement))

    def _do_replace_in_tex(self, pattern, replacement):
        print(f"[STEP] 执行批量文本替换: '{pattern}' → '{replacement}'")
        modified_count = 0
        for tex_file in self.LATEX_DIR.rglob("*.tex"):
            text = tex_file.read_text(encoding="utf-8")
            if pattern in text:
                tex_file.write_text(text.replace(pattern, replacement), encoding="utf-8")
                modified_count += 1
                print(f"[INFO] 修改文件: {tex_file}")
        print(f"[DONE] 替换完成，共修改 {modified_count} 个文件。\n")

    # =====================================================
    # Step 4: 复制主题文件
    # =====================================================
    def copy_theme_files(self):
        return self._register(self._do_copy_theme_files)

    def _do_copy_theme_files(self):
        print("[STEP] 复制主题文件 ...")
        for name in ["preamble.tex", "cover.tex"]:
            src = self.THEME_DIR / name
            dst = self.LATEX_DIR / name
            if src.exists():
                shutil.copy(src, dst)
                print(f"[INFO] 复制主题文件: {src} → {dst}")
            else:
                print(f"[WARN] 未找到 {name}，跳过。")
        print("[DONE] 主题文件复制完成。\n")

    # =====================================================
    # Step 5: 生成 main.tex
    # =====================================================
    def generate_main_tex(self):
        return self._register(self._do_generate_main_tex)

    def _do_generate_main_tex(self):
        print("[STEP] 生成 main.tex ...")
        src_main = self.THEME_DIR / "main.tex"
        dst_main = self.LATEX_DIR / "main.tex"

        if not src_main.exists():
            raise FileNotFoundError("未找到 themes/main.tex 模板文件。")

        main_text = src_main.read_text(encoding="utf-8")
        chapter_inputs = []
        for tex_file in sorted(self.CHAPTERS_DIR.glob("*.tex")):
            relative_path = tex_file.relative_to(self.LATEX_DIR)
            chapter_inputs.append(
                f"\\input{{{relative_path.with_suffix('').as_posix()}}}\n\\vspace*{{1cm}}"
            )

        block = "\n".join(chapter_inputs)
        if "% 文章导入" in main_text:
            main_text = main_text.replace("% 文章导入", f"% 文章导入\n{block}")
        else:
            print("[WARN] main.tex 模板中未找到 '% 文章导入'，已自动追加。")
            main_text += "\n" + block

        dst_main.write_text(main_text, encoding="utf-8")
        print(f"[DONE] main.tex 生成完成: {dst_main}\n")

    # =====================================================
    # Step 6: 构建 PDF
    # =====================================================
    def build_pdf(self):
        return self._register(self._do_build_pdf)

    def _do_build_pdf(self):
        if self.args and self.args.skip_pdf:
            print("[SKIP] 跳过 PDF 构建。\n")
            return
        print("[STEP] 调用 xelatex 构建 PDF ...")
        for i in range(2):
            print(f"[INFO] 第 {i + 1} 次编译 ...")
            subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-output-directory", "../out", "main.tex"],
                cwd=str(self.LATEX_DIR),
                check=True,
            )
        print(f"[DONE] PDF 构建完成: {self.OUTPUT_DIR / 'main.pdf'}\n")

    # =====================================================
    # Step 7: 清理中间文件
    # =====================================================
    def clean_temp(self):
        return self._register(self._do_clean_temp)

    def _do_clean_temp(self):
        print("[STEP] 整理输出目录 ...")
        for file in self.OUTPUT_DIR.iterdir():
            if file.is_file() and file.suffix.lower() != ".pdf":
                shutil.move(str(file), self.TEMP_DIR / file.name)
                print(f"[INFO] 移动中间文件: {file.name} → temp/")
        print("[DONE] 输出目录整理完成。\n")

    # =====================================================
    # Step 8: 统一执行
    # =====================================================
    def run(self):
        """顺序执行所有已注册步骤"""
        print("========== LaTeX Builder 流水线启动 ==========\n")
        if self.args and self.args.only_step:
            step_name = self.args.only_step
            found = False
            for func in self.pipeline:
                if func.__name__ == step_name or func.__name__.endswith(step_name):
                    func()
                    found = True
                    break
            if not found:
                print(f"[ERROR] 未找到步骤: {step_name}")
        else:
            for func in self.pipeline:
                func()
        print("========== 所有流程执行完毕 ==========\n")
        return self


# =========================================================
# 🔸 主流程调用入口
# =========================================================
if __name__ == "__main__":
    (
        LatexBuilder()
        .set_args()
        .clean_latex_dir()
        .convert_markdown_to_latex()
        .copy_photos()
        .replace_in_tex("\\begin{figure}", "\\begin{figure}[H]")
        .copy_theme_files()
        .generate_main_tex()
        .build_pdf()
        .clean_temp()
        .run()
    )