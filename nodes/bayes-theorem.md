---
id: bayes-theorem
title: Bayes' Theorem
summary: Bayes' theorem reverses a conditional probability by combining a likelihood with a prior and normalizing by the probability of the evidence.
type: concept
tags: [math/probability]
prereqs: [conditional-probability, probability, likelihood]
sources: [https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/pages/unit-i/lecture-2/]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Bayes' Theorem

## Summary

**Bayes' theorem** relates two directions of [[conditional-probability]]:

$$P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)},\qquad P(B)>0.$$

## Grounded explanation

The multiplication rule writes the same joint event in two ways:

$$P(A\cap B)=P(A\mid B)P(B)=P(B\mid A)P(A).$$

Equating them and dividing by $P(B)$ gives Bayes’ theorem. In inference language, $P(A)$ is the prior, $P(B\mid A)$ is the [[likelihood]] of evidence $B$ under hypothesis $A$, $P(B)$ is the evidence or normalizer, and $P(A\mid B)$ is the posterior.

If mutually exclusive and exhaustive hypotheses $H_1,\ldots,H_n$ form the cases, the evidence is

$$P(B)=\sum_i P(B\mid H_i)P(H_i),$$

so

$$P(H_j\mid B)=\frac{P(B\mid H_j)P(H_j)}{\sum_i P(B\mid H_i)P(H_i)}.$$

### Worked example

Suppose a condition has prevalence $P(C)=0.01$. A test is positive with probability $0.90$ when the condition is present and $0.05$ otherwise. Then

$$P(C\mid +)=\frac{0.90(0.01)}{0.90(0.01)+0.05(0.99)}\approx0.154.$$

Despite 90% sensitivity, a positive result corresponds to about 15.4% posterior probability because false positives arise from a much larger unaffected population.

The formula does not repair a bad model. Incorrect priors, selection bias, dependence between combined evidence, or shifted test characteristics produce incorrect posteriors. State the reference population, define events unambiguously, and verify denominator terms with frequencies or simulation.

## Prerequisites

- [[conditional-probability]]
- [[probability]]
- [[likelihood]]

## Sources

- [MIT OpenCourseWare 6.041SC, “Lecture 2: Conditioning and Bayes’ Rule”](https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/pages/unit-i/lecture-2/): covers conditional probability, multiplication and total-probability rules, and Bayes’ rule.
