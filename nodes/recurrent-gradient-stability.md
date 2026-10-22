---
id: recurrent-gradient-stability
title: Recurrent Gradient Stability
summary: Recurrent gradient stability concerns how products of transition derivatives shrink or amplify learning signals across time.
type: concept
tags: [ml/deep-learning]
prereqs: [backpropagation-through-time, jacobian]
sources: [https://arxiv.org/html/1211.5063v2]
status: explained
created: 2026-10-23
updated: 2026-10-23
---

# Recurrent Gradient Stability

## Meaning

An earlier recurrent state influences a later loss through many intervening transitions. Even when each local derivative is finite, multiplying many factors can make the resulting signal extremely small or extremely large. These are the vanishing and exploding gradient problems, not a proof that every recurrent model has the same effective memory.

## Mechanism

In [[backpropagation-through-time]], let h_t be the hidden state and J_t=∂h_t/∂h_(t-1) its transition [[jacobian]]. Sensitivity from state h_k to h_T is J_T J_(T-1)…J_(k+1), in that order. For a tanh transition, J_t combines the recurrent weight matrix with activation derivatives; saturation can make some factors small. Products depend on direction as well as magnitude: one scalar threshold on a weight matrix does not fully characterize every nonlinear trajectory.

The mechanism concerns learning credit across a time interval. It does not state that the forward state must become zero, that all distant facts are unrecoverable, or that attention eliminates every optimization difficulty. Recurrent gates and initializations change transition derivatives. Clipping large gradients can bound an update but cannot reconstruct a signal already attenuated near zero. Cutting derivative paths by truncation also changes the training objective's credit assignment.

## Worked example

Take an illustrative scalar path of ten transitions with local derivative 0.5 at every step. Its final-to-initial sensitivity is 0.5¹⁰=1/1024≈0.000977. Another path with local derivative 1.5 has sensitivity 1.5¹⁰≈57.665. A final loss sensitivity of 2 therefore contributes about 0.001953 versus 115.33 to the early state. These are local derivative examples, not universal RNN measurements.

Norm clipping with threshold c rescales a gradient g to g×min(1,c/||g||), preserving its direction when the norm is finite and nonzero. For scalar g=115.33 and c=5 the clipped value is 5; a scalar g=0.001953 stays small. Log gradient norms by temporal distance, inspect activation saturation, check finite gradients, and compare training and long-range task quality at matched settings. A short toy check should establish correct derivative propagation before attributing failed learning to sequence length alone.

## Check your understanding

**Question:** Does clipping exploding gradients solve vanishing gradients? **Answer:** No; limiting a large norm does not restore a small missing learning signal.

## Prerequisites

- [[backpropagation-through-time]]
- [[jacobian]]

## Sources

- <https://arxiv.org/html/1211.5063v2>
