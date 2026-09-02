---
id: stochastic-process
title: Stochastic Process
summary: A stochastic process is an indexed family of random variables, so one uncertain experiment produces an entire path through time or space.
type: concept
tags: [math/probability]
prereqs: [random-variable, probability-distribution]
sources: [https://www.randomservices.org/random/processes/Introduction.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Stochastic Process

## Summary

A **stochastic process** is a family $\{X_t:t\in T\}$ of [[random-variable]]s indexed by time or another coordinate; one outcome of the experiment produces a complete path $t\mapsto X_t$.

## Grounded explanation

For each fixed time $t$, $X_t$ has a [[probability-distribution]]. Across times, the variables also have a joint distribution that describes dependence. Knowing every one-time distribution is not enough: two processes can have identical marginals but very different path behavior.

### Worked example

Let independent coin flips be $Z_1,Z_2,\ldots$, with $Z_i=+1$ for heads and $-1$ for tails. Define $X_0=0$ and $X_t=\sum_{i=1}^t Z_i$. For flips heads, tails, heads, one path is $0,1,0,1$. At time 2, possible values are $-2,0,2$, but the process also records how the path reached them.

An index set may be discrete, as in this random walk, or continuous, as in Brownian motion. The process concept coordinates uncertainty across indices; a single random variable describes only one indexed slice.

## Prerequisites

- [[random-variable]]
- [[probability-distribution]]

## Sources

- Random Services, “Introduction to Stochastic Processes.”
