---
id: conjugate-prior
title: Conjugate Prior
summary: A conjugate prior is a prior distribution chosen so that, after the bayes-rule update, the posterior lands in the same family of distributions as the prior — only its parameters…
type: concept
tags: [math/probability]
prereqs: [bayes-rule, beta-distribution, bernoulli-distribution, likelihood]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Conjugate Prior

## Summary

A **conjugate prior** is a prior distribution chosen so that, after the [[bayes-rule]] update, the **posterior lands in the same family of distributions as the prior** — only its parameters have changed. When this happens, Bayesian updating stops being a calculus problem and becomes simple **bookkeeping**: you read the new parameters off the old ones plus the data, never touching the hard normalizing integral that [[bayes-rule]] hides in its denominator. The flagship example is **Beta–Bernoulli**: take a [[beta-distribution]] prior over an unknown success-probability $p$, whose density has the core $p^{\alpha-1}(1-p)^{\beta-1}$, and observe coin-like data with a [[bernoulli-distribution]] (or binomial) likelihood of the form $p^{h}(1-p)^{t}$ — $h$ successes, $t$ failures. Because both pieces are powers of the *same* two factors $p$ and $(1-p)$, multiplying them (which is exactly what `posterior ∝ likelihood × prior` says) just **adds the exponents**: the posterior core is $p^{\alpha+h-1}(1-p)^{\beta+t-1}$, which is again a Beta — namely $\mathrm{Beta}(\alpha+h,\ \beta+t)$. So updating reduces to "**add the observed successes to $\alpha$ and the observed failures to $\beta$**." This closure also makes learning **sequential**: today's posterior is tomorrow's prior, counts simply accumulate, and an online learner needs to store only the running pair $(\alpha,\beta)$.

## Grounded explanation

### What the concept *is*

Recall the inference setup from [[bayes-rule]]. We have an unknown quantity $\theta$ we want to learn, a **prior** $P(\theta)$ encoding belief before data, a **[[likelihood]]** $P(D\mid\theta)$ saying how probable the observed data $D$ is for each candidate $\theta$, and the **posterior** $P(\theta\mid D)$ — the updated belief — given by

> $P(\theta\mid D) = \dfrac{P(D\mid\theta)\,P(\theta)}{P(D)}, \qquad\text{i.e.}\qquad P(\theta\mid D)\ \propto\ P(D\mid\theta)\,P(\theta),$

where $\propto$ means "proportional to" and the denominator $P(D)$ — the **evidence** — is the fixed number that rescales the posterior so it integrates to 1. For a continuous $\theta$, [[bayes-rule]] tells us that number is itself an integral, $P(D) = \int P(D\mid\theta)\,P(\theta)\,d\theta$. That integral is the expensive part: for an arbitrary prior shape there may be no closed form for it at all.

A **conjugate prior** is a deliberate choice that sidesteps this. Fix a likelihood family (here, coin-like trials). A prior family is called **conjugate** to that likelihood if, whenever the prior is a member of the family, the posterior is *also* a member of the same family — with new parameter values. Symbolically, if the prior is "family $\mathcal{F}$ with parameters $\boldsymbol{\eta}$," then after seeing data $D$ the posterior is "family $\mathcal{F}$ with parameters $\boldsymbol{\eta}'$," where $\boldsymbol{\eta}'$ depends only on $\boldsymbol{\eta}$ and $D$ through a simple rule. The family is said to be **closed under the Bayesian update**.

That closure is the whole point, and it buys two things:

1. **The hard integral becomes free.** If we already know the posterior is, say, a [[beta-distribution]], then its normalizing constant is a *known function of its parameters* — we recognize the shape and write down the constant, instead of computing $P(D)$ from scratch.
2. **Updating becomes arithmetic on the parameters.** Learning from data is reduced to mapping $\boldsymbol{\eta} \to \boldsymbol{\eta}'$, a few additions, rather than a fresh integration each time.

The concept here is *not* "the Beta distribution" or "Bayes' rule" — those are the ingredients. The concept is the **structural match between a prior family and a likelihood family that makes the posterior stay in the family**, and the consequence that update = parameter bookkeeping.

### The flagship: Beta is conjugate to Bernoulli/binomial

Let the unknown be a success-probability: $\theta = p$, the chance of "success" (heads) on a single two-outcome trial. So $p$ is a number in $(0,1)$, and our belief about it is a distribution *over a probability* — exactly what a [[beta-distribution]] expresses. Take the prior to be

> $P(p) \ \propto\ p^{\,\alpha-1}(1-p)^{\,\beta-1}, \qquad p\sim\mathrm{Beta}(\alpha,\beta),$

with shape parameters $\alpha>0,\ \beta>0$. From [[beta-distribution]], the part shown is the **core** that carries all the shape; the omitted constant $1/B(\alpha,\beta)$ only fixes the area to 1. The pseudo-count reading from [[beta-distribution]] will matter: $\alpha$ behaves like a tally of prior "successes," $\beta$ like prior "failures."

Now the data. Suppose we run coin-like trials and record $h$ **successes** (heads) and $t$ **failures** (tails). From [[bernoulli-distribution]], a single trial has likelihood $p^{x}(1-p)^{1-x}$ (which prints $p$ for a success $x{=}1$ and $1-p$ for a failure $x{=}0$); and for $n=h+t$ **independent** trials, the probability of one specific success/failure sequence is the product of the per-trial factors,

> $P(D\mid p) \ =\ p^{\,h}\,(1-p)^{\,t}.$

(If instead we only recorded the *count* $h$ out of $n$, the binomial pmf from [[bernoulli-distribution]] multiplies this by a $\binom{n}{h}$ factor — but $\binom{n}{h}$ does not depend on $p$, so it is just another constant that the $\propto$ in [[bayes-rule]] discards. Either way the *$p$-dependent shape* of the likelihood is $p^{h}(1-p)^{t}$.)

### The justifying identity: exponents add because the bases match

Apply `posterior ∝ likelihood × prior` from [[bayes-rule]], substituting the two shapes above:

$$
P(p\mid D)\ \propto\ \underbrace{p^{\,h}(1-p)^{\,t}}_{\text{likelihood}}\ \times\ \underbrace{p^{\,\alpha-1}(1-p)^{\,\beta-1}}_{\text{prior}}.
$$

Both factors are powers of the *same two bases*, $p$ and $(1-p)$. Multiplying powers of a common base adds the exponents ($p^{a}\cdot p^{b}=p^{a+b}$), so group the $p$'s together and the $(1-p)$'s together:

$$
P(p\mid D)\ \propto\ p^{\,h + (\alpha-1)}\,(1-p)^{\,t + (\beta-1)}\ =\ p^{\,(\alpha+h)-1}\,(1-p)^{\,(\beta+t)-1}.
$$

Look at the right-hand side: it is *exactly* the Beta core from [[beta-distribution]], $p^{\alpha'-1}(1-p)^{\beta'-1}$, with new parameters

> $\boxed{\ \alpha' = \alpha + h, \qquad \beta' = \beta + t.\ }$

So the posterior is $\mathrm{Beta}(\alpha+h,\ \beta+t)$ — **a Beta again.** This single line *is* conjugacy for this pair. The "magic-looking" step — that the posterior happens to be the same kind of object as the prior — is no coincidence: it is forced by the algebraic match between the Beta core $p^{\alpha-1}(1-p)^{\beta-1}$ and the likelihood $p^{h}(1-p)^{t}$, which [[beta-distribution]] flagged as "the same shape" up front. Because they are the same shape, their product is too.

### Why the hard integral disappears

Notice what we never had to compute. [[bayes-rule]] said the true posterior is the product *divided by* the evidence $P(D)=\int_0^1 p^{h}(1-p)^{t}\cdot \tfrac{1}{B(\alpha,\beta)}p^{\alpha-1}(1-p)^{\beta-1}\,dp$ — an integral. But we *recognized* the product's shape as a Beta core with parameters $(\alpha+h,\ \beta+t)$, and [[beta-distribution]] tells us the constant that normalizes that core to area 1 is, by definition, $1/B(\alpha+h,\ \beta+t)$. So

$$
P(p\mid D)\ =\ \frac{1}{B(\alpha+h,\ \beta+t)}\;p^{\,(\alpha+h)-1}(1-p)^{\,(\beta+t)-1}.
$$

We obtained the normalizer **for free, by pattern-matching the family**, instead of evaluating $P(D)$. (In fact, comparing the two expressions shows $P(D)=B(\alpha+h,\beta+t)/B(\alpha,\beta)$ — the evidence integral is handed to us as a ratio of known Beta-function constants, with no integration done.) This is the practical payoff of conjugacy: the one genuinely hard quantity that [[bayes-rule]] hides in its denominator is supplied by the family itself.

The update rule is now memorable in plain English, and it matches the pseudo-count intuition from [[beta-distribution]] perfectly: **add observed successes $h$ to the success-pseudo-count $\alpha$, and observed failures $t$ to the failure-pseudo-count $\beta$.** Real data counts pile onto the imagined prior counts.

### Worked instance — one batch

Start with the prior $\mathrm{Beta}(2,2)$: from [[beta-distribution]], a gentle symmetric bump centered at $p=0.5$ — "probably middling, but I'm only mildly sure." Its prior mean is $\dfrac{\alpha}{\alpha+\beta}=\dfrac{2}{2+2}=0.5$.

Now flip the coin and observe $h = 8$ successes and $t = 2$ failures (ten trials). Apply the rule:

$$
\alpha' = \alpha + h = 2 + 8 = 10, \qquad \beta' = \beta + t = 2 + 2 = 4.
$$

The posterior is $\mathrm{Beta}(10,\ 4)$. No integral was evaluated — two additions did the work. Its **posterior mean**, using the mean formula $\alpha/(\alpha+\beta)$ from [[beta-distribution]], is

$$
\frac{\alpha'}{\alpha'+\beta'} = \frac{10}{10+4} = \frac{10}{14} \approx 0.714.
$$

This is non-degenerate and instructive. The prior mean was $0.5$; the data alone (the raw success fraction) was $8/10 = 0.8$; and the posterior mean $0.714$ sits *between* them — the prior's two pseudo-successes and two pseudo-failures pull the estimate back from $0.8$ toward $0.5$, but the eight real successes pull harder. The posterior is also more concentrated than the prior (its parameters are larger, which [[beta-distribution]] says tightens the bump), reflecting that we now know more. The shape stayed Beta throughout; only the knobs $(\alpha,\beta)$ turned from $(2,2)$ to $(10,4)$.

### Why it matters: sequential updating

Conjugacy's closure has a second consequence that the worked instance sets up. Because the posterior is the same kind of object as the prior, **today's posterior can serve as tomorrow's prior** — the update rule can be applied again, with no change in machinery. This is **sequential (online) updating**.

Continue the example. We now believe $p\sim\mathrm{Beta}(10,4)$. Suppose a *second* batch arrives: $3$ more successes and $0$ failures. Treat $\mathrm{Beta}(10,4)$ as the new prior and apply the same rule:

$$
\alpha'' = 10 + 3 = 13, \qquad \beta'' = 4 + 0 = 4,
$$

giving $\mathrm{Beta}(13,\ 4)$, with posterior mean $\dfrac{13}{13+4} = \dfrac{13}{17}\approx 0.765$ — nudged upward by the three fresh successes, exactly as adding success-counts should do. (Confirm it composes: starting from the original $\mathrm{Beta}(2,2)$ and pooling *all* the data at once — $h = 8+3 = 11$ successes, $t = 2+0 = 2$ failures — gives $\mathrm{Beta}(2+11,\ 2+2) = \mathrm{Beta}(13,4)$, the same answer. Processing data in batches or all together yields identical results, because addition is associative.)

The practical upshot: an online learner watching a stream of coin-like outcomes does **not** need to keep the data. It stores just the two running numbers $(\alpha,\beta)$ — its current Beta posterior — and on each new observation increments $\alpha$ for a success or $\beta$ for a failure. The entire history is compressed into a pair of accumulating counts, and the belief is always available in closed form. That is the dividend conjugacy pays: the recurring, otherwise-expensive [[bayes-rule]] integral is replaced, forever, by addition.

## Prerequisites

- [[bayes-rule]]
- [[beta-distribution]]
- [[bernoulli-distribution]]
- [[likelihood]]

## Sources

_none_
