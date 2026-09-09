---
id: permutation-feature-importance
title: Permutation Feature Importance
summary: Permutation feature importance measures how much a fitted model’s score degrades when one feature is shuffled, estimating reliance on that feature for a chosen dataset and metric rather than intrinsic causal value.
type: concept
tags: [ml/evaluation]
prereqs: [measurement, probability-distribution]
sources: [https://scikit-learn.org/stable/modules/permutation_importance.html]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Permutation Feature Importance

## Summary

**Permutation feature importance** measures a fitted model’s reliance on one feature by randomly breaking that feature’s alignment with the other columns and target, then measuring the score loss. It describes one model, dataset, and metric; it does not establish that the feature is intrinsically useful or causes the prediction.

## Grounded explanation

Let $s(D)$ be a chosen performance [[measurement]] for a fitted model on dataset $D$. For feature $j$, independently shuffle its observed values across rows to create $D_{j,k}$ on repetition $k$. The importance estimate is

$$I_j=s(D)-\frac{1}{K}\sum_{k=1}^{K}s(D_{j,k}).$$

Shuffling preserves the feature’s marginal [[probability-distribution]] but destroys its row-level association. If the fitted model depends on that association, its score falls and $I_j$ is positive. Repetitions expose variability from the random permutations.

Suppose validation accuracy is $0.84$. Three shuffles of feature A produce `0.72`, `0.74`, and `0.73`, so $I_A=0.84-0.73=0.11$. Feature B produces `0.83`, `0.85`, and `0.84`, giving $I_B=0$. This supports pruning B only for this model and validation distribution; a retrained model may use B differently.

Correlated features complicate interpretation. If A and B carry nearly the same signal, shuffling A can leave B available and make A appear unimportant even though the pair matters. Shuffling can also create implausible rows when feature combinations are constrained. Grouped or conditional permutations may be more faithful, but they answer different questions.

Compute importance only after confirming useful held-out performance. Use the deployment metric, repeat permutations, report uncertainty, and remeasure latency and quality after any feature removal. A large importance does not prove causal influence, and a small one does not justify removing a feature without retraining and testing the resulting system.

## Prerequisites

- [[measurement]]
- [[probability-distribution]]

## Sources

- [scikit-learn, “Permutation feature importance”](https://scikit-learn.org/stable/modules/permutation_importance.html): algorithm, held-out evaluation, repeated shuffles, metric dependence, and correlated-feature limitation.
