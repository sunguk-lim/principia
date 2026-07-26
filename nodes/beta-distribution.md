---
id: beta-distribution
title: Beta Distribution
summary: The Beta distribution is a continuous probability-distribution whose values live strictly inside the interval $(0,1)$ — the open stretch between $0$ and $1$, not including the…
type: concept
tags: [math/probability]
prereqs: [probability-distribution]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Beta Distribution

## Summary

The **Beta distribution** is a continuous [[probability-distribution]] whose values live strictly inside the interval $(0,1)$ — the open stretch between $0$ and $1$, not including the endpoints. Because every number in $(0,1)$ is itself a valid *probability*, the Beta distribution is a distribution *over a probability*: it answers "if some unknown success-rate $p$ could be anything between 0 and 1, how plausible is each possible value of $p$?" Its probability density function (pdf) has the shape $f(p) \propto p^{\alpha-1}(1-p)^{\beta-1}$, governed by two **shape parameters** $\alpha > 0$ and $\beta > 0$. The symbol $\propto$ means "proportional to"; a fixed normalizing constant $1/B(\alpha,\beta)$ rescales the curve so its total area is exactly 1, as every pdf must. The two parameters act like **pseudo-counts** of imagined successes ($\alpha$) and failures ($\beta$): $\alpha = \beta = 1$ gives a flat (uniform) curve; $\alpha, \beta > 1$ give a single interior bump; making both large concentrates the bump into a narrow spike. Its mean is $\alpha/(\alpha+\beta)$, and (when $\alpha,\beta>1$) its peak sits at $(\alpha-1)/(\alpha+\beta-2)$. The reason it matters: its $p^{\alpha-1}(1-p)^{\beta-1}$ form is the same algebraic shape as the chance of seeing some successes-and-failures from coin-like trials, which makes Beta the natural way to model an uncertain probability.

## Grounded explanation

### What the concept *is*

Recall from [[probability-distribution]] that a **continuous** distribution describes a random number not by weights on points but by a **probability density function** (pdf): a non-negative height curve $f$ where the probability of landing in an interval $[a,b]$ is the *area under the curve* over that interval, and the *total* area over the whole support is pinned to exactly 1 (normalization). Recall too the crucial subtlety that a density is probability *per unit length*, not a probability — so a density value is allowed to exceed 1.

The **Beta distribution** is one specific family of such continuous pdfs. Its defining feature is twofold:

1. **Its support is the open interval $(0,1)$** — all the real numbers strictly between 0 and 1, with density 0 everywhere outside. We name the variable $p$ (rather than $x$) deliberately: any number in $(0,1)$ is a legitimate probability, so a draw from a Beta distribution *is itself a probability*. This is what people mean by the slogan "a distribution over a probability."
2. **Its density has the form**
$$ f(p) = \frac{1}{B(\alpha,\beta)}\, p^{\,\alpha-1}\,(1-p)^{\,\beta-1}, \qquad 0 < p < 1, $$
and $f(p) = 0$ otherwise. The two numbers $\alpha > 0$ and $\beta > 0$ are the **shape parameters** (read "alpha" and "beta"). The factor $1/B(\alpha,\beta)$ out front is a constant — it does not depend on $p$ — and $B(\alpha,\beta)$ is called the **Beta function**, defined precisely so that the total area comes out to 1.

So the concept is not "a curve" in the abstract; it is *this particular two-knob family* of curves on $(0,1)$, where turning the knobs $\alpha,\beta$ reshapes the curve.

### Reading the formula: the unnormalized core and the constant

It helps to split the density into two pieces:

- The **core**, $p^{\alpha-1}(1-p)^{\beta-1}$, which carries all the *shape* — where the curve is high and where it is low.
- The **normalizing constant**, $1/B(\alpha,\beta)$, which is just a vertical rescale so the whole thing has area 1.

The constant cannot change the *shape*; multiplying every height by the same number stretches the curve uniformly up or down. Shape is entirely the core's job. That is why we wrote the Summary with $\propto$ ("proportional to"): $f(p) \propto p^{\alpha-1}(1-p)^{\beta-1}$ says "the curve has this shape, up to an overall scale."

**Why a normalizing constant is needed at all.** From [[probability-distribution]], a valid pdf must enclose total area exactly 1. But the bare core $p^{\alpha-1}(1-p)^{\beta-1}$ encloses *some* area $A$ over $(0,1)$ that is generally not 1 — it depends on $\alpha,\beta$. Define
$$ B(\alpha,\beta) = \int_0^1 p^{\,\alpha-1}(1-p)^{\,\beta-1}\,dp, $$
which is exactly that area $A$ (here $\int_0^1 \cdots\, dp$ means "the area under the core between 0 and 1"). Then dividing the core by $B(\alpha,\beta)$ scales its area down from $A$ to $A/A = 1$. This is not a magic trick: it is the only thing you *can* do to a fixed-shape curve to make its area 1 — divide by whatever area it currently has. The Beta function is simply "the area the core happens to enclose," given a name.

### The shape intuition: $\alpha,\beta$ as pseudo-counts

Why does the core have the peculiar form $p^{\alpha-1}(1-p)^{\beta-1}$? The cleanest intuition treats $\alpha$ and $\beta$ as imagined **counts**: think of $\alpha-1$ as a number of "successes" and $\beta-1$ as a number of "failures" you are pretending to have already seen for an event whose true success-rate is the unknown $p$.

- The factor $p^{\alpha-1}$ rewards values of $p$ that explain the successes: if you've "seen" successes, large $p$ is more plausible, and $p^{\alpha-1}$ grows with $p$ (when $\alpha-1 > 0$).
- The factor $(1-p)^{\beta-1}$ rewards values of $p$ that explain the failures: failures make small $p$ more plausible, and $(1-p)^{\beta-1}$ grows as $p$ shrinks (when $\beta-1 > 0$).

The product balances the two pulls, peaking wherever $p$ best reconciles the imagined successes and failures. This also explains every qualitative behavior of the family:

- **$\alpha = \beta = 1$ → flat (uniform).** Then $p^{0}(1-p)^{0} = 1 \cdot 1 = 1$ for all $p$: a constant height over $(0,1)$. The core is flat, so after normalizing, $f(p) = 1$ on $(0,1)$ — the **uniform distribution**, which says "every probability between 0 and 1 is equally plausible." (Zero imagined successes and zero imagined failures = total ignorance.)
- **$\alpha, \beta > 1$ → an interior bump.** Both exponents are positive, so the core is 0 at $p=0$ (the $p^{\alpha-1}$ factor vanishes) and 0 at $p=1$ (the $(1-p)^{\beta-1}$ factor vanishes), and positive in between — forcing a single hump peaked somewhere inside $(0,1)$.
- **Large $\alpha,\beta$ → a narrow spike.** Bigger pseudo-counts mean more imagined evidence, so the plausible range of $p$ tightens: the bump grows tall and thin, concentrating near its peak. ("Lots of evidence" = "I'm fairly sure where $p$ is.")
- **Asymmetry.** If $\alpha > \beta$ (more imagined successes than failures), the bump leans toward 1; if $\beta > \alpha$, it leans toward 0.

### The summary numbers: mean and mode

Two single-number summaries of a Beta distribution will let us check our worked instances:

- **Mean** (the center of mass of the curve — the long-run average value of $p$):
$$ \text{mean} = \frac{\alpha}{\alpha + \beta}. $$
This is exactly "successes over total," reading $\alpha$ as successes and $\alpha+\beta$ as total trials — the same way you'd estimate a rate from counts. The pseudo-count picture makes the formula memorable rather than arbitrary.
- **Mode** (the location of the peak — the single most plausible value of $p$), valid when $\alpha,\beta>1$ so a genuine interior peak exists:
$$ \text{mode} = \frac{\alpha - 1}{\alpha + \beta - 2}. $$
This is "successes over total" again, but with the imagined trials counted as $\alpha-1$ and $\beta-1$ — the pseudo-count reading taken literally.

Mean and mode generally differ when the curve is skewed; they coincide only when the curve is symmetric.

### Worked instance 1 — Beta(2,2): a symmetric gentle bump

Take $\alpha = 2$, $\beta = 2$. The core is
$$ p^{\,2-1}(1-p)^{\,2-1} = p^{1}(1-p)^{1} = p(1-p). $$
This is 0 at $p=0$ and at $p=1$, and positive between — a single symmetric hump, highest in the middle. It is **non-degenerate**: both exponents are $1$, not $0$, so neither factor collapses to a constant, and we genuinely see the interior-bump behavior (unlike the flat $\alpha=\beta=1$ case).

**Normalize.** The area under the core is
$$ B(2,2) = \int_0^1 p(1-p)\,dp = \int_0^1 \big(p - p^2\big)\,dp = \tfrac12 - \tfrac13 = \tfrac{3}{6} - \tfrac{2}{6} = \tfrac16. $$
So the area the core encloses is $1/6$, and the true density is the core divided by that area:
$$ f(p) = \frac{p(1-p)}{1/6} = 6\,p(1-p), \qquad 0 < p < 1. $$
Quick check that this is a valid pdf: its area is $6 \times \tfrac16 = 1$. Good — total area exactly 1, as [[probability-distribution]] demands.

**Mean.** $\dfrac{\alpha}{\alpha+\beta} = \dfrac{2}{2+2} = \dfrac{2}{4} = 0.5.$

**Mode.** $\dfrac{\alpha-1}{\alpha+\beta-2} = \dfrac{2-1}{2+2-2} = \dfrac{1}{2} = 0.5.$

Mean and mode agree at $0.5$, exactly as they should for a symmetric curve. The peak height there is $f(0.5) = 6 \times 0.5 \times 0.5 = 1.5$. Note $1.5 > 1$: a perfectly legal *density* value, illustrating the prerequisite's point that a density (probability per unit length) may exceed 1, whereas a probability never can. Beta(2,2) says: "$p$ is probably somewhere in the middle, but I'm only mildly confident" — a soft preference for $0.5$, not a sharp one.

### Worked instance 2 — Beta(8,2): a skewed curve leaning toward 1

Now take $\alpha = 8$, $\beta = 2$ — like having seen 7 imagined successes and 1 imagined failure ($\alpha-1 = 7$, $\beta-1 = 1$). The core is
$$ p^{\,8-1}(1-p)^{\,2-1} = p^{7}(1-p). $$
Because $\alpha > \beta$, the strong $p^7$ factor pushes plausibility toward large $p$, while the single $(1-p)$ factor still forces the density to 0 at $p=1$. The result is a hump that leans hard toward 1 — **skewed**, not symmetric, so this instance exercises the asymmetric branch the first one did not.

**Mean.** $\dfrac{\alpha}{\alpha+\beta} = \dfrac{8}{8+2} = \dfrac{8}{10} = 0.8.$

**Mode.** $\dfrac{\alpha-1}{\alpha+\beta-2} = \dfrac{8-1}{8+2-2} = \dfrac{7}{8} = 0.875.$

Here mean $= 0.8$ and mode $= 0.875$ **differ**, which is the signature of a skewed curve: the peak (most plausible single value, $0.875$) sits to the right of the balance point (center of mass, $0.8$), because the long left tail trailing down toward 0 drags the average below the peak. Contrast this with Beta(2,2), where symmetry forced mean and mode to coincide. Beta(8,2) says: "$p$ is probably high — most likely around $0.875$ — though values somewhat lower remain plausible."

### Why it matters

The reason the Beta distribution earns its own name and constant comes from its core's shape. Imagine flipping a bent coin with unknown heads-probability $p$ and seeing $h$ heads and $t$ tails; the chance of that exact sequence is proportional to $p^{h}(1-p)^{t}$ — large $p$ explains many heads, small $p$ explains many tails. That is *algebraically the same shape* as the Beta core $p^{\alpha-1}(1-p)^{\beta-1}$. Because the two forms match, a Beta distribution is the natural way to express a belief *about* an unknown probability $p$ before and after seeing coin-like data: the pseudo-counts $\alpha,\beta$ play the role of (prior) heads and tails. This match is precisely what makes Beta so useful for modeling uncertain success-rates — a role that more advanced topics build on directly.

## Prerequisites

- [[probability-distribution]]

## Sources

_none_
