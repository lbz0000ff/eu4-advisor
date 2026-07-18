import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import llm


class LlmConfigTest(unittest.TestCase):
    def test_build_client_accepts_config_specific_api_key(self) -> None:
        config = llm.LLMConfig(
            model="judge",
            base_url="https://judge.example/v1",
            api_key="judge-key",
        )

        with patch.object(llm, "OpenAI") as client:
            llm.build_client(config)

        client.assert_called_once_with(
            api_key="judge-key",
            base_url="https://judge.example/v1",
        )


def _tool_response(name: str, arguments: str):
    call = SimpleNamespace(function=SimpleNamespace(name=name, arguments=arguments))
    message = SimpleNamespace(tool_calls=[call])
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class FunctionToolCallTest(unittest.TestCase):
    def test_returns_decoded_arguments_from_named_tool(self) -> None:
        client = MagicMock()
        client.chat.completions.create.return_value = _tool_response(
            "submit_plan",
            json.dumps({"queries": [{"query_en": "Oirat missions", "keywords": ["Oirat"]}]}),
        )

        with patch.object(llm, "build_client", return_value=client):
            result = llm.call_function_tool(
                messages=[{"role": "user", "content": "plan this query"}],
                tool_name="submit_plan",
                description="Submit retrieval queries.",
                parameters={"type": "object", "properties": {}, "additionalProperties": False},
                config=llm.LLMConfig(model="deepseek-v4-flash"),
            )

        self.assertEqual(result["queries"][0]["query_en"], "Oirat missions")
        request = client.chat.completions.create.call_args.kwargs
        self.assertEqual(request["tools"][0]["function"]["name"], "submit_plan")
        self.assertEqual(request["tool_choice"]["function"]["name"], "submit_plan")

    def test_rejects_response_without_requested_tool(self) -> None:
        client = MagicMock()
        client.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(tool_calls=None))]
        )
        with patch.object(llm, "build_client", return_value=client):
            with self.assertRaises(llm.ToolCallError):
                llm.call_function_tool(
                    messages=[],
                    tool_name="submit_plan",
                    description="Submit retrieval queries.",
                    parameters={"type": "object", "properties": {}},
                    config=llm.LLMConfig(model="deepseek-v4-flash"),
                )

    def test_rejects_malformed_tool_arguments(self) -> None:
        client = MagicMock()
        client.chat.completions.create.return_value = _tool_response("submit_plan", "{bad json")
        with patch.object(llm, "build_client", return_value=client):
            with self.assertRaises(llm.ToolCallError):
                llm.call_function_tool(
                    messages=[],
                    tool_name="submit_plan",
                    description="Submit retrieval queries.",
                    parameters={"type": "object", "properties": {}},
                    config=llm.LLMConfig(model="deepseek-v4-flash"),
                )


if __name__ == "__main__":
    unittest.main()
