---
id: gpu-allocation-fragmentation
title: GPU Allocation Fragmentation
summary: "An allocator can reserve device memory yet fail a new request when free capacity is split or bound in unusable blocks."
type: concept
tags: [ml/systems]
prereqs: [gpu-memory-spaces, training-memory-budget]
sources: [https://docs.pytorch.org/docs/2.14/notes/cuda.html]
status: explained
created: 2026-10-09
updated: 2026-10-09
---

# GPU Allocation Fragmentation

## Summary

A GPU workload can have enough free bytes in aggregate but still fail an allocation because the available blocks cannot satisfy its requested size under the allocator's policy. **GPU allocation fragmentation** is one cause; live tensors, cached blocks, library workspaces, and external processes are other causes. Model parameter size alone does not determine peak memory.

## Grounded explanation

The [[training-memory-budget]] includes parameters, optimizer states, gradients, activations, temporary workspaces, and allocator overhead. A caching allocator reserves blocks from device memory and reuses them to avoid expensive allocation calls. If a sequence of different-size requests leaves free capacity spread across blocks or pools, a later large request may not fit without coalescing or releasing reservations. Internal fragmentation wastes space *inside* a granted block; external fragmentation leaves separate free regions that cannot satisfy one request. The physical device, allocator, and CUDA semantics can each impose different limits, so the simplistic claim that every failure means one contiguous physical region is unavailable is unsafe.

In PyTorch, distinguish `memory_allocated` (live tensor allocations) from `memory_reserved` (memory held by its caching allocator). Compare peak allocated and reserved values, allocator snapshots, external process use, and the size/timing of the failing request. A high reserved-minus-allocated gap can motivate inspecting fragmentation, but it is not proof by itself. `empty_cache` releases *unoccupied cached* blocks for other uses; it cannot free live tensors and is not a general fix for insufficient model capacity.

To validate a proposed mitigation, replay the same batch, sequence lengths, checkpointing policy, and allocation trace. Measure peak live bytes, peak reserved bytes, allocation failures, and runtime before and after tuning pool settings, reducing transient peaks, or changing batch shape. Do not reuse a newsletter's fixed percentage of waste across workloads.

## Prerequisites

- [[gpu-memory-spaces]]
- [[training-memory-budget]]

## Sources

- [PyTorch CUDA semantics—memory management](https://docs.pytorch.org/docs/2.14/notes/cuda.html#memory-management): caching allocator, allocated/reserved metrics, and diagnostics.
