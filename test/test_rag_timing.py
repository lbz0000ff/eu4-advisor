import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import numpy as np


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import rag


class _Embedder:
    def embed(self, texts: list[str]) -> np.ndarray:
        return np.ones((len(texts), 1024), dtype=np.float32)


class _FaissIndex:
    def search(self, query: np.ndarray, top_k: int) -> tuple[np.ndarray, np.ndarray]:
        return (
            np.array([[1.0]], dtype=np.float32),
            np.array([[0]], dtype=np.int64),
        )


class _Bm25:
    def get_scores(self, tokens: list[str]) -> np.ndarray:
        return np.zeros(len(rag.chunks), dtype=np.float32)


class _Reranker:
    def rerank(self, query: str, candidates: list[dict], top_k: int) -> list[dict]:
        candidates[0]["rerank_score"] = 3.5
        return candidates[:top_k]


class RagTimingTest(unittest.TestCase):
    def test_search_does_not_call_llm_and_reports_retrieval_timing(self) -> None:
        output = io.StringIO()

        with (
            patch("llm.chat", side_effect=AssertionError("retrieval must not call LLM")),
            patch.object(rag, "_get_bm25", return_value=_Bm25()),
            redirect_stdout(output),
        ):
            rag.hybrid_search(
                "aggressive expansion reduction",
                _Embedder(),
                _FaissIndex(),
                top_k=1,
                keywords=["aggressive expansion", "improve relations"],
                verbose=True,
            )

        timing = output.getvalue()
        self.assertNotIn("query_prep", timing)
        self.assertIn("embed+faiss:", timing)

    def test_search_result_keeps_identity_and_scores(self) -> None:
        with patch.object(rag, "_get_bm25", return_value=_Bm25()):
            results = rag.hybrid_search(
                "test",
                _Embedder(),
                _FaissIndex(),
                top_k=1,
                keywords=["test"],
                reranker=_Reranker(),
            )

        self.assertEqual(results[0]["chunk_index"], 0)
        self.assertEqual(results[0]["rerank_score"], 3.5)
        self.assertIn("rrf_score", results[0])


if __name__ == "__main__":
    unittest.main()
