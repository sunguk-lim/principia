---
id: memorizing-transformer-retrieval
title: Memorizing Transformer Retrieval
summary: A memorizing transformer stores past key–value representations in an external nearest-neighbor memory and retrieves selected old context instead of attending to every past token.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, nearest-neighbor-search, context-window]
sources: [https://arxiv.org/abs/2203.08913]
status: explained
created: 2026-10-16
updated: 2026-10-16
---

# Memorizing Transformer Retrieval

## Summary

A **memorizing transformer** augments local [[transformer-attention]] with a non-differentiable store of earlier key–value representations. A query retrieves a small number of neighbors from that store, allowing direct access to selected older states without full-history attention.

## Grounded explanation

Ordinary attention over a growing sequence requires an expanding set of keys and values. In the Memorizing Transformers paper, representations from prior positions enter an external memory; current queries use [[nearest-neighbor-search]] to select relevant stored keys. Their associated values can then contribute alongside local attention. This differs from Transformer-XL recurrence: prior information is selected by similarity rather than passed only through the latest segment's hidden-state summary.

The memory is not a guarantee of exact fact recall. Retrieval can miss a relevant state, approximate search can return a near but wrong neighbor, and stored vectors depend on the model representation that created them. Capacity, eviction, and access latency remain operational constraints. For a long document with a rare early name, a retrieval path might recover the earlier representation even after it leaves the local [[context-window]], but only if the stored key makes it searchable under the later query. Local attention remains useful for nearby syntax and short dependencies.

Evaluate memory size, retrieval latency, and task accuracy as the required evidence distance grows. Compare a same-compute local-window model, recurrent segment memory, and external key–value retrieval; isolate the gain from more stored information versus better selection. Inspect false retrievals and privacy/retention boundaries for stored states. The original paper grounds the mechanism, not a claim that any particular deployed model uses it or that it makes context effectively infinite.

## Prerequisites

- [[transformer-attention]]
- [[nearest-neighbor-search]]
- [[context-window]]

## Sources

- [Wu et al., Memorizing Transformers](https://arxiv.org/abs/2203.08913): approximate nearest-neighbor retrieval over stored representations.
