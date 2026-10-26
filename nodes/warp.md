---
id: warp
title: Warp
summary: A warp groups 32 CUDA threads for SIMT execution with active-lane masks; divergence and independent thread scheduling require explicit synchronization rather than unconditional lockstep assumptions.
type: concept
tags: [gpu]
prereqs: [streaming-multiprocessor]
sources: [https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html, https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html]
status: explained
created: 2026-06-23
updated: 2026-10-27
---

# Warp

## Meaning

A warp groups 32 CUDA threads on a [[streaming-multiprocessor]] for single-instruction, multiple-thread (SIMT) execution. Each thread has its own state and logical lane number. Instructions execute with an active-lane mask, so not every thread necessarily participates. A warp is not a promise that all 32 threads physically execute every instruction on the same clock cycle.

## Mechanism

Threads that follow the same control path can share instruction issue while applying the instruction to their own values. If a branch sends threads down different paths, the corresponding instructions execute with different masks. This divergence can reduce useful work per issued instruction. It does not establish a universal two-times slowdown: path lengths, compiler predication, instruction throughput, memory stalls and other ready warps all affect elapsed time. A lane outside the active mask does not perform that instruction's logical operation; no claim about its detailed electrical behavior follows.

On NVIDIA devices with compute capability below 7.0, a warp used one shared program counter and an active mask. Starting at capability 7.0, independent thread scheduling maintains per-thread execution state and permits divergence/reconvergence below whole-warp granularity. The SIMT grouping still matters, but old code that assumed implicit lockstep for inter-thread data exchange can be wrong. Use the documented synchronization and participation masks for the actual cooperating threads. Merely belonging to one warp is not a memory-ordering or data-visibility guarantee.

## Worked example

Take lanes 0 through 31. Lanes below 16 take path A, and the rest take path B. Suppose A has four abstract issue steps and B has twelve, and assume a simple serial masked-path model with no overlap or stalls. Then four steps have 16 active lanes and twelve have the other 16. Useful lane-steps total 16*4 + 16*12 = 256; available lane-steps are 32*(4+12) = 512, so useful participation is 50% in this toy model.

That calculation is utilization accounting, not a wall-time benchmark. It does not prove a two-times runtime ratio against an unspecified alternative. Regrouping input so whole warps follow one path can change instruction issue, but can also require extra movement or change locality and scheduling. Measure those costs rather than declaring the penalty eliminated for free.

## Validation and alternatives

Test branch-heavy and uniform inputs, short and long paths, tail groups and the intended target architecture. For inter-thread communication, verify the synchronization primitive's mask and memory-ordering contract rather than rely on observed lockstep in one run. Profile instruction issue, active participation and stalls alongside complete kernel time. Alternatives include grouping similar work, predication, a different decomposition or leaving a branch unchanged when rearrangement costs more than it saves.

## Check your understanding

Can two threads safely exchange data without synchronization just because they share a warp? Not in general. Architecture, participation and the documented synchronization contract matter.

## Prerequisites

- [[streaming-multiprocessor]]

## Sources

- [CUDA programming model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html): warps, lanes and SIMT masks.
- [CUDA advanced kernel programming](https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html): independent thread scheduling and explicit synchronization.
