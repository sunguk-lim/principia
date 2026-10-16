---
id: cold-start-item-serving
title: Cold-Start Item Serving
summary: Cold-start item serving ranks new or unseen items through versioned content features, bounded unknown representations, and latency-aware online metadata fallbacks rather than assuming an ID embedding exists.
type: concept
tags: [ml/systems]
prereqs: [feature-hashing, ml-system-freshness, classifier-serving-contract]
sources: [https://developers.google.com/machine-learning/recommendation/dnn/training, https://developers.google.com/machine-learning/guides/rules-of-ml]
status: explained
created: 2026-10-16
updated: 2026-10-16
---

# Cold-Start Item Serving

## Summary

A newly published catalog item may have no learned ID embedding or interaction history. **Cold-start serving** gives it a bounded, reproducible representation from available metadata while protecting ranking latency and quality.

## Grounded explanation

An ID-only recommender cannot infer much about an unseen item. [[feature-hashing]] can map arbitrary IDs into fixed buckets, but collisions and lack of item history mean that hashability is not personalization. Content, category, price, creator, or other verified metadata can supply features known before interactions. A taxonomy-conditioned unknown embedding is a coarse fallback: it can distinguish broad groups but loses within-group specificity. Version the taxonomy and encoder with the model under the [[classifier-serving-contract]] so old weights never meet a silently changed category map.

An online metadata lookup is another path. It can obtain current attributes without retraining the model, but it adds network latency, cache staleness, missing-key behavior, and failure modes. Set a deadline and a safe fallback before the request path. Async lookup is not magically free: if ranking waits for its result, the dependency still contributes to tail latency. Cache or precompute stable attributes; mark their age under [[ml-system-freshness]]. If metadata is unavailable, use a measured category fallback or an explicit exploration path, not an arbitrary default claimed to preserve relevance.

For a new film, compare three candidates: a global unknown vector, a genre-conditioned vector, and content-derived features loaded from a versioned item store. Replay future-created items so their interaction histories cannot leak into training. Report cold-item ranking quality, catalog coverage, unknown rate, lookup hit rate, p95 latency, outage behavior, and the effect of hash collisions. Keep warm-item quality in the comparison; a cold-start fix should not silently regress established traffic. Retraining cadence and online lookup solve different freshness problems and can coexist.

## Prerequisites

- [[feature-hashing]]
- [[ml-system-freshness]]
- [[classifier-serving-contract]]

## Sources

- [Google, recommendation training guide](https://developers.google.com/machine-learning/recommendation/dnn/training): item features and candidate representation context.
- [Google, Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml): freshness and practical feature-system constraints.
