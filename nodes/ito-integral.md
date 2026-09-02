---
id: ito-integral
title: Itô Integral
summary: The Itô integral accumulates a non-anticipating process against Brownian increments, defined by left-endpoint sums and a mean-square limit.
type: concept
tags: [math/probability]
prereqs: [definite-integral, brownian-motion, expectation]
sources: [https://www.math.uchicago.edu/~lawler/finbook.pdf]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Itô Integral

## Summary

The **Itô integral** $\int_0^T H_t\,dW_t$ accumulates a process $H_t$ against increments of [[brownian-motion]], with each coefficient chosen using information available before the corresponding increment.

## Grounded explanation

For times $0=t_0<\cdots<t_n=T$, approximate the integral by

$$\sum_{i=0}^{n-1}H_{t_i}(W_{t_{i+1}}-W_{t_i}).$$

This resembles a [[definite-integral]], but interval width is replaced by a random Brownian increment. The left endpoint prevents $H_{t_i}$ from peeking at the future increment. Refining the partition defines the limit in mean square, measured with [[expectation]].

### Worked example

On $[0,1]$, use two half-intervals. Let $H_t=1$ on the first and $H_t=2$ on the second. If Brownian increments are $0.3$ and $-0.1$, the step integral is

$$1(0.3)+2(-0.1)=0.1.$$

The second coefficient doubles both positive and negative noise; it does not add ordinary area. For constant $H_t=2$, the integral is exactly $2(W_1-W_0)=2W_1$.

Because Brownian increments have variance proportional to time, squared increments survive in limiting calculations. This produces the distinctive Itô correction in change-of-variable formulas.

## Prerequisites

- [[definite-integral]]
- [[brownian-motion]]
- [[expectation]]

## Sources

- Gregory F. Lawler, *Stochastic Calculus: An Introduction with Applications* — adapted processes and Itô integration.
