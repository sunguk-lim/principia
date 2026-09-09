---
id: feature-hashing
title: Feature Hashing
summary: Feature hashing maps an unbounded set of feature names into a fixed number of numeric coordinates with deterministic hashing, trading bounded memory and open-vocabulary handling for measurable collisions.
type: concept
tags: [ml/feature-engineering]
prereqs: [hash-map, tensor, arithmetic]
sources: [https://arxiv.org/abs/0902.2206]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Feature Hashing

## Summary

**Feature hashing** converts named features into a fixed-width numeric representation without maintaining a growing vocabulary. A deterministic hash chooses a coordinate for each name; values mapped to the same coordinate combine, so memory is bounded but distinct features can collide.

## Grounded explanation

Choose a width $m$. For every feature name $x$, compute a stable integer hash $h(x)$ and use [[arithmetic|modulo arithmetic]] to select coordinate

$$j(x)=h(x)\bmod m.$$

The same location calculation appears in a [[hash-map]], but feature hashing does not keep keys beside the buckets to resolve collisions. It adds the feature's numeric value directly into coordinate $j(x)$ of a one-dimensional [[tensor]]. An optional second hash supplies a sign $s(x)\in\{-1,+1\}$, reducing systematic bias when colliding values add.

For input features with values $v_x$, the output coordinate is

$$z_j=\sum_{x:j(x)=j}s(x)v_x.$$

Take $m=4$. Suppose `red` maps to coordinate 1 with sign $+1$, `round` maps to 3 with sign $+1$, and `rare-brand` also maps to 1 with sign $-1$. For values 2, 5, and 1, the result is `[0, 1, 0, 5]`: coordinate 1 contains $2-1=1$. The representation has accepted a previously unseen name without resizing, but its contribution cannot be separated from `red` after hashing.

Width controls the trade-off. A larger $m$ lowers collision frequency and costs more memory; a smaller $m$ is cheaper and mixes more unrelated signals. The mapping must be identical in training and serving: changing the hash algorithm, seed, text normalization, or width changes feature meaning even if the model file is unchanged.

Feature hashing prevents a categorical vocabulary from growing without bound and gives unknown identifiers a deterministic path. It does not create semantic similarity: two related names need not share a coordinate, while unrelated names may collide. Hashing raw item IDs can therefore bound a learned parameter table but cannot solve cold-start relevance by itself; content features, taxonomy fallbacks, or retraining may still be needed.

Validate candidate widths by measuring collision rates, task quality, memory, and latency on the real feature distribution. Include adversarial or highly frequent names, and version the complete hashing contract with the model so replay and rollback reproduce the same coordinates.

## Prerequisites

- [[hash-map]]
- [[tensor]]
- [[arithmetic]]

## Sources

- [Weinberger et al., “Feature Hashing for Large Scale Multitask Learning”](https://arxiv.org/abs/0902.2206): fixed-dimensional hashing, signed hashing, collision analysis, and empirical evaluation.
