---
id: causal-language-model-training
title: Causal Language-Model Training
summary: Causal language-model training predicts each next token from only its prefix, using a mask that blocks future-token information even when training positions run in parallel.
type: concept
tags: [ml/llm/training]
prereqs: [transformer-attention, subword-tokenization, softmax]
sources: [https://arxiv.org/abs/2005.14165, https://arxiv.org/abs/1706.03762]
status: explained
created: 2026-10-10
updated: 2026-10-10
---

# Causal Language-Model Training

## Summary

A causal language model learns a conditional distribution for token $x_t$ given only earlier tokens $x_{<t}$. Its training target is the next token at each position, not a reconstruction of the full sequence from both directions.

## Grounded explanation

First convert text to discrete units with [[subword-tokenization]]. For a sequence $x_1,\ldots,x_T$, maximize $\sum_{t=1}^{T}\log p_\theta(x_t\mid x_{<t})$, or minimize its negative. A Transformer can evaluate many training positions at once: a triangular mask sets attention scores for future keys to an excluded value before [[softmax]], while [[transformer-attention]] combines only the permitted prefix states. Parallel teacher-forced training therefore does not imply parallel autoregressive generation; at inference the next sampled token becomes part of the following prefix.

For a short sequence “red fox runs,” the position predicting “fox” may read “red” but not “runs.” Shift inputs and labels consistently: an off-by-one target or inverted mask can leak the answer and produce deceptively low loss. Padding positions need their own loss mask. A document boundary needs an explicit policy so one sample does not inadvertently train on another document's private continuation.

The objective estimates next-token likelihood, not factual truth, instruction following, or safe tool use. Compare held-out loss and task-specific behavior across data splits; check contamination, mask orientation, rare-token slices, and generation quality. Altering the context length or tokenizer changes the experiment. The cited model papers ground the autoregressive objective, not a claim that it is optimal for every downstream task.

## Sources

- [Brown et al., GPT-3](https://arxiv.org/abs/2005.14165): autoregressive language-model objective and evaluation.
- [Vaswani et al., Transformer](https://arxiv.org/abs/1706.03762): masked decoder self-attention.
