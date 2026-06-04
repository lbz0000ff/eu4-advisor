"""Embedding + 向量索引管理。
从 data/chunks/chunks.json 加载，按分类建 IndexIDMap FAISS 索引。
每个向量 ID = chunks.json 中的下标，检索后直接定位到 chunk。
"""

import json
import time
from pathlib import Path
from typing import Optional
from collections import defaultdict

import numpy as np
import faiss

CHUNKS_PATH = Path(__file__).parent.parent / "data" / "chunks"
INDEX_PATH = Path(__file__).parent.parent / "data" / "index"
DIM = 1024  # bge-m3 维度


class Embedder:
    """轻量 Embedding 模型封装（自动选择 CPU/GPU）"""

    def __init__(self, model_name: str = "intfloat/multilingual-e5-large"):
        self.model_name = model_name
        self._model = None

    def _pick_device(self) -> str:
        try:
            import torch
            if torch.cuda.is_available():
                print(f"  GPU: {torch.cuda.get_device_name(0)}")
                return "cuda"
        except ImportError:
            pass
        return "cpu"

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            device = self._pick_device()
            print(f"  加载 Embedding 模型: {self.model_name}")
            print(f"  设备: {device}")
            t0 = time.time()
            self._model = SentenceTransformer(
                self.model_name,
                device=device,
            )
            if device == "cuda":
                self._model.half()  # fp16 → ~2x 加速, 不影响输出精度
            print(f"  模型加载完成 ({time.time() - t0:.1f}s)")
        return self._model

    def embed(self, texts: list[str], batch_size: int = 64) -> np.ndarray:
        """批量 embedding，返回 float32 二维数组 (N, DIM)（已 L2 归一化）"""
        tag = "查询" if len(texts) <= 3 else "文本块"
        print(f"  Embedding {len(texts)} 个{tag}...")
        return self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=True,
        )


def build_category_index(embeddings: np.ndarray, ids: np.ndarray,
                         output_path: Path) -> faiss.Index:
    """构建 IndexIDMap(IndexFlatIP) 索引并保存。

    Args:
        embeddings: (N, DIM) 已 L2 归一化的向量
        ids: (N,) 每个向量在 chunks.json 中的位置
    """
    index = faiss.IndexIDMap(faiss.IndexFlatIP(DIM))
    index.add_with_ids(embeddings, ids)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(output_path))
    print(f"  索引已保存: {output_path}")
    return index


def load_index(path: Path) -> faiss.Index:
    """加载 FAISS 索引。"""
    return faiss.read_index(str(path))


def load_chunks(path: Optional[Path] = None) -> list[dict]:
    """加载 chunks.json。"""
    if path is None:
        path = CHUNKS_PATH / "chunks.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def search(query: str, embedder: Embedder, index: faiss.Index,
           chunks: list[dict], top_k: int = 8,
           category: Optional[str] = None) -> list[dict]:
    """检索与 query 最相关的 chunk。

    Args:
        chunks: 全部 chunk 列表，index 返回的 ID 直接作为下标
        category: 非 None 时只返回该分类的结果
    Returns:
        list[dict]: 每个 dict 含 chunk 的全部字段 + score
    """
    q_vec = embedder.embed([query])
    faiss.normalize_L2(q_vec)

    # 多取一些以便分类过滤后还能剩 top_k 个
    search_k = min(top_k * 3, len(chunks))
    scores, ids = index.search(q_vec, search_k)

    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx < 0 or idx >= len(chunks):
            continue
        chunk = chunks[idx]
        if category and chunk["category"] != category:
            continue
        results.append({**chunk, "score": float(score)})
        if len(results) >= top_k:
            break
    return results


def index_all():
    """从 chunks.json 加载全部 chunk，建全局 + 分类 FAISS 索引。"""
    # 1. 加载全部 chunk
    print("加载 chunks.json...")
    chunks = load_chunks()
    print(f"  共 {len(chunks)} 个 chunk")

    # 2. 按分类分组
    by_category = defaultdict(list)
    for i, c in enumerate(chunks):
        by_category[c["category"]].append(i)

    print(f"  共 {len(by_category)} 个分类: {', '.join(sorted(by_category.keys()))}")

    embedder = Embedder()
    INDEX_PATH.mkdir(parents=True, exist_ok=True)

    # 3. 逐类建索引
    for cat, indices in sorted(by_category.items()):
        items = [chunks[i] for i in indices]
        texts = ["passage: " + item["text"] for item in items]
        ids = np.array(indices, dtype=np.int64)

        print(f"\n── {cat} ({len(texts)} chunks) ──")

        embeddings = embedder.embed(texts)
        faiss.normalize_L2(embeddings)

        out_path = INDEX_PATH / f"{cat}.faiss"
        build_category_index(embeddings, ids, out_path)

    # 4. 全局索引
    print(f"\n── 全局 ({len(chunks)} chunks) ──")
    all_texts = ["passage: " + c["text"] for c in chunks]
    all_ids = np.arange(len(chunks), dtype=np.int64)
    all_embeddings = embedder.embed(all_texts)
    faiss.normalize_L2(all_embeddings)
    build_category_index(all_embeddings, all_ids, INDEX_PATH / "global.faiss")

    # 5. 保存 manifest
    manifest = {
        name: {
            "chunks": len(indices),
        }
        for name, indices in sorted(by_category.items())
    }
    manifest["total"] = len(chunks)
    with open(INDEX_PATH / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\n完成! 索引保存到 {INDEX_PATH}")
    print(f"  manifest: {INDEX_PATH / 'manifest.json'}")


if __name__ == "__main__":
    index_all()
