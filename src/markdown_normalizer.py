"""
将 EU4 Wiki 爬取的混合格式文档归一化为标准 Markdown。

转换规则：
  1. [xxx]               → ## xxx
  2. [xxx] yyy           → ## xxx: yyy
  3. +N / −N 前缀行      → - 列表项
  4. | 表格块            → 补齐 Markdown 分隔行
  5. 连续空行            → 最多一个空行

用法：
  python src/markdown_normalizer.py              # 输出到 data_normalized/
  python src/markdown_normalizer.py --inplace    # 直接覆盖原文件
"""

import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUT_DIR = Path(__file__).parent.parent / "data_normalized"


# ─── 正则 ───

# 方括号标题: [xxx] 或 [xxx] yyy
RE_BRACKET_HEADER = re.compile(r"^\[(.+?)\](?:\s+(.*))?$")

# Markdown 标题
RE_MD_HEADER = re.compile(r"^==+\s+.+\s+==+$")

# +/- 数值前缀（+10%、−20%、+1、-5% 等，含 U+2212 减号）
RE_PLUS_MINUS = re.compile(r"^[+\−\-]\d")

# 判断一行是否属于表格（含 | 且不是注释/代码块）
RE_TABLE_LINE = re.compile(r"^\s*(?:\|\s*)?[^|]+\|")

# 表格行：含有 | 分隔符（不匹配纯分隔行 --- ）
# 要求 | 前后都有内容（或至少一侧有内容且不是纯 ---）
RE_PIPE_LINE = re.compile(r".+?\|.+")

# 检测当前行是否已经是 Markdown 分隔行（---|---|---）
RE_SEPARATOR = re.compile(r"^\s*\|?\s*-{3,}\s*(?:\|\s*-{3,}\s*)*\|?\s*$")


def is_blank(line: str) -> bool:
    return line.strip() == ""


def classify_table_block(lines: list[str], start: int) -> int:
    """检测从 start 开始的表格块，返回块结束索引（不包含）。"""
    end = start
    pipe_count = 0
    for i in range(start, len(lines)):
        if is_blank(lines[i]):
            if pipe_count >= 2:
                break  # 遇到空行且已有至少 2 行 pipe → 表格结束
            else:
                return start  # 空行但没有足够 pipe → 不是表格
        if RE_PIPE_LINE.search(lines[i]):
            pipe_count += 1
        elif pipe_count < 1:
            return start  # 还没见过 pipe 就遇到非 pipe 非空行 → 不是表格
        end = i + 1

    return end if pipe_count >= 2 else start


def has_separator_row(lines: list[str], start: int, end: int) -> bool:
    """检查表格块中是否已有分隔行。"""
    for i in range(start + 1, end):
        if RE_SEPARATOR.match(lines[i]):
            return True
    return False


def add_table_separator(lines: list[str], start: int, end: int):
    """在表格首行后插入分隔行（如果没有的话）。"""
    if end - start < 2:
        return  # 不足两行不处理
    if has_separator_row(lines, start, end):
        return

    # 根据首行的列数决定分隔行
    header = lines[start].strip()
    pipe_count = header.count("|")
    # 行首和行尾的 | 只是装饰，中间的 | 才是列分隔符
    # 列数 = 内部 | 数 + 1
    starts = 1 if header.startswith("|") else 0
    ends = 1 if header.endswith("|") else 0
    col_count = max(1, pipe_count + 1 - starts - ends)
    sep = " | ".join(["---"] * col_count)
    # 如果原行首尾有 |，分隔行也补齐
    if header.startswith("|"):
        sep = "| " + sep + " |" if header.endswith("|") else "| " + sep
    elif header.endswith("|"):
        sep = sep + " |"
    lines.insert(start + 1, sep)


def normalize_text(text: str) -> str:
    """归一化单个文档。"""
    # 先做全局替换
    text = text.replace("&nbsp;", " ")
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    # 去掉 HTML 属性残留
    text = re.sub(r'\b(?:align|valign|width|height|class|style|bgcolor)="[^"]*"\s*', "", text)
    text = re.sub(r"<br\s*/?>", " ", text)

    lines = text.split("\n")
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ── 跳过空行（后续会压缩） ──
        if is_blank(line):
            out.append("")
            i += 1
            continue

        # ── 方括号标题 ──
        m = RE_BRACKET_HEADER.match(stripped)
        if m:
            tag = m.group(1)
            rest = m.group(2)
            if rest:
                out.append(f"## {tag}: {rest}")
            else:
                out.append(f"## {tag}")
            i += 1
            continue

        # ── 已经是标准 Markdown 标题（== xxx ==） ──
        if RE_MD_HEADER.match(stripped):
            out.append(stripped)
            i += 1
            continue

        # ── 检测表格块 ──
        if RE_PIPE_LINE.search(line):
            end = classify_table_block(lines, i)
            if end > i:
                add_table_separator(lines, i, end)
                for j in range(i, end):
                    out.append(lines[j])
                i = end
                continue

        # ── +/- 数值前缀 → 列表项 ──
        if RE_PLUS_MINUS.match(stripped):
            out.append("- " + stripped.lstrip("+−\-"))
            i += 1
            continue

        # ── 普通行，原样保留 ──
        out.append(line)
        i += 1

    # ── 压缩连续空行 ──
    result = []
    prev_blank = False
    for line in out:
        if line == "":
            if not prev_blank:
                result.append(line)
            prev_blank = True
        else:
            result.append(line)
            prev_blank = False

    return "\n".join(result)


def normalize_file(src: Path, dst: Path):
    """归一化单个文件，保存到 dst。"""
    try:
        text = src.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  !! 读取失败: {src.name} ({e})")
        return False

    try:
        normalized = normalize_text(text)
    except Exception as e:
        print(f"  !! 归一化失败: {src.name} ({e})")
        return False

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(normalized, encoding="utf-8")
    return True


def normalize_all(inplace: bool = False):
    """遍历 data/ 下所有 .md，归一化后输出。"""
    src_root = DATA_DIR
    dst_root = src_root if inplace else OUT_DIR

    md_files = sorted(src_root.rglob("*.md"))
    if not md_files:
        print(f"!! 在 {src_root} 下没有找到 .md 文件")
        return

    ok = 0
    fail = 0
    for src in md_files:
        rel = src.relative_to(src_root)
        dst = dst_root / rel

        if normalize_file(src, dst):
            ok += 1
        else:
            fail += 1

    loc = "原文件" if inplace else dst_root
    print(f"\n完成: {ok} 个文件已归一化 -> {loc}")
    if fail:
        print(f"失败: {fail} 个文件")


def main():
    inplace = "--inplace" in sys.argv
    normalize_all(inplace=inplace)


if __name__ == "__main__":
    main()
