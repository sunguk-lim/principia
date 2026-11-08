---
id: multi-fidelity-model-selection
title: "Multi-Fidelity Model Selection"
summary: "Multi-fidelity model selection allocates different training resources to candidates while treating early performance as an imperfect predictor of the target-budget objective."
type: concept
tags: [ml/training]
prereqs: [adaptive-validation-overfitting, optimizer-time-to-quality]
sources: [https://arxiv.org/abs/1603.06560]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# Multi-Fidelity Model Selection

## Meaning

A fidelity is the resource level used to assess a candidate: training steps, data amount or another explicitly defined budget. Low-fidelity measurements can screen candidates cheaply. The selection target remains performance at the budget that matters, not whichever configuration looks best after a short run.

## Mechanism

Choose a resource and a promotion rule. Evaluate many candidates cheaply, allocate more to survivors and compare finalists at the target fidelity. Hyperband is a primary example of adaptive resource allocation and early stopping across sampled hyperparameter configurations. It does not guarantee that every short learning curve predicts the same full-budget ranking.

[[optimizer-time-to-quality]] explains why convergence speed and attainable quality are separate objectives. A configuration can win early because its learning schedule spends progress sooner. Preserve the exact comparison objective: fast acceptable training and best final accuracy are different goals. [[adaptive-validation-overfitting]] still applies when the same validation set is queried at many resource levels; resource screening does not supply an independent final estimate.

## One example

At one invented training unit, A has loss .30 and B .40. At four units, A reaches .28 while B reaches .20. Promoting only A after the first unit discards the eventual target-budget winner. Screening both at one unit costs two units and continuing both to four costs six more, for eight total. Promoting only A costs two plus three, or five, but risks a worse final result. The saving and the ranking error must both appear in the comparison.

## Check your understanding

Does this mean early stopping is always wrong? No. It can save substantial work when early scores are informative or the target is time-to-quality. Measure ranking stability, promotion errors and total search cost on representative tasks. Rerun finalists at the actual intended budget and record whether training resumes or restarts. A changed data subset or schedule is a changed fidelity contract, not merely a faster timer.

## Prerequisites

- [[adaptive-validation-overfitting]]
- [[optimizer-time-to-quality]]

## Sources

- <https://arxiv.org/abs/1603.06560>
