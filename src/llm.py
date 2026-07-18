"""LLM 调用封装 — 从 .env 读取配置，兼容任何 OpenAI 格式的 API"""

import json
import os
from dataclasses import dataclass
from typing import Any, Optional
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# 加载项目根目录的 .env
_env_loaded = False
def _ensure_env():
    global _env_loaded
    if not _env_loaded:
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        _env_loaded = True


@dataclass
class LLMConfig:
    provider: str = ""                 # 仅用于兼容，不再依赖
    model: str = ""
    temperature: float = 0.3
    max_tokens: int = 1024
    base_url: str = ""
    api_key: str = ""


class ToolCallError(RuntimeError):
    """The model did not return valid arguments for the requested function tool."""


def _from_env(key: str, default: str = "") -> str:
    _ensure_env()
    return os.environ.get(key, default)


def build_client(config: Optional[LLMConfig] = None) -> OpenAI:
    """从 .env 或 config 构建 OpenAI client，优先级：config > .env > 默认"""
    _ensure_env()
    if config is None:
        config = LLMConfig()

    base_url = (
        config.base_url
        or _from_env("LLM_BASE_URL", "https://api.deepseek.com")
    )
    api_key = (
        config.api_key
        or _from_env("LLM_API_KEY")
        or _from_env("DEEPSEEK_API_KEY")
    )
    if not api_key:
        # 回退到 api_key.txt
        key_file = Path(__file__).parent.parent / "api_key.txt"
        if key_file.exists():
            for line in key_file.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    api_key = line
                    break

    if not api_key:
        raise ValueError(
            "未找到 API Key。请在 .env 中设置 LLM_API_KEY，"
            "或设置环境变量 LLM_API_KEY/DEEPSEEK_API_KEY，"
            "或在 api_key.txt 中填入。"
        )

    return OpenAI(api_key=api_key, base_url=base_url)


def chat(
    messages: list[dict],
    config: Optional[LLMConfig] = None,
    system_prompt: Optional[str] = None,
    **kwargs,
) -> str:
    """向 LLM 发送对话请求，返回文本回答"""
    _ensure_env()
    if config is None:
        config = LLMConfig()

    # 允许通过 kwargs 覆盖 config
    for k, v in kwargs.items():
        if hasattr(config, k):
            setattr(config, k, v)

    # 优先级: config > .env > 硬编码默认
    model = config.model or _from_env("LLM_MODEL", "deepseek-chat")
    temperature = config.temperature
    max_tokens = config.max_tokens

    client = build_client(config)

    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    resp = client.chat.completions.create(
        model=model,
        messages=full_messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content


def call_function_tool(
    messages: list[dict],
    tool_name: str,
    description: str,
    parameters: dict[str, Any],
    config: Optional[LLMConfig] = None,
    system_prompt: Optional[str] = None,
) -> dict[str, Any]:
    _ensure_env()
    if config is None:
        config = LLMConfig()

    full_messages: list[dict] = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    response = build_client(config).chat.completions.create(
        model=config.model or _from_env("LLM_MODEL", "deepseek-v4-flash"),
        messages=full_messages,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        tools=[{
            "type": "function",
            "function": {
                "name": tool_name,
                "description": description,
                "parameters": parameters,
            },
        }],
        tool_choice={"type": "function", "function": {"name": tool_name}},
    )

    calls = response.choices[0].message.tool_calls or []
    matching = [call for call in calls if call.function.name == tool_name]
    if not matching:
        raise ToolCallError(f"model did not call required tool: {tool_name}")

    try:
        arguments = json.loads(matching[0].function.arguments)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ToolCallError(f"invalid arguments for tool {tool_name}: {exc}") from exc
    if not isinstance(arguments, dict):
        raise ToolCallError(f"tool {tool_name} arguments must be an object")
    return arguments


if __name__ == "__main__":
    # 测试 DeepSeek 调用
    print("=" * 40)
    print("测试 DeepSeek API...")
    answer = chat(
        messages=[{"role": "user", "content": "用一句话告诉我欧陆风云4是什么游戏"}],
        max_tokens=100,
    )
    print(f"回答: {answer}")
