---
id: hierarchical-mixture-of-experts-gating
title: Hierarchical Mixture-of-Experts Gating
summary: Hierarchical mixture-of-experts gating selects groups before selecting experts within them, factorizing routing cost while restricting which global expert combinations can be reached.
type: concept
tags: [ml/deep-learning]
prereqs: [mixture-of-experts]
sources: [https://arxiv.org/html/1701.06538v1]
status: explained
created: 2026-10-28
updated: 2026-10-28
---

# Hierarchical Mixture-of-Experts Gating

## Meaning

Hierarchical gating replaces one flat expert-selection decision with a sequence of decisions. A first gate chooses expert groups; gates inside the selected groups choose individual experts. The objective is to reduce a very wide routing decision while retaining conditional expert computation. This is a routing architecture, not a synonym for placing experts on different devices.

## Mechanism

Start from [[mixture-of-experts]]: experts produce candidate transformations and sparse gate weights choose which outputs contribute. In a two-level version, let p(g) be the weight assigned to selected group g and q(e|g) the within-group weight of selected expert e. The final expert weight is p(g)*q(e|g). If each level's selected weights sum to one, the products across selected paths also sum to one.

Only selected group gates need execute at the second level. This can reduce the number of expert scores computed, but the first choice constrains later choices: an excellent expert in an unselected group is unreachable. Sparse selection at two levels does not generally reproduce the global flat top-k. Both levels require appropriate load balancing; an overloaded parent can starve many otherwise capable children.

## Worked example

Take four groups with four experts each. Select two groups, then two experts in each selected group: four final expert paths. Routing scores total 4 at the group level plus 2*4 inside groups, or 12, instead of 16 flat scores. For group weights 0.6 and 0.4, and child weights [0.75,0.25] and [0.5,0.5], final weights are [0.45,0.15,0.20,0.20], summing to one. At a larger hypothetical 64-by-64 hierarchy selecting two groups, scoring requires 64+2*64=192 values rather than 4096. These counts omit projection dimensions, memory traffic and scheduling, so they are not speedup predictions.

## Validation and alternatives

Compare flat and hierarchical routing with matched expert architecture, active path count and quality. Measure routing work, group/expert imbalance, dropped routes and full step latency. Test cases where the flat best experts lie in excluded groups. The Shazeer paper's hierarchy is a primary reference; its conditional computation does not imply constant wall-clock time or automatic geographic/device locality.

## Check your understanding

Are two groups with two selected experts each equivalent to the best four experts globally? No. The parent gate can exclude a group containing globally high-scoring experts.

## Prerequisites

- [[mixture-of-experts]]

## Sources

- <https://arxiv.org/html/1701.06538v1>
