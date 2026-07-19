# Evaluation Set v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a bilingual, reference-guided 60-question evaluation set and align evaluator scoring with answerability.

**Architecture:** `eval/queries.json` remains a flat list consumed by the existing evaluator. Metadata drives recall prompts, abstention scoring, resume validation, and dataset integrity tests without adding dependencies.

**Tech Stack:** Python, unittest, JSON, GPT-5.5 LLM-as-Judge.

## Global Constraints

- Preserve the old dataset as `eval/queries_v1.json`.
- Keep 60 records as 30 English/Chinese semantic pairs.
- Do not treat the set as a public standard benchmark.

---

### Task 1: Dataset Contract

**Files:**
- Modify: `test/test_evaluator.py`
- Modify: `eval/queries.json`
- Create: `eval/queries_v1.json`

- [ ] Add a failing integrity test for count, pair symmetry, answerability, and reference points.
- [ ] Run `run_rocm.bat -m unittest test.test_evaluator.EvaluationDatasetTest -v` and confirm failure.
- [ ] Archive v1 and replace `queries.json` with the 30-pair v2 set.
- [ ] Run the integrity test and confirm it passes.

### Task 2: Reference-Guided Scoring

**Files:**
- Modify: `src/test.py`
- Modify: `test/test_evaluator.py`

- [ ] Add failing tests showing recall prompts contain reference points and unanswerable recall is not applicable.
- [ ] Add failing tests showing appropriate unanswerable responses receive relevancy credit.
- [ ] Pass query metadata into metric functions and implement the minimum scoring branches.
- [ ] Run `run_rocm.bat -m unittest test.test_evaluator -v` and confirm all tests pass.

### Task 3: Resume Safety and Verification

**Files:**
- Modify: `src/test.py`
- Modify: `test/test_evaluator.py`

- [ ] Add a failing test proving a successful old result with changed query text is not reused.
- [ ] Require exact ID and query-text equality in resume loading.
- [ ] Run the complete 45+ test suite and `git diff --check`.
