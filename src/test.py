"""RAG 评测脚本 - 对比模式 + 检索/生成质量评估"""

import json
import re
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from rag import answer, hybrid_search, chunks
from embed import Embedder
from llm import LLMConfig, chat
import faiss

EVAL_FILE = Path(__file__).parent.parent / "eval" / "queries.json"

def load_queries():
    """从 eval/queries.json 加载评测集，支持 --sample 和 --lang 过滤"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=0, help="只跑前 N 条")
    parser.add_argument("--lang", default="", choices=["en", "zh", ""], help="按语言过滤")
    args, _ = parser.parse_known_args()

    with open(EVAL_FILE, encoding="utf-8") as f:
        all_qs = json.load(f)
    filtered = all_qs
    if args.lang:
        filtered = [q for q in filtered if q["lang"] == args.lang]
    if args.sample:
        filtered = filtered[:args.sample]
    # 兼容旧格式：只取 query 文本
    queries = [q["q"] for q in filtered]
    print(f"评测集: {len(filtered)} 条 (共 {len(all_qs)} 条) | 语言过滤: {args.lang or '全部'}")
    return queries

TOP_K = 8
CALL_DELAY = 0.5  # 每次 API 调用后等待秒数，避免 rate limit

# ── LLM-as-Judge 配置 ──
EU4_CONTEXT = """注意：所有用户问题都是关于《欧陆风云4》（Europa Universalis IV）这款游戏的，不是现实历史。
例如 "What is Prussia?" 问的是游戏中的普鲁士（可玩国家/可成立国家），不是现实中的普鲁士王国。
请始终以游戏机制、游戏内容的角度来判断相关性，而非现实历史。"""


def judge_call(prompt: str, max_tokens: int = 512) -> str:
    """调用 LLM，带重试"""
    cfg = LLMConfig(temperature=0.0, max_tokens=max_tokens)
    for attempt in range(3):
        try:
            resp = chat(
                messages=[{"role": "user", "content": prompt}],
                config=cfg,
            )
            if resp and resp.strip():
                return resp
        except Exception as e:
            pass
        # 重试前等待
        time.sleep(2 ** attempt)
    return ""


def extract_json(raw: str) -> dict | None:
    if not raw or not raw.strip():
        return None
    text = raw.strip()
    # 去 ```json 标记
    cleaned = re.sub(r"```(?:json)?", "", text).strip()
    # 找 {} 对
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError:
            pass
    # 直接尝试
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # 搜数字
    nums = re.findall(r"(\d+\.?\d*)", text)
    if nums:
        return {"score": float(nums[0])}
    return None


def judge_json(prompt: str, max_tokens: int = 512) -> dict:
    raw = judge_call(prompt, max_tokens=max_tokens)
    result = extract_json(raw)
    if result is not None:
        return result
    return {"_parse_failed": True, "_raw": raw[:500]}


def load_best_index():
    embedder = Embedder()
    _ = embedder.model
    index = faiss.read_index(str(Path(__file__).parent.parent / "data/index/global.faiss"))
    print(f"  索引: {index.ntotal} 向量")
    return embedder, index, chunks


# ═══════════════════════════════════════
# 检索质量指标
# ═══════════════════════════════════════

def eval_contextual_precision(query: str, retrieved_chunks: list[dict]) -> dict:
    """逐个 chunk 判相关，带回退重试（每次调用间有间隔）"""
    if not retrieved_chunks:
        return {"score": 0.0, "details": "无检索结果"}

    relevant_count = 0
    mapped = []

    for i, r in enumerate(retrieved_chunks[:TOP_K]):
        chunk_text = r["text"][:500]
        prompt = f"""{EU4_CONTEXT}

判断以下文档块是否与用户问题相关。只输出 JSON。

用户问题: {query}

文档块: {chunk_text}

{{"relevant": true/false, "reason": "一句话理由"}}"""
        result = judge_json(prompt)
        if result.get("_parse_failed"):
            # 单次失败先用 False 占位
            mapped.append({
                "rank": i + 1,
                "score": round(r["score"], 4),
                "relevant": False,
                "reason": "judge 解析失败",
                "_raw": result.get("_raw", ""),
            })
        else:
            is_rel = result.get("relevant", False)
            if is_rel:
                relevant_count += 1
            mapped.append({
                "rank": i + 1,
                "score": round(r["score"], 4),
                "relevant": is_rel,
                "reason": result.get("reason", ""),
            })

        # 每个 chunk 之间等一会
        time.sleep(CALL_DELAY)

    precision = relevant_count / TOP_K
    return {
        "score": round(precision, 4),
        "relevant_chunks": relevant_count,
        "total": TOP_K,
        "chunk_judgments": mapped,
    }


def eval_contextual_recall(query: str, all_chunk_texts: list[str]) -> dict:
    if not all_chunk_texts:
        return {"score": 0.0}
    combined = "\n\n---\n\n".join(t[:800] for t in all_chunk_texts[:TOP_K])
    prompt = f"""{EU4_CONTEXT}

判断以下检索内容是否包含足够信息回答用户问题。只输出 JSON。

用户问题: {query}

检索内容:
{combined}

{{"score": 0.0~1.0, "reason": "一句话"}}
1.0=完全覆盖  0.6=部分覆盖  0.3=基本没覆盖"""
    result = judge_json(prompt)
    if result.get("_parse_failed"):
        return {"score": 0.0, "reason": "judge 响应无法解析", "_raw": result.get("_raw", "")}
    return {
        "score": round(float(result.get("score", 0)), 4),
        "reason": result.get("reason", ""),
    }


# ═══════════════════════════════════════
# 生成质量指标
# ═══════════════════════════════════════

def eval_faithfulness(answer_text: str, chunk_texts: list[str]) -> dict:
    context_snippet = "\n\n---\n\n".join(t[:800] for t in chunk_texts[:TOP_K])
    prompt = f"""判断 AI 回答是否完全基于所提供的上下文（无幻觉）。只输出 JSON，不要任何额外文字。

上下文:
{context_snippet}

AI 回答:
{answer_text}

{{"faithfulness_score": 0.0~1.0, "hallucinations": [], "supported_claims": []}}
1.0=完全忠实  0.7=少量合理推断  0.4=部分幻觉  0.0=大量编造"""
    result = judge_json(prompt, max_tokens=768)
    if result.get("_parse_failed"):
        return {
            "score": 0.0,
            "hallucinations": [],
            "supported_claims": [],
            "_parse_failed": True,
            "_raw": result.get("_raw", ""),
        }
    return {
        "score": round(float(result.get("faithfulness_score", 0)), 4),
        "hallucinations": result.get("hallucinations", []),
        "supported_claims": result.get("supported_claims", []),
    }


def eval_answer_relevancy(query: str, answer_text: str) -> dict:
    prompt = f"""{EU4_CONTEXT}

判断 AI 回答是否直接针对用户问题。只输出 JSON。

用户问题: {query}

AI 回答: {answer_text}

{{"relevancy_score": 0.0~1.0, "reason": "一句话"}}
1.0=完全针对  0.7=基本针对  0.4=部分跑题  0.0=答非所问"""
    result = judge_json(prompt)
    if result.get("_parse_failed"):
        return {"score": 0.0, "reason": "judge 响应无法解析", "_raw": result.get("_raw", "")}
    return {
        "score": round(float(result.get("relevancy_score", 0)), 4),
        "reason": result.get("reason", ""),
    }


# ═══════════════════════════════════════
# 主流程
# ═══════════════════════════════════════

def run_all():
    embedder, index, chunks = load_best_index()
    query_list = load_queries()
    if not query_list:
        print("❌ 没有匹配的评测查询，请检查 eval/queries.json")
        return
    print(f"✅ 就绪！共 {len(chunks)} 个文本块\n")

    llm_cfg = LLMConfig()
    results = []

    for i, q in enumerate(query_list, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(query_list)}] 问题: {q}")
        print(f"{'='*60}")

        # ── 1. 检索 ──
        print("  → 检索...")
        raw_results = hybrid_search(q, embedder, index, top_k=TOP_K)
        retrieved_texts = [r["text"] for r in raw_results]

        # ── 2. 检索质量评估（合并为 1 次调用） ──
        time.sleep(CALL_DELAY)
        print("  → 评估检索质量（批量 8 个 chunk，1 次调用）...")
        retrieval_precision = eval_contextual_precision(q, raw_results)
        time.sleep(CALL_DELAY)
        retrieval_recall = eval_contextual_recall(q, retrieved_texts)

        # ── 3. 回答 ──
        time.sleep(CALL_DELAY)
        print("  → 无 RAG 回答...")
        answer_norag = answer(q, use_rag=False, llm_config=llm_cfg)
        time.sleep(CALL_DELAY)
        print("  → 带 RAG 回答...")
        answer_rag = answer(
            q, embedder=embedder, faiss_index=index, llm_config=llm_cfg,
        )

        # ── 4. 生成质量评估 ──
        time.sleep(CALL_DELAY)
        print("  → 评估生成质量...")
        faithfulness = eval_faithfulness(answer_rag, retrieved_texts)
        time.sleep(CALL_DELAY)
        relevancy = eval_answer_relevancy(q, answer_rag)

        entry = {
            "query": q,
            "answer_norag": answer_norag,
            "answer_rag": answer_rag,
            "retrieval_metrics": {
                "contextual_precision": retrieval_precision,
                "contextual_recall": retrieval_recall,
            },
            "generation_metrics": {
                "faithfulness": faithfulness,
                "answer_relevancy": relevancy,
            },
        }
        results.append(entry)
        print(f"  ✅ 完成")

    # ── 汇总 ──
    def avg_score(items, *keys):
        vals = []
        for r in items:
            d = r
            for k in keys:
                d = d.get(k, {})
            if isinstance(d, (int, float)):
                vals.append(d)
        return round(sum(vals) / len(vals), 4) if vals else 0.0

    avg_precision = avg_score(results, "retrieval_metrics", "contextual_precision", "score")
    avg_recall = avg_score(results, "retrieval_metrics", "contextual_recall", "score")
    avg_faithfulness = avg_score(results, "generation_metrics", "faithfulness", "score")
    avg_relevancy = avg_score(results, "generation_metrics", "answer_relevancy", "score")

    summary = {
        "retrieval": {
            "contextual_precision": avg_precision,
            "contextual_recall": avg_recall,
        },
        "generation": {
            "faithfulness": avg_faithfulness,
            "answer_relevancy": avg_relevancy,
        },
    }

    output = {"summary": summary, "results": results}

    answers_path = Path(__file__).parent.parent / "answers.json"
    answers_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n{'='*60}")
    print("📊 评测汇总")
    print(f"{'='*60}")
    print(f"  检索质量:")
    print(f"    Contextual Precision: {avg_precision:.3f}")
    print(f"    Contextual Recall:    {avg_recall:.3f}")
    print(f"  生成质量:")
    print(f"    Faithfulness:         {avg_faithfulness:.3f}")
    print(f"    Answer Relevancy:     {avg_relevancy:.3f}")
    print(f"\n✅ 全部完成！详情已保存到: {answers_path}")


if __name__ == "__main__":
    run_all()
