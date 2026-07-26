---
id: nonparametric-skew
title: Nonparametric Skew
summary: "The nonparametric skew is the simplest robust number for the asymmetry studied in skewness: take the gap between the mean and the median, and divide it by the standard deviation,"
type: concept
tags: [math/probability]
prereqs: [skewness]
sources: [study-notes#5.5]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Nonparametric Skew

## Summary

The **nonparametric skew** is the simplest robust number for the asymmetry studied in [[skewness]]: take the gap between the mean and the median, and divide it by the standard deviation,

$$ S \;=\; \frac{\text{mean} - \text{median}}{\sigma}. $$

Here the **mean** is the value-weighted average, the **median** is the value splitting the probability into two equal halves, and $\sigma$ (the **standard deviation**) is the usual measure of spread — the square root of the average squared distance from the mean. Recall from [[skewness]] that a long *right* tail drags the mean above the median, a long *left* tail pulls it below, and under symmetry the two coincide. So the *sign* of $S$ reads off the skew direction directly: $S > 0$ means the mean sits above the median, which *is* a right tail; $S < 0$ is a left tail; $S = 0$ is the symmetric case. This is not a derived theorem but a *definition* — for this measure, positive skew **means** "mean above median," by construction. It is called *nonparametric* because it assumes no particular distribution shape; it uses only the two centers and the spread, quantities any finite-variance distribution has. It is *robust* because, of the three centers in [[skewness]], the unreliable one is the mode (a purely local feature of the peak), whereas the mean-versus-median pair is the dependable part of the ordering — so a measure built on that pair never depends on the shaky member. Finally there is an exact bound, $|\text{mean} - \text{median}| \le \sigma$, true for *any* distribution with finite variance, so $S$ always lies in $[-1, 1]$. The worked log-normal $(\mu=0,\sigma=1)$ has mean $\approx 1.649$, median $1$, so $\text{mean}-\text{median} \approx 0.649$, and dividing by its standard deviation $\approx 2.161$ gives $S \approx 0.30 > 0$ — a positive nonparametric skew, well inside the $\pm 1$ bound.

## Grounded explanation

### What the concept *is*

[[skewness]] gives a *picture* of asymmetry by comparing three centers — the mean (value-weighted average), the median (the value splitting probability in half), and the mode (the density peak) — and noting that a long right tail separates them in the order mode $<$ median $<$ mean, with the left-tail case mirrored. That picture is qualitative: it tells you the *direction* of the lean but hands you no single number to put on it, and it comes with a warning that the ordering is only a rule of thumb.

The **nonparametric skew** turns the dependable part of that picture into one number. It discards the mode entirely and keeps only the two reliable centers, measuring how far apart they are *in units of the spread*:

$$ S \;=\; \frac{\text{mean} - \text{median}}{\sigma}. $$

Three ingredients, each already familiar from [[skewness]] or its surroundings, all of which any finite-variance distribution possesses:

- The **mean** $\mu$ — the value-weighted average, the balance point of the probability mass.
- The **median** $m$ — the value at which exactly half the probability lies below and half above.
- The **standard deviation** $\sigma$ — the typical size of a deviation from the mean; concretely, the square root of the average of $(X - \mu)^2$. It is the natural yardstick for "how spread out is this distribution," and dividing by it makes $S$ a pure number, free of the units of $X$ (rescaling all the values, say from metres to centimetres, leaves $S$ unchanged because numerator and denominator scale together).

The numerator $\text{mean} - \text{median}$ is the *signed* gap between the two reliable centers; the denominator $\sigma$ rescales that gap so the result is comparable across distributions of wildly different magnitude. The word *nonparametric* signals exactly this generality: unlike a formula tied to a specific family (the log-normal's skew written in its parameter $\sigma$, say), $S$ is computed from the distribution's own mean, median, and spread, whatever shape it has.

### Why the sign defines the direction — by construction

The central feature of $S$ is that its **sign is the skew direction, by definition rather than by argument.** In [[skewness]] the link between "right tail" and "mean above median" was an *explanation* — tail sensitivity drags the value-weighted mean toward a far tail while the median, caring only about the 50% split, barely moves. The nonparametric skew simply *adopts* that gap as the meaning of skew:

- $S > 0 \iff \text{mean} > \text{median}$ — the mean is pulled to the right of the median, which is what a long right tail does. **Positive nonparametric skew = right-skewed**, by fiat.
- $S < 0 \iff \text{mean} < \text{median}$ — left-skewed.
- $S = 0 \iff \text{mean} = \text{median}$ — the symmetric case (and the boundary).

So whereas [[skewness]]'s ordering is a *claim that can be wrong* for awkward distributions, $S$ cannot disagree with itself: asking "is this distribution right-skewed under the nonparametric measure?" *is* asking "is the mean above the median?" — the same question. The denominator $\sigma$ is strictly positive (any non-degenerate distribution has $\sigma > 0$), so dividing by it never flips the sign; it only sets the scale. The direction lives entirely in the numerator.

### Why it is robust — the mode is the weak link

[[skewness]] is explicit that the three-center ordering is a *rule of thumb*, not a theorem, and it identifies the culprit precisely: the **mode**. The mode is a purely *local* feature — the single tallest point of the density — so it tells you nothing about how probability is arranged away from the peak. For a multimodal distribution (several peaks) "the mode" can jump between peaks and need not sit on the bulk side at all; for certain discrete distributions the order scrambles. In fact, under weak measures of skew, *all six* orderings of the three centers are achievable, and the mode is the one that makes them so.

What survives this is the **pair mean-versus-median**. Their signed difference tracks the tail side dependably, because that difference is not *subject to* a separate notion of skew — it *defines* one. The nonparametric skew is robust precisely because it is built from this stable pair and *omits the mode*. It cannot be sabotaged by a wandering peak, because it never consults the peak. This is the design choice that distinguishes $S$ from the full mode $<$ median $<$ mean picture: throw away the unreliable center, keep the two reliable ones, and you get a measure whose verdict you can trust.

### Why it always lies in $[-1, 1]$ — the exact bound

A measure of asymmetry is far more useful if its scale is fixed, so that "$S = 0.3$" means something comparable across distributions. The nonparametric skew has exactly such a fixed range, and it rests on an **exact inequality** that holds for *every* distribution with finite variance:

$$ |\text{mean} - \text{median}| \;\le\; \sigma. $$

In words: the mean and median can never be farther apart than one standard deviation. The median is, among all candidate centers $c$, the one minimising the average *absolute* distance $E\,|X - c|$; the mean minimises the average *squared* distance. Because the absolute-distance-minimiser cannot do worse at its own job than the mean does, and because average absolute distance is itself bounded by the root-mean-square distance $\sigma$ (a consequence of the fact that an average magnitude never exceeds the corresponding root-mean-square), the gap between the two centers is squeezed to at most $\sigma$. That is the bound. (The full chain is a standard result; the load-bearing point for us is only its *consequence*.)

Divide the bound through by $\sigma > 0$ and it says exactly

$$ |S| \;=\; \frac{|\text{mean} - \text{median}|}{\sigma} \;\le\; 1, \qquad\text{i.e.}\qquad S \in [-1,\,1]. $$

So the nonparametric skew is automatically normalised: $0$ is the symmetric center, $+1$ and $-1$ are the extreme possible right- and left-leans, and any real distribution falls in between. No distribution can ever report a nonparametric skew outside this window — the bound is not a convention but a theorem about where the mean and median can sit relative to the spread.

### Worked instance — the log-normal with $\mu = 0,\ \sigma = 1$

Use the same right-skewed distribution worked in [[skewness]], the log-normal with $\mu = 0$, $\sigma = 1$ (so $\ln X$ is a standard normal bell and $X$ trails off into a long right tail). From [[skewness]] we already have its two reliable centers:

- **Mean** $= e^{\mu + \sigma^2/2} = e^{0.5} \approx 1.649$ (the value-weighted average, dragged up by the tail).
- **Median** $= e^{\mu} = e^{0} = 1$ (the order-based half-way point).

Their signed gap is the numerator:

$$ \text{mean} - \text{median} \;\approx\; 1.649 - 1 \;=\; 0.649. $$

It is positive, so already the *sign* announces a right skew — consistent with the long right tail, and matching the mode $<$ median $<$ mean picture from [[skewness]] without ever needing the mode.

For the denominator we need this log-normal's standard deviation. Its variance is the standard log-normal result $\big(e^{\sigma^2} - 1\big)\,e^{2\mu + \sigma^2}$; with $\mu = 0, \sigma = 1$ that is $(e - 1)\,e \approx (1.718)(2.718) \approx 4.671$, so

$$ \sigma_{\text{LN}} \;=\; \sqrt{4.671} \;\approx\; 2.161. $$

Putting it together:

$$ S \;=\; \frac{\text{mean} - \text{median}}{\sigma_{\text{LN}}} \;\approx\; \frac{0.649}{2.161} \;\approx\; 0.30. $$

A clean **positive** nonparametric skew of about $0.30$. This instance is non-degenerate in the way that matters here: the numerator is genuinely nonzero (mean and median are distinct, so the measure is not hiding asymmetry by collapsing to $0$), and the result $0.30$ sits comfortably *inside* the proven window $[-1, 1]$ — confirming the bound rather than grazing it. The number says, on a fixed and unit-free scale, "moderately right-skewed," and its sign agrees with the tail direction by the very construction of the measure.

### Pulling it together

The nonparametric skew is the one-number, robust distillation of [[skewness]]. It keeps the two dependable centers — mean and median — discards the unreliable mode, and reports their signed gap in units of the spread: $S = (\text{mean} - \text{median})/\sigma$. Its sign *is* the skew direction, true by definition rather than by argument, so it can never contradict itself the way the full three-center ordering can. It is robust because it never touches the mode, the member that makes that ordering merely a rule of thumb. And it is bounded, $S \in [-1,1]$, because the mean and median of any finite-variance distribution lie within one standard deviation of each other — an exact inequality, not a convention. The log-normal $(\mu=0,\sigma=1)$ makes it concrete: a gap of $0.649$ over a spread of $2.161$ gives $S \approx 0.30$, a moderate right skew safely inside the $\pm 1$ window. (A different one-number measure, built instead from the average *cubed* standardised deviation — the moment skewness — gives skew its own signed value by a separate route; that is a distinct concept, not this one.)

## Prerequisites

- [[skewness]]

## Sources

- study-notes §5.5 — "Skewness: how general is mode < median < mean?" (the exact bound $|\text{mean}-\text{median}| \le \sigma$, the nonparametric skew $(\text{mean}-\text{median})/\sigma$ defining skew by its sign, and robustness via the mean-vs-median pair).
