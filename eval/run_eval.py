"""
RAG 评测脚本 — 自动跑 50 条中英文查询，输出评测报告。
用法:
    python eval/run_eval.py                     # 跑全部 50 条
    python eval/run_eval.py --rerank            # 带 Cross-Encoder 重排
    python eval/run_eval.py --sample 10          # 只跑前 10 条
    python eval/run_eval.py --lang zh            # 只跑中文
    python eval/run_eval.py --lang en            # 只跑英文
    python eval/run_eval.py --output result.json # 保存详细结果
"""
import json, sys, time, re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag import hybrid_search, chunks, answer
from embed import Embedder
from llm import LLMConfig
import faiss

DATA = Path(__file__).parent.parent / "data"
INDEX_DIR = DATA / "index"

# 预先加载模型和索引
print("加载 Embedding 模型...")
embedder = Embedder()
_ = embedder.model

print("加载 FAISS 索引...")
faiss_index = faiss.read_index(str(INDEX_DIR / "global.faiss"))
print(f"  索引: {faiss_index.ntotal} 向量")

# 可选重排
reranker = None
if "--rerank" in sys.argv:
    from reranker import get_reranker
    reranker = get_reranker()

# 过滤参数
sample = None
if "--sample" in sys.argv:
    idx = sys.argv.index("--sample")
    sample = int(sys.argv[idx + 1])

lang_filter = None
if "--lang" in sys.argv:
    idx = sys.argv.index("--lang")
    lang_filter = sys.argv[idx + 1]

# 读取评测集
with open(Path(__file__).parent / "queries.json", encoding="utf-8") as f:
    all_queries = json.load(f)

# 过滤
queries = all_queries
if lang_filter:
    queries = [q for q in queries if q["lang"] == lang_filter]
if sample:
    queries = queries[:sample]

print(f"\n评测集: {len(queries)} 条 ({len(all_queries)} 条总)\n")

# 指标统计
results = []
times = []
retrieval_scores = []

for i, item in enumerate(queries, 1):
    q = item["q"]
    print(f"[{i:2d}/{len(queries)}] ({item['lang']}) {q[:50]}...")

    t0 = time.time()

    # 只测检索（不调 LLM），看 top-5 的 RRF 分数
    hits = hybrid_search(
        q, embedder, faiss_index,
        top_k=5, category="", verbose=False,
        reranker=reranker,
    )

    t = time.time() - t0
    times.append(t)

    # 记录 top-1 的分数
    top_score = hits[0]["score"] if hits else 0
    retrieval_scores.append(top_score)

    # 记录结果摘要
    sources = [f"{h['source']}/{h['section']}"[:40] for h in hits[:3]]
    results.append({
        "id": item["id"],
        "q": q,
        "lang": item["lang"],
        "cat": item["cat"],
        "type": item["type"],
        "time": round(t, 3),
        "top_score": round(top_score, 4),
        "top_sources": sources,
        "n_results": len(hits),
    })

    # 每 10 条打印进度
    if i % 10 == 0:
        print(f"  ... {i}/{len(queries)} 完成, 平均 {sum(times[-10:])/10:.2f}s/条")

# ── 输出报告 ──
print("\n" + "=" * 60)
print("评测报告")
print("=" * 60)
print(f"总查询: {len(results)}")
print(f"平均耗时: {sum(times)/len(times):.2f}s")
print(f"中位耗时: {sorted(times)[len(times)//2]:.2f}s")
print(f"平均 Top-1 RRF 分数: {sum(retrieval_scores)/len(retrieval_scores):.4f}")
print()

# 按语言统计
for lang in ["zh", "en"]:
    subset = [r for r in results if r["lang"] == lang]
    if subset:
        avg_score = sum(r["top_score"] for r in subset) / len(subset)
        avg_time = sum(r["time"] for r in subset) / len(subset)
        print(f"  [{lang}] {len(subset)}条 | 平均分数: {avg_score:.4f} | 平均耗时: {avg_time:.2f}s")

print()

# 按类型统计
from collections import Counter
type_counts = Counter(r["type"] for r in results)
for t, n in type_counts.most_common():
    subset = [r for r in results if r["type"] == t]
    avg = sum(r["top_score"] for r in subset) / len(subset)
    print(f"  [{t}] {n}条 | 平均分数: {avg:.4f}")

print()

# 检出低分查询 (top_score < 0.02 说明检索可能有问题)
low = [r for r in results if r["top_score"] < 0.02]
if low:
    print(f"⚠ 低分查询 ({len(low)} 条, top_score < 0.02):")
    for r in low:
        print(f"  [{r['id']}] ({r['lang']}) {r['q'][:60]}")
else:
    print("✅ 所有查询分数正常")

# 保存详细结果
output = None
if "--output" in sys.argv:
    idx = sys.argv.index("--output")
    output = sys.argv[idx + 1]
    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n详细结果已保存: {output}")
