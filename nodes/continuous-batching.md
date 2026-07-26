---
id: continuous-batching
title: Continuous Batching
summary: When a language model serves many requests at once, the cheap way to feed the GPU is to run a batch — several sequences advancing together so one big matrix multiply does the work…
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache, queue]
sources:
  - "Yu et al., 'Orca: A Distributed Serving System for Transformer-Based Generative Models', OSDI 2022"
  - "Kwon et al., 'Efficient Memory Management for Large Language Model Serving with PagedAttention' (vLLM), SOSP 2023"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Continuous Batching

## Summary

When a language model serves many requests at once, the cheap way to feed the GPU
is to run a **batch** — several sequences advancing together so one big matrix
multiply does the work of many small ones. The naive scheme, **static batching**,
locks the batch's membership for the whole run: it gathers N requests, decodes them
together, and **no slot is freed until the longest sequence finishes**. A request
that wanted 5 tokens sits idle while a neighbor grinds out 200, and waiting requests
can't start. **Continuous batching** (a.k.a. *in-flight* or *iteration-level*
batching) instead **re-decides the batch's membership at every decode step**: the
moment a sequence emits its end-of-sequence token it is **evicted** from the batch,
and a waiting request is pulled from the [[queue]] of pending arrivals and **admitted**
into the freed slot — so the batch stays full
step after step. This is only possible because decoding already proceeds one token
per step **and** each sequence carries its **own independent [[kv-cache]]**, so
sequences at different lengths can share a batch and join or leave between steps.

## Grounded explanation

**What a batch is and why we want one.** Decoding emits one token per step. At each
step the model multiplies the batch's input vectors by its weight matrices. Doing
this for one sequence barely occupies a GPU; doing it for B sequences stacked into
one matrix costs almost the same wall-clock time but produces B tokens — the GPU is
**throughput-bound**, so a full batch is far more efficient than B separate runs.
The serving question is therefore: *how do we keep the batch full?*

**Why sequences can even coexist in one batch.** From [[kv-cache]], each sequence
keeps two growing buffers — its **K-cache** and **V-cache** — holding the keys and
values of every token it has produced so far. At step $t$ a sequence projects only
its **one** newest token into a query $q_t$, key $k_t$, value $v_t$; it appends
$k_t,v_t$ to *its own* cache and attends $q_t$ over *its own* cached columns. The
crucial fact: **these caches are per-sequence and never interact.** A sequence that
is 3 tokens long and one that is 180 tokens long each just attend over their own
buffer. So a batch is not a single shared state — it is a *bag of independent
decode states*, and the only thing tying them together is that they take a step at
the same time. That is exactly what lets us swap members in and out.

**Why static batching wastes the GPU.** Static batching fixes the bag once. The
batch finishes only when its slowest member finishes, because the scheduler never
looks again until then. Two costs follow: (1) a short sequence keeps occupying its
slot long after it emitted its end token — a **dead slot** doing throwaway compute;
(2) any request that arrives after the batch started must **wait** for the whole
batch to drain before it can be loaded. Both costs grow with the *variance* in
output lengths, which for real traffic (a one-word answer next to a long essay) is
large.

**The continuous-batching insight.** Because the caches are independent and the
loop is already per-step, the scheduler can run **between every pair of steps**:

1. **Evict** any sequence that emitted its end-of-sequence token this step; its
   slot — and its KV-cache memory — is freed.
2. **Admit** waiting requests into the freed slots (a newly admitted request first
   does a *prefill* step to build its initial KV-cache, then joins the per-step
   decode loop).
3. Take one decode step for whatever set of sequences now occupies the batch.

The batch's membership thus changes from step to step, but each member is always
valid because it carries its own cache. The invariant the scheduler maintains is:
**every slot that *can* hold a live sequence *does*** — no slot idles while work is
queued. That is the whole win: idle slots are converted into useful tokens.

**Worked instance.** Suppose the GPU has **4 slots** and four requests arrive, with
these output lengths (in decode steps):

| Request | Output length | Arrival |
|---|---|---|
| A | 2 steps | at start |
| B | 6 steps | at start |
| C | 3 steps | at start |
| D | 4 steps | queued, arrives once a slot frees |

*Static batching.* The scheduler loads A, B, C into 3 of the 4 slots and locks the
batch. (D cannot start — there is a free slot, but static batching does not admit
mid-run; even if D were loaded at the start, the point below is unchanged.) Trace
the slots over steps, writing `–` for a dead/idle slot:

| Step | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
|---|---|---|---|---|
| 1 | A | B | C | – |
| 2 | A (last) | B | C | – |
| 3 | – | B | C (last) | – |
| 4 | – | B | – | – |
| 5 | – | B | – | – |
| 6 | – | B (last) | – | – |

A finishes at step 2, C at step 3, but the batch does not free until **B finishes at
step 6**. Only then can D run, taking 4 more steps (steps 7–10). Count *useful slot
occupancies* (a slot doing real work for a live sequence) versus *total slot-steps*:

- Steps 1–6 use a 4-slot batch ⇒ 24 slot-steps; useful ones = A:2 + B:6 + C:3 = **11**.
- Then D runs steps 7–10 in its own batch ⇒ 16 slot-steps; useful = **4**.
- Total useful = 15 tokens; total slot-steps = 40. **Utilization ≈ 15/40 = 37.5%**,
  and all four requests are done at **step 10**.

*Continuous batching.* Same 4 slots, but the scheduler re-decides each step:

| Step | Slot 1 | Slot 2 | Slot 3 | Slot 4 | Event |
|---|---|---|---|---|---|
| 1 | A | B | C | – | D admitted into free slot 4 (prefill) |
| 2 | A (last) | B | C | D | A finishes → evict |
| 3 | – | B | C (last) | D | slot 1 free; queue empty |
| 4 | – | B | – | D (last) | C, D finish this step |
| 5 | – | B | – | – | |
| 6 | – | B (last) | – | – | B finishes; all done |

Now D started at step 1 (slot 4 was free) and finished at step 4. Every sequence
finished as early as its own length allowed; the batch never waited for B to
release others. All four requests are done at **step 6** instead of step 10 — a
**40% reduction in total time** — and over those 6 steps the useful slot-steps are
still 15 out of 24, **utilization ≈ 62.5%** versus 37.5%. The avoided idle slots
(B's neighbors going dead in the static trace) are exactly the gap continuous
batching closes.

**Why the numbers move the way they do.** The static scheme pays for the *maximum*
output length on *every* slot (the batch is alive for max-length steps, and short
sequences burn dead slot-steps for the difference). Continuous batching pays only
for each sequence's *own* length, because eviction returns the slot immediately and
admission refills it. The larger the spread in output lengths, the larger the gap —
which is why this technique dominates for real serving traffic.

**In practice.** Iteration-level scheduling was introduced by **Orca** (2022); the
widely used **vLLM** server combines it with paged KV-cache memory (so the freed
cache of an evicted sequence can be reused by an admitted one without
fragmentation). Both rest on the same foundation explained here: independent
per-sequence [[kv-cache]] state plus a per-token loop make the batch a swappable
bag rather than a fixed group.

## Prerequisites

- [[kv-cache]]
- [[queue]]

## Sources

- Yu et al., "Orca: A Distributed Serving System for Transformer-Based Generative Models," OSDI 2022.
- Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention" (vLLM), SOSP 2023.
