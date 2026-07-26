---
id: paged-attention
title: Paged attention
summary: The kv-cache grows one token at a time, but a sequence's final length is unknown, so the naive implementation reserves one big contiguous block sized for the maximum length —…
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache, copy-on-write, virtual-memory, page-table]
sources: []
status: explained
created: 2026-06-20
updated: 2026-06-24
---

# Paged attention

## Summary

The [[kv-cache]] grows one token at a time, but a sequence's *final* length is
unknown, so the naive implementation reserves **one big contiguous block** sized for
the **maximum** length — wasting most of it (internal fragmentation) and blocking
sharing. **Paged attention** (the idea behind vLLM) borrows **[[virtual-memory|operating-system virtual
memory]]**: chop the cache into small **fixed-size blocks** ("pages", e.g. 16 tokens
each), allocate them **on demand** as the sequence grows, and keep a per-sequence
**block table** mapping logical token positions → physical blocks. Memory need no
longer be contiguous, fragmentation nearly vanishes, and blocks can be **shared**
across sequences — which lets far more requests run in one batch.

![Paged attention: a per-sequence block table maps logical KV positions to scattered fixed-size physical blocks, allocated on demand and shareable](paged-attention.svg)

## Grounded explanation

Recall the [[kv-cache]]: every step appends one token's `K,V`, so the cache for a
sequence keeps growing. The problem is *where* to put it. The simple choice — a single
contiguous buffer per sequence, pre-sized to the model's max context — has three costs:

1. **Internal fragmentation.** A request that ends after 50 tokens still holds a buffer
   sized for, say, 2048 — the unused tail is dead memory that no other request can use.
2. **No sharing.** Two requests with the **same prompt prefix** (or beam-search
   branches of one request) each keep a full private copy, even though the prefix's
   `K,V` are identical.
3. **Fewer concurrent requests.** Because each sequence hoards a worst-case buffer, GPU
   memory runs out long before compute does, capping batch size and throughput.

Paged attention fixes all three with the OS paging trick:

- **Fixed-size blocks.** The [[kv-cache]] is split into uniform blocks holding a few
  tokens' `K,V` each. The physical blocks live anywhere in a shared pool — not
  contiguous.
- **Block table (the [[page-table]]).** Each sequence keeps a small table: logical block
  *i* → physical block address. Attention reads `K,V` by walking the table, so the math
  is unchanged; only the *lookup* is indirected.
- **Allocate on demand.** A new block is handed out only when the current one fills, so
  a sequence uses ≈ its actual length — internal waste shrinks to at most one
  partly-filled block.
- **Share by reference.** Identical prefix blocks are pointed to by **multiple** block
  tables ([[copy-on-write]] when one diverges), so a shared prompt is stored **once**.

The result: the same GPU holds many more sequences' caches at once, so batch size and
throughput rise sharply — paged attention attacks the **memory** side of the
[[kv-cache]] bottleneck, the same pressure that motivates fewer KV heads.

## Prerequisites

- [[kv-cache]]
- [[virtual-memory]]
- [[page-table]]
- [[copy-on-write]]

## Sources

_none_
