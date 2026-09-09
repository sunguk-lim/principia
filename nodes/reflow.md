---
id: reflow
title: Reflow
summary: Reflow regenerates endpoint pairings with a learned rectified-flow ODE and refits the velocity field so transport trajectories become easier to integrate with few steps.
type: concept
tags: [ml/deep-learning]
prereqs: [flow-matching, differential-equation, probability-distribution]
sources: [https://arxiv.org/abs/2209.03003, https://arxiv.org/abs/2309.06380]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Reflow

## Summary

**Reflow** is a recursive rectification procedure for [[flow-matching]]. It uses a fitted ordinary [[differential-equation]] to induce a new coupling between source and target samples, then fits another flow to straighter interpolation paths under that coupling.

## Grounded explanation

Start with paired endpoints $(X_0,X_1)$ from a coupling of source and target [[probability-distribution]]s. A rectified flow learns a velocity field along the linear interpolation

$$X_t=(1-t)X_0+tX_1.$$

Although each conditional interpolation is straight, the learned marginal velocity can produce curved trajectories when many pairings overlap. Integrating the learned ODE maps fresh source samples to endpoints; pairing each source with its generated endpoint and refitting is **reflow**. The rectified-flow paper proves non-increasing convex transport costs under its idealized rectification construction and motivates repeated rectification for trajectories that coarse solvers can follow more accurately.

Practical recursion is not exact. Finite samples, model error, optimization error, and numerical integration all affect regenerated pairs. Repeating reflow may improve straightness while degrading endpoint fidelity or coverage. Therefore “one pass is always enough” and “more passes always help” are both empirical claims, not consequences of the construction.

InstaFlow uses reflow to improve noise–image assignment before distilling a text-conditioned model to one step. Its reported quality and latency are tied to particular models, data, metrics, hardware, and training budgets; they do not establish a universal recipe or prove feature-space loss is always preferable to pixel loss.

At every round, measure trajectory curvature, solver residual, source-to-endpoint drift, coverage, sample quality, and wall-clock generation cost. Compare zero, one, and multiple reflows under equal compute; vary solver tolerance and fresh samples; and include one-reflow-plus-distillation and few-step baselines. Stop when marginal integration savings no longer compensate for target-generation and refitting error.

## Prerequisites

- [[flow-matching]]
- [[differential-equation]]
- [[probability-distribution]]

## Sources

- [Liu, Gong, and Liu, “Flow Straight and Fast”](https://arxiv.org/abs/2209.03003): introduces rectified flow, recursive rectification, transport-cost properties, and coarse-step sampling motivation.
- [Liu et al., “InstaFlow”](https://arxiv.org/abs/2309.06380): applies reflow to text-conditioned generation before one-step distillation and reports experiment-specific quality and latency.
