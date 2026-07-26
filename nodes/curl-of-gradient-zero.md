---
id: curl-of-gradient-zero
title: Curl of a Gradient is Zero
summary: "For any scalar function $f$, the curl of its gradient is always the zero vector: $\\nabla \\times (\\nabla f) = 0$."
type: concept
tags: [math/calculus]
prereqs: [curl, gradient, hessian, partial-derivative, vector-field, differential-operators]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Curl of a Gradient is Zero

## Summary

For any scalar function $f$, the [[curl]] of its [[gradient]] is always the zero
vector: $\nabla \times (\nabla f) = 0$. A field that is built as a gradient can
never have any local spin — it is *irrotational*. The reason is that the derivative
matrix of a gradient is the [[hessian]], and the Hessian is symmetric, leaving curl
nothing to measure.

## Grounded explanation

The concept here is a single identity that holds no matter which scalar function
you start from: take any $f$ of several variables, form its [[gradient]] $\nabla f$
(the vector of [[partial-derivative]]s, which points uphill), then take the
[[curl]] of that [[vector-field]]. The result is always the zero vector. In words: a
field that is the gradient of *something* has zero curl everywhere. Such a field is
called *irrotational* (no rotation) or *conservative*. The whole point of the node
is not the bare fact $\nabla \times (\nabla f) = 0$ but **why** it is forced to hold.

To see why, line up what each operator measures. The [[curl]] of a vector field
takes mirror-pair differences of partial derivatives: each output component has the
form $\partial F_j/\partial x_i - \partial F_i/\partial x_j$, the difference between
how the $j$-th piece of the field changes along $x_i$ and how the $i$-th piece
changes along $x_j$. Curl is the only one of the [[differential-operators]] carrying
minus signs precisely because it isolates this *antisymmetric* part of the field's
derivative matrix — the part that survives only when those two cross-rates disagree.

Now substitute a gradient into that machine. The field is $F = \nabla f$, so its
$i$-th component is $F_i = \partial f/\partial x_i$. The derivative matrix of this
particular field — the matrix whose $(i,j)$ entry is $\partial F_i/\partial x_j$ —
is by definition the [[hessian]] of $f$, the matrix of second partial derivatives
$H_{ij} = \partial^2 f / \partial x_i\, \partial x_j$. So the very quantity curl
reaches into is the Hessian.

The justifying reason is one property of that matrix: **the Hessian is symmetric**.
Its mirror cells are equal, $\partial^2 f/\partial x_i\,\partial x_j =
\partial^2 f/\partial x_j\,\partial x_i$ — differentiating by $x_i$ then $x_j$ gives
the same result as the reverse order. (This commuting of mixed partials is
Clairaut's theorem; it holds whenever those second derivatives are continuous, which
is the ordinary case.) A symmetric matrix is its own mirror image, so it has **no
antisymmetric part**: every mirror-pair difference is a quantity minus an equal copy
of itself, which is zero. Curl measures exactly that antisymmetric part — and for a
symmetric matrix there is nothing left to measure. That is the mechanism: each curl
component of $\nabla f$ is a difference of two mixed partials that, by symmetry, are
equal, so each component cancels to zero.

Worked instance. Take $f(x,y,z) = x^2 y$. Its [[gradient]] is the vector of first
partials: $\partial f/\partial x = 2xy$, $\partial f/\partial y = x^2$, and
$\partial f/\partial z = 0$, so $\nabla f = (2xy,\ x^2,\ 0)$. Now take the [[curl]]
of this field, component by component, using $\nabla \times F = (\partial F_z/\partial y
- \partial F_y/\partial z,\ \partial F_x/\partial z - \partial F_z/\partial x,\
\partial F_y/\partial x - \partial F_x/\partial y)$ with $F_x = 2xy$, $F_y = x^2$,
$F_z = 0$. First component: $\partial F_z/\partial y - \partial F_y/\partial z =
\partial(0)/\partial y - \partial(x^2)/\partial z = 0 - 0 = 0$. Second component:
$\partial F_x/\partial z - \partial F_z/\partial x = \partial(2xy)/\partial z -
\partial(0)/\partial x = 0 - 0 = 0$. Third component — the interesting one, since
both terms are nonzero before they cancel: $\partial F_y/\partial x -
\partial F_x/\partial y = \partial(x^2)/\partial x - \partial(2xy)/\partial y =
2x - 2x = 0$. That last cancellation is a symmetric mirror pair made explicit: $2x$
is $\partial^2 f/\partial x\,\partial y$ computed one way ($f \to x^2 \to 2x$) and
$2x$ is the same second derivative computed in the other order ($f \to 2xy \to 2x$).
Equal mixed partials, so the difference vanishes. The curl is $(0,0,0)$, as the
identity guarantees.

This identity also runs the other way, and that converse is what makes it useful as
a test. If you compute the [[curl]] of some given vector field and get a *nonzero*
answer, then that field cannot be the [[gradient]] of any scalar function — because
if it were, its curl would have been forced to zero. A nonzero curl is a certificate
of non-conservativeness.

## Prerequisites

- [[curl]]
- [[gradient]]
- [[hessian]]
- [[partial-derivative]]
- [[vector-field]]

## Sources

- etc/differential-operators-summary.html
