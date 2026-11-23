---
id: gpu-kernel-benchmarking
title: "GPU Kernel Benchmarking"
summary: "GPU kernel benchmarking measures a fixed operation and correctness contract under explicit shapes, timing boundaries and execution state rather than extrapolating a best-case speedup."
type: concept
tags: [gpu]
prereqs: [measurement, cuda-stream, roofline-model]
sources: [https://docs.pytorch.org/docs/2.15/benchmark_utils.html, https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html, https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html]
status: explained
created: 2026-11-09
updated: 2026-11-24
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


## Controlled comparisons across streams, caches and time

Record start and stop events on the stream whose work is measured, wait for completion of the stop event, and read the device elapsed interval. If the operation dispatches work into other streams, make the measured completion depend on that work or explicitly exclude it. A synchronized host interval instead measures a declared end-to-end boundary. Device events do not remove contention, and profiler replay can change concurrency, cache state and clocks; do not treat profiler-instrumented host timing as an unperturbed application measurement.

Warmup must match the shapes and implementation, not merely initialize any kernel once. Define hot-cache, cold-cache or production-like reuse before comparing. For an invented pair, A takes 40 microseconds hot and 90 cold, while B takes 60 hot and 70 cold. A wins the hot experiment; B wins the cold one. Neither row can represent production without its reuse distribution. Buffer rotation or explicit eviction can test different conditions, but flushing is not automatically the realistic policy. Inspect a benchmark helper's version and cache policy rather than assuming its name guarantees eviction. Nsight documents replay cache controls and explains why profiler defaults can differ from natural execution.

Interleave or randomize paired A/B trials so all of A is not compared with B after a temperature or clock shift. Preserve the pair, trial order, elapsed times and contemporaneous load. A toy pair with A=100 and B=90 microseconds and a later pair with A=200 and B=180 both favor B by 10%, despite a twofold environment shift. Pairing helps temporal comparability but does not eliminate noisy neighbors or correlations across trials. Prefer an isolated device where available, report median and relevant tails with uncertainty, and choose repetitions based on the precision needed rather than a universal 100-run rule. If the measured difference is unresolved at the experiment's noise level, report that limitation instead of selecting the lower sample mean.

## Prerequisites

- [[measurement]]
- [[cuda-stream]]
- [[roofline-model]]

## Sources

- <https://docs.pytorch.org/docs/2.15/benchmark_utils.html>

- <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html>

- <https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html>
