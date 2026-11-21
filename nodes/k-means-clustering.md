---
id: k-means-clustering
title: K-means clustering
summary: K-means partitions observations into a chosen number of groups by alternating nearest-centroid assignment with centroid recomputation, minimizing within-cluster squared distances only locally.
type: concept
tags: [ml/training]
prereqs: [arithmetic]
sources: [https://scikit-learn.org/stable/modules/clustering.html#k-means, https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html]
status: explained
created: 2026-09-13
updated: 2026-11-22
---

# K-means clustering

## Summary

**K-means clustering** divides observations into a chosen number $K$ of groups by assigning each observation to a nearby representative point (a *centroid*) and repeatedly replacing each centroid with the mean of its assigned observations.

## Grounded explanation

Given observations $x_1,\ldots,x_n$, K-means chooses assignments $z_i \in \{1,\ldots,K\}$ and centroids $\mu_1,\ldots,\mu_K$ to make the within-cluster sum of squared distances small:

$$\sum_{i=1}^{n} \lVert x_i-\mu_{z_i}\rVert^2.$$

Lloyd's algorithm alternates two operations. First, assign each observation to the centroid with the smallest squared distance. Second, for every nonempty cluster, replace its centroid with the coordinate-wise mean of the observations currently assigned to it. Each completed pair of operations does not increase that objective, so the procedure eventually reaches a fixed assignment; it need not find the best possible partition because different initial centroids can lead to different local minima.

The requested $K$ is an input, not a discovered fact. A useful choice depends on the purpose and the data: compare multiple initializations, inspect cluster sizes and stability, and evaluate whether the resulting groups support the downstream task. Scaling matters because squared distance gives large-range features more influence. Missing values, outliers, non-spherical shapes, and unequal-density groups can make nearest-centroid partitions misleading; a low objective alone is not evidence that the groups are meaningful.

## Compare at matched final quality

Epochs count dataset passes, not equal wall time, update counts or final quality. Compare algorithms at a declared final distortion or downstream-quality target using the same data representation, metric, initialization policy, precision and hardware. Record unsuccessful target attainment rather than removing those runs. Include data transfer, initialization, kernel warmup and final nearest-center reassignment according to an explicit timing boundary. Repeat seeds and retain the actual partitions and objective, not just the best run.

A mini-batch algorithm can report losses accumulated while centers move. That is not the objective obtained by assigning every point to the final centers. Recompute the latter for a comparable final measurement. For an invented benchmark, algorithm A reaches distortion 5 in ten seconds and B reports 3 seconds at distortion 8. This is not a matched-quality speedup. If B reaches distortion 5 in seven seconds including comparable scoring, the measured time ratio is 10/7 for that workload, not a general algorithmic guarantee.

An empirically fitted batch recipe still has a fitting domain and budget. Test transfer to different dimensions, center counts, distributions and systems. More centroid moves per pass can improve progress, but launch overhead, memory traffic, arithmetic, precision and convergence affect elapsed time. Neither a lower clustering objective nor a faster implementation alone proves better retrieval or training-data quality.

## Prerequisites

- [[arithmetic]]

## Sources

- [scikit-learn User Guide, “K-means”](https://scikit-learn.org/stable/modules/clustering.html#k-means): defines the within-cluster sum-of-squares objective, Lloyd iteration, initialization sensitivity, and geometric limitations.
- [scikit-learn API Reference, `KMeans`](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html): documents initialization, repeated runs, convergence behavior, and the estimator's fitted outputs.
