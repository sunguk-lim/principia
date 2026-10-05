---
id: quantile
title: Quantile
summary: A quantile is a threshold at which a specified fraction of a distribution lies at or below the threshold, with finite-sample conventions needed for empirical data.
type: concept
tags: [math/statistics]
prereqs: [cumulative-distribution-function]
sources: [https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Quantile

## Summary

A **quantile** at level $q$ is a threshold such that approximately a fraction $q$ of observations lie at or below it. The median is the 0.5 quantile. Unlike a mean, a quantile describes a position in an ordered distribution rather than an average magnitude.

## Grounded explanation

For a population with [[cumulative-distribution-function]] $F$, one common definition is the smallest $x$ with $F(x) \ge q$. Discrete distributions and flat portions can make multiple thresholds plausible, so the convention matters. For a finite sample, sort observations and select or interpolate an order statistic; different software packages use different interpolation rules. State the rule when exact thresholds affect an operational decision.

For example, delivery times of 10, 12, 15, 18, and 40 minutes have median 15. A high quantile is much more sensitive to the long tail than the median, but no single quantile describes the whole distribution. Estimate its uncertainty from enough representative observations, especially near the tail. Under distribution shift, a historical 90th percentile need not cover 90% of future cases.

A quantile is a descriptive threshold; it is not a calibrated probability for a particular individual. In conformal calibration, an adjusted empirical quantile of nonconformity scores becomes a threshold for prediction sets. The finite-sample index and exchangeability assumption carry the coverage claim, not the word “quantile” alone.

## Prerequisites

- [[cumulative-distribution-function]]

## Sources

- [NIST percentile and quantile guidance](https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm): empirical percentiles and conventions.
