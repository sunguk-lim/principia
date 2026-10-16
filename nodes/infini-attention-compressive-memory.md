---
id: infini-attention-compressive-memory
title: Infini-Attention Compressive Memory
summary: Infini-attention combines local segment attention with a bounded compressive memory updated across segments, trading exact remote token access for constant-size accumulated context.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, transformer-xl-segment-recurrence, linear-transformer-attention]
sources: [https://arxiv.org/abs/2404.07143]
status: explained
created: 2026-10-16
updated: 2026-10-16
---

# Infini-Attention Compressive Memory

## Summary

**Infini-attention** combines attention within a current segment with a compressive memory summarizing prior segments. The memory has bounded size even as the number of processed tokens grows.

## Grounded explanation

Full attention to all old tokens grows with sequence length. [[transformer-xl-segment-recurrence]] keeps a finite recent segment state; a memorizing transformer instead retrieves particular old key–value entries. Infini-attention's primary paper proposes a different path: accumulate information from previous segments into a fixed-size associative memory, then combine its retrieved signal with local attention for the current segment. This is related to the fixed-size state used by [[linear-transformer-attention]], but coupled to ordinary local attention so near context can still be represented directly.

Bounded storage is not unlimited fidelity. Compression maps many old contexts into the same finite state; collisions, overwriting, and the learned query representation govern what survives. A long input can be processed in sequence without retaining every token, yet a precise old string or rare exception may no longer be recoverable. The method therefore changes the memory–accuracy trade-off rather than abolishing the [[transformer-attention]] cost of local work.

For evaluation, place controlled facts and distractors at increasing distances. Measure exact retrieval and downstream task quality, not just the largest sequence the implementation accepts. Compare matched local-window, segment-recurrence, external retrieval, and compressive-memory variants at the same model size and compute. Record memory growth, prefill/decode time, interference from later segments, and failure on contradictory updates. A newsletter's context-window or memory-size figures are not independent evidence for the mechanism or for any provider deployment.

## Prerequisites

- [[transformer-attention]]
- [[transformer-xl-segment-recurrence]]
- [[linear-transformer-attention]]

## Sources

- [Munkhdalai et al., Infini-attention](https://arxiv.org/abs/2404.07143): local attention plus bounded compressive memory.
