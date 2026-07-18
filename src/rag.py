"""
RAG 主流程 — FAISS + BM25 混合检索。
"""

import json
import re
import sys
from pathlib import Path

import faiss
import numpy as np
from rank_bm25 import BM25Okapi

from llm import LLMConfig
from nltk.stem import PorterStemmer

_stemmer = PorterStemmer()

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_DIR = DATA_DIR / "index"
CHUNKS_DIR = DATA_DIR / "chunks"

DEFAULT_SYSTEM_PROMPT = """
你是 EU4 Wiki 的信息提取助手。

你的任务：从"参考信息"中提取与问题相关的内容，填入以下模板。

模板：
根据参考信息：
- [事实1，附来源文件名]
- [事实2，附来源文件名]
- ...

参考信息未覆盖：[列出问题涉及但参考信息中没有的方面]

规则：
- 只提取参考信息中明确写出的内容，不要做任何推理或补充
- 每个事实都必须能直接在参考信息中找到原文对应
- 如果没有找到任何相关信息，输出：知识库中未找到相关信息
"""

# ═══════════════════════════
# 1. 加载数据
# ═══════════════════════════

print("加载数据...")
with open(CHUNKS_DIR / "chunks.json", encoding="utf-8") as f:
    chunks: list[dict] = json.load(f)

parent_tables: dict[str, str] = {}
pt_path = CHUNKS_DIR / "parent_tables.json"
if pt_path.exists():
    with open(pt_path, encoding="utf-8") as f:
        parent_tables = json.load(f)

print(f"  {len(chunks)} chunks, {len(parent_tables)} 父表")


# ═══════════════════════════
# 2. 混合检索（手写 RRF 融合）
# ═══════════════════════════

_tokenized_chunks = [[_stemmer.stem(t) for t in c["text"].lower().split()] for c in chunks]
_bm25_index: BM25Okapi | None = None


def _get_bm25():
    global _bm25_index
    if _bm25_index is None:
        _bm25_index = BM25Okapi(_tokenized_chunks)
    return _bm25_index


def hybrid_search(
    query_en: str,
    embedder,
    faiss_index: faiss.Index,
    top_k: int = 8,
    category: str = "",
    verbose: bool = False,
    reranker=None,
    keywords: list[str] | None = None,
) -> list[dict]:
    """Search an already-planned English query with FAISS, BM25, RRF, and reranking."""
    import time
    times: dict[str, float] = {}
    bm25_raw = " ".join(keywords) if keywords else query_en
    print(f"  [query] FAISS: {query_en}  |  BM25: {bm25_raw}")

    t0 = time.time()
    q_vec = embedder.embed(["query: " + query_en])
    faiss.normalize_L2(q_vec)
    faiss_scores, ids = faiss_index.search(q_vec, top_k * 3)
    times["embed+faiss"] = time.time() - t0

    faiss_rank = {}
    for rank, (score, idx) in enumerate(zip(faiss_scores[0], ids[0])):
        if idx < 0 or idx >= len(chunks):
            continue
        faiss_rank[int(idx)] = rank + 1

    # BM25
    t0 = time.time()
    bm25 = _get_bm25()
    tokenized_q = [_stemmer.stem(t) for t in re.sub(r"[^\w\s]", "", bm25_raw.lower()).split()]
    bm25_scores = bm25.get_scores(tokenized_q)
    bm25_top = np.argsort(bm25_scores)[-top_k * 3:][::-1]
    times["bm25"] = time.time() - t0

    bm25_rank = {}
    for rank, idx in enumerate(bm25_top):
        if idx < len(chunks):
            bm25_rank[int(idx)] = rank + 1

    # RRF
    t0 = time.time()
    K = 20
    all_ids = set(faiss_rank.keys()) | set(bm25_rank.keys())
    rrf_scores = {}
    for idx in all_ids:
        chunk = chunks[idx]
        if category and chunk["category"] != category:
            continue
        r1 = faiss_rank.get(idx, 999)
        r2 = bm25_rank.get(idx, 999)
        rrf_scores[idx] = 1 / (K + r1) + 1 / (K + r2)

    # RRF 候选池
    pool_size = top_k * 3 if reranker else top_k
    top = sorted(rrf_scores, key=rrf_scores.get, reverse=True)[:pool_size]
    times["rrf"] = time.time() - t0

    # cross encoder
    rerank_scores = {}
    if reranker:
        t0 = time.time()
        candidates = []
        for idx in top:
            ch = chunks[idx]
            candidates.append({
                "text": ch["text"],
                "index": idx,
                "score": rrf_scores[idx],
            })
        reranked = reranker.rerank(query_en, candidates, top_k)
        rerank_scores = {
            c["index"]: c["rerank_score"]
            for c in reranked
        }
        top = [c["index"] for c in reranked]
        if verbose:
            print(f"  [timing] rerank: {time.time() - t0:.3f}s")

    if verbose:
        print(
            f"  [timing] embed+faiss: {times['embed+faiss']:.3f}s  "
            f"bm25: {times['bm25']:.3f}s  rrf: {times['rrf']:.3f}s"
        )

    # 导入parent table
    results = []
    MAX_PT_TOKENS = 2000
    for idx in top:
        chunk = chunks[idx]
        content = chunk["text"]
        pt_id = chunk.get("parent_table_id", 0)
        if pt_id and str(pt_id) in parent_tables:
            full = parent_tables[str(pt_id)]
            words = full.split()
            if len(words) <= MAX_PT_TOKENS:
                content = chunk["text"] + "\n\n> 完整表格:\n" + "\n".join(
                    "> " + line for line in full.split("\n")
                )
            else:
                truncated_lines = []
                tok_count = 0
                for line in full.split("\n"):
                    line_tok = len(line.split())
                    if tok_count + line_tok > MAX_PT_TOKENS:
                        truncated_lines.append(f"> ... (截断, 原表 {len(words)} tokens)")
                        break
                    truncated_lines.append("> " + line)
                    tok_count += line_tok
                content = chunk["text"] + "\n\n> 表格(前" + str(tok_count) + " tokens):\n" + "\n".join(truncated_lines)

        final_score = rerank_scores.get(idx, rrf_scores[idx])
        results.append({
            "chunk_index": idx,
            "text": content,
            "source": chunk["source_file"],
            "category": chunk["category"],
            "section": chunk["section"],
            "score": final_score,
            "rrf_score": rrf_scores[idx],
            "rerank_score": rerank_scores.get(idx),
        })
    return results


# ═══════════════════════════
# 3. 问答
# ═══════════════════════════

def answer(
    query: str,
    embedder=None,
    faiss_index=None,
    category: str = "",
    llm_config: LLMConfig = None,
    use_rag: bool = True,
    top_k: int = 8,
    reranker=None,
    retrieved_results: list[dict] | None = None,
) -> str:
    if llm_config is None:
        llm_config = LLMConfig()

    if not use_rag:
        from llm import chat
        return chat(
            messages=[{"role": "user", "content": query}],
            config=llm_config, system_prompt=DEFAULT_SYSTEM_PROMPT,
        )

    results = retrieved_results
    if results is None:
        results = hybrid_search(
            query,
            embedder,
            faiss_index,
            top_k,
            category,
            verbose=True,
            reranker=reranker,
        )

    context = "\n\n".join(
        f"[{i}] {r['source']}" + (f" / {r['section']}" if r['section'] else "")
        + f"\n{r['text']}"
        for i, r in enumerate(results, 1)
    )

    from llm import chat
    return chat(
        messages=[{"role": "user", "content": f"参考信息：\n{context}\n\n---\n问题：{query}\n\n请从参考信息中提取答案，不要添加任何参考信息中没有的内容。"}],
        config=llm_config, system_prompt=DEFAULT_SYSTEM_PROMPT,
    )


def compare(query: str, embedder, faiss_index, category: str = "", reranker=None):
    llm_cfg = LLMConfig()
    print(f"\n{'='*60}\n问题: {query}\n{'='*60}\n")
    print("--- 不带 RAG ---")
    print(answer(query, use_rag=False))
    print()
    print("--- 带 RAG ---")
    print(answer(query, embedder=embedder, faiss_index=faiss_index, category=category, reranker=reranker))
    print()


# ═══════════════════════════
# 4. CLI
# ═══════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?")
    parser.add_argument("--compare", action="store_true")
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--no-rag", action="store_true")
    parser.add_argument("--provider", default="deepseek")
    parser.add_argument("--model", default="deepseek-v4-flash")
    parser.add_argument("--category", default="")
    parser.add_argument("--list-categories", action="store_true")
    parser.add_argument("--rerank", action="store_true", help="启用 Cross-Encoder 重排")
    args = parser.parse_args()

    if args.list_categories:
        cats = sorted(set(c["category"] for c in chunks))
        for cat in cats:
            n = sum(1 for c in chunks if c["category"] == cat)
            print(f"  {cat}: {n}")
        sys.exit(0)

    from embed import Embedder
    print("加载 Embedding 模型...")
    embedder = Embedder()
    _ = embedder.model

    reranker = None
    if args.rerank:
        from reranker import get_reranker
        reranker = get_reranker()

    index_name = f"{args.category}.faiss" if args.category else "global.faiss"
    index_path = INDEX_DIR / index_name
    faiss_index = faiss.read_index(str(index_path))
    print(f"  索引: {index_name}")

    llm_cfg = LLMConfig(provider=args.provider, model=args.model)

    if args.query:
        if args.compare:
            compare(args.query, embedder, faiss_index, args.category, reranker=reranker)
        else:
            print(answer(args.query, embedder=embedder, faiss_index=faiss_index,
                         category=args.category, llm_config=llm_cfg,
                         use_rag=not args.no_rag, top_k=args.top_k,
                         reranker=reranker))
    else:
        label = f"[{args.category}] " if args.category else ""
        print(f"Eu4RAG {label}(/quit)")
        while True:
            q = input("\n? ").strip()
            if q.lower() in ("/quit", "/exit", "/q"):
                break
            if args.compare:
                compare(q, embedder, faiss_index, args.category)
            else:
                r = answer(q, embedder=embedder, faiss_index=faiss_index,
                           category=args.category, llm_config=llm_cfg,
                           use_rag=not args.no_rag, top_k=args.top_k,
                           reranker=reranker)
                print(f"\n{r}")
