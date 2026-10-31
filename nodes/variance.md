---
id: variance
title: Variance
summary: Variance is the expected squared distance of a random variable from its mean, while sample variance estimates population spread from observations.
type: concept
tags: [math/statistics]
prereqs: [expectation, arithmetic, random-variable]
sources: [https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Variance

## Meaning

Variance measures spread around a mean by averaging squared deviations. Squaring prevents positive and negative deviations from cancelling, while giving large deviations greater weight. Its units are the square of the original measurement units.

## Mechanism

Let X be a [[random-variable|random variable]] with finite second moment, mu=E[X] its mean, and E the [[expectation]] operation. Population variance is Var(X)=E[(X-mu)²]. Expanding the square with [[arithmetic]] gives the equivalent identity E[X²]-mu², although direct subtraction of similar large machine values can be numerically inaccurate.

For n observations x_1 through x_n, let x_bar be their arithmetic mean. The descriptive average squared deviation uses denominator n. The usual sample-variance estimator s² uses n-1 after estimating the mean from the same observations; under independent identically distributed sampling with finite variance it is unbiased for population variance. These are different quantities, not interchangeable denominator conventions. Standard deviation is the nonnegative square root of variance and restores the original units.

## Worked example

For observations 1, 3 and 5, the mean is (1+3+5)/3=3. Deviations are -2, 0 and 2; squared deviations sum to 4+0+4=8. Descriptive variance is 8/3, about 2.667, while sample variance is 8/(3-1)=4. Their standard deviations are about 1.633 and 2 respectively. Neither calculation is wrong: one describes these three values, the other applies an estimation convention.

For a zero/one variable with success probability p, E[X]=p and E[X²]=p because squaring zero or one leaves it unchanged. Therefore Var(X)=p-p²=p(1-p). Variance of an average further depends on dependence among observations; dividing by sample size assumes an appropriate independence model.

## Boundaries

Variance is sensitive to extreme values and may not exist for some distributions. A small sample estimate is uncertain. Distinguish data spread from uncertainty of an estimated mean, and record the sampling unit and denominator. Correlated benchmark items cannot be treated as independent merely because they have separate rows.

## Prerequisites

- [[random-variable]]
- [[expectation]]
- [[arithmetic]]

## Sources

- <https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm>
