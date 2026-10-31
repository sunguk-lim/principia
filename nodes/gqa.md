---
id: gqa
title: Grouped-query attention (GQA / MQA)
summary: Standard multi-head-attention gives every query head its own key/value head — so the kv-cache stores one K,V per head.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, kv-cache, multi-head-attention]
sources: [https://arxiv.org/abs/2305.13245]
status: explained
created: 2026-06-20
updated: 2026-11-01
---

# Grouped-query attention (GQA / MQA)

## Summary

Standard [[multi-head-attention]] gives every query head its **own**
key/value head — so the [[kv-cache]] stores one `K,V` per head. Since that cache is
the inference bottleneck, **multi-query attention (MQA)** has *all* query heads share
a **single** `K,V` head, and **grouped-query attention (GQA)** is the middle ground:
query heads are split into a few **groups**, and each group shares one `K,V` head.
Fewer `K,V` heads → a proportionally **smaller KV-cache** (and less memory traffic per
step), with a quality/efficiency tradeoff that must be evaluated.

![GQA/MQA: MHA gives each query head its own K,V head; GQA shares one K,V head per group; MQA shares one for all — shrinking the KV-cache](gqa.svg)

## Grounded explanation

In [[transformer-attention]] with $h$ heads, each head $i$ has its own
$Q_i, K_i, V_i$. During decoding the [[kv-cache]] must store the `K` and `V` of
**every head** for **every past token**, so its size scales with the number of
**KV heads**:

$$\text{cache} \;\propto\; 2 \times n_\text{tokens} \times n_\text{layers} \times \underbrace{n_\text{kv-heads}}_{\text{the knob}} \times d_\text{head}.$$

The query heads are cheap to keep many of (they don't persist in the cache); it's the
**KV heads** that cost cache memory. So decouple the two counts:

1. **MHA (baseline).** $n_\text{kv-heads} = h$. Each of the $h$ query heads has its own
   `K,V`. Full cache, full quality.
2. **MQA.** $n_\text{kv-heads} = 1$. All $h$ query heads attend against **one** shared
   `K,V` head — the cache shrinks by a factor of $h$. Cheapest, but the single shared
   head can cost some quality and be unstable to train.
3. **GQA.** $n_\text{kv-heads} = g$ with $1 < g < h$. Partition the $h$ query heads into
   $g$ groups; all heads in a group share that group's `K,V`. The cache shrinks by
   $h/g$ — most of MQA's saving while keeping much of MHA's quality. (Llama-2 70B and
   Mistral use GQA; PaLM and Falcon use MQA.)

So GQA/MQA spend a little attention expressiveness to buy a large cut in the dominant
inference cost — directly attacking the [[kv-cache]] size that motivates them.

## Query heads are not stored KV heads

Let H_q be the number of query heads, H_kv the number of stored key/value heads, D the width of each such head, L the layer count, T retained tokens and B bytes per element. A full uncompressed cache has 2×L×T×H_kv×D×B bytes before metadata, alignment and replication. For L=32, T=1,024, H_kv=8, D=128 and B=2, this is 134,217,728 bytes, or 128 MiB. Changing H_q from 32 to 64 while holding these other quantities fixed leaves that cache payload unchanged, although query computation changes.

In ordinary MHA, H_kv=H_q and D=d_model/H_q. Therefore fixed model width keeps H_kv×D constant. In GQA, changing query head count does not imply that D or H_kv stayed fixed: explicitly state the architecture. Holding H_kv=8 while halving D from 128 to 64 halves the payload; merely increasing H_q at fixed D does not. Smaller cache does not establish unchanged quality or proportional end-to-end speedup. Validate architecture, checkpoint adaptation, real memory traffic and task quality independently.

## Prerequisites

- [[transformer-attention]]
- [[kv-cache]]

## Sources

_none_

- <https://arxiv.org/abs/2305.13245>
