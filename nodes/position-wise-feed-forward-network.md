---
id: position-wise-feed-forward-network
title: Position-Wise Feed-Forward Network
summary: "A Transformer applies the same learned nonlinear channel transformation independently at every sequence position."
type: concept
tags: [ml/llm/architecture]
prereqs: [neural-network, matrix-multiplication, transformer-attention]
sources: [https://arxiv.org/abs/1706.03762]
status: explained
created: 2026-10-09
updated: 2026-10-09
---

# Position-Wise Feed-Forward Network

## Summary

A **position-wise feed-forward network** (FFN) transforms each token representation independently, with the same weights reused at every sequence position. It complements [[transformer-attention]], which mixes information *between* positions. In the original Transformer, an FFN expands width, applies a nonlinearity, then projects back.

## Grounded explanation

For token state $x_i\in\mathbb{R}^{d}$, the original block computes $F(x_i)=\max(0,x_iW_1+b_1)W_2+b_2$. The first [[matrix-multiplication]] maps from model width $d$ to a wider hidden dimension, ReLU adds nonlinearity, and the second maps back to $d$. The same $W_1,W_2$ and biases apply at every position; the operation does not consult other tokens by itself. Attention supplies cross-token context, then FFN transforms the channel representation at each position. Modern gated variants change the activation and multiplication pattern but retain the distinction between token mixing and per-token channel mixing.

For a two-token example, an FFN processes the first and second states with identical parameters yet can produce different outputs because their inputs differ. Swapping the token positions merely swaps those outputs *if no other position signal is added inside this sublayer*. In a Transformer, compare ablations at fixed parameters and compute: remove the FFN, change expansion width, or use a gated variant. Measure quality, inference FLOPs, activation memory, and latency; more width does not guarantee improvement. Verify dimensions and residual compatibility rather than quoting an architecture-specific expansion ratio as universal.

## Prerequisites

- [[neural-network]]
- [[matrix-multiplication]]
- [[transformer-attention]]

## Sources

- [Vaswani et al., Attention Is All You Need](https://arxiv.org/abs/1706.03762): original position-wise FFN equation and encoder/decoder placement.
