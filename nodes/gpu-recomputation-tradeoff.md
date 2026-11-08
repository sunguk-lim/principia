---
id: gpu-recomputation-tradeoff
title: "GPU Recomputation–Memory Trade-off"
summary: "GPU recomputation trades repeated arithmetic for reduced storage or transfer of intermediates, and wins runtime only when the avoided memory cost exceeds added work and execution overhead."
type: concept
tags: [gpu]
prereqs: [roofline-model, activation-checkpointing]
sources: [https://arxiv.org/abs/2205.14135, https://arxiv.org/abs/1604.06174]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# GPU Recomputation–Memory Trade-off

## Meaning

Saving every intermediate avoids repeated arithmetic but can create costly memory traffic or exceed capacity. Recomputation regenerates selected values when needed. Its objectives can be lower peak storage, faster execution or a larger feasible workload; those are distinct benefits and need not occur together.

## Mechanism

The [[memory-hierarchy]] makes the location and lifetime of a value matter. Compare the transfers and storage avoided with the extra operations, dependencies and resource pressure introduced. The [[roofline-model]] provides a conditional performance bound from arithmetic intensity, compute throughput and bandwidth; it is not an exact runtime predictor. A method moving fewer bytes can still be slower if it reduces occupancy or adds synchronization.

[[activation-checkpointing]] applies this principle across a training computation graph. IO-aware attention instead coordinates tiled computation, compact summaries and, in its backward algorithm, regeneration of attention intermediates rather than saving a full quadratic matrix. These mechanisms share a trade-off but are not identical APIs. Rescaling arithmetic alone does not prove that every FlashAttention version performs more total operations than every baseline in every phase.

## One example

In an invented bandwidth-limited step, storing and later reading an intermediate costs 200 MB of traffic. At an achieved 100 GB/s, that transfer alone takes about 2 ms. Suppose regenerating it costs 10 million operations at an achieved 100 billion operations/s: .1 ms. If added dependencies and resource pressure cost another .2 ms, recomputation costs .3 ms against roughly 2 ms avoided. This conditional estimate reverses if saved traffic was cache-resident or the recomputation throughput is far lower. Measure those assumptions rather than treating peak hardware rates as observations.

## Check your understanding

Does a smaller memory footprint imply a faster kernel? No. Validate mathematical outputs and gradients, random-state handling and side effects first. Then profile traffic, peak storage and elapsed time at the same workload. Separate a faster fixed workload from a larger workload that merely becomes possible because storage fell.

## Prerequisites

- [[roofline-model]]
- [[activation-checkpointing]]

## Sources

- <https://arxiv.org/abs/2205.14135>
- <https://arxiv.org/abs/1604.06174>
