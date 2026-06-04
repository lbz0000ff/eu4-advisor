#!/usr/bin/env python
"""一键初始化：爬取 Wiki + 建索引 + 下载 embedding 模型"""
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent

def step(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")

# 1. 爬取
step("1/4 爬取 EU4 Wiki...")
subprocess.run([sys.executable, "src/crawler.py"], cwd=BASE, check=True)

# 2. 分块
step("2/4 分块处理...")
subprocess.run([sys.executable, "src/chunk.py"], cwd=BASE, check=True)

# 3. 建索引
step("3/4 构建 FAISS 索引（下载 embedding 模型约 2GB，首次较慢）...")
subprocess.run([sys.executable, "src/embed.py"], cwd=BASE, check=True)

# 4. 验证
step("4/4 验证...")
result = subprocess.run(
    [sys.executable, "src/rag.py", "what is oirat", "--top-k", "3"],
    cwd=BASE, capture_output=True, text=True,
)
if "Oirat" in result.stdout:
    print("✅ 初始化成功！")
else:
    print("⚠ 验证异常，请检查日志")
    print(result.stdout[-500:])
