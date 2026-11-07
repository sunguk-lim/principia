---
id: balanced-expert-assignment
title: "Balanced Token-Expert Assignment"
summary: "Balanced token-expert assignment jointly chooses routes to maximize declared affinities under per-token and expert-load constraints."
type: concept
tags: [ml/llm/architecture]
prereqs: [mixture-of-experts, arithmetic]
sources: [https://arxiv.org/html/2103.16716v1]
status: explained
created: 2026-11-08
updated: 2026-11-08
---

# Balanced Token-Expert Assignment

## Meaning

Independent token decisions can overload one expert even when enough total expert capacity exists. Balanced assignment coordinates choices across a token group. It sacrifices some local preferences when necessary to satisfy global load constraints.

## Mechanism

For the experts in [[mixture-of-experts]], let s(t,e) be the affinity of token t for expert e. Let a(t,e) be zero or one, indicating an assignment. In a simple one-expert-per-token formulation, require each token's assignments to sum to one and each expert's assignments to equal its quota. Choose feasible assignments maximizing the sum of a(t,e)*s(t,e). Ordinary [[arithmetic]] compares the scores of alternative feasible allocations. Feasibility requires matching total quotas to token count; a larger top-k or unequal capacities needs its own constraints.

BASE Layers is a primary example that formulates balanced assignment during training. The optimization's score objective is not itself model accuracy, and solving it costs time. BASE's section 3.2.2 uses greedy best-expert selection at test time because the balanced assignment can leak future-token information. Its training matcher is not a production decoder's per-step contract.

## One example

Tokens A and B each need one expert. Experts X and Y each have quota one. Affinities are A:(10,9), B:(9,1). Independent first choice overloads X with two tokens. Assigning A to X and B to Y scores 10+1=11. Assigning A to Y and B to X scores 9+9=18, so the latter is the optimal balanced allocation. A gives up its first choice because its loss is one point, while forcing B to Y loses eight. Equal token counts arise from constraints, not from hoping independently greedy choices average out.

## Check your understanding

Does maximum total affinity prove minimum runtime? No. Expert shape, placement and data movement still affect elapsed time. Measure matching overhead, feasibility, score loss relative to unconstrained choices, quality, dispatch and slowest-expert time. Tiny causal decode groups may offer too little flexibility to balance; using future tokens would violate autoregressive semantics. Compare with simpler capacity handling and learned balancing under the same grouping and work budget.

## Prerequisites

- [[mixture-of-experts]]
- [[arithmetic]]

## Sources

- <https://arxiv.org/html/2103.16716v1>
