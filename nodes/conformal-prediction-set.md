---
id: conformal-prediction-set
title: Conformal Prediction Set
summary: A split-conformal prediction set uses calibration residuals from exchangeable data to choose a threshold with finite-sample marginal coverage, not a per-person probability guarantee.
type: concept
tags: [ml/evaluation]
prereqs: [quantile, model-calibration, hypothesis-testing]
sources: [https://arxiv.org/abs/2107.07511]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Conformal Prediction Set

## Summary

A **conformal prediction set** wraps a fixed predictive model with an uncertainty set. In split conformal prediction, a held-out calibration set determines how large that set must be to achieve a chosen *marginal* coverage target under exchangeability. A 90% coverage target describes repeated future examples from the same data-generating process; it does not mean that one patient's diagnosis has a 90% conditional probability of being inside the returned set.

## Grounded explanation

Train the base model without using the calibration examples. Define a nonconformity score that is small when the true outcome fits well. Score the calibration examples, sort those scores, and choose the finite-sample adjusted upper [[quantile]] for error level $\alpha$. For a new input, include candidate outcomes whose scores do not exceed that threshold. Exchangeability gives a rank argument: the new true-outcome score is no more likely than a calibration score to rank beyond the threshold. This is the source of the marginal coverage statement, independent of the model's accuracy.

For classification, the output may be a set of plausible labels. A weak classifier can still achieve coverage by returning large, unhelpful sets. Measure both empirical coverage and set size on held-out data; stratify by clinically relevant groups because marginal coverage can hide poor subgroup or individual conditional coverage. [[model-calibration]] of numeric probabilities is a different question: a conformal set can cover at its target rate without turning the model score into an individualized disease probability.

The guarantee needs the data and procedure assumptions. Distribution shift, leakage from calibration into training, adaptive reuse of the calibration set, or time-dependent samples can break a naive split-conformal claim. Record the split and score definition, audit exchangeability plausibility, and test coverage on later and shifted cohorts. For consequential decisions, report limitations and use domain-specific evaluation, not a single set as a substitute for diagnosis.

## Prerequisites

- [[quantile]]
- [[model-calibration]]
- [[hypothesis-testing]]

## Sources

- [Angelopoulos and Bates, A Gentle Introduction to Conformal Prediction](https://arxiv.org/abs/2107.07511): finite-sample coverage, applications, and assumptions.
