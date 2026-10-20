---
id: amdahls-law
title: Amdahl's Law
summary: Amdahl's law bounds fixed-workload speedup by the fraction of original elapsed work an optimization can actually accelerate.
type: concept
tags: [computing/performance]
prereqs: [arithmetic, measurement]
sources: [https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/]
status: explained
created: 2026-10-21
updated: 2026-10-21
---

# Amdahl's Law

## Meaning

Amdahl's law connects a component speedup to whole-program speedup for a fixed workload. Making one component arbitrarily fast cannot remove time spent elsewhere.

## Mechanism

Let T be original elapsed time, f the fraction of that time accelerated, and s the speedup of that fraction. Assume the remaining work is unchanged, accelerated and unaccelerated durations add, and the optimization adds no overhead. [[arithmetic]] gives new time T_new=T(1-f)+Tf/s, and whole-program speedup S=T/T_new:

$$S=\frac{1}{(1-f)+f/s}.$$

As s grows without bound, the speedup approaches 1/(1-f), provided f<1. This is a limit for the stated decomposition, not a prediction from GPU utilization or operation counts. Estimate f with representative [[measurement]], including the actual critical path. CPU and device times that overlap cannot be blindly added as sequential fractions.

If the optimization introduces overhead h expressed as a fraction of original time, the denominator becomes (1-f)+f/s+h. Workload growth, changed algorithms, changed quality or newly overlapping stages need a different model rather than silently reusing the fixed-workload formula. NVIDIA's CUDA guidance uses Amdahl's and Gustafson's laws to set acceleration expectations before kernel work.

## Worked example

An inference request takes 100 ms: a targeted kernel accounts for 40 ms of nonoverlapping critical-path work and everything else takes 60 ms. Doubling the kernel speed gives 20+60=80 ms, or 100/80=1.25 times whole-request speedup, not two times.

Even a zero-time kernel leaves 60 ms, limiting improvement to 100/60, about 1.67 times. If the faster implementation adds 10 ms of transfers, total time is 90 ms and speedup is only about 1.11 times. These are illustrative inputs, not measurements of a particular engine. Reprofile after the change because a different stage can become limiting.

## Check your understanding

**Question:** Can a two-times kernel speedup establish two-times serving throughput? **Answer:** No. Determine its elapsed-time contribution, overhead, overlap and the serving bottleneck first.

## Prerequisites

- [[arithmetic]]
- [[measurement]]

## Sources

- <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/>
