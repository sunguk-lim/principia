---
id: quantile-quantile-plot
title: Quantile-Quantile Plot
summary: A quantile-quantile (Q-Q) plot compares two distributions by plotting values at equal cumulative probabilities, so a straight pattern signals similarly shaped distributions while systematic bends, shifts, or tail departures expose how they differ.
type: concept
tags: [math/probability]
prereqs: [cumulative-distribution-function]
sources: [https://www.itl.nist.gov/div898/handbook/eda/section3/qqplot.htm]
status: explained
created: 2026-09-12
updated: 2026-09-12
---

# Quantile-Quantile Plot

## Summary

A **quantile-quantile plot** (Q-Q plot) compares two distributions without reducing either to one number. At each cumulative probability level, it takes one value from each distribution and plots the pair. If corresponding quantiles change together by a constant linear rule, the plotted points form an approximately straight line. A shift, change in spread, curvature, or a difference confined to the tails therefore becomes a visible departure from that line.

## Grounded explanation

### Matching equal fractions

The [[cumulative-distribution-function]] (CDF) maps a value to the fraction of observations at or below it. Reading that map backward gives a **quantile**: for a chosen fraction $q$ between 0 and 1, it is the value below which approximately fraction $q$ of observations lie.

A Q-Q plot compares two samples, $A$ and $B$, at the *same* fractions. Choose levels such as $q=0.1, 0.2, \ldots, 0.9$. For each level, find $x_q$, the $q$-quantile of $A$, and $y_q$, the $q$-quantile of $B$, then plot the point $(x_q, y_q)$. The axes contain data values, not probabilities; the shared probability level is what pairs the coordinates.

For equal-sized samples, sorting both samples and pairing values at the same rank produces this construction directly. For unequal sample sizes, one sample's quantiles are interpolated at the levels selected from the other. This lets the plot compare distributional shape even when the samples have different counts.

### Why a line is meaningful

Suppose the two distributions differ only by a location shift and a positive scale change: corresponding quantiles satisfy

$$ y_q = a + b x_q, \qquad b > 0. $$

Every Q-Q point then lies on one straight line. When $a=0$ and $b=1$, that is the 45-degree identity line: equal quantiles have equal values. A nonzero $a$ shifts the line, while a slope $b$ other than one indicates a difference in spread. The exact fitted reference line varies by convention, so its slope and intercept should not be over-interpreted as a hypothesis test.

The useful diagnostic is the *pattern* of departures:

- **Nearly straight points:** the samples have approximately the same shape, possibly with different location or scale.
- **A smooth curve:** their shapes differ, for example through asymmetry or a different rate at which values spread away from the center.
- **Departure only near an end:** their tails differ even if their central values agree.
- **Isolated distant points:** an observation may be unusual relative to the corresponding rank in the other sample.

A Q-Q plot is therefore evidence to investigate, not proof that two populations are identical or different. Sampling variation, small samples, and the selected quantile rule all affect the pattern.

### Comparing data with a model

The same construction supports a **normal Q-Q plot**: one side supplies sample quantiles and the other supplies quantiles from a chosen theoretical distribution. If the sample plausibly follows that distribution after the chosen location and scale adjustment, the points should be approximately linear. The plot can reveal where a model misses—especially in the tails—while preserving information that a single summary statistic would hide.

The Q-Q plot's central discipline is simple: compare like cumulative fractions. Because each point represents the same proportion of two distributions, the geometry turns distributional agreement or disagreement into a directly inspectable pattern.

## Prerequisites

- [[cumulative-distribution-function]] — defines the cumulative fractions whose inverse readings supply the matched quantiles.

## Sources

- National Institute of Standards and Technology, “Quantile-Quantile Plot” (Engineering Statistics Handbook), https://www.itl.nist.gov/div898/handbook/eda/section3/qqplot.htm
