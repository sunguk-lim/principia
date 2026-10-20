---
id: expert-parallelism
title: Expert parallelism (MoE)
summary: A mixture-of-experts layer holds many expert FFNs and routes each token to only a few.
type: concept
tags: [ml/llm/training]
prereqs: [mixture-of-experts, all-to-all]
sources: [https://github.com/deepseek-ai/DeepInfer/blob/main/doc/inference_deployment_qa.md]
status: explained
created: 2026-06-20
updated: 2026-10-21
---
	
# Expert parallelism (MoE)

## Summary

A [[mixture-of-experts]] layer holds **many** expert FFNs and routes each token to only
a **few**. **Expert parallelism (EP)** is how you *run* that layer across GPUs: place
different experts on different GPUs. Because a token's chosen expert usually lives on
**another** GPU, the routed tokens are shipped there and back with **two [[all-to-all]]s**
— **dispatch** (send each token to its expert's GPU), then **combine** (return each result
home). EP is the parallelism strategy whose defining collective is all-to-all, not
all-reduce.

![Expert parallelism: tokens routed by a gate, dispatched to their expert's GPU via all-to-all, then combined back](expert-parallelism.svg)

## Grounded explanation

Start from [[mixture-of-experts]]: a router has already chosen each token's top-k experts
and the per-token compute is sparse. The **only new problem EP introduces is locality** —
the expert FFNs are spread across GPUs, so the routed tokens must *move*. Per layer:

1. **All-to-all #1 — dispatch.** Each expert lives on one GPU. Every GPU simultaneously
   sends each of its tokens to whichever GPU owns that token's expert — every process
   sending a different chunk to every other is exactly an [[all-to-all]]. Afterwards each
   GPU holds precisely the tokens its **local** experts must process.
2. **Expert compute.** Each GPU runs its local experts on the tokens that arrived — sparse
   on both axes (only routed tokens, only local experts).
3. **All-to-all #2 — combine.** The outputs are sent back the way they came — a second
   [[all-to-all]] — so each token's result returns to its origin and the full sequence is
   reconstructed everywhere, ready for the next layer.

So EP wraps the [[mixture-of-experts]] computation in **two [[all-to-all]]s per layer**.
Contrast the other strategies: data/tensor/pipeline parallelism all run the *same* weights
on every token; MoE deliberately sends *different* tokens through *different* expert
weights, which makes all-to-all (not all-reduce) its characteristic collective. Because
all-to-all is the heaviest pattern (`n×n` personalized messages), EP is most practical
within a fast-interconnect domain.

## Wide decode groups and skew

Expert placement also changes the effective batch seen by each expert. In a balanced toy layer, 64 simultaneous token routes distributed over eight experts give eight routes per expert on average. If wider attention-data-parallel groups aggregate 256 routes over those same eight experts, the average becomes 32. Larger expert matrix batches can amortize weight reads and improve kernel efficiency; this is not caused by merely increasing the number of devices while keeping demand fixed.

Routing skew makes averages insufficient: one hot expert can delay the entire step. Redundant copies of hot experts and periodic reassignment can reduce the slowest-rank burden, at the cost of weight memory, statistics and migration traffic. DeepInfer documents different prefill/decode expert layouts and an expert-parallel load balancer using recent load statistics. These are implementation examples, not a claim that wide expert groups always beat tensor parallelism. Compare throughput per GPU, token latency, load skew and collective time at fixed quality and real offered load.

## Prerequisites

- [[mixture-of-experts]]
- [[all-to-all]]

## Sources

_none_

- <https://github.com/deepseek-ai/DeepInfer/blob/main/doc/inference_deployment_qa.md>
