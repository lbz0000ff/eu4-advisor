# OiratRAG Agentic RAG Design

## Goal

Use LangGraph to add a small retrieval-feedback loop to OiratRAG. The system should improve Chinese and complex-question retrieval without replacing the existing FAISS, BM25, RRF, and Cross-Encoder pipeline.

## Scope

The first version contains four nodes:

1. `plan_query`: convert the original question into one to three English search queries with BM25 keywords.
2. `retrieve`: run the existing hybrid retrieval pipeline for each planned query, merge duplicate chunks, and retain retrieval metadata.
3. `check_coverage`: ask the LLM whether the retrieved evidence covers the question. If it does not, produce one to three supplemental search queries.
4. `generate_answer`: answer only from the accumulated evidence and explicitly state which requested aspects are not covered.

The graph performs at most two retrieval rounds. It does not add conversation memory, checkpoint persistence, LangSmith, `ToolNode`, multiple agents, or human approval.

## Architecture

LangGraph is used only for stateful orchestration and conditional routing. Existing OpenAI-compatible model calls remain in `src/llm.py`, and the retrieval algorithms remain independent of LangGraph.

```text
START
  -> plan_query
  -> retrieve
  -> check_coverage
       -> generate_answer when evidence is sufficient
       -> retrieve when evidence is insufficient and round < 2
  -> generate_answer after the second retrieval round
  -> END
```

`src/agentic_rag.py` will own the graph state, node functions, routing function, and graph construction. `src/rag.py` will expose a preprocessing-free retrieval function that accepts an English semantic query and BM25 keywords. This separates LLM planning from deterministic retrieval.

## State

The graph state contains:

- `original_query`: the user's unmodified question.
- `pending_queries`: one to three validated English semantic queries and their BM25 keywords.
- `retrieval_round`: the number of completed retrieval rounds.
- `retrieved_results`: deduplicated chunks accumulated across rounds.
- `coverage_sufficient`: the latest coverage decision.
- `missing_aspects`: aspects that are not supported by current evidence.
- `answer`: the final grounded answer.
- `trace`: query plans, retrieval counts, coverage decisions, and failures needed for evaluation and debugging.

State contains serializable data only. Model clients, embedders, FAISS indexes, and rerankers are injected into node closures when the graph is built rather than stored in graph state.

## Data Flow

The query planner receives the original question and returns strict JSON. Each planned item contains `query_en` and `keywords`. The output is validated before retrieval; Chinese text is not silently passed into the English index when planning fails.

The retrieval node runs FAISS, BM25, RRF, and optional Cross-Encoder reranking for every pending query. Results are deduplicated by chunk index. Existing scores, source, section, and category remain available in the trace and final context.

The coverage node receives the original question plus compact retrieved evidence. It returns strict JSON containing `sufficient`, `missing_aspects`, and `supplemental_queries`. Supplemental queries are used only when the first round is insufficient. After the second round, the graph always proceeds to answer generation.

The answer node uses the original question and all accumulated evidence. It must not introduce facts absent from the evidence. When evidence remains incomplete, it lists the unsupported aspects instead of guessing.

## Error Handling

- Planner and coverage JSON are parsed and validated with explicit schemas.
- Invalid or empty LLM output is retried up to two times.
- Exhausted planner retries raise `QueryPlanningError`; there is no raw-query fallback.
- Exhausted coverage retries raise `CoverageCheckError`; there is no assumed-success fallback.
- Retrieval exceptions retain the node name and query in the raised error.
- An empty retrieval result proceeds to answer generation with a deterministic no-evidence response.
- The two-round limit is enforced by graph state and tested independently of model behavior.

## Testing

Tests use fake planner, coverage checker, and retriever dependencies so graph behavior does not require API calls or model downloads.

Coverage includes:

- planner output validation and retry exhaustion;
- sufficient evidence routing directly to answer generation;
- insufficient evidence triggering exactly one supplemental retrieval round;
- second-round termination even when coverage remains insufficient;
- result deduplication across subqueries and rounds;
- trace preservation for plans, retrievals, and coverage decisions;
- compatibility of the existing CLI and evaluator with supplied retrieved results;
- a five-question bilingual smoke evaluation after unit tests pass.

## LangGraph API Surface

The implementation uses only the Graph API required by this workflow:

- `StateGraph` to define the shared-state workflow;
- `START` and `END` as graph boundaries;
- `add_node` to register the four node functions;
- `add_edge` for fixed transitions;
- `add_conditional_edges` for coverage-based routing;
- `compile` to produce an executable graph;
- `invoke` for synchronous execution.

Persistence, streaming, `Command`, `Send`, subgraphs, and message-specific state are intentionally excluded from this version.

