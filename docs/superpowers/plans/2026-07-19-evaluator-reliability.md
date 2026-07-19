# Evaluator Reliability Implementation Plan

1. Add failing evaluator tests for transient retry classification and backoff.
2. Preserve provider exceptions through Agentic RAG decision errors.
3. Add resume result loading, ordering, and success filtering with tests.
4. Add consecutive transient-failure circuit breaking with tests.
5. Run focused and full test suites, then document the resume command.
