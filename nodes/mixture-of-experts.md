---
id: mixture-of-experts
title: Mixture-of-Experts (MoE)
summary: A Mixture-of-Experts (MoE) layer replaces the transformer's single feed-forward block with many of them — each a small neural-network FFN with its own weights, called an expert —…
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network, softmax]
sources: []
status: explained
created: 2026-06-20
updated: 2026-06-20
---

# Mixture-of-Experts (MoE)

## Summary

A **Mixture-of-Experts (MoE)** layer replaces the transformer's *single*
feed-forward block with **many** of them — each a small `[[neural-network]]` FFN
with its **own** weights, called an **expert** — plus a **router** that, for every
token, picks only the **top-k** experts to actually run. This **decouples** total
parameters from per-token compute: stack hundreds of experts (huge capacity) while
each token still flows through only $k$ of them (small, fixed compute). The price is
a routing decision and uneven expert load.

![Mixture-of-Experts: a router scores the token, picks the top-k experts (the rest stay idle), and combines their outputs weighted by the gate](mixture-of-experts.svg)

## Grounded explanation

A normal transformer layer sends **every** token through **one** FFN — a
`[[neural-network]]` block. MoE changes that block into a population of $E$ experts
$\{\text{FFN}_1, …, \text{FFN}_E\}$, each with independent weights, gated by a router:

1. **Route (the gate).** A tiny linear layer scores the token's hidden vector $h$
   against the experts and normalizes with [[softmax]]:
   $g = \mathrm{softmax}(W_r\,h) \in \mathbb{R}^{E}$ — a probability over experts.
2. **Select top-k (sparsity).** Keep only the $k$ largest gates (typically $k=1$ or
   $2$); the other $E-k$ experts are **not run** for this token. So compute scales
   with $k$ (constant), while parameters scale with $E$ (grows freely). This is the
   whole point: capacity ≫ compute.
3. **Compute + combine.** Run the token through its selected experts and take the
   gate-weighted sum of their outputs:
   $y = \sum_{i \in \text{top-}k} g_i \, \text{FFN}_i(h).$
   The gate values double as mixing weights, so the router is trained end-to-end.

They are called **experts** because, with this routing, each FFN tends to
**specialize** during training (different experts handle different kinds of tokens) —
the roles emerge, they are not assigned. The main difficulty is **load balance**: the
router can collapse onto a few favourite experts, so an auxiliary balancing loss
nudges traffic to spread evenly.

A dense FFN and one expert are the *same* kind of block — MoE just adds *many* and a
gate. And once you have many experts, you can place them on different GPUs: that is
expert-parallelism, where the routing above becomes two `all-to-all`s.

## Prerequisites

- [[neural-network]]
- [[softmax]]

## Sources

_none_
