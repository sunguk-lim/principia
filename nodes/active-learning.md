---
id: active-learning
title: Active Learning
summary: Active learning repeatedly selects unlabeled examples whose acquired labels are expected to improve a model most, seeking a target quality with fewer labels than uninformed sampling.
type: concept
tags: [ml/training]
prereqs: [loss-function, model-calibration, probability-distribution, logarithm]
sources: [https://www.nltk.org/api/nltk.metrics.agreement.html, https://arxiv.org/abs/2005.14165, https://burrsettles.com/pub/settles.activelearning.pdf, https://arxiv.org/abs/1703.02910, https://arxiv.org/abs/1906.08158]
status: explained
created: 2026-09-09
updated: 2026-11-27
---

# Active Learning

## Summary

**Active learning** is a training loop in which the learner chooses which unlabeled examples should be labeled next. The objective is label efficiency: reach a measured quality level with fewer acquired labels than a policy such as uniform random sampling, after counting selection, inference, and annotation costs.

## Grounded explanation

Begin with a labeled set $L$, an unlabeled pool $U$, an annotation budget $b$, and a model trained to minimize a [[loss-function]]. An acquisition function assigns a score to candidates in $U$. Select a batch, obtain its labels from an oracle such as a human annotator, move those examples into $L$, retrain or update the model, and repeat until the budget or a stopping criterion is reached.

Uncertainty sampling is one acquisition rule. For a binary classifier emitting probability $p$, uncertainty is highest near $p=0.5$; an entropy score is

$$H(p)=-p\log p-(1-p)\log(1-p).$$

The log terms use [[logarithm]]. This score is derived from the model's [[probability-distribution]], not from the unknown label. It is only meaningful to the extent that scores express useful uncertainty; [[model-calibration]] checks whether predicted probabilities agree with observed frequencies but does not by itself make an acquisition policy optimal.

Suppose $U$ contains four candidates with positive probabilities `0.50`, `0.52`, `0.90`, and `0.10`, and the budget is two labels. Ranking each point independently by entropy selects `0.50` and `0.52`. If those two candidates are near-duplicates, the second label may add little information. A diversity-aware batch can instead choose one uncertain example and a less redundant candidate. BatchBALD formalizes this issue by selecting examples jointly according to information about model parameters; its experiments show that independent batch acquisition can choose redundant points.

The acquisition distribution is deliberately different from ordinary traffic, so evaluation must remain separate. Keep an untouched representative test set and compare learning curves against random sampling at equal total cost. Audit selected slices, duplicate rates, annotator disagreement, class coverage, and performance on important subgroups. Selecting only surprising points can over-represent outliers or annotation errors, while repeatedly training and scoring a very large model can cost more than the labels saved.

For an expensive model, use staged filtering when validated: a cheaper proxy can remove obvious duplicates or estimate acquisition scores, then the target model evaluates a smaller candidate set. This is an engineering approximation, not an automatic equivalence. Measure whether it preserves the ranking or downstream learning gain, and include compute, latency, and human cost in the stopping rule.

## Predictive entropy for generated sequences

For a language model, define the acquisition unit before computing uncertainty. Let $p_t(v)$ be the model probability of vocabulary token $v$ after the available prefix at position $t$. Its token predictive entropy is $H_t=-\sum_v p_t(v)\log p_t(v)$, using natural logarithms (units of nats), with zero-probability terms contributing zero. This describes predictive spread, not whether the response is false or the uncertainty could be reduced by more training data. Ambiguous valid continuations can have high entropy too.

A sum of token entropies along one sampled or teacher-forced continuation is not automatically the entropy of the whole sequence distribution. Joint sequence entropy averages conditional entropies over the model's possible prefixes. A sampled path is at most an estimator under stated sampling assumptions; a reference path defines a different conditional diagnostic. Tool or final-answer uncertainty can differ from fluent token uncertainty.

Length also changes rankings. In an invented example, a two-token response has per-step entropy 0.5 nats, while a six-token response has 0.3 nats. Sums are 1.0 and 1.8, selecting the longer example; means are 0.5 and 0.3, selecting the shorter one. Neither aggregation is universally correct: select the one that predicts useful annotation gain for the actual labeling unit.

Full vocabulary scores, repeated generations and retraining all consume resources. Validate token aggregation or cheaper proxy scores against random acquisition and task-level error at matched annotation and selection cost. Keep a representative held-out evaluation set and inspect long answers, rare formats and out-of-distribution inputs. A high entropy score is not proof of a useful label, and a confident model can still be wrong.

## Annotator disagreement in the acquisition loop

Model uncertainty and human disagreement are different signals. An acquisition rule can concentrate ambiguous examples, making its acquired batch less reproducible than ordinary traffic. Audit independent labels before adjudication, retain the instruction version and inspect disagreement by acquisition round and task slice. Agreement does not establish truth, while disagreement can reflect unclear policy, multiple valid answers, annotator error or genuinely difficult inputs.

In an invented batch, 20 of 100 acquired items have conflicting independent labels, compared with 4 of 100 randomly monitored traffic items. The difference can reflect selection toward ambiguity rather than a sudden collapse in annotator skill. Resolve the task definition and preserve original labels before treating every conflict as useful model uncertainty. Compare learning gains and adjudication cost; an acquisition policy can spend its entire budget repeatedly selecting irreducibly ambiguous cases. These audits support the loop's quality checks rather than replacing the acquisition objective with a raw disagreement coefficient.

## Prerequisites

- [[loss-function]]
- [[model-calibration]]
- [[probability-distribution]]

- [[logarithm]]

## Sources

- [Settles, “Active Learning Literature Survey”](https://burrsettles.com/pub/settles.activelearning.pdf): pool-based loops, uncertainty sampling, density weighting, batch acquisition, and practical considerations.
- [Gal, Islam, and Ghahramani, “Deep Bayesian Active Learning with Image Data”](https://arxiv.org/abs/1703.02910): uncertainty-based acquisition for deep models and its assumptions.
- [Kirsch, van Amersfoort, and Gal, “BatchBALD”](https://arxiv.org/abs/1906.08158): joint batch acquisition and redundancy in independently ranked batches.

- <https://arxiv.org/abs/2005.14165> — prefix-conditioned language-model probabilities; acquisition aggregation above is an explicit application design choice.

- <https://www.nltk.org/api/nltk.metrics.agreement.html>
