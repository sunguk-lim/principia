---
id: gpu-kernel-benchmarking
title: "GPU Kernel Benchmarking"
summary: "GPU kernel benchmarking measures a fixed operation and correctness contract under explicit shapes, timing boundaries and execution state rather than extrapolating a best-case speedup."
type: concept
tags: [gpu]
prereqs: [measurement, cuda-stream, roofline-model]
sources: [https://docs.pytorch.org/docs/2.15/benchmark_utils.html]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# GPU Kernel Benchmarking

## Meaning

A kernel benchmark measures one operation under declared conditions. It answers a narrower question than application throughput: a faster attention kernel does not by itself establish a faster serving system. Correctness, inputs and timing boundaries define what is being compared.

## Mechanism

Specify shapes, strides, masks, dtype, device, software revision and tolerances. Establish correctness against a suitable independent reference, then perform warmup and repeated timings. [[cuda-stream]] execution is asynchronous: a host call can return before device work ends. Synchronize the measured boundary or use correctly placed device events, stating whether dispatch, data transfer, compilation and allocation are included. PyTorch's benchmark Timer documents warmup, thread control, accelerator synchronization and repeated measurements.

Use [[measurement]] to preserve replicates and variation rather than only the minimum. Distinguish warm-cache from cold-cache conditions and report the clock, thermal and concurrent-load context when relevant. The [[roofline-model]] can guide whether traffic or arithmetic plausibly limits performance, but a claimed bottleneck needs profiling evidence at the actual shape. Different attention phases and batch sizes can have different limits.

## One example

A fictional host timer reports 8 microseconds for enqueueing kernel A and 6 for B. Device-completion timings instead show 80 and 120 microseconds. B enqueues faster but computes more slowly; the two boundaries answer different questions. If a first invocation adds 5 ms of compilation, excluding it is reasonable for a steady-state benchmark only when that exclusion is explicit. A cold-start application must still account for it.

## Check your understanding

Can the maximum speedup over a shape sweep describe all requests? No. Publish per-shape results, numerical failures and a workload-weighted comparison, including shapes with regressions. Compare equally capable baselines and distinguish kernel time from end-to-end time. A valid local result establishes neither universal memory-boundedness nor a guaranteed application speedup.

## Prerequisites

- [[measurement]]
- [[cuda-stream]]
- [[roofline-model]]

## Sources

- <https://docs.pytorch.org/docs/2.15/benchmark_utils.html>
