"""RAG 主流程 - 检索 + 生成"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from llm import chat, LLMConfig
from embed import (
    Embedder, search,
    load_index, load_chunks,
    list_categories, load_category_index, load_category_chunks,
    CATEGORY_NAMES,
)


DEFAULT_SYSTEM_PROMPT = """你是欧陆风云4（Europa Universalis IV）游戏专家。你的知识来源是 EU4 Wiki 文档。

请基于以下提供的参考信息回答用户问题。遵循以下规则：
1. 优先使用参考信息，综合你了解的信息进行回答
2. 如果参考信息覆盖了问题的一部分，如实回答你知道的部分，不需要追求「全部回答」
3. 不要编造数据或捏造数字，但可以根据上下文做合理推断
4. 回答要准确、具体，对 EU4 玩家有帮助，用中文回答问题。"""


def retrieve_context(query: str, embedder: Embedder, index, chunks: list[str],
                     top_k: int = 8) -> str:
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
    top_k: int = 8,
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
            full_prompt = f"参考信息：\n{context}\n---\n用户问题：{query}"
        else:
            full_prompt = f"没有找到相关参考信息。\n用户问题：{query}"
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


def show_categories():
    """打印可用类别"""
    cat_info = list_categories()
    if not cat_info:
        print("⚠ 还没有建过分索引，请先运行 `python3 src/embed.py` 重建")
        print("  或者继续使用旧版单索引模式（不加 --category）")
    else:
        print("可用类别：")
        for cat, info in sorted(cat_info.items()):
            print(f"  {cat:20s} → {info['name']:25s} ({info['chunks']} 块, {info['pages']} 页面)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Eu4RAG - 欧陆风云4 RAG 问答系统")
    parser.add_argument("query", nargs="?", help="问题")
    parser.add_argument("--compare", action="store_true", help="对比模式")
    parser.add_argument("--top-k", type=int, default=8, help="检索数量")
    parser.add_argument("--no-rag", action="store_true", help="不使用 RAG")
    parser.add_argument("--provider", default="deepseek", help="LLM 提供商")
    parser.add_argument("--model", default="deepseek-v4-flash", help="模型名")
    parser.add_argument("--category", default=None,
                        help="指定类别（如 diplomacy/warfare/economy），不加则用旧版全量索引")
    parser.add_argument("--list-categories", action="store_true",
                        help="列出所有已建索引的类别")
    args = parser.parse_args()

    # 纯查询模式：只看类别列表
    if args.list_categories:
        show_categories()
        sys.exit(0)

    print("加载 Embedding 模型...")
    embedder = Embedder()
    _ = embedder.model  # 预加载

    if args.category:
        # ── 按类别检索 ──
        cat = args.category
        cat_info = list_categories()
        if not cat_info:
            print("⚠ 还没有建过类别索引。请先运行 `python3 src/embed.py` 重建")
            sys.exit(1)
        if cat not in cat_info:
            print(f"⚠ 无效类别 '{cat}'，可用类别：")
            show_categories()
            sys.exit(1)
        print(f"加载类别索引: {cat} ({cat_info[cat]['name']})...")
        index = load_category_index(cat)
        chunks = load_category_chunks(cat)
    else:
        # ── 旧版：全量索引（向后兼容） ──
        print("加载全量 FAISS 索引...")
        index = load_index()
        print("加载全量文本块...")
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
        cat_label = f"[类别: {args.category}] " if args.category else ""
        print(f"Eu4RAG 交互模式 {cat_label}（输入 /quit 退出）")
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
