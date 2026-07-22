# EU4 Advisor

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

面向《Europa Universalis IV》英文 Wiki 的中英双语 Agentic RAG 问答系统。项目使用 LangGraph 组织查询规划、混合检索、证据覆盖判断和补充检索，并通过 FAISS、BM25、RRF 与 Cross-Encoder 完成检索和重排。

## 核心流程

```text
用户问题
  -> LLM 生成最多 3 条英文检索式与 BM25 关键词
  -> 每条检索式分别执行 FAISS 与 BM25 Top-24 召回
  -> RRF 融合并使用 Cross-Encoder 重排
  -> 合并、去重并保留 Top-8 证据
  -> 判断证据是否覆盖问题
       -> 充分：生成回答
       -> 不充分：生成补充检索式，最多再检索一轮
```

主要能力：

- 将中文问法转换为英文 Wiki 检索式，并拆解多方面问题。
- 通过 MediaWiki API 分层发现页面，并沿国家页中的任务树和事件引用继续 BFS 爬取。
- 使用 FAISS 语义检索与 BM25 关键词检索，经 RRF 融合和 Cross-Encoder 重排。
- 按 Markdown 标题层级分块，将表格逐行展开并保留父表信息。
- 使用 LangGraph 保存查询计划、检索轮次、证据覆盖判断和最终回答。
- 提供单轮混合检索与 Agentic RAG 两种评测模式。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置模型 API

复制 `.env.example` 为 `.env`，至少填写生成模型配置：

```env
LLM_BASE_URL=https://api.deepseek.com
LLM_API_KEY=
LLM_MODEL=deepseek-chat
```

生成模型和评测模型均使用 OpenAI 兼容接口。运行 LLM-as-Judge 评测时，还需填写 `JUDGE_BASE_URL`、`JUDGE_API_KEY` 和 `JUDGE_MODEL`，也可以使用模板中保留的 UUAPI 兼容变量。

`.env` 已被 Git 忽略，不要把真实密钥写入 `.env.example`。

### 3. 下载 Embedding 与重排模型

默认使用以下 Hugging Face 模型：

- `intfloat/multilingual-e5-large`
- `cross-encoder/ms-marco-MiniLM-L-6-v2`

首次建索引或启用重排时，Sentence Transformers 会自动下载所需模型。国内网络可在运行前设置 Hugging Face 镜像：

```powershell
$env:HF_ENDPOINT = "https://hf-mirror.com"
python scripts/setup.py
```

```bash
HF_ENDPOINT=https://hf-mirror.com python scripts/setup.py
```

也可以从 Hugging Face 或镜像站手动下载模型，再在 `.env` 中填写本地目录：

```env
EMBEDDING_MODEL=D:/models/multilingual-e5-large
RERANKER_MODEL=D:/models/ms-marco-MiniLM-L-6-v2
```

模型文件不会提交到仓库。

### 4. 获取 Wiki 数据并建立索引

```bash
python scripts/setup.py
```

该脚本依次执行 MediaWiki API 爬取、Markdown 归一化、结构化分块、Embedding 计算和 FAISS 索引构建。爬虫会从国家页和游戏概念分类开始，并沿任务树与事件引用继续获取页面，完整运行需要较长时间且依赖 Wiki 可访问。

Wiki 原文、归一化文档、分块结果和索引均为本地生成内容，不包含在仓库中。爬取过程可断点续跑，已存在页面会被跳过。

### 5. 运行问答

```bash
python src/rag.py "训练度和士气有什么区别" --rerank
python src/rag.py "How does discipline affect combat?" --rerank
```

不传问题时进入交互模式：

```bash
python src/rag.py --rerank
```

Web 界面：

```bash
python src/gui.py
```

## 评测

项目测试集包含 60 条中英双语问题，其中 30 组问题互为中英文语义对应，并包含不可回答问题。生成模型使用 DeepSeek V4 Flash，GPT-5.5 作为独立 Judge，按照检索精确率、检索召回率、回答忠实度和回答相关性分别评分。

```bash
python src/test.py --mode baseline --output eval/results/baseline.json
python src/test.py --mode agentic --output eval/results/agentic.json
```

完整 60 题结果：

| 模式 | 检索精确率 | 检索召回率 | 回答忠实度 | 回答相关性 |
|---|---:|---:|---:|---:|
| 原始问题单轮混合检索 | 0.408 | 0.591 | 0.866 | 0.573 |
| Agentic RAG | 0.656 | 0.843 | 0.855 | 0.829 |

逐题结果包含生成内容和调用轨迹，因此 `eval/results/` 默认不提交。评测题目和评测程序保留在仓库中，可使用自己的模型接口复现。

## 项目结构

```text
eu4-advisor/
├── src/
│   ├── agentic_rag.py       # LangGraph 查询规划与覆盖反馈
│   ├── rag.py               # 混合检索、回答生成与 CLI
│   ├── embed.py             # Embedding 与 FAISS 索引
│   ├── reranker.py          # Cross-Encoder 重排
│   ├── chunk.py             # Markdown 与表格分块
│   ├── eu4_crawler.py       # MediaWiki API 与 wikitext 清洗
│   ├── batch_crawl.py       # 页面发现、批量爬取与状态记录
│   ├── markdown_normalizer.py # Markdown 二次归一化
│   ├── llm.py               # OpenAI 兼容模型接口
│   ├── test.py              # baseline 与 Agentic RAG 评测
│   └── gui.py               # Gradio 界面
├── eval/
│   ├── queries.json         # 60 条中英双语项目测试问题
│   └── queries_v1.json      # 旧版测试问题备份
├── scripts/
│   ├── crawl_wiki.py        # 分层 BFS 爬取策略
│   └── setup.py             # 爬取、归一化、分块与建索引
├── test/                    # 单元测试
├── .env.example
└── requirements.txt
```

## 测试

```bash
python -m unittest discover -s test -p "test_*.py"
```

## 数据与版权

Wiki 数据来源于 [Europa Universalis IV Wiki](https://eu4.paradoxwikis.com/)，版权归 Paradox Interactive 和 Wiki 贡献者所有。本仓库仅包含代码和项目测试问题，不包含 Wiki 原文。

## License

MIT
