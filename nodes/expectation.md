---
id: expectation
title: Expectation
summary: A probability-distribution tells you how likely each value of a random variable is, but not what value to expect on average.
type: concept
tags: [math/probability]
prereqs: [probability-distribution, random-variable]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Expectation

## Summary

A [[probability-distribution]] tells you *how likely* each value of a [[random-variable]] is, but not what value to *expect* on average. The **expectation** (or **mean**) $E[X]$ answers that: it is the probability-weighted average of the values — the **center of mass** of the distribution, the point where the spread of probability would balance. For a discrete variable with probability mass function (pmf) $p$, you weight each value by its mass and add: $E[X] = \sum_x x\,p(x)$. For a continuous variable with probability density function (pdf) $f$, the sum becomes an area integral: $E[X] = \int x\,f(x)\,dx$. Expectation has two properties that make it the workhorse of probability. **Linearity**: $E[aX + b] = aE[X] + b$, and $E[X + Y] = E[X] + E[Y]$ for *any* two variables, even dependent ones. The **law of the unconscious statistician** (LOTUS): to average a transformed variable $g(X)$ you reweight the *original* values, $E[g(X)] = \sum_x g(x)\,p(x)$, without ever finding the distribution of $g(X)$. From it comes the **variance** $\mathrm{Var}(X) = E[(X-\mu)^2] = E[X^2] - E[X]^2$, the expected squared distance from the mean $\mu = E[X]$, which measures spread. A warning to carry forward: in general $E[g(X)] \neq g(E[X])$.

## Grounded explanation

### What the concept *is*

A [[probability-distribution]] of a [[random-variable]] $X$ is the complete account of where $X$'s probability lives: for a **discrete** $X$ it is a **probability mass function** (pmf) $p$, where $p(x) = P(X = x)$ is the probability $X$ equals the value $x$; for a **continuous** $X$ it is a **probability density function** (pdf) $f$, a height curve where probability is the *area* under it, and $f(x)$ is probability *per unit length* (not itself a probability). In both cases the total — the summed mass $\sum_x p(x)$ or the enclosed area $\int f(x)\,dx$ — equals exactly $1$, because $X$ is certain to take *some* value.

The distribution says how likely each value is. It does not, by itself, hand you a single number summarizing "what value $X$ tends to come out to." The **expectation** $E[X]$ is that single number. Throughout, $E[\,\cdot\,]$ reads "the expected value of," and the symbol $\mu$ (Greek "mu") is a standard shorthand for $E[X]$.

The defining idea is a **weighted average**. An ordinary average of values $1, 2, 3$ treats them as equally important: $(1+2+3)/3 = 2$. But under a distribution the values are *not* equally likely — each carries its own mass. So we weight each value by exactly how much probability it has, and add:

$$ E[X] = \sum_x x\, p(x) \quad\text{(discrete)}, \qquad E[X] = \int_{-\infty}^{\infty} x\, f(x)\,dx \quad\text{(continuous)}. $$

Here $\sum_x$ adds over every value $x$ in the support (the set of values carrying probability), and $\int_{-\infty}^{\infty} \cdots dx$ is the total area along the whole number line. Each term is a value $x$ multiplied by its weight ($p(x)$ for mass, $f(x)\,dx$ for an infinitesimal slice of area).

### Why this is the "center of mass"

Picture the number line as a weightless rod, and at each value $x$ hang a weight equal to its probability $p(x)$. Because the distribution normalizes — the weights sum to $1$ — the rod carries exactly one unit of total weight. The **balance point** of such a loaded rod, the place you could put a single fingertip under it and have it not tip, is precisely $\sum_x x\,p(x)$: each weight pulls the balance toward itself in proportion to *how heavy it is* and *how far out it sits*. That balance point is $E[X]$. This is why expectation is called the center of mass of the distribution: it is literally the formula a physicist uses for the balance point of distributed weight, with probability playing the role of mass. The continuous version is the same picture with the discrete weights replaced by a continuous smear of density $f(x)$.

This also explains why $E[X]$ need not be a value $X$ can ever take. The balance point of weights at $1$, $2$, $3$ can land at $2.1$, which is none of them — a balance point lives *between* the weights, not *on* one.

### Linearity — the property that makes expectation usable

Two rules let you push expectation through arithmetic without recomputing anything.

**Scaling and shifting one variable.** For constants $a$ and $b$,
$$ E[aX + b] = a\,E[X] + b. $$
*Why.* Form the new variable $aX + b$: every value $x$ becomes $ax + b$, but its probability $p(x)$ is unchanged (rescaling and shifting the number line does not move probability between outcomes). So
$$ E[aX+b] = \sum_x (ax+b)\,p(x) = a\sum_x x\,p(x) + b\sum_x p(x) = a\,E[X] + b\cdot 1, $$
using that $\sum_x p(x) = 1$ by normalization. Physically: stretching the rod by $a$ and sliding it by $b$ moves its balance point exactly the same way.

**Adding two variables.** For *any* two random variables $X$ and $Y$ on the same experiment,
$$ E[X + Y] = E[X] + E[Y]. $$
The remarkable part is the phrase **any two** — this holds even when $X$ and $Y$ are **dependent** (knowing one tells you something about the other). The reason it survives dependence is that expectation is a *sum over outcomes*: on each individual outcome $\omega$, the realized values simply add, $(X+Y)(\omega) = X(\omega) + Y(\omega)$, and summing those per-outcome sums weighted by their probabilities splits into the two separate weighted sums. Dependence is about *how the two values move together*, which would matter for a product or for spread — but for a plain sum it never enters. This is what makes expectation so much friendlier than probability itself: you may add expectations freely.

### The law of the unconscious statistician (LOTUS)

Often you do not want $E[X]$ but the expectation of a *transformed* quantity — say $E[X^2]$, or $E[\,$cost$(X)\,]$. Write $g$ for the transforming function, so $g(X)$ is the new variable that outputs $g(x)$ whenever $X$ outputs $x$.

The naive route is: first find the *distribution* of $g(X)$ (a fresh pmf over the new values), then average. That extra step is usually painful and, it turns out, unnecessary. The **law of the unconscious statistician** says you may average $g$ over the *original* distribution directly:

$$ E[g(X)] = \sum_x g(x)\, p(x) \quad\text{(discrete)}, \qquad E[g(X)] = \int_{-\infty}^{\infty} g(x)\, f(x)\,dx \quad\text{(continuous)}. $$

*Why it holds.* Each original value $x$ occurs with probability $p(x)$, and *whenever* it occurs the transformed variable reads $g(x)$. So the value $g(x)$ inherits exactly the weight $p(x)$. Summing $g(x)$ against those inherited weights is the weighted average of $g(X)$ — without ever assembling the distribution of $g(X)$. (The name jokes that a statistician uses this formula "unconsciously," as if it needed no justification; it does, and the justification is this weight-inheritance.)

**A crucial warning.** In general
$$ E[g(X)] \neq g(E[X]). $$
You may *not* push $g$ inside the expectation. Averaging then transforming is not the same as transforming then averaging — for instance the average of the squares is not the square of the average (we will see exactly this gap below; it is what variance measures). The equality holds only when $g$ is linear (the case covered above). This inequality matters later and is a frequent source of error.

### Variance — expected squared deviation

Expectation gives the center; the next question is how *spread out* the distribution is around that center. Let $\mu = E[X]$ be the mean. The deviation of $X$ from its mean is $X - \mu$. Its raw average is useless — $E[X - \mu] = E[X] - \mu = 0$ by linearity, because positive and negative deviations cancel exactly (that is what "center" means). To stop the cancellation, square the deviation, making it always non-negative, then average it. That is the **variance**:

$$ \mathrm{Var}(X) = E\big[(X - \mu)^2\big]. $$

It is the *expected squared distance from the mean* — large when probability sits far from $\mu$, zero only when $X$ is glued to a single value. By LOTUS with $g(x) = (x - \mu)^2$, you compute it directly as $\sum_x (x-\mu)^2\,p(x)$.

There is a more convenient equivalent form. Expand the square and use linearity ($\mu$ is a constant, so $E[\mu X] = \mu E[X] = \mu^2$ and $E[\mu^2] = \mu^2$):
$$ \mathrm{Var}(X) = E[X^2 - 2\mu X + \mu^2] = E[X^2] - 2\mu E[X] + \mu^2 = E[X^2] - 2\mu^2 + \mu^2 = E[X^2] - \mu^2. $$
So
$$ \boxed{\ \mathrm{Var}(X) = E[X^2] - E[X]^2.\ } $$
In words: the average of the squares minus the square of the average. This is the same gap flagged above — it is precisely $E[g(X)] - g(E[X])$ for $g(x)=x^2$ — and because squared deviations are never negative, the gap is never negative: $E[X^2] \ge E[X]^2$ always.

### Worked instance (discrete)

Reuse the distribution from [[probability-distribution]]: $X$ takes values in $\{1, 2, 3\}$ with masses
$$ p(1) = 0.2, \qquad p(2) = 0.5, \qquad p(3) = 0.3. $$
(These are non-negative and sum to $0.2 + 0.5 + 0.3 = 1$ — a valid distribution, and non-degenerate, since all three masses are positive and unequal.)

**Mean.** Weight each value by its mass and add:
$$ E[X] = 1(0.2) + 2(0.5) + 3(0.3) = 0.2 + 1.0 + 0.9 = 2.1 = \mu. $$
Note $2.1$ is not one of the values $1, 2, 3$ — it is the balance point between them, pulled above $2$ because the mass at $3$ ($0.3$) slightly outweighs the mass at $1$ ($0.2$).

**Second moment via LOTUS.** Take $g(x) = x^2$, so $g(1)=1$, $g(2)=4$, $g(3)=9$. We reweight these by the *original* masses — never building the distribution of $X^2$:
$$ E[X^2] = 1(0.2) + 4(0.5) + 9(0.3) = 0.2 + 2.0 + 2.7 = 4.9. $$

**Variance.** Using $\mathrm{Var}(X) = E[X^2] - E[X]^2$:
$$ \mathrm{Var}(X) = 4.9 - (2.1)^2 = 4.9 - 4.41 = 0.49. $$

**The warning, made concrete.** Here $g(E[X]) = (E[X])^2 = (2.1)^2 = 4.41$, but $E[g(X)] = E[X^2] = 4.9$. They differ by $0.49$ — exactly the variance. This is a live demonstration that $E[g(X)] \neq g(E[X])$: averaging the squares gave $4.9$, squaring the average gave $4.41$, and the positive gap *is* the spread of the distribution.

### Worked instance (linearity, two dice)

Linearity earns its keep when a variable is a *sum*. Let $X$ be the total of two fair six-sided dice. Doing it the hard way means building the pmf of the sum (the famous triangular distribution: $7$ is likeliest, $2$ and $12$ rarest) and then averaging — real work. Linearity bypasses all of it.

Let $D_1$ and $D_2$ be the two individual dice, so $X = D_1 + D_2$. For one fair die, each face $1,\dots,6$ has mass $\tfrac{1}{6}$, so
$$ E[D_1] = \tfrac{1}{6}(1+2+3+4+5+6) = \tfrac{1}{6}(21) = 3.5. $$
By symmetry $E[D_2] = 3.5$ as well. Then by $E[X+Y] = E[X]+E[Y]$,
$$ E[X] = E[D_1] + E[D_2] = 3.5 + 3.5 = 7. $$
The expected sum of two dice is $7$ — obtained without ever touching the sum's distribution. (And had the dice been somehow dependent, e.g. rigged to move together, this answer would not change one bit: linearity of expectation does not care.)

### Pulling it together

| Quantity | Definition | Discrete formula | What it tells you |
|---|---|---|---|
| Mean $E[X] = \mu$ | probability-weighted average | $\sum_x x\,p(x)$ | center of mass / balance point |
| $E[g(X)]$ (LOTUS) | average of a transform | $\sum_x g(x)\,p(x)$ | no need for $g(X)$'s distribution |
| Variance $\mathrm{Var}(X)$ | expected squared deviation | $E[X^2] - E[X]^2$ | spread around the mean |

The single engine behind all of it is the weighted average: each value counted in proportion to the probability the [[probability-distribution]] assigns it. Linearity follows because a weighted sum splits over addition; LOTUS follows because a transformed value inherits its input's weight; variance is just LOTUS applied to squared deviation. And the standing caution — $E[g(X)] \neq g(E[X])$ — is not a footnote but the very thing variance measures.

## Prerequisites

- [[probability-distribution]]

## Sources

_none_
