# Eu4RAG — EU4 Wiki 检索增强问答系统

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

面向《Europa Universalis IV》Wiki 的中英文混合 RAG 问答系统。支持中文查询自动翻译与扩展、FAISS + BM25 混合检索、Cross-Encoder 重排。

## 功能

- **中英文混合查询** — 中文问题自动翻译成英文检索词，同时提取关键词给 BM25
- **混合检索** — FAISS 语义检索 + BM25 关键词检索 + RRF 融合 + Cross-Encoder 重排
- **结构化分块** — 基于标题层级 + 表格行级展开，保留父表引用
- **查询扩展** — LLM 自动补充 EU4 领域同义词，提高检索命中率
- **Web GUI** — Gradio 界面，支持分类过滤和重排开关
- **CLI 交互** — 命令行问答和对比评测模式

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

创建 `.env` 文件（已提供模板），填入你的 API Key：

```env
LLM_BASE_URL=https://api.deepseek.com
LLM_API_KEY=sk-your-key-here
LLM_MODEL=deepseek-chat
```

支持任何 OpenAI 兼容的 API，切换只需改 `.env`：

```env
# 本地 Ollama
LLM_BASE_URL=http://localhost:8000/v1
LLM_API_KEY=not-needed
LLM_MODEL=qwen2.5:14b

# OpenAI
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-xxx
LLM_MODEL=gpt-4o-mini
```

### 3. 初始化（爬取 Wiki + 建索引）

```bash
python scripts/setup.py
```

这将依次执行：爬取 Wiki 页面 → 分块处理 → 构建 FAISS 索引。首次运行需下载 embedding 模型（约 2GB）。

### 4. 运行

**Web 界面：**
```bash
python src/gui.py
```

**命令行问答：**
```bash
python src/rag.py "瓦剌是什么国家"
python src/rag.py "how to form prussia" --rerank
```

**交互模式：**
```bash
python src/rag.py
```

## 项目结构

```
Eu4RAG/
├── src/                    # 核心代码
│   ├── rag.py              # RAG 主流程（检索 + 问答）
│   ├── embed.py            # Embedding + FAISS 索引构建
│   ├── llm.py              # LLM 调用封装（OpenAI 兼容）
│   ├── chunk.py            # 维基页面分块
│   ├── crawler.py          # EU4 Wiki 爬虫
│   ├── gui.py              # Gradio Web 界面
│   └── reranker.py         # Cross-Encoder 重排
├── eval/                   # 评测集（中英文 160+ 条）
│   ├── queries.json
│   └── run_eval.py
├── scripts/
│   └── setup.py            # 一键初始化脚本
├── data/                   # 数据（gitignore，运行 setup 生成）
│   ├── raw/                # 爬取的 Wiki 页面
│   ├── chunks/             # 分块结果
│   └── index/              # FAISS 索引
├── .env                    # API 配置模板
└── requirements.txt
```

## 检索流程

```
用户查询 (中/英/混合)
    ↓
LLM 预处理（翻译 + 关键词提取 + 查询扩展）
    ↓
┌─ FAISS 语义检索 (top-72) ─┐
│ BM25 关键词检索 (top-72)  │
└────── RRF 融合 ──────────┘
    ↓ top-24
Cross-Encoder 重排
    ↓ top-8
LLM 生成回答
```

## 评测

```bash
# 跑 10 条样本
python src/test.py --sample 10

# 跑全部 160+ 条
python src/test.py
```

评测指标：
- **Contextual Precision** — 检索结果中相关 chunk 的比例
- **Contextual Recall** — 检索结果对问题的信息覆盖度
- **Faithfulness** — 回答是否忠实于检索内容
- **Answer Relevancy** — 回答是否扣题

## 技术栈

| 组件 | 选型 |
|---|---|
| Embedding | intfloat/multilingual-e5-large (1024d) |
| 向量检索 | FAISS IndexFlatIP (余弦相似度) |
| 关键词检索 | BM25Okapi (rank_bm25) |
| 重排 | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| 融合策略 | RRF (K=20) |
| LLM | DeepSeek / OpenAI / 本地模型 (OpenAI 兼容) |
| 分块 | MarkdownHeaderTextSplitter + RecursiveCharacter |
| UI | Gradio |

## 免责声明

本项目使用的 Wiki 数据来源于 [Europa Universalis IV Wiki](https://eu4.paradoxwikis.com/)，版权归 Paradox Interactive 和 Wiki 贡献者所有。本仓库仅包含代码，不包含 Wiki 内容。用户需自行运行爬虫获取数据。

## License

MIT
