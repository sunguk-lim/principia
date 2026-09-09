---
id: temporal-data-leakage
title: Temporal Data Leakage
summary: Temporal data leakage occurs when model development uses information that would not have existed at the simulated prediction time, making historical evaluation optimistically unlike deployment.
type: concept
tags: [ml/evaluation]
prereqs: [dataset-lineage, concept-drift]
sources: [https://scikit-learn.org/stable/common_pitfalls.html#data-leakage, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Temporal Data Leakage

## Summary

**Temporal data leakage** occurs when training, feature construction, model selection, or evaluation sees information that was unavailable at the prediction timestamp being simulated. The resulting score answers a hindsight question rather than the production forecasting question.

## Grounded explanation

Assign each example a prediction time $t_p$. Every input value must have an availability time $t_a$ satisfying $t_a\le t_p$; event time alone is insufficient because an event may arrive or finish aggregation later. Labels may mature after $t_p$, but they cannot be used as features or influence fitted preprocessing for that prediction.

Consider daily fraud prediction. A payment event happens Monday at 09:00, a chargeback label arrives Friday, and a “seven-day chargeback count” is recomputed the following Monday. Joining that final count back to Monday by customer ID leaks outcomes learned after the decision. A random row split can hide the error by placing later records and duplicated entities on both sides.

A chronological split is necessary but not sufficient. Fit scalers, feature selection, imputation, and thresholds only on each training interval. Reconstruct features with point-in-time joins and record their source versions in [[dataset-lineage]]. Add a gap when labels or features have a known delay. Walk-forward evaluation trains on past intervals and tests on the immediately following interval, repeating across several cutoffs.

For example, with months 1–6, one backtest can train on 1–3, leave month 4 as a one-month gap, and test on 5; the next can train on 1–4, gap 5, and test on 6. This prevents the evaluated model from learning directly from its future, while multiple cutoffs reveal time variation. Performance can still change because of [[concept-drift]]; a temporal drop is evidence to investigate, not automatic proof of leakage.

Audit every feature’s event time, availability time, aggregation window, and join condition. Compare random and temporal splits, deduplicate entities or sessions where needed, and verify online/offline feature parity. The invariant is simple: replaying a historical decision may read only artifacts that the real system could have read at that moment.

## Prerequisites

- [[dataset-lineage]]
- [[concept-drift]]

## Sources

- [scikit-learn, “Data leakage”](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage): unavailable-at-prediction information and train-only fitting.
- [scikit-learn `TimeSeriesSplit`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html): ordered folds and configurable gaps.
