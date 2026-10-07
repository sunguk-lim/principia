---
id: chunked-prefill
title: Chunked Prefill
summary: Chunked prefill schedules a long prompt across multiple token-budgeted iterations so active decode requests need not wait for one uninterrupted prompt-processing step.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache, transformer-attention, continuous-batching]
sources: [https://docs.vllm.ai/en/latest/configuration/optimization.html]
status: explained
created: 2026-06-23
updated: 2026-10-08
---

# Chunked Prefill

## Summary

**Chunked prefill** splits a long prompt across serving iterations so the scheduler can interleave its processing with active decode requests. It changes *when* prompt tokens are processed, not the semantic intent of the prompt. The important trade-off is between time to first token for the newly arrived request and inter-token latency for requests already decoding.

## Grounded explanation

In [[continuous-batching]], an iteration may contain decode tokens from running requests and prompt tokens from new ones. Without chunking, a long prefill can occupy a large iteration and delay the next output token for every active stream. A token budget bounds how much prefill joins an iteration. Causal [[transformer-attention]] lets a later prompt chunk read prior chunks' [[kv-cache]] state; the serving implementation must preserve positions, masks, and state across chunk boundaries.

vLLM's V1 optimization guide documents a decode-priority policy: pending decode requests are scheduled first, then available capacity under `max_num_batched_tokens` is used for prefill; a prefill that does not fit is chunked. It reports that smaller token budgets can improve inter-token latency, while larger budgets can improve time to first token and throughput on some hardware. The parameter is a per-iteration *token budget*, not necessarily a fixed per-request chunk size. Actual behavior depends on version, batch mix, model, attention backend, and available cache memory.

For example, if an active request is streaming while a 32K-token prompt arrives, scheduling the entire new prompt at once can produce a visible pause. Several shorter prefill iterations can give the active stream opportunities to decode. The arriving request still waits until all of its prompt has been processed before it can emit a first token, and extra chunk boundaries can add scheduling or cache-read overhead. Neither every prefill nor every decode is universally compute- or memory-bound; arithmetic intensity changes with sequence length, batch, and hardware.

Chunking preserves the *causal dependency structure* for a correctly implemented model, but different kernel shapes and floating-point reduction orders can produce numerical differences. It is therefore wrong to promise bit-identical outputs merely from causality. Validate masks/positions and output quality against an unchunked reference with tolerances, then sweep the token budget under representative prompt/output lengths and concurrency. Measure time to first token, inter-token latency distributions, throughput, peak cache use, and starvation. Prefer the simplest scheduler that meets the service objective rather than assuming smaller chunks are always better.

## Sources

- [vLLM, Optimization and Tuning — Chunked Prefill](https://docs.vllm.ai/en/latest/configuration/optimization.html): V1 decode-priority scheduling and `max_num_batched_tokens` trade-offs.
