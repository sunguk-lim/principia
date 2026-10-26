---
id: prefill-vs-decode
title: Prefill vs Decode
summary: Prefill constructs prompt state while decode extends generated state; token reuse, batch shape and context length determine their actual compute, memory and scheduling limits.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache, roofline-model]
sources: [https://github.com/vllm-project/vllm/blob/main/docs/configuration/optimization.md, https://huggingface.co/docs/transformers/cache_explanation, https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html]
status: explained
created: 2026-06-23
updated: 2026-10-27
---

# Prefill vs Decode

## Meaning

Prefill processes prompt tokens to construct the [[kv-cache]] used for generation. Decode extends that state with generated tokens. Their execution shapes often differ sharply, but neither phase has an unconditional compute-bound or memory-bound label.

## Mechanism

A prompt supplies many token positions together, allowing a dense layer to reuse weights across many activation rows. Ordinary one-token autoregressive decode has one new row per active request. That distinction can move the operations to different positions in the [[roofline-model]]. It does not establish measured saturation: short prompts, large decode batches, long attention contexts, sparse expert routing, data transfers and device-specific kernels change the outcome.

State the algorithm before counting. In a conventional decoder, processing the final prompt position already produces the distribution for the first output token. A subsequent decode forward pass consumes a sampled output token to produce the next distribution; a second complete weight pass is not inherently required merely to sample the first output. Speculative and multi-token methods have different schedules. Prompt processing can also be chunked across iterations rather than executed in one uninterrupted pass.

The cache avoids recomputing past keys and values, but attending to retained state still has a cost. For dense layers that do not fit in fast cache, weight reads can dominate a small decode batch. As the number of simultaneous requests grows, weights can be reused across more rows. Longer retained contexts can instead increase attention-state traffic. A sparse expert model touches selected experts rather than necessarily reading every expert weight on every step.

## Worked example

For an idealized dense matrix region containing one million sixteen-bit weights, one traversal of its weights is 2 MB. Suppose each token row requires approximately two million multiply/add operations and ignore activation and attention traffic for this illustration. One row then provides about one operation per weight byte. Sixty-four rows sharing that traversal provide about 128 million operations over 2 MB, or 64 operations/byte.

Those sixty-four rows could be prompt positions or sixty-four independent active decode requests. Both increase this layer's idealized weight reuse. They do not make the complete phases equivalent: cache lengths, causal attention, admission, output readiness and actual data movement differ. The example explains why phase names alone cannot identify a bottleneck.

## Validation and alternatives

Measure prompt length, output length, active-request batch and cached context alongside queueing, first-token and inter-token latency. Separate weight, attention-state, communication and launch costs with traces. Compare mixed-phase scheduling with bounded prompt chunks when long prompt work delays ongoing generation, accounting for chunk overhead and lost weight reuse. More concurrency can improve throughput while worsening per-request latency and cache demand. Verify quality and data residency before comparing timings; a headline phase label is not a diagnosis.

## Check your understanding

Is decode always bandwidth-bound because it produces one token? No. The batch contains rows from multiple requests, and context, architecture, kernel support and scheduling determine the actual limiting resource.

## Prerequisites

- [[kv-cache]]
- [[roofline-model]]

## Sources

- [vLLM optimization guide source](https://github.com/vllm-project/vllm/blob/main/docs/configuration/optimization.md): mixed-phase scheduling, prompt chunking, cache preemption and tuning trade-offs.
- [Hugging Face cache explanation](https://huggingface.co/docs/transformers/cache_explanation): prompt-forward output distribution and subsequent cached-token loop.
- [CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html): profiling, workload-dependent arithmetic/data movement and complete-path measurement. The numeric example is an independent idealized derivation.
