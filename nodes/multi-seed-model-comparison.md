---
id: multi-seed-model-comparison
title: "Multi-Seed Model Comparison"
summary: "Multi-seed model comparison estimates how a training intervention changes outcomes across prespecified random conditions rather than reporting the luckiest run."
type: concept
tags: [ml/evaluation]
prereqs: [paired-benchmark-uncertainty]
sources: [https://scikit-learn.org/stable/common_pitfalls.html]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# Multi-Seed Model Comparison

## Meaning

Random initialization, data order and stochastic training can change a trained model's result. A multi-seed comparison repeats the intervention under a declared set of random conditions. It estimates sensitivity to those conditions, not every source of uncertainty about future data or software versions.

## Mechanism

Specify candidate configurations, seeds, dataset splits and compute budgets before selection. Where meaningful, match random conditions across candidates and analyze the differences, following [[paired-benchmark-uncertainty]]. Equal seed integers alone do not prove equivalent randomness: changed code can consume random draws differently. Keep realized splits and relevant configuration in the experiment record.

[[variance]] across training repeats is distinct from finite-test-set variation. Repeating seeds against the same leaked test data cannot restore independence, and reusing one unusually favorable seed can hide instability. The scikit-learn randomness guidance distinguishes reproducible estimator/splitter settings from robustness across random initializations; the relevant controls depend on the estimator and evaluation procedure.

## One example

For three invented matched conditions, A scores [70,72,68] and B scores [71,73,69]. Both vary, but every paired difference B-A is +1; their means are 70 and 71. In a second comparison B scores [75,69,69], also averaging 71, but paired differences are [+5,-3,+1]. The same mean improvement now has much greater sensitivity. Three runs illustrate the distinction; they are not a universal sufficient sample size or a basis for declaring a precise significance level.

## Check your understanding

Should only the best B run be compared with A's average? No. That changes the selection procedure and inflates the apparent benefit. Report all prespecified runs, paired differences, spread, failed runs and budget. Choose repetition count from expected variability and decision stakes; a fixed recommendation such as three or five seeds is not a statistical guarantee. Keep dataset and deployment uncertainty visible alongside seed sensitivity.

## Prerequisites

- [[paired-benchmark-uncertainty]]

## Sources

- <https://scikit-learn.org/stable/common_pitfalls.html>
