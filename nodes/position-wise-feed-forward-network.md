---
id: position-wise-feed-forward-network
title: Position-Wise Feed-Forward Network
summary: "A Transformer applies the same learned nonlinear channel transformation independently at every sequence position."
type: concept
tags: [ml/llm/architecture]
prereqs: [neural-network, matrix-multiplication, transformer-attention, residual-connection]
sources: [https://arxiv.org/abs/1706.03762]
status: explained
created: 2026-10-09
updated: 2026-11-10
---

# Position-Wise Feed-Forward Network

## Summary

A **position-wise feed-forward network** (FFN) transforms each token representation independently, with the same weights reused at every sequence position. It complements [[transformer-attention]], which mixes information *between* positions. In the original Transformer, an FFN expands width, applies a nonlinearity, then projects back.

## Grounded explanation

For token state $x_i\in\mathbb{R}^{d}$, the original block computes $F(x_i)=\max(0,x_iW_1+b_1)W_2+b_2$. The first [[matrix-multiplication]] maps from model width $d$ to a wider hidden dimension, ReLU adds nonlinearity, and the second maps back to $d$. The same $W_1,W_2$ and biases apply at every position; the operation does not consult other tokens by itself. Attention supplies cross-token context, then FFN transforms the channel representation at each position. Modern gated variants change the activation and multiplication pattern but retain the distinction between token mixing and per-token channel mixing.

For a two-token example, an FFN processes the first and second states with identical parameters yet can produce different outputs because their inputs differ. Swapping the token positions merely swaps those outputs *if no other position signal is added inside this sublayer*. In a Transformer, compare ablations at fixed parameters and compute: remove the FFN, change expansion width, or use a gated variant. Measure quality, inference FLOPs, activation memory, and latency; more width does not guarantee improvement. Verify dimensions and residual compatibility rather than quoting an architecture-specific expansion ratio as universal.

## Feature-dependent writes into a residual state

The output projection also has a useful column view. Use column-vector notation in this subsection: let h be the m-dimensional hidden feature vector after the activation or gate, D a d-by-m output matrix, and b a d-dimensional bias. Write D's columns as $d_j$. Then the sublayer output is $Dh+b=\sum_{j=1}^{m}h_jd_j+b$. Each feature scales one output direction. A surrounding [[residual-connection]] adds this contribution to a carried d-dimensional token state; pre-normalization, post-normalization and gating determine the exact full block.

For an invented m=3, d=2 example, take columns (1,0), (0,2), (1,-1), hidden activations h=(2,1,3), and zero output bias. The output is 2(1,0)+1(0,2)+3(1,-1)=(5,-1). With carried state (4,6), residual addition gives (9,5). If the third column changes by (0.5,0), the output changes by 3(0.5,0)=(1.5,0), and the new residual state is (10.5,5). On another input with the third activation zero, that column edit contributes no immediate change.

This decomposition explains input-dependent effect, not independent semantic ownership of each feature. A direction can serve several behaviors, and later layers can mix its consequences. Verify the implementation's matrix orientation, gated hidden activation and normalization placement; copying a “column edit” into a row-oriented formulation can target the wrong feature. The equation above describes this sublayer's immediate delta, not a guaranteed whole-model change in accuracy.

## Prerequisites

- [[neural-network]]
- [[matrix-multiplication]]
- [[transformer-attention]]
- [[residual-connection]]

## Sources

- [Vaswani et al., Attention Is All You Need](https://arxiv.org/abs/1706.03762): original position-wise FFN equation and encoder/decoder placement.
