---
id: vllm
title: vLLM
summary: A high-throughput LLM inference/serving engine whose contribution is an engine loop that fuses paged KV-cache memory management (PagedAttention) with iteration-level continuous batching, so memory waste and idle GPU compute both collapse.
type: concept
tags: [ml/llm/inference]
prereqs: [paged-attention, continuous-batching, prefill-vs-decode, kv-cache]
sources: [arxiv:2309.06180]
status: explained
created: 2026-07-06
updated: 2026-07-06
---

# vLLM

## Summary

**vLLM** is an LLM **inference and serving engine** built to maximize *throughput* —
tokens per second across many concurrent requests. Its contribution is not one new
trick but an **engine loop** that fuses two mechanisms which attack the two things that
throttle a naive server: **[[paged-attention]]** removes the wasted GPU *memory* that
otherwise caps how many requests fit at once, and **[[continuous-batching]]** removes the
wasted GPU *compute* of a batch whose slots sit idle. Because the [[prefill-vs-decode]]
decode phase is memory-bound, its cost per token *falls* as the batch grows — so freeing
memory (pillar one) and keeping the batch full (pillar two) **compound** into throughput.
On its original benchmark vLLM served **2–4× more throughput** than the prior systems at
the same latency, purely from managing the [[kv-cache]] better — no model change.

## Grounded explanation

### What vLLM *is* — an engine, not an attention variant

vLLM is a **serving system**: a process that accepts a stream of generation requests and
drives a GPU (or several) to answer them. The concept to grasp is the **engine** — how it
schedules work and manages memory across *many* requests at once — not any single kernel.
Its two headline pieces, [[paged-attention]] and [[continuous-batching]], are prerequisite
sub-mechanisms explained in their own nodes; vLLM is the architecture that runs them
**together** in one loop. Everything below is about that loop and *why* the combination
wins.

### The problem: throughput dies on two wasted resources

A served model produces tokens by the [[prefill-vs-decode]] cycle — a compute-bound
**prefill** of the prompt, then many memory-bound **decode** steps, one token each. To go
fast you run **many requests as a batch**, so one weight load from GPU memory serves many
tokens instead of one. Two separate wastes stop a naive server from keeping that batch
large and full:

1. **Wasted memory (caps how many requests fit).** Each request needs a growing
   [[kv-cache]]. The naive allocator reserves **one contiguous buffer sized for the
   model's maximum context** per request, because the final length is unknown. A request
   that stops after 200 tokens still pins a 2048-token buffer — most of it dead. GPU
   memory runs out after a handful of requests, long before compute does, so the batch
   is *small*.
2. **Wasted compute (caps how full the batch stays).** With **static batching** the
   batch's membership is locked until its slowest member finishes. Short requests leave
   dead slots doing throwaway work, and newly arrived requests wait — so the batch is
   *not full* even when work is queued.

Both wastes throttle the same lever — the effective batch size — and vLLM removes them
with one mechanism each.

### Pillar one — [[paged-attention]] frees the memory

vLLM stores each request's [[kv-cache]] not as a max-sized contiguous buffer but as
**fixed-size blocks** (e.g. 16 tokens of K,V each), drawn on demand from a shared pool,
addressed through a per-request **block table** (the full mechanism, and the OS-memory
analogy behind it, is [[paged-attention]]). The consequence vLLM exploits: internal waste
drops from "a whole max-length buffer minus what you used" to **at most one partly-filled
block** per request. The same GPU memory now holds **many more** requests' caches at once
— which is exactly the cap that limited batch size.

### Pillar two — [[continuous-batching]] keeps the batch full

vLLM's scheduler runs **[[continuous-batching]]** (iteration-level scheduling): it
re-decides the batch's membership **every step**, evicting a request the instant it emits
its end token and admitting a waiting one into the freed slot (and its freed KV blocks). No
slot idles while work is queued. Crucially this composes with pillar one: because the
evicted request's [[kv-cache]] is paged, its freed blocks return to the pool and are handed
straight to the admitted request with **no fragmentation** — the two mechanisms were
co-designed to share the same block pool.

### The engine loop — one step, three coordinated parts

Concretely the engine holds three components that act in concert on every iteration:

- a **scheduler** (does [[continuous-batching]]) — picks which requests run this step,
  subject to a **block budget**: how many KV blocks the pool can still hand out;
- a **block manager** (does [[paged-attention]]) — allocates physical blocks for the new
  tokens, maintains each request's block table, frees blocks of finished requests;
- a **model executor** — runs one batched forward pass on the GPU.

One iteration:

1. **Schedule.** The scheduler admits waiting requests (each begins with a [[prefill-vs-decode]]
   prefill of its prompt) and continues in-flight requests (one decode token each), stopping
   admission when the block budget is exhausted. If running requests need more blocks than
   remain, it **preempts** one — freeing its blocks now and recomputing or swapping them
   later — so the loop never deadlocks on memory.
2. **Allocate.** The block manager hands out physical blocks for this step's new tokens and
   updates the block tables.
3. **Run.** The executor does a single forward pass over the whole batch — prefill tokens of
   the admitted requests plus one decode token for each continuing request — producing one
   new token per running sequence.
4. **Retire.** Requests that emitted their end token are returned to the client and their
   blocks freed back to the pool, ready for step *n+1*'s admissions.

Trace a **single request R** through this loop: at admission it gets, say, block table
`[b7]` (prompt fills block 0); as it decodes past 16 tokens the manager appends `[b7, b23]`;
when R finishes, `b7` and `b23` return to the pool and the scheduler immediately admits a
queued request into that space. The block table is the one object tying the scheduler's
"who runs" decision to the block manager's "where the K,V live" — the seam where the two
pillars meet.

### Why it compounds — a worked instance

Take **OPT-13B in fp16 on one 40 GB A100** (vLLM's original setting) and derive the batch
each scheme allows.

- **Weights:** 13B params × 2 bytes = **26 GB**. After ~2 GB of activation working memory,
  about **12 GB** is left for the [[kv-cache]].
- **KV per token:** $2 \times L \times H \times d_\text{head} \times 2\text{ bytes}$ with
  $L=40$ layers, hidden $H \cdot d_\text{head} = 5120$ (the leading 2 = K and V, the trailing
  2 = fp16 bytes) $= 2 \times 40 \times 5120 \times 2 \approx$ **0.8 MB/token**.
- **KV budget:** $12\text{ GB} / 0.8\text{ MB} \approx$ **15,000 token-slots** total, shared
  across all concurrent requests.

Now split by allocator, for a workload whose requests actually generate **~256 tokens** on
average but whose model max context is **2048**:

| Scheme | Memory charged per request | Concurrent requests in 15,000 slots |
|---|---|---|
| Naive max-reservation | 2048 (reserved up front) | $15000 / 2048 \approx$ **7** |
| Paged (on demand) | ~256 actual + ≤16 slack | $15000 / 256 \approx$ **58** |

PagedAttention alone lifts the feasible batch from ~7 to ~58 — **nearly 8×** more requests
sharing each weight load. That is where the [[prefill-vs-decode]] insight cashes in: decode
is **memory-bound**, re-streaming the whole 26 GB of weights to emit one token per request,
so putting ~8× more requests under that one weight load pushes decode **rightward toward the
compute ceiling** — throughput climbs with batch size until the cores saturate. Continuous
batching then ensures those ~58 slots stay *occupied* step after step rather than draining to
the slowest request.

The two effects multiply: **memory headroom raises the ceiling on batch size; scheduling
keeps the batch at that ceiling.** The end-to-end gain is **sub-linear** in the 8× memory
figure — the paper measures **2–4×** throughput — because batch growth has diminishing
returns once decode nears the compute ridge, and real traffic mixes in longer, variable
lengths. The lesson is the shape, not the exact factor: vLLM turns *memory management* into
*throughput*, without touching the model's math.

### Beyond the core

The same block-table machinery underpins vLLM's further features — sharing identical
prompt-prefix blocks across requests, slicing long prefills into chunks interleaved with
decodes to smooth latency, splitting a too-large model across GPUs, and drafting tokens ahead
to verify in one pass. These are extensions built *on* the two pillars above, not part of
what makes vLLM the engine it is; each is its own concept.

## Prerequisites

- [[paged-attention]]
- [[continuous-batching]]
- [[prefill-vs-decode]]
- [[kv-cache]]

## Sources

- Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention" (vLLM), SOSP 2023 — arxiv:2309.06180.
