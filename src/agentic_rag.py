"""Bounded LangGraph retrieval loop with injected external services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, TypedDict, cast

from langgraph.graph import END, START, StateGraph
from openai import OpenAIError
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from llm import LLMConfig, ToolCallError, call_function_tool


MAX_RETRIEVAL_ROUNDS = 2
MAX_QUERIES_PER_ROUND = 3
DEFAULT_TOP_K = 8


class SearchQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query_en: str = Field(min_length=1)
    keywords: list[str] = Field(min_length=1, max_length=5)


class QueryPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    queries: list[SearchQuery] = Field(min_length=1, max_length=MAX_QUERIES_PER_ROUND)


class CoverageDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sufficient: bool
    missing_aspects: list[str]
    supplemental_queries: list[SearchQuery] = Field(max_length=MAX_QUERIES_PER_ROUND)


class QueryPlanningError(RuntimeError):
    """The LLM did not provide a valid query plan after two attempts."""


class CoverageCheckError(RuntimeError):
    """The LLM did not provide a valid coverage decision after two attempts."""


class RetrievalError(RuntimeError):
    """An injected retriever failed for a planned query."""


class AgenticRAGState(TypedDict, total=False):
    original_query: str
    pending_queries: list[dict[str, Any]]
    retrieval_round: int
    retrieved_results: list[dict[str, Any]]
    coverage_sufficient: bool
    missing_aspects: list[str]
    answer: str
    trace: dict[str, list[dict[str, Any]]]


@dataclass(frozen=True)
class AgenticRAGServices:
    planner: Callable[[str], QueryPlan]
    retriever: Callable[[SearchQuery], list[dict[str, Any]]]
    coverage_checker: Callable[[str, list[dict[str, Any]], int], CoverageDecision]
    answer_generator: Callable[[str, list[dict[str, Any]], list[str]], str]


def _score(result: dict[str, Any]) -> float:
    value = result.get("rerank_score")
    if value is None:
        value = result.get("score", result.get("rrf_score", 0.0))
    return float(value)


def _merge_results(
    existing: list[dict[str, Any]],
    incoming: list[dict[str, Any]],
    top_k: int,
) -> list[dict[str, Any]]:
    by_index = {item["chunk_index"]: item for item in existing}
    for item in incoming:
        previous = by_index.get(item["chunk_index"])
        if previous is None or _score(item) > _score(previous):
            by_index[item["chunk_index"]] = item
    return sorted(by_index.values(), key=_score, reverse=True)[:top_k]


def build_agentic_graph(services: AgenticRAGServices, top_k: int = DEFAULT_TOP_K) -> Any:
    """Create a graph which plans once and retrieves for at most two rounds."""
    result_limit = min(max(top_k, 0), DEFAULT_TOP_K)

    def plan_query(state: AgenticRAGState) -> dict[str, Any]:
        plan = services.planner(state["original_query"])
        return {
            "pending_queries": [item.model_dump() for item in plan.queries],
            "retrieval_round": 0,
            "retrieved_results": [],
            "missing_aspects": [],
            "trace": {"plans": [plan.model_dump()], "retrievals": [], "coverage": []},
        }

    def retrieve(state: AgenticRAGState) -> dict[str, Any]:
        pending = [SearchQuery.model_validate(item) for item in state["pending_queries"]]
        incoming: list[dict[str, Any]] = []
        counts: list[dict[str, Any]] = []
        for planned in pending:
            try:
                found = services.retriever(planned)
            except Exception as exc:
                raise RetrievalError(
                    f"retrieve node failed for query {planned.query_en!r}: {exc}"
                ) from exc
            incoming.extend(found)
            counts.append({"query": planned.model_dump(), "count": len(found)})

        trace = {key: list(value) for key, value in state["trace"].items()}
        trace["retrievals"].append(
            {"round": state["retrieval_round"] + 1, "queries": counts}
        )
        return {
            "retrieval_round": state["retrieval_round"] + 1,
            "retrieved_results": _merge_results(
                state.get("retrieved_results", []), incoming, result_limit
            ),
            "trace": trace,
        }

    def check_coverage(state: AgenticRAGState) -> dict[str, Any]:
        decision = services.coverage_checker(
            state["original_query"],
            state["retrieved_results"],
            state["retrieval_round"],
        )
        if (
            state["retrieved_results"]
            and
            not decision.sufficient
            and state["retrieval_round"] < MAX_RETRIEVAL_ROUNDS
            and not decision.supplemental_queries
        ):
            raise CoverageCheckError("insufficient evidence requires supplemental queries")

        trace = {key: list(value) for key, value in state["trace"].items()}
        trace["coverage"].append(
            {"round": state["retrieval_round"], **decision.model_dump()}
        )
        return {
            "coverage_sufficient": decision.sufficient,
            "missing_aspects": decision.missing_aspects,
            "pending_queries": [
                item.model_dump() for item in decision.supplemental_queries
            ],
            "trace": trace,
        }

    def route_after_coverage(state: AgenticRAGState) -> str:
        if (
            state["coverage_sufficient"]
            or state["retrieval_round"] >= MAX_RETRIEVAL_ROUNDS
            or (
                not state["retrieved_results"]
                and not state["pending_queries"]
            )
        ):
            return "generate_answer"
        return "retrieve"

    def generate_answer(state: AgenticRAGState) -> dict[str, str]:
        if not state["retrieved_results"]:
            return {"answer": "知识库中未找到相关信息"}
        return {
            "answer": services.answer_generator(
                state["original_query"],
                state["retrieved_results"],
                state["missing_aspects"],
            )
        }

    builder = StateGraph(AgenticRAGState)
    builder.add_node("plan_query", plan_query)
    builder.add_node("retrieve", retrieve)
    builder.add_node("check_coverage", check_coverage)
    builder.add_node("generate_answer", generate_answer)
    builder.add_edge(START, "plan_query")
    builder.add_edge("plan_query", "retrieve")
    builder.add_edge("retrieve", "check_coverage")
    builder.add_conditional_edges("check_coverage", route_after_coverage)
    builder.add_edge("generate_answer", END)
    return builder.compile()


def _call_validated_tool(
    *,
    prompt: str,
    tool_name: str,
    description: str,
    model_type: type[BaseModel],
    config: LLMConfig,
    error_type: type[RuntimeError],
) -> BaseModel:
    failures: list[str] = []
    schema = model_type.model_json_schema()
    for _ in range(2):
        try:
            arguments = call_function_tool(
                messages=[{"role": "user", "content": prompt}],
                tool_name=tool_name,
                description=description,
                parameters=schema,
                config=config,
            )
            return model_type.model_validate(arguments)
        except (ToolCallError, ValidationError, OpenAIError) as exc:
            failures.append(str(exc))
    raise error_type("; ".join(failures))


def make_llm_planner(config: LLMConfig) -> Callable[[str], QueryPlan]:
    def planner(query: str) -> QueryPlan:
        result = _call_validated_tool(
            prompt=(
                "Convert this Europa Universalis IV question into one to three English Wiki "
                "searches. Use terminology that is likely to appear in the Wiki. Do not "
                f"answer the question.\n\nQuestion: {query}"
            ),
            tool_name="submit_search_plan",
            description="Submit English semantic queries and BM25 keywords for EU4 Wiki retrieval.",
            model_type=QueryPlan,
            config=config,
            error_type=QueryPlanningError,
        )
        return cast(QueryPlan, result)

    return planner


def _coverage_context(evidence: list[dict[str, Any]]) -> str:
    return "\n\n".join(
        f"[{number}] {item['source']} / {item.get('section', '')}\n{item['text'][:2000]}"
        for number, item in enumerate(evidence, 1)
    )


def make_llm_coverage_checker(
    config: LLMConfig,
) -> Callable[[str, list[dict[str, Any]], int], CoverageDecision]:
    def checker(
        query: str, evidence: list[dict[str, Any]], round_number: int
    ) -> CoverageDecision:
        result = _call_validated_tool(
            prompt=(
                "Judge whether the retrieved EU4 Wiki evidence covers every factual part "
                "of the question. If coverage is insufficient, list missing aspects and "
                "submit English supplemental searches. "
                f"This is retrieval round {round_number} of {MAX_RETRIEVAL_ROUNDS}.\n\n"
                f"Question: {query}\n\nEvidence:\n{_coverage_context(evidence)}"
            ),
            tool_name="submit_coverage_decision",
            description="Report evidence coverage and any supplemental English searches.",
            model_type=CoverageDecision,
            config=config,
            error_type=CoverageCheckError,
        )
        return cast(CoverageDecision, result)

    return checker
