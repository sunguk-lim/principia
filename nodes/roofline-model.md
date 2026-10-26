---
id: roofline-model
title: Roofline Model
summary: The roofline model bounds operation rate by the smaller of a compatible compute ceiling and memory bandwidth times arithmetic intensity; measured points below the roof require further diagnosis.
type: concept
tags: [ml/llm/inference]
prereqs: [arithmetic-intensity, memory-hierarchy]
sources: [https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html#roofline-charts]
status: explained
created: 2026-06-23
updated: 2026-10-27
---

# Roofline Model

## Meaning

The roofline model combines arithmetic and data movement into a performance envelope. It is an upper-bound model under stated counting and hardware assumptions, not a proof that a real workload reaches the roof or that every low-intensity workload saturates memory bandwidth.

## Mechanism

Let W be work counted in floating-point operations and D be transferred bytes at a specified memory level. Their ratio I=W/D is [[arithmetic-intensity]], in operations per byte. Let P be a compatible compute ceiling in operations per second and B the memory-level bandwidth in bytes per second. The operation rate R obeys the modeled bound

$$R \leq \min(P, B I).$$

Why the minimum? Completing W operations needs at least W/P seconds of arithmetic capability; moving D bytes needs at least D/B seconds. Even assuming ideal overlap, elapsed time cannot be smaller than the larger requirement. Dividing W by that time gives the smaller rate ceiling. The ridge occurs at I=P/B, where the two ceilings agree.

The [[memory-hierarchy]] makes the memory level essential. A cache-level roof uses traffic and bandwidth at that cache, while a main-memory roof uses main-memory traffic. Do not combine ideal algorithmic bytes, cache bandwidth and unrelated measured operations into one point. Compute format and operation conventions must also match: scalar versus matrix arithmetic, supported numeric format, sparsity and whether a multiply-add counts as two operations affect the ceiling.

## Worked example

Take hypothetical P=100 trillion operations/s and B=3 trillion bytes/s. The ridge is 100/3, about 33.3 operations/byte. An element-wise add reads two four-byte values and writes one: one operation over 12 useful bytes, so I=1/12. Its modeled bandwidth ceiling is 3 trillion /12 = 0.25 trillion operations/s.

For an n-by-n matrix product with n=4096, assume approximately 2*n^3 operations and an idealized one-read/one-write total of three n-by-n four-byte arrays. Intensity is 2*n^3/(12*n^2)=n/6, about 682.7 operations/byte. Its modeled ceiling is the 100-trillion compute roof. The 400-times ratio between these two ceilings compares different operations' rate ceilings, not the runtimes or measured speedups of two programs.

If a measured add achieves only 0.05 trillion operations/s, it is five times below its 0.25-trillion roof. That gap still needs explanation: limited parallelism, small problem size, launch cost, access pattern, dependencies or measurement scope can matter. Replacing memory with a faster interface is not proven sufficient by the point's horizontal position.

## Validation and alternatives

Use matched measured work and traffic, a documented format-specific ceiling and sustained bandwidth appropriate to the device and access pattern. Inspect achieved bandwidth, instruction issue, stalls and occupancy rather than label a workload bound solely from its intensity. A low-intensity kernel may benefit from fusion or locality; a high-intensity kernel below the roof may benefit from better tiling or more parallel work without changing hardware. Profile the application separately to determine whether the kernel's time is consequential at all.

## Check your understanding

Does lying left of the ridge prove that memory bandwidth is saturated? No. It identifies the tighter modeled ceiling; the observed point can be far below it for other reasons.

## Prerequisites

- [[arithmetic-intensity]]
- [[memory-hierarchy]]

## Sources

- [NVIDIA Nsight Compute roofline charts](https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html#roofline-charts): compatible compute/memory ceilings, arithmetic intensity and achieved points. Numerical examples are independent derivations of the envelope.
