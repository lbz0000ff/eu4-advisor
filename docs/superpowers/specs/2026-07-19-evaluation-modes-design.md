# Evaluation Modes Design

## Goal

Run a fair v2 comparison between the historical single-pass Hybrid RAG pipeline and the LangGraph Agentic RAG pipeline.

## Modes

- `baseline`: send the original user query directly to FAISS and BM25, fuse with RRF, rerank once, keep Top-8, and generate from those same results.
- `agentic`: use the existing LangGraph query planner, up to two retrieval rounds, coverage checking, Top-8 merge, and answer generation.
- Both modes use identical embedding, reranker, generator, Judge, question set, answer prompt, and metric functions.

## Safety

- Add required CLI option `--mode baseline|agentic`.
- Store `evaluation_mode` in run configuration and every result entry.
- Resume rejects an output created by the other mode.
- Baseline calls retrieval exactly once per question and records an auditable trace.
- Existing transient connection retry and circuit-breaker behavior applies to both modes.

## Verification

- Unit-test single retrieval and result reuse in baseline.
- Unit-test CLI mode parsing and resume mode mismatch.
- Run a one-pair smoke for each mode to distinct output files.
