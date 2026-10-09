---
id: sparse-attention-patterns
title: Sparse Attention Patterns
summary: Sparse attention patterns restrict which token pairs interact, trading lower potential sequence cost for coverage, routing, and implementation risks that must be tested on long-range tasks.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, sliding-window-attention, measurement]
sources: [https://arxiv.org/abs/1904.10509, https://arxiv.org/abs/2004.05150, https://arxiv.org/abs/2007.14062]
status: explained
created: 2026-10-10
updated: 2026-10-10
---

# Sparse Attention Patterns

## Summary

Dense attention connects each query to every permitted key. Sparse patterns compute a chosen subset of those edges. The design question is which omitted interactions can be reconstructed through local windows, global tokens, strides, random links, or multiple layers.

## Grounded explanation

[[transformer-attention]] over $n$ positions forms $O(n^2)$ scores when dense. A local window of width $w$ allows roughly $O(nw)$ pairs; adding a stride or global tokens expands reach while retaining fewer than all pairs. [[sliding-window-attention]] is one fixed pattern. Sparse Transformer, Longformer, and BigBird describe different combinations of local, global, strided, and random links; their complexity guarantees depend on exact widths, number of globals, and implementation. A pattern's mathematical edge count is not a throughput result if a kernel still materializes a dense matrix or irregular indexing dominates.

A purely local stack can propagate information across blocks only after enough layers. A global token can bridge distant positions faster, but it may become a bandwidth or representation bottleneck. A random or learned pattern can improve connectivity while making retrieval less predictable. For a task requiring one fact near the start and one near the end, test whether the chosen pattern supports the necessary path, rather than relying on average perplexity alone.

Compare with dense and local-window baselines at matched model quality, context length, hardware, and batch size. Measure long-range recall, downstream accuracy, prefill/decode latency, memory traffic, and actual sparse-kernel utilization using [[measurement]]. Vary fact placement and sequence length. The broad pattern-selection concept is not equivalent to a particular hierarchical retrieval index or a universal linear-time guarantee.

## Sources

- [Child et al., Sparse Transformer](https://arxiv.org/abs/1904.10509): sparse factorizations of attention.
- [Beltagy et al., Longformer](https://arxiv.org/abs/2004.05150): local and global attention.
- [Zaheer et al., BigBird](https://arxiv.org/abs/2007.14062): local, global, and random attention.
