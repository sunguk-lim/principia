---
id: change-of-variables
title: Change of Variables
summary: You have a random variable $X$ with a known density, and you build a new variable $Y$ by feeding $X$ through a function, $Y = g(X)$ — for instance squaring it, taking its…
type: concept
tags: [math/probability]
prereqs: [cumulative-distribution-function, derivative, random-variable, differential, jacobian]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Change of Variables

## Summary

You have a random variable $X$ with a known density, and you build a new variable $Y$ by feeding $X$ through a function, $Y = g(X)$ — for instance squaring it, taking its logarithm, or scaling it. **Change of variables** answers: what is the density of $Y$? The naive guess "just plug $g$ in" is wrong, because $g$ stretches and squeezes the number line unevenly, and a density is probability *per unit length* — so when a region of inputs gets stretched out into a wider region of outputs, the same probability is spread over more room and the density there must thin out. The clean fact lives not at the level of the density but at the level of the [[cumulative-distribution-function]]: when $g$ is strictly increasing, the event "$X$ at or below $x$" is the *same event* as "$Y$ at or below $g(x)$," so their cumulative probabilities are equal, $F_X(x) = F_Y(g(x))$. Differentiating that equality in $x$ — the left side returns the density of $X$ (the [[derivative]] of a CDF is its density), the right side picks up a chain-rule factor $g'(x)$ — yields the master formula $f_X(x) = f_Y(g(x))\,|g'(x)|$. The factor $|g'(x)|$ is the local stretch of $g$: where $g$ is steep, outputs spread apart and density thins; where $g$ is shallow, outputs bunch up and density piles. It is exactly the rebalancing that keeps the total probability equal to 1 after the reshape — and because $g$ is a *bijection* between the support of $X$ and the support of $Y$, no probability is created or lost, only relocated.

## Grounded explanation

### What the concept *is*

We start with a continuous [[random-variable]] $X$ — a quantity whose value is uncertain — whose probability is described by a **density** $f_X$, where probability is area under the curve $f_X$ and $f_X(x)$ measures probability *per unit length* near $x$. We also have its [[cumulative-distribution-function]] $F_X(x) = P(X \le x)$, the running total of probability accumulated from the far left up to $x$, and we know from that prerequisite that the density is the slope of the running total: $f_X(x) = F_X'(x)$.

Now we form a **new** random variable by transforming $X$ through a function $g$:

$$ Y = g(X). $$

Every time $X$ comes out at a value $x$, the new variable $Y$ comes out at $g(x)$. So $Y$ is also random, with its own density $f_Y$ and its own running total $F_Y$. **Change of variables** is the rule that produces $f_Y$ from $f_X$ and $g$. (The name comes from the act of replacing the variable $X$ by the new variable $Y=g(X)$.)

We require two things of $g$:

- **Strictly monotonic** — either always increasing or always decreasing, never doubling back. This guarantees $g$ is *one-to-one*: each output value comes from exactly one input value, so we can run the transformation backwards. Write the inverse as $x = g^{-1}(y)$, the unique input that $g$ sends to the output $y$.
- **Differentiable**, so its slope $g'(x)$ — the [[derivative]] of $g$, the instantaneous rate at which the output moves as the input nudges — exists everywhere.

The concept itself is the boxed relationship we will derive:

$$ \boxed{\,f_X(x) = f_Y\!\big(g(x)\big)\,\big|g'(x)\big|\,} $$

and equivalently, solving for the thing we usually want (the density of the *new* variable, written in terms of $y$),

$$ f_Y(y) = \frac{f_X\!\big(g^{-1}(y)\big)}{\big|g'(g^{-1}(y))\big|}. $$

The rest of this node explains *why* this is true, why the strange absolute-value-of-a-slope factor appears, and runs it on real numbers.

### Why "just substitute" fails — the density is per unit length

Here is the trap. A density is not a probability; it is a probability *rate* — probability per unit of length along the axis. When $g$ maps inputs to outputs, it does not preserve length. A nonlinear $g$ stretches some stretches of the line and compresses others: a steep part of $g$ takes a small interval of inputs and fans it out into a wide interval of outputs, while a shallow part squashes a wide input interval into a narrow output interval.

Probability, however, is conserved — it is attached to the *outcomes*, not to the axis. The chunk of probability that lived in a small input interval must reappear, undiminished, in whatever output interval that input interval maps to. If that output interval is *wider* (the steep case), the same probability now occupies more length, so the density — probability per unit length — must be *smaller* there. If the output interval is *narrower* (the shallow case), the density must be *larger*. That correction factor is the local stretch of $g$, and it is precisely $|g'(x)|$, the magnitude of the slope. Plugging $g$ in without it would conserve heights, not areas — and it is areas (probabilities) that must be conserved. This is the WHY in one sentence: **a density transforms by reweighting with the local length-stretch so that area, i.e. probability, is preserved.**

### The derivation, done at the level of the CDF

The reason the derivation is clean is that we do *not* work with the density directly. We work with the [[cumulative-distribution-function]], where the relationship is an exact equality of events, and only differentiate at the very end.

**Increasing case.** Suppose $g$ is strictly increasing. Then "input at or below $x$" and "output at or below $g(x)$" describe the *identical* event: $X \le x$ happens in exactly the same outcomes as $g(X) \le g(x)$, because an increasing $g$ preserves the order of every pair of values. (If $X \le x$ then applying $g$ to both sides keeps the inequality, $g(X) \le g(x)$; and conversely, because $g$ is one-to-one and increasing, $g(X) \le g(x)$ forces $X \le x$.) Equal events have equal probability, and since $Y = g(X)$,

$$ F_X(x) = P(X \le x) = P\big(g(X) \le g(x)\big) = P\big(Y \le g(x)\big) = F_Y\big(g(x)\big). $$

So the two running totals are locked together: $F_X(x) = F_Y(g(x))$. This single equality *is* the heart of change of variables; everything else is calculus. Notice that at this cumulative level there is **no correction factor at all** — probabilities transfer through a monotonic map untouched. The stretch factor is born only when we differentiate.

Now differentiate both sides with respect to $x$, using $f = F'$ from the [[cumulative-distribution-function]] prerequisite (the [[derivative]] of a running total is its density). The left side is immediate:

$$ \frac{d}{dx}\,F_X(x) = f_X(x). $$

The right side is a composition — $F_Y$ evaluated at the inner function $g(x)$ — so its derivative is the **chain rule**: differentiate the outer function $F_Y$ at the inner value $g(x)$, then multiply by the derivative of the inner function $g$. The outer derivative $F_Y'$ is just $f_Y$, so

$$ \frac{d}{dx}\,F_Y\big(g(x)\big) = F_Y'\big(g(x)\big)\cdot g'(x) = f_Y\big(g(x)\big)\,g'(x). $$

Setting the two equal gives, in the increasing case,

$$ f_X(x) = f_Y\big(g(x)\big)\,g'(x). $$

Since $g$ is increasing, $g'(x) > 0$, so here $g'(x) = |g'(x)|$ already — the factor is the (positive) local stretch.

**Decreasing case.** Now suppose $g$ is strictly decreasing. Order is *reversed*: $X \le x$ now corresponds to $g(X) \ge g(x)$ (a smaller input gives a *larger* output). So the matching event flips to the upper tail:

$$ F_X(x) = P(X \le x) = P\big(g(X) \ge g(x)\big) = P\big(Y \ge g(x)\big) = 1 - F_Y\big(g(x)\big), $$

where the last step uses that "at or above $g(x)$" is the complement of "at or below $g(x)$," and probabilities of complementary events sum to 1. Differentiate this in $x$. The left side is $f_X(x)$ as before. On the right, the constant $1$ differentiates to $0$, and the chain rule on $-F_Y(g(x))$ gives $-f_Y(g(x))\,g'(x)$:

$$ f_X(x) = -\,f_Y\big(g(x)\big)\,g'(x). $$

This looks like it has the wrong sign — but a density can never be negative, and indeed it isn't: $g$ is *decreasing*, so $g'(x) < 0$, and $-g'(x) = |g'(x)| > 0$. The minus sign exactly converts the negative slope into its magnitude:

$$ f_X(x) = f_Y\big(g(x)\big)\,\big|g'(x)\big|. $$

**Both cases merge.** Increasing gave $g'(x) = |g'(x)|$; decreasing gave $-g'(x) = |g'(x)|$. Either way,

$$ f_X(x) = f_Y\big(g(x)\big)\,\big|g'(x)\big|. $$

The absolute value is not a patch bolted on for tidiness — it is forced by the two cases agreeing, the precise residue left behind by the flipped inequality in the decreasing case, and it encodes the intuition from before: only the *magnitude* of the stretch matters for how density rebalances; whether $g$ flips direction is irrelevant to area. Solving for $f_Y$ at a given output $y$ (substitute $x = g^{-1}(y)$, so $g(x) = y$) gives the usable form

$$ f_Y(y) = \frac{f_X\!\big(g^{-1}(y)\big)}{\big|g'(g^{-1}(y))\big|}. $$

The slope sits in the denominator here: where $g$ is steep ($|g'|$ large), $f_Y$ is divided down — density thins, matching "outputs spread out." Where $g$ is shallow, $f_Y$ is divided by a small number — density piles up. The conservation of total area is automatic, because the equality we differentiated already had $F_Y \to 1$ at the far right.

### The rigorous infinitesimal version — why the slope manipulation is legitimate

The CDF derivation is airtight, but it leans on the chain rule applied to $F_Y(g(x))$, which can feel like a piece of symbolic magic. There is a second derivation, working directly with little chunks of probability, that exposes exactly *why* the slope factor is the right one and proves that the intuitive "$dy/dx$" juggling is not hand-waving but a genuine limit. It also re-derives the result without ever differentiating a CDF, so it stands on its own.

Take the increasing case and look at a tiny input interval $[x, x+\Delta x]$ of width $\Delta x$. By the very definition of a density, the probability that $X$ lands in it is the density times the width, plus a correction that shrinks faster than $\Delta x$ itself:

$$ P\big(X \in [x, x+\Delta x]\big) = f_X(x)\,\Delta x + o(\Delta x). $$

Here $o(\Delta x)$ — read "little-o of $\Delta x$" — is shorthand for *any* quantity that becomes negligible compared to $\Delta x$ as $\Delta x \to 0$; formally, dividing it by $\Delta x$ sends it to $0$. It is the leftover from approximating the slightly-curved area under $f_X$ over the interval by a single rectangle of height $f_X(x)$: the rectangle captures the bulk, $f_X(x)\,\Delta x$, and the sliver of mismatch is $o(\Delta x)$.

Now push that input interval through $g$. Because $g$ is increasing and one-to-one, the event "$X \in [x, x+\Delta x]$" is the *same event* as "$Y \in [g(x),\, g(x+\Delta x)]$" — the input interval and its image carry identical probability, the same mass-conservation idea as before, now at the scale of a single sliver. The image interval has width

$$ \Delta y = g(x+\Delta x) - g(x) = g'(x)\,\Delta x + o(\Delta x), $$

which is simply the [[derivative]] in its defining role: the change in output is the slope times the change in input, up to an $o(\Delta x)$ curvature correction (this *is* the limit definition of $g'(x)$, rearranged). So the same chunk of probability, $f_X(x)\,\Delta x + o(\Delta x)$, now occupies an output interval of width $g'(x)\,\Delta x + o(\Delta x)$. The **average density of $Y$** over that image interval is mass divided by width:

$$ \frac{f_X(x)\,\Delta x + o(\Delta x)}{g'(x)\,\Delta x + o(\Delta x)}. $$

Divide top and bottom by $\Delta x$. The leading terms become $f_X(x)$ and $g'(x)$; the $o(\Delta x)$ terms, divided by $\Delta x$, *provably vanish* as $\Delta x \to 0$ — that is precisely what the little-o notation guarantees. So the average density over a shrinking interval converges to the density at the point:

$$ \frac{f_X(x)\,\Delta x + o(\Delta x)}{g'(x)\,\Delta x + o(\Delta x)} \;\xrightarrow{\ \Delta x \to 0\ }\; \frac{f_X(x)}{g'(x)} = f_Y\big(g(x)\big). $$

Rearranging $f_Y(g(x)) = f_X(x)/g'(x)$ gives $f_X(x) = f_Y(g(x))\,g'(x)$, the boxed formula again (with $|g'|$ once the decreasing case is folded in). The payoff of this version is conceptual: it shows that writing "$dy = g'(x)\,dx$" and cancelling differentials, which looks like sloppy algebra on infinitesimals, is shorthand for this honest limit in which the $o(\Delta x)$ corrections are *carried along and shown to die*. The slope factor is exactly the ratio of output-width to input-width for a sliver of probability — the local stretch — and nothing has been swept under the rug.

### Mass preservation as a bijection — the Jacobian conserves total probability

The deepest reason the formula must look this way is that change of variables can neither create nor destroy probability. The strict monotonicity we demanded does more than make the inequality flips clean: it makes $g$ a **bijection** between the support of $X$ (the set of values $X$ can take) and the support of $Y$. A bijection is a perfect one-to-one pairing — every input maps to exactly one output and every output comes from exactly one input — so the entire probability mass of $X$ is not diminished but merely *relocated* onto the new axis. Nothing falls off the edge; nothing is double-counted.

This is most vivid when the two supports look completely different. Take $g = \ln$, the natural logarithm, as the map. Its domain is the positive half-line $(0, \infty)$ and its range is the whole real line $(-\infty, \infty)$. So $Y = \ln X$ carries a variable living on the positive reals over to one living on the entire line, and its inverse $x = e^{y}$ carries the whole line back onto the positive half-line. A reader might worry: the input $X$ only ever takes positive values, yet $Y$ ranges over negatives too — where does the probability on the negative side of $Y$ come from, and does restricting $X$ to $x > 0$ throw mass away? It does not. The negative half of $Y$ is not invented and the positive-only restriction on $X$ discards nothing; the mass is simply *re-addressed* by the bijection. Concretely, the outputs $y \in (-\infty, 0)$ are the images of inputs $x \in (0,1)$; the single output $y = 0$ is the image of $x = 1$; and outputs $y \in (0, \infty)$ are the images of $x \in (1, \infty)$. Every scrap of probability on the $Y$ axis has a unique home on the $X$ axis and vice versa.

That the relocation conserves the *total* is not a separate fact to be checked but an automatic consequence of the stretch factor — and this is where the [[jacobian]] (the local stretch $|g'|$) reveals its true job. Write the substitution that pairs the axes: $y = \ln x$, whose [[differential]] is $dy = dx/x$ (since the [[derivative]] of $\ln x$ is $1/x$). As $x$ sweeps from $0$ to $\infty$, $y$ sweeps from $-\infty$ to $\infty$, and the total mass of $X$ rewrites itself, term for term, into the total mass of $Y$:

$$ \int_{0}^{\infty} f_X(x)\,dx = \int_{0}^{\infty} f_Y(\ln x)\,\frac{1}{x}\,dx = \int_{-\infty}^{\infty} f_Y(y)\,dy = 1. $$

Read the middle step carefully. The factor $1/x$ is the Jacobian $|g'(x)|$, and it is *exactly* what the substitution $dy = dx/x$ requires to convert the $x$-integral into the $y$-integral with no residue. If the stretch factor were any other function, the substitution would not balance and the total would not come out to $1$. So the Jacobian is not a cosmetic correction — it is the precise weight that makes the change of integration variable an identity, which is the same as saying it is what conserves total probability. The endpoint $x = 0$ corresponds to $y = -\infty$, a limit never actually attained, and any single point carries zero probability for a continuous variable, so excluding $x \le 0$ removes nothing measurable. The bijection accounts for all the mass; the Jacobian keeps the books exact.

### Worked instance — turning a uniform into an exponential

We pick a **nonlinear** $g$ so the stretch factor genuinely varies with the input (a linear $g$ would give a constant $|g'|$ and hide the whole point).

Let $X$ be **uniform on $(0,1)$**: its density is flat,

$$ f_X(x) = 1 \quad \text{for } 0 < x < 1, \qquad f_X(x) = 0 \text{ otherwise}. $$

(Height $1$ over a base of length $1$ gives total area $1$ — a valid density.) Transform it by the natural logarithm, negated:

$$ Y = g(X) = -\ln X. $$

Check the requirements. On $0 < x < 1$, $\ln x$ runs over $(-\infty, 0)$, so $-\ln x$ runs over $(0, \infty)$: the outputs $y$ are the positive reals. The slope is $g'(x) = -\tfrac{1}{x}$ (the [[derivative]] of $-\ln x$), which is negative throughout $(0,1)$ — so $g$ is strictly **decreasing**, hence one-to-one, and differentiable. Both requirements hold. Note $|g'(x)| = 1/x$, which is *not* constant — it blows up near $x=0$ and equals $1$ near $x=1$ — so this is a genuinely non-degenerate stretch. And it is a genuine **bijection**: the support of $X$, the open interval $(0,1)$, is paired perfectly with the support of $Y$, the half-line $(0, \infty)$, each output coming from exactly one input.

Invert the transformation. From $y = -\ln x$ we get $\ln x = -y$, so

$$ x = g^{-1}(y) = e^{-y}. $$

Now assemble $f_Y(y)$ from the boxed formula in its solved form, for $y > 0$:

$$ f_Y(y) = \frac{f_X\!\big(g^{-1}(y)\big)}{\big|g'(g^{-1}(y))\big|}. $$

Evaluate each piece by hand. The input that produced output $y$ is $g^{-1}(y) = e^{-y}$; since $e^{-y}$ lies in $(0,1)$ for every $y > 0$, the flat density there is $f_X(e^{-y}) = 1$. The slope magnitude at that input is $|g'(x)| = 1/x$ evaluated at $x = e^{-y}$, namely $1/e^{-y} = e^{y}$. Therefore

$$ f_Y(y) = \frac{1}{e^{y}} = e^{-y} \quad \text{for } y > 0, $$

and $f_Y(y) = 0$ for $y \le 0$ (no input maps there). This is the **exponential density** — the transformation $-\ln X$ converts a flat uniform into a decaying exponential.

Trace the intuition through the numbers. Near $x = 1$ (so $y$ near $0$), the stretch is mild, $|g'| = 1$, and $f_Y(0) = e^{0} = 1$ — the density is as tall as the original. Near $x = 0$ (so $y$ large), $g$ is extremely steep, $|g'| = 1/x$ is huge, that tiny sliver of inputs gets fanned out across the entire far-right tail, and dividing by the large stretch makes $f_Y$ tiny — $f_Y$ decays toward $0$. The steepness of $g$ is exactly what carves the exponential's tail out of the uniform's flat top.

**Verify mass preservation directly.** A density must enclose total area $1$, and the bijection-plus-Jacobian argument says this should fall out automatically from the substitution itself. Run that substitution explicitly. We want the total mass of $X$, which is plainly $1$; let us watch it turn into the total mass of $Y$. With $y = -\ln x$ we have $dy = -dx/x$, and the Jacobian magnitude is $|dy/dx| = 1/x = e^{y}$. As $x$ sweeps from $0$ to $1$, $y$ sweeps from $\infty$ down to $0$; absorbing the sign by flipping the limits,

$$ \int_{0}^{1} f_X(x)\,dx = \int_{0}^{1} 1 \cdot dx = \int_{0}^{\infty} f_Y(y)\,dy, $$

and computing the right-hand integral on its own confirms the value is indeed $1$:

$$ \int_{0}^{\infty} e^{-y}\,dy = \Big[-e^{-y}\Big]_{0}^{\infty} = \big(-e^{-\infty}\big) - \big(-e^{0}\big) = (0) - (-1) = 1. $$

Both sides equal $1$: the unit mass of the uniform on $(0,1)$ has been relocated, intact, onto the exponential on $(0,\infty)$. The Jacobian $1/x$ is precisely the weight that made the two integrals match — exactly the mass-preservation mechanism the bijection guarantees, now confirmed on concrete numbers. (Cross-check via the CDF equality itself: $g$ decreasing gives $F_X(x) = 1 - F_Y(g(x))$. The uniform's running total is $F_X(x) = x$ on $(0,1)$. So $1 - F_Y(-\ln x) = x$, i.e. $F_Y(-\ln x) = 1 - x$. Writing $y = -\ln x$, hence $x = e^{-y}$, gives $F_Y(y) = 1 - e^{-y}$, whose [[derivative]] is $f_Y(y) = e^{-y}$ — the same answer, obtained straight from the event equality without the boxed formula.)

### Pulling it together

A transformed variable $Y = g(X)$ does **not** inherit the density of $X$ by substitution, because $g$ reshapes the number line unevenly while probability must be conserved. The correct rule, $f_X(x) = f_Y(g(x))\,|g'(x)|$, is derived not at the density level but at the [[cumulative-distribution-function]] level, where strict monotonicity makes "$X \le x$" and "$Y \le g(x)$" the same event (or its complement when $g$ decreases), so the running totals are locked: $F_X(x) = F_Y(g(x))$ or $1 - F_Y(g(x))$. Differentiating that equality with the chain rule — using that the [[derivative]] of a running total is its density — drops out the local-stretch factor $|g'(x)|$, whose absolute value is forced by the increasing and decreasing cases agreeing. The same factor can be obtained without differentiating a CDF, by the rigorous infinitesimal version: a sliver of probability $f_X(x)\Delta x + o(\Delta x)$ maps to an output interval of width $g'(x)\Delta x + o(\Delta x)$, and their ratio tends to $f_X(x)/g'(x) = f_Y(g(x))$ as the $o(\Delta x)$ corrections provably vanish — which is why the "$dy/dx$" manipulation is a real limit, not hand-waving. Underneath both derivations is one conservation law: $g$ is a bijection between the supports, so its whole mass is relocated, never lost, and the Jacobian $|g'|$ is exactly the weight that makes the substitution $\int f_X\,dx = \int f_Y\,dy = 1$ balance. That factor thins the density where $g$ is steep and thickens it where $g$ is shallow, conserving total probability — as the worked $Y = -\ln X$ shows, carving a normalized exponential out of a flat uniform with the unit mass intact.

## Prerequisites

- [[cumulative-distribution-function]]
- [[derivative]]

## Sources

_none_
