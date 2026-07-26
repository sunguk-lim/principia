---
id: moment-generating-function
title: Moment Generating Function
summary: The moment generating function (MGF) of a random variable $X$ is a single function $M_X(t) = E[e^{tX}]$ — for each real number $t$, it is the expectation of the exponential…
type: concept
tags: [math/probability]
prereqs: [expectation, random-variable]
sources: [study-notes.html §5.4]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Moment Generating Function

## Summary

The **moment generating function** (MGF) of a random variable $X$ is a single function $M_X(t) = E[e^{tX}]$ — for each real number $t$, it is the [[expectation]] of the exponential $e^{tX}$. It packs the entire shape of $X$ into one function of the dummy variable $t$. The name announces its purpose: it *generates the moments* of $X$, where the $k$-th **moment** is $E[X^k]$ (the mean is the first, $E[X^2]$ the second, and so on). The trick is differentiation at the origin. Because $e^{tX}$ expands as $1 + tX + \tfrac{t^2}{2}X^2 + \cdots$, taking the [[expectation]] term by term puts the moments into the coefficients; differentiating $k$ times and setting $t=0$ strips everything away except the $k$-th moment. So $M_X'(0) = E[X]$ recovers the mean and $M_X''(0) = E[X^2]$ the second moment. A landmark example is the normal distribution $N(\mu, \sigma^2)$ (the familiar symmetric bell curve with center $\mu$ and spread $\sigma^2$): its MGF is $M(t) = \exp(\mu t + \tfrac{1}{2}\sigma^2 t^2)$, obtained by *completing the square* inside the defining integral. One immediate payoff: if $Y \sim N(\mu,\sigma^2)$ then $E[e^Y]$ is just the normal MGF read off at $t=1$, giving $e^{\mu + \sigma^2/2}$ — which is exactly the mean of the log-normal variable $e^Y$.

## Grounded explanation

### What the concept *is*

Start from [[expectation]]: for a [[random-variable]] $X$, $E[g(X)]$ is the probability-weighted average of the transformed value $g(X)$, computed by averaging $g$ over $X$'s own distribution (the law of the unconscious statistician). The **moment generating function** picks one particular family of transforms and bundles the results. Introduce a real auxiliary variable $t$ — a knob we are free to turn, not a random quantity — and for each fixed $t$ form the transform $g(x) = e^{tx}$. Its [[expectation]] is a number depending on $t$. Letting $t$ range produces a *function*:

$$ M_X(t) = E\!\left[e^{tX}\right]. $$

Here $e$ is the base of the natural exponential, $e^{tX}$ is the random variable that outputs $e^{tx}$ whenever $X$ outputs $x$, and $M_X(t)$ (read "the MGF of $X$ at $t$") is the resulting average. At $t=0$ the transform is $e^{0}=1$ for every outcome, so $M_X(0) = E[1] = 1$ always — the MGF is pinned to pass through $1$ at the origin. The whole content lives in how it bends away from that point as $t$ moves, and that bending is what encodes $X$.

### Why it is called "moment generating"

A **moment** of $X$ is an [[expectation]] of a power: the $k$-th moment is $E[X^k]$. The first moment $E[X]$ is the mean; the second moment $E[X^2]$ feeds the variance $E[X^2] - E[X]^2$. These numbers are the basic summary statistics of $X$, and the MGF hands them all over through a single mechanical operation — differentiation.

The key identity is the **power-series expansion** of the exponential. For any number $u$,

$$ e^{u} = 1 + u + \frac{u^2}{2!} + \frac{u^3}{3!} + \cdots, $$

where $k! = 1\cdot 2 \cdots k$ is the factorial. Substituting $u = tX$ turns this into a series in the random variable $X$:

$$ e^{tX} = 1 + tX + \frac{t^2 X^2}{2!} + \frac{t^3 X^3}{3!} + \cdots. $$

Now take the [[expectation]] of both sides. Expectation is linear — it passes through sums and pulls out constants — and $t$ is a constant with respect to the averaging, so the powers of $t$ come out front and each random power $X^k$ becomes its moment $E[X^k]$:

$$ M_X(t) = E\!\left[e^{tX}\right] = 1 + E[X]\,t + \frac{E[X^2]}{2!}\,t^2 + \frac{E[X^3]}{3!}\,t^3 + \cdots. $$

This is the heart of the matter: **the moments sit inside the MGF as the coefficients of its power series**. The MGF is just a bookkeeping device that lines the moments up along increasing powers of $t$.

To extract one cleanly, differentiate with respect to $t$ and then evaluate at $t=0$ — the maneuver that gives the function its name. Differentiating the series once,

$$ M_X'(t) = E[X] + E[X^2]\,t + \frac{E[X^3]}{2!}\,t^2 + \cdots, $$

and setting $t=0$ kills every term that still carries a factor of $t$, leaving only the constant:

$$ M_X'(0) = E[X]. $$

The first derivative at the origin *is* the mean. Differentiate a second time and again set $t=0$: the same cancellation leaves $M_X''(0) = E[X^2]$, the second moment. In general the $k$-th derivative at zero, $M_X^{(k)}(0)$, equals the $k$-th moment $E[X^k]$, because differentiating $k$ times and evaluating at $0$ selects exactly the coefficient of $t^k$ (with its $k!$ from the factorial cancelled by the $k!$ that differentiation brings down). One function, differentiated repeatedly at a single point, dispenses the whole sequence of moments — that is why it *generates* them.

### A worked normal MGF — completing the square

Take $X$ a normal variable $N(\mu, \sigma^2)$: a continuous variable whose density (the bell curve) is

$$ f(x) = \frac{1}{\sigma\sqrt{2\pi}}\,\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right), $$

with $\mu$ its center and $\sigma^2$ its spread (so $\sigma$, the standard deviation, sets the width). To get its MGF we average $e^{tx}$ against this density (LOTUS, the transform-averaging rule from [[expectation]]):

$$ M_X(t) = E\!\left[e^{tX}\right] = \int_{-\infty}^{\infty} e^{tx}\,\frac{1}{\sigma\sqrt{2\pi}}\,\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right) dx, $$

where $\int_{-\infty}^{\infty}\cdots dx$ sums the contribution of every value of $x$ along the whole line. The integrand multiplies two exponentials, so add their exponents:

$$ tx - \frac{(x-\mu)^2}{2\sigma^2}. $$

This is a quadratic in $x$, and the **non-obvious step** is *completing the square* — rewriting the quadratic as a perfect square plus a leftover that does not involve $x$. Expand and regroup:

$$ tx - \frac{(x-\mu)^2}{2\sigma^2} = -\frac{1}{2\sigma^2}\Big[(x-\mu)^2 - 2\sigma^2 t\,x\Big]. $$

Inside the brackets, force a perfect square by absorbing the linear term into the squared term. The value that completes $(x-\mu)^2 - 2\sigma^2 t\,x$ into a square is $\big(x - (\mu + \sigma^2 t)\big)^2$; matching the two and tracking what is left over gives

$$ tx - \frac{(x-\mu)^2}{2\sigma^2} = -\frac{\big(x - (\mu + \sigma^2 t)\big)^2}{2\sigma^2} + \Big(\mu t + \tfrac{1}{2}\sigma^2 t^2\Big). $$

(You can verify the bracketed leftover $\mu t + \tfrac12\sigma^2 t^2$ by expanding the right side back out — the $x^2$, $x$, and constant terms agree.) The point of the maneuver is that the first piece is *again* a normal density's exponent, only re-centered from $\mu$ to $\mu + \sigma^2 t$. So when we put it back under the integral, that piece integrates to exactly $1$ (every normal density encloses total area $1$, regardless of where it is centered), and the leftover — having no $x$ in it — slides outside the integral as a constant factor:

$$ M_X(t) = \exp\!\Big(\mu t + \tfrac{1}{2}\sigma^2 t^2\Big)\underbrace{\int_{-\infty}^{\infty}\frac{1}{\sigma\sqrt{2\pi}}\exp\!\left(-\frac{\big(x-(\mu+\sigma^2 t)\big)^2}{2\sigma^2}\right)dx}_{=\,1} = \exp\!\Big(\mu t + \tfrac{1}{2}\sigma^2 t^2\Big). $$

So the normal MGF is $M_X(t) = \exp(\mu t + \tfrac{1}{2}\sigma^2 t^2)$.

**Sanity check against the generating property.** Differentiate: $M_X'(t) = (\mu + \sigma^2 t)\exp(\mu t + \tfrac12\sigma^2 t^2)$. At $t=0$ the exponential is $1$ and the front factor is $\mu$, so $M_X'(0) = \mu$. The derivative at the origin recovers the mean $E[X]=\mu$, exactly as the generating property promised — a live confirmation that the function we built is doing its job.

### The payoff — the log-normal mean

Here is why this matters in the source's running problem. Suppose $Y \sim N(\mu, \sigma^2)$ and we form the new variable $e^Y$ — a *log-normal* variable (so named because its logarithm, $Y$, is normal). It takes only positive values and is right-skewed. We want its mean, $E[e^Y]$.

The temptation is to push the exponential inside and write $e^{E[Y]} = e^{\mu}$ — but [[expectation]] warns that $E[g(Y)] \neq g(E[Y])$ for a nonlinear $g$, and $\exp$ is nonlinear, so that is wrong. The mean is genuinely an integral, $E[e^Y] = \int e^{y} f(y)\,dy$. The MGF makes the integral free: $E[e^Y]$ is precisely $E[e^{tY}]$ read at $t = 1$, i.e. the normal MGF evaluated at $t=1$:

$$ E\!\left[e^{Y}\right] = M_Y(1) = \exp\!\Big(\mu\cdot 1 + \tfrac{1}{2}\sigma^2\cdot 1^2\Big) = e^{\mu + \sigma^2/2}. $$

Put concrete numbers to it. Let $\mu = 0$ and $\sigma^2 = 1$ (a standard normal $Y$). Then the log-normal mean is $e^{0 + 1/2} = e^{1/2} \approx 1.6487$. Note this is strictly larger than the wrong answer $e^{\mu} = e^{0} = 1$: the gap factor $e^{\sigma^2/2} = e^{1/2}$ is exactly the correction the MGF supplies, and it is what records the rightward pull of the log-normal's tail. The whole calculation reduced to plugging $t=1$, $\mu=0$, $\sigma^2=1$ into one closed-form function — which is the practical reason to carry the MGF around.

### Pulling it together

The moment generating function is one object, $M_X(t) = E[e^{tX}]$, doing three jobs at once. As a **structure** it is a transform-averaged [[expectation]] indexed by a free knob $t$. As an **algorithm** it dispenses moments: differentiate $k$ times, set $t=0$, read off $E[X^k]$ — the mean falling out of the first derivative, the second moment from the second. And as a **closed form** for specific distributions (here the normal, via completing the square) it turns otherwise-hard expectation integrals into one evaluation — the log-normal mean $e^{\mu+\sigma^2/2}$ being nothing more than the normal MGF at $t=1$.

## Prerequisites

- [[expectation]]
- [[random-variable]]

## Sources

- `study-notes.html` §5.4 — "Summary statistics — three statistics, three derivations" (normal MGF $M_Y(t)=e^{\mu t + \sigma^2 t^2/2}$ by completing the square; log-normal mean as $M_Y(1)=e^{\mu+\sigma^2/2}$).
