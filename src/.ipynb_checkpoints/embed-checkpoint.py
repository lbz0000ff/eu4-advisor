"""Embedding + 向量索引管理（CPU/GPU 通用版）
修复：所有送入 FAISS 的数组都经由 list → np.array 重建，彻底杜绝 swig_ptr 报错
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
CHUNKS_DIR = DATA_DIR / "chunks"
INDEX_PATH = DATA_DIR / "faiss.index"
CHUNKS_PATH = DATA_DIR / "chunks.json"


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
            print(f"加载 Embedding 模型: {self.model_name}")
            print(f"推理后端: {providers}")
            t0 = time.time()
            self._model = TextEmbedding(
                model_name=self.model_name,
                providers=providers,
            )
            print(f"模型加载完成 ({time.time() - t0:.1f}s)")
        return self._model

    def embed(self, texts: list[str], batch_size: int = 32) -> np.ndarray:
        """批量 embedding，返回完全标准、独立的 float32 二维数组"""
        print(f"Embedding {len(texts)} 个文本块...")
        raw_vectors = list(self.model.embed(texts, batch_size=batch_size))

        # ★ 关键：逐个将向量转成 Python list，再用 np.array 重建
        # 这会斩断所有底层共享内存，得到 FAISS 100% 接受的数组
        pure_lists = [v.tolist() for v in raw_vectors]
        embeddings = np.array(pure_lists, dtype=np.float32)
        return embeddings


def build_index(embeddings: np.ndarray) -> faiss.Index:
    """构建 FAISS 索引并保存（对数组做极限重建以兼容 SWIG）"""
    dim = embeddings.shape[1]
    print(f"构建 FAISS 索引 (维度: {dim})...")

    # 第一次深度重建，确保归一化前的数组绝对标准
    embeddings = np.array(embeddings.tolist(), dtype=np.float32)

    # 归一化
    try:
        faiss.normalize_L2(embeddings)
    except ValueError:
        print("faiss.normalize_L2 失败，手动 L2 归一化...")
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        embeddings = embeddings / norms

    # 归一化后再次全量重建 —— 除法运算可能又引入非标准内存
    embeddings = np.array(embeddings.tolist(), dtype=np.float32)

    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)                     # 现在一定不会报错
    faiss.write_index(index, str(INDEX_PATH))
    print(f"FAISS 索引已保存: {INDEX_PATH}")
    return index


def load_index() -> faiss.Index:
    """加载 FAISS 索引"""
    if not INDEX_PATH.exists():
        raise FileNotFoundError(f"索引文件不存在: {INDEX_PATH}")
    return faiss.read_index(str(INDEX_PATH))


def save_chunks(chunks: list[str]):
    """保存文本块列表"""
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"文本块已保存: {CHUNKS_PATH} ({len(chunks)} 块)")


def load_chunks() -> list[str]:
    """加载文本块列表"""
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(f"文本块文件不存在: {CHUNKS_PATH}")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def search(query: str, embedder: Embedder, index: faiss.Index,
           chunks: list[str], top_k: int = 5) -> list[dict]:
    """检索与 query 最相关的文本块"""
    q_vec = embedder.embed([query])
    # 查询向量也做一次深度重建（虽然单条一般没问题，但保持一致性强）
    q_vec = np.array(q_vec.tolist(), dtype=np.float32)
    faiss.normalize_L2(q_vec)
    scores, indices = index.search(q_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < len(chunks):
            results.append({
                "score": float(score),
                "text": chunks[idx][:500],
                "index": int(idx),
            })
    return results


def index_all(raw_dir: Optional[Path] = None):
    """读取所有 raw 文件 → 分块 → Embedding → 建索引"""
    if raw_dir is None:
        raw_dir = DATA_DIR / "raw"

    all_chunks = []
    md_files = sorted(raw_dir.glob("*.md"))
    if not md_files:
        print(f"⚠ 在 {raw_dir} 中没有找到 .md 文件，请先运行 crawler.py")
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
    raw_dir = DATA_DIR / "raw"
    md_files = list(raw_dir.glob("*.md"))
    if not md_files:
        print("未找到原始页面，先运行 crawler.py 爬取数据")
        sys.exit(1)

    index_all()