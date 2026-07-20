"""Cross-Encoder 重排 — 对混合检索初筛结果做二次精排。"""
import os
import time
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


load_dotenv(Path(__file__).parent.parent / ".env")


class Reranker:
    """Cross-Encoder 重排器，懒加载模型。"""

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = (
            model_name
            or os.environ.get("RERANKER_MODEL")
            or "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers.cross_encoder import CrossEncoder
            print(f"  加载重排模型: {self.model_name}")
            t0 = time.time()
            self._model = CrossEncoder(self.model_name)
            print(f"  重排模型加载完成 ({time.time() - t0:.1f}s)")
        return self._model

    def rerank(self, query: str, candidates: list[dict], top_k: int = 8) -> list[dict]:
        """对候选结果做 Cross-Encoder 重排。

        Args:
            query: 原始查询（预处理后的英文查询）
            candidates: 候选结果列表（含 text 字段）
            top_k: 重排后保留的结果数
        Returns:
            按相关性从高到低排序的结果列表
        """
        pairs = [(query, c["text"]) for c in candidates]
        scores = self.model.predict(pairs, show_progress_bar=False)

        indexed = list(zip(scores, candidates))
        indexed.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, c in indexed[:top_k]:
            c["rerank_score"] = float(score)
            results.append(c)
        return results


# 全局单例
_reranker: Optional[Reranker] = None


def get_reranker() -> Reranker:
    global _reranker
    if _reranker is None:
        _reranker = Reranker()
    return _reranker


def rerank_results(query: str, candidates: list[dict], top_k: int = 8) -> list[dict]:
    """便捷函数：重排候选结果。"""
    return get_reranker().rerank(query, candidates, top_k)
