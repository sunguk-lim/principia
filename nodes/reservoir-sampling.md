---
id: reservoir-sampling
title: Reservoir Sampling
summary: Reservoir sampling maintains a uniform fixed-size sample of a stream prefix without knowing its eventual length.
type: concept
tags: [math/probability]
prereqs: [probability, dynamic-array]
sources: [https://www.cs.umd.edu/~samir/498/vitter.pdf]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Reservoir Sampling

## Summary

Keep a bounded sample while giving late arrivals the same chance as earlier records. Algorithm R stores the first $k$ records, then probabilistically replaces a stored record as each new one arrives. Its target is the entire observed prefix, not just recent traffic.

## Grounded explanation

| Symbol | Type and meaning |
|---|---|
| $k$ | Positive integer, maximum number of stored records |
| $n$ | Integer, records processed so far |
| $i$ | Integer, position of the current incoming record |
| $j$ | Uniform random integer from 1 through $i$ |

Store records in a [[dynamic-array]] capped at $k$ slots. Fill those slots first. For arrival $i>k$, draw $j$: if $j\leq k$, replace slot $j$; otherwise discard the arrival. All $i$ draw outcomes must have equal [[probability]]. The new record enters with chance $k/i$. Processing $n$ records takes linear work and stores at most $k$ records, plus a counter and random-generator state.

### An original worked trace

Take $k=2$ and arrivals A, B, C, D, E. Start with `[A, B]`. For C, draw 2 from 1–3: replace slot 2, giving `[A, C]`. For D, draw 4 from 1–4: discard D. For E, draw 1 from 1–5: obtain `[E, C]`. This trace illustrates replacement and rejection; it is one possible run, not proof that every run has representative categories.

The fairness calculation explains the rule. Before record $i$, an old record has inclusion chance $k/(i-1)$. Conditional on being stored, it is removed only if the draw selects its particular slot, chance $1/i$. Its new inclusion chance is therefore

$$\frac{k}{i-1}\left(1-\frac1i\right)=\frac{k}{i}.$$

The arrival also has chance $k/i$. Starting with certainty for the first $k$ records proves equal marginal inclusion at every prefix. Uniformity over whole size-$k$ subsets is stronger: a target subset containing the arrival can arise from $i-k$ predecessor subsets, each followed by a particular replacement of probability $1/i$; a subset without it survives a rejection of probability $(i-k)/i$. Thus both kinds have equal probability by induction.

### Limits and validation

Uniformity concerns record positions. Repeated events still count repeatedly; heavy users can dominate an event sample. Sampling without replacement does not make selected records statistically independent. Historical uniformity can also be undesirable when recent behavior is the actual learning target.

For a small stream, enumerate all draws and compare final subset probabilities exactly. For production recovery, checkpoint the counter, contents, and random-generator state together; replayed events otherwise change the sampling population. Combining equally sized reservoirs from unequal partitions by simple concatenation is not a valid uniform global sample.

## Sources

- [Vitter, Random Sampling with a Reservoir, §2](https://www.cs.umd.edu/~samir/498/vitter.pdf): Algorithm R and the sampling invariant. Trace and validation discussion above are independent explanations.
