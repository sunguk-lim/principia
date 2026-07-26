---
id: normal-distribution
title: Normal Distribution
summary: "The normal distribution (or Gaussian) is the most important continuous probability-distribution: a smooth, symmetric bell-shaped density curve."
type: concept
tags: [math/probability]
prereqs: [probability-distribution, exponential-function]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Normal Distribution

## Summary

The **normal distribution** (or **Gaussian**) is the most important continuous [[probability-distribution]]: a smooth, symmetric **bell-shaped** density curve. It is described by two numbers — the **mean** $\mu$ (the center the bell sits over) and the **standard deviation** $\sigma$ (how wide the bell spreads). Its probability density function is $f(x) = \frac{1}{\sigma\sqrt{2\pi}}\,\exp\!\big(-\frac{(x-\mu)^2}{2\sigma^2}\big)$, built from the [[exponential-function]] applied to a *negative squared distance* from the center. That single ingredient explains the whole shape: the density is highest at $x=\mu$ (zero distance), it is mirror-symmetric about $\mu$ (because distance is squared, so $+d$ and $-d$ score the same), and it dies away fast in both directions (because squared distance grows quickly and $\exp$ of a large negative number is tiny). The lead constant $\frac{1}{\sigma\sqrt{2\pi}}$ is not arbitrary — it is exactly the scale that makes the total area under the curve equal 1, as any [[probability-distribution]] demands. It is ubiquitous because sums of many small independent effects tend to pile up into this bell.

## Grounded explanation

### What the concept *is*

From [[probability-distribution]] we know that a continuous random quantity $X$ is described by a **probability density function** (pdf) $f$: a non-negative height curve where the probability that $X$ lands in an interval is the **area** under $f$ over that interval, and the **total area must equal exactly 1** (normalization — the quantity is certain to take *some* value). A density is probability *per unit length*, not a probability; a single exact point has probability 0.

The **normal distribution** is one specific, exceptionally important choice of that curve $f$. Instead of a flat rectangle (the uniform pdf from the prerequisite), its curve is a smooth **bell**: a single rounded hump, tallest in the middle, tapering symmetrically to near-zero on both sides and never quite touching the axis. The concept here is *this particular shape and the formula that produces it* — and, crucially, *why* each piece of the formula creates the feature it does.

### The two symbols that pin down the bell

A normal distribution is fixed by exactly two numbers:

- $\mu$ (Greek "mu") — the **mean**: the location on the number line where the bell is centered. Moving $\mu$ slides the whole curve left or right without changing its shape.
- $\sigma$ (Greek "sigma") — the **standard deviation**: a positive number measuring the **spread**. Small $\sigma$ → a tall, narrow bell; large $\sigma$ → a short, wide bell. Its square $\sigma^2$ is called the **variance**, but we will work with $\sigma$ directly.

With these, the pdf is

$$ f(x) = \frac{1}{\sigma\sqrt{2\pi}}\,\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right). $$

Here $\exp(\,\cdot\,)$ is the [[exponential-function]] $e^{(\cdot)}$, $\pi \approx 3.14159$ is the usual circle constant, and $\sqrt{2\pi} \approx 2.5066$. Read the formula in two halves: the **kernel** $\exp\!\big(-\frac{(x-\mu)^2}{2\sigma^2}\big)$, which gives the bell its shape, and the **front constant** $\frac{1}{\sigma\sqrt{2\pi}}$, which only rescales the height. We take them in turn.

### Why the kernel makes a symmetric bell that decays fast

Look first at the quantity $x-\mu$: this is the **signed distance** of the point $x$ from the center $\mu$. The kernel does three things to it, each producing one visible feature of the bell.

1. **Squaring → symmetry.** The kernel uses $(x-\mu)^2$, the *squared* distance. Squaring throws away the sign: a point one unit to the right of $\mu$ ($x-\mu = +1$) and a point one unit to the left ($x-\mu = -1$) both give $(x-\mu)^2 = 1$, hence identical density. So the curve is a perfect mirror image about the vertical line $x=\mu$. The bell is **symmetric about its mean**, and that symmetry is *caused by* the square.

2. **Negative sign + the exponential → a peak at the center that falls off.** Recall from [[exponential-function]] that $e^{t}$ is always positive and monotonic: larger $t$ gives larger $e^t$, and $e^0 = 1$ is its value at zero. The kernel feeds it $t = -\frac{(x-\mu)^2}{2\sigma^2}$, which is always $\le 0$. It equals **0 only when $x=\mu$** (zero distance), where the kernel is $e^0 = 1$ — its largest possible value. As $x$ moves away from $\mu$, the squared distance grows, $t$ becomes more negative, and $e^t$ shrinks toward 0. So the curve **peaks exactly at $x=\mu$** and slopes downward on both sides. Because $\exp$ stays strictly positive, the curve never reaches 0 — the bell has **tails that extend forever** but get vanishingly thin.

3. **Squared distance + exp → *fast* decay (thin tails).** Why a bell and not a slow, lazy slope? Because the input to $\exp$ falls off as the *square* of the distance. Doubling the distance from $\mu$ quadruples the squared distance, so the exponent becomes four times as negative, and $\exp$ of that is dramatically smaller. Squared growth inside a negative exponential means the density **collapses rapidly** once you are a few multiples of $\sigma$ away from center. That fast collapse is exactly what gives the Gaussian its characteristic "narrow shoulders, near-flat tails" silhouette rather than a broad plateau.

The role of $\sigma$ now reads off the kernel directly. It appears as $2\sigma^2$ in the denominator under the squared distance. Distance is therefore measured *in units of $\sigma$*: what matters is the ratio $\frac{x-\mu}{\sigma}$. If $\sigma$ is small, even a modest physical distance is "many $\sigma$ away," so the exponent plunges and the bell is narrow; if $\sigma$ is large, you must travel far before the exponent bites, so the bell is wide. A useful landmark: at exactly one $\sigma$ from center ($x = \mu \pm \sigma$) the exponent is $-\frac{\sigma^2}{2\sigma^2} = -\frac12$, the same on both sides — these are the **inflection points** where the curve switches from bending down to bending up, the "shoulders" of the bell.

### Why the front constant is forced, not chosen

The kernel alone is a perfectly good bell shape, but it is **not yet a pdf** — its total area is not 1. [[probability-distribution]] requires normalization: the whole area under $f$ must equal exactly 1, because $X$ is certain to land *somewhere*. So we must divide the kernel by whatever its raw area happens to be.

It is a standard (and famous) result of calculus that the area under the bare kernel is

$$ \int_{-\infty}^{\infty} \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right) dx = \sigma\sqrt{2\pi}. $$

That is the *entire* reason the front constant is $\frac{1}{\sigma\sqrt{2\pi}}$: it is the reciprocal of the kernel's natural area, dividing the area back down to 1. So $\frac{1}{\sigma\sqrt{2\pi}}$ is not a magic decoration — it is precisely the **normalizer** demanded by the closed-world rule "total area = 1." (Notice it also scales correctly with spread: a wider bell, larger $\sigma$, has a larger raw area $\sigma\sqrt{2\pi}$, so it is divided by more, making it *shorter* — which is why widening a bell lowers its peak, keeping the area fixed at 1.)

Note this front value can itself exceed 1, and that is allowed: as [[probability-distribution]] stresses, a *density* may be larger than 1; only a *probability* (an area) may not. For a very narrow bell (tiny $\sigma$), the peak height $\frac{1}{\sigma\sqrt{2\pi}}$ is huge, but the curve is correspondingly thin, so the enclosed area stays exactly 1.

### The 68–95–99.7 rule

Because the shape is completely fixed once you measure distance in units of $\sigma$, the *fraction of area* (i.e. probability) lying within a given number of $\sigma$ of the center is always the same, for every normal distribution:

- within $\mu \pm 1\sigma$: about **68%** of the area,
- within $\mu \pm 2\sigma$: about **95%**,
- within $\mu \pm 3\sigma$: about **99.7%**.

So a normal quantity lands within one standard deviation of its mean roughly two times in three, and almost never (about 3 in 1000) strays beyond three. These areas come from integrating the pdf; we quote them rather than derive them, but they follow purely from the bell's fixed shape.

### The standard normal and why this distribution is everywhere

The simplest case is $\mu = 0$, $\sigma = 1$, called the **standard normal**, whose variable is conventionally written $Z$. Its pdf simplifies to $f(x) = \frac{1}{\sqrt{2\pi}}\exp(-x^2/2)$. Every other normal is just a shifted, stretched copy: if $Z$ is standard normal, then $X = \mu + \sigma Z$ is normal with mean $\mu$ and standard deviation $\sigma$ — the $+\mu$ slides the center, the $\times\sigma$ stretches the width. So there is really only *one* shape, viewed through different choices of origin ($\mu$) and ruler ($\sigma$).

Why is it ubiquitous? In one line: the **Central Limit Theorem** says that when you add up *many small, independent random effects*, their sum tends toward a normal distribution almost regardless of what each individual effect looks like. Measurement errors, total of many tiny pushes, averages of large samples — these are sums of many little contributions, so the bell shows up over and over in nature and statistics.

### Worked instance

Let us evaluate the density at specific points and watch the mechanism produce real numbers. Throughout, use $\sqrt{2\pi} \approx 2.5066$ and recall from [[exponential-function]] that $e^0 = 1$ and $e^{-1/2} \approx 0.6065$.

**Standard normal ($\mu = 0$, $\sigma = 1$), at the peak $x = 0$.** The signed distance is $x - \mu = 0$, so the squared distance is 0, the exponent is $-\frac{0}{2\cdot 1} = 0$, and the kernel is $e^0 = 1$ — its maximum. The front constant is $\frac{1}{1\cdot 2.5066} = \frac{1}{2.5066} \approx 0.3989$. So
$$ f(0) = \frac{1}{\sqrt{2\pi}} \cdot e^{0} = 0.3989 \times 1 \approx 0.399. $$
The peak height is about $0.399$. (It exceeds nothing alarming — and note it is below 1 here because $\sigma = 1$ is not small.)

**Check the symmetry, at $x = 1$ and $x = -1$.** Both are one unit from center, so both have signed distance $\pm 1$ and squared distance $1$. The exponent is $-\frac{1^2}{2\cdot 1^2} = -\frac12$, and the kernel is $e^{-1/2} \approx 0.6065$ at *both* points — the square erased the sign. Hence
$$ f(1) = f(-1) = \frac{1}{\sqrt{2\pi}} \cdot e^{-1/2} = 0.3989 \times 0.6065 \approx 0.242. $$
Two things are confirmed at once: the densities at $+1$ and $-1$ are **equal** (symmetry), and each is **lower** than the peak $0.399$ (decay away from center). The point $x=\pm 1$ is exactly one $\sigma$ out — the inflection "shoulder."

**Shift the mean: $\mu = 2$, $\sigma = 1$.** Now the center moves to $x = 2$. At $x = 2$ the signed distance is $2 - 2 = 0$, so by the identical calculation the kernel is again $e^0 = 1$ and
$$ f(2) = \frac{1}{1\cdot\sqrt{2\pi}} \cdot e^{0} \approx 0.399. $$
The peak **height is unchanged** ($0.399$) but has **slid to $x = 2$** — because $\sigma$ is the same, only $\mu$ moved. This is the "shifted copy" claim made concrete: changing $\mu$ relocates the bell without reshaping it. (As a cross-check, $f$ at $x = 1$ for this shifted bell, distance $1-2 = -1$, gives $0.399 \times e^{-1/2} \approx 0.242$ — the same shoulder value as before, now sitting one unit *left* of the new center instead of at $-1$.)

These numbers exercise every branch of the formula: the peak (exponent 0, kernel 1), an off-center point (nonzero squared distance, shrunken kernel), the left–right symmetry (sign erased by squaring), and a mean shift (peak relocated, height preserved).

## Prerequisites

- [[probability-distribution]]
- [[exponential-function]]

## Sources

_none_
