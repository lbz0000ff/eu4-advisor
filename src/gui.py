"""Eu4RAG Web UI — Gradio"""

import sys
from pathlib import Path

import gradio as gr
import faiss

# rag.py 在顶层加载 chunks 和 parent_tables
from rag import build_agentic_runtime, chunks
from embed import Embedder
from llm import LLMConfig
from reranker import get_reranker

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_DIR = DATA_DIR / "index"


# ═══════════════════════════
# 全局加载（启动时一次）
# ═══════════════════════════

print("加载 Embedding 模型...")
embedder = Embedder()
_ = embedder.model

print("加载 FAISS 索引...")
faiss_index = faiss.read_index(str(INDEX_DIR / "global.faiss"))
print(f"  索引已加载 ({faiss_index.ntotal} 向量)")

categories = sorted(set(c["category"] for c in chunks))


# ═══════════════════════════
# 问答函数
# ═══════════════════════════

def query_fn(question: str, category: str, top_k: int, use_rerank: bool):
    if not question.strip():
        return "", ""

    llm_cfg = LLMConfig()
    reranker = get_reranker() if use_rerank else None

    agentic_graph = build_agentic_runtime(
        embedder,
        faiss_index,
        reranker=reranker,
        category=category,
        top_k=top_k,
        llm_config=llm_cfg,
    )
    state = agentic_graph.invoke(
        {"original_query": question},
        config={"recursion_limit": 10},
    )
    results = state["retrieved_results"]
    llm_answer = state["answer"]

    # 格式化检索明细
    details = ""
    if results:
        parts = []
        for i, r in enumerate(results, 1):
            source = f"`{r['source']}`"
            if r["section"]:
                source += f" / {r['section']}"
            parts.append(
                f"**[{i}] {source}**  (score: {r['score']:.3f})\n\n"
                f">{r['text'][:300]}")
        details = "\n\n".join(parts)

    return llm_answer, details


# ═══════════════════════════
# Gradio 界面
# ═══════════════════════════

css = """
footer {display:none !important}
details {margin-bottom: 1em}
"""

with gr.Blocks(
    title="Eu4RAG",
    theme=gr.themes.Soft(),
    css=css,
) as demo:
    gr.Markdown("# Eu4RAG — EU4 Wiki Q&A")

    with gr.Row():
        cat_dropdown = gr.Dropdown(
            choices=[""] + categories,
            value="",
            label="Category (optional)",
            info="Filter by category",
            scale=2,
        )
        top_k_slider = gr.Slider(
            minimum=4, maximum=20, value=8, step=2,
            label="Top-K",
            scale=1,
        )

    with gr.Row():
        question = gr.Textbox(
            label="Question",
            placeholder="e.g. What are Prussian national ideas?",
            scale=4,
        )
        submit = gr.Button("Submit", variant="primary", scale=1, min_width=100)

    with gr.Row():
        rerank_checkbox = gr.Checkbox(
            label="Cross-Encoder Rerank",
            value=True,
            info="Use cross-encoder to re-rank retrieval results (slower but more accurate)",
        )

    answer_box = gr.Markdown(label="Answer")

    with gr.Accordion("Retrieval Results", open=False):
        details_box = gr.Markdown()

    # 事件绑定
    submit.click(
        fn=query_fn,
        inputs=[question, cat_dropdown, top_k_slider, rerank_checkbox],
        outputs=[answer_box, details_box],
    )
    question.submit(
        fn=query_fn,
        inputs=[question, cat_dropdown, top_k_slider, rerank_checkbox],
        outputs=[answer_box, details_box],
    )


if __name__ == "__main__":
    demo.launch()
