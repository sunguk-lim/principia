---
id: skewness
title: Skewness
summary: Skewness is the asymmetry of a distribution — whether its probability leans symmetrically about a center or trails off into one long tail.
type: concept
tags: [math/probability]
prereqs: [expectation, cumulative-distribution-function]
sources: [study-notes#5.5]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Skewness

## Summary

**Skewness** is the *asymmetry* of a distribution — whether its probability leans symmetrically about a center or trails off into one long tail. The cleanest way to see it is to compare a distribution's three "centers." The **mean** is the [[expectation]] $E[X]$, the probability-weighted average value. The **median** is the value $m$ where the [[cumulative-distribution-function]] reaches one half, $F(m) = \tfrac12$ — the point with equal probability on each side. The **mode** is the location of the density peak, the single most likely value (the tallest point of the pdf). For a symmetric, single-peaked distribution all three coincide. When the distribution has a long *right* tail (right-skew), they separate in the order mode $<$ median $<$ mean; a long *left* tail mirrors this to mean $<$ median $<$ mode. The reason is **tail sensitivity**: the three centers each "feel" a far-out tail differently. The mean integrates value against probability, so a long tail of distant values physically drags the balance point toward it; the median, being only the 50%-crossing of the running total, shifts much less; the mode ignores the tail entirely, sitting at the peak regardless of what happens far away. So a long right tail pulls the mean farthest, the median a little, the mode not at all — hence mode $<$ median $<$ mean. This three-way ordering is a reliable *rule of thumb*, not a theorem: multimodal or certain discrete distributions can violate it. The worked log-normal case ($\mu=0,\sigma=1$) gives mode $\approx 0.368 <$ median $= 1 <$ mean $\approx 1.649$ — a textbook right skew.

## Grounded explanation

### What the concept *is*

Two distributions can share the same average and the same spread yet *look* completely different: one a tidy bell, symmetric about its center, the other lopsided — bunched on the left with a long thin tail stretching off to the right. **Skewness** is the name for that difference. It is the *asymmetry* of a distribution: the extent to which probability fails to mirror itself about a central value, instead leaning to one side and trailing into a tail on the other.

To make "asymmetry" precise without inventing new machinery, compare three different notions of the distribution's *center*. Each is already available from the prerequisites; they only agree when the distribution is symmetric, and the *way they disagree* is exactly the skew.

- **Mean.** The mean is the [[expectation]] $\mu = E[X]$ — the probability-weighted average of the values, the balance point of the distribution viewed as distributed mass. It answers "what value does $X$ come out to on average?"

- **Median.** The median is the value $m$ at which the [[cumulative-distribution-function]] $F(x) = P(X \le x)$ — the running total of probability accumulated from the far left up to $x$ — first reaches one half:
  $$ F(m) = \tfrac{1}{2}. $$
  By construction $X$ is equally likely to land below $m$ as above it (probability $\tfrac12$ on each side). The median answers "what value splits the probability into two equal halves?"

- **Mode.** The mode is the location of the *density peak* — the value $x^\star$ where the probability density function is tallest, $f(x^\star) = \max_x f(x)$. (For a discrete variable it is the value of largest mass; for a continuous one, the highest point of the height curve.) The mode answers "what single value is most likely / most concentrated?" Unlike the other two it is a purely *local* feature: it depends only on the shape near the peak, not on probability elsewhere.

A distribution that is **symmetric** about a point and has a **single peak** at that same point has all three centers stacked on top of each other: $\text{mode} = \text{median} = \text{mean}$. The peak sits at the axis of symmetry; the symmetry forces the 50% crossing to that axis too; and the balance point of symmetric mass is the axis. Skewness is precisely what happens when symmetry breaks and these three pull apart.

### The generic signature: the three-center ordering

When a distribution is **right-skewed** — most of its probability bunched at smaller values, with a long thin tail reaching toward larger ones — the three centers separate into the order
$$ \text{mode} \;<\; \text{median} \;<\; \text{mean}. $$
**Left-skew** is the exact mirror image (a long tail toward *smaller* values), giving
$$ \text{mean} \;<\; \text{median} \;<\; \text{mode}. $$
These orderings are the *generic signature* of skew — they recur across many of the standard right-skewed families (exponential, gamma, chi-squared, Poisson, and others), not just the one example we will work below. The mean always sits on the *tail side*, the mode on the *bulk side*, and the median between them.

### Why — tail sensitivity

The ordering is not a coincidence of formulas; it follows from a single idea, **tail sensitivity**: each of the three centers reacts differently to probability sitting far out in a tail.

- **The mean is the most tail-sensitive.** Because $\mu = E[X]$ is a value-weighted average — each value counted in proportion to its probability, $\sum_x x\,p(x)$ or $\int x\,f(x)\,dx$ — a tail contributes terms in which a *large* value $x$ is multiplied by its (small) probability. Even a thin tail of far-out values adds positive pull, and because the value $x$ itself is large the pull can be substantial. Picture the [[expectation]]'s "balance point of a loaded rod" image: hanging even a light weight far out along the rod tips the balance noticeably, because leverage grows with distance. A long right tail therefore drags the mean rightward, toward the tail.

- **The median moves less.** The median is the 50%-crossing of the [[cumulative-distribution-function]], $F(m) = \tfrac12$. What matters for $m$ is only *how much* probability lies on each side, never *how far out* it sits. Stretching the right tail farther out moves distant probability around but, as long as it stays on the right side of $m$, does not change the fact that half the probability is below $m$. So the median responds to the *redistribution* of probability but is blind to the *distance* the tail reaches. It shifts toward the tail somewhat — because skewing the shape does move the half-way point — but far less than the leverage-driven mean.

- **The mode does not move at all.** The mode is just the location of the density peak. A long tail can do whatever it likes far from the peak; as long as the bulk stays where it is, the tallest point of the density stays put. The mode ignores the tail entirely.

Put the three reactions side by side for a long *right* tail: the mode stays at the bulk, the median creeps a little toward the tail, and the mean is dragged farthest toward the tail. That is exactly $\text{mode} < \text{median} < \text{mean}$. The left-skew ordering is the same argument with the tail on the other side, flipping every inequality.

### A rule of thumb, not a theorem

This three-way ordering is reliable enough to be the standard mental picture of skew, but it is a *rule of thumb*, not a guaranteed law. The unreliable member is the **mode**: as a purely local feature of the peak, it misbehaves for **multimodal** distributions (several peaks — *which* peak is the mode can jump around and need not sit on the bulk side at all) and for certain **discrete** distributions, where the order can scramble. There even exist skewed distributions whose conventional asymmetry measures disagree in sign with $\text{mean} - \text{median}$. What *is* robust is the pair mean-vs-median: the signed gap $\text{mean} - \text{median}$ tracks the side the tail is on dependably, because that gap (rescaled by the spread) is itself taken *as* one definition of skew — the so-called nonparametric skew, whose sign defines that notion of skew by construction. So when the rule and an exact measure might conflict, trust the mean-versus-median comparison over any claim resting on the mode.

(Two further refinements live in their own concepts, not here. One is a measure built from the [[expectation]] of the *cubed* standardized deviation — the third-moment skewness — which gives skew a single signed number. The other is a transformation-based notion: a distribution counts as strongly right-skewed when it is a *convex* increasing reshaping of a symmetric one, the curvature of that reshaping being what stretches one tail and compresses the other; under that stronger condition, with a single peak, the ordering mode $\le$ median $\le$ mean is actually guaranteed. Both are separate topics; the tail-sensitivity picture above is the load-bearing intuition.)

### Worked instance — the log-normal with $\mu = 0,\ \sigma = 1$

Take a concrete right-skewed distribution and watch the three centers separate. Let $X$ be **log-normal** with parameters $\mu = 0$ and $\sigma = 1$: that means $\ln X$ is a standard normal variable (the familiar symmetric bell, centered at $0$ with spread $1$), so $X$ itself takes only positive values and trails off into a long right tail. We compute each center its own way — each by the route its *definition* dictates — and the three closed forms below are standard results for the log-normal; the point here is the comparison they produce.

- **Mode** (peak of the density) $= e^{\mu - \sigma^2} = e^{0 - 1} = e^{-1} \approx 0.368$. The most-likely single value sits well *below* $1$, because the bulk of a log-normal is squeezed toward small positive numbers.

- **Median** (the $x$ with $F(x) = \tfrac12$) $= e^{\mu} = e^{0} = 1$. This is exact and intuitive: $\ln X$ is symmetric about $0$, so its median is $0$; the median is *order-based*, so it passes straight through the increasing map $x \mapsto e^x$, landing at $e^0 = 1$. Half the probability lies below $1$, half above.

- **Mean** (the [[expectation]] $E[X]$) $= e^{\mu + \sigma^2/2} = e^{0 + 1/2} = e^{0.5} \approx 1.649$. The mean is *value-weighted*, so the long right tail of large values drags it well above the median — exactly the tail-sensitivity effect, now in numbers.

Lining them up:
$$ \underbrace{0.368}_{\text{mode}} \;<\; \underbrace{1}_{\text{median}} \;<\; \underbrace{1.649}_{\text{mean}}. $$
A clean, strict right skew: mode $<$ median $<$ mean, with the mean pulled farthest right by the tail and the mode anchored at the bulk. This instance is non-degenerate — all three centers are *distinct* (no two collapse together, which would hide the asymmetry), and they fall in the exact generic order the tail-sensitivity argument predicted. (For the log-normal this ordering is in fact strict and never scrambles, because it is a convex reshaping of the symmetric normal — but that guarantee is the separate transformation story noted above; the numbers here illustrate the right-skew case of the general rule.)

### Pulling it together

Skewness is asymmetry, made legible by comparing three centers: the **mean** $E[X]$ (the [[expectation]], value-weighted), the **median** (the $x$ where the [[cumulative-distribution-function]] hits $\tfrac12$), and the **mode** (the density peak). They coincide under symmetry and separate under skew, in the order mode $<$ median $<$ mean for a right tail and its mirror for a left tail. The single explanation is tail sensitivity — the mean feels a far tail most (leverage on a weighted average), the median a little (only the 50% split matters, not distance), the mode not at all (a purely local peak). The log-normal $(\mu=0,\sigma=1)$ makes it concrete at $0.368 < 1 < 1.649$. Treat the ordering as a dependable rule of thumb whose weak link is the mode, and lean on the mean-versus-median gap when you need the asymmetry's direction for certain.

## Prerequisites

- [[expectation]]
- [[cumulative-distribution-function]]

## Sources

- study-notes §5.5 — "Skewness: how general is mode < median < mean?"
