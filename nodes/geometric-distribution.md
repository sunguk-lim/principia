---
id: geometric-distribution
title: Geometric Distribution
summary: Imagine repeating the same yes/no experiment over and over — flipping a coin until it lands heads, say — where each attempt succeeds with the same fixed probability $p$ and the…
type: concept
tags: [math/probability]
prereqs: [probability-distribution, random-variable]
sources: [etc/study-notes.html]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Geometric Distribution

## Summary

Imagine repeating the *same* yes/no experiment over and over — flipping a coin until it lands heads, say — where each attempt succeeds with the same fixed probability $p$ and the attempts don't influence one another. The **geometric distribution** is the [[probability-distribution]] of *how long you wait*: how many failures pile up before that first success arrives. Its rule is one clean formula — the probability of seeing exactly $k$ failures and then a success is $(1-p)^k\,p$, because you need $k$ independent flops (each of probability $1-p$) followed by one win (probability $p$). The weights start at their largest on $k=0$ and shrink geometrically — each step multiplies by $1-p$ — which is where the name comes from. Its signature trait is **memorylessness**: having already waited a while tells you nothing about how much longer you'll wait, since each fresh trial is oblivious to the past. On average you suffer $(1-p)/p$ failures (equivalently $1/p$ total trials). It is the natural model for "toss until the first head," and fitting $p$ from data by maximum likelihood collapses to the intuitive answer: the number of successes divided by the number of trials.

## Grounded explanation

### What the concept *is*

The geometric distribution is one specific [[probability-distribution]] — a complete rule assigning a probability to each value of a random variable — chosen to answer a *waiting-time* question. Recall that a [[probability-distribution]] over a discrete variable is a **probability mass function** (pmf): a non-negative weight $p(k) = P(K=k)$ on each value $k$ the variable can take, with all weights summing to exactly 1. The geometric distribution is the particular pmf you get from the following setup.

Fix a single experiment with only two outcomes — call them **success** and **failure** — where success has a fixed probability $p$ (a number with $0 < p \le 1$) and failure therefore has probability $1-p$. Now repeat this experiment again and again under two conditions:

- **Identical:** every repetition has the very same success probability $p$. The coin doesn't change between flips.
- **Independent:** the outcome of one repetition has no bearing on any other. (Two events are **independent** when knowing one happened doesn't shift the probability of the other; concretely, the probability that both occur is the product of their separate probabilities.)

Each such repetition is called a **trial**. The quantity we track is the [[random-variable]] $K$ = *the number of failed trials that occur before the first success* (a function that maps each run of the experiment to a non-negative integer). The geometric distribution is the [[probability-distribution]] of $K$.

A note on convention, since it trips people up. Two equivalent versions exist: **$K$ = number of failures before the first success** (so $K$ can be $0, 1, 2, \dots$), or **$N$ = number of trials up to and including the first success** (so $N = K+1$ and starts at $1$). They describe the same process shifted by one. This node uses the failures-count version $K$ throughout, matching the source; translate to trials by adding 1.

### The defining formula and *why* it holds

The pmf is

$$ P(K = k) = (1-p)^k\, p, \qquad k = 0, 1, 2, \dots $$

Here $k$ is a specific non-negative whole number, $(1-p)^k$ means $(1-p)$ multiplied by itself $k$ times (with $(1-p)^0 = 1$), and the **support** — the set of values carrying any probability — is all the non-negative integers.

Why this exact product? The event "$K = k$" is the event of one *particular* sequence of outcomes: **fail, fail, …, fail** ($k$ times) **then succeed**. Spell out that sequence and use independence to multiply the per-trial probabilities:

- The first $k$ trials must each be a failure. One failure has probability $1-p$; because the trials are independent, the chance of $k$ failures in a row is the product $(1-p) \times (1-p) \times \cdots = (1-p)^k$.
- The very next trial must be a success, probability $p$.
- Multiplying (independence again): $(1-p)^k \cdot p$.

That is the whole derivation — the "magic-looking" exponent $k$ is just *counting how many independent failure-probabilities got multiplied together*.

**It is a valid distribution (normalization).** The weights must be non-negative and sum to 1. Non-negativity is immediate: $p \ge 0$ and $(1-p)^k \ge 0$. For the sum, add the weights over every possible $k$:

$$ \sum_{k=0}^{\infty} (1-p)^k\, p \;=\; p \sum_{k=0}^{\infty} (1-p)^k. $$

The remaining sum $\sum_{k=0}^{\infty} (1-p)^k = 1 + (1-p) + (1-p)^2 + \cdots$ is a **geometric series** — a sum where each term is a fixed ratio $r = 1-p$ times the previous one. When the ratio satisfies $0 \le r < 1$ (true here whenever $p > 0$), such a series adds up to the finite value $\frac{1}{1-r}$. With $r = 1-p$ that is $\frac{1}{1-(1-p)} = \frac{1}{p}$. Hence

$$ p \cdot \frac{1}{p} = 1, $$

so the weights sum to exactly 1, as a [[probability-distribution]] demands. (The series gives the distribution its name — its weights are the terms of a geometric series, each $(1-p)$ times the one before, so they decay geometrically as $k$ grows.)

### The signature property: memorylessness

Here is the geometric distribution's defining trait, and the reason it is *the* discrete waiting-time model. Suppose you have already endured $m$ failures with no success yet. How much *additional* waiting remains? The answer: the distribution of the extra wait is **exactly the original geometric distribution** — as if you had just started. Formally, the probability of waiting at least $j$ more failures, *given* you've already failed $m$ times, equals the unconditional probability of waiting at least $j$ failures from scratch.

The reason is built into the setup, not added on: the trials are independent and identical. The trials still to come neither remember nor care that earlier trials failed; each future trial still succeeds with probability $p$ on its own. So the past failures carry no information about the future — the process has **no memory**. A gambler who has flipped twenty tails in a row is, on the next flip, in exactly the same position as someone picking up a fresh coin. (The geometric distribution is the *only* discrete distribution with this property — which is why "memoryless waiting" and "geometric" are essentially synonyms.)

### How long do you wait on average?

The **mean** (or **expected value**) of a random variable is the long-run average of its values, computed by weighting each value by its probability and summing: $\sum_k k \cdot P(K=k)$. Carrying out that weighted sum for the geometric pmf gives

$$ \text{mean number of failures} = \frac{1-p}{p}. $$

Reading it sanity-checks the formula: if success is near-certain ($p$ close to 1), the numerator $1-p$ is tiny, so you expect almost no failures — right, you usually win immediately. If success is rare ($p$ close to 0), the ratio blows up, so you expect a long string of failures — also right. Counting *total trials* instead of failures adds the one final successful trial: $\frac{1-p}{p} + 1 = \frac{1}{p}$. So a success probability of $p$ means you wait, on average, $1/p$ trials — e.g. $p = 1/6$ for rolling a particular face on a die gives a mean of 6 rolls, matching intuition.

### Worked instance

Take $p = 0.3$ (a 30% chance of success per trial), so $1-p = 0.7$. Read a few weights off the pmf $P(K=k) = (0.7)^k (0.3)$:

- $P(K = 0) = (0.7)^0 \cdot 0.3 = 1 \cdot 0.3 = 0.3$. *(Succeed immediately, zero failures — the single most likely outcome.)*
- $P(K = 1) = (0.7)^1 \cdot 0.3 = 0.7 \cdot 0.3 = 0.21$.
- $P(K = 2) = (0.7)^2 \cdot 0.3 = 0.49 \cdot 0.3 = 0.147$. *(Two failures, then a success.)*

The weights $0.3, 0.21, 0.147, \dots$ strictly decrease, each exactly $0.7$ times the one before — the geometric decay. This instance is non-degenerate: $p$ is neither 0 nor 1, so no weight collapses to 0 and the decay is genuinely visible. Its mean number of failures is $\frac{1-p}{p} = \frac{0.7}{0.3} \approx 2.33$, or about $1/0.3 \approx 3.33$ total trials.

### Estimating $p$ from data: "toss until the first head"

The source's worked example fits the geometric distribution to observed data — the central applied use. You run the "toss until the first head" experiment $n$ separate times (independent **runs**), and run $i$ records $k_i$ = the number of tails (failures) before its first head. You don't know the coin's true $p$; you want the value best supported by the data. The standard recipe is **maximum likelihood**: choose the $p$ that makes the observed data most probable.

Because the runs are independent, the probability of the whole dataset is the product of each run's geometric weight, $\prod_{i=1}^{n} (1-p)^{k_i} p$. Products of many small numbers are awkward, so take the logarithm (the logarithm turns products into sums and, being strictly increasing, doesn't move the location of the maximum). This **log-likelihood** is

$$ \ell(p) = \Big(\textstyle\sum_i k_i\Big)\ln(1-p) + n\ln p, $$

where $\sum_i k_i$ is the total number of failures across all runs and $n \ln p$ collects the $n$ successes (one ends each run). To maximize, set the derivative to zero and solve; the result is

$$ \hat p = \frac{n}{\,n + \sum_i k_i\,} = \frac{\#\text{successes}}{\#\text{trials}}. $$

The reasoning behind that final equality is worth seeing, because it is the punchline. The numerator $n$ is the number of successes — exactly one per run, $n$ runs. The denominator counts *all trials ever made*: run $i$ took $k_i$ failures plus its one closing success, i.e. $1 + k_i$ trials, and summing over runs gives $\sum_i (1 + k_i) = n + \sum_i k_i$. So the estimate is literally **successes divided by trials** — the plainest imaginable answer ("if 12 heads turned up across 40 total flips, estimate $p = 12/40 = 0.3$"). The elaborate machinery of likelihoods and logarithms collapses back to the proportion you'd have guessed by eye, which is exactly why this example is instructive: it shows the formal method recovering common sense.

## Prerequisites

- [[probability-distribution]]
- [[random-variable]]

## Sources

- `etc/study-notes.html` — "Worked example — tossing until the first head": the geometric model $P(K=k)=(1-p)^k p$ and the maximum-likelihood estimate $\hat p = n/(n+\sum_i k_i) = \#\text{successes}/\#\text{trials}$.
