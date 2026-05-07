"""RAG 主流程 - 检索 + 生成"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from llm import chat, LLMConfig
from embed import Embedder, load_index, load_chunks, search


DEFAULT_SYSTEM_PROMPT = """你是欧陆风云4（Europa Universalis IV）游戏专家。你的知识来源是 EU4 Wiki 文档。

请基于以下提供的参考信息回答用户问题。遵循以下规则：
1. 只根据参考信息回答，不要编造 Wiki 上没有的内容
2. 如果参考信息不足以回答，直接说「根据现有资料无法回答」
3. 回答要准确、具体，对 EU4 玩家有帮助"""


def retrieve_context(query: str, embedder: Embedder, index, chunks: list[str],
                     top_k: int = 5) -> str:
    """检索相关上下文，拼接成 LLM 可用的格式"""
    results = search(query, embedder, index, chunks, top_k=top_k)
    if not results:
        return ""

    parts = []
    for i, r in enumerate(results, 1):
        parts.append(f"[参考 {i}] (相关度: {r['score']:.3f})\n{r['text']}")

    return "\n\n".join(parts)


def answer(
    query: str,
    embedder: Embedder = None,
    index=None,
    chunks: list[str] = None,
    llm_config: LLMConfig = None,
    top_k: int = 5,
    use_rag: bool = True,
) -> str:
    """RAG 问答主函数"""
    if llm_config is None:
        llm_config = LLMConfig()

    if use_rag:
        if embedder is None or index is None or chunks is None:
            raise ValueError("开启 RAG 需要提供 embedder, index, chunks")

        context = retrieve_context(query, embedder, index, chunks, top_k=top_k)

        if context:
            full_prompt = f"""参考信息：
{context}

---

用户问题：{query}"""
        else:
            full_prompt = f"""没有找到相关参考信息。

用户问题：{query}"""
    else:
        full_prompt = query

    return chat(
        messages=[{"role": "user", "content": full_prompt}],
        config=llm_config,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
    )


def compare(query: str, embedder: Embedder, index, chunks: list[str]):
    """对比: 不带 RAG vs 带 RAG"""
    print(f"\n{'='*60}")
    print(f"问题: {query}")
    print(f"{'='*60}\n")

    print("--- 不带 RAG（裸模型回答）---")
    no_rag = answer(query, use_rag=False)
    print(no_rag)
    print()

    print("--- 带 RAG ---")
    with_rag = answer(query, embedder=embedder, index=index, chunks=chunks)
    print(with_rag)
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Eu4RAG - 欧陆风云4 RAG 问答系统")
    parser.add_argument("query", nargs="?", help="问题")
    parser.add_argument("--compare", action="store_true", help="对比模式")
    parser.add_argument("--top-k", type=int, default=5, help="检索数量")
    parser.add_argument("--no-rag", action="store_true", help="不使用 RAG")
    parser.add_argument("--provider", default="deepseek", help="LLM 提供商")
    parser.add_argument("--model", default="deepseek-chat", help="模型名")
    args = parser.parse_args()

    print("加载 Embedding 模型...")
    embedder = Embedder()
    _ = embedder.model  # 预加载

    print("加载 FAISS 索引...")
    index = load_index()

    print("加载文本块...")
    chunks = load_chunks()
    print(f"✅ 就绪！共 {len(chunks)} 个文本块\n")

    llm_cfg = LLMConfig(provider=args.provider, model=args.model)

    if args.query:
        if args.compare:
            compare(args.query, embedder, index, chunks)
        else:
            result = answer(
                args.query,
                embedder=embedder, index=index, chunks=chunks,
                llm_config=llm_cfg, top_k=args.top_k,
                use_rag=not args.no_rag,
            )
            print(result)
    else:
        print("Eu4RAG 交互模式（输入 /quit 退出）")
        while True:
            query = input("\n❓ ").strip()
            if query.lower() in ("/quit", "/exit", "/q"):
                break
            if args.compare:
                compare(query, embedder, index, chunks)
            else:
                result = answer(
                    query,
                    embedder=embedder, index=index, chunks=chunks,
                    llm_config=llm_cfg, top_k=args.top_k,
                    use_rag=not args.no_rag,
                )
                print(f"\n💬 {result}")
