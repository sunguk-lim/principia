---
id: cohen-kappa
title: "Cohen\u2019s Kappa"
summary: "Cohen\u2019s kappa rescales observed categorical agreement relative to agreement expected from the two raters\u2019 empirical label marginals."
type: concept
tags: [ml/evaluation]
prereqs: [confusion-matrix, probability]
sources: [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html]
status: explained
created: 2026-11-13
updated: 2026-11-13
---

# Cohen’s Kappa

## Meaning

Cohen’s kappa measures agreement between two categorical raters beyond a specified chance baseline. The raters are symmetric: neither is automatically ground truth. It is not classification accuracy unless one separately designates a trusted reference.

## Mechanism

Construct a [[confusion-matrix]] with rater A on rows and rater B on columns. Let n be the total items, C_ij the count in row i and column j, p_o the diagonal count divided by n, a_k rater A’s fraction using class k, and b_k rater B’s fraction using that class. The [[probability]] of chance agreement under independent marginal draws is p_e=sum_k a_k b_k. Define

$$\kappa=\frac{p_o-p_e}{1-p_e}.$$

The numerator removes agreement expected from label frequency; the denominator scales by the maximum additional agreement available. This is an explicit baseline model, not a claim that real raters label randomly. If p_e=1 the denominator is zero and kappa is undefined; do not silently convert it to perfect reliability.

## One example

For ten items, joint counts for labels reject/accept are [[4,1],[2,3]]. The diagonal gives p_o=(4+3)/10=.7. A uses each label five times, while B uses reject six times and accept four times, so p_e=.5×.6+.5×.4=.5. Thus kappa=(.7-.5)/(1-.5)=.4. The raw agreement is 70%, not 40%; kappa answers a different question.

## Boundaries and check

Kappa depends on prevalence and marginal disagreement. Report the count table, label definitions, sample size, uncertainty and raw agreement alongside it. Ordered labels may motivate explicitly weighted kappa, which changes the penalty for different disagreements. Two biased raters can agree strongly while both being wrong. Test label-order consistency, absent classes and the degenerate denominator before using it as a release criterion.

## Prerequisites

- [[confusion-matrix]]
- [[probability]]

## Sources

- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html>
