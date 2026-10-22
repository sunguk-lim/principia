---
id: chain-rule
title: Chain Rule
summary: The chain rule differentiates a composition by multiplying each local derivative evaluated at its own intermediate input.
type: concept
tags: [math/calculus]
prereqs: [derivative]
sources: [https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule]
status: explained
created: 2026-10-23
updated: 2026-10-23
---

# Chain Rule

## Meaning

The chain rule explains how a small input change propagates through successive functions. It is not a rule for multiplying the functions themselves. Every local sensitivity is evaluated where that stage actually receives its input.

## Mechanism

Let u=g(x) and y=f(u), with both functions differentiable at the relevant values. A [[derivative]] measures the first-order change in output per input change. A small change Δx produces approximately g′(x)Δx at u; that intermediate change produces approximately f′(u)g′(x)Δx at y. Therefore

$$\frac{dy}{dx}=f'(g(x))g'(x).$$

The approximation errors shrink faster than the corresponding small change under differentiability, which is why multiplying the first-order factors gives the limiting derivative. Evaluate the outer derivative at g(x), not at g′(x). Longer compositions multiply further local factors in dependency order. If one input affects an output through several paths, add the path contributions rather than selecting one arbitrarily.

## Worked example

Let g(x)=3x+2 and f(u)=u². At x=2, the intermediate value is u=8. The local derivatives are g′(2)=3 and f′(8)=16, giving dy/dx=16×3=48. Direct expansion gives y=(3x+2)²=9x²+12x+4, whose derivative at 2 is 18×2+12=48 as well. The agreement checks both the local factors and their evaluation points.

The derivative predicts a small-change response, not an exact finite change. For Δx=0.01 the first-order prediction is Δy≈0.48; actual y changes from 64 to 8.03²=64.4809, or 0.4809. The remaining 0.0009 is the second-order term, not evidence that the rule failed. Check analytic derivatives with shrinking finite differences away from nonsmooth boundaries. A derivative undefined at a clipping boundary requires a declared convention rather than this smooth derivation.

## Check your understanding

**Question:** Is f′(g′(x))g′(x) the chain rule? **Answer:** No. The outer derivative receives the intermediate value g(x), not the inner derivative.

## Prerequisites

- [[derivative]]

## Sources

- <https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule>
