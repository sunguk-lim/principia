---
id: stochastic-differential-equation
title: Stochastic Differential Equation
summary: A stochastic differential equation defines continuous-time dynamics with a deterministic drift term and a Brownian-noise diffusion term interpreted through an Itô integral.
type: concept
tags: [math/probability]
prereqs: [differential-equation, ito-integral, brownian-motion]
sources: [https://diffusion.csail.mit.edu/]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Stochastic Differential Equation

## Summary

A **stochastic differential equation (SDE)** augments a [[differential-equation]] with random forcing, usually written as a drift term times $dt$ plus a diffusion term times a [[brownian-motion]] increment.

## Grounded explanation

An Itô SDE has the form

$$dX_t=a(X_t,t)\,dt+b(X_t,t)\,dW_t.$$

Here $X_t$ is the unknown process, $a$ is deterministic drift per unit time, $b$ scales the noise, and $W_t$ is [[brownian-motion]]. The precise meaning is the integral equation

$$X_t=X_0+\int_0^t a(X_s,s)\,ds+\int_0^t b(X_s,s)\,dW_s,$$

where the second term is an [[ito-integral]]. This interpretation is necessary because Brownian motion has no ordinary derivative.

### Worked example

Use $dX_t=-0.5X_t\,dt+0.2\,dW_t$, initial value $X_0=1$, and step $\Delta t=0.25$. Euler–Maruyama approximates

$$X_1=X_0-0.5X_0\Delta t+0.2\sqrt{\Delta t}\,Z,$$

where $Z$ is a standard normal draw. For $Z=0.4$,

$$X_1=1-0.5(1)(0.25)+0.2(0.5)(0.4)=0.915.$$

The drift pulls the state toward zero by $0.125$; this realized noise pushes it upward by $0.04$. Repeating with new independent draws produces different paths governed by the same law.

An SDE specifies a distribution over paths, not one deterministic trajectory. Validation checks both discretization error and distributional quantities such as means, variances, or known transition laws.

## Prerequisites

- [[differential-equation]]
- [[ito-integral]]
- [[brownian-motion]]

## Sources

- MIT IAP 2025, “Generative AI with Stochastic Differential Equations.”
- Gregory F. Lawler, *Stochastic Calculus: An Introduction with Applications*.
