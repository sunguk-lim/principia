---
id: symmetric-antisymmetric-decomposition
title: Symmetric-Antisymmetric Decomposition
summary: "Every square matrix M (a grid of numbers with as many rows as columns) splits in exactly one way into two pieces added together: a symmetric part S, which is unchanged when you…"
type: concept
tags: [math/linear-algebra]
prereqs: [matrix-multiplication]
sources:
  - differential-operators-summary.html
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Symmetric-Antisymmetric Decomposition

## Summary

Every square matrix `M` (a grid of numbers with as many rows as columns) splits in exactly one
way into two pieces added together: a *symmetric* part `S`, which is unchanged when you flip it
across its main diagonal, plus an *antisymmetric* part `A`, which turns into its own negative
under that flip. The recipe is `S = ½(M + Mᵀ)` and `A = ½(M − Mᵀ)`, where `Mᵀ` is `M` flipped
across the diagonal. The reason this matters: when `M` describes how a flowing fluid stretches and
spins near a point, `S` captures all of the *stretching and shearing* (how a small circle is
squashed into an ellipse) while `A` captures the pure *rotation* (how fast the blob spins) — one
clean cut separating distortion from spin.

## Grounded explanation

Start with the central object. A *square matrix* `M` is a grid of numbers with the same number of
rows as columns; write `M[i][j]` for the number in row `i`, column `j`. The *main diagonal* is the
line of entries `M[1][1], M[2][2], …` where the row number equals the column number.

The one operation we need on top of this is the **transpose**, written `Mᵀ`. It is the matrix you
get by reflecting `M` across its main diagonal: the entry at row `i`, column `j` of `Mᵀ` is the
entry at row `j`, column `i` of the original, i.e. `Mᵀ[i][j] = M[j][i]`. The diagonal entries stay
put; every off-diagonal entry swaps places with its mirror partner on the other side of the
diagonal.

With the transpose in hand we can name two special kinds of matrix:

- A matrix is **symmetric** when it equals its own transpose, `Mᵀ = M`. Concretely, every mirror
  pair is equal: `M[i][j] = M[j][i]`. Reflecting it across the diagonal changes nothing.
- A matrix is **antisymmetric** (also called *skew-symmetric*) when it equals *minus* its own
  transpose, `Mᵀ = −M`. Concretely, every mirror pair consists of opposite numbers,
  `M[i][j] = −M[j][i]`. A consequence forced by this rule: each diagonal entry must equal its own
  negative (`M[i][i] = −M[i][i]`), which is only possible if it is zero — so an antisymmetric
  matrix always has all zeros down its diagonal.

**The decomposition.** Claim: any square `M` can be written as `M = S + A` with `S` symmetric and
`A` antisymmetric, and there is exactly one such pair. The construction is

```
S = ½(M + Mᵀ)        A = ½(M − Mᵀ)
```

Here `M + Mᵀ` and `M − Mᵀ` are formed entry-by-entry (add or subtract the matching numbers), and
`½(…)` halves every entry. These are not the matrix product of the prerequisite
[[matrix-multiplication]]; they are the simpler entrywise sum, difference, and scaling — the same
arithmetic that lives *inside* each cell of a matrix product, here used on its own.

Why this works — the *why*, not just the recipe. Two facts do all the work.

*First, adding the two pieces returns `M`.* Adding them entrywise, `S + A = ½(M + Mᵀ) + ½(M − Mᵀ)`.
The two `+½Mᵀ` and `−½Mᵀ` terms cancel, and the two `½M` terms combine to a full `M`. So
`S + A = M` exactly. Nothing is lost or added; the split merely re-bundles the same numbers.

*Second, each piece really is of its claimed type.* This rests on one identity about the transpose:
flipping a sum across the diagonal flips each summand, so `(M + Mᵀ)ᵀ = Mᵀ + (Mᵀ)ᵀ`, and flipping
twice gives back the original, `(Mᵀ)ᵀ = M`. Hence `(M + Mᵀ)ᵀ = Mᵀ + M = M + Mᵀ` — so `M + Mᵀ` is
unchanged by transposing, which makes `S` symmetric. The same step on the difference gives
`(M − Mᵀ)ᵀ = Mᵀ − M = −(M − Mᵀ)` — so `A` turns into its own negative, which makes `A`
antisymmetric.

*Why the split is unique.* Suppose `M = S + A` for **some** symmetric `S` and antisymmetric `A`,
without assuming the formulas. Transpose both sides: `Mᵀ = Sᵀ + Aᵀ = S − A` (using `Sᵀ = S` and
`Aᵀ = −A`). Now we have two equations, `M = S + A` and `Mᵀ = S − A`. Adding them gives `M + Mᵀ = 2S`,
i.e. `S = ½(M + Mᵀ)`; subtracting gives `M − Mᵀ = 2A`, i.e. `A = ½(M − Mᵀ)`. So *any* valid split
is forced to be exactly the one the recipe builds — there is no second answer. That uniqueness is
what lets us speak of *the* symmetric part and *the* antisymmetric part of a matrix.

**Why anyone cares.** Picture a fluid flowing, and look very close to one point. The way the flow
changes from place to place near that point is captured by a square matrix called the *Jacobian* —
each entry says how fast one velocity component changes as you step in one direction. A tiny blob of
fluid sitting at that point gets transformed by this matrix: it can be stretched, sheared, and spun
all at once, and the raw Jacobian tangles those effects together. Feed the Jacobian through this
decomposition and the tangle separates. The symmetric part `S` — called the *strain* — holds all the
stretching and shearing: it is what deforms a small circle of fluid into an ellipse, with no net
turning. The antisymmetric part `A` holds the pure *rotation*: it spins the blob rigidly, like a
record on a turntable, without changing its shape. So one algebraic split answers two physically
different questions — "how does the flow distort?" (read `S`) and "how does the flow spin?"
(read `A`) — that the original matrix had mixed together.

There is a sharper payoff hiding in `A`. Because an antisymmetric matrix has zero diagonal and each
below-diagonal entry is just minus the one above, it carries very few independent numbers — in two
dimensions, only one. That single independent number *is* the flow's spin rate, the quantity called
the **curl**. So the antisymmetric part is not merely "the rotation, roughly" — its lone free entry
is (half of) the curl on the nose. The decomposition is the bridge from a full derivative matrix to
the curl.

**Worked instance.** Take a genuinely lopsided matrix — not symmetric, not antisymmetric, no zeros
in special places — so every part of the mechanism actually fires:

```
M = [ 2  3 ]
    [ 1  4 ]
```

First the transpose: swap each off-diagonal entry with its mirror partner, leaving the diagonal `2`
and `4` alone. The off-diagonal `3` (row 1, col 2) and `1` (row 2, col 1) trade places:

```
Mᵀ = [ 2  1 ]
     [ 3  4 ]
```

Now `S = ½(M + Mᵀ)`. Add entrywise: `2+2=4`, `3+1=4`, `1+3=4`, `4+4=8`; then halve each:

```
S = ½ [ 4  4 ]  =  [ 2  2 ]
      [ 4  8 ]     [ 2  4 ]
```

Check `S` is symmetric: its mirror pair is `2` and `2` — equal, so `Sᵀ = S`. Good.

Now `A = ½(M − Mᵀ)`. Subtract entrywise: `2−2=0`, `3−1=2`, `1−3=−2`, `4−4=0`; then halve each:

```
A = ½ [ 0   2 ]  =  [ 0   1 ]
      [ −2  0 ]     [ −1  0 ]
```

Check `A` is antisymmetric: the diagonal is all zero, and the mirror pair is `1` and `−1` —
opposites, so `Aᵀ = −A`. Good.

Finally confirm they reassemble: `S + A` entrywise is `2+0=2`, `2+1=3`, `2+(−1)=1`, `4+0=4`, which
is exactly the original `M = [[2,3],[1,4]]`. The split lost nothing.

Reading the physics off this instance: the strain `S = [[2,2],[2,4]]` says the flow stretches and
shears the blob (the off-diagonal `2`s are shear, the diagonal `2` and `4` are stretching along the
two axes). The rotation `A = [[0,1],[−1,0]]` has one independent number, `1`; that entry is half the
curl, so this flow spins with a definite, single rate while it deforms. One matrix, two clean stories.

## Prerequisites

- [[matrix-multiplication]]

## Sources

- `differential-operators-summary.html` — the Jacobian of a flow
  splits motion into expansion (divergence), rotation (curl), and shear; divergence and curl are
  read out of the Jacobian as its trace and its antisymmetric part.
