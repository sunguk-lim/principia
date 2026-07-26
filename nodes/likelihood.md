---
id: likelihood
title: Likelihood
summary: A probability-distribution $P(D \mid \theta)$ answers "given the setting $\theta$, how probable is each possible data outcome $D$?" — here $\theta$ (Greek "theta") is a parameter…
type: concept
tags: [math/probability]
prereqs: [probability-distribution]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Likelihood

## Summary

A [[probability-distribution]] $P(D \mid \theta)$ answers "given the setting $\theta$, how probable is each possible data outcome $D$?" — here $\theta$ (Greek "theta") is a **parameter**, a number (or set of numbers) that pins down which distribution we mean, and $D$ stands for the **data**, the outcome that actually got observed. The **likelihood** is what you get by *flipping which slot is the variable*: you fix $D$ at the data you really saw and let $\theta$ vary, reading $L(\theta) = P(D \mid \theta)$ as a function **of the parameter**. Same formula, opposite reading. The crucial twist: read as a function of $D$ it is a probability distribution (its values over all outcomes sum or integrate to exactly 1); read as a function of $\theta$ it is **not** a distribution — its values over different $\theta$ do not sum to 1, because $\theta$ is not the thing the randomness is spread over. When the data are several independent observations the likelihood is the **product** of each observation's probability, and taking the logarithm turns that awkward product into a sum, the **log-likelihood** $\ell(\theta)$, which (because $\ln$ is increasing) peaks at the very same $\theta$ — which is why fitting a model means maximizing the log-likelihood.

## Grounded explanation

### Starting point: a distribution that carries a knob

Recall from [[probability-distribution]] that a distribution is the complete rule for how probability is spread across the values a random quantity can take, with the total pinned to exactly 1 (a sum of point-masses in the discrete case, an area under a density in the continuous case). Now attach a **knob** to that rule.

Write the distribution as $P(D \mid \theta)$, read "the probability of the data $D$ *given* the parameter $\theta$." Two symbols, defined before use:

- $\theta$ — the **parameter**: a number, or a list of numbers, that selects *which* distribution we are talking about. Turning the knob $\theta$ swaps in a different distribution over the data.
- $D$ — the **data**: the outcome that the random process produced. Until we observe it, $D$ is the random thing; the distribution tells us how its probability is spread.

For each fixed setting of the knob $\theta$, $P(D \mid \theta)$ is an honest [[probability-distribution]] over $D$: hold $\theta$ still, sweep $D$ over all its possible outcomes, and the values sum (discrete) or integrate (continuous) to exactly 1. That is the "given $\theta$" reading — $\theta$ is a fixed setting, $D$ is the variable.

### The concept: flip which argument varies

Here is the whole move. After we run the experiment, **the data $D$ stops being unknown** — we *saw* it. What we don't know is the knob: which $\theta$ produced what we saw. So we flip the roles.

> Fix $D$ at the observed value. Let $\theta$ be the variable. Read the very same expression $P(D \mid \theta)$ as a function of $\theta$.

That function is the **likelihood**, written

$$ L(\theta) = P(D \mid \theta), \qquad D \text{ fixed at the observed data.} $$

Nothing in the formula changed — only *which slot we are sweeping*. $L(\theta)$ measures, for each candidate setting of the knob, **how probable the data we actually saw would have been under that setting.** A $\theta$ that would have made the observed data very probable scores high; a $\theta$ that would have made it nearly impossible scores low. That score is the entire point: it is how we rank competing explanations $\theta$ of one fixed observation.

### Why the likelihood is NOT a probability distribution (the key insight)

This is the step that looks like sleight of hand, so here is the justification in full.

A [[probability-distribution]] earns its name from **normalization**: the total over the variable equals exactly 1, *because the variable is certain to take some value*. That law applies to the slot the randomness lives in — namely $D$. Sweep $D$ (with $\theta$ fixed) and you get 1, every time. Good: $P(\cdot \mid \theta)$ is a distribution over $D$.

But the likelihood sweeps the *other* slot, $\theta$. And $\theta$ is **not** a random outcome of the experiment — it is a fixed (if unknown) setting of the knob; nothing forces "$\theta$ takes some value" to be an event whose probability must total 1. So there is no law pinning $\sum_\theta L(\theta)$ to anything in particular. In general

$$ \sum_\theta L(\theta) \neq 1. $$

The two readings of the *same numbers* therefore have different status:

| Reading | Variable | Other slot | Is it a distribution? | Total over the variable |
|---|---|---|---|---|
| $P(D \mid \theta)$ as a function of $D$ | $D$ (data) | $\theta$ fixed | **yes** | exactly 1 |
| $L(\theta) = P(D \mid \theta)$ as a function of $\theta$ | $\theta$ (parameter) | $D$ fixed | **no** | no constraint |

So "likelihood" is precisely the name we give the second reading, to flag that it is *not* a distribution over $\theta$. Calling $L(\theta)$ a "probability of $\theta$" is the classic error; the values are real and comparable, but they are not probabilities of the parameter.

### Many independent observations: a product

Usually the data are not one observation but several. Say we collect $n$ observations $d_1, d_2, \dots, d_n$ (the subscript $i$ just indexes which observation; $d_i$ is the $i$-th one), and they are **independent** — each one's outcome does not influence any other's. For independent events, the probability that *all* of them happen together is the product of their individual probabilities. Applying that to the data under a candidate $\theta$:

$$ L(\theta) = \prod_{i=1}^{n} P(d_i \mid \theta), $$

where $\prod_{i=1}^{n}$ means "multiply together, over $i$ running from $1$ to $n$." Each factor $P(d_i \mid \theta)$ is the probability the model assigns to one observation; the joint likelihood multiplies them.

### The log-likelihood, and why we maximize it

A product of many small numbers is awkward: it shrinks toward 0 fast, and products are clumsy to handle. The fix is to take the natural logarithm and use the rule $\ln(ab) = \ln a + \ln b$ — the log of a product is the sum of the logs. Define the **log-likelihood**

$$ \ell(\theta) = \ln L(\theta) = \ln \prod_{i=1}^{n} P(d_i \mid \theta) = \sum_{i=1}^{n} \ln P(d_i \mid \theta), $$

where $\ell$ (script "ell") is the standard symbol for it. The product has become a clean **sum**.

Now the justification for the move that powers all model fitting: **$\ell(\theta)$ and $L(\theta)$ peak at the same $\theta$.** The reason is that $\ln$ is **strictly increasing** — if $L(\theta_1) > L(\theta_2)$ then $\ln L(\theta_1) > \ln L(\theta_2)$, with the order of *every* pair preserved. A monotonic increasing function never reshuffles the ranking of its inputs, so it cannot move the location of the highest point. The *height* changes; the *argmax* (the $\theta$ where the peak sits) does not. Therefore "find the $\theta$ that makes the observed data most probable" can be done on $\ell$ — a sum that is easy to differentiate and add — instead of on $L$ — a fragile product — with the identical answer. This is exactly why estimation maximizes the log-likelihood rather than the likelihood itself.

### Worked instance: a coin with unknown bias

A coin lands heads with probability $p$ and tails with probability $1 - p$; the parameter is $\theta = p$, a single number in $[0, 1]$. We flip it $10$ times — independently — and observe $h = 8$ heads and $t = 2$ tails. The data $D$ is now **fixed** at "8 heads, 2 tails"; $p$ is what we sweep.

Each heads contributes a factor $p$, each tails a factor $1 - p$. By independence the likelihood is the product of all ten factors — eight $p$'s and two $(1-p)$'s:

$$ L(p) = \prod_{i=1}^{10} P(d_i \mid p) = p^{8}\,(1 - p)^{2}. $$

This is a genuine function *of $p$*, so evaluate it at two competing settings of the knob to watch it vary:

- At $p = 0.8$: $\; L(0.8) = 0.8^{8} \times 0.2^{2} = 0.16777 \times 0.04 \approx 0.00671.$
- At $p = 0.5$ (a fair coin): $\; L(0.5) = 0.5^{8} \times 0.5^{2} = 0.5^{10} \approx 0.000977.$

Comparing, $0.00671 / 0.000977 \approx 6.9$: the setting $p = 0.8$ makes the observed 8-heads-out-of-10 about **6.9 times more probable** than the fair-coin setting $p = 0.5$. That ratio is the likelihood doing its job — ranking explanations of one fixed observation. (The instance is non-degenerate: both factors are live, since $8 \neq 0$ and $2 \neq 0$, so neither $p^8$ nor $(1-p)^2$ collapses.)

The log-likelihood of the same data is the sum

$$ \ell(p) = 8 \ln p + 2 \ln(1 - p). $$

Check that it preserves the ranking: $\ell(0.8) = \ln(0.00671) \approx -5.00$ and $\ell(0.5) = \ln(0.000977) \approx -6.93$. Since $-5.00 > -6.93$, $p = 0.8$ still wins, by the same margin in log terms ($-5.00 - (-6.93) \approx 1.93 = \ln 6.9$) — exactly as the strictly-increasing $\ln$ guarantees.

**And it is not a distribution over $p$.** Add the likelihood across a grid of candidate $p$ values, say $p = 0.0, 0.1, 0.2, \dots, 1.0$. The endpoints give $L(0) = 0$ and $L(1) = 0$ (eight heads is impossible if $p=0$; two tails is impossible if $p=1$), the interior values are all small positive numbers like the two above, and their sum lands nowhere near 1 — it is roughly $0.03$, not $1$. There is no normalization law forcing otherwise, because $p$ is the knob, not the random outcome. Contrast this with the *data* slot: for any fixed $p$, summing $P(D \mid p)$ over all $11$ possible head-counts $0, 1, \dots, 10$ does give exactly 1 — that slot is a [[probability-distribution]]; the $p$ slot is not.

## Prerequisites

- [[probability-distribution]]

## Sources

_none_
