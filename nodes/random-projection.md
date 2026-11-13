---
id: random-projection
title: Random Projection
summary: Random projection maps vectors through a randomly chosen scaled matrix to reduce coordinates while controlling geometric distortion under a stated distribution and target dimension.
type: concept
tags: [math/linear-algebra]
prereqs: [variance, matrix-multiplication, normal-distribution, euclidean-distance]
sources: [https://scikit-learn.org/stable/modules/random_projection.html]
status: explained
created: 2026-11-14
updated: 2026-11-14
---

# Random Projection

## Meaning

Random projection chooses a linear map without learning its directions from the dataset, then applies the same map to each vector. It can reduce the number of coordinates at the cost of distortion; it is not arbitrary coordinate deletion or a guarantee of preserving every possible input.

## Mechanism

Let x be a column vector with d coordinates. Draw a matrix R with k rows and d columns, then compute z=Rx using [[matrix-multiplication]]. The result z has k coordinates. One standard construction draws entries independently from a [[normal-distribution]] with mean zero and [[variance]] 1/k. That scaling prevents expected squared lengths from growing with the number of output coordinates. Once sampled, R remains fixed for transforming related examples and later queries.

Measure the ratio of projected to original squared [[euclidean-distance]] for nonidentical point pairs. A ratio near one indicates small distortion for that pair. Averages alone can hide a badly distorted pair or subset. Redrawing the map independently for each item would put those items in incompatible coordinate systems.

## One example

Take a possible two-by-three random-sign map R whose rows are (1,1,1)/sqrt(2) and (1,-1,1)/sqrt(2). Each entry has magnitude 1/sqrt(2). For x=(1,2,3), matrix multiplication gives z=(6,2)/sqrt(2). For y=(4,6,3), it gives (13,1)/sqrt(2). Original squared separation is 9+16=25; projected squared separation is (49+1)/2=25. This pair is preserved by this particular draw.

But w=(2,2,2) has the same projection as x, even though original squared separation is 1+0+1=2. No reduction from three coordinates to two can protect every direction. The example is a possible sign-matrix draw, not evidence that a two-dimensional target meets a whole-dataset probability guarantee.

A suitably distributed random map with enough output coordinates protects a fixed finite set with a stated probability; a severe coordinate reduction need not protect every direction. The map can discard information and generally cannot reconstruct the original vector exactly.

## Check your understanding

Must fitting a random-projection transformer optimize a prediction loss? No. In this construction it samples a matrix of the required shape. Validate downstream quality and distortion separately, and preserve the seed or matrix for reproducibility.

## Prerequisites

- [[matrix-multiplication]]
- [[normal-distribution]]
- [[euclidean-distance]]

## Sources

- <https://scikit-learn.org/stable/modules/random_projection.html>
