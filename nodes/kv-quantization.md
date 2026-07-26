---
id: kv-quantization
title: KV-Cache Quantization
summary: The kv-cache — the stored keys and values of every past token — is normally held in 16-bit floats (FP16), and for long context or large batch it is the biggest thing in memory and…
type: concept
tags: [ml/llm/inference]
prereqs: [quantization, kv-cache]
sources:
  - "Liu et al., 'KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache' (2024), arXiv:2402.02750"
  - "Hooper et al., 'KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization' (2024), arXiv:2401.18079"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# KV-Cache Quantization

## Summary

The [[kv-cache]] — the stored keys and values of every past token — is normally
held in 16-bit floats (FP16), and for long context or large batch it is the
biggest thing in memory *and* the thing the model must re-read from memory on
**every** decode step. KV-cache quantization shrinks it by storing those cached
`K` and `V` numbers as low-precision integers (INT8, even INT4) instead of FP16,
using ordinary [[quantization]]: keep a small integer code per value plus a shared
**scale `s`**, and multiply back (`x̂ = q × s`) the moment a value is needed for
attention. INT8 halves the cache (2×); INT4 quarters it (4×) — and because decode
is bottlenecked on *moving* the cache, not computing on it, reading half as many
bytes makes each step roughly that much faster. The one non-obvious wrinkle: the
**keys** have a few wildly large "outlier" channels that would wreck a single
shared scale, so practice quantizes keys **per-channel** and values **per-token**
rather than one scale for the whole cache.

## Grounded explanation

**Where the cost is.** Recall from [[kv-cache]] that decoding stores, for the
whole sequence, `2 × n_tokens × n_layers × n_heads × d_head` numbers, and that for
long context or large batch this cache is the **dominant** inference cost. Two
costs, really. (1) *Memory*: the cache can dwarf the model's own weights — e.g. a
batch of 32 sequences of 8192 tokens, 32 layers, 32 heads, `d_head = 128`, at 2
bytes each (FP16), is `2 × 8192 × 32 × 32 × 128 × 32 × 2 bytes ≈ 137 GB`, more
than fits beside the weights on one accelerator. (2) *Bandwidth*: from [[kv-cache]],
each decode step computes only **one** new token but must read the **entire**
cache back out of memory to attend against it. Decode is therefore *memory-bound* —
the arithmetic is trivial; the time goes to streaming those bytes in. Halve the
bytes and you roughly halve both the footprint and the per-step read time. That is
the entire motivation.

**The idea: apply [[quantization]] to the cache contents.** Instead of storing each
cached key/value as an FP16 number, store it as a low-bit integer **code** plus a
shared **scale**, exactly the scheme from [[quantization]]: a code `q` stands for
the real value `q × s`, where the scale that loses nothing to clipping is
`s = max(|x|) / q_max` and `q_max = 2^(b−1) − 1` for `b` bits (INT8: `q_max = 127`;
INT4: `q_max = 7`). The cache write becomes `q = round(x / s)`; the cache read —
which happens inside attention every step — becomes `x̂ = q × s`. FP16→INT8 takes
each value from 16 bits to 8 (2× smaller); FP16→INT4 takes it to 4 (4× smaller).
The price, also straight from [[quantization]], is bounded rounding error
`|x̂ − x| ≤ s/2`: the keys and values fed into attention are now slightly perturbed.
This is the whole trade — a small, bounded error on `K`/`V` in exchange for 2×–4×
less cache to store and stream.

**The non-obvious step: keys have outliers, so granularity matters.** If you could
use one scale for the entire cache you would — one number to store. But recall the
granularity warning from [[quantization]]: a single outlier inflates `M = max(|x|)`
and so inflates `s`, and a larger `s` coarsens *every other value* (a stray large
entry can force all the small ones to round to code `0`, erasing them). It turns
out the **key** vectors of trained transformers have exactly this pathology: within
a key vector, a *few specific coordinates* (the same coordinate across all tokens —
a "channel") carry persistently huge magnitudes, while the rest are small. One
per-tensor scale built from those outliers would crush the many small coordinates
to zero. The fix is finer granularity, chosen to match where the outliers live:

- **Keys: per-channel.** The outliers are aligned by *coordinate*, so give **each
  coordinate (channel) its own scale**, computed over that coordinate across the
  cached tokens. An outlier channel then gets a large scale that only coarsens
  *itself*; the well-behaved channels keep small scales and stay sharp.
- **Values: per-token.** Value vectors don't show the same fixed-channel outlier
  structure, so they're quantized **per token** — each token's whole value vector
  shares one scale — which also fits the cache layout (a token's `V` arrives all at
  once when the token does).

Some methods (e.g. KVQuant) go further and keep a handful of the very worst outlier
channels in full FP16, quantizing only the rest — paying a little storage to remove
the values that hurt most. The unifying point is the [[quantization]] lesson: put
the scale boundaries where the outliers *aren't*, so one big value can't drag the
grid coarse for its neighbors.

**Worked instance.** Take one cached key vector with a clear outlier coordinate and
one cached value vector, and quantize both to **INT8** (`q_max = 127`).

*Key vector* `k = [0.5, −0.8, 12.0, 0.3]` — coordinate 3 is the outlier (12.0 vs.
neighbors near ±0.5).

- **Per-tensor (the wrong way), to see the failure.** One scale from the whole
  vector: `M = 12.0`, `s = 12.0 / 127 ≈ 0.0945`. Codes `q = round(k/s)`:
  `0.5/0.0945 = 5.3 → 5`; `−0.8/0.0945 = −8.5 → −8`; `12.0/0.0945 = 127 → 127`;
  `0.3/0.0945 = 3.2 → 3`. Dequantized: `[0.472, −0.756, 12.00, 0.284]`. The small
  values survive here only because INT8 is fairly fine — but the *error budget* is
  set by the outlier: `s/2 ≈ 0.047`, so the small `0.3` carries error `≈ 0.016`,
  about **5%** of its value. Drop to INT4 (`q_max = 7`, `s = 12.0/7 ≈ 1.714`) and
  the disaster from [[quantization]] strikes: `round(0.5/1.714)=0`, `round(0.3/1.714)=0`,
  `round(−0.8/1.714)=0` — three of four coordinates collapse to `0`, leaving
  `[0, 0, 7, 0]` → `[0, 0, 12.0, 0]`. The outlier ate the whole vector.

- **Per-channel (the right way).** Each coordinate has its own scale (in real use,
  computed across all cached tokens for that coordinate; here, per single value for
  illustration). The small coordinates now get small scales — e.g. coordinate 1
  with magnitude `0.5` gets `s_1 = 0.5/127 ≈ 0.00394`, so `0.5` maps to code `127`
  and is recovered as `0.500`, error `≈ 0.002` (`< s_1/2 ≈ 0.002`) instead of being
  swamped by the outlier. The outlier coordinate keeps its own large scale
  (`12.0/127 ≈ 0.0945`) and is recovered as `12.00`. No coordinate is coarsened by
  another's magnitude. *This contrast is the reason for per-channel keys.*

*Value vector* `v = [0.2, −1.3, 3.1, 0.05]` — no extreme outlier, quantized
**per-token** (one scale for the whole vector). `M = 3.1`, `s = 3.1/127 ≈ 0.0244`.
Codes: `round(0.2/0.0244)=8`, `round(−1.3/0.0244)=−53`, `round(3.1/0.0244)=127`,
`round(0.05/0.0244)=2`. Dequantized `v̂ = [0.195, −1.293, 3.100, 0.0488]`, every
error under `s/2 ≈ 0.0122`. Because `v` has no outlier, one shared (per-token)
scale is already fine — which is exactly why values don't need the per-channel
treatment keys do.

**What it costs, what it buys.** Storage drops by the bit ratio: this key/value
pair at FP16 is `8 numbers × 16 bits = 128 bits`; at INT8 it is
`8 × 8 = 64 bits` plus the scales (2×, before scale overhead), and at INT4
`8 × 4 = 32 bits` (4×). Across the whole cache that is the difference between a
context fitting in memory or not, and between each decode step reading 137 GB or
~68 GB (INT8) / ~34 GB (INT4) — directly proportional to decode speed, since the
step is memory-bound. The cost is the per-value rounding error `≤ s/2` now riding
on the `K`/`V` that enter attention, plus the small bookkeeping of many scales
(more scales = more bits, the same bits-vs-error trade from [[quantization]], now
applied to the scales themselves). Choosing per-channel keys and per-token values
is what keeps that error small enough — typically INT8 is nearly lossless and
well-done INT4 is usable — so the 2×–4× win comes almost for free.

## Prerequisites

- [[quantization]]
- [[kv-cache]]

## Sources

- Liu et al., "KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache"
  (2024), arXiv:2402.02750 — per-channel keys, per-token values.
- Hooper et al., "KVQuant: Towards 10 Million Context Length LLM Inference with KV
  Cache Quantization" (2024), arXiv:2401.18079 — per-channel key quantization and
  isolating outlier channels in high precision.
