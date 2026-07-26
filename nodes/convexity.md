---
id: convexity
title: Convexity
summary: "A function is convex when its graph curves upward like a bowl: every straight line drawn between two points on the graph stays on or above the graph, the function never dips below…"
type: concept
tags: [math/calculus]
prereqs: [derivative]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Convexity

## Summary

A function is **convex** when its graph curves upward like a bowl: every straight
line drawn between two points on the graph stays on or above the graph, the
function never dips below any of its own tangent lines, and its slope only ever
increases. The single payoff is **Jensen's inequality** — "the function of an
average is at most the average of the function."

## Grounded explanation

### What we mean by a function and by "above"

A **function** $f$ takes an input number $x$ and returns an output number $f(x)$;
its **graph** is the set of points $(x, f(x))$ plotted on a plane, with the input
on the horizontal axis and the output on the vertical axis. When we say one curve
is "above" another, we mean: at the same horizontal position $x$, its vertical
($f(x)$) value is larger.

### View (a): the chord lies on or above the graph

Pick two inputs $a$ and $b$ with $a < b$. The **chord** is the straight line
segment joining the two graph points $(a, f(a))$ and $(b, f(b))$. Any input
between $a$ and $b$ can be written as a **weighted average** of the endpoints:
choose a weight $t$ with $0 \le t \le 1$ and form

$$x = (1-t)\,a + t\,b.$$

Here $t$ slides the point from $a$ (when $t=0$) to $b$ (when $t=1$); the two
weights $1-t$ and $t$ are each at least zero and sum to $1$, so $x$ really does
sit between $a$ and $b$. The height of the **chord** above that $x$ is the *same*
weighted average of the endpoint heights, $(1-t)\,f(a) + t\,f(b)$ (a straight line
interpolates its endpoints linearly — this is just arithmetic). The function $f$
is **convex** exactly when the actual graph height never exceeds the chord height:

$$f\big((1-t)\,a + t\,b\big) \;\le\; (1-t)\,f(a) + t\,f(b)
\qquad\text{for every } 0 \le t \le 1.$$

This is the definition. The bowl shape is the picture of it: stretch a string
between any two points of a bowl and the string hangs above the bowl's floor.

### View (b): the function lies above its tangent lines

A **tangent line** at an input $x_0$ is the straight line that touches the graph
at $(x_0, f(x_0))$ and has the same slope there — and that slope is precisely the
[[derivative]] $f'(x_0)$, the instantaneous rate of change of $f$ at $x_0$. The
tangent line's height at any input $x$ is

$$\text{tangent}(x) = f(x_0) + f'(x_0)\,(x - x_0),$$

i.e. start at the touch height $f(x_0)$ and add slope $\times$ horizontal travel.
For a convex function the graph never dips below any tangent line:
$f(x) \ge f(x_0) + f'(x_0)(x - x_0)$ for all $x$. A bowl always sits above the flat
ruler you rest against its side. This view is the bridge to optimization: if the
slope $f'(x_0) = 0$ at some point, the tangent is horizontal at height $f(x_0)$,
and since the whole graph lies above that horizontal line, $f(x_0)$ is the
**global minimum** — a flat spot of a convex function cannot be a mere local dip.

### View (c): the second derivative is non-negative — and why it ties the others together

The [[derivative]] $f'$ is itself a function of $x$ (the slope at each point). Take
its [[derivative]] again to get the **second derivative** $f''$ — the rate of
change *of the slope*. This is the justifying identity that unifies the three
views:

> $f$ is convex $\iff$ $f''(x) \ge 0$ everywhere.

The *why*: $f'' \ge 0$ says the slope $f'$ is **non-decreasing** as $x$ moves
right (a quantity whose rate of change is never negative never goes down). A slope
that only steepens — gentle, then steep — is exactly a curve that bends upward,
which is exactly the bowl of view (a) and the lie-above-tangents property of view
(b). Reading it backward: if the slope ever *fell*, the curve would bulge upward
over a chord and the chord would cut below it, breaking convexity. So "second
[[derivative]] never negative" and "curves upward" are the same statement, and a
non-negative curvature is what forces both the chord and the tangent conditions to
hold.

### The payoff: Jensen's inequality

View (a) compared the graph to a chord between **two** points. The same upward
curving lets us average **many** points at once. Take inputs $x_1, x_2, \dots,
x_n$ and **weights** $w_1, w_2, \dots, w_n$ that are each non-negative
($w_i \ge 0$) and sum to one ($w_1 + w_2 + \cdots + w_n = 1$). The **weighted
average** of the inputs is $\bar{x} = w_1 x_1 + w_2 x_2 + \cdots + w_n x_n$. Then
for any convex $f$:

$$f\!\left(\sum_{i} w_i\, x_i\right) \;\le\; \sum_{i} w_i\, f(x_i)
\qquad\text{(Jensen's inequality)}.$$

In words: **$f$ of the average is at most the average of $f$.** The two-point
chord inequality of view (a) is the special case $n=2$ with weights $1-t$ and $t$;
piling on more points (each new one again landing on or above the relevant chord)
extends it to any number of weighted points. *(When the weights are read as a
probability distribution over a random quantity $X$, this is written
$f(E[X]) \le E[f(X)]$ — the same statement, used elsewhere in the brain.)*

### Concave: the mirror image

A function is **concave** when it curves the *other* way — a dome instead of a
bowl. Everything flips: $f'' \le 0$ (slope non-increasing), the graph lies on or
*below* its chords and tangents, and Jensen reverses to
$f(\sum_i w_i x_i) \ge \sum_i w_i f(x_i)$. A straight line, $f'' = 0$, is the
boundary case: it is both convex and concave, and Jensen holds with **equality**.

### Worked instance

Take $f(x) = x^2$. Its [[derivative]] is $f'(x) = 2x$ (the slope), and the
[[derivative]] of that is $f''(x) = 2$. Since $2 \ge 0$ everywhere, $f$ is
**convex** — and strictly so, because the curvature is genuinely positive, not
zero. Now check Jensen with two points $x_1 = 1$ and $x_2 = 3$ and equal weights
$w_1 = w_2 = \tfrac{1}{2}$ (non-negative, summing to $1$).

- **Left side — $f$ of the average.** The weighted average is
  $\bar{x} = \tfrac{1}{2}\cdot 1 + \tfrac{1}{2}\cdot 3 = 2$, so
  $f(\bar{x}) = 2^2 = 4$.
- **Right side — average of $f$.** $f(1) = 1$ and $f(3) = 9$, so the average is
  $\tfrac{1}{2}\cdot 1 + \tfrac{1}{2}\cdot 9 = \tfrac{1 + 9}{2} = 5$.

Jensen predicts $4 \le 5$ — true, and **strict** ($4 < 5$), as a strictly convex
function demands when the points differ. The gap of $1$ is the upward bulge of the
parabola pulling the curve below the chord at $x = 2$.

For contrast, take the **linear** $f(x) = 2x + 1$ (so $f'' = 0$, the boundary
case). With the same $x_1 = 1$, $x_2 = 3$, equal weights: the average input is
$2$, giving $f(2) = 5$; the inputs give $f(1) = 3$ and $f(3) = 7$, averaging to
$\tfrac{3 + 7}{2} = 5$. Both sides equal $5$, so Jensen holds with **equality** —
exactly as expected when there is no curvature to create a gap. (A concave
example such as $f(x) = \sqrt{x}$, with $f'' < 0$, would instead make $f$ of the
average *exceed* the average of $f$, the inequality flipped.)

## Prerequisites

- [[derivative]]

## Sources

_none_
