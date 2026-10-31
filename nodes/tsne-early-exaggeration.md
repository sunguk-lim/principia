---
id: tsne-early-exaggeration
title: t-SNE Early Exaggeration
summary: Early exaggeration temporarily scales t-SNE input affinities to strengthen attraction before ordinary neighborhood optimization resumes.
type: concept
tags: [ml/representation-learning]
prereqs: [t-sne, gradient-descent]
sources: [https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html, https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/manifold/_t_sne.py]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# t-SNE Early Exaggeration

## Meaning

Early exaggeration is an initial optimization phase of [[t-sne]], not a second dataset or a guarantee that plotted clusters represent real populations. It temporarily strengthens the attractive part of the neighborhood force before returning to the ordinary objective.

## Mechanism

Let p_ij be the normalized input affinity between different observations i and j, q_ij the current normalized map affinity, y_i their map positions, and alpha a factor greater than one. In the usual t-SNE force expression, the pair contribution is proportional to (p_ij-q_ij) times a distance-dependent factor and the displacement y_i-y_j. Early exaggeration replaces p_ij with alpha times p_ij in this force, strengthening attraction relative to repulsion during [[gradient-descent]]. After the initial phase alpha returns to one.

The scaled affinities sum to alpha, not one. Renormalizing them immediately would cancel the scaling and remove the intended change. Thus this is not simply fitting another normalized target distribution whose probabilities should all equal larger map probabilities simultaneously.

## Worked example

For one pair, take input affinity 0.02 and current map affinity 0.01. Without exaggeration the attractive-minus-repulsive coefficient is 0.02-0.01=0.01. With alpha=4 it is 0.08-0.01=0.07, seven times the original coefficient for this pair. This comparison holds the current positions and common distance factor fixed; it is not a sevenfold prediction of total movement or final separation. For a weak pair with affinity 0.001 and map affinity 0.01, the coefficient remains negative: 0.004-0.01=-0.006. Scaling every affinity does not make every pair attract.

## Boundaries and validation

Learning rate, initialization, duration and exaggeration interact. The scikit-learn implementation multiplies the affinities during its exploration phase and divides them back before continuation. Check the installed version rather than treating one schedule as universal. Inspect convergence, several seeds and neighborhood preservation; large visual gaps are not calibrated distances. Selectively exaggerating only strong affinities is a different method requiring its own evidence, not an established automatic improvement to the standard algorithm.

## Prerequisites

- [[t-sne]]
- [[gradient-descent]]

## Sources

- <https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html>
- <https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/manifold/_t_sne.py>
