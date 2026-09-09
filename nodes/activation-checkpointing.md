---
id: activation-checkpointing
title: Activation Checkpointing
summary: Activation checkpointing reduces training memory by saving selected computation-graph boundaries and recomputing omitted intermediate activations during backpropagation.
type: concept
tags: [ml/training]
prereqs: [computation-graph, neural-network, memory-hierarchy]
sources: [https://arxiv.org/abs/1604.06174, https://docs.pytorch.org/docs/stable/checkpoint.html]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Activation Checkpointing

## Summary

**Activation checkpointing** trades computation for training memory. Instead of retaining every intermediate activation from a [[neural-network]] forward pass, it stores selected boundaries and recomputes the missing interior activations when backpropagation reaches that region.

## Grounded explanation

Backpropagation traverses a [[computation-graph]] in reverse and needs intermediate forward values to calculate gradients. Keeping all of them avoids repeated work but consumes memory proportional to the saved activations. Checkpointing chooses a subset to retain in fast storage from the [[memory-hierarchy]].

Consider six sequential layers split into segments `[1,2]`, `[3,4]`, and `[5,6]`. Store the input to each segment rather than all six layer outputs. During the backward pass for layers 5–6, rerun that segment’s forward operations from its stored input, use the regenerated activations for gradients, then release them. Repeat for the preceding segments. Peak saved activation memory falls, while forward computation increases.

The trade-off depends on partitioning. More checkpoints retain more activations and require less recomputation; fewer checkpoints save more memory and repeat more work. Chen et al. show schedules with sublinear memory in network depth, including an $O(\sqrt{n})$-memory construction with roughly one extra forward pass for an $n$-layer chain. Those asymptotic results do not predict a universal runtime percentage for every architecture or implementation.

Recomputation must preserve semantics. Random operations need compatible random-number state, and mutable global state or side effects can make the second forward execution differ from the first. Framework implementations document restrictions and offer variants with different recording and early-stop behavior.

Measure peak allocated and reserved memory, step time, throughput, and numerical agreement on the target model and sequence or batch sizes. Checkpoint the blocks whose retained activations dominate memory, not merely every layer. This technique reduces activation storage; it does not remove parameter, gradient, optimizer-state, communication-buffer, or allocator overhead.

## Prerequisites

- [[computation-graph]]
- [[neural-network]]
- [[memory-hierarchy]]

## Sources

- [Chen et al., “Training Deep Nets with Sublinear Memory Cost”](https://arxiv.org/abs/1604.06174): systematic recomputation schedules and memory/compute bounds.
- [PyTorch checkpoint documentation](https://docs.pytorch.org/docs/stable/checkpoint.html): recomputation semantics, RNG-state handling, and implementation variants.
