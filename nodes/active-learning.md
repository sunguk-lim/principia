---
id: active-learning
title: Active Learning
summary: Active learning repeatedly selects unlabeled examples whose acquired labels are expected to improve a model most, seeking a target quality with fewer labels than uninformed sampling.
type: concept
tags: [ml/training]
prereqs: [loss-function, model-calibration, probability-distribution]
sources: [https://burrsettles.com/pub/settles.activelearning.pdf, https://arxiv.org/abs/1703.02910, https://arxiv.org/abs/1906.08158]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Active Learning

## Summary

**Active learning** is a training loop in which the learner chooses which unlabeled examples should be labeled next. The objective is label efficiency: reach a measured quality level with fewer acquired labels than a policy such as uniform random sampling, after counting selection, inference, and annotation costs.

## Grounded explanation

Begin with a labeled set $L$, an unlabeled pool $U$, an annotation budget $b$, and a model trained to minimize a [[loss-function]]. An acquisition function assigns a score to candidates in $U$. Select a batch, obtain its labels from an oracle such as a human annotator, move those examples into $L$, retrain or update the model, and repeat until the budget or a stopping criterion is reached.

Uncertainty sampling is one acquisition rule. For a binary classifier emitting probability $p$, uncertainty is highest near $p=0.5$; an entropy score is

$$H(p)=-p\log p-(1-p)\log(1-p).$$

This score is derived from the model's [[probability-distribution]], not from the unknown label. It is only meaningful to the extent that scores express useful uncertainty; [[model-calibration]] checks whether predicted probabilities agree with observed frequencies but does not by itself make an acquisition policy optimal.

Suppose $U$ contains four candidates with positive probabilities `0.50`, `0.52`, `0.90`, and `0.10`, and the budget is two labels. Ranking each point independently by entropy selects `0.50` and `0.52`. If those two candidates are near-duplicates, the second label may add little information. A diversity-aware batch can instead choose one uncertain example and a less redundant candidate. BatchBALD formalizes this issue by selecting examples jointly according to information about model parameters; its experiments show that independent batch acquisition can choose redundant points.

The acquisition distribution is deliberately different from ordinary traffic, so evaluation must remain separate. Keep an untouched representative test set and compare learning curves against random sampling at equal total cost. Audit selected slices, duplicate rates, annotator disagreement, class coverage, and performance on important subgroups. Selecting only surprising points can over-represent outliers or annotation errors, while repeatedly training and scoring a very large model can cost more than the labels saved.

For an expensive model, use staged filtering when validated: a cheaper proxy can remove obvious duplicates or estimate acquisition scores, then the target model evaluates a smaller candidate set. This is an engineering approximation, not an automatic equivalence. Measure whether it preserves the ranking or downstream learning gain, and include compute, latency, and human cost in the stopping rule.

## Prerequisites

- [[loss-function]]
- [[model-calibration]]
- [[probability-distribution]]

## Sources

- [Settles, “Active Learning Literature Survey”](https://burrsettles.com/pub/settles.activelearning.pdf): pool-based loops, uncertainty sampling, density weighting, batch acquisition, and practical considerations.
- [Gal, Islam, and Ghahramani, “Deep Bayesian Active Learning with Image Data”](https://arxiv.org/abs/1703.02910): uncertainty-based acquisition for deep models and its assumptions.
- [Kirsch, van Amersfoort, and Gal, “BatchBALD”](https://arxiv.org/abs/1906.08158): joint batch acquisition and redundancy in independently ranked batches.
