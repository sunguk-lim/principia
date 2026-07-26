---
id: cumulative-distribution-function
title: Cumulative Distribution Function
summary: A probability-distribution tells you how a random-variable's probability is spread across its values — as point-weights (a pmf) when the values are separate, or as area under a…
type: concept
tags: [math/probability]
prereqs: [probability-distribution, random-variable]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Cumulative Distribution Function

## Summary

A [[probability-distribution]] tells you how a [[random-variable]]'s probability is spread across its values — as point-weights (a pmf) when the values are separate, or as area under a height curve (a pdf) when they form a continuous range. The **cumulative distribution function** (CDF), written $F$, repackages that same information as a *running total*: $F(x)$ is the probability that the variable comes out at or below $x$, i.e. $F(x) = P(X \le x)$. You build it by accumulating the distribution from the far left up to $x$ — summing the masses at all points $\le x$ in the discrete case, or sweeping out the area under the curve up to $x$ in the continuous case. This single function works for both kinds of variable, always climbs from 0 (far left) to 1 (far right) because the total probability is 1, and lets you read off the probability of any interval by subtraction, $P(a < X \le b) = F(b) - F(a)$. In the continuous case the running total and the height curve are inverse operations: the height is the *rate* at which the total grows, so differentiating the CDF recovers the density. The CDF also answers the reverse question — "which value sits at a given cumulative probability?" — giving quantiles such as the median (the value where the running total reaches one half).

## Grounded explanation

### What the concept *is*

Recall from [[probability-distribution]] that the distribution of a [[random-variable]] $X$ — a quantity whose value is uncertain — is the complete rule for where its probability lives. We write $P(\text{statement about } X)$ for "the probability that the statement is true." The distribution comes in two costumes: a **probability mass function** (pmf) $p$ for a *discrete* $X$ (one that takes separated, listable values), where $p(x) = P(X = x)$ is the weight sitting exactly on the value $x$; and a **probability density function** (pdf) $f$ for a *continuous* $X$ (one taking every value across a stretch of the line), where probability is *area under the curve* $f$ over an interval and the probability of any single exact point is 0. In both costumes the total probability is exactly 1, because $X$ is certain to take *some* value.

The pmf and pdf are descriptions of *local* probability — what sits at a point, or how dense probability is near a point. The **cumulative distribution function** (CDF) takes the very same distribution and answers a different, *accumulated* question:

$$ F(x) = P(X \le x). $$

In words: $F(x)$ is the probability that $X$ comes out at the value $x$ *or any value below it*. The symbol $F$ is a function of a real input $x$ and returns a probability (a number between 0 and 1). "$X \le x$" is the event "$X$ is less than or equal to the number $x$." This one definition — accumulate everything up to $x$ — is the whole concept. It is not a new piece of probability; it is the existing distribution read as a *running total* instead of a *local weight*.

Why bother, when the pmf or pdf already says everything? Three payoffs make the CDF the right tool: (1) it is **one uniform object** that describes discrete and continuous variables (and even mixtures) with the same formula $P(X \le x)$, where the pmf and pdf need two different machineries; (2) it turns "probability of an interval" into plain **subtraction**; and (3) for a continuous variable it is the exact **inverse operation** to the density, which is what lets you move between a distribution and its accumulated form at will. We will see each below.

### Building the running total

The recipe is "accumulate the distribution from the far left up to $x$." The two costumes of the distribution give two concrete ways to accumulate.

**Discrete.** Add up the masses of every point that is at $x$ or below it:

$$ F(x) = \sum_{x_i \le x} p(x_i), $$

where the symbol $\sum_{x_i \le x}$ means "sum $p(x_i)$ over all support points $x_i$ that satisfy $x_i \le x$" (a "support point" is a value carrying nonzero mass). As $x$ slides rightward across the line, $F$ stays flat between support points — nothing new gets added — and **jumps upward** by exactly $p(x_i)$ each time $x$ crosses a support point $x_i$. So a discrete CDF is a **staircase**: flat treads, with a riser of height $p(x_i)$ at each value $x_i$.

**Continuous.** Sweep out the area under the density up to $x$:

$$ F(x) = \int_{-\infty}^{x} f(t)\,dt, $$

where $\int_{-\infty}^{x} f(t)\,dt$ denotes "the area between the curve $f$ and the horizontal axis, accumulated from the far left up to the point $x$." (The variable inside is renamed $t$ only so it is not confused with the upper limit $x$; it is a dummy that ranges over everything below $x$.) Here $F$ rises **smoothly**, with no jumps, because adding the sliver of area from a single point contributes nothing — consistent with the prerequisite fact that a continuous variable has $P(X = c) = 0$ at any exact point $c$.

The two formulas are the same act in different arithmetic: *sum* the point-weights below $x$, or *integrate* the area below $x$. Both answer "how much probability sits at or below $x$?"

### Why the CDF must look the way it does

Three properties are forced by the definition $F(x) = P(X \le x)$ together with the prerequisite facts about a distribution. These are not conventions; each follows from the meaning.

1. **It never decreases.** If $b \ge a$, then the event "$X \le a$" is *contained in* the event "$X \le b$" (any outcome at or below $a$ is also at or below $b$). A larger event cannot have smaller probability, so $F(b) \ge F(a)$. As $x$ moves right, the running total can only stay flat or climb — never fall.

2. **It starts at 0 and ends at 1.** Push $x$ to the far left ($x \to -\infty$): the event "$X \le x$" becomes "$X$ is below everything," which is impossible, so $F(x) \to 0$. Push $x$ to the far right ($x \to +\infty$): the event becomes "$X$ is at or below everything," which is certain, so $F(x) \to 1$. This endpoint value of 1 is exactly the **normalization** of the distribution — the total mass (sum) or total area (integral) is 1 — now read as "the running total, once it has swept up everything, equals the whole probability." The CDF climbs monotonically across the gap from 0 to 1.

3. **It is right-continuous (and the discrete jumps land where you'd want).** Because the defining inequality is "$\le$" (at or below, *including* $x$ itself), the mass sitting *exactly* on a support point $x_i$ is counted the instant $x$ reaches $x_i$ — not just after. So at a jump the CDF takes its *higher* value: $F(x_i)$ already includes $p(x_i)$. This is the technical reason the convention is $P(X \le x)$ rather than $P(X < x)$, and it makes the interval rule below come out cleanly.

### The payoff: probability of an interval by subtraction

Here is the workhorse identity. The probability that $X$ lands in the half-open interval $(a, b]$ — *above* $a$ but *at or below* $b$ — is

$$ P(a < X \le b) = F(b) - F(a). $$

**Why.** The event "$X \le b$" splits into two mutually exclusive pieces: "$X \le a$" and "$a < X \le b$." Probabilities of mutually exclusive pieces add, so $P(X \le b) = P(X \le a) + P(a < X \le b)$, i.e. $F(b) = F(a) + P(a < X \le b)$. Rearranging isolates the interval: $P(a < X \le b) = F(b) - F(a)$. The running total bought us this: subtract the total accumulated up to $a$ from the total up to $b$, and what remains is precisely the probability deposited *between* them.

### The continuous payoff: the density is the slope of the CDF

In the continuous case the CDF and the density are **inverse operations**. The CDF accumulates area: $F(x) = \int_{-\infty}^{x} f(t)\,dt$. The reverse of "accumulate area" is "find the rate at which area is being added," which is the derivative. By the fundamental theorem of calculus, differentiating an accumulated-area function returns the curve being accumulated:

$$ f(x) = F'(x), $$

where $F'(x)$ is the slope of $F$ at $x$ — how fast the running total is climbing there. This is the precise meaning of "density is probability *per unit length*" from the prerequisite: the density at $x$ is literally the *rate* at which probability piles up as $x$ advances. Where $f$ is tall, $F$ is steep (probability accumulating fast); where $f$ is 0, $F$ is flat (nothing being added). So the distribution and its CDF are two views of one object, connected by integrate-one-way / differentiate-back. This invertibility is what makes the CDF the natural handle for a distribution.

### Reading it backwards: quantiles and the median

Everything above maps a *value* $x$ to a *cumulative probability* $F(x)$. Reading the function backwards — from a target probability to the value that achieves it — gives a **quantile**. The most familiar is the **median**: the value $m$ at which the running total reaches one half,

$$ F(m) = \tfrac{1}{2}, $$

so that $X$ is equally likely (probability $\tfrac{1}{2}$ each side) to fall below or above $m$. More generally, the **inverse CDF** takes a probability $q$ between 0 and 1 and returns the value $x$ with $F(x) = q$ — the value below which a fraction $q$ of the probability sits. Because $F$ climbs monotonically from 0 to 1, every target $q$ in $(0,1)$ has such a value, so this backward reading is well defined.

### Worked instance (discrete)

Take the discrete distribution from [[probability-distribution]]: $X$ on the support $\{1, 2, 3\}$ with masses

$$ p(1) = 0.2, \qquad p(2) = 0.5, \qquad p(3) = 0.3 \quad (\text{summing to } 1). $$

Accumulate left to right using $F(x) = \sum_{x_i \le x} p(x_i)$. The staircase, by region:

- **$x < 1$:** no support point is $\le x$ yet, so the sum is empty and $F(x) = 0$.
- **$1 \le x < 2$:** only the point $1$ qualifies, so $F(x) = p(1) = 0.2$.
- **$2 \le x < 3$:** points $1$ and $2$ qualify, so $F(x) = p(1) + p(2) = 0.2 + 0.5 = 0.7$.
- **$x \ge 3$:** all three qualify, so $F(x) = 0.2 + 0.5 + 0.3 = 1.0$.

This is a genuine staircase (three distinct risers of heights $0.2$, $0.5$, $0.3$), non-degenerate because no jump is 0. Check the forced properties: it never decreases ($0 \le 0.2 \le 0.7 \le 1.0$); it starts at 0 and ends at 1 (normalization, read as the final tread); and the jump at each $x_i$ lands on the higher value — at $x = 2$, $F(2) = 0.7$ already *includes* $p(2)$, because the definition uses "$\le$" (right-continuity).

Now read probabilities off it.
- $P(X \le 2) = F(2) = 0.7$ directly.
- Interval by subtraction: $P(1 < X \le 3) = F(3) - F(1) = 1.0 - 0.2 = 0.8$. Sanity check against the masses: $1 < X \le 3$ means $X \in \{2, 3\}$, and $p(2) + p(3) = 0.5 + 0.3 = 0.8$. They agree.

A note on the "$\le$ vs $<$" care that right-continuity demands: here $P(1 < X \le 3)$ excludes the point $1$ but includes $3$. Subtracting $F(1) = 0.7$ instead would have *also* dropped the mass at $2$, which is wrong — using $F(1) = 0.2$ correctly removes only the mass at or below $1$. With a discrete variable the choice of endpoints matters, and the CDF's "$\le$" convention is what makes the subtraction land on exactly the points you intend.

### Worked instance (continuous)

Take the continuous distribution from [[probability-distribution]]: $X$ **uniform on $[0, 2]$**, with density $f(x) = 0.5$ for $0 \le x \le 2$ and $f(x) = 0$ otherwise.

Accumulate area using $F(x) = \int_{-\infty}^{x} f(t)\,dt$. By region:

- **$x < 0$:** no area yet (the density is 0 to the left of the support), so $F(x) = 0$.
- **$0 \le x \le 2$:** the accumulated area is a rectangle of height $0.5$ and width $x - 0 = x$, so $F(x) = 0.5 \, x = x/2$. It rises smoothly — no jumps — from $F(0) = 0$ to $F(2) = 1$.
- **$x > 2$:** all the area (the full rectangle of area $0.5 \times 2 = 1$) is already swept up, so $F(x) = 1$.

Check the properties: $F$ never decreases (it climbs steadily on $[0,2]$ and is flat outside); it runs from 0 to 1 (the endpoint 1 is the normalization — the whole area); and it is continuous everywhere, with no jumps, matching $P(X = c) = 0$ for a continuous variable.

Now use it.
- **Recover the density by differentiating.** On $[0, 2]$, $F(x) = x/2$, whose slope is $F'(x) = 1/2 = 0.5 = f(x)$. The derivative of the CDF returns the density exactly, confirming $f = F'$: the running total climbs at a constant rate of $0.5$ per unit length, which *is* the constant density.
- **Find the median.** Solve $F(m) = \tfrac{1}{2}$: on $[0,2]$ that is $m/2 = 0.5$, giving $m = 1$. So $1$ is the median — equally likely to land below or above it — which matches intuition, since $1$ is the midpoint of the uniform range $[0, 2]$.
- **Interval by subtraction.** $P(0.5 < X \le 1.5) = F(1.5) - F(0.5) = 1.5/2 - 0.5/2 = 0.75 - 0.25 = 0.5$. The middle half of the range carries half the probability — again as expected for a uniform variable, since that interval is half the length of $[0,2]$.

### Pulling it together

The CDF is one function, $F(x) = P(X \le x)$, that re-expresses any [[probability-distribution]] as a running total swept from the far left up to $x$ — a summed staircase for a discrete variable, a smoothly accumulated area for a continuous one. The same three properties hold in both costumes for the same reasons: it never decreases (bigger events hold more probability), it climbs from 0 to 1 (the endpoint 1 *is* normalization), and it is right-continuous (the "$\le$" includes the point itself). Those properties earn the payoffs: interval probability by subtraction $F(b) - F(a)$ in both costumes; density-as-slope $f = F'$ in the continuous costume, which makes the CDF and the density inverse operations; and quantiles such as the median by reading the function backwards. That is why the CDF, not the pmf or pdf, is the uniform handle on a distribution.

## Prerequisites

- [[probability-distribution]]
- [[random-variable]]

## Sources

_none_
