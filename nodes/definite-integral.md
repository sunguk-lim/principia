---
id: definite-integral
title: Definite Integral
summary: A definite integral is the limit of sums of function values times interval widths, representing signed accumulation over an interval.
type: concept
tags: [math/calculus]
prereqs: [arithmetic]
sources: [https://openstax.org/books/calculus-volume-1/pages/5-2-the-definite-integral]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Definite Integral

## Summary

The **definite integral** $\int_a^b f(x)\,dx$ is the limit of finite sums that accumulate a quantity $f(x)$ across the interval from $a$ to $b$.

## Grounded explanation

Split $[a,b]$ into subintervals of widths $\Delta x_i$, choose a point $x_i^*$ in each, and form the [[arithmetic]] sum

$$S_n=\sum_{i=1}^n f(x_i^*)\Delta x_i.$$

If these sums approach one value as the largest width shrinks to zero, that value is the definite integral. Positive function values add area above the axis; negative values subtract area below it.

### Worked example

For $f(x)=x$ on $[0,2]$, use two equal intervals of width 1 and right endpoints 1 and 2. The sum is $1\cdot1+2\cdot1=3$. With four intervals of width $0.5$, the right-endpoint sum is

$$0.5(0.5+1+1.5+2)=2.5.$$

Refining further approaches 2, the exact integral $\int_0^2x\,dx=2$. The finite sums matter because later integrals with random increments are also defined first on stepwise approximations and then by a limit.

## Prerequisites

- [[arithmetic]]

## Sources

- OpenStax, *Calculus Volume 1*, “The Definite Integral.”
