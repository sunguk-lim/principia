---
id: cuda-graph-replay
title: CUDA Graph Replay for Inference
summary: CUDA graph replay reduces repeated host launch work by capturing a compatible device-operation sequence, trading flexibility and memory for lower launch overhead.
type: concept
tags: [gpu]
prereqs: [cuda-kernel, cuda-stream, prefill-vs-decode, llm-inference-memory-budget]
sources: [https://docs.pytorch.org/docs/2.14/notes/cuda.html#cuda-graphs, https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__GRAPH.html, https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html]
status: explained
created: 2026-10-16
updated: 2026-10-26
---

# CUDA Graph Replay for Inference

## Summary

A **CUDA graph** captures an execution path of device work and dependencies, then replays it with less repeated host submission overhead. The operations do not become intrinsically faster.

## Grounded explanation

In eager execution, the CPU enqueues each [[cuda-kernel]] and transfer. A decode iteration may contain many short kernels; the GPU can finish one before the host submits the next. A timeline then shows idle launch gaps even when each kernel has improved. CUDA graph replay submits a captured sequence through a smaller host path. Dependencies and [[cuda-stream]] ordering are part of the capture.

Graph replay is useful only when the execution structure is compatible with the captured path. PyTorch documents static shapes and stable memory addresses as important constraints, along with warm-up and capture on a separate stream. Inputs can change through stable buffers, but changing shapes, data-dependent control flow, allocations, or synchronization may require a different graph or eager execution. Captured graphs reserve resources, so the number of shape variants contributes to the [[llm-inference-memory-budget]].

For LLM inference, [[prefill-vs-decode]] matters: long prefill kernels may already dominate host launch time, while repeated decode steps with small active batches can be launch-bound. A server can capture several common batch or shape buckets, pad into a compatible bucket, or fall back to eager execution. Padding spends device work; more captures spend startup time and memory. Neither policy is universally best.

Before enabling graphs, profile host launch time, GPU idle gaps, kernel time, queueing, and synchronization under the live request mix. Compare eager and replay paths at the same model, precision, output quality, batch distribution, and hardware. Report prefill and decode separately, p50/p95 inter-token latency, throughput, peak memory, warm-up cost, and graph coverage. If GPU kernels dominate end-to-end time, replay alone has little headroom; if numerical or shape behavior changes, correctness outranks a small latency gain.

## Replay data, update rules, and amortization

Capture records eligible operations; it is not a completed forward-pass result. In PyTorch stream capture, the captured GPU operations are recorded rather than executed at that moment. After instantiation, each replay executes them on the current contents of the retained buffers. Warm up eagerly first to initialize libraries and allocations, using the documented side-stream ordering. Keep input and output tensors alive for the graph's lifetime. Rebinding a Python variable to a new tensor does not redirect a captured pointer. Copy fresh inputs into the retained storage before launch, and do not overwrite output storage before its consumer finishes.

Do not generalize the fixed-argument PyTorch replay contract into a claim that CUDA can never change graph parameters. CUDA's lower-level executable-graph update APIs permit supported parameter changes with compatibility checks; topology or node-type changes can require re-instantiation. Updating a scalar or pointer through those APIs is different from mutating data already stored at a fixed pointer. Check update results and use re-instantiation or eager fallback when unsupported. CPU-side work is not automatically replayed; host-dependent branches need an explicitly supported mechanism rather than a Python branch assumed to rerun. Random-number state must also follow the framework's graph-safe contract.

Consider a hypothetical measured decode interval: eager execution takes 120 microseconds, including 80 microseconds of device work and 40 of attributable submission gaps. Replay takes 88, including the same 80 of device work and 8 of remaining gaps. The saving is 32 microseconds, not 40, and the idealized speed ratio is 120/88, about 1.36. If warm-up, capture and instantiation add 8 milliseconds, they cost 8,000 microseconds. Equal total time occurs after 8,000/32=250 replays; only more replays win under these fixed assumptions. Include input-copy, synchronization and output-consumption costs in both measured paths. These are illustrative timings, not a hardware benchmark.

Buckets also change the denominator. A batch of 5 routed to a captured batch of 8 has 3 padded slots: 3/8=37.5% of those slots are inactive, though runtime need not scale linearly with slot count. More buckets reduce padding but can reserve extra graph-pool memory and increase preparation time. Measure the actual batch distribution, eager fallbacks and peak memory, not only the fastest captured shape. Compare replay with kernel fusion separately: packaging existing launches and changing the device operations are different interventions.

## Prerequisites

- [[cuda-kernel]]
- [[cuda-stream]]
- [[prefill-vs-decode]]
- [[llm-inference-memory-budget]]

## Sources

- [PyTorch CUDA semantics, CUDA graphs](https://docs.pytorch.org/docs/2.14/notes/cuda.html#cuda-graphs): capture, replay, address and shape constraints.
- [NVIDIA CUDA Runtime graph management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__GRAPH.html): graph execution API.

- <https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html>
