---
id: weight-load-amortization
title: Weight-Load Amortization
summary: Weight-load amortization is the reason batching rescues the slow, memory-starved generation step of a large language model.
type: concept
tags: [ml/llm/inference]
prereqs: [roofline-model, memory-hierarchy, matrix-multiplication]
sources:
  - "etc/llm_parallelism_strategies.jsx — MemoryMovement panel (prefill Bn>1 vs decode Bn=1; one weight-tile load reused across Bn token rows; weights W dominate HBM traffic in both phases)"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Weight-Load Amortization

## Summary

Weight-load amortization is the reason batching rescues the slow, memory-starved
generation step of a large language model. To compute one layer, the machine must first
drag that layer's weight matrix up from the slow main memory (HBM, the high-bandwidth
DRAM beside the chip) into the fast compute units. That weight load is a *fixed* cost: it
costs the same number of bytes whether you are computing for one token or for many. If
you process a single token, the whole weight load buys you just one token's worth of
arithmetic — very few operations per byte moved, so by the [[roofline-model]] the
operation is memory-bound and the cores sit nearly idle waiting on bandwidth. If instead
you process a *batch* of B tokens together, the *same single weight load* is reused to
compute all B tokens at once: the byte cost is unchanged but the arithmetic done per byte
grows roughly B-fold. On the [[roofline-model]] that slides the operation rightward, off
the bandwidth-limited slope and toward the compute-bound flat ceiling. So spreading one
unavoidable weight load over more tokens turns wasted bandwidth into nearly free
throughput — which is exactly why inference servers batch requests as aggressively as
they can.

## Grounded explanation

### What the concept *is*: a fixed byte cost spread over a variable amount of work

The central object is a single [[matrix-multiplication]] inside one layer of the model,
written `O = X · W`. Here `W` is the layer's **weight matrix** — a fixed table of learned
numbers, the same for every token the model ever processes. `X` holds the **inputs**: one
row of `X` is one token's vector of features (its current internal representation), and
the matrix product transforms every input row by the shared weights to produce the
corresponding output row of `O`. Two sizes matter. Call `B` the number of rows of `X`
fed in together — the **batch size**, i.e. how many tokens are processed in one matrix
multiply (the source writes this `Bn`). Call `W` (in bytes) the size of the weight matrix
that must be loaded from main memory for this multiply.

The physical fact that drives everything: the cores cannot multiply by a weight they
have not yet fetched, and the weights live in the slow main memory (HBM) — the bottom
rung of the [[memory-hierarchy]] that the cores can actually address — not in the fast
on-chip SRAM beside the compute units. So *before* the arithmetic, the machine pays to move `W` bytes up the memory
hierarchy. Crucially, **that move costs `W` bytes regardless of `B`** — one copy of the
weight matrix serves every row of `X` you happen to have loaded alongside it. The inputs
`X` are tiny by comparison (a token's feature vector is a single row; the weight matrix
is a full square table), so to a good approximation the bytes moved per layer are just
`W`, fixed, while the arithmetic performed scales with the number of rows `B`.

Weight-load amortization is the act of **dividing that fixed `W`-byte cost across as many
tokens as you can fit into one multiply** — paying the load once and "amortizing" it (in
the accounting sense: spreading a fixed expense over many units) over `B` outputs instead
of one.

### Why it works: batching raises arithmetic intensity, sliding you across the roofline

The [[roofline-model]] gives us the exact handle. Recall its key quantity, **arithmetic
intensity** — the floating-point operations a computation performs divided by the bytes
it must move from slow memory. The [[roofline-model]] says performance is capped by
whichever is smaller: the cores' peak operation rate, or the memory bandwidth multiplied
by the arithmetic intensity. Low intensity puts you on the rising, bandwidth-limited slope
(memory-bound — bandwidth is the wall); high intensity puts you under the flat,
compute-limited ceiling (compute-bound — the cores are the wall). The corner between them
is the machine's balance point.

Now watch what `B` does to the intensity of `O = X · W`:

- **Bytes moved** is `W`, fixed (the weight matrix loaded once), essentially independent
  of `B`.
- **Operations performed** is the arithmetic of the multiply, and it scales with the
  number of input rows: each of the `B` rows of `X` must be combined against the same
  weight matrix, so the total operation count is roughly `B` times the per-row cost.

Therefore arithmetic intensity — operations over bytes — is roughly `B × (per-row
operations) / W`, which is **proportional to `B`**. This is the entire mechanism, and it
is the one non-obvious step worth pinning down: doubling the batch does *not* double the
bytes moved (the weight load is shared, not repeated), so it doubles the *intensity*. The
single shared weight load is what makes intensity rise with `B` instead of staying flat.

Map that onto the [[roofline-model]]. At `B = 1` the intensity is tiny — one weight load
for one token's worth of math — so the operation lands far left on the rising slope:
deeply memory-bound, cores starved, the full weight bandwidth paid for almost no compute.
As `B` grows, intensity scales up roughly `×B`, and the operation slides rightward along
the slope toward the balance point and then under the flat ceiling. Once it crosses into
the compute-bound region, the cores are saturated: they are doing useful work every cycle,
and the weight bandwidth that was the bottleneck is now comfortably keeping up. Past that
crossover, adding still more tokens no longer speeds up *per-token* work — you have run
out of slope to climb and hit the flat compute roof — but up to that point each extra
token in the batch was nearly free throughput, because it rode along on a weight load that
was already being paid for.

There is a structural reason the math changes character too. With `B = 1`, `X` is a single
row, so `O = X · W` is a **matrix–vector** [[matrix-multiplication]]: one thin vector
against a big matrix, each weight touched exactly once — the worst possible reuse. With
`B > 1`, `X` is a block of rows, so it becomes a **matrix–matrix** multiply: each loaded
weight is now reused across all `B` rows of the block. Reuse of a loaded value across many operations *is* high
arithmetic intensity, which is precisely the lever the [[roofline-model]] rewards.

### Worked instance: a weight tile, batch 1 versus batch 32

Take one weight tile of `W = 16` megabytes that the layer must load from main memory, and
suppose computing one token's output row against that tile costs `F` floating-point
operations. Hold the hardware fixed (some peak core rate and some bandwidth), so the
[[roofline-model]]'s balance point is a fixed number of operations per byte.

**Batch 1 (one token):** bytes moved ≈ `16` MB (the weight load; the single input row is
negligible). Operations performed ≈ `F`. Arithmetic intensity ≈ `F / 16` MB — call this
`I₁`. This is the matrix–vector case: every weight is used once. `I₁` is small, so on the
[[roofline-model]] the point sits far left on the bandwidth slope: **memory-bound**. The
attainable speed is bandwidth × `I₁`, a small fraction of peak compute; the cores spend
most of their time waiting for the next slice of weights to arrive.

**Batch 32 (thirty-two tokens together):** the *same* `16` MB weight tile is loaded — the
bytes moved are still ≈ `16` MB, because one weight load serves all 32 rows. But the
operations are now ≈ `32 × F`. Arithmetic intensity ≈ `32F / 16` MB = `32 × I₁`: **thirty-two
times higher**, purely from amortizing the fixed load over 32 tokens. On the
[[roofline-model]] the point has slid `32×` to the right. If `32 × I₁` now exceeds the
balance point, the operation has crossed into the **compute-bound** region: its ceiling is
the full peak core rate, and bandwidth is no longer the wall. The bandwidth used per token
has dropped by `32×` (the same `16` MB now amortized across 32 outputs instead of 1), which
is the `≈32×` improvement in bandwidth efficiency.

The honest stopping condition: this rightward slide only helps until the point reaches the
flat compute ceiling. Suppose `I₁` is `1/40` of the balance point. Then `B = 40` puts the
intensity right at the balance point; beyond that, the operation is firmly compute-bound and
larger batches no longer raise per-token throughput — they only add to the time one full
batch takes. So weight-load amortization buys dramatic efficiency in the memory-bound regime
and then flattens out exactly where the [[roofline-model]] says it must: at the ridge between
slope and ceiling.

### Why it matters: prefill is already amortized, decode is not, and that is the memory wall

This single mechanism explains the lopsided performance of the two phases of running a
language model. **Prefill** — the phase that ingests the user's prompt — processes many
tokens at once, so its batch is naturally large (`B` is the whole prompt block). Each
weight load is reused across all those rows, intensity is high, and prefill is comfortably
compute-bound: the cores are the bottleneck, which is the healthy regime. **Decode** — the
phase that generates the answer one token at a time — produces a single new token per step,
so its batch is `B = 1`. Each weight load buys exactly one token's worth of math, intensity
is at rock bottom, and decode slams into the memory wall: the chip spends the step streaming
the entire weight set out of main memory to compute one row, with the cores mostly idle. In
the source's traffic accounting, the weight bytes dominate every step in both phases — but
in prefill that cost is divided over many tokens, and in decode it is borne by one.

The fix follows directly: make decode's batch bigger by serving many independent requests
together, so their single-token steps stack into one multiply with `B > 1` and share each
weight load. (In production this is done by continuously merging and splitting requests into
a shared running batch as they arrive and finish, so the batch stays as full as possible at
every step.) That is the operational form of weight-load amortization, and it is why a
serving system batches requests aggressively: each request added to a memory-bound decode
step rides along on weight loads that are already being paid for, converting otherwise-wasted
bandwidth into extra throughput — until the batch grows large enough that the multiply turns
compute-bound, at which point the [[roofline-model]] says there is nothing left to amortize.

## Prerequisites

- [[roofline-model]]
- [[memory-hierarchy]]
- [[matrix-multiplication]]

## Sources

- `etc/llm_parallelism_strategies.jsx`, MemoryMovement panel — the `O = X · W` view with `Bn` token-rows and a weight tile of `Bm` columns; HBM is identical in prefill and decode, and only the slice of `X` pulled out differs (prefill `Bn > 1`, decode `Bn = 1`); one weight-tile load is reused across all `Bn` rows, amortizing the load over `Bn` tokens (compute-bound) versus producing a single row with no amortization (the memory wall). The traffic bars show weight bytes dominating each step in both phases.
