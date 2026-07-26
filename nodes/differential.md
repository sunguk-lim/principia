---
id: differential
title: Differential (Total Derivative)
summary: "The differential $Df$ of a scalar function $f$ of several inputs is its full (total) first derivative: a single row of numbers, the partial-derivatives laid side by side, that…"
type: concept
tags: [math/calculus]
prereqs: [partial-derivative]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Differential (Total Derivative)

## Summary

The **differential** $Df$ of a scalar function $f$ of several inputs is its *full* (total)
first derivative: a single **row** of numbers, the [[partial-derivative]]s laid side by side,
that behaves as a *linear map* — feed it a direction and it returns the rate at which $f$
changes along that direction, the best straight-line estimate of how $f$ moves near a point.

## Grounded explanation

A [[partial-derivative]] answers a *narrow* question: how fast does $f$ change if I nudge
**one** input and freeze the rest? For a function of several inputs there is one such number
per input — $\partial f/\partial x_1,\ \partial f/\partial x_2,\ \dots,\ \partial f/\partial x_n$
(here $f$ is the function, $x_1,\dots,x_n$ are its $n$ input slots, and $n$ is how many inputs it
takes). Each one looks down a single coordinate axis. But real motion is rarely along one axis: you
might step in a direction that changes *several* inputs at once. The differential is the object that
answers the *full* question — change $f$ in **any** direction — and it does so by packaging all the
partials into one thing.

**The central object: a row that is a machine, not a list.** The differential $Df$ is written

$$Df = \left[\ \frac{\partial f}{\partial x_1}\quad \frac{\partial f}{\partial x_2}\quad \cdots\quad \frac{\partial f}{\partial x_n}\ \right]$$

— the partials written *across*, as a single row. The point is not that they are collected (you
could collect them many ways); it is what this row *does*. It is a **linear map**: a rule that
"eats" a direction and returns a number, and that respects scaling and addition (doubling the
direction doubles the output; the output for a sum of directions is the sum of the outputs). A
*direction* here is a vector $v = (v_1, \dots, v_n)$, one component per input slot, saying how much
each input is being nudged. The map acts by pairing the row against $v$ term-by-term and summing:

$$Df(v) = \frac{\partial f}{\partial x_1}\,v_1 + \frac{\partial f}{\partial x_2}\,v_2 + \cdots + \frac{\partial f}{\partial x_n}\,v_n .$$

**Why this is the right object — the WHY.** Near a chosen point, a smooth $f$ is almost flat: zoom
in far enough and its graph is indistinguishable from a tilted plane. $Df(v)$ is the rise of that
plane when you walk along $v$. Concretely, if you start at a point and take the small step $v$, then

$$f(\text{point} + v)\ \approx\ f(\text{point}) + Df(v),$$

and this approximation is the *best possible* linear one — the unique linear map whose error
shrinks faster than the step length as the step goes to zero. That is exactly why the partials must
combine *linearly*: each $v_i$ contributes its own slot's rate $\partial f/\partial x_i$ scaled by
how far that slot moved, and the contributions simply add. The differential is the whole-tangent-plane
generalization of the single-axis slope a [[partial-derivative]] gives.

**Differential vs gradient — a row or a column?** This is the distinction worth getting right. The
**gradient**, written $\nabla f$, holds the *same* partial derivatives — but stacked into a **column**
instead of a row. Same numbers, different object. The reason they are different objects is a general
shape convention: **rows = outputs, columns = inputs**. A derivative is laid out as a grid with one
row per output of the function and one column per input. A *scalar* function has exactly **one**
output, so its derivative has exactly **one row** — that single row is the differential. The gradient
is its **transpose**: take the row and tip it on its side into a column. Why bother keeping both? Because
a *row* and a *column* play different roles. The differential (the row) is a **map that eats vectors**:
hand it a direction $v$ and it hands back a rate. The gradient (the column) **is itself a vector** — a
direction living in the input space, the one pointing most steeply uphill. They carry identical
information and are tied by the identity $Df(v) = \nabla f \cdot v$ (the row applied to $v$ equals the
gradient paired with $v$), but you should not conflate "a thing that acts on directions" with "a
direction." One is the machine; the other is the kind of object the machine eats.

**Worked instance.** Take $f(x,y) = x^2 y$, a function of two inputs $x$ and $y$. Its two
[[partial-derivative]]s: holding $y$ fixed, $\partial f/\partial x = 2xy$; holding $x$ fixed,
$\partial f/\partial y = x^2$. Evaluate at the point $(x,y) = (1,2)$: $\partial f/\partial x = 2(1)(2) = 4$
and $\partial f/\partial y = (1)^2 = 1$. So the differential there is the **row**

$$Df = [\,4\quad 1\,],$$

while the gradient is its transpose, the **column** $\nabla f = \begin{bmatrix} 4 \\ 1 \end{bmatrix}$ —
same two numbers, tipped on their side. (This instance is non-degenerate: both partials are nonzero
and unequal, so neither slot drops out and the row/column distinction is visible rather than collapsed.)
Now apply the differential to the direction $v = (0.1,\ 0.2)$ — a small step that nudges $x$ by $0.1$
and $y$ by $0.2$ at once:

$$Df(v) = 4(0.1) + 1(0.2) = 0.4 + 0.2 = 0.6 .$$

Check it against the function directly. The actual change is $f(1.1,\ 2.2) - f(1,2)$. Now
$f(1.1, 2.2) = (1.1)^2(2.2) = (1.21)(2.2) = 2.662$ and $f(1,2) = (1)^2(2) = 2$, so the true change is
$2.662 - 2 = 0.662$. The differential predicted $0.6$ — close, with the small gap ($0.062$) being the
curvature the linear map cannot see. That is the differential doing its one job: turning the
direction $v$ into the best linear estimate of how $f$ moves.

## Prerequisites

- [[partial-derivative]]

## Sources

- etc/differential-operators-summary.html
