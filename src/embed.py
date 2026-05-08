"""Embedding + 向量索引管理（CPU/GPU 通用版）
支持按分类文件夹建索引（每个 data/raw/ 下的子目录 = 一个类别）。
"""

import os
import re
import json
import time
from pathlib import Path
from typing import Optional

import numpy as np
import faiss


DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
CATEGORIES_DIR = DATA_DIR / "categories"
MANIFEST_PATH = CATEGORIES_DIR / "manifest.json"

# 向后兼容：旧的全局索引
INDEX_PATH = DATA_DIR / "faiss.index"
CHUNKS_PATH = DATA_DIR / "chunks.json"
CHUNKS_DIR = DATA_DIR / "chunks"

# 类别显示名称（中文）
CATEGORY_NAMES = {
    "diplomacy":   "外交 Diplomacy",
    "military":    "战争 Military",
    "economy":     "经济 Economy",
    "government":  "政府/政治 Government",
    "religion":    "宗教 Religion",
    "tech_ideas":  "科技/理念 Tech & Ideas",
    "countries":   "国家 Countries",
    "dlc":         "DLC 资料片",
    "misc":        "其他 Misc",
}


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """将文本按段落和句子切分成块"""
    sections = re.split(r"\n(?=#{1,3}\s)", text)
    chunks = []
    for section in sections:
        if not section.strip():
            continue
        words = section.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i : i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
    return chunks


def _guess_providers() -> list[str]:
    """自动检测可用的推理后端"""
    providers = ["CPUExecutionProvider"]
    try:
        import onnxruntime
        available = onnxruntime.get_available_providers()
        if "CUDAExecutionProvider" in available:
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        elif "ROCMExecutionProvider" in available:
            providers = ["ROCMExecutionProvider", "CPUExecutionProvider"]
    except ImportError:
        pass
    return providers


class Embedder:
    """轻量 Embedding 模型封装（自动选择 CPU/GPU）"""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from fastembed import TextEmbedding
            providers = _guess_providers()
            print(f"  加载 Embedding 模型: {self.model_name}")
            print(f"  推理后端: {providers}")
            t0 = time.time()
            self._model = TextEmbedding(
                model_name=self.model_name,
                providers=providers,
            )
            print(f"  模型加载完成 ({time.time() - t0:.1f}s)")
        return self._model

    def embed(self, texts: list[str], batch_size: int = 32) -> np.ndarray:
        """批量 embedding，返回完全标准、独立的 float32 二维数组"""
        tag = "查询" if len(texts) <= 3 else "文本块"
        print(f"  Embedding {len(texts)} 个{tag}...")
        raw_vectors = list(self.model.embed(texts, batch_size=batch_size))
        pure_lists = [v.tolist() for v in raw_vectors]
        embeddings = np.array(pure_lists, dtype=np.float32)
        return embeddings


def build_index(embeddings: np.ndarray, output_path: Optional[Path] = None) -> faiss.Index:
    """构建 FAISS 索引并保存"""
    if output_path is None:
        output_path = INDEX_PATH
    dim = embeddings.shape[1]
    print(f"  构建 FAISS 索引 (维度: {dim})...")

    embeddings = np.array(embeddings.tolist(), dtype=np.float32)
    try:
        faiss.normalize_L2(embeddings)
    except ValueError:
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        embeddings = embeddings / norms
    embeddings = np.array(embeddings.tolist(), dtype=np.float32)

    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(output_path))
    print(f"  索引已保存: {output_path}")
    return index


def load_index() -> faiss.Index:
    """加载全局 FAISS 索引（向后兼容）"""
    if not INDEX_PATH.exists():
        raise FileNotFoundError(f"索引文件不存在: {INDEX_PATH}")
    return faiss.read_index(str(INDEX_PATH))


def save_chunks(chunks: list[str], output_path: Optional[Path] = None):
    """保存文本块列表"""
    if output_path is None:
        output_path = CHUNKS_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"  文本块已保存: {output_path} ({len(chunks)} 块)")


def load_chunks() -> list[str]:
    """加载全局文本块（向后兼容）"""
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(f"文本块文件不存在: {CHUNKS_PATH}")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def search(query: str, embedder: Embedder, index: faiss.Index,
           chunks: list[str], top_k: int = 8) -> list[dict]:
    """检索与 query 最相关的文本块"""
    q_vec = embedder.embed([query])
    q_vec = np.array(q_vec.tolist(), dtype=np.float32)
    faiss.normalize_L2(q_vec)
    scores, indices = index.search(q_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < len(chunks):
            results.append({
                "score": float(score),
                "text": chunks[idx],
                "index": int(idx),
            })
    return results


# ═══════════ 类别分索引（基于文件夹） ═══════════

def list_categories() -> dict:
    """读取 manifest，返回所有已建索引的类别信息"""
    if not MANIFEST_PATH.exists():
        return {}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def category_path(category: str) -> Path:
    """类别索引目录路径"""
    return CATEGORIES_DIR / category


def load_category_index(category: str) -> faiss.Index:
    """加载指定类别的 FAISS 索引"""
    index_path = category_path(category) / "faiss.index"
    if not index_path.exists():
        raise FileNotFoundError(
            f"类别 '{category}' 的索引不存在。请先运行 python3 src/embed.py"
        )
    return faiss.read_index(str(index_path))


def load_category_chunks(category: str) -> list[str]:
    """加载指定类别的文本块列表"""
    chunks_path = category_path(category) / "chunks.json"
    if not chunks_path.exists():
        raise FileNotFoundError(
            f"类别 '{category}' 的文本块不存在。请先运行 python3 src/embed.py"
        )
    with open(chunks_path, "r", encoding="utf-8") as f:
        return json.load(f)


def index_all(raw_dir: Optional[Path] = None):
    """按 data/raw/ 下的子文件夹分组建索引"""
    if raw_dir is None:
        raw_dir = RAW_DIR

    # 获取所有子目录（每个子目录 = 一个类别）
    subdirs = sorted([
        d for d in raw_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])

    if not subdirs:
        # 没有子目录时尝试旧版扁平文件
        md_files = list(raw_dir.glob("*.md"))
        if md_files:
            print("检测到旧版扁平结构，使用 index_all_flat()...")
            return index_all_flat(raw_dir)
        else:
            print(f"⚠ 在 {raw_dir} 中没有找到数据文件。请先运行 crawler.py")
            return None

    print(f"发现 {len(subdirs)} 个分类文件夹:")
    for d in subdirs:
        md_count = len(list(d.glob("*.md")))
        name = CATEGORY_NAMES.get(d.name, d.name)
        print(f"  {d.name:20s} → {name} ({md_count} 个页面)")

    # 逐类别处理
    embedder = Embedder()
    manifest = {}

    for subdir in subdirs:
        cat_name = subdir.name
        md_files = sorted(subdir.glob("*.md"))
        if not md_files:
            print(f"\n  ⚠ {cat_name}/ 中没有 .md 文件，跳过")
            continue

        # 读取并切块
        all_chunks = []
        page_count = 0
        for md_path in md_files:
            text = md_path.read_text(encoding="utf-8")
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            page_count += 1

        print(f"\n── 类别: {CATEGORY_NAMES.get(cat_name, cat_name)} "
              f"({page_count} 页面, {len(all_chunks)} 块) ──")

        # 嵌入 + 建索引
        embeddings = embedder.embed(all_chunks)
        cat_dir = category_path(cat_name)
        cat_dir.mkdir(parents=True, exist_ok=True)
        build_index(embeddings, output_path=cat_dir / "faiss.index")
        save_chunks(all_chunks, output_path=cat_dir / "chunks.json")

        manifest[cat_name] = {
            "pages": page_count,
            "chunks": len(all_chunks),
            "name": CATEGORY_NAMES.get(cat_name, cat_name),
        }

    # 保存 manifest
    CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    total_chunks = sum(v["chunks"] for v in manifest.values())
    print(f"\n✅ 索引完成！共 {len(manifest)} 个类别, {total_chunks} 个文本块")
    print(f"  manifest: {MANIFEST_PATH}")
    return embedder


def index_all_flat(raw_dir: Optional[Path] = None):
    """旧版：所有页面合并建一个索引（向后兼容）"""
    if raw_dir is None:
        raw_dir = RAW_DIR

    all_chunks = []
    md_files = sorted(raw_dir.glob("*.md"))
    if not md_files:
        print(f"⚠ 在 {raw_dir} 中没有找到 .md 文件")
        return None

    print(f"读取 {len(md_files)} 个原始页面...")
    for md_path in md_files:
        text = md_path.read_text(encoding="utf-8")
        chunks = chunk_text(text)
        all_chunks.extend(chunks)

    print(f"共分得 {len(all_chunks)} 个文本块")
    embedder = Embedder()
    embeddings = embedder.embed(all_chunks)
    build_index(embeddings)
    save_chunks(all_chunks)
    print(f"✅ 索引完成！共 {len(all_chunks)} 块")
    return embedder


if __name__ == "__main__":
    import sys

    mode = "auto"
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    if mode == "flat":
        print("=== 旧版模式：单个全局索引 ===")
        index_all_flat()
    else:
        print("=== 新版模式：按分类文件夹建索引 ===")
        index_all()
