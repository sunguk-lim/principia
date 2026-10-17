---
id: selective-classification
title: Selective Classification
summary: Selective classification combines a predictor with a reject rule and evaluates error conditional on acceptance together with the fraction of inputs accepted.
type: concept
tags: [ml/evaluation]
prereqs: [conditional-probability, model-calibration]
sources: [https://proceedings.neurips.cc/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html]
status: explained
created: 2026-10-18
updated: 2026-10-18
---

# Selective Classification

## Summary

Selective classification combines a predictor with a reject rule and evaluates error conditional on acceptance together with the fraction of inputs accepted.

## Grounded explanation

A classifier normally returns an answer for every input, including cases where that answer is unreliable. A selective classifier adds a *selection rule*: return the prediction only when the rule accepts it; otherwise abstain or hand the input to another process. The central object is the pair of predictor and selector, not a confidence score alone.

Let $X$ be an input, $Y$ its correct label, $f(X)$ the proposed label, and $g(X)$ a binary selector: $1$ accepts and $0$ rejects. Define coverage $C=P(g(X)=1)$ and selective risk

$$R=P(f(X)\ne Y\mid g(X)=1).$$

This [[conditional-probability]] measures error *among accepted cases*. It is undefined when coverage is zero. Rejecting everything cannot count as perfect service: always report coverage, accepted counts, and risk together.

For example, a predictor makes 100 errors on 1,000 cases. A selector accepts 600 cases containing 12 errors, so coverage is $600/1000=60\%$ and selective risk is $12/600=2\%$. These are illustrative counts, not a model benchmark. The rejected 400 cases still require a policy; their processing cost and eventual outcomes belong in the end-to-end evaluation.

A common selector accepts when the largest model score exceeds a threshold. [[model-calibration]] checks whether scores correspond to observed correctness frequencies, but good average calibration alone does not guarantee a chosen selective risk on every class or future population. Conversely, a selector can use another diagnostic rather than a probability estimate. Raising the threshold reduces or preserves coverage; empirical risk need not decrease monotonically on a finite sample.

Choose a threshold using representative labeled selection data and check it on separate evaluation data. Plot risk against coverage, report sample counts and uncertainty, and examine rare classes. A desired risk bound requires the assumptions and statistical construction supporting that bound; a threshold number by itself is not a guarantee. Distribution changes, new classes, or a revised predictor invalidate automatic transfer of an old measured operating point.

Compare selective prediction with always answering, rules, a second model, and human review under the same error and rejection costs. A learned `unknown` label is useful only if training and evaluation make it meaningful; it does not automatically detect every input outside the offered categories.

## Prerequisites

- [[conditional-probability]]
- [[model-calibration]]

## Sources

- <https://proceedings.neurips.cc/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html>
