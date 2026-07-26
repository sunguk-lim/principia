---
id: empirical-bayes
title: Empirical Bayes
summary: Empirical Bayes is a shortcut for choosing the prior in bayes-rule.
type: concept
tags: [math/probability]
prereqs: [bayes-rule, likelihood]
sources: [study-notes.html §3]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Empirical Bayes

## Summary

Empirical Bayes is a shortcut for choosing the prior in [[bayes-rule]]. Recall that the rule combines a *prior* — a distribution over the unknown quantity before seeing data — with the *likelihood* of the data to produce the *posterior*, the updated belief. But the prior itself is usually written with a few knobs called **hyper-parameters** (for a coin's bias, the prior `Beta(α, β)` has knobs `α` and `β`), and someone must fix their values. The fully principled answer is to treat the hyper-parameters as *also* uncertain and infer them — a hierarchical model — but that is expensive. Empirical Bayes instead **estimates the hyper-parameters directly from the data**, typically by maximizing the **marginal likelihood** `P(D | α, β)` — the probability the prior assigns to the data after averaging over every possible value of the unknown — and then **plugs those single best values into the prior** and runs [[bayes-rule]] as usual. It is cheap and often works well. The catch, and the source's warning, is that it **spends the data twice**: once to set the prior, again to update it. That double use is not paid for, so the posteriors come out **overconfident** — their uncertainty is understated.

## Grounded explanation

### Where the difficulty starts: the prior has knobs nobody set

In [[bayes-rule]] the answer is `posterior ∝ likelihood × prior`: a belief about an unknown quantity `θ` is the prior `P(θ)` reweighted by how well each value of `θ` predicted the observed data `D`, via the [[likelihood]] `P(D | θ)` — the same expression read as a function of the parameter `θ` rather than of the data. To actually run the rule you must commit to a specific prior. Priors are rarely written as bare numbers; they come as a *family* governed by a few control values. The source's running example is a coin whose unknown bias `p` (its probability of heads) is given a `Beta(α, β)` prior — a distribution on the interval from 0 to 1 shaped by two positive numbers `α` and `β` that act like pseudo-counts of heads and tails "seen" before any real flip. These shape-controlling numbers are the **hyper-parameters** (the prefix *hyper-* meaning they sit one level above the ordinary unknown `p`: `p` is what we infer, `α` and `β` say what we believed about `p` in advance).

So a question sits underneath [[bayes-rule]] that the rule itself does not answer: *what should `α` and `β` be?* If you pick them carelessly the prior may fight the data; if you pick them by peeking at the data you risk circular reasoning. Empirical Bayes is one disciplined way to answer this question.

### The honest baseline it is a shortcut for: hierarchical Bayes

To see why Empirical Bayes is called a *shortcut*, first picture the thorough alternative, **hierarchical Bayes**. Here you refuse to commit to fixed hyper-parameters and instead admit you are uncertain about `α` and `β` too. You place a further prior — a **hyper-prior** — over the hyper-parameters, and then infer `α`, `β` and `p` *together* in one application of [[bayes-rule]] over the whole collection of unknowns. The data flows up through this stack and informs the prior through a single coherent posterior. Because `α` and `β` are never frozen — they stay uncertain throughout — that uncertainty is carried into the final answer: the intervals you report on `p` come out appropriately wide. The price is that you now have to do the harder, more expensive inference over an enlarged set of unknowns, which often has no clean closed form. Hierarchical Bayes is the honest baseline; Empirical Bayes trades some of that honesty for speed.

### The mechanism: maximize the marginal likelihood, then plug in

Empirical Bayes makes the cheap move. Instead of staying uncertain about `α` and `β`, it picks one *best* pair of values and freezes them. The criterion for "best" is the **marginal likelihood** — the probability the prior assigns to the data once the unknown `p` has been averaged out. For a single setting of the hyper-parameters it is

> `P(D | α, β) = ∫ P(D | p) · P(p | α, β) dp`,

read as follows. `P(D | p)` is the ordinary likelihood: how probable the data `D` is if the bias were exactly `p`. `P(p | α, β)` is the prior on `p` controlled by the hyper-parameters. Their product is summed over every possible `p` (the integral sign `∫ … dp` means "add up across all values of `p`, weighting by each"). The result `P(D | α, β)` no longer mentions `p` at all — `p` has been *marginalized away*, which is what "marginal" means — leaving a number that scores the hyper-parameters alone: *how well does the prior `Beta(α, β)`, as a whole, predict the data we actually saw?*

The estimate is the pair that scores highest:

> `(α̂, β̂) = argmax over (α, β) of P(D | α, β)`,

where the hat in `α̂` (read "alpha-hat") marks an estimated value and `argmax` means "the argument that maximizes" — the `(α, β)` at which the marginal likelihood peaks. Having found `(α̂, β̂)`, Empirical Bayes **plugs them in**: it treats `Beta(α̂, β̂)` as if it were the prior all along, and runs [[bayes-rule]] in the ordinary way, `posterior ∝ likelihood × prior`, to update each coin. The whole second stage is just plain [[bayes-rule]] — the only novelty is *how the prior was chosen*.

### Why it works, and the one flaw: spending the data twice

The reason this is appealing: maximizing the marginal likelihood lets the data set the prior to something reasonable rather than a hand-guessed value, and it is far cheaper than carrying a hyper-prior and inferring everything at once. In many problems the plugged-in prior is close to what the full hierarchical model would have found, so the point estimates of `p` are good.

The flaw is exactly the source's phrase: Empirical Bayes **spends the data twice**. The same dataset `D` is used *first* to choose the hyper-parameters `(α̂, β̂)`, and *then again* to update the prior into a posterior. Standard [[bayes-rule]] is honest because the prior is fixed *before* the data is consulted — the data enters only once, through the likelihood. Empirical Bayes breaks that separation. By picking the hyper-parameters that best fit the data, the prior is already pulled toward the data, and then the same data is allowed to pull again during the update. This double-counting is never paid for: the procedure acts as if `(α̂, β̂)` were known exactly, when in fact they were only *estimated* and carry their own uncertainty. Throwing that uncertainty away makes the posterior too narrow — its reported confidence is higher than the evidence warrants. Hierarchical Bayes avoids the double-counting precisely because it never freezes `α` and `β`: keeping them uncertain propagates the genuine doubt about the prior into wider, more honest intervals.

### Worked instance: many coins flipped a few times each

The double-counting is harmless when there is little to estimate, so take the source's non-degenerate setting: not one coin but **many coins**, say 200 of them, each flipped only a handful of times — perhaps 10 flips apiece. Each coin `j` has its own unknown bias `p_j`, and we believe the coins are similar — drawn from one shared population — but we do not know the population's shape. That shared shape is the prior `Beta(α, β)`, and `α`, `β` are the hyper-parameters to be set.

Run Empirical Bayes:

1. **Estimate the shared prior from all the coins at once.** Form the marginal likelihood of the *entire* dataset under a candidate `(α, β)`. Because each coin is a separate draw, this is the product over coins of each coin's marginal likelihood, `∏_j P(D_j | α, β)`, where `D_j` is coin `j`'s flip record and each factor `P(D_j | α, β) = ∫ P(D_j | p_j) · P(p_j | α, β) dp_j` integrates out that coin's own bias. Maximizing this product over `(α, β)` finds the population shape `Beta(α̂, β̂)` that best explains the spread of results across all 200 coins. Concretely, if coins land heads about 60% of the time on average with modest spread, the fit might come out near `α̂ ≈ 6`, `β̂ ≈ 4` — a prior centered around 0.6 and worth roughly `α̂ + β̂ = 10` pseudo-flips of prior strength.

2. **Plug it in and update each coin separately.** Now use `Beta(α̂, β̂) = Beta(6, 4)` as the prior for *every* coin and apply [[bayes-rule]] per coin. A coin that came up, say, 8 heads in 10 flips does not get the raw estimate `8/10 = 0.8`; its posterior combines the data counts with the prior pseudo-counts to land near `(α̂ + 8) / (α̂ + β̂ + 10) = (6 + 8) / (10 + 10) = 14/20 = 0.7`. The estimate has been pulled from 0.8 toward the population center 0.6 — this pull is called **shrinkage**, and it is exactly what borrowing strength across the 200 coins buys: each coin, having only 10 flips of its own, leans on what the whole population taught us.

This is where Empirical Bayes shines — with 200 coins informing `(α̂, β̂)`, the hyper-parameters are pinned down well, and treating them as fixed does little harm. But the warning still bites: those same 200 coins were used to *set* `Beta(6, 4)` and then *again* to update each coin, so the per-coin posterior intervals come out a touch too tight.

Contrast the hierarchical version of the *identical* setup. Instead of freezing `Beta(6, 4)`, you put a hyper-prior over `(α, β)` and infer the population shape jointly with all 200 biases. The answer for a coin's center is similar — you still get shrinkage toward roughly 0.6 — but because `(α, β)` remain uncertain rather than pinned at `(6, 4)`, that uncertainty flows into every coin's posterior, yielding **wider, honest intervals**. Same shrinkage, more candid error bars. That difference — overconfident from spending the data twice, versus calibrated from never freezing the prior — is the whole reason to know which method you are using.

## Prerequisites

- [[bayes-rule]]
- [[likelihood]]

## Sources

- study-notes.html — §3, "Letting the data inform the prior, properly" (Hierarchical Bayes vs. Empirical Bayes).
