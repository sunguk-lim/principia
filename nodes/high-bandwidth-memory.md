---
id: high-bandwidth-memory
title: High-Bandwidth Memory
summary: High-bandwidth memory stacks DRAM dies behind a wide interface near an accelerator, increasing aggregate transfer capacity without making memory capacity, bandwidth and access latency interchangeable.
type: concept
tags: [gpu/memory]
prereqs: [memory-hierarchy]
sources: [https://www.micron.com/products/memory/hbm, https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/]
status: explained
created: 2026-10-27
updated: 2026-10-27
---

# High-Bandwidth Memory

## Meaning

High-bandwidth memory (HBM) is a stacked main-memory technology used beside many accelerators. Multiple dynamic-memory dies are stacked vertically and connected through the silicon and small inter-die contacts. A wide interface provides many simultaneous data-transfer paths. HBM occupies the large, off-chip tier of the [[memory-hierarchy]]; it is not the processor's on-chip register file or cache.

## Mechanism

The design combines vertical storage density with a very wide connection to the processor. Think of a transfer path as a set of lanes, each carrying bits at a stated rate. Aggregate ideal bandwidth is lane count times bits per second per lane, divided by eight to express bytes per second. More independent stacks can increase aggregate width and capacity, subject to the actual controllers, packaging and power limits.

This does not make a single dependent memory request instantaneous. Capacity says how many bytes fit; bandwidth says how many bytes can move per second; access latency says how long a particular request waits. A program with independent transfers can use many paths, while a dependent pointer sequence may leave most of them idle. Caches can prevent some transfers altogether, so report which level's traffic is measured.

## Worked example

Use hypothetical decimal units, not a product specification. Suppose four stacks each provide 16 GB of capacity and sustain 0.5 TB/s on an appropriate streaming workload. They offer 64 GB total capacity and at most 2 TB/s aggregate measured streaming bandwidth under those assumptions. Reading 8 GB once has a bandwidth floor of 8/2000 seconds = 4 milliseconds. It is not a prediction of complete execution time: arithmetic, dependencies, cache behavior and contention remain. A 70 GB working set does not fit merely because the interface is fast; a 4 GB working set can still run slowly if access is serial or most time is elsewhere.

## Validation and alternatives

Check the exact device and board variant: even the original H100 SXM and PCIe descriptions use different HBM generations and active-resource configurations. Measure sustained bandwidth with the relevant access pattern, not a peak data-sheet number. Include read/write mix, locality, concurrency, power and the achieved memory footprint. Compare with a smaller cached working set, reduced numeric storage, or a different device rather than assuming every workload needs maximum HBM capacity. Vendor product speedups are workload-specific claims, not consequences of stacking alone.

## Check your understanding

Does twice the HBM capacity imply twice the token rate? No. Capacity and transfer rate are separate, and neither proves the application's limiting stage.

## Prerequisites

- [[memory-hierarchy]]

## Sources

- [Micron HBM overview and FAQ](https://www.micron.com/products/memory/hbm): stacked DRAM, through-silicon connections and wide interfaces. Marketing comparison figures are not used here.
- [NVIDIA Hopper architecture](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/): HBM stacks, cache and board-specific memory configurations.
