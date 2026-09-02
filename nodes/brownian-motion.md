---
id: brownian-motion
title: Brownian Motion
summary: Brownian motion is a continuous-path stochastic process whose disjoint increments are independent and whose increment over duration Δt is normal with variance Δt.
type: concept
tags: [math/probability]
prereqs: [stochastic-process, normal-distribution]
sources: [https://www.randomservices.org/random/brown/Standard.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Brownian Motion

## Summary

**Brownian motion** $W_t$ is a continuous-path [[stochastic-process]] starting at zero, with independent increments and $W_{t+h}-W_t$ distributed normally with mean $0$ and variance $h$.

## Grounded explanation

The defining properties are $W_0=0$, continuous paths, independent increments over disjoint intervals, and

$$W_{t+h}-W_t\sim N(0,h),$$

where $N(0,h)$ is a [[normal-distribution]] with standard deviation $\sqrt h$. The square-root scaling makes fluctuations shrink more slowly than elapsed time, so Brownian paths are continuous but not smooth enough to possess an ordinary derivative.

### Worked example

Over a step $h=0.25$, an increment has standard deviation $\sqrt{0.25}=0.5$. If standardized normal draws for three steps are $0.6,-1.0,0.2$, the increments are $0.3,-0.5,0.1$ and the path values are $W_0=0$, $W_{0.25}=0.3$, $W_{0.5}=-0.2$, $W_{0.75}=-0.1$. Each step's scale follows its duration, and the draws are independent.

Brownian motion is the canonical continuous source of random disturbance used in stochastic differential equations.

## Prerequisites

- [[stochastic-process]]
- [[normal-distribution]]

## Sources

- Random Services, “Standard Brownian Motion.”
