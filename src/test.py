"""RAG evaluation with auditable retrieval and LLM-as-Judge outputs."""

import argparse
import json
import os
import re
import sys
import time
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import faiss
from dotenv import load_dotenv


ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))
load_dotenv(ROOT / ".env")

from embed import Embedder
from llm import LLMConfig, chat
from rag import answer, build_agentic_runtime, chunks
from reranker import get_reranker


EVAL_FILE = ROOT / "eval" / "queries.json"
DEFAULT_OUTPUT = ROOT / "answers.json"
TOP_K = 8
CALL_DELAY = 0.5
AGENTIC_MAX_ATTEMPTS = 4
AGENTIC_RETRY_BASE_DELAY = 2.0
TRANSIENT_FAILURE_LIMIT = 3

EU4_CONTEXT = """注意：所有用户问题都是关于《欧陆风云4》（Europa Universalis IV）这款游戏的，不是现实历史。
例如 "What is Prussia?" 问的是游戏中的普鲁士（可玩国家/可成立国家），不是现实中的普鲁士王国。
请始终以游戏机制、游戏内容的角度判断相关性。"""

ABSTENTION_ANSWERS = {
    "知识库中未找到相关信息",
    "未找到相关信息",
    "no relevant information was found in the knowledge base",
    "no relevant information found",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=0, help="只跑前 N 条")
    parser.add_argument("--lang", default="", choices=["en", "zh", ""], help="按语言过滤")
    parser.add_argument("--include-no-rag", action="store_true", help="额外生成无 RAG 对照回答")
    parser.add_argument("--generation-attempts", type=int, default=2, help="空回答或异常时的生成尝试次数")
    parser.add_argument("--call-delay", type=float, default=CALL_DELAY, help="模型调用间隔秒数")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="结果 JSON 路径")
    parser.add_argument("--resume", action="store_true", help="复用输出文件中的成功题目并续跑")
    return parser.parse_args()


def load_queries(args: argparse.Namespace | None = None) -> list[dict[str, Any]]:
    if args is None:
        args = parse_args()
    with EVAL_FILE.open(encoding="utf-8") as file:
        queries = json.load(file)
    if args.lang:
        queries = [item for item in queries if item["lang"] == args.lang]
    if args.sample:
        queries = queries[: args.sample]
    print(
        f"评测集: {len(queries)} 条 | "
        f"语言过滤: {args.lang or '全部'}"
    )
    return queries


def build_generator_config() -> LLMConfig:
    return LLMConfig(
        model=os.environ.get("LLM_MODEL", "deepseek-chat"),
        base_url=os.environ.get("LLM_BASE_URL", ""),
        api_key=os.environ.get("LLM_API_KEY", "") or os.environ.get("DEEPSEEK_API_KEY", ""),
        temperature=0.3,
        max_tokens=1024,
    )


def build_judge_config() -> LLMConfig:
    judge_api_key = (
        os.environ.get("JUDGE_API_KEY", "")
        or os.environ.get("UUAPI_API_KEY", "")
    )
    if not judge_api_key:
        raise ValueError("未设置 JUDGE_API_KEY 或 UUAPI_API_KEY")
    return LLMConfig(
        model=(
            os.environ.get("JUDGE_MODEL", "")
            or os.environ.get("RACE_MODEL", "")
            or "gpt-5.5"
        ),
        base_url=(
            os.environ.get("JUDGE_BASE_URL", "")
            or os.environ.get("UUAPI_BASE_URL", "")
            or "https://uuapi.net/v1"
        ).rstrip("/"),
        api_key=judge_api_key,
        temperature=0.0,
        max_tokens=1024,
    )


def config_metadata(config: LLMConfig) -> dict[str, Any]:
    return {
        "model": config.model,
        "base_url": config.base_url,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
    }


def judge_call(
    prompt: str,
    max_tokens: int = 512,
    config: LLMConfig | None = None,
) -> tuple[str, str, int]:
    """Call the judge and retain the final error instead of swallowing it."""
    base_config = config or build_judge_config()
    call_config = replace(base_config, temperature=0.0, max_tokens=max_tokens)
    last_error = ""
    for attempt in range(1, 4):
        try:
            response = chat(
                messages=[{"role": "user", "content": prompt}],
                config=call_config,
            )
            if response and response.strip():
                return response.strip(), "", attempt
            last_error = "empty_judge_response"
        except Exception as error:
            last_error = f"{type(error).__name__}: {error}"
        if attempt < 3:
            time.sleep(2 ** (attempt - 1))
    return "", last_error, 3


def extract_json(raw: str) -> dict[str, Any] | None:
    if not raw or not raw.strip():
        return None
    text = raw.strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        result = json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError:
        return None
    return result if isinstance(result, dict) else None


def _matches_type(value: Any, expected: type | tuple[type, ...]) -> bool:
    if isinstance(value, bool) and expected in ((int, float), (float, int)):
        return False
    return isinstance(value, expected)


def judge_json(
    prompt: str,
    required_fields: dict[str, type | tuple[type, ...]],
    max_tokens: int = 512,
    config: LLMConfig | None = None,
) -> dict[str, Any]:
    raw, call_error, attempts = judge_call(prompt, max_tokens=max_tokens, config=config)
    metadata = {
        "_judge_raw": raw,
        "_judge_attempts": attempts,
    }
    if call_error:
        return {
            **metadata,
            "_judge_failed": True,
            "_failure_reason": call_error,
        }
    result = extract_json(raw)
    if result is None:
        return {
            **metadata,
            "_judge_failed": True,
            "_failure_reason": "invalid_json",
        }
    for field, expected_type in required_fields.items():
        if field not in result:
            return {
                **metadata,
                "_judge_failed": True,
                "_failure_reason": f"missing_field:{field}",
            }
        if not _matches_type(result[field], expected_type):
            return {
                **metadata,
                "_judge_failed": True,
                "_failure_reason": f"invalid_type:{field}",
            }
    return {**result, **metadata}


def _judge_metadata(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "_judge_raw": result.get("_judge_raw", ""),
        "_judge_attempts": result.get("_judge_attempts", 0),
    }


def _invalid_metric(
    reason: str,
    judge_result: dict[str, Any] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    result = {
        "score": None,
        "valid": False,
        "failure_reason": reason,
        **extra,
    }
    if judge_result is not None:
        result.update(_judge_metadata(judge_result))
    return result


def _valid_score(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    score = float(value)
    return score if 0.0 <= score <= 1.0 else None


def load_components():
    embedder = Embedder()
    _ = embedder.model
    index = faiss.read_index(str(ROOT / "data" / "index" / "global.faiss"))
    reranker = get_reranker()
    _ = reranker.model
    print(f"  索引: {index.ntotal} 向量")
    return embedder, index, reranker


def eval_contextual_precision(
    query: str,
    retrieved_chunks: list[dict],
    judge_config: LLMConfig | None = None,
) -> dict[str, Any]:
    selected = retrieved_chunks[:TOP_K]
    if not selected:
        return {
            "score": 0.0,
            "valid": True,
            "relevant_chunks": 0,
            "total": 0,
            "chunk_judgments": [],
            "evaluation_mode": "deterministic_empty_retrieval",
        }

    documents = "\n\n".join(
        f"[{rank}] {item['text']}"
        for rank, item in enumerate(selected, 1)
    )
    prompt = f"""{EU4_CONTEXT}

判断每个检索块是否与用户问题相关。必须为每个编号返回一项，且只输出 JSON。

用户问题:
{query}

检索块:
{documents}

输出格式:
{{"judgments":[{{"rank":1,"relevant":true,"reason":"一句话理由"}}]}}"""
    judged = judge_json(
        prompt,
        required_fields={"judgments": list},
        max_tokens=1536,
        config=judge_config,
    )
    if judged.get("_judge_failed"):
        return _invalid_metric(
            judged["_failure_reason"],
            judged,
            relevant_chunks=None,
            total=len(selected),
            chunk_judgments=[],
        )

    judgments = judged["judgments"]
    if len(judgments) != len(selected):
        return _invalid_metric(
            "judgment_count_mismatch",
            judged,
            relevant_chunks=None,
            total=len(selected),
            chunk_judgments=[],
        )

    by_rank: dict[int, dict[str, Any]] = {}
    for item in judgments:
        if not isinstance(item, dict):
            return _invalid_metric("invalid_judgment_item", judged, total=len(selected))
        rank = item.get("rank")
        relevant = item.get("relevant")
        if not isinstance(rank, int) or not isinstance(relevant, bool):
            return _invalid_metric("invalid_judgment_schema", judged, total=len(selected))
        by_rank[rank] = item
    if set(by_rank) != set(range(1, len(selected) + 1)):
        return _invalid_metric("invalid_judgment_ranks", judged, total=len(selected))

    mapped = []
    relevant_count = 0
    for rank, retrieved in enumerate(selected, 1):
        item = by_rank[rank]
        if item["relevant"]:
            relevant_count += 1
        mapped.append(
            {
                "rank": rank,
                "score": round(float(retrieved.get("score", 0.0)), 4),
                "relevant": item["relevant"],
                "reason": str(item.get("reason", "")),
            }
        )
    return {
        "score": round(relevant_count / len(selected), 4),
        "valid": True,
        "relevant_chunks": relevant_count,
        "total": len(selected),
        "chunk_judgments": mapped,
        **_judge_metadata(judged),
    }


def eval_contextual_recall(
    query: str,
    all_chunk_texts: list[str],
    judge_config: LLMConfig | None = None,
    reference_points: list[str] | None = None,
    answerable: bool = True,
) -> dict[str, Any]:
    if not answerable:
        return _invalid_metric("not_applicable_unanswerable")
    if not all_chunk_texts:
        return {
            "score": 0.0,
            "valid": True,
            "reason": "无检索结果",
            "evaluation_mode": "deterministic_empty_retrieval",
        }
    combined = "\n\n---\n\n".join(all_chunk_texts[:TOP_K])
    expected = "\n".join(f"- {point}" for point in (reference_points or []))
    prompt = f"""{EU4_CONTEXT}

判断检索内容是否覆盖参考答案要点并足以回答用户问题。只输出 JSON。

用户问题:
{query}

参考答案要点:
{expected or "未提供额外要点，请根据问题判断"}

检索内容:
{combined}

输出格式:
{{"score":0.0,"reason":"一句话理由"}}
score 必须在 0.0 到 1.0 之间。"""
    judged = judge_json(
        prompt,
        required_fields={"score": (int, float), "reason": str},
        config=judge_config,
    )
    if judged.get("_judge_failed"):
        return _invalid_metric(judged["_failure_reason"], judged)
    score = _valid_score(judged["score"])
    if score is None:
        return _invalid_metric("score_out_of_range", judged)
    return {
        "score": round(score, 4),
        "valid": True,
        "reason": judged["reason"],
        **_judge_metadata(judged),
    }


def _normalized_answer(answer_text: str) -> str:
    return re.sub(r"[\s。.!！]+$", "", answer_text.strip().lower())


def is_abstention(answer_text: str) -> bool:
    return _normalized_answer(answer_text) in ABSTENTION_ANSWERS


def eval_faithfulness(
    answer_text: str,
    chunk_texts: list[str],
    judge_config: LLMConfig | None = None,
) -> dict[str, Any]:
    if not answer_text or not answer_text.strip():
        return _invalid_metric("empty_answer")
    if is_abstention(answer_text):
        return _invalid_metric("abstained")
    if not chunk_texts:
        return _invalid_metric("missing_context")

    context = "\n\n---\n\n".join(chunk_texts[:TOP_K])
    prompt = f"""判断 AI 回答是否完全基于所提供的上下文。只输出 JSON。

上下文:
{context}

AI 回答:
{answer_text}

输出格式:
{{"faithfulness_score":0.0,"hallucinations":[],"supported_claims":[]}}
faithfulness_score 必须在 0.0 到 1.0 之间。"""
    judged = judge_json(
        prompt,
        required_fields={
            "faithfulness_score": (int, float),
            "hallucinations": list,
            "supported_claims": list,
        },
        max_tokens=1536,
        config=judge_config,
    )
    if judged.get("_judge_failed"):
        return _invalid_metric(judged["_failure_reason"], judged)
    score = _valid_score(judged["faithfulness_score"])
    if score is None:
        return _invalid_metric("score_out_of_range", judged)
    return {
        "score": round(score, 4),
        "valid": True,
        "hallucinations": judged["hallucinations"],
        "supported_claims": judged["supported_claims"],
        **_judge_metadata(judged),
    }


def eval_answer_relevancy(
    query: str,
    answer_text: str,
    judge_config: LLMConfig | None = None,
    answerable: bool = True,
) -> dict[str, Any]:
    if not answer_text or not answer_text.strip():
        return {
            "score": 0.0,
            "valid": True,
            "reason": "回答为空",
            "evaluation_mode": "deterministic_empty_answer",
        }
    if is_abstention(answer_text):
        return {
            "score": 0.0 if answerable else 1.0,
            "valid": True,
            "reason": (
                "可回答问题发生拒答"
                if answerable
                else "不可回答问题被正确拒答"
            ),
            "evaluation_mode": "deterministic_abstention",
        }

    answerability_instruction = (
        "该问题被标记为不可由当前知识库确定回答。回答应明确说明无法确定、"
        "不存在普遍答案或需要额外条件，而不是编造确定结论。"
        if not answerable
        else "该问题可由知识库回答。"
    )
    prompt = f"""{EU4_CONTEXT}

判断 AI 回答是否直接针对用户问题。只输出 JSON。

答案条件:
{answerability_instruction}

用户问题:
{query}

AI 回答:
{answer_text}

输出格式:
{{"relevancy_score":0.0,"reason":"一句话理由"}}
relevancy_score 必须在 0.0 到 1.0 之间。"""
    judged = judge_json(
        prompt,
        required_fields={"relevancy_score": (int, float), "reason": str},
        config=judge_config,
    )
    if judged.get("_judge_failed"):
        return _invalid_metric(judged["_failure_reason"], judged)
    score = _valid_score(judged["relevancy_score"])
    if score is None:
        return _invalid_metric("score_out_of_range", judged)
    return {
        "score": round(score, 4),
        "valid": True,
        "reason": judged["reason"],
        **_judge_metadata(judged),
    }


def generate_no_rag_answer(
    query: str,
    llm_config: LLMConfig,
    max_attempts: int = 2,
) -> dict[str, Any]:
    last_error = "empty_response"
    for attempt in range(1, max_attempts + 1):
        try:
            response = answer(query, use_rag=False, llm_config=llm_config)
            if response and response.strip():
                return {
                    "text": response.strip(),
                    "status": "ok",
                    "attempts": attempt,
                    "failure_reason": "",
                }
            last_error = "empty_response"
        except Exception as error:
            last_error = f"{type(error).__name__}: {error}"
        if attempt < max_attempts:
            time.sleep(1)
    return {
        "text": "",
        "status": "failed",
        "attempts": max_attempts,
        "failure_reason": last_error,
    }


def _nested_score(item: dict[str, Any], *keys: str) -> float | None:
    value: Any = item
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    metric_paths = {
        "contextual_precision": ("retrieval_metrics", "contextual_precision", "score"),
        "contextual_recall": ("retrieval_metrics", "contextual_recall", "score"),
        "faithfulness": ("generation_metrics", "faithfulness", "score"),
        "answer_relevancy": ("generation_metrics", "answer_relevancy", "score"),
    }
    values: dict[str, list[float]] = {}
    for name, path in metric_paths.items():
        values[name] = [
            score
            for result in results
            if (score := _nested_score(result, *path)) is not None
        ]

    def mean(name: str) -> float | None:
        scores = values[name]
        return round(sum(scores) / len(scores), 4) if scores else None

    statuses = [result["generation_status"]["status"] for result in results]
    answers = [result["answer_rag"] for result in results]
    return {
        "retrieval": {
            "contextual_precision": mean("contextual_precision"),
            "contextual_recall": mean("contextual_recall"),
        },
        "generation": {
            "faithfulness": mean("faithfulness"),
            "answer_relevancy": mean("answer_relevancy"),
        },
        "valid_counts": {
            name: {"valid": len(scores), "total": len(results)}
            for name, scores in values.items()
        },
        "answers": {
            "generated": statuses.count("ok"),
            "failed": statuses.count("failed"),
            "abstained": sum(is_abstention(text) for text in answers if text),
            "total": len(results),
        },
    }


def write_output(
    output_path: Path,
    run_config: dict[str, Any],
    results: list[dict[str, Any]],
    complete: bool,
) -> None:
    output = {
        "run_config": {**run_config, "complete": complete},
        "summary": summarize(results),
        "results": results,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_successful_resume_results(
    output_path: Path,
    query_items: list[dict[str, Any]],
) -> dict[Any, dict[str, Any]]:
    if not output_path.exists():
        return {}
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    expected_count = len(query_items)
    previous_count = payload.get("run_config", {}).get("query_count")
    if previous_count != expected_count:
        raise ValueError(
            f"无法续跑: 结果文件配置为 {previous_count} 题，当前为 {expected_count} 题"
        )

    allowed_queries = {item.get("id"): item.get("q") for item in query_items}
    successful: dict[Any, dict[str, Any]] = {}
    for result in payload.get("results", []):
        query_id = result.get("query_id")
        status = result.get("generation_status", {}).get("status")
        if (
            query_id in allowed_queries
            and result.get("query") == allowed_queries[query_id]
            and status == "ok"
        ):
            successful[query_id] = result
    return successful


def order_results(
    query_items: list[dict[str, Any]],
    results_by_id: dict[Any, dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        results_by_id[item.get("id")]
        for item in query_items
        if item.get("id") in results_by_id
    ]


def update_transient_failure_streak(
    current: int,
    state: dict[str, Any],
    limit: int = TRANSIENT_FAILURE_LIMIT,
) -> tuple[int, bool]:
    streak = current + 1 if state.get("transient_failure") else 0
    return streak, streak >= limit


def _format_score(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.3f}"


def _failed_metrics(failure_reason: str) -> dict[str, dict[str, Any]]:
    return {
        "contextual_precision": _invalid_metric(failure_reason),
        "contextual_recall": _invalid_metric(failure_reason),
        "faithfulness": _invalid_metric(failure_reason),
        "answer_relevancy": _invalid_metric(failure_reason),
    }


def agentic_failure_metrics() -> dict[str, dict[str, Any]]:
    return _failed_metrics("agentic_rag_failed")


def is_transient_connection_error(error: BaseException) -> bool:
    current: BaseException | None = error
    seen: set[int] = set()
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if isinstance(current, (ConnectionError, TimeoutError)):
            return True
        if type(current).__name__ in {"APIConnectionError", "APITimeoutError"}:
            return True
        current = current.__cause__ or current.__context__
    return False


def run_agentic_question(
    graph,
    query: str,
    max_attempts: int = 4,
    base_delay: float = 2.0,
    sleep_fn=time.sleep,
) -> dict[str, Any]:
    attempts = max(1, max_attempts)
    for attempt in range(1, attempts + 1):
        try:
            state = graph.invoke(
                {"original_query": query}, config={"recursion_limit": 10}
            )
            state["attempts"] = attempt
            return state
        except Exception as error:
            transient = is_transient_connection_error(error)
            if transient and attempt < attempts:
                delay = base_delay * (2 ** (attempt - 1))
                print(
                    f"  DeepSeek 连接失败，第 {attempt}/{attempts} 次，"
                    f"{delay:g} 秒后重试..."
                )
                sleep_fn(delay)
                continue

            error_type = type(error).__name__
            error_message = str(error)
            return {
                "answer": "",
                "retrieved_results": [],
                "trace": {
                    "plans": [],
                    "retrievals": [],
                    "coverage": [],
                    "failure": {"type": error_type, "message": error_message},
                },
                "failure_reason": f"{error_type}: {error_message}",
                "transient_failure": transient,
                "attempts": attempt,
            }

    raise AssertionError("unreachable")


def generation_status_from_agentic_state(state: dict[str, Any]) -> dict[str, Any]:
    answer_text = state.get("answer", "")
    failure_reason = str(state.get("failure_reason", ""))
    if failure_reason:
        return {
            "text": answer_text if isinstance(answer_text, str) else "",
            "attempts": int(state.get("attempts", 1)),
            "status": "failed",
            "failure_reason": failure_reason,
        }
    if not isinstance(answer_text, str) or not answer_text.strip():
        return {
            "text": "",
            "attempts": 1,
            "status": "failed",
            "failure_reason": "empty_answer",
        }
    return {
        "text": answer_text,
        "attempts": int(state.get("attempts", 1)),
        "status": "ok",
        "failure_reason": "",
    }


def run_all() -> None:
    args = parse_args()
    query_items = load_queries(args)
    if not query_items:
        print("没有匹配的评测查询，请检查 eval/queries.json")
        return

    generator_config = build_generator_config()
    judge_config = build_judge_config()
    embedder, index, reranker = load_components()
    agentic_graph = build_agentic_runtime(
        embedder,
        index,
        reranker=reranker,
        top_k=TOP_K,
        llm_config=generator_config,
    )
    judge_independent = (
        generator_config.model != judge_config.model
        or generator_config.base_url != judge_config.base_url
    )
    if not judge_independent:
        print("警告: 生成模型与 Judge 相同，本次结果不适合作为正式对外分数。")

    run_config = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "query_count": len(query_items),
        "question_set": {
            "path": str(EVAL_FILE),
            "version": "v2",
            "origin": "project-specific, AI-assisted generation",
            "standard_benchmark": False,
            "total_questions": 60,
            "languages": ["zh", "en"],
        },
        "top_k": TOP_K,
        "call_delay_seconds": args.call_delay,
        "generator": config_metadata(generator_config),
        "judge": config_metadata(judge_config),
        "judge_independent": judge_independent,
        "embedding_model": embedder.model_name,
        "reranker_model": reranker.model_name,
        "retrieval": {
            "faiss_candidates": TOP_K * 3,
            "bm25_candidates": TOP_K * 3,
            "fusion": "RRF",
            "rerank_top_k": TOP_K,
        },
        "agentic_rag": {
            "framework": "LangGraph",
            "max_retrieval_rounds": 2,
            "max_queries_per_round": 3,
            "decision_format": "tool_calls + Pydantic",
            "connection_retry": {
                "max_attempts": AGENTIC_MAX_ATTEMPTS,
                "base_delay_seconds": AGENTIC_RETRY_BASE_DELAY,
                "consecutive_failure_limit": TRANSIENT_FAILURE_LIMIT,
            },
        },
    }
    results_by_id = (
        load_successful_resume_results(args.output, query_items)
        if args.resume
        else {}
    )
    if results_by_id:
        print(f"断点续跑: 复用 {len(results_by_id)} 条成功结果")
    consecutive_transient_failures = 0

    for number, query_item in enumerate(query_items, 1):
        query = query_item["q"]
        query_id = query_item.get("id")
        if query_id in results_by_id:
            print(f"[{number}/{len(query_items)}] 已完成，跳过: {query}")
            continue
        print(f"\n{'=' * 60}")
        print(f"[{number}/{len(query_items)}] 问题: {query}")
        print(f"{'=' * 60}")

        print("  -> 运行 Agentic RAG...")
        agentic_state = run_agentic_question(
            agentic_graph,
            query,
            max_attempts=AGENTIC_MAX_ATTEMPTS,
            base_delay=AGENTIC_RETRY_BASE_DELAY,
        )
        retrieved = agentic_state["retrieved_results"]
        retrieved_texts = [item["text"] for item in retrieved]
        generated = generation_status_from_agentic_state(agentic_state)
        answer_rag = generated["text"]

        if generated["status"] == "failed":
            failure_reason = (
                "agentic_rag_failed"
                if agentic_state.get("failure_reason")
                else generated["failure_reason"]
            )
            metrics = _failed_metrics(failure_reason)
            precision = metrics["contextual_precision"]
            recall = metrics["contextual_recall"]
            faithfulness = metrics["faithfulness"]
            relevancy = metrics["answer_relevancy"]
        else:
            time.sleep(args.call_delay)
            print("  -> 评估检索精确率...")
            precision = eval_contextual_precision(query, retrieved, judge_config)
            time.sleep(args.call_delay)
            print("  -> 评估检索覆盖度...")
            recall = eval_contextual_recall(
                query,
                retrieved_texts,
                judge_config,
                reference_points=query_item.get("reference_points", []),
                answerable=query_item.get("answerable", True),
            )

        no_rag = None
        if args.include_no_rag:
            time.sleep(args.call_delay)
            print("  -> 生成无 RAG 对照...")
            no_rag = generate_no_rag_answer(
                query,
                generator_config,
                max_attempts=args.generation_attempts,
            )

        if generated["status"] == "ok":
            time.sleep(args.call_delay)
            print("  -> 评估生成质量...")
            faithfulness = (
                eval_faithfulness(answer_rag, retrieved_texts, judge_config)
                if query_item.get("answerable", True)
                else _invalid_metric("not_applicable_unanswerable")
            )
            time.sleep(args.call_delay)
            relevancy = eval_answer_relevancy(
                query,
                answer_rag,
                judge_config,
                answerable=query_item.get("answerable", True),
            )

        entry = {
            "query_id": query_item.get("id"),
            "pair_id": query_item.get("pair_id"),
            "query": query,
            "lang": query_item.get("lang"),
            "category": query_item.get("cat"),
            "query_type": query_item.get("type"),
            "difficulty": query_item.get("difficulty"),
            "answerable": query_item.get("answerable", True),
            "reference_points": query_item.get("reference_points", []),
            "retrieved_contexts": retrieved,
            "answer_norag": None if no_rag is None else no_rag["text"],
            "no_rag_generation_status": no_rag,
            "answer_rag": answer_rag,
            "generation_status": generated,
            "agent_trace": agentic_state["trace"],
            "retrieval_metrics": {
                "contextual_precision": precision,
                "contextual_recall": recall,
            },
            "generation_metrics": {
                "faithfulness": faithfulness,
                "answer_relevancy": relevancy,
            },
        }
        results_by_id[query_id] = entry
        results = order_results(query_items, results_by_id)
        write_output(args.output, run_config, results, complete=False)
        print("  完成并保存")

        consecutive_transient_failures, should_abort = (
            update_transient_failure_streak(
                consecutive_transient_failures,
                agentic_state,
            )
        )
        if should_abort:
            print(
                f"连续 {TRANSIENT_FAILURE_LIMIT} 题连接失败，评测已中止。"
                "网络恢复后使用 --resume 继续。"
            )
            return

    results = order_results(query_items, results_by_id)
    write_output(args.output, run_config, results, complete=True)
    summary = summarize(results)
    print(f"\n{'=' * 60}")
    print("评测汇总")
    print(f"{'=' * 60}")
    print("  检索质量:")
    print(
        "    Contextual Precision: "
        f"{_format_score(summary['retrieval']['contextual_precision'])}"
    )
    print(
        "    Contextual Recall:    "
        f"{_format_score(summary['retrieval']['contextual_recall'])}"
    )
    print("  生成质量:")
    print(
        "    Faithfulness:         "
        f"{_format_score(summary['generation']['faithfulness'])}"
    )
    print(
        "    Answer Relevancy:     "
        f"{_format_score(summary['generation']['answer_relevancy'])}"
    )
    print(f"  有效样本数: {json.dumps(summary['valid_counts'], ensure_ascii=False)}")
    print(f"\n结果已保存到: {args.output}")


if __name__ == "__main__":
    run_all()
