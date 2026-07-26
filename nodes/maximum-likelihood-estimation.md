---
id: maximum-likelihood-estimation
title: Maximum Likelihood Estimation
summary: Maximum likelihood estimation (MLE) is a recipe for turning observed data into a single best guess for an unknown parameter.
type: concept
tags: [math/probability]
prereqs: [likelihood, derivative, bernoulli-distribution, probability-distribution]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Maximum Likelihood Estimation

## Summary

**Maximum likelihood estimation (MLE)** is a recipe for turning observed data into a single best guess for an unknown parameter. The idea is a one-line principle: of all the parameter settings you *could* have used, pick the one under which the data you actually saw would have been **most probable** — the setting that makes your observation least surprising. Concretely, the [[likelihood]] $L(\theta)$ scores each candidate parameter $\theta$ by how probable it makes the data; MLE returns the $\theta$ that maximizes that score, written $\hat{\theta} = \arg\max_\theta L(\theta)$ (the "$\arg\max$" means "the argument that produces the maximum," and the hat on $\hat\theta$ marks it as an *estimate* computed from data, not the true value). To find that peak we don't maximize $L$ directly — a fragile product of many small numbers — but its logarithm, the log-likelihood $\ell(\theta)$, which peaks at the *same* place (because $\ln$ is increasing) yet turns the product into a sum. At a smooth interior peak the function is momentarily flat, so its [[derivative]] is zero; we therefore solve $\ell'(\theta) = 0$ for the stationary point and confirm it is a maximum. Run this on a [[bernoulli-distribution]] coin observed with $h$ heads and $t$ tails and the algebra delivers $\hat p = h / (h+t)$ — the MLE for a coin is simply "heads over total flips," the observed proportion. The method recovers exactly the answer intuition expects, and that agreement is *why* the principle is trusted.

## Grounded explanation

### The problem MLE solves

You have a model with a knob you cannot see. A coin has some heads-probability $p$; a sensor has some noise level; a drug has some response rate. You cannot read the knob off directly — you only get to watch the process produce data. The question MLE answers is the most basic one in statistics: **given the data I observed, what single value of the knob should I report as my best guess?**

Throughout, $\theta$ (Greek "theta") denotes the unknown **parameter** — the knob setting we want to estimate — and $D$ denotes the **data** we actually observed. From [[likelihood]] we have the tool that connects the two: the likelihood function

$$ L(\theta) = P(D \mid \theta), \qquad D \text{ fixed at the observed data,} $$

read as a function *of the parameter*. For each candidate setting $\theta$, $L(\theta)$ reports **how probable the data we actually saw would have been if that $\theta$ were the truth.** A $\theta$ that would have rendered the observation nearly impossible scores near $0$; a $\theta$ that would have made it very likely scores high. Recall the crucial caveat from [[likelihood]]: $L(\theta)$ is *not* a probability distribution over $\theta$ — its values across different $\theta$ do not sum to $1$ — but the values are real, comparable scores. MLE is built precisely on *comparing* them.

### The principle, and why it is the principled choice

Here is the whole concept in one sentence:

> **Maximum likelihood estimation reports the parameter value under which the observed data is most probable.**

Formally, the **maximum likelihood estimate** is

$$ \hat{\theta} = \arg\max_{\theta}\, L(\theta). $$

The notation $\arg\max_\theta$ means "the value of $\theta$ at which the following expression is largest" — not the largest *value* of $L$ (that would be $\max_\theta L$), but the *location* of that peak. The hat in $\hat\theta$ is standard shorthand for "an estimate built from data," distinguishing it from the unknown true $\theta$.

Why is "make the data most probable" a *principled* rule rather than an arbitrary one? Because it is the answer to a fair question: among the explanations on the table, which one is *least astonished* by what happened? A parameter setting under which your observation would have been a one-in-a-million fluke is a poor explanation of that observation; a setting under which the observation was exactly what you'd expect is a good one. MLE formalizes "the explanation that fits best is the one that finds the data least surprising." It does **not** claim $\hat\theta$ is the most probable parameter — we just saw the likelihood is not a distribution over $\theta$, so "most probable $\theta$" is not even defined here without extra assumptions. It claims something cleaner and assumption-free: $\hat\theta$ is the setting that assigns the **highest probability to the facts in hand**.

### The log trick: why we maximize $\ell$ instead of $L$

Real data are many observations, not one. From [[likelihood]], independent observations multiply: if the data are $d_1, \dots, d_n$ (the subscript $i$ just indexes which observation $d_i$ is the $i$-th), then

$$ L(\theta) = \prod_{i=1}^{n} P(d_i \mid \theta), $$

where $\prod_{i=1}^n$ means "multiply together over $i$ from $1$ to $n$." This product is hostile to the tool we want to use next. It is a chain of many factors each below $1$, so it collapses toward $0$; and to differentiate a product of $n$ varying factors is a mess.

The fix, also from [[likelihood]]: take the natural logarithm and define the **log-likelihood**

$$ \ell(\theta) = \ln L(\theta) = \sum_{i=1}^{n} \ln P(d_i \mid \theta), $$

using $\ln(ab) = \ln a + \ln b$ — the log of a product is the sum of the logs. The fragile product has become a clean sum, and a sum is exactly what a [[derivative]] handles **termwise**: the derivative of a sum is the sum of the derivatives, so each observation contributes its own piece independently.

The one thing we must not break is *where the peak sits*. It is safe because $\ln$ is **strictly increasing**: if $L(\theta_1) > L(\theta_2)$ then $\ln L(\theta_1) > \ln L(\theta_2)$, for every pair. A strictly increasing function never reshuffles the ranking of its inputs, so it cannot move the location of the highest one. The peak's *height* changes; its *argmax* does not. Therefore

$$ \arg\max_\theta L(\theta) = \arg\max_\theta \ell(\theta), $$

and we are free to maximize the convenient $\ell$ and report the identical $\hat\theta$.

### Finding the peak with the derivative

Now we use [[derivative]] to locate the maximum. The [[derivative]] $\ell'(\theta)$ is the instantaneous rate of change of $\ell$ as $\theta$ nudges: positive where $\ell$ is rising, negative where it is falling. At a smooth interior peak — the top of a hill — the function is momentarily neither rising nor falling; it is **flat**. So at the peak the slope is zero:

$$ \ell'(\theta) = 0. $$

This is the **stationary-point condition**. We solve it for $\theta$ to get the candidate $\hat\theta$. One caution that the principle demands: $\ell'(\theta)=0$ holds at *any* flat spot — a maximum, a minimum, or a plateau — so it is **necessary but not sufficient.** We must confirm the stationary point is a maximum and not a minimum. The simplest honest check: a peak is where the slope **switches from positive to negative** as $\theta$ increases through it (rising just before, falling just after). If $\ell'$ is positive to the left of $\hat\theta$ and negative to its right, $\hat\theta$ is a maximum. (Endpoints of the parameter's allowed range need a separate look, since the function need not be flat there.)

So the full MLE algorithm is four steps:

1. Write the [[likelihood]] $L(\theta)$ as the product of the per-observation probabilities the model assigns — each factor $P(d_i \mid \theta)$ is read off the model's [[probability-distribution]] evaluated at the observed value $d_i$.
2. Take logs to get the log-likelihood $\ell(\theta)$ — a sum.
3. Differentiate and set $\ell'(\theta) = 0$; solve for $\theta$.
4. Check the stationary point is a maximum.

### Worked instance: the bias of a coin

Let the model be a [[bernoulli-distribution]] coin. Each flip is an independent Bernoulli trial that lands **heads** (the outcome we track, coded $1$) with probability $p$ and **tails** (coded $0$) with probability $1 - p$; the parameter is $\theta = p$, a single number in $[0,1]$. We flip the coin and record $h$ **heads** and $t$ **tails**, for $n = h + t$ flips total. The data $D$ is now fixed at "$h$ heads, $t$ tails"; $p$ is the knob we sweep.

**Step 1 — the likelihood.** From the [[bernoulli-distribution]], one heads contributes a factor $p$ and one tails a factor $1 - p$. By independence the flips multiply, giving $h$ factors of $p$ and $t$ factors of $(1-p)$:

$$ L(p) = p^{h}\,(1 - p)^{t}. $$

**Step 2 — the log-likelihood.** Take logs, using $\ln(ab) = \ln a + \ln b$ and $\ln(x^k) = k\ln x$:

$$ \ell(p) = \ln\!\big(p^{h}(1-p)^{t}\big) = h \ln p + t \ln(1 - p). $$

The product of $n$ factors has become a sum of just two terms — one per outcome type.

**Step 3 — differentiate and set to zero.** We differentiate term by term. The [[derivative]] of $\ln p$ with respect to $p$ is $1/p$; the derivative of $\ln(1-p)$ is $-1/(1-p)$ (the inner $1 - p$ decreases as $p$ rises, which supplies the minus sign). Hence

$$ \ell'(p) = \frac{h}{p} - \frac{t}{1 - p}. $$

Setting $\ell'(p) = 0$:

$$ \frac{h}{p} = \frac{t}{1 - p} \;\;\Longrightarrow\;\; h\,(1 - p) = t\,p \;\;\Longrightarrow\;\; h - h p = t p \;\;\Longrightarrow\;\; h = (h + t)\,p, $$

so the stationary point is

$$ \boxed{\;\hat p = \dfrac{h}{h + t}\;} $$

— **heads over total flips**, the observed proportion of heads.

**Step 4 — confirm it is a maximum.** Look at the sign of $\ell'(p) = \tfrac{h}{p} - \tfrac{t}{1-p}$ on either side of $\hat p$. As $p$ rises from $0$ toward $1$, the first term $h/p$ shrinks and the second term $t/(1-p)$ grows, so $\ell'$ moves steadily from positive to negative — crossing zero exactly once, at $\hat p$. Positive slope to the left, negative to the right: $\hat p$ is a maximum, as required. (At the boundaries $\ell$ runs off to $-\infty$ whenever $h>0$ and $t>0$, since $\ln 0 = -\infty$, so the interior peak is genuinely the top.)

**Plug in numbers.** Suppose we flip the coin $10$ times and see $h = 8$ heads and $t = 2$ tails (a non-degenerate case: both counts are nonzero, so both terms of $\ell$ are live and neither factor of $L$ collapses). Then

$$ \hat p = \frac{h}{h+t} = \frac{8}{8 + 2} = \frac{8}{10} = 0.8. $$

The maximum likelihood estimate of the coin's heads-probability is **$0.8$** — exactly the fraction of flips that came up heads. We can sanity-check against the [[likelihood]] scores: $L(0.8) = 0.8^{8}(0.2)^{2} \approx 0.00671$, whereas a fair-coin guess scores $L(0.5) = 0.5^{10} \approx 0.000977$, about $6.9\times$ smaller. No other $p$ beats $0.8$; the calculus found the true top of the hill, and it coincides with the common-sense estimate "$8$ out of $10$."

That coincidence is the payoff. MLE did not *assume* "use the observed proportion"; it *derived* it from the single principle "make the data most probable." When a principled, mechanical procedure reproduces the answer intuition already trusts, that is strong evidence the principle is sound — and the same machinery then keeps working in models where intuition gives out.

### An honest edge case

The formula $\hat p = h/(h+t)$ takes the data at face value, which can over-commit on thin evidence. Flip the coin **once**, see $1$ head and $0$ tails, and the MLE is $\hat p = 1/(1+0) = 1.0$: the procedure declares the coin will *never* land tails, on the strength of a single flip. That is plainly over-confident — yet it is exactly what "the parameter making the data most probable" says, since $p = 1$ assigns probability $1$ to "one head." MLE has no built-in skepticism; it trusts the data completely. Tempering that with prior belief is the job of a different estimation principle, beyond this node.

## Prerequisites

- [[likelihood]]
- [[derivative]]
- [[bernoulli-distribution]]
- [[probability-distribution]]

## Sources

_none_
