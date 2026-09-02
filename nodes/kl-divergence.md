---
id: kl-divergence
title: Kullback–Leibler Divergence
summary: Kullback–Leibler divergence is the expected log density ratio from one probability distribution to another, measuring information lost when the second approximates the first.
type: concept
tags: [math/probability]
prereqs: [probability-distribution, expectation]
sources: [https://statproofbook.github.io/P/kl-nonneg.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Kullback–Leibler Divergence

## Summary

**Kullback–Leibler divergence** $D_{KL}(P\|Q)$ measures how differently two [[probability-distribution]]s weight the same outcomes by taking, under $P$, the [[expectation]] of the log ratio $p/q$.

## Grounded explanation

For discrete outcomes,

$$D_{KL}(P\|Q)=\sum_x p(x)\log\frac{p(x)}{q(x)}.$$

It is nonnegative and equals zero only when the distributions agree wherever $P$ has mass. It is not symmetric, so it is not a geometric distance.

### Worked example

Let $P=(0.5,0.5)$ and $Q=(0.75,0.25)$. Using natural logarithms,

$$D_{KL}(P\|Q)=0.5\log(0.5/0.75)+0.5\log(0.5/0.25)\approx0.144.$$

Reversing the arguments gives about $0.131$, demonstrating asymmetry. If $Q$ assigns zero probability to an outcome that $P$ considers possible, the divergence is infinite because $Q$ cannot represent that event.

In variational inference, minimizing $D_{KL}(q\|p)$ makes a tractable approximation $q$ resemble a target posterior $p$ under this particular asymmetric penalty.

## Prerequisites

- [[probability-distribution]]
- [[expectation]]

## Sources

- The Book of Statistical Proofs, “Non-negativity of the Kullback–Leibler divergence.”
