---
id: recurrent-neural-network
title: Recurrent Neural Network
summary: A recurrent neural network reuses a parameterized state transition across sequence positions so each hidden state depends on the preceding state and current input.
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network, work-span-model]
sources: [https://arxiv.org/html/1211.5063v2, https://arxiv.org/html/1706.03762v7]
status: explained
created: 2026-10-23
updated: 2026-10-23
---

# Recurrent Neural Network

## Meaning

A recurrent neural network (RNN) processes a sequence by carrying a hidden state from one position to the next. Its defining property is a shared transition applied repeatedly, not an unlimited memory guarantee. A vanilla RNN places a nonlinearity inside that state update.

## Mechanism

Let x_t be the input vector at step t, h_t a d-dimensional state, W_h a d×d recurrent matrix, W_x a d×p input matrix for p-dimensional inputs, and b a d-vector bias. A [[neural-network]] transition is

$$h_t=\sigma(W_hh_{t-1}+W_xx_t+b),$$

where σ is an elementwise nonlinear function and h_0 is an explicit initial state. The same matrices are used at every step. Reusing parameters does not mean successive h_t values are equal. Because h_t is needed to compute h_(t+1), the ordinary evaluation has T dependent transitions for T positions. The [[work-span-model]] distinguishes this temporal chain from the parallel scalar work within each transition. Dense recurrent products alone take O(Td²) work; the shorthand O(T) holds width fixed.

## Worked example

Choose a scalar state, h_0=1, W_h=0.5, W_x=2, b=-1 and inputs x_1=2, x_2=-1. Use rectification σ(z)=max(0,z). The first preactivation is 0.5×1+2×2-1=3.5, so h_1=3.5. The second is 0.5×3.5+2×(-1)-1=-1.25, so h_2=0. Both the active and clipped branches matter: replacing the two nonlinear transitions with one unrestricted affine map would not preserve this mechanism in general.

Input projections can be batched ahead of time, separate examples can advance together, and matrix operations can be distributed. None automatically removes the vanilla transition's dependency on the previous nonlinear state. A fixed-width decode state has size independent of sequence length, but training commonly retains intermediate states, and bounded state cannot promise exact recall of every past token. Gated and structured variants require their own analysis; they are not all equivalent to this vanilla update.

## Check your understanding

**Question:** Does increasing batch parallelism remove each example's temporal state dependency? **Answer:** No; it advances independent examples concurrently while preserving the chain within each example.

## Prerequisites

- [[neural-network]]
- [[work-span-model]]

## Sources

- <https://arxiv.org/html/1211.5063v2>
- <https://arxiv.org/html/1706.03762v7>
