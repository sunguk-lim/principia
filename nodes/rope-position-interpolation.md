---
id: rope-position-interpolation
title: RoPE Position Interpolation
summary: RoPE position interpolation compresses requested position coordinates into the pretrained coordinate range before computing rotations.
type: concept
tags: [ml/llm/architecture]
prereqs: [rotary-position-embedding, measurement]
sources: [https://arxiv.org/html/2306.15595v2]
status: explained
created: 2026-10-23
updated: 2026-10-23
---

# RoPE Position Interpolation

## Meaning

Position interpolation extends a RoPE-based model's coordinate range by feeding smaller position indices to its rotation rule. It is different from merely allocating a larger cache or claiming that relative-position dependence guarantees extrapolation. The altered coordinates change attention scores, so useful accuracy remains an adaptation and evaluation question.

## Mechanism

In [[rotary-position-embedding]], a coordinate pair at position p rotates by pθ for its assigned frequency θ. Let L be the training context length, L_new the requested length, and s=L_new/L>1 an extension factor. Uniform interpolation replaces p by p/s, making the angle pθ/s. For positions numbered from zero through L_new-1, the largest effective coordinate is (L_new-1)/s<L. This is the paper's linear down-scaling mechanism, not every later frequency-dependent RoPE scaling method.

The price is compressed relative separation: an offset Δp rotates by Δpθ/s. Nearby positions become less separated in phase as well as distant positions being brought into range. The cited paper studies fine-tuning after interpolation; its model sizes, update counts and benchmark results are experimental settings rather than universal sufficient conditions. [[measurement]] must test both the extended range and the original short-context workload.

## Worked example

Take an illustrative training length L=4, requested length L_new=8 and one pair frequency θ=π/4. Then s=2. Raw position p=6 would rotate by 6π/4=3π/2, whereas interpolation uses effective position 3 and angle 3π/4. A raw gap of two tokens becomes an angular gap π/4 rather than π/2. No token is removed; only its positional coordinate changes.

Changing this mapping during cached generation can invalidate keys already rotated with the old convention. Specify one consistent schedule, coordinate offsets and cache-compatibility policy. Validate cached versus full-prefix outputs with the same mapping. Measure distant-fact retrieval at multiple offsets, long-document answer support, short-context regressions, memory and prefill/decode latency. A configured large context or a mathematically evaluable rotation is not proof that the model reliably uses every position.

## Check your understanding

**Question:** Does doubling the interpolation factor leave local positional phases unchanged? **Answer:** No. Uniform interpolation compresses every positional gap.

## Prerequisites

- [[rotary-position-embedding]]
- [[measurement]]

## Sources

- <https://arxiv.org/html/2306.15595v2>
