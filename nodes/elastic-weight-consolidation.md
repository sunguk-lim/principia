---
id: elastic-weight-consolidation
title: Elastic Weight Consolidation
summary: Elastic weight consolidation slows changes to parameters estimated important for earlier tasks by adding a Fisher-weighted quadratic penalty during sequential learning.
type: concept
tags: [ml/training]
prereqs: [neural-network, regularization, likelihood, maximum-likelihood-estimation]
sources: [https://arxiv.org/abs/1612.00796]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Elastic Weight Consolidation

## Summary

**Elastic weight consolidation** (EWC) is a continual-learning form of [[regularization]]. After learning an old task, it penalizes movement away from the old parameters in directions estimated important to that task.

## Grounded explanation

Let $\theta^*$ be parameters after an old task, $F_i$ a diagonal importance estimate for parameter $i$, and $L_{new}$ the new-task loss. EWC optimizes

$$L(\theta)=L_{new}(\theta)+\frac{\lambda}{2}\sum_i F_i(\theta_i-\theta_i^*)^2.$$

The original method estimates $F_i$ from the diagonal Fisher information under the old task. The Fisher estimate is built from score gradients of the [[likelihood]], connecting parameter sensitivity to [[maximum-likelihood-estimation]]: parameters whose training-objective gradients carry more information receive a larger penalty.

In a [[neural-network]], large $F_i$ makes parameter $i$ stable while small $F_i$ leaves it plastic. The coefficient $\lambda$ controls the global stability–plasticity trade-off. If it is too small, old-task quality can collapse; if it is too large, learning the new task can stall.

EWC is an approximation. A diagonal importance matrix ignores interactions between parameters, and an estimate from limited old-task data may protect the wrong directions. Strongly conflicting tasks may require changes precisely where the old task is sensitive. Multiple tasks also require a policy for combining or decaying prior penalties.

Evaluate old and new tasks together across a $\lambda$ sweep and several task orders. Compare against no protection, replay, distillation, parameter isolation, and equivalent compute or storage budgets. Inspect per-layer update norms and report both retained performance and adaptation, rather than calling unchanged old accuracy a success by itself.

## Prerequisites

- [[neural-network]]
- [[regularization]]
- [[likelihood]]
- [[maximum-likelihood-estimation]]

## Sources

- [Kirkpatrick et al., “Overcoming Catastrophic Forgetting in Neural Networks”](https://arxiv.org/abs/1612.00796): selectively slow learning on weights important to previous tasks using a Fisher-weighted quadratic constraint.
