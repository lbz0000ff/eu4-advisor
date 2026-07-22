import sys
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import agentic_rag
from agentic_rag import (
    AgenticRAGServices,
    CoverageCheckError,
    CoverageDecision,
    QueryPlan,
    QueryPlanningError,
    RetrievalError,
    SearchQuery,
    build_agentic_graph,
    make_llm_coverage_checker,
    make_llm_planner,
)
from llm import LLMConfig
from openai import OpenAIError
from pydantic import ValidationError


def hit(index: int, score: float = 1.0) -> dict:
    return {
        "chunk_index": index,
        "source": f"{index}.md",
        "section": "section",
        "text": f"evidence {index}",
        "score": score,
        "rrf_score": score,
        "rerank_score": score,
    }


class AgenticRAGGraphTest(unittest.TestCase):
    def test_sufficient_first_round_routes_directly_to_answer(self) -> None:
        calls: list[str] = []
        services = AgenticRAGServices(
            planner=lambda query: QueryPlan(
                queries=[SearchQuery(query_en="Oirat", keywords=["Oirat"])]
            ),
            retriever=lambda query: calls.append(query.query_en) or [hit(1)],
            coverage_checker=lambda query, evidence, round_number: CoverageDecision(
                sufficient=True, missing_aspects=[], supplemental_queries=[]
            ),
            answer_generator=lambda query, evidence, missing: "grounded answer",
        )

        result = build_agentic_graph(services).invoke({"original_query": "瓦剌是什么？"})

        self.assertEqual(calls, ["Oirat"])
        self.assertEqual(result["retrieval_round"], 1)
        self.assertEqual(result["answer"], "grounded answer")

    def test_insufficient_first_round_runs_one_supplemental_round(self) -> None:
        coverage_calls = 0

        def check(query: str, evidence: list[dict], round_number: int) -> CoverageDecision:
            nonlocal coverage_calls
            coverage_calls += 1
            if round_number == 1:
                return CoverageDecision(
                    sufficient=False,
                    missing_aspects=["missions"],
                    supplemental_queries=[
                        SearchQuery(
                            query_en="Oirat missions", keywords=["Oirat missions"]
                        )
                    ],
                )
            return CoverageDecision(
                sufficient=False,
                missing_aspects=["mission rewards"],
                supplemental_queries=[SearchQuery(query_en="unused", keywords=["unused"])],
            )

        services = AgenticRAGServices(
            planner=lambda query: QueryPlan(
                queries=[SearchQuery(query_en="Oirat", keywords=["Oirat"])]
            ),
            retriever=lambda query: [hit(1)]
            if query.query_en == "Oirat"
            else [hit(1, 0.5), hit(2)],
            coverage_checker=check,
            answer_generator=lambda query, evidence, missing: f"{len(evidence)} chunks",
        )

        result = build_agentic_graph(services).invoke({"original_query": "瓦剌任务有什么？"})

        self.assertEqual(coverage_calls, 2)
        self.assertEqual(result["retrieval_round"], 2)
        self.assertEqual([item["chunk_index"] for item in result["retrieved_results"]], [1, 2])
        self.assertEqual(result["answer"], "2 chunks")
        self.assertEqual(len(result["trace"]["coverage"]), 2)

    def test_result_merge_keeps_higher_scoring_duplicate(self) -> None:
        services = AgenticRAGServices(
            planner=lambda query: QueryPlan(
                queries=[
                    SearchQuery(query_en="q1", keywords=["q1"]),
                    SearchQuery(query_en="q2", keywords=["q2"]),
                ]
            ),
            retriever=lambda query: [hit(7, 0.2)]
            if query.query_en == "q1"
            else [hit(7, 0.9)],
            coverage_checker=lambda *args: CoverageDecision(
                sufficient=True, missing_aspects=[], supplemental_queries=[]
            ),
            answer_generator=lambda *args: "answer",
        )

        result = build_agentic_graph(services).invoke({"original_query": "question"})

        self.assertEqual(len(result["retrieved_results"]), 1)
        self.assertEqual(result["retrieved_results"][0]["score"], 0.9)

    def test_retrieval_error_identifies_failed_query(self) -> None:
        services = AgenticRAGServices(
            planner=lambda query: QueryPlan(
                queries=[SearchQuery(query_en="Oirat", keywords=["Oirat"])]
            ),
            retriever=lambda query: (_ for _ in ()).throw(RuntimeError("index unavailable")),
            coverage_checker=lambda *args: CoverageDecision(
                sufficient=True, missing_aspects=[], supplemental_queries=[]
            ),
            answer_generator=lambda *args: "answer",
        )

        with self.assertRaisesRegex(RetrievalError, "Oirat"):
            build_agentic_graph(services).invoke({"original_query": "瓦剌是什么？"})

    def test_result_count_is_capped_at_eight_across_two_rounds(self) -> None:
        services = AgenticRAGServices(
            planner=lambda query: QueryPlan(
                queries=[
                    SearchQuery(query_en="first", keywords=["first"]),
                    SearchQuery(query_en="second", keywords=["second"]),
                    SearchQuery(query_en="third", keywords=["third"]),
                ]
            ),
            retriever=lambda query: [hit(index, float(index)) for index in range(10)],
            coverage_checker=lambda query, evidence, round_number: CoverageDecision(
                sufficient=round_number == 2,
                missing_aspects=[],
                supplemental_queries=[]
                if round_number == 2
                else [SearchQuery(query_en="supplement", keywords=["supplement"])],
            ),
            answer_generator=lambda *args: "answer",
        )

        result = build_agentic_graph(services, top_k=99).invoke({"original_query": "question"})

        self.assertEqual(result["retrieval_round"], 2)
        self.assertEqual(len(result["retrieved_results"]), 8)
        self.assertEqual(
            [item["chunk_index"] for item in result["retrieved_results"]],
            list(range(9, 1, -1)),
        )

    def test_insufficient_coverage_without_supplemental_queries_is_an_error(self) -> None:
        services = AgenticRAGServices(
            planner=lambda query: QueryPlan(
                queries=[SearchQuery(query_en="Oirat", keywords=["Oirat"])]
            ),
            retriever=lambda query: [hit(1)],
            coverage_checker=lambda *args: CoverageDecision(
                sufficient=False, missing_aspects=["missions"], supplemental_queries=[]
            ),
            answer_generator=lambda *args: "answer",
        )

        with self.assertRaises(CoverageCheckError):
            build_agentic_graph(services).invoke({"original_query": "question"})

    def test_empty_first_round_without_supplemental_queries_returns_fixed_answer(self) -> None:
        retrieval_calls: list[str] = []
        answer_calls: list[str] = []
        services = AgenticRAGServices(
            planner=lambda query: QueryPlan(
                queries=[SearchQuery(query_en="Oirat", keywords=["Oirat"])]
            ),
            retriever=lambda query: retrieval_calls.append(query.query_en) or [],
            coverage_checker=lambda *args: CoverageDecision(
                sufficient=False, missing_aspects=["facts"], supplemental_queries=[]
            ),
            answer_generator=lambda *args: answer_calls.append("called") or "unexpected",
        )

        result = build_agentic_graph(services).invoke({"original_query": "question"})

        self.assertEqual(retrieval_calls, ["Oirat"])
        self.assertEqual(result["retrieval_round"], 1)
        self.assertEqual(result["answer"], "知识库中未找到相关信息")
        self.assertEqual(answer_calls, [])


class LLMDecisionContractTest(unittest.TestCase):
    def test_planner_enforces_keyword_limit_on_tool_arguments(self) -> None:
        planner = make_llm_planner(LLMConfig(model="deepseek-v4-flash"))
        oversized = {
            "queries": [
                {
                    "query_en": "Crownland mechanics",
                    "keywords": ["one", "two", "three", "four", "five", "six"],
                }
            ]
        }

        with patch.object(
            agentic_rag, "call_function_tool", return_value=oversized
        ) as tool_call:
            result = planner("How does Crownland work?")

        self.assertEqual(result.queries[0].keywords, ["one", "two", "three", "four", "five"])
        tool_call.assert_called_once()

    def test_planner_disables_thinking_for_forced_tool_call(self) -> None:
        planner = make_llm_planner(LLMConfig(model="deepseek-v4-flash"))
        valid = {
            "queries": [
                {"query_en": "Oirat missions", "keywords": ["Oirat", "missions"]}
            ]
        }

        with patch.object(
            agentic_rag, "call_function_tool", return_value=valid
        ) as tool_call:
            planner("瓦剌任务是什么？")

        self.assertFalse(tool_call.call_args.kwargs["thinking"])

    def test_query_plan_schema_forbids_extra_properties(self) -> None:
        schema = QueryPlan.model_json_schema()

        self.assertIs(schema["additionalProperties"], False)
        self.assertIs(schema["$defs"]["SearchQuery"]["additionalProperties"], False)

    def test_query_plan_rejects_more_than_three_queries(self) -> None:
        with self.assertRaises(ValidationError):
            QueryPlan.model_validate(
                {
                    "queries": [
                        {"query_en": str(index), "keywords": [str(index)]}
                        for index in range(4)
                    ]
                }
            )

    def test_invalid_planner_tool_arguments_are_retried_twice_then_fail(self) -> None:
        invalid = {
            "queries": [
                {
                    "query_en": "Oirat missions",
                    "keywords": ["Oirat"],
                    "unexpected": True,
                }
            ]
        }
        planner = make_llm_planner(LLMConfig(model="deepseek-v4-flash"))

        with patch.object(agentic_rag, "call_function_tool", return_value=invalid) as tool_call:
            with self.assertRaises(QueryPlanningError):
                planner("瓦剌任务是什么？")

        self.assertEqual(tool_call.call_count, 2)

    def test_invalid_coverage_tool_arguments_are_retried_twice_then_fail(self) -> None:
        checker = make_llm_coverage_checker(LLMConfig(model="deepseek-v4-flash"))

        with patch.object(agentic_rag, "call_function_tool", return_value={"sufficient": True}) as tool_call:
            with self.assertRaises(CoverageCheckError):
                checker("question", [hit(1)], 1)

        self.assertEqual(tool_call.call_count, 2)

    def test_planner_openai_error_is_retried_twice_then_converted(self) -> None:
        planner = make_llm_planner(LLMConfig(model="deepseek-v4-flash"))

        with patch.object(
            agentic_rag,
            "call_function_tool",
            side_effect=OpenAIError("connection failed"),
        ) as tool_call:
            with self.assertRaises(QueryPlanningError):
                planner("瓦剌任务是什么？")

        self.assertEqual(tool_call.call_count, 2)

    def test_coverage_openai_error_is_retried_twice_then_converted(self) -> None:
        checker = make_llm_coverage_checker(LLMConfig(model="deepseek-v4-flash"))

        with patch.object(
            agentic_rag,
            "call_function_tool",
            side_effect=OpenAIError("request timed out"),
        ) as tool_call:
            with self.assertRaises(CoverageCheckError):
                checker("question", [hit(1)], 1)

        self.assertEqual(tool_call.call_count, 2)


if __name__ == "__main__":
    unittest.main()
