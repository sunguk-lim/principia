---
id: recurrent-gradient-stability
title: Recurrent Gradient Stability
summary: Recurrent gradient stability concerns how products of transition derivatives shrink or amplify learning signals across time.
type: concept
tags: [ml/deep-learning]
prereqs: [backpropagation-through-time, jacobian]
sources: [https://arxiv.org/html/1211.5063v2, https://arxiv.org/abs/1504.00941]
status: explained
created: 2026-10-23
updated: 2026-10-24
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

## Rectification and finite-horizon amplification

For a rectified transition $h_t=\max(0,Wh_{t-1}+u_t)$, let $D_t$ be the diagonal matrix with one on positive preactivations and zero on negative ones. Away from zero, $J_t=D_tW$. Replacing tanh with ReLU changes $D_t$ but does not remove $W$ or make the changing masks commute with it. An inactive coordinate cuts that local derivative route; other coordinates can still carry sensitivity. Positive states are unbounded, so forward growth must be checked separately from gradient norms.

A single eigenvalue threshold cannot classify every finite nonlinear trajectory. Even for an unmasked linear transition, take $W=\begin{pmatrix}0.5&4\\0&0.5\end{pmatrix}$ and initial perturbation $v=(0,1)$. Both eigenvalues are $0.5$, yet $Wv=(4,0.5)$ has length $\sqrt{16.25}\approx4.03$ versus initial length one. The next perturbation is $W^2v=(4,0.25)$, still large. The off-diagonal coupling creates temporary growth even though powers eventually decay. The eigenvalues here are the roots of $(0.5-\lambda)^2=0$, while length is the square root of the sum of squared coordinates. No general spectral theorem is needed to verify the counterexample by direct multiplication.

In a nonlinear recurrence, inspect actual ordered derivative products or their action on test directions, not only eigenvalues of the bare weight matrix. ReLU's active derivative is one, but an identity initialization can lose that property after learning or when inputs change the activation masks. Compare initialization, gates and residual updates using matched long-horizon tasks. None makes clipping a cure for vanished information or makes all recurrent gradients inevitably explode.

## Prerequisites

- [[backpropagation-through-time]]
- [[jacobian]]

## Sources

- <https://arxiv.org/html/1211.5063v2>

- <https://arxiv.org/abs/1504.00941>
