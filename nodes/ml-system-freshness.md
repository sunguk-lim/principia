---
id: ml-system-freshness
title: ML System Freshness
summary: ML system freshness measures how old the model, features, candidates, and cached predictions are when a decision is served relative to how quickly the task changes.
type: concept
tags: [ml/evaluation]
prereqs: [concept-drift, measurement]
sources: [https://developers.google.com/machine-learning/guides/rules-of-ml#rule_8_know_the_freshness_requirements_of_your_system]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# ML System Freshness

## Summary

**ML system freshness** is the age of the information embodied in a served decision. Model age is only one component: source events, computed features, candidate sets, indexes, and cached predictions can each be stale on a different clock.

## Grounded explanation

For a served artifact produced at time $t_a$ and used at $t_s$, define age $A=t_s-t_a$. A freshness service-level objective can require, for example, that 99% of recommendation candidate sets have $A\le 6$ hours. This is a [[measurement]] of age, not a claim that six hours is universally acceptable.

End-to-end staleness is governed by the oldest load-bearing stage. Fresh source events do not help when ranking uses yesterday’s cached candidates; hourly predictions do not help when their features update weekly. Instrument event time, processing time, artifact version, and serving time at every boundary.

Choose refresh cadence by measuring quality as artifacts age. If engagement is stable for three days, nightly computation may be adequate. If intent changes within minutes, use a hybrid design: compute stable candidates in batch, update recent-event features or reranking online, and retain bounded fallbacks when the online path fails.

Freshness differs from [[concept-drift]]. Drift changes the relationship the model must learn; stale serving can fail even with unchanged model parameters because a user, item, or inventory state changed after precomputation. Retraining more often cannot repair an old cache downstream, and refreshing predictions cannot repair a model whose learned relationship has drifted.

Monitor age distributions, missed update deadlines, late events, cache age, and task quality by age bucket. Test the cost and failure modes of each faster path: lower age may increase compute, load pressure, partial-update inconsistency, and operational complexity. Set the freshness target from observed quality loss and business consequences rather than from a fashionable batch-versus-streaming label.

## Prerequisites

- [[concept-drift]]
- [[measurement]]

## Sources

- [Google, “Rules of Machine Learning,” Rule 8](https://developers.google.com/machine-learning/guides/rules-of-ml#rule_8_know_the_freshness_requirements_of_your_system): measure how quality degrades with model age and align monitoring with required update cadence; Rule 10 also documents silent failures from stale input tables.
