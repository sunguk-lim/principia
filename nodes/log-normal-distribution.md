---
id: log-normal-distribution
title: Log-Normal Distribution
summary: "A positive random quantity $X$ is log-normal when its logarithm is normal: $Y = \\ln X$ follows a normal-distribution with mean $\\mu$ and standard deviation $\\sigma$, or…"
type: concept
tags: [math/probability]
prereqs: [change-of-variables, normal-distribution, expectation, convexity, moment-generating-function, skewness, exponential-function, moment-skewness]
sources: [study-notes.html §5.2, study-notes.html §5.3, study-notes.html §5.4, study-notes.html §5.5]
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# Log-Normal Distribution

## Summary

A positive random quantity $X$ is **log-normal** when its logarithm is normal: $Y = \ln X$ follows a [[normal-distribution]] with mean $\mu$ and standard deviation $\sigma$, or equivalently $X = e^{Y}$ is a [[normal-distribution]] passed through the exponential. It is the natural model for things that are *multiplicatively* random — prices, incomes, particle sizes, biological growth — because multiplying many small independent factors is the same as *adding* their logs, and sums of many small additive effects go normal. Its density is obtained by [[change-of-variables]] on the map $g(x) = \ln x$, whose stretch factor is $|g'(x)| = 1/x$; that $1/x$ Jacobian is the fingerprint of the log transform and is what makes the distribution live only on $x > 0$ and lean to the right. The signature lesson is that its three "typical value" summaries land at three *different* places, each reached by its own route: the **median** $e^{\mu}$ (quantiles ride straight through the monotonic log), the **mode** $e^{\mu - \sigma^2}$ (maximize the density — the Jacobian's $-\ln x$ term drags the peak left), and the **mean** $e^{\mu + \sigma^2/2}$, which is exactly the normal's [[moment-generating-function]] read off at $t=1$: $E[X] = E[e^Y] = M_Y(1) = e^{\mu+\sigma^2/2}$. The spread $\sigma^2$ fans those three apart, which is precisely the **right [[skewness]]** the log-normal is famous for; and because $X = e^Y$ is a *convex increasing transform of a symmetric* normal, the convex-transformation-order guarantees that the right-skew order $\text{mode} < \text{median} < \text{mean}$ can **never scramble** — the [[convexity]] of $\exp$ being the structural cause.

## Grounded explanation

This node is the capstone of a small theory: it pulls together change of variables, the normal, expectation, the moment generating function, convexity, skewness, and the convex transformation order into one running example. Each of the three "centers" of the log-normal is reached by a *different* prerequisite, and the ordering between them is *explained twice over* — once by computing the numbers, once by structure.

### What the concept *is*

Start with a quantity whose logarithm behaves normally. Let $Y$ be a [[normal-distribution]] with mean $\mu$ (Greek "mu," the center) and standard deviation $\sigma > 0$ (the spread), written $Y \sim N(\mu, \sigma^2)$, where $\sigma^2$ is the variance. From the [[normal-distribution]] prerequisite its density is

$$ f_Y(y) = \frac{1}{\sigma\sqrt{2\pi}}\,\exp\!\left(-\frac{(y-\mu)^2}{2\sigma^2}\right), \qquad y \in (-\infty, \infty), $$

where $\exp(\cdot) = e^{(\cdot)}$ is the exponential function and $\sqrt{2\pi} \approx 2.5066$.

Now define a new variable by exponentiating:

$$ X = e^{Y}, \qquad \text{equivalently} \qquad Y = \ln X. $$

$X$ is called **log-normal** precisely because *its log is normal*. The name describes the relationship, not $X$ itself: it is the variable whose logarithm is the normal one. Because $e^{(\cdot)}$ — the [[exponential-function]] — is always strictly positive, $X$ ranges only over the positive reals $x > 0$, no matter how negative $Y$ gets. The concept of this node is the density of $X$ and — the real teaching — the three different "center" statistics it produces, why they disagree, and why they disagree *in a fixed order that can never invert*.

Why care? The [[normal-distribution]] arises when many small *additive* effects pile up (its Central Limit motivation). But many real quantities are built *multiplicatively*: a stock that gains 3% then loses 1% then gains 2% has its factors *multiplied*, $1.03 \times 0.99 \times 1.02$. Taking logs turns that product into a *sum* of small terms, $\ln 1.03 + \ln 0.99 + \ln 1.02$ — and a sum of many small independent terms is normal. So the *log* of the quantity is normal, which is exactly the definition of log-normal. This is why prices, incomes, file sizes, and organism sizes are so often modeled this way.

### The density, via change of variables

We know $f_Y$ (it is normal) and want $f_X$, the density of $X = e^Y$. This is exactly the setting of [[change-of-variables]]: a variable with a known density passed through a function. That prerequisite's master relation, for a strictly monotonic differentiable map, is

$$ f_{\text{known}}(\text{old}) = f_{\text{new}}\!\big(g(\text{old})\big)\,\big|g'(\text{old})\big|. $$

Apply it with the *log* as the transforming map: let $g$ send $x \mapsto \ln x$, so $g(X) = \ln X = Y$. Then $X$ is the variable whose density we seek and $Y$ (the normal) is the one we know. Plugging in,

$$ f_X(x) = f_Y\!\big(g(x)\big)\,\big|g'(x)\big| = f_Y(\ln x)\,\big|g'(x)\big|. $$

We need two pieces. First, the stretch factor: $g(x) = \ln x$ has derivative $g'(x) = 1/x$, so for $x > 0$,

$$ \big|g'(x)\big| = \frac{1}{x}. $$

This is the **Jacobian fingerprint** of the log transform — a $1/x$ out front, present in every log-normal density and in nothing else. Second, $f_Y$ evaluated at the inner value $\ln x$: substitute $y = \ln x$ into the normal density. Together,

$$ \boxed{\,f_X(x) = \frac{1}{x\,\sigma\sqrt{2\pi}}\,\exp\!\left(-\frac{(\ln x - \mu)^2}{2\sigma^2}\right), \qquad x > 0\,} $$

and $f_X(x) = 0$ for $x \le 0$ (no value of $Y$ maps there, since $e^Y$ is always positive). The map $g(x) = \ln x$ is strictly increasing and differentiable on $x > 0$, so [[change-of-variables]] applies cleanly — it is one-to-one, with no doubling back.

No probability is lost by living only on $x > 0$. The map $x = e^y$ is a *bijection* between the whole real line (the support of $Y$) and the positive half-line (the support of $X$): the negative half of the normal is not discarded but *relocated*, with $y \in (-\infty,0)$ landing in $x \in (0,1)$, $y=0$ at $x=1$, and $y \in (0,\infty)$ in $x \in (1,\infty)$. The point $x=0$ corresponds to $y = -\infty$, never attained; a single point carries zero probability, so excluding $x \le 0$ removes nothing. (The $1/x$ Jacobian is exactly the substitution factor $dy = dx/x$ that makes $\int_0^\infty f_X(x)\,dx = \int_{-\infty}^\infty f_Y(y)\,dy = 1$ automatic.)

Read the formula. The exponential kernel is a *bell in $\ln x$*: it is largest when $\ln x = \mu$ and dies as $\ln x$ departs from $\mu$ in either direction. But the kernel is multiplied by $1/x$, which is *not* symmetric in $x$ — it is large for small $x$ and small for large $x$. That asymmetric $1/x$ is what skews the whole picture to the right and forces the three center-statistics apart, which we now compute.

### Three centers, three routes

The three "centers" are exactly the trio that [[skewness]] compares to read off a distribution's asymmetry: the **mode** (the density peak), the **median** (the value with half the probability on each side), and the **mean** (the [[expectation]], the value-weighted balance point). A symmetric distribution like the [[normal-distribution]] stacks all three at the same point $\mu$. The log-normal breaks that coincidence — and the general lesson of the source is that *each statistic transforms by its own rule*, because each is a different **kind** of statistic.

**(1) Median — quantiles ride through the monotonic map (order-based).** The **median** $m$ is the value with half the probability below it: $P(X \le m) = 1/2$. The map $x \mapsto \ln x$ is strictly increasing, so it *preserves order*: $X \le m$ happens in exactly the same outcomes as $\ln X \le \ln m$, i.e. $Y \le \ln m$. Therefore $P(X \le m) = P(Y \le \ln m)$. Setting this to $1/2$ means $\ln m$ is the median of $Y$. But $Y$ is normal, hence symmetric about $\mu$, so *its* median is its center $\mu$. Thus $\ln m = \mu$, giving

$$ m = e^{\mu}. $$

This route used **no Jacobian at all** — quantiles are *order-based*, so they pass straight through the increasing map: the general rule is $\text{median}(X) = g^{-1}(\text{median}(Y))$, here $\text{median}(X) = e^{\text{median}(Y)}$.

**(2) Mode — maximize the density (density-based; the Jacobian drags the peak left).** The **mode** is the location of the density's peak, the $x > 0$ maximizing $f_X(x)$. Maximizing $f_X$ is the same as maximizing its logarithm (a monotonic move that simplifies the algebra):

$$ \ln f_X(x) = -\ln x - \frac{(\ln x - \mu)^2}{2\sigma^2} + \text{const}, $$

where the constant collects the $-\ln(\sigma\sqrt{2\pi})$ term. Two pieces depend on $x$: the $-\ln x$ comes straight from the $1/x$ **Jacobian**, and the $-(\ln x - \mu)^2/(2\sigma^2)$ comes from the normal kernel. Set the derivative in $x$ to zero, using $\frac{d}{dx}\ln x = 1/x$:

$$ \frac{d}{dx}\ln f_X(x) = -\frac{1}{x} - \frac{\ln x - \mu}{\sigma^2 x} = -\frac{1}{x}\left(1 + \frac{\ln x - \mu}{\sigma^2}\right) = 0. $$

Since $1/x \ne 0$, the bracket must vanish: $1 + (\ln x - \mu)/\sigma^2 = 0$, so $\ln x - \mu = -\sigma^2$, i.e. $\ln x = \mu - \sigma^2$. Therefore

$$ \text{mode} = e^{\mu - \sigma^2}. $$

Here is the lesson made precise: *without* the Jacobian, the density would peak where the normal kernel peaks, at $\ln x = \mu$ (giving $e^\mu$); the extra $-\ln x$ from the $1/x$ contributes the standalone $-1/x$ in the derivative, which is what pushes the solution to $\ln x = \mu - \sigma^2$. The Jacobian **drags the peak left** by exactly $\sigma^2$ in log-space. So the mode sits *below* the median $e^\mu$. The mode is a density-based statistic — it cannot ignore the Jacobian the way the order-based median did.

**(3) Mean — an expectation of $e^Y$, evaluated as the normal's MGF at $t=1$ (expectation-based).** The **mean** is $E[X]$, the [[expectation]] (probability-weighted average / balance point). Since $X = e^Y$, we want $E[e^Y]$. The tempting shortcut $e^{E[Y]} = e^{\mu}$ is *wrong* — [[expectation]] warns that $E[g(Y)] \ne g(E[Y])$ for a nonlinear $g$, and $\exp$ is nonlinear. By the law of the unconscious statistician, the honest value is the integral

$$ E[X] = E[e^Y] = \int_{-\infty}^{\infty} e^{y}\, f_Y(y)\, dy = \int_{-\infty}^{\infty} e^{y}\,\frac{1}{\sigma\sqrt{2\pi}}\,\exp\!\left(-\frac{(y-\mu)^2}{2\sigma^2}\right) dy. $$

This integral is *already solved* by a prerequisite. The [[moment-generating-function]] of $Y$ is $M_Y(t) = E[e^{tY}]$, and for a [[normal-distribution]] the MGF node derives — by completing the square inside exactly this integral — the closed form

$$ M_Y(t) = \exp\!\Big(\mu t + \tfrac{1}{2}\sigma^2 t^2\Big). $$

Our integral $E[e^Y]$ is precisely $E[e^{tY}]$ read off at $t = 1$. So no fresh integration is needed; just substitute $t = 1$:

$$ \boxed{\,E[X] = E[e^Y] = M_Y(1) = \exp\!\Big(\mu\cdot 1 + \tfrac{1}{2}\sigma^2\cdot 1^2\Big) = e^{\mu + \sigma^2/2}\,} $$

The mean carries an extra $+\sigma^2/2$ in the exponent beyond the median's $\mu$, so it sits *above* the median. (The same MGF tool, differentiated, yields the variance $\mathrm{Var}(X) = E[X^2] - E[X]^2 = (e^{\sigma^2}-1)\,e^{2\mu+\sigma^2}$ — but the mean is the part we lean on here.) This is the synthesis hinge of the node: the log-normal mean is *nothing but the normal MGF at $t=1$*, which is *why* it carries the gap factor $e^{\sigma^2/2}$ over the median.

### Why the ordering is right-skew — and why it can never scramble

Collect the three results:

$$ \text{mode} = e^{\mu-\sigma^2}, \qquad \text{median} = e^{\mu}, \qquad \text{mean} = e^{\mu+\sigma^2/2}. $$

Because $e^{(\cdot)}$ is increasing and $\mu - \sigma^2 < \mu < \mu + \sigma^2/2$ (using $\sigma^2 > 0$), exponentiating preserves the order:

$$ \text{mode} < \text{median} < \text{mean}. $$

This is the **right-[[skewness]]** signature exactly. From the [[skewness]] prerequisite, the order $\text{mode} < \text{median} < \text{mean}$ is the generic fingerprint of a long *right* tail, and the intuition is **tail sensitivity**: the mean integrates value against probability, so a long right tail of large values drags it farthest; the median (only the 50% point) moves less; the mode (a local peak feature) does not move at all. The single spread parameter $\sigma^2$ is what fans the three apart; as $\sigma \to 0$ the distribution collapses to a spike and the three coincide.

But [[skewness]] is careful to call that ordering a *rule of thumb*, not a theorem — under the weak measures of skew (the third moment ([[moment-skewness]]), or the nonparametric gap $(\text{mean}-\text{median})/\sigma$) the mode is unreliable and the order *can* scramble for multimodal or certain discrete distributions. The log-normal is special: its order is **strict and never scrambles**, and the deepest reason is structural, supplied by the convex-transformation-order.

**The mean-above-median half, by [[convexity]].** First the local mechanism. The exponential $\exp$ is **convex** — its second derivative $\frac{d^2}{dy^2}e^y = e^y > 0$ everywhere, the bowl shape from [[convexity]]. **Jensen's inequality** for a convex function says $g(E[Y]) \le E[g(Y)]$ — "the function of the average is at most the average of the function." With $g = \exp$ and $E[Y] = \mu$ for the normal $Y$:

$$ \underbrace{e^{E[Y]}}_{=\,e^{\mu}\,=\,\text{median}} = e^{\mu} \;\le\; \underbrace{E[e^{Y}]}_{=\,e^{\mu+\sigma^2/2}\,=\,\text{mean}}, $$

strictly so because $\exp$ is *strictly* convex and $Y$ is genuinely spread out. So **mean $\ge$ median**, the gap factor being $e^{\sigma^2/2} \ge 1$. This is the convexity-supplied direction of the same $E[g(X)] \ne g(E[X])$ warning carried over from [[expectation]].

**Why the *whole* order is locked, by the convex-transformation-order.** The reason the log-normal's order can never invert is the strong, structural notion of skew from the convex-transformation-order prerequisite. A distribution is right-skewed *in van Zwet's strong sense* exactly when it is a **convex, increasing transformation of a symmetric distribution**. The log-normal is the textbook instance: $Y$ is the symmetric normal, and the *constructing* map is $g(y) = e^y$ — increasing, and **convex** by the [[convexity]] fact above. So $X = e^Y$ is *certified* strongly right-skewed: the curvature of $\exp$ stretches the upper tail and compresses the lower one, manufacturing the right tail out of the symmetric base. By the **Groeneveld–Meeden** guarantee — strong right-skew order *plus* unimodality (the log-normal has one peak) — the ordering $\text{mode} \le \text{median} \le \text{mean}$ is *guaranteed*, never able to scramble for any $\sigma > 0$.

A standing caution from that prerequisite, worth repeating because it is easy to invert: the map that must be convex is the one *building* $X$ from the symmetric base — here $\exp$, which is convex. It is tempting to cite "the logarithm is concave," but $\log$ runs the *other* way, mapping $X$ back to the symmetric $Y$; its concavity merely *confirms* that a concave map symmetrizes a right-skewed variable. Always test the *constructing* map for [[convexity]], never its inverse.

A second, numerical confirmation that the log-normal never scrambles: its **moment skewness** (the third standardized moment, a single signed number) is

$$ \gamma = (e^{\sigma^2} + 2)\sqrt{e^{\sigma^2} - 1} \; > \; 0 \quad \text{for every } \sigma > 0, $$

and it *grows* with $\sigma$ — the same parameter that fans the three centers apart. Positive moment skewness, the structural convex-order guarantee, and the computed $e^{\mu-\sigma^2} < e^{\mu} < e^{\mu+\sigma^2/2}$ all agree: the log-normal is unambiguously, permanently right-skewed.

### Worked instance — the standard log-normal, $\mu = 0$, $\sigma = 1$

Take $Y \sim N(0, 1)$ (the standard normal), so $X = e^Y$ is the standard log-normal. This is non-degenerate: $\sigma = 1 \ne 0$, so the three centers genuinely separate (if $\sigma$ were $0$, all three would collapse to $e^\mu$ and the lesson would vanish). Compute each by its own route.

- **Median** $= e^{\mu} = e^{0} = 1$ (order-based — straight through the map). Half of $X$'s probability lies below $1$, which makes sense, since $Y = \ln X$ is below its median $0$ exactly when $X < 1$.
- **Mode** $= e^{\mu - \sigma^2} = e^{0 - 1} = e^{-1} \approx 0.368$ (density-based — Jacobian drags it left). The peak of the density sits well left of the median, dragged there by the $\sigma^2 = 1$ shift the Jacobian forces.
- **Mean** $= e^{\mu + \sigma^2/2} = e^{0 + 1/2} = e^{1/2} \approx 1.649$ (expectation-based — the MGF $M_Y(1)$). Concretely, $M_Y(1) = e^{0\cdot 1 + \frac12 \cdot 1 \cdot 1^2} = e^{1/2}$. The balance point sits to the *right* of the median, pulled out by the convex exponential.

Putting the three numbers on the line:

$$ \underbrace{0.368}_{\text{mode}} \;<\; \underbrace{1}_{\text{median}} \;<\; \underbrace{1.649}_{\text{mean}} \qquad (\text{mode} < \text{median} < \text{mean}), $$

a clear right skew. (Numerically: $e^{-1} = 1/e \approx 1/2.71828 \approx 0.3679$, and $e^{1/2} = \sqrt{e} \approx \sqrt{2.71828} \approx 1.6487$.) Check the Jensen gap directly: median $= e^{E[Y]} = e^0 = 1$, mean $= E[e^Y] \approx 1.6487$, and indeed $1 \le 1.6487$ — the convexity bulge is the $0.6487$ excess of mean over median, exactly the gap factor $e^{\sigma^2/2} = e^{1/2}$.

The moment skewness here is $\gamma = (e^{1} + 2)\sqrt{e^{1} - 1} = (2.71828 + 2)\sqrt{1.71828} \approx 4.718 \times 1.311 \approx 6.18 > 0$ — strongly positive, confirming the right skew with a single number. And by the convex-transformation-order, because $X = e^Y$ is a convex increasing transform of the symmetric $N(0,1)$ and is unimodal, this $0.368 < 1 < 1.649$ ordering is *proven unscramblable*, not merely observed.

We can also read the density's value to confirm the mode is a peak. With $\mu=0,\sigma=1$, $f_X(x) = \frac{1}{x\sqrt{2\pi}}\exp(-\tfrac12(\ln x)^2)$. At the mode $x = e^{-1}\approx 0.3679$: $\ln x = -1$, so $f_X = \frac{1}{0.3679 \times 2.5066}\exp(-\tfrac12) = \frac{1}{0.9222}\times 0.6065 \approx 1.0846 \times 0.6065 \approx 0.658$. At the median $x = 1$: $\ln x = 0$, so $f_X = \frac{1}{1 \times 2.5066}\times e^0 \approx 0.399$. The density is indeed higher at the mode ($0.658$) than at the median ($0.399$) — the peak really is to the left, exactly as the Jacobian-shifted mode predicted.

### Pulling it together

$X$ is **log-normal** when $\ln X$ is a [[normal-distribution]] $N(\mu,\sigma^2)$, equivalently $X = e^Y$. Passing the normal density through the increasing map $\ln$ via [[change-of-variables]] yields $f_X(x) = \frac{1}{x\sigma\sqrt{2\pi}}\exp(-(\ln x-\mu)^2/(2\sigma^2))$ on $x>0$, the $1/x$ Jacobian being the log transform's fingerprint and the source of the asymmetry. The three centers — the same trio [[skewness]] compares — are reached by three *kinds* of route: the order-based **median** $e^\mu$ (quantile straight through the monotonic map, no Jacobian); the density-based **mode** $e^{\mu-\sigma^2}$ (maximize the density, the Jacobian's $-\ln x$ dragging the peak left by $\sigma^2$); and the expectation-based **mean** $e^{\mu+\sigma^2/2}$, which is exactly the normal [[moment-generating-function]] $M_Y(t)$ at $t=1$. [[convexity]] of $\exp$ via Jensen forces mean $\ge$ median, giving right [[skewness]]; and the convex-transformation-order — $X=e^Y$ as a convex increasing transform of a symmetric normal, unimodal — upgrades that from a rule of thumb to a Groeneveld–Meeden *guarantee* that $\text{mode} < \text{median} < \text{mean}$ can never scramble. For $\mu=0,\sigma=1$ it reads $0.368 < 1 < 1.649$, with moment skewness $\gamma \approx 6.18 > 0$.

## Prerequisites

- [[change-of-variables]]
- [[normal-distribution]]
- [[expectation]]
- [[convexity]]
- [[moment-generating-function]]
- [[skewness]]
## Sources

- `study-notes.html` §5.2 — "The log-normal density" (density via change of variables, the $1/x$ Jacobian fingerprint).
- `study-notes.html` §5.3 — "Why restricting to $x>0$ preserves all the mass" ($x=e^y$ bijection, mass relocated not lost).
- `study-notes.html` §5.4 — "Summary statistics — three statistics, three derivations" (median $e^\mu$ by pushing the quantile through $g$; mode $e^{\mu-\sigma^2}$ by maximizing the density; mean $e^{\mu+\sigma^2/2}$ as the normal MGF $M_Y(1)$; the convexity/Jensen ordering).
- `study-notes.html` §5.5 — "Skewness: how general is mode < median < mean?" (tail-sensitivity rule of thumb; moment skewness $\gamma=(e^{\sigma^2}+2)\sqrt{e^{\sigma^2}-1}>0$; van Zwet convex transformation order and the Groeneveld–Meeden guarantee).
