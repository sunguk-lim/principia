---
id: bernoulli-distribution
title: Bernoulli Distribution
summary: "The Bernoulli distribution is the simplest non-trivial probability-distribution: a single trial with exactly two outcomes — call them success (coded as the number $1$) and failure…"
type: concept
tags: [math/probability]
prereqs: [probability-distribution]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Bernoulli Distribution

## Summary

The **Bernoulli distribution** is the simplest non-trivial [[probability-distribution]]: a single trial with exactly two outcomes — call them **success** (coded as the number $1$) and **failure** (coded as $0$). One number $p$, the probability of success, fixes everything; failure then has probability $1 - p$, because the two probabilities must sum to 1. Its probability mass function (pmf) can be written in one compact line, $p(x) = p^x (1-p)^{1-x}$ for $x \in \{0, 1\}$, a formula whose only job is to print $p$ when $x = 1$ and $1 - p$ when $x = 0$. On average such a trial yields $p$ (its **mean**), and its **variance** — a measure of spread — is $p(1-p)$, largest exactly when $p = 0.5$ (a fair coin is the least predictable). Stacking $n$ such independent trials and counting how many succeed gives the **binomial distribution**, whose pmf $P(k) = \binom{n}{k}\, p^k (1-p)^{n-k}$ multiplies the chance of one specific success/failure pattern by $\binom{n}{k}$, the number of distinct patterns with exactly $k$ successes. This is the coin-flipping-with-counts model at the heart of much of statistics.

## Grounded explanation

### What the concept *is*

Recall from [[probability-distribution]] that a discrete distribution is described by a **probability mass function** (pmf) $p$, where $p(x) = P(X = x)$ — the probability that the random quantity $X$ comes out exactly equal to the value $x$ — and that a valid pmf must satisfy two rules: **non-negativity** ($p(x) \ge 0$ for every $x$) and **normalization** ($\sum_x p(x) = 1$, the masses over all values in the **support** add to exactly 1). The support is the set of values carrying nonzero probability.

The **Bernoulli distribution** is the smallest interesting instance of this machinery. Its support has just two values. Picture any single experiment whose result you can read as one of two things: a coin lands heads or tails, a thrown dart hits or misses, a patient responds to a drug or doesn't, a transmitted bit arrives correct or corrupted. We adopt one convention: code the outcome we are tracking ("success") as the number $\mathbf{1}$ and the other outcome ("failure") as $\mathbf{0}$. So the support is $\{0, 1\}$.

A random quantity $X$ that takes value $1$ with probability $p$ and value $0$ with probability $1 - p$ is said to **follow a Bernoulli distribution with parameter $p$**, written $X \sim \mathrm{Bernoulli}(p)$. Here $p$ is a single number between $0$ and $1$ called the **success probability**; the symbol $\sim$ reads "is distributed as." That one number is the *entire* distribution — there is nothing else to specify.

### Why failure must have probability $1 - p$

Why isn't the failure probability a second free number? Because normalization forbids it. There are only two values in the support, and they are mutually exclusive (one trial cannot be both a success and a failure). By the normalization rule, the two masses must sum to 1:
$$ p(1) + p(0) = 1. $$
We have *named* the success mass $p(1) = p$. Solving, $p(0) = 1 - p$. The failure probability is not an independent choice — it is *pinned* by certainty. The trial must produce *some* outcome, that event has probability 1, and with only two mutually exclusive options the leftover probability $1 - p$ has nowhere to go but onto failure. This is exactly the "total mass equals 1" law from [[probability-distribution]], applied to a support of size two.

For this to be a genuine pmf we also need non-negativity: $p \ge 0$ and $1 - p \ge 0$. The second forces $p \le 1$. Together these say $0 \le p \le 1$ — which is just the statement that $p$ is a probability.

### The compact one-line pmf

We could simply tabulate the distribution as "$p(1) = p$, $p(0) = 1-p$," and that is complete. But there is a tidy single formula that produces both lines, and it is worth understanding because the binomial below is built directly on it:
$$ p(x) = p^{x}\,(1 - p)^{1 - x}, \qquad x \in \{0, 1\}. $$
Here $p^x$ means "$p$ raised to the power $x$" and $(1-p)^{1-x}$ means "$(1-p)$ raised to the power $1 - x$." The formula looks like magic, but it is just a switch built out of exponents, using the fact that **any number raised to the power $0$ equals $1$** and **any number raised to the power $1$ equals itself**. Check the two cases:

- **$x = 1$ (success):** $p^{1} (1-p)^{1 - 1} = p^{1} (1-p)^{0} = p \cdot 1 = p$. ✓
- **$x = 0$ (failure):** $p^{0} (1-p)^{1 - 0} = 1 \cdot (1-p)^{1} = 1 - p$. ✓

So the exponents $x$ and $1 - x$ act as on/off switches: whichever outcome occurred keeps its probability factor, while the other factor collapses to $1$ and vanishes. The formula is not a new fact — it is the same two-line table, written so that a single expression covers both rows.

### The mean: what a Bernoulli trial yields on average

The **mean** (also called the **expected value**) of a discrete random quantity is the average of its possible values, each weighted by its probability — that is, $\sum_x x \cdot p(x)$. It answers: if you repeated the trial many times and averaged the coded outcomes, what number would you settle toward? Write it $E[X]$ ("the expected value of $X$"). For Bernoulli there are only two terms:
$$ E[X] = 0 \cdot p(0) + 1 \cdot p(1) = 0 \cdot (1-p) + 1 \cdot p = p. $$
So $E[X] = p$. This is pleasingly direct: because failure is coded as $0$, it contributes nothing to the sum, and success contributes its own probability. If you flip a coin that comes up heads (=1) with probability $0.3$ a thousand times and average the $1$s and $0$s, you drift toward $0.3$ — the long-run *fraction* of successes is the average of the coded outcomes precisely because the only nonzero code is $1$.

### The variance: how spread out the outcome is

The **variance** measures how far, on average, outcomes land from the mean — the *spread* of the distribution. It is defined as the expected value of the squared distance from the mean: $\sum_x (x - E[X])^2 \, p(x)$. We write it $\mathrm{Var}(X)$. Squaring keeps the two directions of deviation from cancelling and gives a single non-negative number; a variance of $0$ means no spread at all (the outcome is certain), and larger values mean a less predictable outcome.

With mean $E[X] = p$, the two outcomes sit at distances $(0 - p)$ and $(1 - p)$ from the mean:
$$ \mathrm{Var}(X) = (0 - p)^2 \, p(0) + (1 - p)^2 \, p(1) = p^2 (1 - p) + (1 - p)^2 \, p. $$
Both terms share a factor $p(1-p)$; pull it out:
$$ \mathrm{Var}(X) = p(1-p)\big[\, p + (1 - p) \,\big] = p(1-p)\cdot 1 = p(1 - p). $$
The bracket collapsed to $1$ because $p + (1-p) = 1$ — normalization sneaking in again. So $\mathrm{Var}(X) = p(1 - p)$.

This formula tells a story. The spread is **zero at the extremes** ($p = 0$ or $p = 1$): if success is impossible or guaranteed, the outcome never varies, so there is nothing to be uncertain about. The spread is **largest in the middle**: the product $p(1-p)$ is maximized at $p = 0.5$, where it equals $0.5 \times 0.5 = 0.25$. A fair coin is the *most* unpredictable Bernoulli trial — exactly the case where you have the least idea which way it will fall. That matches intuition, and the algebra confirms it.

### Worked instance: $\mathrm{Bernoulli}(0.3)$

Take $p = 0.3$ — a biased coin that comes up "success" (heads, coded $1$) only 30% of the time. This is non-degenerate: neither outcome is impossible, and $p \neq 0.5$ so the two outcomes are genuinely unequal.

- **pmf via the formula.** Success: $p(1) = 0.3^{1} \cdot 0.7^{0} = 0.3 \cdot 1 = 0.3$. Failure: $p(0) = 0.3^{0} \cdot 0.7^{1} = 1 \cdot 0.7 = 0.7$.
- **Normalization check:** $0.3 + 0.7 = 1.0$. ✓ Valid distribution.
- **Mean:** $E[X] = 0 \cdot 0.7 + 1 \cdot 0.3 = 0.3$.
- **Variance:** $\mathrm{Var}(X) = p(1-p) = 0.3 \times 0.7 = 0.21$.

For contrast, a fair coin ($p = 0.5$) would have variance $0.5 \times 0.5 = 0.25 > 0.21$: the $p = 0.3$ coin is *slightly more predictable* than a fair one, because leaning toward "failure" removes a little uncertainty. Pushing further, $p = 0.1$ gives variance $0.1 \times 0.9 = 0.09$ — much more predictable still, since you can bet on failure and usually be right.

### From one trial to many: the binomial distribution

The Bernoulli distribution describes *one* trial. The natural next question is: if I run $n$ independent trials, each $\mathrm{Bernoulli}(p)$, **how many successes** do I get in total? Let $K$ be that count. **Independent** means the outcome of one trial does not affect any other, so the probability of a *specific sequence* of outcomes is the product of the individual outcome probabilities. The distribution of $K$ is the **binomial distribution**, written $K \sim \mathrm{Binomial}(n, p)$, and its support is $\{0, 1, 2, \dots, n\}$ — you can get anywhere from zero successes to all $n$.

Its pmf is
$$ P(K = k) = \binom{n}{k}\, p^{k}\,(1 - p)^{n - k}, \qquad k \in \{0, 1, \dots, n\}. $$
There are two pieces, and each earns its place.

**The probability of one specific pattern, $p^k (1-p)^{n-k}$.** Fix a particular sequence of $n$ outcomes that contains exactly $k$ successes and $n - k$ failures — say, for $n = 3$, the sequence success-success-failure. Because the trials are independent, the probability of that exact sequence is the product of the per-trial probabilities: $p$ for each of the $k$ successes and $(1-p)$ for each of the $n - k$ failures, i.e. $p \cdot p \cdots (1-p) = p^{k}(1-p)^{n-k}$. Crucially, *every* sequence with the same count $k$ has this *same* probability, because multiplication does not care about the order of the factors.

**The count of such patterns, $\binom{n}{k}$.** But success-success-failure is not the only way to get 2 successes in 3 trials; so are success-failure-success and failure-success-success. The count $K = k$ does not pin down *which* trials succeeded — it lumps together all sequences that share the same number of successes. The symbol $\binom{n}{k}$, read "$n$ choose $k$," is exactly **the number of distinct ways to choose which $k$ of the $n$ trials are the successes**. Since each of those equally-likely patterns has probability $p^k(1-p)^{n-k}$, and they are mutually exclusive ways to reach the count $k$, we *add* them — which, being all equal, means multiplying one pattern's probability by how many patterns there are. That product is the binomial pmf. The Bernoulli per-trial formula $p^x(1-p)^{1-x}$ is the seed; the binomial is that seed multiplied out across $n$ trials and then grouped by total count.

### Worked instance: $\mathrm{Binomial}(n = 3,\ p = 0.3)$

Three independent flips of the $p = 0.3$ coin; $K$ = number of heads. The support is $\{0, 1, 2, 3\}$. We need the four "choose" counts. $\binom{3}{0} = 1$ (one way to pick zero successes: all fail), $\binom{3}{1} = 3$ (the lone success can be any of the 3 trials), $\binom{3}{2} = 3$ (equivalently, pick which single trial *fails*), $\binom{3}{3} = 1$ (all succeed).

Now each probability, deriving every number:
$$ P(K = 0) = \binom{3}{0}\,0.3^{0}\,0.7^{3} = 1 \cdot 1 \cdot 0.343 = 0.343, $$
$$ P(K = 1) = \binom{3}{1}\,0.3^{1}\,0.7^{2} = 3 \cdot 0.3 \cdot 0.49 = 3 \cdot 0.147 = 0.441, $$
$$ P(K = 2) = \binom{3}{2}\,0.3^{2}\,0.7^{1} = 3 \cdot 0.09 \cdot 0.7 = 3 \cdot 0.063 = 0.189, $$
$$ P(K = 3) = \binom{3}{3}\,0.3^{3}\,0.7^{0} = 1 \cdot 0.027 \cdot 1 = 0.027. $$
(Here $0.7^3 = 0.7 \times 0.7 \times 0.7 = 0.343$, $0.7^2 = 0.49$, $0.3^2 = 0.09$, $0.3^3 = 0.027$.)

So getting exactly 2 heads in 3 flips of this coin has probability $\mathbf{0.189}$ — under 1 in 5, which is sensible since this coin disfavors heads. The single most likely count is $1$ (probability $0.441$), clustered near the mean number of successes $n p = 3 \times 0.3 = 0.9 \approx 1$.

**Normalization check — the $n + 1 = 4$ masses must sum to 1**, since $K$ is certain to take *some* count in $\{0,1,2,3\}$:
$$ 0.343 + 0.441 + 0.189 + 0.027 = 1.000. \checkmark $$
The total is exactly 1, confirming this is a valid [[probability-distribution]] over the four possible counts. Notice the roles of the two binomial pieces in the numbers: the middle counts $k = 1, 2$ get a $\times 3$ boost from $\binom{3}{k}$ (many patterns reach them), while the extreme counts $k = 0, 3$ get only $\times 1$ (a single all-fail or all-succeed pattern). The "choose" factor is what gives the binomial its characteristic bulge in the middle.

### Why this matters

The Bernoulli distribution is the atom of yes/no randomness, and the binomial is what you get by counting atoms. Together they are the standard model for "I ran a fixed number of independent yes/no trials and counted the successes": coin flips, click-through rates, defect counts, poll responses. Because the binomial pmf is built from a clean formula in $p$, it is the launching point for estimating an unknown success probability from observed counts — the bridge from these distributions to statistical inference.

## Prerequisites

- [[probability-distribution]]

## Sources

_none_
