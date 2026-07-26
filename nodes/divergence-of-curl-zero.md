---
id: divergence-of-curl-zero
title: Divergence of a Curl is Zero
summary: "For any vector field $F$, the divergence of its curl is exactly zero: $\\nabla \\cdot (\\nabla \\times F) = 0$."
type: concept
tags: [math/calculus]
prereqs: [divergence, curl, partial-derivative, vector-field]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Divergence of a Curl is Zero

## Summary

For *any* [[vector-field]] $F$, the [[divergence]] of its [[curl]] is exactly zero:
$\nabla \cdot (\nabla \times F) = 0$. A curl field can never spread out or
converge — it has no sources and no sinks anywhere. Such a field is called
**solenoidal** (or *source-free*). The flip side is just as useful: if a field
has nonzero divergence somewhere, it cannot be written as the curl of anything.

## Grounded explanation

The two operators in play are already known. The [[curl]] of a field $F$ takes
each component-pair difference of partial derivatives and packs them into a new
vector; it is the *antisymmetric* part of how $F$ changes, the one operator
carrying minus signs. The [[divergence]] of a field takes that field's three
*diagonal* partials — the rate of change of each component along its own axis —
and adds them into a single scalar measuring net outflow.

The claim is that feeding the output of [[curl]] into [[divergence]] always
gives zero, no matter what $F$ is. To see *why*, follow the derivatives.

Write $F = (P, Q, R)$, naming its three component functions. Its [[curl]] is the
vector

$$\nabla \times F = \left(\frac{\partial R}{\partial y}-\frac{\partial Q}{\partial z},\ \ \frac{\partial P}{\partial z}-\frac{\partial R}{\partial x},\ \ \frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right).$$

Each component is a *mirror-pair* difference: one partial minus its mirror image
with the variables swapped. Now take the [[divergence]] of this vector — that
means differentiating its first component by $x$, its second by $y$, its third
by $z$, and adding the three results:

$$\nabla \cdot (\nabla \times F) = \frac{\partial}{\partial x}\!\left(\frac{\partial R}{\partial y}-\frac{\partial Q}{\partial z}\right) + \frac{\partial}{\partial y}\!\left(\frac{\partial P}{\partial z}-\frac{\partial R}{\partial x}\right) + \frac{\partial}{\partial z}\!\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right).$$

Expanding the six terms, every one is a *mixed second partial* — a [[partial-derivative]]
taken twice, once by each of two different variables. Here is the key step.
Mixed partials are equal regardless of the order you take them: differentiating
$R$ first by $y$ then by $x$ gives the same function as first by $x$ then by $y$,
written $\frac{\partial^2 R}{\partial x\,\partial y} = \frac{\partial^2 R}{\partial y\,\partial x}$. (This holds whenever the second
derivatives are continuous — true for any ordinary smooth field.) That equality
is the whole engine of the identity.

With that equality in hand, group the six terms by which component they came
from. The two terms in $R$ are $\frac{\partial^2 R}{\partial x\,\partial y}$ (from the first slot) and
$-\frac{\partial^2 R}{\partial y\,\partial x}$ (from the second). They are the same mixed partial with
*opposite* signs, so they cancel. The two terms in $Q$ are
$-\frac{\partial^2 Q}{\partial x\,\partial z}$ and $+\frac{\partial^2 Q}{\partial z\,\partial x}$ — again equal and opposite,
cancelling. The two in $P$, $+\frac{\partial^2 P}{\partial y\,\partial z}$ and $-\frac{\partial^2 P}{\partial z\,\partial y}$,
cancel too. Three cancelling pairs, sum zero.

The opposite signs are not luck: they are inherited from the minus signs that
*define* the [[curl]]. The [[curl]] builds each component as one partial minus
its mirror; the [[divergence]] then hits each of those mirrors with the matching
outer derivative, so every term meets its sign-flipped twin. This is the same
antisymmetry that makes the curl of a gradient vanish, applied one level down:
there, a symmetric object met an antisymmetric operator; here, an antisymmetric
object meets a symmetric one. Either way the symmetric and antisymmetric pieces
annihilate.

**Worked instance.** Take $F = (xy,\ yz,\ zx)$, so $P = xy$, $Q = yz$, $R = zx$ —
a field with genuine cross-coupling, not a degenerate one. First its [[curl]],
component by component:

- First slot: $\dfrac{\partial R}{\partial y} - \dfrac{\partial Q}{\partial z} = \dfrac{\partial (zx)}{\partial y} - \dfrac{\partial (yz)}{\partial z} = 0 - y = -y.$
- Second slot: $\dfrac{\partial P}{\partial z} - \dfrac{\partial R}{\partial x} = \dfrac{\partial (xy)}{\partial z} - \dfrac{\partial (zx)}{\partial x} = 0 - z = -z.$
- Third slot: $\dfrac{\partial Q}{\partial x} - \dfrac{\partial P}{\partial y} = \dfrac{\partial (yz)}{\partial x} - \dfrac{\partial (xy)}{\partial y} = 0 - x = -x.$

So $\nabla \times F = (-y,\ -z,\ -x)$. Now its [[divergence]] — differentiate
each component by its own axis and add:

$$\nabla \cdot (\nabla \times F) = \frac{\partial (-y)}{\partial x} + \frac{\partial (-z)}{\partial y} + \frac{\partial (-x)}{\partial z} = 0 + 0 + 0 = 0.$$

Each term vanishes because the curl handed the $x$-axis a component depending
only on $y$, the $y$-axis one depending only on $z$, and the $z$-axis one
depending only on $x$ — the cross-coupling that the mirror-differences leave
behind is always *off the diagonal*, exactly where the divergence does not look.
The result is zero, as the identity guarantees for every field.

## Prerequisites

- [[vector-field]]
- [[divergence]]
- [[curl]]
- [[partial-derivative]]

## Sources

- etc/differential-operators-summary.html
