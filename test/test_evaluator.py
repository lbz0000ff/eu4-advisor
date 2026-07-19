import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import rag


spec = importlib.util.spec_from_file_location("rag_evaluator", ROOT / "src" / "test.py")
evaluator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(evaluator)


class RagAnswerTest(unittest.TestCase):
    def test_answer_reuses_provided_retrieval_results(self) -> None:
        retrieved = [
            {
                "source": "wiki.md",
                "section": "AE",
                "text": "Improve relations increases aggressive expansion decay.",
                "score": 1.0,
            }
        ]

        with (
            patch.object(rag, "hybrid_search", side_effect=AssertionError("retrieved twice")),
            patch("llm.chat", return_value="answer") as chat,
        ):
            result = rag.answer(
                "How to reduce AE?",
                retrieved_results=retrieved,
            )

        self.assertEqual(result, "answer")
        self.assertIn("Improve relations", chat.call_args.kwargs["messages"][0]["content"])


class AgenticEvaluationTest(unittest.TestCase):
    def test_transient_connection_failure_retries_with_exponential_backoff(self) -> None:
        graph = unittest.mock.MagicMock()
        graph.invoke.side_effect = [
            ConnectionError("network down"),
            TimeoutError("request timed out"),
            {
                "answer": "answer",
                "retrieved_results": [{"text": "context"}],
                "trace": {"plans": [], "retrievals": [], "coverage": []},
            },
        ]
        sleep = unittest.mock.MagicMock()

        result = evaluator.run_agentic_question(
            graph,
            "query",
            max_attempts=4,
            base_delay=2.0,
            sleep_fn=sleep,
        )

        self.assertEqual(result["answer"], "answer")
        self.assertEqual(graph.invoke.call_count, 3)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [2.0, 4.0])

    def test_non_transient_graph_failure_is_not_retried(self) -> None:
        graph = unittest.mock.MagicMock()
        graph.invoke.side_effect = RuntimeError("invalid graph state")

        result = evaluator.run_agentic_question(graph, "query", max_attempts=4)

        self.assertEqual(graph.invoke.call_count, 1)
        self.assertFalse(result["transient_failure"])

    def test_exhausted_connection_retries_are_marked_transient(self) -> None:
        graph = unittest.mock.MagicMock()
        graph.invoke.side_effect = ConnectionError("network down")

        result = evaluator.run_agentic_question(
            graph,
            "query",
            max_attempts=3,
            base_delay=0,
        )

        self.assertEqual(graph.invoke.call_count, 3)
        self.assertTrue(result["transient_failure"])

    def test_one_graph_invocation_returns_answer_contexts_and_trace(self) -> None:
        graph = unittest.mock.MagicMock()
        graph.invoke.return_value = {
            "answer": "answer",
            "retrieved_results": [{"text": "context"}],
            "trace": {"plans": [], "retrievals": [], "coverage": []},
        }

        result = evaluator.run_agentic_question(graph, "query")

        graph.invoke.assert_called_once_with(
            {"original_query": "query"},
            config={"recursion_limit": 10},
        )
        self.assertEqual(result["answer"], "answer")
        self.assertEqual(result["retrieved_results"][0]["text"], "context")
        self.assertEqual(result["trace"]["plans"], [])

    def test_graph_failure_returns_auditable_state_without_retry(self) -> None:
        graph = unittest.mock.MagicMock()
        graph.invoke.side_effect = RuntimeError("planner unavailable")

        result = evaluator.run_agentic_question(graph, "query")

        graph.invoke.assert_called_once_with(
            {"original_query": "query"},
            config={"recursion_limit": 10},
        )
        self.assertEqual(result["answer"], "")
        self.assertEqual(result["retrieved_results"], [])
        self.assertEqual(result["failure_reason"], "RuntimeError: planner unavailable")
        self.assertEqual(
            result["trace"]["failure"],
            {"type": "RuntimeError", "message": "planner unavailable"},
        )

    def test_empty_agentic_answer_is_a_failed_generation(self) -> None:
        status = evaluator.generation_status_from_agentic_state({"answer": ""})

        self.assertEqual(status["status"], "failed")
        self.assertEqual(status["failure_reason"], "empty_answer")

    def test_agentic_failure_metrics_are_invalid(self) -> None:
        metrics = evaluator.agentic_failure_metrics()

        self.assertFalse(metrics["contextual_precision"]["valid"])
        self.assertIsNone(metrics["contextual_precision"]["score"])
        self.assertEqual(
            metrics["answer_relevancy"]["failure_reason"],
            "agentic_rag_failed",
        )


class EvaluationResumeTest(unittest.TestCase):
    def test_resume_keeps_only_successful_matching_queries(self) -> None:
        payload = {
            "run_config": {"query_count": 3},
            "results": [
                {"query_id": 101, "generation_status": {"status": "ok"}},
                {"query_id": 102, "generation_status": {"status": "failed"}},
                {"query_id": 999, "generation_status": {"status": "ok"}},
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.json"
            path.write_text(json.dumps(payload), encoding="utf-8")

            resumed = evaluator.load_successful_resume_results(
                path,
                [{"id": 101}, {"id": 102}, {"id": 103}],
            )

        self.assertEqual(set(resumed), {101})

    def test_results_are_written_in_query_order(self) -> None:
        ordered = evaluator.order_results(
            [{"id": 101}, {"id": 102}, {"id": 103}],
            {103: {"query_id": 103}, 101: {"query_id": 101}},
        )

        self.assertEqual([item["query_id"] for item in ordered], [101, 103])

    def test_transient_failure_streak_resets_and_trips_at_limit(self) -> None:
        self.assertEqual(
            evaluator.update_transient_failure_streak(
                2, {"transient_failure": False}, limit=3
            ),
            (0, False),
        )
        self.assertEqual(
            evaluator.update_transient_failure_streak(
                2, {"transient_failure": True}, limit=3
            ),
            (3, True),
        )


class JudgeParsingTest(unittest.TestCase):
    def test_judge_defaults_to_linar_uuapi_gpt_5_5(self) -> None:
        with patch.dict(
            "os.environ",
            {"UUAPI_API_KEY": "uuapi-key"},
            clear=True,
        ):
            config = evaluator.build_judge_config()

        self.assertEqual(config.base_url, "https://uuapi.net/v1")
        self.assertEqual(config.model, "gpt-5.5")
        self.assertEqual(config.api_key, "uuapi-key")

    def test_extract_json_rejects_number_only_fallback(self) -> None:
        self.assertIsNone(evaluator.extract_json("I would give this 0.9"))

    def test_judge_json_rejects_missing_required_field_and_keeps_raw(self) -> None:
        raw = '{"score": 1.0}'

        with patch.object(evaluator, "judge_call", return_value=(raw, "", 1)):
            result = evaluator.judge_json(
                "prompt",
                required_fields={"faithfulness_score": (int, float)},
            )

        self.assertTrue(result["_judge_failed"])
        self.assertIn("faithfulness_score", result["_failure_reason"])
        self.assertEqual(result["_judge_raw"], raw)


class MetricEvaluationTest(unittest.TestCase):
    def test_contextual_precision_batches_all_chunks_in_one_judge_call(self) -> None:
        retrieved = [
            {"text": "relevant", "score": 0.9},
            {"text": "irrelevant", "score": 0.8},
        ]
        judged = {
            "judgments": [
                {"rank": 1, "relevant": True, "reason": "yes"},
                {"rank": 2, "relevant": False, "reason": "no"},
            ],
            "_judge_raw": "raw",
            "_judge_attempts": 1,
        }

        with patch.object(evaluator, "judge_json", return_value=judged) as judge:
            result = evaluator.eval_contextual_precision("query", retrieved)

        self.assertEqual(judge.call_count, 1)
        self.assertEqual(result["score"], 0.5)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["_judge_raw"], "raw")

    def test_empty_answer_is_invalid_without_calling_judge(self) -> None:
        with patch.object(
            evaluator,
            "judge_json",
            side_effect=AssertionError("judge should not be called"),
        ):
            result = evaluator.eval_faithfulness("", ["context"])

        self.assertIsNone(result["score"])
        self.assertFalse(result["valid"])
        self.assertEqual(result["failure_reason"], "empty_answer")


class SummaryTest(unittest.TestCase):
    def test_summarize_does_not_count_failed_agentic_generation(self) -> None:
        summary = evaluator.summarize(
            [
                {"generation_status": {"status": "ok"}, "answer_rag": "answer"},
                {"generation_status": {"status": "failed"}, "answer_rag": ""},
            ]
        )

        self.assertEqual(summary["answers"]["generated"], 1)
        self.assertEqual(summary["answers"]["failed"], 1)
        self.assertEqual(summary["answers"]["total"], 2)


if __name__ == "__main__":
    unittest.main()
