---
id: feature-space-serving-budget
title: Feature-Space Serving Budget
summary: A feature-space serving budget evaluates feature crosses by their incremental prediction value and measured extraction, lookup, memory, and tail-latency cost under production traffic.
type: concept
tags: [ml/systems]
prereqs: [feature-hashing, permutation-feature-importance, measurement]
sources: [https://developers.google.com/machine-learning/crash-course/categorical-data/feature-crosses, https://scikit-learn.org/stable/modules/feature_extraction.html#feature-hashing]
status: explained
created: 2026-10-17
updated: 2026-10-17
---

# Feature-Space Serving Budget

## Summary

A feature cross represents an interaction between two or more inputs. Crossing high-cardinality categories can create a large *possible* feature space, but it does not automatically make every request perform many remote lookups. The useful systems question is whether a cross improves held-out outcomes enough to justify its actual extraction, storage, lookup, and inference cost under the service-level objective.

## Grounded explanation

If feature A has $a$ categories and B has $b$, their pair has up to $ab$ possible values. Most may never occur. Sparse one-hot, embedding-table, and [[feature-hashing]] implementations store and access that space differently. A sparse example can still activate only one pair even when the global vocabulary is enormous; a dense or remotely fetched representation may have very different per-request costs. Do not infer a cache miss or a memory-bandwidth bottleneck from cardinality alone—profile the live serving path.

Separate stages: raw-feature acquisition, transformation and cross construction, feature-store access, model-table lookup, compute, and network queueing. Record p50 and p99 latency, bytes moved, cache-hit rate, memory residency, and per-stage CPU/GPU time. [[measurement]] on an end-to-end request is needed because optimizing arithmetic will not repair a remote lookup bottleneck. Estimate quality using a time-appropriate holdout, then ablate candidate crosses and re-train. [[permutation-feature-importance]] can rank reliance for a fixed model, but correlated crosses may substitute for one another and shuffling can create implausible combinations.

Options include dropping a cross, limiting its vocabulary, hashing it into a bounded table, compressing an embedding, caching a frequent lookup, or increasing capacity. Each changes the error–cost trade-off differently. Hashing bounds storage while introducing collisions; a smaller embedding may save memory while losing information. A zero learned coefficient does not remove the upstream feature pipeline unless the feature is actually pruned from serving.

## Validation

Use the same time-respecting test set and production-like request mix for every candidate. Compare model quality, worst-slice error, p99 latency, throughput, cache behavior, and cost under matched load. Profile before assuming the bottleneck; validate the full deployment path after pruning, not only offline AUC. Treat any reported percentage gain or latency target from a saved interview question as an unverified scenario, not a measured result.

## Prerequisites

- [[feature-hashing]]
- [[permutation-feature-importance]]
- [[measurement]]

## Sources

- [Google ML Crash Course, categorical feature crosses](https://developers.google.com/machine-learning/crash-course/categorical-data/feature-crosses): interaction construction and sparsity risk.
- [scikit-learn feature extraction and hashing](https://scikit-learn.org/stable/modules/feature_extraction.html#feature-hashing): bounded hashed representation and its trade-offs.
