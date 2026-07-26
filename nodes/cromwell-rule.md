---
id: cromwell-rule
title: Cromwell's Rule
summary: "Cromwell's rule is a discipline on how you choose a prior in bayes-rule: never assign a prior probability of exactly 0 (or exactly 1) to any proposition that is not logically…"
type: concept
tags: [math/probability]
prereqs: [bayes-rule]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Cromwell's Rule

## Summary

Cromwell's rule is a discipline on how you choose a prior in [[bayes-rule]]: **never assign a prior probability of exactly 0 (or exactly 1) to any proposition that is not logically certain.** The reason follows directly from the rule's own arithmetic. [[bayes-rule]] says the posterior is proportional to likelihood times prior, `posterior ∝ likelihood × prior`. So wherever the prior is exactly 0, the posterior there is `likelihood × 0 = 0` — and it stays 0 no matter what data later arrives, because every update only ever *multiplies* by a new likelihood factor, and any product with 0 is 0. A prior that rules a possibility out with probability 0 (or in, with probability 1) is called **dogmatic**: it can never be revised by evidence. This matters because of a normally reassuring fact — a merely *wrong* (but non-dogmatic) prior gets washed out as data accumulates, so the posterior eventually concentrates on the truth regardless of where it started. The dogmatic prior is the one exception that breaks this self-correction. The practical fix is to use a prior that is strictly positive everywhere a value is even conceivable, so no possibility is pre-condemned to 0.

## Grounded explanation

### What the rule is

A **prior**, in [[bayes-rule]], is the probability you assign to each possible value of an unknown quantity `θ` *before* you see any data. Cromwell's rule is a constraint on that choice. It says: for any value of `θ` that is genuinely *possible* — anything not ruled out by pure logic — your prior must give it a probability strictly greater than 0 and strictly less than 1. Equivalently, reserve the extreme values 0 and 1 only for propositions that are *logically certain* (true or false by definition, like "a thing equals itself"), never for empirical claims about the world. A prior that violates this — one that hands some live possibility a flat 0 (or a flat 1) — is called a **dogmatic** prior.

### Why a 0 in the prior is permanent — the WHY from [[bayes-rule]]

The danger comes straight from the update formula. [[bayes-rule]] gives the **posterior** (belief after data) as

> `posterior ∝ likelihood × prior`,

that is, for each candidate value of `θ` the new belief `P(θ | D)` is the **prior** `P(θ)` multiplied by the **likelihood** `P(D | θ)` (how well that `θ` predicted the observed data `D`), up to a fixed rescaling that does not depend on `θ`. Read this one value at a time. For a value `θ₀` where the prior is `P(θ₀) = 0`, the posterior is

> `P(θ₀ | D) ∝ P(D | θ₀) × 0 = 0`,

and this holds **for every possible dataset `D`**, because the likelihood `P(D | θ₀)` is just *some number* being multiplied by 0. Multiplying any finite number by 0 yields 0. So the posterior at `θ₀` is 0, and if you keep collecting data — feeding each new posterior back in as the prior for the next round — you keep multiplying that 0 by fresh likelihood factors, and it stays 0 indefinitely. **No amount of evidence can resurrect a possibility the prior set to 0.** The symmetric case, a prior of 1 on one value, forces every *other* value to prior 0 (probabilities sum to 1), which freezes those competitors at 0 forever in the same way. That permanence is what makes a dogmatic prior fatal: it is not a belief that data can correct, but a belief data cannot touch.

### The one exception to self-correction

Why single this out? Because in the *non*-dogmatic case [[bayes-rule]] is forgiving. Suppose your prior is simply *wrong* — it leans toward the wrong answer — but still assigns every possibility some positive probability. As data accumulates, the likelihood `P(D | θ)` is recomputed over more and more observations, so its pull grows with the amount of data, while the prior is a fixed factor that does not grow. The repeated reweighting therefore drags the posterior toward whichever `θ` actually predicts the data best, and the influence of the starting prior fades away. The posterior concentrates on the truth *regardless of where the prior began* — a wrong prior only slows early learning, it cannot mislead in the long run. This benign behavior relies on one thing: the truth must have started with *positive* prior probability, so that the reweighting has something nonzero to amplify. A dogmatic prior is precisely the case where that condition fails. It is the single exception that converts "a wrong prior gets corrected" into "a wrong prior can never be corrected."

### Worked instance: a coin you are certain favors tails

Let `θ = p`, the unknown probability that a coin lands heads on a single flip; `p` can in principle be any value in the interval from 0 to 1. Suppose you adopt a **dogmatic** prior: you are *certain* the coin favors tails, so you assign prior probability 0 to the entire range `p ≥ 0.5` and spread all your prior probability over `p < 0.5`. In symbols, `P(p ≥ 0.5) = 0`.

Now run an experiment that screams the opposite: flip the coin 100 times and observe **100 heads**. Intuitively this is overwhelming evidence that `p` is near 1. Apply [[bayes-rule]] value by value. For any `p ≥ 0.5`, the posterior is

> `P(p | 100 heads) ∝ P(100 heads | p) × P(p) = P(100 heads | p) × 0 = 0`.

Even though the likelihood `P(100 heads | p)` is *enormous* near `p = 1` (a heads-favoring coin makes 100 straight heads very plausible), it is being multiplied by a prior of 0. The product is 0 across the whole region `p ≥ 0.5`. So the posterior still places **zero** probability on the coin favoring heads — after 100 heads in a row. The data is helpless; the dogmatic prior has permanently sealed off the true region.

Contrast a non-dogmatic prior on the same data. Take the uniform prior, often written `Beta(1, 1)`, which assigns *equal positive density* to every value of `p` in the open interval `(0, 1)` — no value is set to 0. Now nothing is pre-condemned. The same 100-heads likelihood, peaking sharply near `p = 1`, reweights this prior and the posterior collapses toward `p ≈ 1`, exactly as common sense demands. The only difference between the two runs is whether the truth started with positive prior probability.

### The fix

The remedy is the direct converse of the failure: choose a prior that is **strictly positive everywhere a value is even plausible**, so the reweighting in [[bayes-rule]] always has a nonzero quantity to act on. For a probability `p` ranging over `(0, 1)`, a `Beta(α, β)` prior with both shape parameters `α > 0` and `β > 0` is positive across the *entire* open interval — it never hits 0 in the interior — and is therefore "safe" by Cromwell's rule: every possibility retains a foothold that data can later amplify or shrink. (The uniform `Beta(1, 1)` above is the special case `α = β = 1`.) The rule of thumb, then: keep your prior away from the hard 0 and the hard 1 unless logic itself forces them, and let the data — not a dogmatic assumption — decide what is impossible.

## Prerequisites

- [[bayes-rule]]

## Sources

_none_
