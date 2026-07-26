---
id: cosine-similarity
title: Cosine Similarity
summary: Cosine similarity measures how aligned two vectors are — how nearly they point in the same direction — independent of how long either one is.
type: concept
tags: [math/linear-algebra]
prereqs: [vector-dot-product]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Cosine Similarity

## Summary

**Cosine similarity** measures how *aligned* two vectors are — how nearly they point in the same direction — independent of how long either one is. It takes the [[vector-dot-product]] of the two vectors and divides it by the product of their lengths, leaving a single number between $-1$ and $+1$: $+1$ when they point the exact same way, $0$ when they are perpendicular (unrelated), and $-1$ when they point in exactly opposite directions.

## Grounded explanation

A **vector** here is just an ordered list of numbers, which we picture as an arrow from the origin to a point. Two things about an arrow matter: its **direction** (which way it points) and its **magnitude** or **length** (how far it reaches). The length of a vector $u$, written $\lVert u\rVert$, is the ordinary distance from the origin to its tip — for $u=(u_1,\dots,u_n)$ it is $\sqrt{u_1^2+\cdots+u_n^2}$, the square root of the sum of its squared entries (an application of the Pythagorean theorem).

The [[vector-dot-product]] of two equal-length vectors $u$ and $v$, written $u\cdot v$, multiplies their matching entries and sums the results into a single number. That prerequisite also gives the geometric identity we build on here:

$$u \cdot v \;=\; \lVert u\rVert\,\lVert v\rVert\,\cos\theta$$

where $\theta$ is the angle between the two arrows and $\cos\theta$ (the **cosine** of that angle) is a number that equals $1$ when the angle is $0$ (same direction), $0$ when the angle is $90$ degrees (perpendicular), and $-1$ when the angle is $180$ degrees (opposite directions). The dot product therefore already mixes together *three* ingredients: the two lengths and the angle. The trouble is that a large dot product could mean the vectors are well aligned, *or* merely that one of them is very long — the two effects are tangled.

**The defining idea of cosine similarity is to untangle them.** If we divide the dot product by both lengths, the two length factors on the right-hand side cancel exactly, leaving the angle ingredient alone:

$$\cos\theta \;=\; \frac{u \cdot v}{\lVert u\rVert\,\lVert v\rVert}.$$

This quotient *is* cosine similarity. It is the one non-obvious step, and the identity above is its justification: because the dot product equals $\lVert u\rVert\,\lVert v\rVert\cos\theta$, dividing out the two magnitudes is algebraically guaranteed to isolate $\cos\theta$ and nothing else. The result depends only on the *directions* of the two arrows, never on their lengths.

**Why normalizing by length is the whole point.** Scaling a vector — making the arrow twice as long without turning it — does not change its direction, so it must not change the similarity. The division enforces exactly that: stretch either vector and both its dot-product contribution and its length grow by the same factor, which then cancels. This is what makes the measure useful for comparing data of unequal size. When each piece of text is turned into a vector of numbers (an embedding, where similar meaning is arranged to produce a small angle), a long document and a short one about the same topic will have very different vector lengths but nearly the same direction — so cosine similarity scores them as similar, where a raw dot product would be dominated by the longer one. Reading the number off is then direct: a value near $+1$ means a small angle and thus close alignment ("very similar"); near $0$ means perpendicular and thus unrelated; near $-1$ means opposing. This is the standard score used to rank candidates in nearest-neighbor search, where one asks which stored vectors point most nearly the same way as a query vector.

**Worked instance.** Take $u=(1,0)$ and $v=(1,1)$. Their dot product is $1\cdot 1 + 0\cdot 1 = 1$. The lengths are $\lVert u\rVert=\sqrt{1^2+0^2}=1$ and $\lVert v\rVert=\sqrt{1^2+1^2}=\sqrt{2}$. So the cosine similarity is $\frac{1}{1\cdot\sqrt{2}}=\frac{1}{\sqrt{2}}\approx 0.71$, which is indeed $\cos$ of $45$ degrees — the angle between a vector pointing straight along the first axis and one pointing diagonally. Now compare $u$ with $w=(0,1)$: the dot product is $1\cdot 0 + 0\cdot 1 = 0$, so the cosine similarity is $0$ — the two arrows are perpendicular, the "unrelated" case. Finally compare $u$ with $x=(2,0)$: the dot product is $1\cdot 2 + 0\cdot 0 = 2$, and the lengths are $1$ and $2$, giving $\frac{2}{1\cdot 2}=1$. Even though $x$ is twice as long as $u$, the score is the maximum $1$, because they point in the very same direction — the concrete demonstration that cosine similarity ignores magnitude and reports only alignment.

## Prerequisites

- [[vector-dot-product]]

## Sources

_none_
