---
id: del-operator
title: Del operator (∇)
summary: The del operator $\nabla$ is a formal vector — a vector whose three entries are not numbers but instructions to differentiate.
type: concept
tags: [math/calculus]
prereqs: [partial-derivative, vector-dot-product, cross-product]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-18
updated: 2026-06-25
---

# Del operator (∇)

## Summary

The **del operator** $\nabla$ is a *formal vector* — a vector whose three entries are
not numbers but **instructions to differentiate**. Written out, it is
$\nabla = \left(\tfrac{\partial}{\partial x},\ \tfrac{\partial}{\partial y},\ \tfrac{\partial}{\partial z}\right)$.
Its point is economy: a single object that, when "multiplied" with a function or a
field the three ways a vector can multiply, produces the entire family of first-order
differential operators of vector calculus.

## Grounded explanation

**The building block.** Each entry of $\nabla$ is a [[partial-derivative]] operator —
$\tfrac{\partial}{\partial x}$ means "measure how the input changes as $x$ moves, holding
the other variables fixed." On its own, $\tfrac{\partial}{\partial x}$ is incomplete: it is
a verb waiting for an object. Only when you hand it a function $f$ does it produce a
number-valued thing, $\tfrac{\partial f}{\partial x}$. Stacking the three coordinate
partials side by side gives $\nabla$.

**Why call it a "formal vector."** $\nabla$ looks like a vector $(a, b, c)$, but $a, b, c$
here are operators, not real numbers. The word *formal* flags exactly this: it has the
*form* of a vector, and we are allowed to push the symbols around using the algebra of
vectors, even though its slots hold instructions. The price of this convenience is that
one phrase changes meaning. When the rules of vectors tell you to "multiply" an entry of
$\nabla$ by a piece of the field, **"multiply" does not mean arithmetic — it means
*apply*.** Writing $\tfrac{\partial}{\partial x}\cdot f$ does not multiply two numbers; it
applies the operator $\tfrac{\partial}{\partial x}$ to the function $f$, yielding
$\tfrac{\partial f}{\partial x}$.

**Why this substitution is legitimate.** It is not a sloppy abuse of notation; it works for
a precise reason. The vector products — scalar multiplication, the [[vector-dot-product]],
and the [[cross-product]] — are built by **distributing** a multiplication across sums and
pulling scalar factors out front. (Recall the dot product $a\cdot b = \sum_i a_i b_i$ is a
sum of products; the cross product's entries are differences of products.) Differentiation
obeys those same two laws: it is **linear**. That is,
$\tfrac{\partial}{\partial x}(f + g) = \tfrac{\partial f}{\partial x} + \tfrac{\partial g}{\partial x}$
(it distributes over sums), and
$\tfrac{\partial}{\partial x}(cf) = c\,\tfrac{\partial f}{\partial x}$ for a constant $c$
(scalars pull out). Because "apply $\tfrac{\partial}{\partial x}$" follows the exact
bookkeeping rules that "multiply by a number" follows, every step of dot- and cross-product
algebra still goes through with *apply* swapped in for *multiply*. Linearity is the bridge
that lets $\nabla$ masquerade as a vector.

**The one catch: order matters.** Ordinary multiplication of numbers commutes — $3\times 5 =
5\times 3$. Applying an operator does **not** commute, and this is where the formal-vector
disguise must be read carefully. Compare two arrangements of the same symbols:
$\tfrac{\partial}{\partial x}\,f$ means "differentiate $f$ with respect to $x$," giving the
function $\tfrac{\partial f}{\partial x}$. But $f\,\tfrac{\partial}{\partial x}$ means
"first multiply by $f$, then differentiate whatever comes next" — that is still an operator,
a verb waiting for an object, not a finished function. The two are different *kinds of
thing*. The rule that resolves all such ambiguity is simple: **$\nabla$ always acts to its
right.** It is hungry, and it eats the field written after it.

**The three products — the payoff.** A vector can be multiplied exactly three ways, and
$\nabla$ inherits all three. Let $f$ be a scalar function (one number out per point) and let
$F = (F_1, F_2, F_3)$ be a *vector field* (a vector out per point — for instance, the
velocity of a flowing fluid). Then:

- **Scalar multiplication.** Multiplying the vector $\nabla$ by the scalar $f$ scales each
  entry, i.e. applies each partial to $f$:
  $\nabla f = \left(\tfrac{\partial f}{\partial x},\ \tfrac{\partial f}{\partial y},\ \tfrac{\partial f}{\partial z}\right)$.
  This is the **gradient** — a vector pointing in the direction $f$ increases fastest.
  (The gradient is the column-vector transpose of the differential $Df$, the row form of those
  same partials; they carry identical information but play opposite roles: $Df$ is a map that eats
  directions, $\nabla f$ is itself a direction.)

- **Dot product.** The [[vector-dot-product]] pairs matching entries and sums them. Pairing
  $\tfrac{\partial}{\partial x}$ with $F_1$ means *apply* it, so
  $\nabla\cdot F = \tfrac{\partial F_1}{\partial x} + \tfrac{\partial F_2}{\partial y} + \tfrac{\partial F_3}{\partial z}$.
  The dot product always returns a single number, so this is a **scalar** field — the
  **divergence**, measuring how much the field spreads outward at each point.

- **Cross product.** The [[cross-product]] of two vectors returns a third vector built from
  cross-differences of entries. With *apply* in place of multiply,
  $\nabla\times F = \left(\tfrac{\partial F_3}{\partial y} - \tfrac{\partial F_2}{\partial z},\ \ \tfrac{\partial F_1}{\partial z} - \tfrac{\partial F_3}{\partial x},\ \ \tfrac{\partial F_2}{\partial x} - \tfrac{\partial F_1}{\partial y}\right)$.
  The cross product returns a vector, so this is a **vector** field — the **curl**, measuring
  how fast and about which axis the field rotates.

One operator, three multiplications, three different operators out. That is the whole engine.

**Worked instance.** Write $\nabla$ in three dimensions:
$$\nabla = \left(\frac{\partial}{\partial x},\ \frac{\partial}{\partial y},\ \frac{\partial}{\partial z}\right).$$
Take the concrete field $F = (x,\ y,\ z)$ — at every point the arrow points straight out
from the origin, like an expanding gas.

First, see that **$\nabla\cdot F$ and $F\cdot\nabla$ are different kinds of object.** Form
$\nabla\cdot F$ by pairing-and-applying: $\tfrac{\partial}{\partial x}$ applied to $F_1 = x$
gives $1$; $\tfrac{\partial}{\partial y}$ applied to $F_2 = y$ gives $1$;
$\tfrac{\partial}{\partial z}$ applied to $F_3 = z$ gives $1$. Summing,
$\nabla\cdot F = 1 + 1 + 1 = 3$ — a plain **number** (the divergence: the field is spreading
at rate $3$ everywhere). Now reverse the order. $F\cdot\nabla$ pairs $F_1 = x$ with
$\tfrac{\partial}{\partial x}$ in the *other* order, giving
$x\tfrac{\partial}{\partial x} + y\tfrac{\partial}{\partial y} + z\tfrac{\partial}{\partial z}$
— this is still an **operator**, a verb with nothing to act on yet; hand it a function $g$
and it returns $x\tfrac{\partial g}{\partial x} + y\tfrac{\partial g}{\partial y} +
z\tfrac{\partial g}{\partial z}$. So $\nabla\cdot F$ (a number) $\neq$ $F\cdot\nabla$ (an
operator): non-commutativity is not a subtlety here, it changes the *type* of the answer.

Now run the same $\nabla$ through all three products to see the family appear. Take the
scalar $f = x^2 + y^2 + z^2$.

- *Gradient (scalar-multiply):*
  $\nabla f = (2x,\ 2y,\ 2z)$ — a vector, pointing radially outward, the uphill direction of $f$.
- *Divergence (dot product):* $\nabla\cdot F = 3$ — a scalar, computed above.
- *Curl (cross product):* using $F = (x, y, z)$, the first entry is
  $\tfrac{\partial F_3}{\partial y} - \tfrac{\partial F_2}{\partial z} = \tfrac{\partial z}{\partial y} - \tfrac{\partial y}{\partial z} = 0 - 0 = 0$,
  and by the same cancellation the other two entries are $0$, so $\nabla\times F = (0,0,0)$
  — a vector, here the zero vector, telling us a purely outward-spraying field has no spin.

The same symbol $\nabla$, combined with a field through scalar-multiply, dot, and cross,
produced a vector, a scalar, and a vector — the gradient, the divergence, and the curl —
each a legitimate result because differentiation is linear, and each read by letting $\nabla$
act to its right.

## Prerequisites

- [[partial-derivative]]
- [[vector-dot-product]]
- [[cross-product]]
## Sources

- `etc/differential-operators-summary.html` — "Reading ∇ correctly" ("multiply" means
  *apply*; $\nabla$ is a *formal vector* because differentiation is linear;
  non-commutativity, $\nabla\cdot F \neq F\cdot\nabla$, read $\nabla$ to its right), and
  "The three products" (scalar-multiply → gradient, dot → divergence, cross → curl).
