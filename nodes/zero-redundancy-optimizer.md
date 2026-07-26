---
id: zero-redundancy-optimizer
title: Zero Redundancy Optimizer
summary: The Zero Redundancy Optimizer (ZeRO) removes the wasteful replication built into plain data-parallelism.
type: concept
tags: [ml/llm/training]
prereqs: [data-parallelism, gather]
sources:
  - "Rajbhandari, S. et al. \"ZeRO: Memory Optimizations Toward Training Trillion Parameter Models.\" SC, 2020. https://arxiv.org/abs/1910.02054"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Zero Redundancy Optimizer

## Summary

The **Zero Redundancy Optimizer** (ZeRO) removes the wasteful **replication** built into
plain [[data-parallelism]]. Plain data parallelism keeps a *full copy* of three things on
every worker: the model **parameters** (the trained numbers), the **gradients** (one
adjustment-number per parameter, produced each step), and the **optimizer states** (extra
per-parameter bookkeeping the update rule carries between steps). Holding all three on
every GPU is hugely redundant. ZeRO instead **shards** them — cuts each into N equal
pieces and gives each of the N workers just one piece — and **[[gather]]s** a piece back only
for the moment it is needed. It does this in three escalating stages, each cutting per-GPU
memory further at the price of more communication, so a model far larger than one GPU's
memory can still be trained while keeping data parallelism's simple "split the batch"
structure.

## Grounded explanation

Recall what [[data-parallelism]] stores. Every GPU holds the *same* full model and, each
step, computes a gradient from its own slice of the batch, then averages gradients across
GPUs so all replicas apply the identical update and stay in sync. For that to work, each
GPU keeps a complete copy of: the **parameters** `P` (call its size, in bytes, `P` too),
the **gradients** (same count as parameters, so another `P` bytes), and the **optimizer
states**. The optimizer states are the part people underestimate. A plain update just does
`weight ← weight − learning_rate · gradient`, carrying nothing between steps. But the
popular Adam update keeps, *per parameter*, a running average of the gradient and a running
average of the gradient squared — two extra numbers each — plus a high-precision master
copy of the weights. In the usual mixed-precision setup that adds up to roughly `2P` bytes
of optimizer state, i.e. about *twice* the parameter memory. So plain data parallelism
spends about `P + P + 2P = 4P` bytes per GPU on the model, **the same `4P` repeated on
every one of the N GPUs**. That repetition is the "redundancy" ZeRO is named after.

**The key idea.** None of those three things is needed *in full, all the time*. A
parameter is only consulted when its layer runs; a gradient only matters at the moment the
optimizer updates that parameter; an optimizer state is touched only during that same
update. So instead of every GPU storing the whole of everything, ZeRO assigns each GPU
**ownership of 1/N of each array** and reconstructs a full piece on demand: gather the
needed slice from its owners just before use, then drop the gathered copy and fall back to
the 1/N resident share. The result of the step is mathematically identical to plain data
parallelism — the same averaged update reaches the same weights — but no GPU ever holds the
full set of all three arrays at once.

**Three stages, each sharding one more array.** ZeRO is offered in increasing levels
because each array can be sharded independently, and sharding more of them saves more
memory but moves more data over the network:

- **Stage 1** shards only the **optimizer states**. They are the biggest single block
  (the `2P` above), so removing their replication is the largest one-step win for the
  least added communication. Each GPU keeps full parameters and full gradients but owns
  only `2P/N` of the optimizer state, updating just its own 1/N of the weights and then
  sharing the updated slices.
- **Stage 2** additionally shards the **gradients**. Since a GPU only needs the full
  gradient for the parameters it will update, it can keep just `P/N` of the gradients and
  let each gradient-slice be summed onto its owner rather than held everywhere.
- **Stage 3** additionally shards the **parameters** themselves. Now a GPU permanently
  holds only `P/N` of the weights and must gather a layer's full weights right before that
  layer computes, then discard them afterward. This deepest stage is exactly the scheme
  also known as Fully Sharded Data Parallel (FSDP): the same idea, sharding all three
  arrays. (Sharding parameters across workers to fit a too-large model is distinct from
  tensor parallelism or pipeline parallelism, which split *one* layer's math across GPUs;
  ZeRO keeps each layer's math whole and only distributes *storage*.)

**Worked instance.** Take a model whose parameters occupy `P` bytes, trained with Adam, on
`N = 8` GPUs. Plain [[data-parallelism]] costs, per GPU:
`P (params) + P (grads) + 2P (optimizer) = 4P`. Apply the stages, dividing only the sharded
arrays by `N = 8`:

- **Stage 1** (shard optimizer): `P + P + 2P/8 = P + P + 0.25P = 2.25P` per GPU.
- **Stage 2** (also shard gradients): `P + P/8 + 2P/8 = P + 0.125P + 0.25P = 1.375P`.
- **Stage 3** (also shard parameters): `P/8 + P/8 + 2P/8 = 4P/8 = 0.5P`.

So Stage 3 turns the original `4P` into `4P/N = 0.5P` — an 8× reduction in per-GPU model
memory at `N = 8`. Concretely, a model whose parameters, gradients, and Adam states would
need 1.2 TB on a single GPU (far past any one device) fits in about 150 GB per GPU under
Stage 3, which is now within reach. The price is communication: the deeper the stage, the
more often a piece must be gathered before use and re-sharded after, so memory savings are
paid for in extra data crossing the network each step — the central trade-off ZeRO lets you
dial.

## Prerequisites

- [[data-parallelism]]
- [[gather]]

## Sources

- Rajbhandari, S. et al. "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models." SC, 2020. https://arxiv.org/abs/1910.02054
