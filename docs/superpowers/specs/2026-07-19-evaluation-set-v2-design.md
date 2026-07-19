# Evaluation Set v2 Design

## Goal

Replace the exploratory 60-question set with a stable project evaluation set that supports retrieval comparisons, bilingual analysis, and abstention checks.

## Dataset

- Keep 60 questions as 30 semantically equivalent English/Chinese pairs.
- Use natural Chinese phrasing while preserving the same information need as the English pair.
- Remove patch-specific, typo-dependent, and undefined strategy-superlative questions from the answerable subset.
- Store `pair_id`, `difficulty`, `answerable`, and `reference_points` on every item.
- Include three bilingual unanswerable pairs covering universal optimum, guaranteed strategy, and future-version prediction.
- Preserve the original dataset as `eval/queries_v1.json`.

## Evaluation

- Contextual Recall for answerable questions is judged against explicit reference points.
- Contextual Recall is not applicable for unanswerable questions.
- Answer Relevancy for unanswerable questions rewards a clear refusal or qualification and penalizes fabricated certainty.
- Resume only reuses a prior result when both query ID and exact query text match.

## Validation

- Exactly 60 records and 30 pair IDs.
- Every pair contains one English and one Chinese record.
- Pair members have identical answerability, category, type, and reference points.
- Every answerable item has at least two reference points.
