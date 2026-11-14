---
id: dataset-distribution-shift
title: "Dataset Distribution Shift"
summary: "Dataset distribution shift is a difference between reference and target data-generating distributions that can change inputs, label frequencies or input-to-target relationships without changing the schema."
type: concept
tags: [ml/data]
prereqs: [probability-distribution, conditional-probability, evaluation-slices]
sources: [https://raw.githubusercontent.com/tensorflow/data-validation/master/docs/get_started.md]
status: explained
created: 2026-11-15
updated: 2026-11-15
---

# Dataset Distribution Shift

## Meaning

Two datasets can contain identical fields and allowed label codes but represent different populations. Distribution shift concerns the probabilities of examples and targets, not just syntactic validity. A shift can occur between data sources, between training and serving, or over time; the last case is not the only one.

## Mechanism

Let X denote inputs and Y the target under a declared task. Let P be a reference [[probability-distribution]] and Q a target distribution. The joint distributions differ when P(X,Y) differs from Q(X,Y). The factorization into P(X) times P(Y given X), using [[conditional-probability]], distinguishes a changed input mix from a changed relationship between inputs and targets. A change in class frequencies is another useful view; special shift assumptions must be checked, not inferred from one histogram.

An unlabeled feature comparison can reveal a changed input distribution but cannot generally establish that the target relationship stayed fixed. Changed labeling instructions or data collection can mimic or contribute to a population difference. Separate instrument errors, annotation semantics and genuine target change before deciding to retrain or reweight.

TensorFlow Data Validation distinguishes schema validation from comparisons of training/serving statistics and comparisons across training days. Such tests identify particular measured differences under configured thresholds. Passing marginal feature checks does not prove equality of the full joint distribution or unchanged task quality.

## One example

A reference population is 80% short requests and 20% long requests. A target population is 40% short and 60% long. Suppose a fixed classifier's error is 5% on short requests and 20% on long ones in both populations. Reference error is .8×.05+.2×.20=.08; target error is .4×.05+.6×.20=.14. The rise from 8% to 14% needs no change in within-group behavior or schema: the mixture changed.

Use [[evaluation-slices]] to report both group errors and group proportions. If a new annotation rule instead changes the correct label for the same long request, reweighting the old groups alone does not repair the semantic mismatch.

## Validation and alternatives

Compare provenance, missingness, feature and label distributions where available, and fixed-model performance on independently labeled target examples. Preserve a stable reference and inspect uncertainty, correlated features and small slices. Consider recollection, policy reconciliation, recalibration, retraining or justified weighting only after diagnosis. A detected shift is neither proof of harm nor proof that one particular remedy is valid.

## Prerequisites

- [[probability-distribution]]
- [[conditional-probability]]
- [[evaluation-slices]]

## Sources

- <https://raw.githubusercontent.com/tensorflow/data-validation/master/docs/get_started.md>
