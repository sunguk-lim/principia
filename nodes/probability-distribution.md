---
id: probability-distribution
title: Probability Distribution
summary: A random-variable is a function that assigns numbers to outcomes, with each value carrying a probability.
type: concept
tags: [math/probability]
prereqs: [random-variable]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Probability Distribution

## Summary

A [[random-variable]] is a function that assigns numbers to outcomes, with each value carrying a probability. A **probability distribution** is the full bookkeeping of *how that probability is spread across the values* — the complete answer to "how likely is each number, or each range of numbers?" When the variable takes separate, countable values, the distribution is a list of point-weights called a **probability mass function** (pmf): a weight on each value, all weights non-negative and summing to exactly 1. When the variable can take any value in a continuous range, no single point can carry weight (there are too many of them), so probability is described instead by a **probability density function** (pdf): a height curve where probability is the *area* under it over an interval, with the total area equal to exactly 1. The total always equals 1 because the variable is certain to take *some* value. The central subtlety: a density is probability *per unit length*, not a probability — it can exceed 1, and the chance of any exact point is 0.

## Grounded explanation

### What the concept *is*

Recall that a [[random-variable]] $X$ is a function assigning a number to each outcome, where each value it can produce carries a probability. Knowing that $X$ "is random" is not yet useful; we want the *whole picture* of where its probability lives. The **probability distribution** of $X$ is exactly that picture: a complete rule that, for any value or range of values, tells you the probability that $X$ lands there.

There is one rule, but it wears two costumes depending on the kind of values $X$ takes.

- **Discrete** — $X$ takes separated values you can list (e.g. $1, 2, 3$, or all the whole numbers). Probability sits on the points themselves.
- **Continuous** — $X$ takes every value across a stretch of the number line (e.g. any real number between $0$ and $2$). Probability is smeared along the line, not parked on points.

Two terms used throughout:
- **Support** — the set of values where the distribution puts any probability at all (where the weight or the height is nonzero). Outside the support, $X$ effectively never lands.
- **Normalization** — the requirement that the *total* probability equals exactly 1.

### The discrete case: a probability mass function

When $X$ is discrete, its distribution is a **probability mass function** (pmf), written $p$. For each value $x$ that $X$ can take, $p(x)$ is the probability that $X$ equals that value:

$$ p(x) = P(X = x). $$

Here $P(X = x)$ reads "the probability that the random variable $X$ comes out equal to the number $x$." A pmf must obey two rules:

1. **Non-negativity:** $p(x) \ge 0$ for every $x$. (A probability can never be negative.)
2. **Normalization:** $\sum_x p(x) = 1$, where $\sum_x$ means "add up over all values $x$ in the support."

**Why normalization is forced — not a convention.** When you observe $X$, it *must* produce some value; "no value at all" is not a possible result. The event "$X$ equals one of its possible values" is therefore certain, and a certain event has probability 1. Since the values are separate and mutually exclusive (a single observation can't be both $1$ and $2$), the probability of "some value" is the sum of the individual probabilities. That sum is the probability of a certainty, so it must equal 1. Normalization is not a tidy choice we impose — it is what *certainty plus mutual exclusivity* forces.

To get the probability of a *range*, you simply add the masses of the points in that range. For an event like "$X \ge 2$," sum $p(x)$ over every value $x$ that is at least 2.

### Worked instance (discrete)

Let $X$ take values in the support $\{1, 2, 3\}$ with masses

$$ p(1) = 0.2, \qquad p(2) = 0.5, \qquad p(3) = 0.3. $$

Check the two rules. **Non-negativity:** $0.2, 0.5, 0.3$ are all $\ge 0$. **Normalization:** add them,
$$ 0.2 + 0.5 + 0.3 = 1.0, $$
so the total mass is exactly 1 — a valid distribution. (This instance is non-degenerate: no mass is 0, and the three weights differ, so the shape is genuinely uneven.)

Now compute $P(X \ge 2)$, the probability $X$ comes out at least 2. The qualifying values are $2$ and $3$, so add their masses:
$$ P(X \ge 2) = p(2) + p(3) = 0.5 + 0.3 = 0.8. $$
As a sanity check, the complement is $P(X = 1) = 0.2$, and $0.8 + 0.2 = 1$ — consistent.

### The continuous case: a probability density function

Now let $X$ be continuous — say it can be *any* real number between $0$ and $2$. Try to describe it with a pmf and you hit a wall: there are infinitely many values in that stretch, and to keep the total at 1 each individual point would have to carry essentially no weight. In fact, for a continuous $X$, **the probability of any single exact value is 0**:
$$ P(X = c) = 0 \quad \text{for every exact point } c. $$
This is not a paradox: there are so many points that any one of them is infinitely unlikely to be hit *exactly*, even though some point certainly occurs. So point-masses cannot describe a continuous distribution.

The fix is to describe probability by a **height curve** $f$, the **probability density function** (pdf), and to read probability as **area under the curve over an interval**. The pdf must obey:

1. **Non-negativity:** $f(x) \ge 0$ for every $x$. (Heights can't be negative; negative area would be a negative probability.)
2. **Normalization:** the total area under $f$ equals 1, written
$$ \int_{-\infty}^{\infty} f(x)\,dx = 1, $$
where $\int_{-\infty}^{\infty} f(x)\,dx$ denotes "the total area between the curve $f$ and the horizontal axis, across the entire number line." Outside the support the height is 0, so only the support contributes area.

The probability that $X$ falls in an interval $[a, b]$ is the area of the slice of the curve between $a$ and $b$:
$$ P(a \le X \le b) = \int_a^b f(x)\,dx. $$

**Why normalization is forced here too.** Exactly the same reason as the discrete case: $X$ must take *some* value, so the event "$X$ lands somewhere on the line" is certain, and its probability is 1. That total probability is the *whole* area under $f$. Hence the whole area must equal 1. Same law — certainty equals total mass — only now "total mass" is an area rather than a sum.

**Density is NOT probability — the crucial subtlety.** The number $f(x)$ is *not* "the probability that $X = x$" (that probability is 0, as shown). Instead $f(x)$ is a **density**: probability *per unit length* near $x$. You only turn a density into a probability by multiplying by a length — i.e. by taking the area over an interval. A direct consequence: **a density value may exceed 1.** That is not an error. If probability is concentrated over a short interval, the height must be tall to make the area work out — height times width is what must stay $\le 1$, not the height alone. So "$f(x) > 1$" is perfectly legal; "$P(\text{some event}) > 1$" never is.

### Worked instance (continuous)

Let $X$ be **uniform on $[0, 2]$**: equally likely to land anywhere in that stretch and nowhere outside it. "Equally likely" means the height is the same constant over the whole support, so

$$ f(x) = \begin{cases} 0.5, & 0 \le x \le 2, \\ 0, & \text{otherwise.} \end{cases} $$

The support is $[0, 2]$; outside it the density is 0.

**Verify normalization.** Over $[0, 2]$ the curve is a flat rectangle of height $0.5$ and width $2 - 0 = 2$. Its area is height $\times$ width:
$$ \int_{-\infty}^{\infty} f(x)\,dx = 0.5 \times 2 = 1. $$
Total area is exactly 1, so this is a valid pdf.

**Density below 1 here — but it could exceed 1.** Notice $f(x) = 0.5 < 1$ on $[0, 2]$. Now spread the *same* total probability of 1 over a *shorter* interval, say uniform on $[0, 0.5]$. The width is $0.5$, so to keep area $= 1$ the height must be
$$ f(x) = \frac{1}{0.5} = 2 \quad \text{on } [0, 0.5], $$
a density of $2 > 1$. The probability is still capped at 1 (area $= 2 \times 0.5 = 1$); only the *height* climbed above 1. This makes "density $\neq$ probability" concrete: a height of 2 is not a probability of 2 — it is 2 units of probability per unit length, over half a unit of length.

**Compute a probability as area.** Back on the uniform-$[0,2]$ variable, find $P(X \le 0.5)$, the chance $X$ lands in $[0, 0.5]$. That slice is a rectangle of height $0.5$ and width $0.5 - 0 = 0.5$:
$$ P(X \le 0.5) = \int_0^{0.5} f(x)\,dx = 0.5 \times 0.5 = 0.25. $$
So $X$ has a 25% chance of landing in the first quarter of its range — which matches intuition, since $[0, 0.5]$ is one quarter of the length of the uniform support $[0, 2]$. And because the endpoint carries no area, $P(X \le 0.5) = P(X < 0.5)$: including or excluding the single point $0.5$ changes nothing, exactly because a single point has probability 0.

### Pulling the two costumes together

The pmf and the pdf are the same idea — a full account of where a [[random-variable]]'s probability lives — expressed for two kinds of values:

| | Discrete (pmf $p$) | Continuous (pdf $f$) |
|---|---|---|
| What $f(x)$ / $p(x)$ is | probability *at* the point: $P(X=x)$ | probability *density* (per unit length); not a probability |
| Non-negativity | $p(x) \ge 0$ | $f(x) \ge 0$ |
| Normalization (total = 1) | $\sum_x p(x) = 1$ | $\int f(x)\,dx = 1$ |
| Probability of a range | **sum** masses in the range | **area** under the curve over the range |
| Can the value exceed 1? | no — each $p(x) \le 1$ | yes — a density can be $> 1$ |
| $P(X = \text{exact point})$ | $= p(x)$, can be positive | $= 0$ |

In both costumes the engine is the same single law: the variable is certain to take *some* value, so the total — summed mass or enclosed area — is pinned to exactly 1.

## Prerequisites

- [[random-variable]]

## Sources

_none_
