---
id: cuda-graph-replay
title: CUDA Graph Replay for Inference
summary: CUDA graph replay reduces repeated host launch work by capturing a compatible device-operation sequence, trading flexibility and memory for lower launch overhead.
type: concept
tags: [gpu]
prereqs: [cuda-kernel, cuda-stream, prefill-vs-decode, llm-inference-memory-budget]
sources: [https://docs.pytorch.org/docs/2.14/notes/cuda.html#cuda-graphs, https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__GRAPH.html]
status: explained
created: 2026-10-16
updated: 2026-10-16
---

# CUDA Graph Replay for Inference

## Summary

A **CUDA graph** captures an execution path of device work and dependencies, then replays it with less repeated host submission overhead. The operations do not become intrinsically faster.

## Grounded explanation

In eager execution, the CPU enqueues each [[cuda-kernel]] and transfer. A decode iteration may contain many short kernels; the GPU can finish one before the host submits the next. A timeline then shows idle launch gaps even when each kernel has improved. CUDA graph replay submits a captured sequence through a smaller host path. Dependencies and [[cuda-stream]] ordering are part of the capture.

Graph replay is useful only when the execution structure is compatible with the captured path. PyTorch documents static shapes and stable memory addresses as important constraints, along with warm-up and capture on a separate stream. Inputs can change through stable buffers, but changing shapes, data-dependent control flow, allocations, or synchronization may require a different graph or eager execution. Captured graphs reserve resources, so the number of shape variants contributes to the [[llm-inference-memory-budget]].

For LLM inference, [[prefill-vs-decode]] matters: long prefill kernels may already dominate host launch time, while repeated decode steps with small active batches can be launch-bound. A server can capture several common batch or shape buckets, pad into a compatible bucket, or fall back to eager execution. Padding spends device work; more captures spend startup time and memory. Neither policy is universally best.

Before enabling graphs, profile host launch time, GPU idle gaps, kernel time, queueing, and synchronization under the live request mix. Compare eager and replay paths at the same model, precision, output quality, batch distribution, and hardware. Report prefill and decode separately, p50/p95 inter-token latency, throughput, peak memory, warm-up cost, and graph coverage. If GPU kernels dominate end-to-end time, replay alone has little headroom; if numerical or shape behavior changes, correctness outranks a small latency gain.

## Prerequisites

- [[cuda-kernel]]
- [[cuda-stream]]
- [[prefill-vs-decode]]
- [[llm-inference-memory-budget]]

## Sources

- [PyTorch CUDA semantics, CUDA graphs](https://docs.pytorch.org/docs/2.14/notes/cuda.html#cuda-graphs): capture, replay, address and shape constraints.
- [NVIDIA CUDA Runtime graph management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__GRAPH.html): graph execution API.
