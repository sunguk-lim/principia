---
id: transformer-xl-segment-recurrence
title: Transformer-XL Segment Recurrence
summary: Transformer-XL reuses detached hidden states from prior segments to extend the effective dependency path beyond a fixed training segment without attending to all earlier tokens at once.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, positional-encoding, context-window]
sources: [https://arxiv.org/abs/1901.02860]
status: explained
created: 2026-10-16
updated: 2026-10-16
---

# Transformer-XL Segment Recurrence

## Summary

**Transformer-XL** processes text in segments and reuses hidden states from an earlier segment as memory for the next one. Relative position handling lets this recurrence represent cross-segment order without reusing an absolute index as if it began again.

## Grounded explanation

A standard [[transformer-attention]] block trained on isolated fixed-length segments cannot directly attend to a preceding segment. Transformer-XL stores the previous segment's layer states and makes them visible as keys and values when computing the current segment. The cached states are detached from the current gradient path, keeping training backpropagation bounded; nevertheless, forward information can flow across segment boundaries. Its primary paper describes both this recurrence and relative positional encoding.

For segment length $L$ and cached length $M$, each current token attends over at most the current and retained prior states, not over an unbounded full history. The per-segment attention work therefore depends on $L(L+M)$; total work for a growing document is approximately linear in the number of segments when $L$ and $M$ stay fixed. Calling this “unlimited context” is misleading: the direct cache remains bounded and information from much older text must survive through transformed hidden states. A model may forget or blur details even when it can process arbitrarily many segments sequentially.

This is different from sliding-window attention, which exposes nearby prior tokens, and from external retrieval, which can select distant content by a query. The recurrence has no external index and no guarantee that a specific old fact remains recoverable. [[positional-encoding]] matters because reusing segment positions naively would confuse order. [[context-window]] still bounds directly visible states on one step.

Validate on controlled long-range dependency tasks with evidence placed at increasing distances, not only on short perplexity. Compare fixed-window, sliding-window, and recurrence models at matched parameters, compute, and memory. Track retrieval accuracy by distance, throughput, peak memory, and errors after segment boundaries. Do not infer a modern production model's architecture from its advertised context length.

## Prerequisites

- [[transformer-attention]]
- [[positional-encoding]]
- [[context-window]]

## Sources

- [Dai et al., Transformer-XL](https://arxiv.org/abs/1901.02860): segment-level recurrence and relative positional treatment.
