---
id: termination-aware-evaluation
title: "Termination-Aware Model Evaluation"
summary: "Termination-aware evaluation records correctness and generation completion separately so token-limit censoring, answer extraction and repetition cannot masquerade as one capability score."
type: concept
tags: [ml/evaluation]
prereqs: [request-token-budget, llm-sampling-controls, measurement]
sources: [https://huggingface.co/docs/transformers/main/en/internal/generation_utils, https://huggingface.co/docs/transformers/main_classes/text_generation]
status: explained
created: 2026-11-10
updated: 2026-11-10
---

# Termination-Aware Model Evaluation

## Meaning

Correctness and completion are different events. A run can give the right answer and continue until its limit, or stop cleanly with the wrong answer. A score based only on extracted answers or only on stopping behavior hides that distinction. Termination-aware evaluation retains both and states how the evaluator treats unfinished output.

## Mechanism

For each run record the allowed budget, generated length, stop condition, extracted answer and grading result. Separate natural end-of-sequence, an explicit stop rule, hard length exhaustion, timeout and infrastructure failure. A [[request-token-budget]] bounds work; it is not a semantic correctness checker. [[llm-sampling-controls]] changes continuation behavior, so hold it fixed for an edit comparison or evaluate a declared sweep separately.

Declare whether an answer before truncation counts and whether later contradictory text invalidates it. Transformers generation utilities document outputs that can end at a maximum length or earlier on an end token; applications still need their own answer extraction and outcome labels. Use [[measurement]] to report a joint table, not a causal claim that every length-limited output was incorrect or that shorter reasoning is better.

## One example

In an invented 100-run evaluation, 40 runs stop cleanly with correct answers, 10 contain a correct answer but hit the limit, 20 stop cleanly with wrong answers, and 30 hit the limit without a correct answer. Extracted correctness is 50/100 under a rule accepting any noncontradicted correct answer. Clean-stop rate is 60/100. Correct-and-clean completion is 40/100. Reporting any one of these as all three would change the claim. If truncated runs are excluded, the conditional accuracy is 40/60, not an all-run accuracy.

## Check your understanding

Does fewer limit hits demonstrate new knowledge? No. A change may reduce repetition, alter stopping, change extraction compliance or genuinely improve solving. Inspect trajectories, compare matched budgets and record correctness versus tokens across a budget sweep. Limit hits censor how long generation would otherwise continue; do not treat the cap as an observed natural completion length.

## Prerequisites

- [[request-token-budget]]
- [[llm-sampling-controls]]
- [[measurement]]

## Sources

- <https://huggingface.co/docs/transformers/main/en/internal/generation_utils>
- <https://huggingface.co/docs/transformers/main_classes/text_generation>
