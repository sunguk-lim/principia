---
id: data-parallelism
title: Data parallelism
summary: Data parallelism scales training by putting a full copy of the same neural-network on every GPU, giving each copy a different slice of the data batch, and keeping the copies…
type: concept
tags: [ml/llm/training]
prereqs: [neural-network, gradient-descent, all-reduce]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-19
---

# Data parallelism

## Summary

**Data parallelism** scales training by putting a **full copy of the same
[[neural-network]] on every GPU**, giving each copy a **different slice of the data
batch**, and keeping the copies identical by **[[all-reduce]]-ing the gradients** every
step. Each GPU runs [[gradient-descent]] on its own data, then all-reduce averages the
gradients so every replica applies the *same* update. You scale the **batch**, not the
model — so it only works when the model fits on one GPU.

![Data parallelism: same model per GPU, different data, gradients all-reduced to one ∇avg, identical update](data-parallelism.svg)

## Grounded explanation

This is the first concept that joins the two branches of the brain — the
[[neural-network]] / [[gradient-descent]] side and the [[all-reduce]] (MPI) side:

1. **Replicate the model.** Every GPU holds the *same* [[neural-network]] with the
   *same* weights. (In the figure, every "model" box is identical/gray.)
2. **Split the data.** Each GPU gets a different batch, runs the forward pass, and gets
   a **different** prediction and loss — because the data differs, not the model. So
   each GPU's [[gradient-descent]] step computes a **different gradient** `∇ᵢ`.
3. **All-reduce the gradients.** Here is the crux: if each GPU just applied its own
   `∇ᵢ`, the replicas would drift apart. Instead, [[all-reduce]] combines all the
   gradients into one averaged `∇avg` and hands the *same* `∇avg` to every GPU (the
   gold step in the figure). Averaging gradients is mathematically the gradient of the
   whole combined batch.
4. **Identical update.** Every GPU applies `W -= lr · ∇avg` — the **same** update — so
   the replicas that started equal **stay equal**. The next step begins from an
   identical model everywhere.

**What it costs / when it fails.** The communication is one [[all-reduce]] of the full
gradient per step (large at scale). And every GPU still stores the *entire* model plus
its gradients and optimizer state — so data parallelism alone breaks once the model no
longer fits on a single GPU. (That limit is what tensor parallelism, pipeline
parallelism, and FSDP/ZeRO exist to solve — the next nodes in this branch.)

## Prerequisites

- [[neural-network]]
- [[gradient-descent]]
- [[all-reduce]]

## Sources

_none_
