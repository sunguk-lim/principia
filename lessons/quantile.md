# Quantile

## Meaning

A **quantile** at level $q$ is a threshold such that approximately a fraction $q$ of observations lie at or below it. The median is the 0.5 quantile. Unlike a mean, a quantile describes a position in an ordered distribution rather than an average magnitude.

## Mechanism

For a population with [[cumulative-distribution-function]] $F$, one common definition is the smallest $x$ with $F(x) \ge q$. Discrete distributions and flat portions can make multiple thresholds plausible, so the convention matters. For a finite sample, sort observations and select or interpolate an order statistic; different software packages use different interpolation rules. State the rule when exact thresholds affect an operational decision.

For example, delivery times of 10, 12, 15, 18, and 40 minutes have median 15. A high quantile is much more sensitive to the long tail than the median, but no single quantile describes the whole distribution. Estimate its uncertainty from enough representative observations, especially near the tail. Under distribution shift, a historical 90th percentile need not cover 90% of future cases.

## One example

For five sorted delivery times, the median is the middle observation. A higher quantile targets a threshold farther into the slow tail.

## Check your understanding

**Question:** What must be specified to reproduce an empirical quantile exactly?

**Answer:** The quantile level and finite-sample selection or interpolation convention.
