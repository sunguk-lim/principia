---
id: pass-at-k-evaluation
title: "Pass-at-k Evaluation"
summary: "Pass-at-k measures the probability that at least one of a fixed number of sampled candidates passes a declared oracle, rather than mean single-generation correctness or deployable selection accuracy."
type: concept
tags: [ml/evaluation]
prereqs: [probability, paired-benchmark-uncertainty, evaluation-oracle-availability]
sources: [https://arxiv.org/abs/2107.03374, https://raw.githubusercontent.com/openai/human-eval/master/human_eval/evaluation.py]
status: explained
created: 2026-11-10
updated: 2026-11-10
---

# Pass-at-k Evaluation

## Meaning

Mean generation accuracy counts correct samples. Pass-at-k counts a problem as solved when at least one of k sampled candidates passes. These measure different events, even when computed from the same stored generations. A real application also needs a way to select or verify that candidate; an oracle-based score does not automatically provide one.

## Mechanism

Let n be the number of sampled candidates for one problem, c the number that pass, and k the allowed number of tries, with 1≤k≤n. Let $\binom{a}{b}$ count size-b subsets from a objects, with zero subsets when b>a. The HumanEval estimator is

$$\widehat{\mathrm{pass@}k}=1-\frac{\binom{n-c}{k}}{\binom{n}{k}}.$$

There are $\binom{n}{k}$ possible size-k selections from the stored samples and $\binom{n-c}{k}$ all-failing selections. Taking one minus their fraction gives the success fraction. Under the sampling assumptions used for the evaluation, this estimates the repeated-sampling objective. It is not a license to treat adaptively repaired or correlated beam candidates as independent fresh attempts. With independent attempts each having success [[probability]] p, the population event is $1-(1-p)^k$; heterogeneous problems must be averaged per problem rather than substituting an overall mean p.

## One example

Two invented problems each receive four samples. Their correct counts are one and three. Mean sample correctness is (1+3)/8=50%. With two tries, the subset estimator for the first is $1-\binom{3}{2}/\binom{4}{2}=1-3/6=50\%$; for the second it is $1-\binom{1}{2}/6=100\%$. Mean estimated pass-at-two is 75%. With all four stored tries, both have at least one success, so observed coverage is 100%. The three percentages have different meanings and budgets.

## Check your understanding

Does pass-at-ten equal the accuracy of a production system returning one selected answer? No. The selector may miss the passing sample, and a weak oracle may accept a bad one. [[evaluation-oracle-availability]] separates observable correctness from unavailable reference information. Preserve problem-level grouping and use [[paired-benchmark-uncertainty]] for comparisons. Report sample budget, decoding policy, n, k, oracle, failures and the actual selection strategy; more sampling is additional work, not a free model improvement.

## Prerequisites

- [[probability]]
- [[paired-benchmark-uncertainty]]
- [[evaluation-oracle-availability]]

## Sources

- <https://arxiv.org/abs/2107.03374>
- <https://raw.githubusercontent.com/openai/human-eval/master/human_eval/evaluation.py>
