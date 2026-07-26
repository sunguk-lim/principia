---
id: cross-product
title: Cross Product
summary: The cross product $u \times v$ takes two vectors in ordinary three-dimensional space and returns a third vector — one that points perpendicular to both inputs, whose length equals…
type: concept
tags: [math/linear-algebra]
prereqs: [vector-dot-product]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Cross Product

## Summary

The **cross product** $u \times v$ takes two vectors in ordinary three-dimensional
space and returns a third **vector** — one that points perpendicular to both inputs,
whose length equals the area of the parallelogram the two inputs span. Where the
[[vector-dot-product]] collapses two vectors into a single number measuring how much
they point the *same* way, the cross product builds a new arrow measuring how much
they point in *different* directions — how strongly they spread out a patch of plane.

## Grounded explanation

Fix the setting. A vector here is a triple of real numbers $u = (u_1, u_2, u_3)$,
an arrow in three-dimensional space; its **length** (or magnitude) $\lVert u \rVert$
is how long that arrow is, and the **angle** $\theta$ between two vectors is the
opening between them, from $0$ (same direction) to $\pi$ (opposite). These are the
same ingredients the [[vector-dot-product]] uses: recall it produces a single number
$u \cdot v = \lVert u \rVert\, \lVert v \rVert \cos\theta$, largest when the vectors
are aligned and zero when they are perpendicular. Hold that picture, because the
cross product is its mirror image.

**What the cross product is.** The cross product $u \times v$ is again a *vector*,
not a number. It is pinned down by three facts, and the whole concept is just these
three facts working together:

1. **Direction — perpendicular to both.** $u \times v$ is at right angles to $u$ and
   to $v$ at once; it sticks straight out of the flat plane those two arrows lie in.
   This is exactly the information the [[vector-dot-product]] *discards*: the dot
   product tells you alignment within the shared plane, while the cross product steps
   *out* of that plane entirely.

2. **Magnitude — the area they span.** Its length is
   $\lVert u \times v \rVert = \lVert u \rVert\, \lVert v \rVert \sin\theta$. Two
   arrows from a common origin frame a parallelogram, and this number is precisely
   that parallelogram's area. Notice the swap: the dot product carries $\cos\theta$,
   which peaks when the vectors coincide; the cross product carries $\sin\theta$,
   which peaks when they are perpendicular. That single swap of $\cos$ for $\sin$ is
   why the dot product measures *alignment* and the cross product measures *spread*.
   Two arrows pointing the same way enclose no area ($\sin 0 = 0$); two arrows at a
   right angle enclose the most.

3. **Orientation — the right-hand rule.** Facts 1 and 2 leave one ambiguity: a line
   perpendicular to the plane points two opposite ways, and a given area could be
   either. The choice is fixed by the *right-hand rule* — point your right hand's
   fingers along $u$, curl them toward $v$, and your thumb points along
   $u \times v$. This is a convention, but a consistent one, and it forces a striking
   property: $u \times v = -\,(v \times u)$. Swapping the inputs reverses which way
   you curl your fingers, so the thumb flips. The cross product is therefore
   **anti-commutative** — order matters, and reversing it negates the result. The
   [[vector-dot-product]] has no such issue: $u \cdot v = v \cdot u$, because a plain
   number has no "side" to flip.

**Why the magnitude rule forces the parallel case to vanish.** When $u$ and $v$ point
the same way (or exactly opposite), $\theta$ is $0$ (or $\pi$), so $\sin\theta = 0$
and the length is zero — the cross product is the zero vector. This is not an edge-case
nuisance; it is the meaning. Parallel arrows span a flat, degenerate parallelogram with
no area, and "no area" *is* "zero vector." So the cross product doubles as a test:
$u \times v = 0$ exactly when $u$ and $v$ are parallel, just as $u \cdot v = 0$ exactly
when they are perpendicular. The two products probe opposite relationships.

**Computing it.** From the three facts, the coordinate formula for
$u = (u_1, u_2, u_3)$ and $v = (v_1, v_2, v_3)$ is
$$u \times v = (\,u_2 v_3 - u_3 v_2,\ \ u_3 v_1 - u_1 v_3,\ \ u_1 v_2 - u_2 v_1\,).$$
Each component is a small cross-difference of two products — and you can see the
anti-commutativity already in the algebra: swap $u$ and $v$ and every term flips sign.

**Worked instance.** Take the two unit arrows along the first two axes,
$u = (1, 0, 0)$ and $v = (0, 1, 0)$ — perpendicular, each of length $1$. Feed them to
the formula component by component:

- first component: $u_2 v_3 - u_3 v_2 = (0)(0) - (0)(1) = 0$;
- second component: $u_3 v_1 - u_1 v_3 = (0)(0) - (1)(0) = 0$;
- third component: $u_1 v_2 - u_2 v_1 = (1)(1) - (0)(0) = 1$.

So $u \times v = (0, 0, 1)$ — the unit arrow along the *third* axis. Check it against
the three facts. It is perpendicular to both inputs (it points "up," out of the plane
the first two axes lie in). Its length is $1$, matching the area
$\lVert u \rVert \lVert v \rVert \sin\theta = (1)(1)\sin 90^\circ = 1$ of the unit
square they span. And the right-hand rule confirms the sign: fingers along the first
axis curling toward the second, thumb up. Reversing the order,
$v \times u = (0, 0, -1)$, points down — the promised anti-commutativity.

Now the contrasting degenerate case, to see fact 2 bite. Cross a vector with itself:
$u \times u = (1,0,0) \times (1,0,0)$. Every component is a difference of two *equal*
products — first: $(0)(0)-(0)(0)=0$; second: $(0)(1)-(1)(0)=0$; third:
$(1)(0)-(0)(1)=0$ — giving $(0,0,0)$. A vector is perfectly parallel to itself, spans
no area, and the cross product is zero. (The [[vector-dot-product]] of a vector with
itself does the opposite: $u \cdot u = \lVert u \rVert^2$, its largest, since the
vector is perfectly aligned with itself.)

**Why this operation earns its own name.** Treated abstractly, there are only three
ways to multiply a vector by something: scale it by a number, take a dot product with
another vector (output: a number, measuring alignment), or take a cross product with
another vector (output: a vector, measuring spread and rotation). The cross product is
the third of these, and the only one whose output is itself a directed quantity — the
only product that captures *turning*. That is why it is the engine behind the notion of
**curl**: when a vector field describes a flowing fluid, applying this same cross-product
bookkeeping to a vector of derivatives extracts how fast the flow is spinning at each
point, and which axis it spins about — a rotation, which only a perpendicular,
right-hand-oriented vector can name. The dot product, lacking direction, could never do
this; capturing rotation is precisely the gap the cross product fills.

## Prerequisites

- [[vector-dot-product]]

## Sources

- `etc/differential-operators-summary.html` — frames dot and cross as two of the
  "three products" a vector admits, and the cross product as the operation behind
  curl ($\nabla \times F$).
