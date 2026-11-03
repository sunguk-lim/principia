---
id: soap-optimizer
title: SOAP Optimizer
summary: SOAP applies Adam-style coordinate adaptation in the eigenbasis of Shampoo statistics and maps the resulting update back to parameter coordinates.
type: concept
tags: [ml/deep-learning]
prereqs: [adam, shampoo-optimizer]
sources: [https://arxiv.org/html/2409.11321v2, https://github.com/nikhilvyas/SOAP]
status: explained
created: 2026-11-04
updated: 2026-11-04
---

# SOAP Optimizer

## Meaning

SOAP changes the coordinate system in which [[adam]] adapts gradient magnitudes. [[shampoo-optimizer]] supplies structured row and column statistics; their eigenvectors define a rotated basis. Adam-style statistics are then updated in that basis even between expensive basis refreshes.

## Mechanism

Let G be an m-by-n gradient, Q_L the m-by-m orthonormal eigenvector matrix of a row statistic and Q_R the n-by-n counterpart for columns. Convert to Gprime=Q_L transpose*G*Q_R. Maintain directional and squared-gradient statistics in this coordinate system, compute an Adam-style normalized update Dprime, and return D=Q_L*Dprime*Q_R transpose to update the original parameter matrix.

This is not just computing ordinary Adam and rotating its answer afterward: coordinatewise nonlinear scaling does not generally commute with rotation. When the basis changes, previously accumulated state must remain meaningful. A first-moment matrix can be transformed between bases; diagonal second-moment information does not encode all cross-covariances, so its transport is an algorithmic approximation. Follow the reference implementation's state projection and refresh policy, not an invented exact-invariance claim.

## One example

For a two-coordinate illustration, take Q with columns [1,1]/sqrt(2) and [1,-1]/sqrt(2), and g=[3,1]. The rotated gradient is [2*sqrt(2),sqrt(2)]. Suppose the already accumulated rotated first and square states yield normalized direction [1,0.5], with startup corrections already accounted for. Mapping back gives [1.5/sqrt(2),0.5/sqrt(2)], approximately [1.0607,0.3536]. These chosen state values illustrate the mapping, not a full first Adam step or a predicted speedup.

## Check your understanding

Is a rarely refreshed basis free? No. Measure decomposition, statistic construction, state projection, memory and distributed communication as well as ordinary steps. Compare refresh intervals and tuned Adam/Shampoo baselines on held-out quality and total time. The paper's reported gains are specific experiments; they do not establish SOAP as a universally faster replacement.

## Prerequisites

- [[adam]]
- [[shampoo-optimizer]]

## Sources

- <https://arxiv.org/html/2409.11321v2>
- <https://github.com/nikhilvyas/SOAP>
