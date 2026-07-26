---
id: vector-field
title: Vector Field
summary: A vector field is a rule that pins a little arrow to every point of a space.
type: concept
tags: [math/calculus]
prereqs: [arithmetic, scalar-field]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# Vector Field

## Summary

A vector field is a rule that pins a little arrow to every point of a space. At each
location you stand, the rule hands you not a single number but a whole *arrow* — a
quantity with both a size and a direction. Picture the wind over a map: at every spot
the wind has a speed and a heading, so the wind *is* a vector field. Contrast this with
a scalar field, which attaches just one number to each point (the temperature at every
spot on the same map). The vector field is the carrier of "a directed quantity that
varies from place to place," and it is the kind of object that the machinery of vector
calculus — divergence, curl, the Jacobian — is built to chew on.

## Grounded explanation

Start with what a *vector* is, since the whole idea rests on it. A number on its own —
say `3` — is a **scalar**: a bare magnitude, the sort of thing the four operations of
[[arithmetic]] act on directly. A **vector** is an ordered list of such numbers written
together, like `(0, 1)` or `(−1, 0)`, and that list carries a richer meaning: it names
both a direction and a length. In two dimensions you read `(a, b)` as "go `a` steps east
and `b` steps north," which traces out an arrow from the origin to the spot `a` east and
`b` north. So `(0, 1)` is an arrow of length one pointing straight up; `(−1, 0)` is an
arrow of length one pointing left. The two slots are just numbers, so everything we ever
*do* to a vector — stretch it, add two of them, compare them — bottoms out in the
[[arithmetic]] of those slots.

Now the central object. A **field** is the idea of attaching some value to *every point*
of a space at once, the value being allowed to differ from point to point. Attach a
single number to each point and you have a **[[scalar-field]]** — a temperature reading at
every location. Attach a whole vector to each point and you have a **vector field**. So a
vector field is a function: you feed it a point — a location, itself written as a list of
coordinate numbers like `(x, y)` — and it returns a vector, an arrow, anchored at that
point. Written compactly, a vector field in the plane is a rule `F` that takes a
two-number input `(x, y)` and produces a two-number output, the components of the arrow
sitting there. In `n`-dimensional space it takes `n` numbers in and gives `n` numbers
out, which is what the shorthand `F: ℝⁿ → ℝⁿ` records: same count going in as coming out,
a point mapped to an arrow living in the same kind of space.

Here is **why** the matching counts matter, and why this is the natural input type for
the rest of vector calculus. The input and output have the same number of slots because
the arrow is meant to live *at* the point — it is the velocity of the fluid right there,
the pull of the force right there. That shared dimensionality is exactly the structure
that lets later operators ask geometric questions of a field: *is the field spreading
apart or piling up near this point* (divergence), *is it swirling around this point*
(curl). Those questions only make sense because at every point there is a fresh arrow to
compare against its neighbours; a single number per point (a scalar field) has no
direction to spread or swirl, so it cannot be asked them in the same way. The vector
field is the "directed" half of the basic split that organizes the whole subject: an
operator either starts *from a scalar function* `f` (one number per point) or *from a
vector field* `F` (one arrow per point). Knowing which half you are in tells you what the
operator can even mean.

Work a concrete instance to see an arrow actually vary across space. Take the rule
`F(x, y) = (−y, x)`. It accepts a point `(x, y)` and returns the vector whose first slot
is `−y` and whose second slot is `x` — each output slot built from the input slots by the
sign-flip and copy of [[arithmetic]]. Evaluate it at four points, deriving every number:

- At `(1, 0)`: first slot `−y = −0 = 0`, second slot `x = 1`, so `F = (0, 1)` — an arrow
  of length one pointing **up**.
- At `(0, 1)`: first slot `−y = −1`, second slot `x = 0`, so `F = (−1, 0)` — an arrow of
  length one pointing **left**.
- At `(−1, 0)`: first slot `−y = −0 = 0`, second slot `x = −1`, so `F = (0, −1)` — an
  arrow pointing **down**.
- At `(0, −1)`: first slot `−y = −(−1) = 1`, second slot `x = 0`, so `F = (1, 0)` — an
  arrow pointing **right**.

Place those four arrows at their four points: at the east point it points north, at the
north point it points west, at the west point it points south, at the south point it
points east. Each arrow is tangent to the circle through its point, and they all march
the same way around — counterclockwise. The field *circulates*. This is the canonical
rotational field, and it is non-degenerate precisely because the arrow genuinely turns as
you move from point to point rather than staying fixed or vanishing; that turning is what
gives it a nonzero "swirl" while it neither spreads out nor piles up. Notice also what
makes it a vector field and not a scalar field: at `(1, 0)` the answer is the arrow
`(0, 1)`, two coordinated numbers naming a direction — not a lone reading like a
temperature. That is the whole distinction made concrete.

## Prerequisites

- [[arithmetic]]

## Sources

- `etc/differential-operators-summary.html` — the input split "from a scalar function
  `f`" versus "from a vector field `F`", with `F: ℝ³ → ℝ³`, and the framing of divergence,
  curl, and the Jacobian as operators that take a vector field as input.
