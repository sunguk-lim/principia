---
id: adafactor
title: Adafactor
summary: Adafactor approximates matrix squared-gradient statistics using row and column summaries to reduce optimizer-state storage.
type: concept
tags: [ml/deep-learning]
prereqs: [adam, matrix-multiplication]
sources: [https://arxiv.org/html/1804.04235]
status: explained
created: 2026-11-04
updated: 2026-11-04
---

# Adafactor

## Meaning

Adafactor exploits matrix structure to reduce the storage of [[adam]]-like squared-gradient statistics. Rather than keep one second-moment number per matrix element, it stores row and column summaries and reconstructs a factored approximation. This is a memory–approximation trade-off, not the same update with universally identical results.

## Mechanism

For an n-by-m parameter matrix, let V be the nonnegative matrix of smoothed squared gradients. Define r_i as its row mean, c_j as its column mean and mu as its overall mean. When mu is positive, the approximation is Vhat_ij=r_i*c_j/mu. This reconstruction has the original row and column means but cannot represent every interaction. [[matrix-multiplication]] supplies the matrix structure; r times c is an outer product, not a dense learned matrix of independent states.

The optimizer divides gradients by a stabilized root of the reconstruction. The original method also uses update clipping, a time-varying square-average decay and relative parameter-scale learning rates. Optional first-moment state and treatment of vector parameters alter total storage. Factoring the second moment alone does not specify all Adafactor variants.

## One example

Take V=[[1,9],[9,1]]. Its row means and column means are both [5,5], and mu=5. Every reconstructed entry is 5*5/5=5. The memory summary preserved marginal means but lost the alternating pattern: neither the original 1s nor the 9s are recovered. A 2-by-2 example does not save storage, but a 1000-by-2000 matrix replaces two million second-moment values with roughly 3000 summaries.

## Check your understanding

Does reducing state to row-plus-column size make the full training memory linear in row count? No. Weights, gradients, activations, temporary reconstruction and optional momentum remain. Check zero-scale handling, clipping, factored dimensions and checkpoint compatibility. Compare quality, peak memory and time-to-quality with a tuned baseline; fitting a larger batch may matter more than saving optimizer arithmetic.

## Prerequisites

- [[adam]]
- [[matrix-multiplication]]

## Sources

- <https://arxiv.org/html/1804.04235>
