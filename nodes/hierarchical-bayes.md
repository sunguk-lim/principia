---
id: hierarchical-bayes
title: Hierarchical Bayes
summary: Plain bayes-rule turns a prior belief about an unknown θ into a posterior by reweighting it with the data — but it assumes you already fixed the prior.
type: concept
tags: [math/probability]
prereqs: [bayes-rule, beta-distribution, likelihood]
sources: [study-notes.html §3]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Hierarchical Bayes

## Summary

Plain [[bayes-rule]] turns a prior belief about an unknown `θ` into a posterior by reweighting it with the data — but it assumes you already *fixed* the prior. Often the prior itself has knobs (its **hyper-parameters**) you are unsure about. The tempting fix — peek at the data, tune those knobs to match, then update with the same data — is circular "double-dipping": you spend the data twice and end up overconfident. Hierarchical Bayes is the disciplined alternative: instead of hand-setting the prior's knobs, you treat them as *additional unknowns*, put a further distribution on them (a **hyper-prior**), and infer everything *jointly* with one application of [[bayes-rule]] over the enlarged unknown — the main parameter and the hyper-parameters together. The result is a single coherent posterior in which the data informs the prior through the proper inference machinery rather than by hand, with uncertainty about each level honestly carried into the next. Its signature payoff is **partial pooling**: when many related groups share one hyper-prior, each group's estimate borrows strength from the others, so a data-starved group is pulled toward the shared population pattern instead of trusting its own noisy handful of observations.

## Grounded explanation

### The gap in flat Bayes: who chose the prior's knobs?

Recall the inference form of [[bayes-rule]]: for an unknown `θ` and observed data `D`,

> `P(θ | D) ∝ P(D | θ) · P(θ)` — **posterior ∝ likelihood × prior**,

with the omitted denominator just renormalizing the result to sum to 1. To run this you must supply a concrete prior `P(θ)`, the distribution over `θ` *before* the data.

A prior is rarely a single curve; it is usually a *named shape with adjustable parameters*. Take the running case: `θ` is the bias `p` of a coin — the probability it lands heads, a number in `(0,1)`. A natural prior over a probability is the **[[beta-distribution]]**, written `Beta(α, β)`. It is just the family of curves

> `Beta(α, β) ∝ p^(α−1) · (1−p)^(β−1)`,

shaped by two positive numbers `α` and `β`. The intuition: `α` acts like a count of heads you "imagine having already seen" and `β` like a count of imagined tails, before any real flips. Large `α` relative to `β` puts the prior's mass near `p = 1` (you expect a heads-leaning coin); equal `α = β` centers it at `p = ½`; `α = β = 1` is flat (every bias equally likely). The pair `(α, β)` are the prior's **hyper-parameters** — "hyper" because they sit one level *above* the parameter `p` we ultimately care about: they are parameters *of the prior on* `p`, not of the data directly.

Here is the gap. Flat Bayes simply *assumes* you pinned down `(α, β)`. But where did those numbers come from? If you genuinely do not know the coin and have no imagined counts to offer, any choice is a guess, and a confident wrong guess biases everything downstream.

### Why you must not just read the knobs off the data

The seductive shortcut is to let the data choose `(α, β)`: collect the flips, find the `(α, β)` whose prior best matches what you saw, lock those in, then apply [[bayes-rule]] to get the posterior on `p`. This is **double-dipping**, and it is incoherent. The data is used *twice* — once to manufacture the prior, then again as the "fresh" evidence the prior is updated by. But [[bayes-rule]] is only valid when the prior is what you believed *before* the data; a prior secretly built *from* that same data is no longer a genuine prior. The cost is concrete: the posterior comes out **overconfident** — narrower than the evidence warrants — because the uncertainty you had about `(α, β)` was quietly thrown away the moment you replaced the unknown knobs with single fitted numbers. (This plug-in shortcut has a name, *empirical Bayes*; more on it below.)

### The fix: promote the knobs to unknowns and apply Bayes' rule once, jointly

Hierarchical Bayes refuses to hand-pick `(α, β)`. Instead it admits the honest truth — `(α, β)` are *also* unknown — and treats them exactly the way [[bayes-rule]] treats any unknown: as quantities to be inferred from data, equipped with their own prior. That extra prior, the distribution over the hyper-parameters, is the **hyper-prior**, `P(α, β)`. It expresses your *vague* beliefs about the knobs (e.g. "they are positive, probably modest in size") without committing to exact values.

Now build one enlarged unknown out of *all* the things you do not know — here `(p, α, β)` — and apply [[bayes-rule]] to that whole bundle at once. The [[likelihood]] `P(D | p)` (how probable the observed flips are given the coin's bias) and the two stacked prior factors combine:

> `P(p, α, β | D) ∝ P(D | p) · P(p | α, β) · P(α, β)`.

Read the right side as a chain of dependence, top down: the hyper-prior `P(α, β)` says what the knobs might be; given knobs, `P(p | α, β) = Beta(α, β)` says what the bias might be; given the bias, `P(D | p)` says what data we'd expect. This is **one** posterior, over the *joint* of every level. The same single move of [[bayes-rule]] — posterior ∝ likelihood × prior — is applied, only with "the prior" now being the full layered product `P(p | α, β) · P(α, β)`, and "the unknown" now the whole tuple `(p, α, β)`.

That single change resolves the double-dipping. Nothing is fitted-then-frozen; the data flows through [[bayes-rule]] exactly once, and it simultaneously sharpens our belief about `p` *and* about `(α, β)`. The data **does** inform the prior — but coherently, as a byproduct of one legitimate update, not by a separate hand-tuning pass. And because `(α, β)` remain *distributions* in the posterior rather than fixed numbers, the leftover uncertainty about the knobs is carried honestly into the uncertainty about `p`, instead of being discarded — which is precisely the overconfidence the shortcut suffered.

To answer a question purely about the coin's bias, you collapse the joint posterior down to `p` alone by *summing out* the knobs over all their possible values — `P(p | D) = ∫ P(p, α, β | D) dα dβ` — so the reported uncertainty in `p` already includes the spread you had over `(α, β)`.

### Why this is worth the extra layer: partial pooling and shrinkage

The extra layer earns its keep most visibly when there is not one coin but *many related groups* sharing structure. Suppose you have a whole box of coins — coin 1, coin 2, …, coin K — each with its own unknown bias `p₁, …, p_K`, and you flip each some number of times. Two naive extremes are both bad:

- **No pooling** — estimate each `pₖ` from only its own flips. A coin flipped just twice gives a wild estimate (two heads ⇒ "bias = 1.0"), trusting a tiny sample completely.
- **Complete pooling** — lump every flip together and assume all coins share one bias. This ignores that the coins genuinely differ.

Hierarchical Bayes threads between them. Let *all* the biases share **one common hyper-prior** `Beta(α, β)` — i.e. each `pₖ` is drawn from the same `Beta(α, β)`, whose `(α, β)` are themselves unknown and inferred from *all* the coins at once. The joint posterior is now

> `P(p₁,…,p_K, α, β | D) ∝ [∏ₖ P(Dₖ | pₖ) · P(pₖ | α, β)] · P(α, β)`,

where `Dₖ` is coin `k`'s flips. Because the shared `(α, β)` are learned from the *pooled* evidence of every coin, they encode "what biases coins in this box tend to have" — the population pattern. Each individual `pₖ` is then pulled partway from its own noisy sample toward that learned population center. This is **partial pooling** (each coin borrows strength from the others through the shared layer) and the pull itself is called **shrinkage** — estimates are *shrunk* toward the common mean. Crucially the pull is *adaptive*: a coin with hundreds of flips has a strong likelihood `P(Dₖ | pₖ)` that resists the pull and stays near its own data; a coin with two flips has a weak likelihood and is pulled hard toward the population mean, exactly where its own scant data should *not* be trusted. The "double-dip" worry never arises because `(α, β)` are inferred jointly with the `pₖ`'s in one coherent posterior — the data informs the shared prior legitimately.

### Worked instance: three coins, one of them data-starved

Take three coins sharing an unknown `Beta(α, β)`. Their flip records:

- coin 1: `80` heads, `20` tails (100 flips) — its own data points to bias near `0.80`;
- coin 2: `40` heads, `60` tails (100 flips) — its own data points to bias near `0.40`;
- coin 3: `2` heads, `0` tails (2 flips) — its own data alone says bias `= 1.0`.

Run the joint inference. The shared `(α, β)` are learned from all three coins; the well-sampled coins 1 and 2 dominate that learning because their likelihoods are sharp, so the inferred population settles around a mean bias of roughly `0.6` with moderate spread — say the posterior favors `(α, β)` near `(3, 2)`, whose mean `α/(α+β) = 3/5 = 0.60`. These act as pseudo-counts: about 3 imagined heads and 2 imagined tails added to each coin.

Now read off each coin's shrunk estimate as the posterior mean `(α + hₖ) / (α + β + hₖ + tₖ)`, using `(α, β) = (3, 2)`:

- coin 1: `(3 + 80) / (5 + 100) = 83 / 105 ≈ 0.79` — barely moved from its own `0.80`; 100 flips swamp the 5 pseudo-counts.
- coin 2: `(3 + 40) / (5 + 100) = 43 / 105 ≈ 0.41` — likewise barely moved from `0.40`.
- coin 3: `(3 + 2) / (5 + 2) = 5 / 7 ≈ 0.71` — pulled sharply down from the absurd `1.0` toward the population mean `0.60`, because its 2 flips cannot resist the 5 shared pseudo-counts.

That last line is the whole point. No-pooling would have reported coin 3 as a certain `1.0` on the strength of two flips; complete-pooling would have forced it (and everyone) to the single lumped average, erasing coins 1 and 2's real difference. Hierarchical Bayes does neither: it lets the two well-measured coins teach the shared prior, then lends that knowledge to the third — a `0.71` that is honestly uncertain and far more sensible than `1.0`. And `(α, β)` were never hand-set; they fell out of the same joint posterior, so no data was spent twice.

### Contrast: empirical Bayes, the plug-in shortcut

There is a popular middle road called **empirical Bayes** that is worth naming precisely so it is not confused with the genuine article. Empirical Bayes estimates the hyper-parameters `(α, β)` *from the data* — typically the single `(α, β)` that maximizes the probability of the observed data after `p` has been summed out (the "marginal likelihood") — and then **plugs those fixed numbers in** as if they had been the prior all along, running ordinary [[bayes-rule]] on `p` from there. It is genuinely useful and often gives similar point estimates, partly because it too produces shrinkage. But it is exactly the double-dip described earlier dressed up: the data sets the prior, then the same data updates it, and the uncertainty about `(α, β)` is collapsed to a point estimate. So empirical-Bayes posteriors tend to come out **overconfident** — too narrow. Hierarchical Bayes differs in one decisive respect: it keeps `(α, β)` as a *distribution* inside one joint posterior and never freezes them, so the uncertainty at the upper level propagates down to `p`. Empirical Bayes is the plug-in approximation; hierarchical Bayes is the coherent original it approximates.

## Prerequisites

- [[bayes-rule]]

## Sources

- `study-notes.html` §3 — "Letting the data inform the prior, properly": hierarchical Bayes places a hyper-prior on `(α, β)` and infers them jointly with `p`; empirical Bayes as the plug-in shortcut that "spends the data twice."
