---
id: directional-derivative
title: Directional Derivative
summary: The directional derivative of a scalar function $f$ (a function whose output is a single number) is the rate at which $f$ changes as you step away from a chosen point in a chosen…
type: concept
tags: [math/calculus]
prereqs: [partial-derivative, vector-dot-product, differential]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Directional Derivative

## Summary

The **directional derivative** of a scalar function $f$ (a function whose output
is a single number) is the rate at which $f$ changes as you step away from a
chosen point in a chosen direction $v$. It generalizes the [[partial-derivative]],
which only measures change along a coordinate axis, to any direction at all. Its
value is the [[vector-dot-product]] of the gradient of $f$ with the direction:
$D_v f = \nabla f \cdot v$.

## Grounded explanation

Start with the central object. A **scalar function** $f(x, y)$ takes a point in the
plane and returns one number — think of it as a height, so $f$ describes a surface
of hills and valleys above the $xy$-plane. Standing at a point, the question
"how steeply does the ground rise?" has no single answer: it depends on which way
you face. The **directional derivative** $D_v f$ is precisely that answer — the
slope of the surface as you walk in the direction given by the vector $v$. Here $v$
is taken to be a **unit vector** (length $1$), so the slope is measured per unit of
distance travelled and the direction alone, not the step size, sets the result.

This is a strict generalization of the [[partial-derivative]]. A partial
derivative $\partial f / \partial x$ is the rate of change of $f$ when only $x$
moves and the other inputs are held fixed — that is, the slope as you walk along
the $x$-axis. But "along the $x$-axis" is just one particular direction, the unit
vector $(1, 0)$. The directional derivative asks the same question for *any*
direction. So the partial derivatives are nothing but the directional derivatives
along the coordinate axes; the new concept is the whole family of slopes, of which
the partials are two special members.

Now the central formula and the **why** behind it. Collect the partial derivatives
of $f$ into a single vector called the **gradient**, written $\nabla f$: for
$f(x, y)$ it is $\nabla f = (\partial f / \partial x,\; \partial f / \partial y)$.
(The gradient is just this stacking of partial derivatives — every piece of it is
a [[partial-derivative]].) The [[differential]] $Df$ packages those same partials
as a *row* that acts as a linear map: $Df(v)$ feeds direction $v$ in and returns
the first-order change in $f$. The claim is that the slope in direction $v$ — that
is, $Df(v)$ — equals the [[vector-dot-product]] of the gradient with that direction:

$$D_v f = Df(v) = \nabla f \cdot v$$

Why does combining the per-axis slopes by a dot product give the slope in a slanted
direction? Because a small step in direction $v = (v_x, v_y)$ is simultaneously a
step of $v_x$ along the $x$-axis and $v_y$ along the $y$-axis. The change in height
contributed by the $x$-part is (its slope) times (how far you went in $x$), namely
$(\partial f / \partial x)\, v_x$; likewise the $y$-part contributes
$(\partial f / \partial y)\, v_y$. The total change is their sum,
$(\partial f / \partial x)\, v_x + (\partial f / \partial y)\, v_y$ — and a sum of
matched products *is* exactly the [[vector-dot-product]] $\nabla f \cdot v$. The dot
product is the bookkeeping that adds up the contributions from each axis.

This formula immediately answers a deeper question: of all directions, which one is
steepest? Recall that the [[vector-dot-product]] also equals
$\lVert \nabla f \rVert \, \lVert v \rVert \cos\theta$, where $\lVert \cdot \rVert$
denotes a vector's length and $\theta$ is the angle between $\nabla f$ and $v$.
Since $v$ is a unit vector, $\lVert v \rVert = 1$, so
$D_v f = \lVert \nabla f \rVert \cos\theta$. The length $\lVert \nabla f \rVert$ is
fixed at the point; only $\cos\theta$ varies with the direction you choose, and
$\cos\theta$ is largest (equal to $1$) when $\theta = 0$ — that is, when $v$ points
the *same way* as the gradient. So the steepest uphill direction is the direction of
$\nabla f$ itself, and the steepest slope is its magnitude $\lVert \nabla f \rVert$.
That is the justification for the often-stated fact that **the gradient points uphill**:
it is not a separate axiom but a direct consequence of the directional derivative being
a dot product.

A concrete worked instance. Let $f(x, y) = x^2 + y^2$ (a bowl-shaped surface). Its
partial derivatives are $\partial f / \partial x = 2x$ and
$\partial f / \partial y = 2y$, so the gradient is $\nabla f = (2x, 2y)$. Evaluate at
the point $(1, 1)$: there $\nabla f = (2, 2)$. Now compare two directions.

Along the $x$-axis, $v = (1, 0)$ (already a unit vector). The directional derivative
is the dot product $D_v f = (2, 2) \cdot (1, 0) = 2\cdot 1 + 2\cdot 0 = 2$ — and note
this is exactly the partial derivative $\partial f / \partial x = 2x = 2$ at $(1,1)$,
confirming the partials as the axis-aligned special case.

Along the diagonal, the raw direction $(1, 1)$ has length $\sqrt{1^2 + 1^2} = \sqrt{2}$,
so its unit vector is $v = (1, 1)/\sqrt{2}$. Then
$D_v f = (2, 2) \cdot (1, 1)/\sqrt{2} = (2\cdot 1 + 2\cdot 1)/\sqrt{2} = 4/\sqrt{2}
\approx 2.83$. The diagonal slope $2.83$ is steeper than the axis slope $2$ — and that
is no accident: at $(1, 1)$ the gradient is $(2, 2)$, which points along the diagonal,
so the diagonal is the uphill direction and yields the largest slope, namely
$\lVert \nabla f \rVert = \sqrt{2^2 + 2^2} = \sqrt{8} = 4/\sqrt{2} \approx 2.83$. The
two computations agree, closing the loop between the dot-product formula and the
steepest-ascent insight.

## Prerequisites

- [[partial-derivative]]
- [[vector-dot-product]]
- [[differential]]

## Sources

- etc/differential-operators-summary.html
