---
id: moment-skewness
title: Moment Skewness
summary: Moment skewness is the standard quantitative measure of skewness — it turns the lopsidedness of a distribution into a single signed number $\gamma$ (Greek "gamma").
type: concept
tags: [math/probability]
prereqs: [skewness, expectation]
sources: [study-notes#5.5]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Moment Skewness

## Summary

**Moment skewness** is the standard *quantitative* measure of [[skewness]] — it turns the lopsidedness of a distribution into a single signed number $\gamma$ (Greek "gamma"). Where [[skewness]] is described qualitatively by comparing the three centers (mean, median, mode), moment skewness pins it to one figure: $\gamma$ is the **third standardized moment**, the [[expectation]] of the *cubed* standardized deviation, $\gamma = E\!\big[((X-\mu)/\sigma)^3\big]$, where $\mu = E[X]$ is the mean (the [[expectation]] of $X$) and $\sigma$ is the standard deviation (the typical distance from the mean). The quantity $(X-\mu)/\sigma$ is the **z-score** — how many standard deviations $X$ sits above ($+$) or below ($-$) the mean — and cubing it is the crucial move: an odd power *keeps the sign* (a negative cubed stays negative) while heavily amplifying large magnitudes. So values far out in a long *right* tail produce large *positive* cubes that dominate the average and push $\gamma > 0$ (right skew); a long left tail pushes $\gamma < 0$; a perfectly symmetric distribution has positive and negative cubes cancel exactly, giving $\gamma = 0$. The caveat to carry: because $\gamma$ is built from the third moment, it is a *different operationalization* of "skew" than the center-comparison picture, and for unusual (multimodal or discrete) distributions the two can even **disagree in sign**. For the log-normal, $\gamma$ is always positive and grows with the spread parameter $\sigma$: $\gamma = (e^{\sigma^2}+2)\sqrt{e^{\sigma^2}-1}$. With $\sigma = 1$ this is $\approx 6.18$ — strongly right-skewed; as $\sigma \to 0$ it collapses to $\gamma \to 0$, the symmetric limit.

## Grounded explanation

### What the concept *is*

[[skewness]] is the asymmetry of a distribution — whether its probability mirrors itself about a center or trails off into one long tail. The node on [[skewness]] makes that *qualitative*, by comparing three notions of "center": the **mean** (the [[expectation]] $\mu = E[X]$, the probability-weighted average / balance point), the **median** (the value splitting probability into two equal halves), and the **mode** (the location of the density peak). Their separation — mode $<$ median $<$ mean for a right tail, the mirror for a left tail — *signals* skew but does not *measure* it: it gives an ordering, not a number.

**Moment skewness** supplies the missing number. It is the standard quantitative measure of skew: a single signed scalar $\gamma$ whose sign says which way the distribution leans and whose magnitude says how strongly. Throughout, $\gamma$ (Greek "gamma") denotes this number, $\mu = E[X]$ is the mean, and $\sigma$ — the **standard deviation** — is the typical spread, defined as the square root of the variance $E[(X-\mu)^2]$ (the [[expectation]] of the squared deviation from the mean). The variance is built from the [[expectation]] as in that node; $\sigma$ is its square root, carried in the same units as $X$ so that "one $\sigma$" is a genuine distance along the value axis.

### Building the number: standardize, cube, average

The definition is assembled in three deliberate steps, each correcting a defect of a naive attempt.

**Step 1 — center it.** Skew is about the *shape* of the trailing, not about where the distribution happens to sit, so first remove the mean: work with the deviation $X - \mu$. This makes the measure ignore any constant shift of $X$.

**Step 2 — standardize it.** Skew should also not depend on the *units* or the *scale* — a distribution measured in centimeters is no more or less skewed than the same one measured in meters. So divide the deviation by the spread $\sigma$, forming the **z-score**
$$ Z = \frac{X - \mu}{\sigma}. $$
The z-score is a pure, unitless number: it reports *how many standard deviations* $X$ lies above the mean (positive) or below it (negative). A value one $\sigma$ above the mean has $Z = +1$; one two $\sigma$ below has $Z = -2$. Standardizing makes $\gamma$ **scale-invariant** — the same for $X$ and for $aX + b$ — which is exactly what a measure of pure shape must be.

**Step 3 — cube it, then average.** Now we need to convert "leans left or right" into a signed average. Why the *third* power specifically? Consider the candidates:

- The **first** power averages to zero by construction: $E[Z] = E[(X-\mu)/\sigma] = (E[X]-\mu)/\sigma = 0$, since the [[expectation]] of the deviation from the mean is zero (positive and negative deviations cancel — that is what "mean" means). So the first moment carries no skew information.
- The **second** power, $E[Z^2]$, is always $1$ (it is the variance of the standardized variable). Squaring throws away the sign — a deviation of $-3$ and one of $+3$ both become $+9$ — so a symmetric distribution and a skewed one are indistinguishable to it. The second moment measures *spread*, not lean.
- The **third** power is the first one that both *keeps the sign* and *weights the tails*. Cubing is an **odd** function: $(-2)^3 = -8$, $(+2)^3 = +8$ — the sign survives. And it is a *growing* power: a z-score of $3$ cubes to $27$, while one of $0.5$ cubes to $0.125$. So values far out in a tail contribute cubes vastly larger than those of the bulk near the center.

Putting the three steps together, **moment skewness** is the [[expectation]] of the cubed z-score:
$$ \gamma \;=\; E\!\left[\left(\frac{X-\mu}{\sigma}\right)^{3}\right]. $$
This is the **third standardized moment** ("third" for the cube, "standardized" for the division by $\sigma$, "moment" for the [[expectation]] of a power). The [[expectation]] here is computed exactly as in that node: weight each cubed-z value by the probability of the underlying $x$ and sum (or integrate) — averaging a transform of $X$ over the original distribution, without ever building the distribution of the cube itself.

### Why the sign reads the tail

The cube is what makes $\gamma$ read direction. Split the distribution into its left side (where $Z < 0$, contributing *negative* cubes) and its right side (where $Z > 0$, contributing *positive* cubes). The [[expectation]] averages all of them together, so $\gamma$ is a tug-of-war between the two signed piles.

For a **symmetric** distribution the two sides are mirror images: every value at $Z = +c$ is matched by an equally probable value at $Z = -c$, and $(+c)^3 + (-c)^3 = 0$. Every pair cancels, so $\gamma = 0$. Symmetry forces moment skewness to vanish — consistent with the center-comparison picture, where symmetry makes mode, median, and mean coincide.

For a **right-skewed** distribution — a long thin tail reaching toward large values — the far-out tail values have large positive z-scores, and cubing magnifies them out of all proportion to their (small) probabilities. Even though the tail is *thin*, each of its cubes is *enormous*, and there is no matching pile of equally extreme negative cubes on the (short, blunt) left side to cancel them. The positive pile wins: $\gamma > 0$. A long *left* tail is the mirror image — large *negative* cubes dominate — giving $\gamma < 0$. So the sign of $\gamma$ names the side the long tail is on, and its magnitude grows with how far and how heavily that tail reaches: this is the tail-sensitivity intuition of [[skewness]], now sharpened from an ordering into a number.

### A caveat: it is a *different* measure of skew

Moment skewness and the center-comparison view of [[skewness]] are two different *operationalizations* of the same loose idea, and they need not always agree. The [[skewness]] node already flags that the three-center ordering is a rule of thumb, not a theorem; the matching caution here is sharper. Because $\gamma$ is built entirely from the **third moment** — the cube-weighted [[expectation]] — it can, for unusual distributions, **disagree in sign** with the nonparametric reading of skew, the rescaled gap $(\text{mean} - \text{median})/\sigma$ whose sign *defines* skew by construction in the [[skewness]] node. For the common, well-behaved families the two notions point the same way, but for **multimodal** distributions (several peaks) or certain **discrete** ones, the cube-weighted average and the mean-versus-median gap can come out with opposite signs. The lesson is that "the skew" is not a single unambiguous quantity: $\gamma$ is *one* precise answer (the moment answer), the nonparametric skew is *another*, and they are different functionals of the distribution that happen to coincide in the easy cases. There is also a stronger, transformation-based ordering — counting a distribution as right-skewed when it is a *convex* increasing reshaping of a symmetric one (van Zwet's convex transformation order) — under which, with a single peak, the three centers cannot scramble; but that is a separate, stricter notion than the third moment.

### Worked instance — the log-normal

For the **log-normal** distribution (the variable $X$ whose logarithm $\ln X$ is a symmetric normal bell, so $X$ takes only positive values and trails into a long right tail — the same example worked in [[skewness]]), moment skewness has a clean closed form in terms of its single spread parameter $\sigma$:
$$ \gamma \;=\; \left(e^{\sigma^2} + 2\right)\sqrt{\,e^{\sigma^2} - 1\,}. $$
Because $e^{\sigma^2} > 1$ for any $\sigma > 0$, both factors are strictly positive, so $\gamma > 0$ *always*: the log-normal is right-skewed for every nonzero spread, and the order of its centers never scrambles. This is the value-bearing, non-degenerate case — let us run real numbers and also check the limit.

Take $\sigma = 1$. Then $e^{\sigma^2} = e^{1} = e \approx 2.71828$. Substituting:

- First factor: $e^{\sigma^2} + 2 = 2.71828 + 2 = 4.71828$.
- Inside the root: $e^{\sigma^2} - 1 = 2.71828 - 1 = 1.71828$, whose square root is $\sqrt{1.71828} \approx 1.31083$.
- Multiply: $\gamma = 4.71828 \times 1.31083 \approx 6.185$.

So $\gamma \approx 6.18$ — a *strongly* right-skewed distribution (for comparison, $\gamma = 0$ is symmetric, and values of one or two already count as noticeably skewed). The large positive number is the long upper tail of the log-normal making its presence felt: those rare but extreme large values cube into a huge positive pile that the [[expectation]] cannot ignore.

Now the **degenerate limit**, to confirm the formula behaves. As $\sigma \to 0$, the exponent $\sigma^2 \to 0$, so $e^{\sigma^2} \to e^0 = 1$. The root $\sqrt{e^{\sigma^2} - 1} \to \sqrt{1 - 1} = \sqrt{0} = 0$, while the first factor tends to $1 + 2 = 3$ (finite). Their product tends to $3 \times 0 = 0$, so $\gamma \to 0$. This is exactly right: as the spread vanishes the log-normal collapses toward a single spike, which is symmetric (trivially), and a symmetric distribution must have $\gamma = 0$. Between these — small $\sigma$ giving small $\gamma$, larger $\sigma$ giving larger $\gamma$ — moment skewness grows monotonically with $\sigma$, the same parameter that fans the three centers apart in [[skewness]]. The number $\gamma$ and the ordering tell one consistent story for this family.

### Pulling it together

Moment skewness $\gamma$ is the standard *quantitative* measure of [[skewness]]: the third standardized moment, $\gamma = E[((X-\mu)/\sigma)^3]$ — the [[expectation]] of the cubed z-score. Standardizing (subtract the mean $\mu = E[X]$, divide by the spread $\sigma$) makes it ignore location and scale, leaving pure shape; cubing is the load-bearing choice, the lowest odd power that *keeps the sign* of a deviation while *amplifying* far-out tail values, so the [[expectation]] of those cubes comes out positive for a right tail ($\gamma > 0$), negative for a left tail ($\gamma < 0$), and zero under symmetry (matching cubes cancel). It is a distinct operationalization from the mean-median-mode picture and can disagree in sign with the nonparametric skew for odd (multimodal or discrete) distributions. The log-normal makes it concrete: $\gamma = (e^{\sigma^2}+2)\sqrt{e^{\sigma^2}-1}$, always positive, $\approx 6.18$ at $\sigma = 1$ and $\to 0$ as $\sigma \to 0$.

## Prerequisites

- [[skewness]]
- [[expectation]]

## Sources

- study-notes §5.5 — "Skewness: how general is mode < median < mean?" (moment skewness $\gamma$, the third standardized moment; log-normal formula and caveat)
