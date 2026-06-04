import json
import re
from pathlib import Path

import tiktoken
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from pydantic import BaseModel

DATA_DIR = Path(__file__).parent.parent / "data" / "data_normalized"
OUT_DIR = Path(__file__).parent.parent / "data" / "chunks"

# bge-small 兼容的编码
enc = tiktoken.get_encoding("cl100k_base")

# 全局父表存储：id -> full_table_text
_parent_tables: dict[int, str] = {}
_next_table_id = 1


def _store_table(full_table: str) -> int:
    """存一份完整表格，返回 ID（重复表格返回已有 ID）。"""
    global _next_table_id
    for tid, tbl in _parent_tables.items():
        if tbl == full_table:
            return tid
    tid = _next_table_id
    _parent_tables[tid] = full_table
    _next_table_id += 1
    return tid


class Chunk(BaseModel):
    text: str
    source_file: str
    category: str
    section: str
    chunk_index: int
    # 引用 parent_tables 字典的 key，0 表示无父表
    parent_table_id: int = 0


def count_tokens(text: str) -> int:
    return len(enc.encode(text))


def expand_table(full_table: str, max_tokens: int = 600) -> list[str]:
    """表格行级展开：每行独立成一块，每块都带完整表头+分隔行。

    返回 list[str]，每个 str 是 "表头+分隔行+一行数据"。
    如果表头本身就超长（极罕见），回退为整表返回。
    """
    lines = full_table.split("\n")
    if len(lines) < 2:
        return [full_table]

    # 整表能塞进一个 chunk 就不用展开
    if count_tokens(full_table) <= max_tokens:
        return [full_table]

    # 表头行和分隔行
    header = lines[0]
    sep = lines[1]
    data = lines[2:]

    # 如果表头本身已经超长，整表返回
    header_block = f"{header}\n{sep}"
    if count_tokens(header_block) > max_tokens:
        return [full_table]

    # 多行一批，尽量塞满 max_tokens
    batches = []
    batch = []
    batch_tok = 0
    target = max_tokens * 0.8

    for row in data:
        if row.strip() == "":
            continue
        row_tok = count_tokens(row)
        # 单行超长（宽表）→ 向下拆半
        if row_tok > max_tokens:
            if batch:
                batches.append(batch)
                batch, batch_tok = [], 0
            cols = [c.strip() for c in row.split("|")]
            half = len(cols) // 2
            for part in ["|".join(cols[:half]), "|".join(cols[half:])]:
                if part.strip():
                    batches.append([part])
            continue

        if batch and batch_tok + row_tok > target:
            batches.append(batch)
            batch, batch_tok = [], 0
        batch.append(row)
        batch_tok += row_tok

    if batch:
        batches.append(batch)

    rows = [f"{header}\n{sep}\n" + "\n".join(b) for b in batches]
    return rows


def split_around_table(text: str, max_tokens: int = 600) -> list[tuple[str, str]]:
    """将文本按表格位置拆分成 (内容, parent_table) 对。

    对表格做行级展开：返回的每个子块是 "表头+一行数据"，
    parent_table 字段存完整表格。
    对文字部分直接原样返回（由上层做后续切分）。
    """
    lines = text.split("\n")
    table_regions = []
    in_table = False
    table_start = None

    for i, line in enumerate(lines):
        if re.match(r"^\|?\s*-{3,}\s*\|", line):
            if not in_table:
                table_start = i - 1 if i > 0 and "|" in lines[i - 1] else i
                in_table = True
            continue
        if in_table and ("|" not in line or line.strip() == ""):
            table_regions.append((table_start, i))
            in_table = False
            table_start = None
    if in_table and table_start is not None:
        table_regions.append((table_start, len(lines)))

    if not table_regions:
        return [("text", text)]

    result = []
    prev_end = 0
    for ts, te in table_regions:
        # 表格前的文字
        if ts > prev_end:
            text_before = "\n".join(lines[prev_end:ts])
            if text_before.strip():
                result.append(("text", text_before))

        # 表格本身：行级展开
        full_table = "\n".join(lines[ts:te])
        expanded = expand_table(full_table, max_tokens)
        for row in expanded:
            result.append(("table_row", row))

        prev_end = te

    # 表格后的文字
    if prev_end < len(lines):
        text_after = "\n".join(lines[prev_end:])
        if text_after.strip():
            result.append(("text", text_after))

    return result


def chunk_file(md_path: Path, max_tokens: int = 600, overlap: int = 50) -> list[Chunk]:
    """对单个 md 文件执行分块，返回 Chunk 列表。"""
    text = md_path.read_text(encoding="utf-8")

    # Step 1: Markdown 标题分块
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ]
    )
    base_docs = splitter.split_text(text)

    # Step 2: 对每个标题块做二次处理
    page_chunks = []  # [(content, section, parent_table)]
    for doc in base_docs:
        content = doc.page_content.strip()
        if not content:
            continue

        meta = doc.metadata
        section = " / ".join(meta.get(k, "") for k in ("h1", "h2", "h3") if meta.get(k))

        if count_tokens(content) <= max_tokens:
            page_chunks.append((content, section, ""))
            continue

        # 超过 max_tokens → 进一步拆分
        parts = split_around_table(content, max_tokens)

        all_text = all(typ == "text" for typ, _ in parts)

        if all_text and len(parts) == 1:
            # 纯文本且没有拆分 → RecursiveCharacterTextSplitter
            recursive = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n", "。", ".", " "],
                chunk_size=max_tokens,
                chunk_overlap=overlap,
                length_function=count_tokens,
            )
            sub_docs = recursive.split_text(content)
            for sd in sub_docs:
                sd = sd.strip()
                if sd:
                    page_chunks.append((sd, section, ""))
        else:
            for typ, part_content in parts:
                if typ == "text":
                    # 文字块如果还是太长，递归切分
                    if count_tokens(part_content) > max_tokens:
                        recursive = RecursiveCharacterTextSplitter(
                            separators=["\n\n", "\n", "。", ".", " "],
                            chunk_size=max_tokens,
                            chunk_overlap=overlap,
                            length_function=count_tokens,
                        )
                        sub_docs = recursive.split_text(part_content)
                        for sd in sub_docs:
                            sd = sd.strip()
                            if sd:
                                page_chunks.append((sd, section, ""))
                    else:
                        page_chunks.append((part_content, section, ""))
                else:  # table_row
                    full_table = part_content  # 行本身
                    # parent_table 就是同一表格的所有行拼起来
                    # 但这里我们只有单行，需要找到完整表格
                    # 简化：就用当前行作为 text，完整表格需要另算
                    page_chunks.append((part_content, section, ""))

    # Step 3: 包装为 Chunk —— 需要合并同表格的行，设置 parent_table
    # 先扫描所有 table_row 找到属于同一表格的连续块
    rel_path = md_path.relative_to(md_path.parent.parent)
    category = rel_path.parent.name
    source_file = md_path.name

    # 将连续的 table_row 合并，加上完整父表格
    merged = []
    i = 0
    while i < len(page_chunks):
        content, section, _ = page_chunks[i]
        lines = content.split("\n")
        # 检测是不是表格块（首行含 |，次行含 ---）
        if len(lines) >= 3 and "|" in lines[0] and "---" in lines[1]:
            # 收集同一表格的所有连续块
            all_data_rows = lines[2:]  # 当前块的数据行
            j = i + 1
            while j < len(page_chunks):
                next_content = page_chunks[j][0]
                next_lines = next_content.split("\n")
                if len(next_lines) >= 3 and next_lines[0] == lines[0] and next_lines[1] == lines[1]:
                    all_data_rows.extend(next_lines[2:])
                    j += 1
                else:
                    break
            full_table = "\n".join([lines[0], lines[1]] + all_data_rows)
            table_id = _store_table(full_table)
            # 返回分批后的块（多行一批），都指向同一父表
            for k in range(i, j):
                merged.append((page_chunks[k][0], section, table_id))
            i = j
        else:
            merged.append((content, section, 0))
            i += 1

    chunks = [
        Chunk(
            text=text,
            source_file=source_file,
            category=category,
            # section 为空时用文件名做 fallback
            section=section or f"[{source_file.removesuffix('.md')}]",
            chunk_index=i,
            parent_table_id=parent_table_id,
        )
        for i, (text, section, parent_table_id) in enumerate(merged)
    ]
    return chunks


def chunk_all(max_tokens: int = 600, overlap: int = 50):
    """遍历 data_normalized/ 下所有 md 文件，分块并保存。"""
    md_files = sorted(DATA_DIR.rglob("*.md"))
    if not md_files:
        print(f"!! 在 {DATA_DIR} 下没有找到 .md 文件")
        return

    all_chunks = []
    total_tokens = 0
    for path in md_files:
        try:
            chunks = chunk_file(path, max_tokens, overlap)
            all_chunks.extend(chunks)
            total_tokens += sum(count_tokens(c.text) for c in chunks)
        except Exception as e:
            print(f"  !! {path.name}: {e}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # chunks.json — 无缩进，parent_table 用 ID 引用
    out_path = OUT_DIR / "chunks.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            [c.model_dump() for c in all_chunks],
            f, ensure_ascii=False, indent=None, separators=(",", ":"),
        )

    # parent_tables.json — 完整表格字典
    pt_path = OUT_DIR / "parent_tables.json"
    with open(pt_path, "w", encoding="utf-8") as f:
        json.dump(_parent_tables, f, ensure_ascii=False, indent=None, separators=(",", ":"))

    pt_mb = pt_path.stat().st_size / 1024 / 1024
    ck_mb = out_path.stat().st_size / 1024 / 1024
    print(f"\n完成: {len(md_files)} 个文件 -> {len(all_chunks)} 个分块 ({total_tokens} tokens)")
    print(f"  chunks.json:        {ck_mb:.1f} MB")
    print(f"  parent_tables.json: {pt_mb:.1f} MB")
    return all_chunks


def test():
    """Test chunker on a few files."""
    test_files = [
        DATA_DIR / "countries" / "Denmark.md",
        DATA_DIR / "diplomacy" / "Alliance.md",
        DATA_DIR / "economy" / "Buildings.md",
    ]
    for path in test_files:
        if not path.exists():
            print(f"!! file not found: {path}")
            continue
        print(f"\n{'='*60}")
        print(f"file: {path.relative_to(DATA_DIR)}")
        print(f"{'='*60}")
        try:
            chunks = chunk_file(path, max_tokens=600)
            for c in chunks:
                tok = count_tokens(c.text)
                sec = c.section or "(no section)"
                tag = " [table]" if c.parent_table_id else ""
                preview = c.text[:60].replace("\n", " ")
                try:
                    print(f"  [{tok:3d} tok]{tag:7s} {sec:25s} | {preview}...")
                except UnicodeEncodeError:
                    safe = preview.encode("ascii", errors="replace").decode("ascii")
                    print(f"  [{tok:3d} tok]{tag:7s} {sec:25s} | {safe}...")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"  !! error: {e}")


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        test()
    else:
        chunk_all()
