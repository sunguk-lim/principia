---
id: fsdp
title: FSDP / ZeRO
summary: FSDP (Fully Sharded Data Parallel, a.k.a.
type: concept
tags: [ml/llm/training]
prereqs: [data-parallelism, all-gather, reduce-scatter]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-25
---

# FSDP / ZeRO

## Summary

**FSDP** (Fully Sharded Data Parallel, a.k.a. **ZeRO**) is [[data-parallelism]] in which
each GPU permanently stores only **1/N of every layer's parameters, gradients, and
optimizer state** instead of a full replica. A layer's full weights are reconstructed
**just-in-time** with an [[all-gather]] right before they're used, then **discarded**;
gradients are summed back to their owner with a [[reduce-scatter]]. So only **one layer is
materialized in full at any instant** — peak memory ≈ one layer, not the whole model —
while the *math* stays identical to plain data parallelism.

![FSDP: each GPU keeps 1/N of every layer; all-gather to FULL just-in-time, compute, discard; backward re-gather then reduce-scatter|1174](fsdp.svg)

## Grounded explanation

Plain [[data-parallelism]] replicates the whole model on every GPU and syncs once per step
with an all-reduce of the gradients. Its limit is **memory**: every GPU holds the entire
model plus its gradients and optimizer state. FSDP removes that by **sharding** — each GPU
owns just 1/N of each layer — and paying it back with two collectives, per layer:

1. **Forward, layer by layer.** The owned shards are useless alone, so right before layer
   *L* runs, an **[[all-gather]]** reconstructs its *full* weights on every GPU (each GPU
   contributes its 1/N and receives all the others — in the figure, the shards **slide**
   between GPU columns). Each GPU computes `hₗ` on its **own** batch, then **discards** the
   full copy — freeing the memory immediately.
2. **Backward, layer by layer (in reverse).** The weights were discarded, so FSDP
   **all-gathers `Wₗ` again** to compute the gradient `∂Wₗ` (you can't differentiate a
   layer you don't hold). Each GPU's `∂Wₗ` reflects only its own batch, so a
   **[[reduce-scatter]]** sums each shard's gradient across all GPUs and leaves every owner
   just its 1/N (the gold flash). That sharded, globally-summed gradient is what the
   optimizer applies — to its shard only.

**Why it stays correct (sync).** The two collectives bind the GPUs together: [[all-gather]]
gives every GPU the *identical* full weights (so all replicas compute with the same
parameters), and [[reduce-scatter]] makes each kept gradient-shard reflect the *whole*
global batch. So the result is the same as data parallelism — FSDP just **decomposes that
one all-reduce into `reduce-scatter + all-gather` and spreads it across the layers** (each
of those compound collectives is itself built from the simpler primitives: gather
collects chunks *into* one rank, scatter deals chunks *out* from one rank), which
is why it costs more communication (a gather per layer, every forward and backward) but a
fraction of the memory. It is what lets a model too large to replicate be trained at all.

## Prerequisites

- [[data-parallelism]]
- [[all-gather]]
- [[reduce-scatter]]
## Sources

_none_
