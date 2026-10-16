---
id: mamba-2
title: Mamba-2
summary: Mamba-2 recasts a selective state-space recurrence as structured state-space duality, enabling a chunkwise, matrix-friendly training algorithm while retaining bounded recurrent decode state.
type: concept
tags: [ml/llm/architecture]
prereqs: [mamba, linear-transformer-attention]
sources: [https://arxiv.org/abs/2405.21060]
status: explained
created: 2026-10-17
updated: 2026-10-17
---

# Mamba-2

## Summary

[[mamba]] keeps a fixed-size state and makes its update depend on the current token. **Mamba-2** is not just a faster kernel for the same block: state-space duality (SSD) expresses a structured recurrence and a restricted attention-like matrix calculation as two views of one computation. This permits chunkwise work that uses matrix hardware efficiently during training, while autoregressive decoding still advances a bounded state.

## Grounded explanation

A recurrent sequence mixer summarizes prior tokens in a state. A full-attention mixer instead retains position-indexed keys and values. The SSD construction identifies a structured semiseparable matrix whose entries can be evaluated either through a recurrence or through blockwise matrix operations. In Mamba-2, a selective decay controls how previous state is carried forward and a new key–value contribution is written. That shared representation connects the recurrence with [[linear-transformer-attention]] without claiming that it is identical to unrestricted softmax attention.

For a long prompt, processing every token serially would underuse an accelerator. Chunkwise evaluation does parallel work inside blocks and propagates compact state between blocks. During one-token-at-a-time generation, only the updated recurrent state must persist for this mixer; it does not allocate a separate KV entry per earlier token. The state has bounded capacity, so exact retrieval from arbitrarily long histories is not guaranteed. A hybrid decoder may retain some full-attention layers precisely for addressable history.

## When it matters

Compare Mamba-2 with a full-attention baseline and the original Mamba at matched quality, tokenization, training budget, and hardware. Report prefill throughput, decode time, state bytes, long-context retrieval, and tasks requiring rapid changes of remembered information. A paper's kernel speedup is workload-specific evidence, not a universal model-level speedup.

## Prerequisites

- [[mamba]]
- [[linear-transformer-attention]]

## Sources

- [Dao and Gu, *Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality*](https://arxiv.org/abs/2405.21060).
