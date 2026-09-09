---
id: t-sne
title: t-Distributed Stochastic Neighbor Embedding
summary: t-SNE visualizes high-dimensional data by optimizing a two- or three-dimensional map whose nearby points preserve local similarity relationships.
type: concept
tags: [ml/representation-learning]
prereqs: [nearest-neighbor-search, kl-divergence]
sources: [https://jmlr.org/papers/v9/vandermaaten08a.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# t-Distributed Stochastic Neighbor Embedding

## Summary

**t-SNE** is a visualization method that places high-dimensional observations in a two- or three-dimensional map while trying to preserve which observations are local neighbors.

## Grounded explanation

t-SNE is for inspecting structure, not for producing a generally faithful low-dimensional coordinate system. It starts from pairwise neighborhood relationships among the original observations, then assigns map locations so that observations with high local similarity remain near one another. The resulting display can make clusters or local neighborhoods easier to inspect, but its axes do not carry an intrinsic meaning and distances between well-separated groups need not preserve the original global geometry.

The method represents neighbor relationships in the input and map spaces as probability distributions. It then minimizes a [[kl-divergence]] from the input-neighborhood distribution to the map-neighborhood distribution. Because that penalty weights pairs that are neighbors in the input space, an output that separates originally close observations is costly. This objective explains why t-SNE is especially useful for local structure and why a visually separated map is not, by itself, evidence of equally separated populations in the original data.

For a practical use, first choose the observations and their representation, run t-SNE with multiple seeds and parameter settings, and compare the recurring local neighborhoods with the original [[nearest-neighbor-search]] results. Treat a stable pattern as a hypothesis to investigate, not a conclusion: validate it against labels, domain measurements, or a method designed for the downstream task. The map is an exploratory view; it does not replace a classifier, a clustering evaluation, or an estimate of global distance.

## Prerequisites

- [[nearest-neighbor-search]]
- [[kl-divergence]]

## Sources

- [van der Maaten and Hinton, “Visualizing Data using t-SNE”](https://jmlr.org/papers/v9/vandermaaten08a.html): the abstract describes a method that gives each high-dimensional datapoint a location in a two- or three-dimensional map and reports its focus on structure across scales.
