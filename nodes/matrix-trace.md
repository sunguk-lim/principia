---
id: matrix-trace
title: Matrix Trace
summary: The trace of a square matrix is the single number you get by adding up the entries that sit on its main diagonal — the entries M[1][1], M[2][2], … running from the top-left corner…
type: concept
tags: [math/linear-algebra]
prereqs: [matrix-multiplication]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Matrix Trace

## Summary

The trace of a square matrix is the single number you get by adding up the
entries that sit on its main diagonal — the entries `M[1][1], M[2][2], …` running
from the top-left corner to the bottom-right. Written `tr(M) = M[1][1] + M[2][2] +
… + M[n][n]`. It collapses an `n×n` grid of numbers down to one scalar, and the
remarkable thing is that this scalar does not depend on the coordinate system you
happened to write the matrix in: it captures something intrinsic about the
transformation the matrix performs — its total local rate of expansion.

## Grounded explanation

A square matrix is an `n×n` block of numbers (`n` rows, `n` columns). Its **main
diagonal** is the set of entries whose row index equals their column index:
`M[1][1]`, `M[2][2]`, and so on down to `M[n][n]`. The **trace** is just their sum,
`tr(M) = Σ M[i][i]`. Nothing is multiplied; you read off the corner-to-corner
entries and add. So for the `2×2` matrix `M = [[2, 1], [3, 4]]`, the diagonal
entries are `2` (top-left) and `4` (bottom-right), and `tr(M) = 2 + 4 = 6`. The
off-diagonal entries `1` and `3` are simply ignored.

Stated that flatly the trace looks arbitrary — why would adding *those particular*
entries mean anything? The answer is three properties, the third of which is the
whole point.

**It is linear.** Scaling every entry of `M` by a number `c` scales each diagonal
entry by `c`, so `tr(cM) = c·tr(M)`; and adding two matrices adds their diagonals
entry-by-entry, so `tr(M + N) = tr(M) + tr(N)`. The trace passes straight through
scaling and addition — useful, but not yet surprising.

**It is cyclic: `tr(AB) = tr(BA)`.** This one is not obvious, because the matrix
products `AB` and `BA` are themselves usually *different* matrices. Recall from
[[matrix-multiplication]] that the `[i][i]` entry of the product `AB` is the sum
`A[i][1]·B[1][i] + A[i][2]·B[2][i] + …`, i.e. row `i` of `A` against column `i` of
`B`. To get `tr(AB)` we add this over all `i`, which is the grand total of every
product `A[i][j]·B[j][i]` over all pairs `(i, j)`. Now do the same for `tr(BA)`: it
is the grand total of every `B[j][i]·A[i][j]`. But `A[i][j]·B[j][i]` and
`B[j][i]·A[i][j]` are the same numbers (ordinary multiplication commutes), just
summed in a different order — so the two grand totals are equal. The diagonals of
`AB` and `BA` can look completely different entry-by-entry, yet they sum to the
same thing.

**It is basis-invariant — and this is what makes the trace deep.** A matrix is one
way of writing down a *linear map* (a transformation that stretches, rotates, and
shears space) once you have fixed a coordinate system. Choose different coordinates
and the *same* map is described by a *different* matrix `M'`, related to the
original by `M' = P⁻¹ M P`, where `P` is the matrix that translates between the two
coordinate systems and `P⁻¹` is its undo (its inverse, so that `P⁻¹ P` leaves a
vector unchanged). Apply the cyclic property to this. Group the three factors as
`(P⁻¹)(M P)` — treat `A = P⁻¹` and `B = M P`. Then `tr(P⁻¹ M P) = tr(A B) =
tr(B A) = tr(M P P⁻¹) = tr(M)`, because `P P⁻¹` cancels to leave `M`. So every
coordinate description of the same map has the same trace. The trace is therefore
not a fact about the *numbers in the grid* — those change when you change
coordinates — but a fact about the *map itself*.

What intrinsic fact? The total local rate of expansion. Each diagonal entry
`M[i][i]` measures how strongly the map stretches along its `i`-th coordinate
direction; summing them gives the net stretch across all directions at once. If you
drop a tiny blob of volume into the flow described by the map, the trace tells you
how fast that volume is growing (positive trace) or shrinking (negative trace),
independent of how you painted the axes — which is exactly why it must be
basis-invariant. A volume change is a physical event; it cannot depend on your
choice of grid.

This is precisely how the trace appears in the source's table of differential
operators. The *Jacobian* there is the matrix of all first partial derivatives of a
vector field `F` — its `[i][j]` entry is `∂Fᵢ/∂xⱼ`, the rate at which the `i`-th
output component changes as you nudge the `j`-th input. Its diagonal entries
`∂F₁/∂x₁, ∂F₂/∂x₂, …` are the rates at which each component changes along *its own*
direction — the per-axis local stretches. The source defines the **divergence** of
`F` as the "sum of the diagonal partials — the trace," i.e. `tr(Jacobian)`. Reading
this through the geometry above: the divergence is the net local rate at which the
flow expands volume, the "uniform expansion" part of a tiny blob's motion. The
trace is the operation that extracts that expansion number from the full matrix of
derivatives, discarding the off-diagonal terms (which the source attributes to
rotation and shear).

**Worked instance of the cyclic property** (the non-obvious one), with a pair where
`AB ≠ BA` so nothing collapses. Take `A = [[1, 2], [0, 1]]` and
`B = [[3, 0], [1, 2]]`. Multiplying (row of the left against column of the right,
per [[matrix-multiplication]]):

`AB`: top row `[1·3 + 2·1,  1·0 + 2·2] = [5, 4]`; bottom row
`[0·3 + 1·1,  0·0 + 1·2] = [1, 2]`. So `AB = [[5, 4], [1, 2]]`, and
`tr(AB) = 5 + 2 = 7`.

`BA`: top row `[3·1 + 0·0,  3·2 + 0·1] = [3, 6]`; bottom row
`[1·1 + 2·0,  1·2 + 2·1] = [1, 4]`. So `BA = [[3, 6], [1, 4]]`, and
`tr(BA) = 3 + 4 = 7`.

The two product matrices are genuinely different — `AB` has off-diagonals `4, 1`
while `BA` has `6, 1` — yet both traces are `7`. The diagonals (`5, 2` versus
`3, 4`) reshuffle the same total, exactly as the pairing argument above predicts.

## Prerequisites

- [[matrix-multiplication]]

## Sources

- `etc/differential-operators-summary.html` — divergence defined as "sum of the
  diagonal partials — the trace" of the Jacobian; the Jacobian's trace as the
  uniform-expansion part of a flow's local motion.
