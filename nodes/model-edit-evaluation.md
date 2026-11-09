---
id: model-edit-evaluation
title: "Model-Edit Evaluation"
summary: "Model-edit evaluation separates target efficacy, generalization, unrelated-behavior preservation and causal attribution under matched decoding and held-out interventions."
type: concept
tags: [ml/evaluation]
prereqs: [model-parameter-editing, paired-benchmark-uncertainty, adaptive-validation-overfitting]
sources: [https://arxiv.org/abs/2202.05262, https://rome.baulab.info/]
status: explained
created: 2026-11-10
updated: 2026-11-10
---

# Model-Edit Evaluation

## Meaning

An edited model can answer the targeted question differently without achieving a useful, reliable repair. Evaluate four different claims: the intended change happened, it transfers to intended variants, unrelated behavior survives, and the intervention rather than another changed setting explains the observation. None follows automatically from a higher aggregate score.

## Mechanism

Start with the exact baseline and a documented [[model-parameter-editing]] intervention. Hold tokenizer, prompts, answer extraction, decoding parameters and token budgets fixed. Evaluate the target, paraphrases and related implications, and an independently selected preservation set. ROME's efficacy, generalization and specificity evaluations exemplify these separate axes for factual edits. Other edit goals need their own acceptance criteria; factual-edit metrics are not a universal reasoning-repair benchmark.

Use appropriate ablations or matched random edits to test whether the selected tensor, direction or scale matters. A random edit control should match the property being ruled out, not just have arbitrary nonzero values. Retain task-level pairs for [[paired-benchmark-uncertainty]]. If many patches were screened on the evaluation tasks, [[adaptive-validation-overfitting]] requires a fresh final assessment; inspecting fewer parameters does not erase that selection.

## One example

An invented patch changes a target answer from wrong to right in 8/10 repeated trials. A paraphrase succeeds in 3/10 and a preservation set falls from 90/100 to 78/100. The target result is encouraging but neither broad generalization nor preserved capability has been shown. If the baseline used a smaller output limit than the patch, even the target comparison is confounded. Restore a matched limit and rerun both before attributing the difference to the edited tensor.

## Check your understanding

Can a matched before/after comparison establish the proposed internal mechanism? It can establish an effect under those conditions, but mechanism needs further targeted controls. Separate changed outputs from why they changed, report failed interventions, and assess multiple independent tasks or edits when claiming a reusable method. Do not convert success on one hand-picked patch into a general repair guarantee.

## Prerequisites

- [[model-parameter-editing]]
- [[paired-benchmark-uncertainty]]
- [[adaptive-validation-overfitting]]

## Sources

- <https://arxiv.org/abs/2202.05262>
- <https://rome.baulab.info/>
