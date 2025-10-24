#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import shutil
import subprocess
from pathlib import Path
import pypandoc
import argparse
from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional

# -------- 新增：Step 数据结构 --------
@dataclass
class Step:
    name: str
    fn: Callable[["LatexBuilder"], None]                   # 接收 builder 实例
    tags: set[str] = field(default_factory=set)            # 例如 {"md"}, {"pdf"}, {"cleanup"}
    when: Callable[["LatexBuilder"], bool] = lambda _b: True  # 声明式条件

class LatexBuilder:
    """LaTeX 构建流水线类（更彻底的链式/声明式）"""

    def __init__(self):
        self.MARKDOWN_DIR = Path("./markdown")
        self.THEME_DIR = Path("./themes")
        self.LATEX_DIR = Path("./latex")
        self.CHAPTERS_DIR = self.LATEX_DIR / "chapters"
        self.OUTPUT_DIR = Path("./out")
        self.TEMP_DIR = self.OUTPUT_DIR / "temp"
        self.TEMPLATE_PATH = self.THEME_DIR / "article.tex"

        for directory in [self.CHAPTERS_DIR, self.OUTPUT_DIR, self.TEMP_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

        self.pipeline: list[Step] = []     # 现在管道里是 Step，而不是函数
        self.args = None

    # ---------------- 参数注入 ----------------
    def set_args(self, argv: Optional[list[str]] = None):
        """解析命令行参数并保存（新增多种流水线控制）"""
        parser = argparse.ArgumentParser(description="LaTeX 构建流水线工具")
        # 老选项（兼容）
        parser.add_argument("--skip-md", action="store_true", help="跳过 Markdown → LaTeX 转换")
        parser.add_argument("--skip-pdf", action="store_true", help="跳过 PDF 构建")
        parser.add_argument("--only-step", type=str, default=None,
                            help="仅执行指定步骤（兼容旧参数，等价于 --only）")

        # 新选项（声明式控制）
        parser.add_argument("--only", type=str, default=None,
                            help="只执行这些步骤名或标签，逗号分隔，如: --only=md,build_pdf")
        parser.add_argument("--skip", type=str, default=None,
                            help="跳过这些步骤名或标签，逗号分隔，如: --skip=cleanup")
        parser.add_argument("--from", dest="from_step", type=str, default=None,
                            help="从某一步开始（包含），按步骤名")
        parser.add_argument("--until", dest="until_step", type=str, default=None,
                            help="直到某一步结束（包含），按步骤名")
        parser.add_argument("--dry-run", action="store_true",
                            help="只打印计划，不执行")
        parser.add_argument("--on-error", choices=["stop", "continue"], default="stop",
                            help="遇到错误是停止还是继续后续步骤")
        self.args = parser.parse_args(argv)
        # 兼容：--only-step -> --only
        if self.args.only is None and self.args.only_step:
            self.args.only = self.args.only_step
        return self

    # ---------------- 注册器（现在带名字/标签/条件） ----------------
    def _register(self, func: Callable[["LatexBuilder"], None],
                  *, name: Optional[str] = None,
                  tags: Iterable[str] = (),
                  when: Optional[Callable[["LatexBuilder"], bool]] = None):
        step = Step(
            name=name or getattr(func, "__name__", "anon_step"),
            fn=func,
            tags=set(tags),
            when=when or (lambda _b: True),
        )
        self.pipeline.append(step)
        return self

    # ---------------- Step 0: 清理 LaTeX 目录 ----------------
    def clean_latex_dir(self):
        return self._register(
            LatexBuilder._do_clean_latex_dir,
            name="clean_latex_dir",
            tags={"init", "cleanup"},
        )

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

    # ---------------- Step 1: Markdown → LaTeX ----------------
    def convert_markdown_to_latex(self):
        return self._register(
            LatexBuilder._do_convert_markdown_to_latex,
            name="convert_markdown_to_latex",
            tags={"md"},
            when=lambda b: not getattr(b.args, "skip_md", False)
        )

    def _do_convert_markdown_to_latex(self):
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

    # ---------------- Step 2: 复制图片 ----------------
    def copy_photos(self):
        return self._register(
            LatexBuilder._do_copy_photos,
            name="copy_photos",
            tags={"md"},
            when=lambda b: not getattr(b.args, "skip_md", False)
        )

    def _do_copy_photos(self):
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

    # ---------------- Step 3: 替换文本（参数化，给定稳定名字） ----------------
    def replace_in_tex(self, pattern: str, replacement: str, *, name: Optional[str] = None):
        step_name = name or f"replace_in_tex:{pattern}=>{replacement}"
        return self._register(
            lambda b, p=pattern, r=replacement: b._do_replace_in_tex(p, r),
            name=step_name,
            tags={"text"},
        )

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

    # ---------------- Step 4: 复制主题文件 ----------------
    def copy_theme_files(self):
        return self._register(
            LatexBuilder._do_copy_theme_files,
            name="copy_theme_files",
            tags={"theme"},
        )

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

    # ---------------- Step 5: 生成 main.tex ----------------
    def generate_main_tex(self):
        return self._register(
            LatexBuilder._do_generate_main_tex,
            name="generate_main_tex",
            tags={"md", "theme"},
        )

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

    # ---------------- Step 6: 构建 PDF ----------------
    def build_pdf(self):
        return self._register(
            LatexBuilder._do_build_pdf,
            name="build_pdf",
            tags={"pdf"},
            when=lambda b: not getattr(b.args, "skip_pdf", False)
        )

    def _do_build_pdf(self):
        print("[STEP] 调用 xelatex 构建 PDF ...")
        for i in range(2):
            print(f"[INFO] 第 {i + 1} 次编译 ...")
            subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-output-directory", "../out", "main.tex"],
                cwd=str(self.LATEX_DIR),
                check=True,
            )
        print(f"[DONE] PDF 构建完成: {self.OUTPUT_DIR / 'main.pdf'}\n")

    # ---------------- Step 7: 清理中间文件 ----------------
    def clean_temp(self):
        return self._register(
            LatexBuilder._do_clean_temp,
            name="clean_temp",
            tags={"cleanup"},
        )

    def _do_clean_temp(self):
        print("[STEP] 整理输出目录 ...")
        for file in self.OUTPUT_DIR.iterdir():
            if file.is_file() and file.suffix.lower() != ".pdf":
                self.TEMP_DIR.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file), self.TEMP_DIR / file.name)
                print(f"[INFO] 移动中间文件: {file.name} → temp/")
        print("[DONE] 输出目录整理完成。\n")

    # ---------------- 统一执行：先选出“计划”，再执行 ----------------
    def _split_csv(self, s: Optional[str]) -> set[str]:
        if not s:
            return set()
        return {x.strip() for x in s.split(",") if x.strip()}

    def run(self):
        print("========== 规划执行计划 ==========")
        steps = [s for s in self.pipeline if s.when(self)]  # 先按 when 过滤

        # 名称/标签筛选
        only = self._split_csv(getattr(self.args, "only", None))
        skip = self._split_csv(getattr(self.args, "skip", None))
        if only:
            steps = [s for s in steps if (s.name in only) or (s.tags & only)]
        if skip:
            steps = [s for s in steps if not ((s.name in skip) or (s.tags & skip))]

        # 区间选择
        from_name = getattr(self.args, "from_step", None)
        until_name = getattr(self.args, "until_step", None)
        if from_name:
            try:
                idx = next(i for i, s in enumerate(steps) if s.name == from_name)
                steps = steps[idx:]
            except StopIteration:
                print(f"[WARN] --from 未找到步骤：{from_name}，忽略。")
        if until_name:
            try:
                idx = next(i for i, s in enumerate(steps) if s.name == until_name)
                steps = steps[: idx + 1]
            except StopIteration:
                print(f"[WARN] --until 未找到步骤：{until_name}，忽略。")

        # 打印计划
        for i, s in enumerate(steps, 1):
            tag_str = ",".join(sorted(s.tags)) or "-"
            print(f"{i:02d}. {s.name}  (tags={tag_str})")
        print("=================================\n")

        if getattr(self.args, "dry_run", False):
            print("[DRY RUN] 仅展示计划，不执行。")
            return self

        print("========== LaTeX Builder 流水线启动 ==========\n")
        on_error = getattr(self.args, "on_error", "stop")
        for s in steps:
            print(f"[RUN] {s.name}")
            try:
                s.fn(self)        # 统一调用（把 builder 传进去）
            except Exception as e:
                print(f"[ERROR] {s.name}: {e}")
                if on_error == "continue":
                    print("[INFO] 继续后续步骤 ...")
                    continue
                raise
        print("========== 所有流程执行完毕 ==========\n")
        return self

if __name__ == "__main__":
    (
        LatexBuilder()
        .set_args()
        .clean_latex_dir()
        .convert_markdown_to_latex()
        .copy_photos()
        .replace_in_tex("\\begin{figure}", "\\begin{figure}[H]", name="fix_figure_float")
        .copy_theme_files()
        .generate_main_tex()
        .build_pdf()
        .clean_temp()
        .run()
    )