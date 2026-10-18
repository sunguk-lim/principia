---
id: rotary-position-embedding
title: Rotary Position Embedding
summary: Rotary position embedding rotates query and key coordinate pairs so their inner product depends on relative position.
type: concept
tags: [ml/llm/architecture]
prereqs: [positional-encoding, matrix-multiplication]
sources: [https://arxiv.org/abs/2104.09864]
status: explained
created: 2026-10-19
updated: 2026-10-19
---

# Rotary Position Embedding

## Meaning

Rotary position embedding (RoPE) encodes position by rotating pairs of projected query and key coordinates. It is a specific mechanism, not just another name for positional encoding or a promise of unlimited context.

## Mechanism

Let q and k be two-coordinate vectors and R(a) the 2×2 matrix with rows (cos(a), -sin(a)) and (sin(a), cos(a)). A query at integer position m becomes R(mθ)q and a key at n becomes R(nθ)k, where θ is that coordinate pair’s frequency. [[matrix-multiplication]] gives (R(mθ)q)ᵀR(nθ)k=qᵀR((n-m)θ)k because R(a)ᵀR(b)=R(b-a). Absolute rotations thus produce relative-position dependence in the dot product. Higher-dimensional heads use several coordinate pairs and frequencies. [[positional-encoding]] supplies the general motivation; RoPE specifies how the score receives positional information without adding the same position vector to every token representation.

## Worked example

Choose q=(1,2), k=(3,1), θ=π/2, m=1, and n=2. The rotated query is (-2,1), the rotated key (-3,-1), and their dot product is 6-1=5. The relative rotation R(π/2)k=(-1,3) gives q·(-1,3)=-1+6=5, the same result. Jointly shifting both positions by one preserves that relative score. This does not establish reliable extrapolation: frequency scaling, trained position ranges, masks, and positional-coordinate conventions affect behavior. Test same-offset invariance numerically, cached decoding offsets, long-range retrieval, and image-grid aspect ratios. Frequency changes generally require evaluation rather than being a free context extension.

## Check your understanding

Does relative dependence mean attention ignores content? No: the rotated inner product still depends on q and k as well as the offset.

## Prerequisites

- [[positional-encoding]]
- [[matrix-multiplication]]

## Sources

- <https://arxiv.org/abs/2104.09864>
