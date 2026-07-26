---
id: full-bayesian-inference
title: Full Bayesian Inference
summary: Full Bayesian inference is the choice to keep the entire posterior distribution P(θ | D) that bayes-rule produces, instead of crushing it down to a single representative number.
type: concept
tags: [math/probability]
prereqs: [bayes-rule, likelihood]
sources: [study-notes.html]
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# Full Bayesian Inference

## Summary

Full Bayesian inference is the choice to **keep the entire posterior distribution** `P(θ | D)` that [[bayes-rule]] produces, instead of crushing it down to a single representative number. Recall that [[bayes-rule]] turns a prior belief `P(θ)` about an unknown quantity `θ` and the [[likelihood]] `P(D | θ)` of the observed data `D` into a whole *distribution* over `θ` — a curve assigning a probability (or probability density) to every candidate value. Cheaper methods discard that curve: maximum-likelihood estimation (MLE) ignores the prior and reports the single `θ` under which the data is most probable; maximum-a-posteriori estimation (MAP) keeps the prior but still reports only the single highest *peak* of the posterior. Both hand back a lone point and throw the rest of the curve — its spread, its shape, its tails — away. Full Bayes refuses that collapse. By retaining the full distribution it can report not just a best guess but an honest measure of how *uncertain* that guess is (a **credible interval**, a range that holds a stated share of the posterior probability), and it can make predictions by **averaging over every value of `θ` weighted by its posterior probability** rather than betting everything on one value. The cost is that you carry a whole distribution instead of a number; the payoff is uncertainty you can quote and predictions that hedge across possibilities. As data accumulates the posterior concentrates and the prior washes out, so all three methods converge — the difference between them matters most precisely when data is scarce.

## Grounded explanation

### The starting point: [[bayes-rule]] hands you a whole distribution

From [[bayes-rule]], inference about an unknown quantity `θ` (the "parameter" — the thing we want to learn, such as a coin's bias) given observed data `D` yields the **posterior**

> `P(θ | D) = P(D | θ) · P(θ) / P(D)`,  i.e.  `P(θ | D) ∝ P(D | θ) · P(θ)`,

where `P(θ)` is the **prior** (belief before data), `P(D | θ)` is the [[likelihood]] (how probable the data is if `θ` were the true value — a function of the parameter with the data held fixed, as established in [[likelihood]]), and `P(D)` is the normalizing **evidence** that makes the result sum or integrate to 1. The crucial fact, established in [[bayes-rule]], is that the posterior `P(θ | D)` is not a number — it is a *distribution*, a function that assigns a value to **every** candidate `θ`. It has a location (where its mass sits), a spread (how widely belief is spread across values), and a shape (whether it is symmetric, skewed, or has heavy tails). The whole question of this node is: once [[bayes-rule]] hands you this rich object, how much of it do you keep?

### The estimation hierarchy: three levels of how much you keep

A **point estimate** is a single chosen value of `θ` offered as "the answer" — one number standing in for the whole distribution. There is a hierarchy of three methods, all starting from the *same* modelled likelihood `P(D | θ)`, differing only in how much of the prior and posterior they use:

- **MLE (maximum-likelihood estimation)** — uses **no prior**. It returns the single `θ` that maximizes the likelihood alone: the value under which the observed data would have been most probable. Formally the `θ` achieving the largest `P(D | θ)`. Output: a point.
- **MAP (maximum-a-posteriori estimation)** — uses a prior, but still returns a point. It maximizes `P(D | θ) · P(θ)` — likelihood times prior, which by [[bayes-rule]] is the (unnormalized) posterior — and returns the location of its single highest peak. The peak of a distribution is its **mode**, the most probable value. So MAP reports the posterior's mode. Output: still a point.
- **Full Bayes** — uses a prior and keeps the **entire posterior distribution** `P(θ | D)`. Output: the whole distribution, not a point.

MLE and MAP both *collapse* the posterior to one number — MLE by ignoring the prior and peaking the likelihood, MAP by peaking the full posterior. Full Bayes performs no collapse. That is the single defining move of this concept: **do not reduce `P(θ | D)` to a point; carry it whole.**

### Why keep the whole thing — what a point estimate throws away

A point estimate answers "which `θ`?" but is silent on "how sure are we?" Two posteriors can share the *same* peak yet describe completely different states of knowledge: one a tall narrow spike (the data has pinned `θ` down tightly), the other a low broad mound (`θ` could plausibly be many values). MAP reports the *same* mode for both and so reports the same answer for two situations that are not at all the same. The information distinguishing them — the **spread** — lives in the part of the curve the point estimate discarded. Full Bayes keeps it, and this buys two concrete things a point cannot give.

**First, a credible interval — honest uncertainty.** Because the posterior is a genuine distribution that integrates to 1, you can find a range of `θ` values that together hold, say, 95% of the posterior probability. That range is a **95% credible interval**: a direct statement that, given the data and prior, there is a 95% probability the true `θ` lies inside it. A point estimate cannot say this — a single value has no width — but the full posterior can, simply by reading off where 95% of its area sits. A narrow interval means the data pinned `θ` down; a wide one is an honest admission that it did not.

**Second, prediction by averaging instead of betting.** Suppose we want the probability of some *new* observation — call it `new` — given the data we have already seen. A point estimate forces a bet: plug the single chosen `θ` into the likelihood and predict `P(new | θ̂)`, ignoring that `θ̂` might be wrong. Full Bayes instead consults *every* value of `θ`, asks each one for its prediction `P(new | θ)`, and **averages those predictions, weighting each by how much posterior probability that `θ` carries**. This weighted average is the **posterior predictive distribution**:

> `P(new | D) = ∫ P(new | θ) · P(θ | D) dθ`

(a sum rather than an integral when `θ` takes discrete values). The integral sign `∫ … dθ` here *is* the averaging: it sweeps `θ` across all its values, multiplies each value's prediction `P(new | θ)` by that value's posterior weight `P(θ | D)`, and accumulates the total. Eliminating `θ` from the answer this way — summing it out against its posterior — is called **marginalizing** over `θ`. The justification is exactly the law of total probability that [[bayes-rule]] already used to build its normalizer `P(D)`: the probability of `new` is the sum over all the disjoint ways it can happen (one way per value of `θ`), each weighted by that value's probability. The effect is that uncertainty in `θ` is carried *forward* into the prediction: when the posterior is broad, the predictions of its many plausible `θ` values disagree and the averaged forecast is appropriately hedged; a point estimate, having thrown the breadth away, would have reported a falsely confident single forecast.

### The non-obvious step made plain

The one move that can look like magic is the posterior predictive integral — "why integrate the parameter away rather than just use its best value?" The answer is that `θ` is not a fixed known quantity but an unknown one we have only a *distribution* over. To honestly predict `new` we must account for *every* value `θ` might take, in proportion to how credible the data made it. Averaging `P(new | θ)` against the weights `P(θ | D)` does exactly that; picking one `θ` and ignoring the rest pretends to a certainty we do not have. The integral is not extra machinery — it is the refusal to throw the posterior away, applied to prediction.

### Worked instance: a coin, MLE vs MAP vs full Bayes

Take a coin with unknown bias `p` (the probability it lands heads — here `p` plays the role of `θ`). We flip it and observe `h = 8` heads and `t = 2` tails, so the data is `D = (8 heads, 2 tails)`. Because the flips are independent, the likelihood is `P(D | p) = p^h · (1−p)^t = p^8 (1−p)^2`.

Choose for the prior a **Beta distribution**, `Beta(α, β)`, whose density is proportional to `p^(α−1) (1−p)^(β−1)`. Its two parameters `α` and `β` act like *pseudo-counts* — heads and tails imagined before any real data — so it expresses a prior belief about `p` in the same currency as the data. Take a mild `Beta(2, 2)` prior: `α = 2`, `β = 2`, i.e. one pretend-head and one pretend-tail, a gentle nudge toward the fair value `p = 0.5`.

Now compare what each method returns.

**MLE — no prior, the likelihood's peak.** Maximizing `p^8 (1−p)^2` gives the observed proportion of heads,

> `p̂_MLE = h / (h + t) = 8 / (8 + 2) = 0.8`.

A single number, `0.8`, with no statement of confidence and no use of the prior.

**MAP — prior included, but still the posterior's peak (its mode).** Multiplying likelihood by the `Beta(2,2)` prior and reading off the mode gives

> `p̂_MAP = (α + h − 1) / (α + β + h + t − 2) = (2 + 8 − 1) / (2 + 2 + 8 + 2 − 2) = 9 / 12 = 0.75`.

Still one number — pulled slightly from `0.8` toward the prior's centre `0.5` by the pseudo-counts, but it again reports only the location of the peak and nothing about the spread.

**Full Bayes — keep the whole posterior.** By [[bayes-rule]], the posterior is proportional to likelihood times prior:

> `P(p | D) ∝ p^8 (1−p)^2 · p^(2−1) (1−p)^(2−1) = p^(8+2−1) (1−p)^(2+2−1) = p^9 (1−p)^3`.

That is again a Beta density — specifically `Beta(α + h, β + t) = Beta(2 + 8, 2 + 2) = Beta(10, 4)` — obtained simply by adding the data counts to the prior's pseudo-counts. (The neat fact that a Beta prior yields a Beta posterior is incidental here; what matters is that the *entire* distribution is retained.) Full Bayes does not collapse `Beta(10, 4)` to a point. From the whole curve it can report:

- The **posterior mean**, `(α + h) / (α + β + h + t) = (2 + 8) / (2 + 2 + 8 + 2) = 10 / 14 ≈ 0.714`. This is the *average* value of `p` under the posterior — a different summary from the mode `0.75`, because the posterior is skewed; a point method must pick one summary, but full Bayes is not obliged to choose.
- A **95% credible interval** — the range of `p` capturing 95% of the area under `Beta(10, 4)`. That curve sits mostly between roughly `0.45` and `0.90`, so a positive but clearly uncertain estimate; the interval *quantifies* how far the data has — and has not — pinned the bias down. Neither `0.8` nor `0.75` could say this.
- A **posterior predictive** for the next flip: averaging `P(next = heads | p) = p` over the posterior is just the posterior mean of `p`, `≈ 0.714` — so the probability the next toss is heads, having marginalized over our uncertainty about `p`, is about `0.714`, automatically hedged below the raw MLE `0.8` because the breadth of the posterior is folded in.

So from identical data the three methods return progressively richer answers: MLE `0.8` (a point, no prior, no uncertainty); MAP `0.75` (a point, prior included, still no uncertainty); full Bayes the whole `Beta(10, 4)` (a mean of about `0.714`, a credible interval, and hedged predictions). Note the convergence the hierarchy promises: with only ten flips the prior visibly shifts the answer, but if we observed `800` heads and `200` tails the added pseudo-counts `2` and `2` would be negligible, the posterior would spike narrowly near `0.8`, its mode and mean and the MLE would nearly coincide, and the credible interval would shrink toward a point — the prior washes out and the three methods agree. The gap between them is largest exactly when data is scarce, which is when keeping the uncertainty matters most.

### Layered priors as a natural extension

The same keep-the-distribution logic extends one level up. In the coin example the prior's pseudo-counts `α` and `β` were *fixed inputs* we chose by hand. One can instead treat those prior parameters as themselves uncertain and place a further prior on *them* — a prior over priors — and infer the whole stack jointly; this is hierarchical-bayes, useful when many related quantities share a common but unknown prior. A pragmatic shortcut, **empirical Bayes**, instead *estimates* those prior parameters from the data itself (typically by maximizing the evidence `P(D)`) and then proceeds as usual — trading some Bayesian purity for convenience. Both are variations on the same theme of this node: decide how much of the relevant distribution to keep versus collapse, here applied to the prior's own parameters rather than to `θ`.

## Prerequisites

- [[bayes-rule]]
- [[likelihood]]
## Sources

- `etc/study-notes.html` — §2 estimation-hierarchy panel ("MLE and MAP both collapse the parameter to a single number; full Bayesian inference keeps the entire posterior distribution"), the MLE/MAP coin worked examples, and §3 Beta–Bernoulli posterior `Beta(α+h, β+t)`.
