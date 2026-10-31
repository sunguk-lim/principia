---
id: paired-benchmark-uncertainty
title: Paired Benchmark Uncertainty
summary: Paired benchmark uncertainty estimates model differences from matched per-item outcomes while preserving dependencies and declared prompt variation.
type: concept
tags: [ml/evaluation]
prereqs: [hypothesis-testing, variance, measurement]
sources: [https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Paired Benchmark Uncertainty

## Meaning

When two models answer the same benchmark items, their results are paired. Uncertainty about their difference depends on which items changed, not just each model's separate accuracy and sample size. An error bar for one score is not automatically an error bar for the difference.

## Mechanism

For item i, let a_i and b_i be zero/one correctness indicators for models A and B. Define d_i=b_i-a_i, which is -1, 0 or 1. The mean of d_i is the accuracy change. Its [[variance]] depends on joint outcomes: shared successes and failures contribute zero, while disagreements determine the change's variability. [[hypothesis-testing]] requires a sampling and dependence model appropriate to the claim.

A paired bootstrap draws item indices with replacement and uses the same sampled indices for both systems. Independent resampling destroys that pairing. If questions share documents or templates, resample suitable groups rather than pretending all questions are independent. [[measurement]] should also distinguish item sampling from prompt-template and example-selection variation.

## Worked example

On 100 items, A gets 60 correct and B gets 62. Suppose ten move from wrong to right and eight from right to wrong. The net change is (10-8)/100=0.02, or two percentage points. Eighteen items disagree. Another pair with three gains and one loss has the same aggregate change but only four disagreements, so its paired uncertainty differs.

For one standalone score near 60% on 500 independent binary items, a plug-in standard error is sqrt(0.6×0.4/500), approximately 0.0219. This is about 2.2 percentage points for that single score under those assumptions, not the paired change's standard error and not a bound on prompt sensitivity.

## Validation and boundaries

Predeclare metrics, comparisons and prompt policy. Store per-item outcomes and group identifiers, use paired intervals or tests, and disclose multiple comparisons and selected slices. Repeat prompt conditions separately rather than silently combining them into independent examples. A narrow interval on one contaminated or unrepresentative dataset does not establish deployment generalization. Report effect size and uncertainty together; lack of a detectable change is not proof of equal capabilities.

## Prerequisites

- [[hypothesis-testing]]
- [[variance]]
- [[measurement]]

## Sources

- <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html>
