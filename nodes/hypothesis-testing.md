---
id: hypothesis-testing
title: Hypothesis Testing
summary: Hypothesis testing compares an observed statistic with its distribution under a stated null model and controls how often that null is rejected when it is true.
type: concept
tags: [math/statistics]
prereqs: [probability-distribution, conditional-probability]
sources: [https://www.itl.nist.gov/div898/handbook/prc/section1/prc131.htm]
status: explained
created: 2026-09-17
updated: 2026-09-17
---

# Hypothesis Testing

## Summary

**Hypothesis testing** starts with a precise baseline claim—the **null hypothesis**—and asks whether an observed result would be unusually extreme if that baseline were true. It does not calculate the probability that the null itself is true. It controls a decision rule's false-rejection rate under the null.

## Grounded explanation

Let $H_0$ be a null hypothesis and let $S$ be a statistic computed from observed data. The null specifies a [[probability-distribution]] for $S$. Before seeing the data, choose a significance level $\alpha$: the maximum probability of rejecting $H_0$ when it is true. A critical region is then chosen so

$$P(S\text{ falls in the critical region}\mid H_0)\le \alpha.$$

This is a [[conditional-probability]] statement. The conditioning phrase “given that $H_0$ is true” is essential: the procedure describes how data behave under the null, not how probable the null is after observing data.

The **p-value** is the probability, under $H_0$, of a statistic at least as extreme as the observed one. A small p-value means that the observation is difficult to reconcile with the null model. Rejecting at level $\alpha$ means the p-value is at most $\alpha$. It does not mean that the chance of a false conclusion for this particular result is $\alpha$, and it does not measure practical importance.

### Worked example

Suppose $H_0$ says that a coin lands heads with probability $0.5$. Choose the statistic $S$ as the number of heads in 100 flips and set $\alpha=0.05$. Under the null, $S$ has a distribution centered at 50. Observing 65 heads is evidence against $H_0$ only to the extent that outcomes of 65 or more heads, together with equally extreme low counts for a two-sided test, occupy at most 5% of the null distribution. The p-value is that tail probability, not $P(H_0\mid S=65)$.

The test's conclusion depends on the null model, statistic, tail definition, sample plan, and threshold. Repeatedly trying statistics or thresholds after looking at the data changes the false-positive rate. Report the statistic, p-value or interval, sample size, assumptions, and effect size; use held-out data or corrected procedures when many tests are searched.

## Prerequisites

- [[probability-distribution]]
- [[conditional-probability]]

## Sources

- [NIST/SEMATECH e-Handbook, “Critical values and p values”](https://www.itl.nist.gov/div898/handbook/prc/section1/prc131.htm): definitions of significance level, rejection regions, and p-values under a null hypothesis.
