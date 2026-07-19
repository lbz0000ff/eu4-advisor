# Evaluation Modes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add explicit baseline and agentic evaluation modes with comparable outputs.

**Architecture:** Mode-specific execution produces the same evaluator state contract. Shared persistence, scoring, retry, and summary code consumes that contract.

**Tech Stack:** Python, unittest, FAISS, BM25, Cross-Encoder, LangGraph.

## Global Constraints

- Baseline performs exactly one direct hybrid retrieval using the original query.
- Agentic behavior remains unchanged.
- Results from different modes cannot be resumed into each other.

---

### Task 1: Baseline State Contract

- [ ] Add a failing test for one hybrid retrieval and answer generation from the returned Top-8.
- [ ] Implement `run_baseline_question` returning answer, retrieved results, trace, and failure metadata.
- [ ] Apply the existing transient retry behavior to baseline generation.

### Task 2: CLI Routing and Persistence

- [ ] Add a failing parser test for `--mode`.
- [ ] Add mode-specific runtime construction and execution in `run_all`.
- [ ] Persist mode in run configuration and result entries.

### Task 3: Resume Safety and Verification

- [ ] Add a failing test for resume mode mismatch.
- [ ] Validate prior `evaluation_mode` before reusing results.
- [ ] Run focused tests, the complete suite, and one bilingual smoke per mode.
