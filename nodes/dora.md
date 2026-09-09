---
id: dora
title: DoRA
summary: DoRA adapts a pretrained weight by training its output-channel magnitudes separately from a LoRA-parameterized directional update.
type: concept
tags: [ml/deep-learning]
prereqs: [lora, low-rank-factorization, fine-tuning]
sources: [https://arxiv.org/abs/2402.09353]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# DoRA

## Summary

**Weight-Decomposed Low-Rank Adaptation (DoRA)** separates the magnitude and direction of a pretrained weight matrix, then uses [[lora]] to adapt direction while learning magnitude directly.

## Grounded explanation

For a weight matrix $W$ whose columns correspond to output directions, write a column-wise decomposition

$$W=m\odot\frac{V}{\lVert V\rVert_c},$$

where $m$ stores column magnitudes, $V$ stores directions, $\lVert\cdot\rVert_c$ denotes column-wise norms, and $m$ is applied column by column to the normalized matrix.

DoRA freezes the pretrained directional base and forms

$$V'=W_0+BA,$$

where $BA$ is the [[low-rank-factorization]] learned by LoRA. The effective adapted weight is

$$W'=m\odot\frac{V'}{\lVert V'\rVert_c}.$$

Thus magnitude updates are not constrained to be low-rank, while directional updates remain parameter-efficient. The exact decomposition axis and shape convention depend on the layer implementation and must match the paper and framework code.

DoRA is still a [[fine-tuning]] method, not a guarantee of better quality at every rank or task. Normalization adds training computation and numerical considerations; parameter count, optimizer state, and merge behavior differ from plain LoRA. After training, implementations can often materialize or merge the effective weight for inference, subject to the serving representation and runtime constraints.

Compare against LoRA and full fine-tuning at matched trainable-parameter, data, step, and search budgets. Report quality, convergence variance, peak memory, training throughput, adapter storage, and inference latency before and after merge. Test zero or tiny column norms and mixed-precision stability.

## Prerequisites

- [[lora]]
- [[low-rank-factorization]]
- [[fine-tuning]]

## Sources

- [Liu et al., “DoRA: Weight-Decomposed Low-Rank Adaptation”](https://arxiv.org/abs/2402.09353): proposes separate magnitude and LoRA-based directional adaptation and evaluates it against LoRA and full fine-tuning.
