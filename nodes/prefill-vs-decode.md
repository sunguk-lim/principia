---
id: prefill-vs-decode
title: Prefill vs Decode
summary: Serving a large language model splits into two phases with opposite cost profiles.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache, roofline-model]
sources:
  - "etc/llm_parallelism_strategies.jsx — ChunkedPrefill panel (one-sentence prefill: weight-matmul linear, attention quadratic; the memory-bound/compute-bound flip) and MemoryMovement panel (prefill Bn>1 amortized vs decode Bn=1 memory wall)"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Prefill vs Decode

## Summary

Serving a large language model splits into **two phases with opposite cost
profiles**. In **prefill** the whole prompt is pushed through the model in one
forward pass to populate the [[kv-cache]] — all prompt tokens travel through each
weight together, so every weight loaded from memory is reused across many tokens.
That makes each loaded byte do a lot of arithmetic, which by the
[[roofline-model]] puts prefill **right of the ridge: compute-bound**, limited by
how fast the cores can compute. In **decode** the model then generates the answer
**one token at a time**; each step must re-read the model's entire weights (and the
growing [[kv-cache]]) from memory just to emit a single token, so almost no
arithmetic is done per byte loaded. That puts decode **far left of the ridge:
memory-bound**, limited by bandwidth, with the cores idling while bytes stream in.
The same hardware therefore behaves completely differently in the two phases — and
because a long prefill running in a scheduler step can stall the decodes of other
in-flight requests, the contrast is what motivates fixes like chunked prefill.

## Grounded explanation

### What the concept *is*: one model, two regimes on the roofline

A served language model does the same matrix multiplies in both phases — the
difference is **how many tokens ride through each loaded weight at once**, and that
single difference flips which hardware limit binds. Recall from the
[[roofline-model]] the controlling quantity: a computation's **arithmetic
intensity** is the number of floating-point operations it performs per byte it must
drag up from slow main memory. The model places a computation on a rising-then-flat
"roof" at the spot fixed by that intensity. Land left of the corner (the **ridge
point**, where the machine's compute ceiling meets its bandwidth ceiling) and you
are **memory-bound** — bandwidth is the wall and the cores idle. Land right of the
ridge and you are **compute-bound** — the cores are the wall and extra bandwidth
sits unused. Prefill and decode are the *same model's* two operating points, and
they fall on **opposite sides of that one ridge**.

### Prefill: many tokens per weight load → high intensity → compute-bound

Prefill is the phase that processes the prompt before any output token exists. Its
job is to run every prompt token through every layer once and, in doing so, fill
the [[kv-cache]] — computing and storing each prompt token's key and value so that
later steps never recompute them. The crucial structural fact is that **all prompt
tokens go through the model together, in parallel.** Consider one weight matrix
inside a layer and the operation it performs, $O = X \cdot W$, where the rows of
$X$ are tokens. In prefill there are *many* rows — every prompt token at once. To
multiply, the hardware loads a tile of the weights $W$ from memory **once**, then
reuses that same loaded tile against **every** token row. The expensive byte
transfer (the weights) is **amortized over many tokens**: one load, many results.

By the [[roofline-model]] this is exactly what raises arithmetic intensity — many
floating-point operations are squeezed out of each loaded byte. So prefill lands
**right of the ridge, compute-bound**: the cores are the bottleneck, working flat
out, while the memory system comfortably keeps up. Prefill's cost therefore grows
with **prompt length** — more tokens means more core work — and it is the phase
where the expensive cores actually earn their keep.

(One refinement the source stresses: prefill has two kinds of work inside each
layer. The weight multiplies just described grow *linearly* with prompt length $N$,
but **attention** — each token attending to all prior tokens — grows
*quadratically*, as $N^2$, because a token at position $p$ must look back at $p$
earlier tokens. For ordinary prompt lengths the linear weight work dominates and
prefill is solidly compute-bound; only for a very long single prompt does the
quadratic attention term swell enough to dominate the cores' time. The headline
holds: prefill keeps the cores busy.)

### Decode: one token per weight load → near-zero intensity → memory-bound

Decode is the generation phase. Here the model emits the answer **one token at a
time**: it produces a token, appends it to the input, and runs the whole model
again to produce the next — autoregression. This is precisely the setting the
[[kv-cache]] exists for: each decode step computes only the *one* new token's query,
key, and value, appends that key/value to the cache, and attends against every
cached column, so it never recomputes the past. That makes each step cheap in
*arithmetic* — but it is exactly what makes decode **memory-bound**.

Take the same operation $O = X \cdot W$, but now $X$ has **one row** — the single
new token. To compute it the hardware still must load **the entire model's weights
from memory**, every layer's matrices, just as in prefill. Yet that whole load
produces only **one** output row. There is **no amortization**: a weight byte is
read, used once, discarded. On top of the weights, the step must also re-read the
[[kv-cache]] — which grows with every token generated — to attend over the past.
So decode moves a huge volume of bytes (weights plus a growing cache, often several
gigabytes) to do a tiny amount of arithmetic on behalf of one token.

That is rock-bottom arithmetic intensity, and by the [[roofline-model]] it places
decode **far left of the ridge, deeply memory-bound**. The ceiling it is pinned
under is bandwidth times intensity, far below peak compute; the cores sit mostly
**idle, waiting for weights to stream in**. The lever that helps prefill (faster
cores) does nothing for decode, because decode is nowhere near the compute ceiling —
the only things that help are more bandwidth, fewer bytes moved, or sharing each
expensive weight load across **more** tokens (batching many requests' decode steps
together so one weight load serves many tokens at once, recovering the amortization
prefill gets for free).

### Worked instance: a 500-token prompt, then generation

Take a single request with a **500-token prompt**, served on a chip whose
[[roofline-model]] ridge sits at, say, ~33 floating-point operations per byte (the
representative balance from that node).

**Prefill** runs once over all 500 tokens. For each weight matrix, the hardware
loads a weight tile and reuses it across all 500 token rows: one byte load, 500
tokens' worth of arithmetic. The intensity is high — hundreds of operations per
byte — so on the roof this lands **right of the ridge**, in the compute-bound
region. The cores run near peak; the whole prompt is consumed in **one large
batched pass**, and at the end the [[kv-cache]] holds the keys and values of all 500
tokens. Concretely, the dominant byte transfer is the model's weights (on the order
of a gigabyte or more), and that single transfer is paid off across all 500 tokens.

**Decode** then generates the answer token by token. To produce the **first** output
token, the hardware again streams the *entire* weights — that same gigabyte-plus —
but this time it yields **one** token. Intensity collapses to a fraction of an
operation per byte; on the roof this is **far left of the ridge**, deeply
memory-bound, cores idling while the weights stream. To produce the **second** token
it streams the whole weights *again* (plus a [[kv-cache]] now one column longer), and
so on for every token of the answer. Each decode step is a separate, bandwidth-
limited re-streaming of the model to emit a single token.

So the contrast is sharp and lives on **one** [[roofline-model]] roof: prefill is a
single FLOP-limited matmul sitting right of the ridge with the cores busy; each
decode step is a separate bandwidth-limited pass sitting far left of the ridge with
the cores idle — same chip, same weights, opposite sides of the same corner, purely
because prefill reuses each loaded weight across 500 tokens while decode reuses it
across one.

### Why it matters: the phases want different things, and mixing them hurts

Because the two phases bind on different limits, they want different optimizations —
prefill chases core throughput, decode chases bandwidth and large batches. The
trouble is that a real server interleaves them: new requests need prefill while
older requests are mid-decode. A scheduler step runs one batch with a fixed token
budget, and **prefill is token-heavy** (the whole prompt at once) while **decode is
one token per request.** If a long prefill is allowed to occupy a whole step, every
request that is mid-generation **stalls** — its next decode token waits behind the
prefill. This is the central tension the source draws out, and the fix it motivates
is **chunked prefill**: slice a long prefill into small pieces and pack each
scheduler step with one prefill chunk *plus* the other requests' decode tokens, so
in-flight generations keep producing tokens instead of freezing behind a big
prompt. More broadly, the same logic — keep the expensive weight load busy serving
as many tokens as possible — is why decode requests are batched together
(continuous batching). The whole apparatus exists because prefill and decode sit on
opposite sides of the [[roofline-model]] ridge.

## Prerequisites

- [[kv-cache]]
- [[roofline-model]]

## Sources

- `etc/llm_parallelism_strategies.jsx`, MemoryMovement panel — the $O = X \cdot W$ picture with the same weights $W$ in memory both phases: prefill pulls many token rows so one weight-tile load is amortized across them (compute-bound), decode pulls one row so the load produces a single output (the memory wall).
- `etc/llm_parallelism_strategies.jsx`, ChunkedPrefill panel — the single-sentence prefill where weight-matmul is linear and attention quadratic, the memory-bound/compute-bound flip, and the scheduling motivation: a long prefill in one step stalls in-flight decodes, so prefill is chunked and interleaved with decode tokens.
