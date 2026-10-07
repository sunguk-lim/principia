---
id: hierarchical-sparse-attention-index
title: Hierarchical Sparse Attention Index
summary: A hierarchical sparse attention index narrows candidate past tokens in stages so deeper queries search a bounded subset rather than the entire context.
type: concept
tags: [ml/llm/inference]
prereqs: [transformer-attention, kv-cache, nearest-neighbor-search]
sources: [https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash]
status: explained
created: 2026-10-08
updated: 2026-10-08
---

# Hierarchical Sparse Attention Index

## Summary

Full [[transformer-attention]] compares a query with every earlier key. A sparse index chooses a smaller candidate set before computing attention. A **hierarchical** index lets an initial broad stage propose candidates and makes later stages refine that pool rather than search the full history again. This is approximate information selection, not a free reduction in work.

## Grounded explanation

A query over a long [[kv-cache]] has two costs: finding relevant past positions and reading their values. Sparse attention reduces the second only if selection is cheap and recall is high enough. The index itself may require keys, scores, or a learned representation; caching and sharing those structures across layers can save bytes while coupling the layers' choices. The [[nearest-neighbor-search]] analogy is useful, but a learned attention index need not implement a generic ANN algorithm.

DeepSeek's V4.1 Flash model card calls its mechanism Compressed Sparse Attention 2. It reports layer modes named Full, Reindex, and Reuse, with a hierarchical decoder index whose later stages search a candidate pool built by the first Full stage. Those names and efficiency figures describe one implementation, not a general guarantee. A missed token cannot be recovered by more precise attention over the wrong pool, so early-stage recall is the principal quality risk.

Compare with dense attention and fixed local-window attention at matched model quality and hardware. Measure candidate recall on tasks requiring old information, index construction cost, cache bytes, prefill/decode latency, and sensitivity to context length. Test adversarially placed facts and multi-hop dependencies; report failures separately from aggregate next-token loss. Quantization, candidate selection, and cross-layer reuse need independent ablations before attributing a speedup.

## Sources

- [DeepSeek V4.1 Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash): primary description of Full/Reindex/Reuse modes and hierarchical candidate selection; numerical gains are author-reported.
