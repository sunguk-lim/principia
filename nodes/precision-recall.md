---
id: precision-recall
title: Precision and Recall
summary: Precision measures the positive fraction of alerts, while recall measures the detected fraction of actual positives.
type: concept
tags: [ml/evaluation]
prereqs: [conditional-probability]
sources: [https://scikit-learn.org/stable/modules/model_evaluation.html]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Precision and Recall

## Summary

Precision asks whether alerts are useful; recall asks how much of the positive population was found. Their denominators differ, so excellent detection rates need not imply a manageable alert queue.

## Grounded explanation

Let $Y=1$ denote a true positive-class case and $A=1$ denote an alert. These metrics are [[conditional-probability]] statements: precision is $P(Y=1\mid A=1)$ and recall is $P(A=1\mid Y=1)$.

| Symbol | Type and meaning |
|---|---|
| $TP$ | Integer count, alerted positives |
| $FP$ | Integer count, alerted negatives |
| $FN$ | Integer count, missed positives |
| $TN$ | Integer count, unalerted negatives |
| $\pi$ | Scalar positive fraction in the population |
| $r$ | Scalar recall, also called true-positive rate |
| $f$ | Scalar false-positive rate |

$$\mathrm{precision}=\frac{TP}{TP+FP},\qquad r=\frac{TP}{TP+FN},\qquad f=\frac{FP}{FP+TN}.$$

If there are no alerts, precision has a zero denominator; if no positives exist, recall does. Report counts and the convention used instead of silently treating these cases as strong performance.

### Original example: the denominator dominates

Suppose there are 100 positive cases and 1,000,000 negative cases. At one threshold, 80 positives and 1,000 negatives trigger alerts. Then $TP=80$, $FN=20$, $FP=1000$, and $TN=999000$.

- Recall: $80/100=80\%$.
- False-positive rate: $1000/1000000=0.1\%$.
- Precision: $80/1080\approx7.41\%$.

Despite detecting most positives and rejecting nearly all negatives, 1,000 of the 1,080 alerts are false. A daily review capacity of 200 cannot handle this threshold.

For a population of size $N$, expected alerted positives number $Nr\pi$, and alerted negatives number $Nf(1-\pi)$. Cancelling $N$ yields

$$\mathrm{precision}=\frac{r\pi}{r\pi+f(1-\pi)}.$$

This independent derivation makes the base-rate effect explicit. Holding $r$ and $f$ fixed while positives become rarer reduces precision. It does not prove that a classifier's rates remain fixed under arbitrary distribution changes.

### Curves and decisions

Varying the alert threshold creates a precision-recall curve. The ROC curve instead plots recall against false-positive rate. ROC area summarizes ranking across thresholds, not precision at the threshold deployed. Neither summary selects a business operating point automatically.

Choose an operating point on held-out, representative data using missed-case costs, false-alert costs, and review capacity. Increasing the threshold reduces or preserves alert counts and recall; precision need not increase monotonically on finite data. Validate the resulting counts over time and relevant population slices. A threshold meeting a precision floor yesterday is not a guarantee tomorrow.

## Sources

- [scikit-learn model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html): classification counts, precision-recall and ROC definitions. Numerical example and base-rate derivation are independent.
