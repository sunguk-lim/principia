---
id: concept-drift
title: Concept Drift
summary: Concept drift is a change over time in the conditional relationship that maps inputs to the target a deployed model is meant to predict.
type: concept
tags: [ml/deep-learning]
prereqs: [conditional-probability, probability-distribution]
sources: [arxiv:2004.05785]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Concept Drift

## Summary

**Concept drift** occurs when the predictive relationship changes over time—formally, when the [[conditional-probability]] of the target given the input is no longer the one learned from historical data.

## Grounded explanation

Let $X$ be an input, $Y$ the target, and $t$ time. The learned concept is the conditional relationship $P_t(Y\mid X)$. Concept drift means

$$P_{t_1}(Y\mid X)\ne P_{t_2}(Y\mid X)$$

for relevant times $t_1$ and $t_2$. This is distinct from a change only in $P_t(X)$, the input [[probability-distribution]]. Input drift can alter what cases arrive without changing the correct label for a given case; concept drift changes that correct relationship itself. Both can hurt a fixed model, but they require different diagnoses.

### Worked example

A fraud model learned that transactions from feature group $X=a$ were fraudulent 10% of the time. After criminals change tactics, 30 of the next 100 labeled transactions in the same group are fraud. The observed relationship moved from about $P(Y=1\mid X=a)=0.10$ to $0.30$. A model that still emits 0.10 is stale even if the total volume and feature histogram are unchanged.

Drift may be abrupt, gradual, recurring, or confined to one region of the input space. Detection therefore needs time-aware windows and delayed labels when available. A rising error rate is evidence of degraded predictions, not by itself proof of concept drift: label noise, instrumentation changes, or a changed input mix can produce similar symptoms.

The operational loop has three separate jobs: detect that behavior changed, understand which relationship changed and when, then adapt by retraining, reweighting, or selecting a model suited to the new regime. Validation must replay data in time order; random shuffling can leak later regimes into training and hide the failure.

## Prerequisites

- [[conditional-probability]]
- [[probability-distribution]]

## Sources

- Lu et al., “Learning under Concept Drift: A Review,” arXiv:2004.05785 — definition and detect/understand/adapt framework.
