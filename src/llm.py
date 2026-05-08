"""LLM 调用封装 - 支持 DeepSeek 和 SiliconFlow（Qwen 等）"""

import os
from dataclasses import dataclass, field
from typing import Optional
from openai import OpenAI


@dataclass
class LLMConfig:
    provider: str = "deepseek"          # "deepseek" | "siliconflow"
    model: str = "deepseek-v4-flash"        # deepseek-chat / Qwen/Qwen3.5-4B
    temperature: float = 0.3
    max_tokens: int = 1024
    base_urls: dict = field(default_factory=lambda: {
        "deepseek": "https://api.deepseek.com",
        "siliconflow": "https://api.siliconflow.cn/v1",
    })


def load_api_key(provider: str = "deepseek") -> str:
    """按优先级读取 API Key: 环境变量 > api_key.txt"""
    env_var_map = {
        "deepseek": "DEEPSEEK_API_KEY",
        "siliconflow": "SILICONFLOW_API_KEY",
    }
    env_var = env_var_map.get(provider)
    if env_var and (key := os.environ.get(env_var)):
        return key

    # 从项目根目录的 api_key.txt 读取
    key_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "api_key.txt")
    if os.path.exists(key_file):
        with open(key_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line

    raise ValueError(f"未找到 {provider} 的 API Key。请设置环境变量 {env_var} 或在 api_key.txt 中填入。")


def build_client(config: LLMConfig) -> OpenAI:
    """构建 OpenAI-compatible client"""
    base_url = config.base_urls[config.provider]
    api_key = load_api_key(config.provider)
    return OpenAI(api_key=api_key, base_url=base_url)


def chat(
    messages: list[dict],
    config: Optional[LLMConfig] = None,
    system_prompt: Optional[str] = None,
    **kwargs,
) -> str:
    """向 LLM 发送对话请求，返回文本回答"""
    if config is None:
        config = LLMConfig()

    # 允许通过 kwargs 覆盖 config
    for k, v in kwargs.items():
        if hasattr(config, k):
            setattr(config, k, v)

    client = build_client(config)

    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    resp = client.chat.completions.create(
        model=config.model,
        messages=full_messages,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    # 测试 DeepSeek 调用
    print("=" * 40)
    print("测试 DeepSeek API...")
    answer = chat(
        messages=[{"role": "user", "content": "用一句话告诉我欧陆风云4是什么游戏"}],
        max_tokens=100,
    )
    print(f"回答: {answer}")
