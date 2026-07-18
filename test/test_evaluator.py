import importlib.util
import sys
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


class GenerationTest(unittest.TestCase):
    def test_generate_rag_answer_retries_empty_response(self) -> None:
        retrieved = [{"text": "context"}]

        with patch.object(evaluator, "answer", side_effect=["", "final answer"]) as answer:
            result = evaluator.generate_rag_answer(
                "query",
                retrieved,
                evaluator.LLMConfig(model="generator"),
                max_attempts=2,
            )

        self.assertEqual(result["text"], "final answer")
        self.assertEqual(result["attempts"], 2)
        self.assertEqual(result["status"], "ok")
        self.assertIs(answer.call_args.kwargs["retrieved_results"], retrieved)


if __name__ == "__main__":
    unittest.main()
