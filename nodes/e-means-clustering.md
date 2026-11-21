---
id: e-means-clustering
title: "E-Means Clustering"
summary: "E-means optimizes k-means with scheduled exponential sum-and-count mini-batch updates, explicit center revival and a closing mean computation."
type: concept
tags: [ml/training]
prereqs: [mini-batch-k-means, centroid-revival]
sources: ["https://arxiv.org/abs/2611.09501", "https://github.com/facebookresearch/faiss/blob/108b92a248790b0f065f57deeb072039f75efca5/contrib/e_means/e_means.py", "https://github.com/facebookresearch/faiss/blob/108b92a248790b0f065f57deeb072039f75efca5/contrib/e_means/base.py", "https://github.com/facebookresearch/faiss/blob/108b92a248790b0f065f57deeb072039f75efca5/contrib/e_means/README.md"]
status: explained
created: 2026-11-22
updated: 2026-11-22
---

# E-Means Clustering

## Meaning

E-means is a particular mini-batch optimization procedure for squared-distance clustering. Frequent updates, exponential statistics, a step schedule, revival and fitted default recipes work together. It is not simply Lloyd's algorithm with smaller data transfers, nor a guarantee of identical final partitions.

## Mechanism

Use [[mini-batch-k-means]] assignments to collect, for each center j, batch count n_j and coordinate sum s_j. Let S_j and N_j be running weighted sum and mass. With step alpha and decay gamma=1-alpha, update S_j to gamma*S_j+alpha*s_j and N_j to gamma*N_j+alpha*n_j; the center is S_j/N_j when mass is positive. The inspected implementation stores the algebraically equivalent center and mass. For an ordinary update with 0<alpha<1, a cluster with no assigned points keeps its position while its mass decays; the implementation separately handles alpha=1.

For an invented center with N=10 and c=2, let a batch contain two points with sum 16 and alpha=.5. The updated mass is 6 and weighted sum is .5*20+.5*16=18, yielding c=3. This is not the naive blend .5*2+.5*8=5: averaging sums and counts gives occupancy-dependent effective steps.

### Scheduled steps and fitted defaults

The inspected code uses alpha(p)=alpha0*[.1+.9*(1+cos(pi*p))/2], where p is normalized update progress clamped at one. Its endpoints are alpha0 and .1*alpha0. The floor and progress definition are implementation-specific; do not assume every cosine schedule ends at zero. The recipe fits batch and initial-step rules from problem size and budget, then applies rounding, caps and overrides. This is empirical configuration, not a proof that tuning never matters. Shipped fit coefficients and low-dimensional defaults can differ from a paper's original settings.

### Revival and final readout

Apply [[centroid-revival]] according to the versioned policy. At closing, compute means from assignments gathered during the last moving pass. Those labels are not necessarily nearest to the final centers. Use a new assignment pass to obtain final nearest-center labels and a comparable final objective. Moving-pass objective sums and final-center distortion are different measurements.

## Boundaries and check

Compare time to matched final distortion, including transfer, assignment, initialization and any final scoring. Pin data order, seeds, precision, backend, dimensions, center count and recipe. Evaluate multiple geometries and downstream tasks. The primary paper reports specific benchmark gains; this explanation does not claim independent reproduction or a universal speedup.

**Check:** Can two runs with equal epoch counts be assumed to have equal work or quality? No. Their recipes, update counts, kernels and final scoring can differ.

## Prerequisites

- [[mini-batch-k-means]]
- [[centroid-revival]]

## Sources

- <https://arxiv.org/abs/2611.09501>
- <https://github.com/facebookresearch/faiss/blob/108b92a248790b0f065f57deeb072039f75efca5/contrib/e_means/e_means.py>
- <https://github.com/facebookresearch/faiss/blob/108b92a248790b0f065f57deeb072039f75efca5/contrib/e_means/base.py>
- <https://github.com/facebookresearch/faiss/blob/108b92a248790b0f065f57deeb072039f75efca5/contrib/e_means/README.md>
