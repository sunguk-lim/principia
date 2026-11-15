---
id: zero-redundancy-optimizer
title: Zero Redundancy Optimizer
summary: ZeRO partitions optimizer states, gradients and parameters across data-parallel workers in stages, reducing persistent model-state replication while trading communication and temporary reconstruction costs.
type: concept
tags: [ml/llm/training]
prereqs: [data-parallelism, gather, training-memory-budget]
sources: [https://arxiv.org/abs/1910.02054, https://deepspeed.readthedocs.io/en/latest/zero3.html]
status: explained
created: 2026-06-23
updated: 2026-11-16
---

# Zero Redundancy Optimizer

## Meaning

ZeRO reduces redundant model-state storage across workers that otherwise train with full [[data-parallelism]] replicas. It progressively partitions optimizer state, gradients and parameters. A worker owns only its assigned portion of partitioned state, while communication makes the required values available for computation. The point is storage ownership, not dividing every layer's arithmetic into smaller tensor operations.

## Mechanism

Separate three persistent byte totals for one unsharded model: W for working parameters, G for gradients and O for optimizer-related state, including any master parameter copy. Let N be the number of equal workers. Ignoring padding, temporary reconstruction and communication buffers, the per-worker persistent totals are:

| Mode | Per-worker persistent model-state bytes |
| --- | --- |
| Replicated | W + G + O |
| ZeRO stage 1 | W + G + O/N |
| ZeRO stage 2 | W + G/N + O/N |
| ZeRO stage 3 | (W + G + O)/N |

Stage 1 partitions optimizer state and updates the owned parameters. Stage 2 also partitions reduced gradients. Stage 3 also partitions the working parameters, collecting needed parameter groups around forward and backward computation. The [[gather]] principle explains reconstructing distributed pieces; an implementation's collective schedule, grouping and overlap determine communication and temporary live memory.

These are model-state formulas, not peak-device-memory promises. The [[training-memory-budget]] also includes retained activations, temporary workspaces, prefetched parameter groups and collective buffers. Some full parameter groups can be live during execution even when permanent storage is partitioned. Equal division is an idealization; uneven groups, padding, precision and retention policies affect actual allocation.

## One example

Let M = 1 billion parameters. Assume explicitly: FP16 working weights use 2M bytes, FP16 gradients use 2M, and optimizer-related state uses 12M: 4M for an FP32 master copy and 8M for two FP32 Adam moment arrays. Thus W=2 GB, G=2 GB and O=12 GB in decimal units, for 16 GB of replicated persistent state. With N=4 workers:

- Stage 1: 2 + 2 + 12/4 = 7 GB per worker.
- Stage 2: 2 + 2/4 + 12/4 = 5.5 GB.
- Stage 3: (2 + 2 + 12)/4 = 4 GB.

This derives the state terms from their actual dtypes. FP32 gradients would change G to 4 GB and change every relevant total. A framework without a separate master copy has a different O. Four GB of persistent state does not mean a four-GB device can run stage 3: activations and reconstructed groups still need space.

## Boundaries and validation

Fully sharded data parallel implementations share the general partition-and-reconstruct approach with stage 3, but product APIs, collective schedules and memory lifetimes are not identical contracts. Tensor and pipeline partitioning divide computations differently and may be combined with state sharding. Host or storage offload moves some state to a different memory tier rather than merely dividing device storage by N.

At fixed model, precision, effective batch and optimizer objective, measure peak allocated and reserved device bytes, communication volume, step time and update agreement within the chosen numerical tolerance. Inspect the largest temporary reconstruction and activation peak. Deeper sharding can fit a larger model yet run more slowly on a constrained interconnect; storage savings alone do not establish a speedup.

## Check your understanding

**Question:** Is optimizer state always twice the byte size of FP16 working weights? **Answer:** No. Under the stated master-copy-plus-two-moments policy it is six times that size; precision and optimizer choices determine the actual ratio.

## Prerequisites

- [[data-parallelism]]
- [[gather]]
- [[training-memory-budget]]

## Sources

- <https://arxiv.org/abs/1910.02054>
- <https://deepspeed.readthedocs.io/en/latest/zero3.html>
