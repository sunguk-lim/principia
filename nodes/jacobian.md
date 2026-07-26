---
id: jacobian
title: Jacobian (J)
summary: The Jacobian of a vector-field is the square grid holding all of the field's first partial-derivatives — its full derivative, the single matrix that says, to first order, how the…
type: concept
tags: [math/calculus]
prereqs: [partial-derivative, matrix-trace, symmetric-antisymmetric-decomposition, vector-field, differential]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-18
updated: 2026-06-24
---

# Jacobian (J)

## Summary

The **Jacobian** of a [[vector-field]] is the square grid holding *all* of the field's
first [[partial-derivative]]s — its full derivative, the single matrix that says, to
first order, how the field stretches, spins, and shears the space around a point.
Rows index the field's output components, columns index the input variables. Its
deep payoff: split it once with the [[symmetric-antisymmetric-decomposition]] and the
local motion of a tiny blob of fluid falls apart into three clean pieces —
*expansion* (read off as the [[matrix-trace]], which is the divergence), *rotation*
(the antisymmetric part, which is the curl), and *shear* (the leftover off-diagonal
of the symmetric part, which the named operators never isolate).

## Grounded explanation

Start with the central object: a **[[vector-field]]** — a function
$F:\mathbb{R}^n \to \mathbb{R}^m$ that takes a point with $n$ input coordinates
$(x_1,\dots,x_n)$ and returns an output with $m$ components $(F_1,\dots,F_m)$. Picture
it as a fluid flow: at every point of space, $F$ gives the velocity vector of the
fluid sitting there.

The **Jacobian** $J$ assembles every first [[partial-derivative]] of this field into
one rectangular grid. Recall that a [[partial-derivative]] $\partial F_i/\partial x_j$
measures how fast one output component $F_i$ changes as you nudge one input variable
$x_j$, holding all the other inputs fixed. The Jacobian collects all $m \times n$ of
these rates, placing the rate for output $i$ and input $j$ in row $i$, column $j$:

$$J_{ij} = \frac{\partial F_i}{\partial x_j}$$

So **rows are indexed by output components, columns by input variables**. That layout
is the whole point: it is exactly the shape needed for $J$ to act as the *best linear
approximation* of $F$ near a point — the multi-output generalization of the scalar
[[differential]], which is a single row of partials; here we stack one such row per
output component to get the full matrix. "Linear approximation" means that if you step a
small displacement $\Delta x$ away from the point, the change in the field is, to
first order, the matrix-times-vector product $J\,\Delta x$ — the curved, complicated
$F$ is replaced locally by the flat linear map $J$, just as an ordinary derivative
replaces a curve by its tangent line. For a flow, that linear map is precisely the
recipe for how the fluid stretches and rotates the immediate neighborhood of the
point.

When the field maps a space to itself ($m = n$), $J$ is **square** — as many rows as
columns — and we can ask what *kind* of motion that local linear map performs. This is
where the depth lives. A square matrix describing a flow tangles three different
physical effects together: the blob of fluid can be inflated or deflated, spun, and
squashed, all at the same time, and the raw entries of $J$ mix these into one grid.
The [[symmetric-antisymmetric-decomposition]] is the algebra that untangles them. It
states that any square matrix splits *uniquely* into a symmetric part $S$ (unchanged
when reflected across its main diagonal) and an antisymmetric part $A$ (which becomes
its own negative under that reflection):

$$J = S + A,\qquad S = \tfrac{1}{2}(J + J^{\mathsf T}),\qquad A = \tfrac{1}{2}(J - J^{\mathsf T})$$

where $J^{\mathsf T}$ is $J$ reflected across its diagonal. Reading the geometry off
$S$ and $A$ gives the three parts of the blob's motion:

**(1) Expansion — the trace.** The [[matrix-trace]] of $J$ is the sum of its diagonal
entries $\partial F_1/\partial x_1 + \partial F_2/\partial x_2 + \cdots$, each of which
is the rate at which one component grows along *its own* direction. By the trace's
basis-invariance, this sum is the net local rate at which the flow inflates volume —
the **divergence** of the field. (The antisymmetric part $A$ contributes nothing here:
it has all zeros on its diagonal, so $\operatorname{tr}(J) = \operatorname{tr}(S)$.)
This is the uniform-expansion piece: a positive trace means a dropped blob swells, a
negative trace means it shrinks.

**(2) Rotation — the antisymmetric part.** $A$ is a rigid spin: it turns the blob
without stretching it or changing its area, like a record on a turntable. Because an
antisymmetric matrix is forced to have a zero diagonal and to make each below-diagonal
entry the negative of the one above, it stores very few independent numbers — in two
dimensions, just one. That lone free entry *is* the flow's spin rate, the **curl**. So
the curl is literally read out of the Jacobian's antisymmetric part.

**(3) Shear/strain — the off-diagonal of the symmetric part.** What remains is the
*off-diagonal* of $S$. This is the piece the named operators do not give a single
symbol to. It distorts a small circle of fluid into an ellipse — stretching it along
one diagonal direction while squeezing it along the perpendicular one — *without*
rotating it and *without* changing its area. (The diagonal of $S$ carries the
per-axis stretching that the trace already summed; the off-diagonal is the pure shear
on top of that.)

So divergence and curl are **two readouts of the same Jacobian** — its trace and its
antisymmetric part — and shear is the third piece, the one the operator zoo never
names. One matrix of partial derivatives, decomposed once, answers three physically
distinct questions: how does the flow inflate, how does it spin, how does it distort.

**Worked instance.** Take a concrete 2-D flow whose velocity field is

$$F(x,y) = \big(\,2x + 3y,\;\; x + 4y\,\big),$$

so $F_1 = 2x + 3y$ and $F_2 = x + 4y$. Its Jacobian collects the four first partials.
Row 1 holds the partials of $F_1$: $\partial F_1/\partial x = 2$ and
$\partial F_1/\partial y = 3$. Row 2 holds the partials of $F_2$:
$\partial F_2/\partial x = 1$ and $\partial F_2/\partial y = 4$. So

$$J = \begin{bmatrix} 2 & 3 \\ 1 & 4 \end{bmatrix}.$$

(This field is linear, so its Jacobian is the same constant matrix at every point,
which keeps the numbers clean; for a curved field the same recipe is evaluated point
by point.) Now decompose. The transpose $J^{\mathsf T}$ swaps the two off-diagonal
entries $3$ and $1$, leaving the diagonal alone:

$$J^{\mathsf T} = \begin{bmatrix} 2 & 1 \\ 3 & 4 \end{bmatrix}.$$

The symmetric part adds and halves entrywise — $2{+}2{=}4$, $3{+}1{=}4$, $1{+}3{=}4$,
$4{+}4{=}8$, then halve:

$$S = \tfrac{1}{2}\begin{bmatrix} 4 & 4 \\ 4 & 8 \end{bmatrix} = \begin{bmatrix} 2 & 2 \\ 2 & 4 \end{bmatrix}.$$

The antisymmetric part subtracts and halves — $2{-}2{=}0$, $3{-}1{=}2$, $1{-}3{=}{-}2$,
$4{-}4{=}0$, then halve:

$$A = \tfrac{1}{2}\begin{bmatrix} 0 & 2 \\ -2 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}.$$

These reassemble correctly: $S + A$ entrywise is $2{+}0,\,2{+}1,\,2{-}1,\,4{+}0 =
2,3,1,4$, the original $J$. Now read off the three parts with numbers:

- **Expansion (trace → divergence):** $\operatorname{tr}(J) = 2 + 4 = 6$, a positive
  number — the flow inflates a tiny blob at a net rate of $6$ per unit time. This is
  the divergence of $F$.
- **Rotation (antisymmetric part → curl):** $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$
  has one independent entry, $1$. That entry is (half) the curl, so the flow spins the
  blob rigidly with a single definite rate while everything else happens.
- **Shear (off-diagonal of $S$):** the off-diagonal of $S$ is $2$. This squashes a
  small circle of fluid into an ellipse — stretching along one diagonal, compressing
  along the other — with no rotation and no area change. It is the leftover that
  neither the divergence nor the curl captures.

One $2 \times 2$ matrix of partial derivatives, split once, telling all three stories
at once: it inflates ($6$), spins (rate $1$), and shears ($2$).

## Prerequisites

- [[partial-derivative]]
- [[matrix-trace]]
- [[symmetric-antisymmetric-decomposition]]
- [[vector-field]]
- [[differential]]

## Sources

- `etc/differential-operators-summary.html` — the Jacobian as "every first partial —
  the full derivative"; divergence and curl "read out of the Jacobian" as "its trace
  and its antisymmetric part"; and the flow-geometry paragraph: "the Jacobian of a
  flow splits a tiny blob's motion into three parts: uniform expansion (the
  divergence), rigid rotation (the curl), and shear (the leftover, which distorts a
  circle into an ellipse)."
