---
id: pareto-candidate-selection
title: "Pareto Candidate Selection"
summary: "Pareto candidate selection retains candidates not dominated across declared objectives while keeping frontier membership separate from a deployable final choice."
type: concept
tags: [math/optimization]
prereqs: [measurement, evaluation-slices]
sources: [https://arxiv.org/abs/2507.19457, https://arxiv.org/html/2507.19457v2]
status: explained
created: 2026-11-10
updated: 2026-11-10
---

# Pareto Candidate Selection

## Meaning

When several task scores or costs matter, the best average can discard a useful specialist. A Pareto frontier retains candidates for which no other evaluated candidate is at least as good on every declared objective and strictly better on at least one. Membership says “not dominated here,” not “best for production.”

## Mechanism

Define an objective vector for each candidate and which direction is preferable. Compare candidates on the same tasks using [[measurement]]. Remove dominated candidates, resolve exact ties with a documented policy, and select parents or finalists from the remaining archive. [[evaluation-slices]] explains how task families can supply separate objectives without hiding a regression in the average. Higher-is-better scores and lower-is-better costs must not be compared with the same inequality.

GEPA uses a task-wise candidate pool and Pareto-inspired sampling to preserve complementary strengths. Its particular selection rule is not identical to every formal multiobjective optimizer: an implementation may sample candidates that are best on individual examples, rather than uniformly sampling the complete mathematical frontier. Inspect the actual selection policy. Winning one subset alone neither defines general Pareto optimality nor guarantees generalization.

## One example

All invented scores are to be maximized. A scores (9, 4), B (7, 7), C (6, 3), and D (8, 8) on two fixed task families. A dominates C, since 9>6 and 4>3. D dominates B, since 8>7 in both coordinates. Neither A nor D dominates the other: A wins the first family and D the second. Retain A and D. D has the higher unweighted mean, 8 versus 6.5, but A remains a possible search parent. If latency becomes a third objective, recompute membership rather than keeping the old verdict automatically.

## Check your understanding

Must a frontier remain small? No. With many objectives, noisy measurements or conflicting tasks, most candidates may be nondominated. Bound archive size, reevaluate borderline differences and record any approximation used to prune it. A final product still needs priorities or constraints to choose among trade-offs; frontier membership does not replace that decision.

## Prerequisites

- [[measurement]]
- [[evaluation-slices]]

## Sources

- <https://arxiv.org/abs/2507.19457>
- <https://arxiv.org/html/2507.19457v2>
