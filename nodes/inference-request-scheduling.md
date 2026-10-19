---
id: inference-request-scheduling
title: Inference Request Scheduling
summary: An inference request scheduler admits and batches prefill and decode work within KV-cache and latency limits rather than sending each API request directly to a GPU.
type: concept
tags: [ml/llm/inference]
prereqs: [prefill-vs-decode, llm-inference-memory-budget, continuous-batching, queue, chunked-prefill]
sources: [https://docs.vllm.ai/en/latest/configuration/optimization/, https://docs.vllm.ai/en/latest/design/paged_attention/, https://arxiv.org/abs/2309.06180]
status: explained
created: 2026-10-02
updated: 2026-10-20
---

# Inference Request Scheduling

## Summary

An **inference request scheduler** decides which waiting and active requests receive GPU work next. Admission, batching, and cache allocation couple latency and throughput: the next request cannot always run immediately merely because its model weights fit.

## Grounded explanation

An arriving request enters a [[queue]] with prompt length, generation limit, and service objective. [[prefill-vs-decode]] separates the large prompt computation from token-at-a-time generation. With [[continuous-batching]], a scheduler can batch active decode steps and admit new prefills when compute and KV capacity allow. Long prefills may delay decode tokens; too many active requests can exhaust the [[llm-inference-memory-budget]]. Paged KV allocation reduces waste, not the live cache bytes required by resident tokens.

Consider one long prompt arriving while short conversations are decoding. Running its entire prefill at once may improve immediate admission but raise inter-token latency for active users. Delaying it may improve those users' experience but increase its time to first token. Chunked prefill, admission limits, and priority policies are alternatives whose value depends on workload and fairness constraints. A scheduler also needs a defined response to cancellation, timeout, and memory pressure; an OOM is a failed admission policy, not merely a model-size fact.

Replay a representative mix of prompt lengths, output lengths, concurrency, and arrival bursts. Measure queue wait, time to first token, inter-token latency, p95 end-to-end latency, throughput, KV occupancy, preemptions, and OOMs. Compare policies under the same model, hardware, and quality settings. vLLM's documented paged attention and the PagedAttention paper ground the cache-allocation constraint; the best scheduling policy remains workload-dependent.

## Token budgets and recomputation preemption

A [[chunked-prefill]] scheduling iteration has both a work budget and a state-capacity constraint. In a decode-prioritizing chunked policy, each active ordinary decode may consume one scheduled token; unused token budget can go to prompt chunks. For a hypothetical 12-token budget with five one-token decodes, seven prompt tokens fit. A 20-token waiting prefill can consume seven now and continue later. This is a toy accounting example, not a promise about kernel duration or a universal scheduler order; speculative steps and other architectures can have different work units.

A token budget does not reserve all future KV growth. If live state no longer fits, the scheduler may preempt a request and later recompute its prefix, trading useful progress for temporary capacity. vLLM V1 documentation describes recomputation preemption and a decode-first chunked-prefill policy; verify the deployed version rather than inferring all engines use it. Admission caps, smaller token budgets, more cache capacity and parallelism can change pressure, with communication or latency costs. Measure preemptions, recomputed tokens, waiting time and tail latency, and validate cancellation and resumed output. Two stages sharing an iteration is not evidence that prefill and decode have identical execution semantics.

## Prerequisites

- [[prefill-vs-decode]]
- [[llm-inference-memory-budget]]
- [[continuous-batching]]
- [[queue]]

## Sources

- [vLLM Paged Attention design](https://docs.vllm.ai/en/latest/design/paged_attention/): KV-block allocation and reuse.
- [Kwon et al., Efficient Memory Management for Large Language Model Serving](https://arxiv.org/abs/2309.06180): memory management for serving.

- <https://docs.vllm.ai/en/latest/configuration/optimization/>
