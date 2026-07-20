#!/usr/bin/env python
"""一键初始化：爬取、归一化、分块、建索引并验证。"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def step(msg: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


def main() -> None:
    step("1/5 通过 MediaWiki API 爬取 EU4 Wiki...")
    subprocess.run([sys.executable, "scripts/crawl_wiki.py"], cwd=ROOT, check=True)

    step("2/5 归一化 Markdown...")
    subprocess.run([sys.executable, "src/markdown_normalizer.py"], cwd=ROOT, check=True)

    step("3/5 分块处理...")
    subprocess.run([sys.executable, "src/chunk.py"], cwd=ROOT, check=True)

    step("4/5 构建 FAISS 索引，首次运行会下载 Embedding 模型...")
    subprocess.run([sys.executable, "src/embed.py"], cwd=ROOT, check=True)

    step("5/5 验证...")
    result = subprocess.run(
        [sys.executable, "src/rag.py", "what is oirat", "--top-k", "3"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if "Oirat" in result.stdout:
        print("初始化成功！")
    else:
        print("验证异常，请检查日志")
        print(result.stdout[-500:])


if __name__ == "__main__":
    main()
