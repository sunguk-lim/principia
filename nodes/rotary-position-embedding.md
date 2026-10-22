---
id: rotary-position-embedding
title: Rotary Position Embedding
summary: Rotary position embedding rotates query and key coordinate pairs so their inner product depends on relative position.
type: concept
tags: [ml/llm/architecture]
prereqs: [positional-encoding, matrix-multiplication, complex-number]
sources: [https://arxiv.org/abs/2104.09864]
status: explained
created: 2026-10-19
updated: 2026-10-23
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

## Complex-pair representation

The same two-coordinate rotation can be expressed with [[complex-number]] arithmetic. Write a query pair as z_q=a+ib and a key pair as z_k=c+id. Multiplication by u(α)=cos(α)+i sin(α) sends (a,b) to (a cos(α)-b sin(α), a sin(α)+b cos(α)), exactly the real rotation matrix already defined above. The unit-length factor changes direction without changing pair length. The real dot product is Re(z_q conjugate(z_k)), not Re(z_q z_k).

At positions m and n, the score contribution becomes Re(u(mθ)z_q conjugate(u(nθ)z_k))=Re(u((m-n)θ)z_q conjugate(z_k)). This is the complex form of the same relative-position identity; the sign differs from writing the real matrix on the key because conjugation and the dot product place the rotation on the other operand.

Reuse q=(1,2), k=(3,1), θ=π/2, m=1 and n=2. Their complex forms are 1+2i and 3+i. Rotation gives -2+i and -3-i; multiplying the first by the conjugate of the second gives (-2+i)(-3+i)=5-5i, whose real part is the same score 5. No extra expressive capacity was added by changing notation. Validate pair ordering, conjugation, angle sign, dtype and cached position offsets against the real-pair implementation before treating a complex kernel as equivalent.

## Prerequisites

- [[positional-encoding]]
- [[matrix-multiplication]]

## Sources

- <https://arxiv.org/abs/2104.09864>
