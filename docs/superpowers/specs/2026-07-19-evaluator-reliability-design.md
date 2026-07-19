# Evaluator Reliability Design

## Goal

Prevent transient provider outages from silently contaminating a long RAG evaluation and allow an interrupted run to continue without repeating successful questions.

## Behavior

- Retry transient API connection and timeout failures up to four total attempts.
- Use exponential delays of 2, 4, and 8 seconds between attempts.
- Do not retry schema, validation, authentication, or other deterministic failures.
- Mark the final failure as transient and persist it for auditability.
- Abort after three consecutive questions exhaust their transient retries.
- Add `--resume`. It loads the selected output file, keeps successful matching query IDs, and reruns failed or missing questions.
- Persist results in evaluation-set order after every completed question.

## Boundaries

- Retry a whole LangGraph invocation from a clean state.
- Preserve the original exception as a cause when planner or coverage retries are exhausted so the evaluator can classify failures by type.
- Existing behavior remains unchanged unless a transient failure occurs or `--resume` is supplied.

## Tests

- Transient graph failures retry with exponential delays and can recover.
- Non-transient graph failures are not retried.
- Exhausted transient retries are marked in the returned state.
- Resume retains successful entries and schedules failed or missing entries.
- Three consecutive exhausted transient questions trigger the circuit breaker.
