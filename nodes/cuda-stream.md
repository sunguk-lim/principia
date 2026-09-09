---
id: cuda-stream
title: CUDA Stream
summary: A CUDA stream is an ordered queue of device work whose operations execute in issue order while independent streams may overlap when dependencies and hardware permit.
type: concept
tags: [gpu]
prereqs: [cuda-kernel, thread-synchronization]
sources: [https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__STREAM.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# CUDA Stream

## Summary

A **CUDA stream** is an ordered sequence of asynchronous device operations. Work submitted to one stream is ordered; work in different streams may run concurrently when dependencies, resources, and the device allow it.

## Grounded explanation

Kernel launches, memory copies, events, and host callbacks can be enqueued into a stream. If operations $A$ then $B$ enter the same stream, $B$ does not begin before the ordering requirements of $A$ are satisfied. Different streams have no such implicit total order.

Overlap is conditional. A copy may overlap a [[cuda-kernel]] only when the transfer type, memory placement, copy engine, device capability, and absence of dependencies permit it. Two kernels may serialize because they exhaust compute or memory resources even when placed in separate streams.

Events express cross-stream dependencies without forcing the host to wait: record an event after producing data in one stream, then make another stream wait on it before consuming that data. Broad device or stream synchronization is simpler but can erase intended concurrency. This is related to [[thread-synchronization]], but stream order governs queued device operations rather than CPU thread execution.

The default stream has configuration-dependent synchronization semantics, so code should not assume that it is independent of every nondefault stream. Host callbacks also block later work in their stream while running and must obey CUDA’s restrictions.

Validate a pipeline with a GPU timeline, not enqueue timestamps. Compare end-to-end throughput and latency after warm-up, verify outputs, and inspect copy/kernel overlap, idle gaps, synchronization calls, and resource saturation. More streams add scheduling and memory-lifetime complexity and cannot improve a workload with no independent work.

## Prerequisites

- [[cuda-kernel]]
- [[thread-synchronization]]

## Sources

- [NVIDIA, CUDA Runtime API — Stream Management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__STREAM.html): stream creation, ordered asynchronous operations, events, callbacks, synchronization, and default-stream behavior.
