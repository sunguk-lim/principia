---
id: bayes-rule
title: Bayes' Rule
summary: "Bayes' rule is the formula that inverts a conditional probability: it converts \"how probable is the evidence given the cause?\" into \"how probable is the cause given the evidence?\"…"
type: concept
tags: [math/probability]
prereqs: [probability, probability-distribution, likelihood]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Bayes' Rule

## Summary

Bayes' rule is the formula that *inverts* a conditional probability: it converts "how probable is the evidence given the cause?" into "how probable is the cause given the evidence?" Often we can easily state one direction — a test catches 99% of sick people, `P(positive | sick)` — but what we actually want is the reverse, `P(sick | positive)`, the chance you are sick once your test comes back positive. From the [[probability]] definition of conditional probability, both directions share the same joint probability `P(A ∩ B)`; eliminating that shared term gives `P(A | B) = P(B | A) · P(A) / P(B)`. Written for an unknown quantity `θ` (the cause) and observed data `D` (the evidence), this reads **posterior ∝ likelihood × prior**: the [[probability-distribution]] over `θ` *after* seeing the data equals the prior distribution `P(θ)` reweighted by how well each value of `θ` predicted the data, `P(D | θ)`, then rescaled so the result sums to 1. The rescaling denominator only fixes the overall size, so for the *shape* of the answer it can be ignored — but it is required to recover actual probabilities. The famous lesson is counterintuitive: with a rare disease, even a "99% accurate" test can leave you far more likely healthy than sick.

## Grounded explanation

### The problem: one conditional is easy, the other is what we want

Recall from [[probability]] that the **conditional probability** of event `A` given event `B`, written `P(A | B)`, is the probability that `A` holds once we restrict attention to the trials where `B` held. Its definition is

> `P(A | B) = P(A ∩ B) / P(B)`,  requiring `P(B) > 0`,

where `A ∩ B` ("A and B") is the event that *both* happen, and `P(A ∩ B)` is its **joint probability**. Conditioning is directional: `P(A | B)` and `P(B | A)` are different questions. `P(B | A)` divides the same joint probability by `P(A)` instead:

> `P(B | A) = P(A ∩ B) / P(A)`,  requiring `P(A) > 0`.

Here is the practical bind. In many real problems one direction is easy to know and the *other* is the one we care about. A medical test is calibrated by giving it to people already known to be sick, which directly measures `P(positive | sick)`. But a patient with a positive result wants `P(sick | positive)` — the reverse. Bayes' rule is exactly the bridge from the conditional we have to the conditional we want.

### The derivation: eliminate the shared joint probability

The two definitions above contain the *same* numerator, `P(A ∩ B)`. That shared term is the hinge. Multiply each definition by its denominator to solve for it:

- from the first, `P(A ∩ B) = P(A | B) · P(B)`;
- from the second, `P(A ∩ B) = P(B | A) · P(A)`.

Both right-hand sides equal the one quantity `P(A ∩ B)`, so they equal each other:

> `P(A | B) · P(B) = P(B | A) · P(A)`.

Now divide both sides by `P(B)` (allowed because `P(B) > 0`) to isolate the conditional we want:

> **`P(A | B) = P(B | A) · P(A) / P(B)`.**

That is Bayes' rule. Nothing was assumed beyond the definition of conditional probability twice over; the single "magic-looking" move is recognizing that the joint probability `P(A ∩ B)` is common to both directions and can be eliminated. The rule simply re-expresses one conditional in terms of the *reverse* conditional, scaled by the two unconditional probabilities `P(A)` and `P(B)`.

### Reading it as belief updating: prior, likelihood, posterior

The rule becomes a tool when we rename the events to match a question of *inference*. Let `θ` (Greek "theta") stand for an unknown state of the world we want to learn — the cause, hypothesis, or parameter (e.g. "this patient is sick"). Let `D` stand for the data we actually observe — the evidence (e.g. "the test was positive"). Substituting `A = θ` and `B = D` into Bayes' rule:

> **`P(θ | D) = P(D | θ) · P(θ) / P(D)`.**

Each piece is a [[probability-distribution]] over `θ`, with a standard name:

- **Prior**, `P(θ)` — the distribution over the possible values of `θ` *before* seeing any data. It encodes what we believed (or how common each state is) in advance.
- **[[likelihood]]**, `P(D | θ)` — for each candidate value of `θ`, how probable the observed data `D` would be *if that value were true*. This is the easy, forward direction, the one the test calibration gives us. (Read as a function of `θ` for fixed observed `D`, it is the likelihood; it need not itself sum to 1 over `θ`.)
- **Posterior**, `P(θ | D)` — the distribution over `θ` *after* folding in the data. This is the updated belief, and the answer we wanted.
- **Evidence / normalizer**, `P(D)` — the overall probability of the data, regardless of `θ`.

In words: **posterior = likelihood × prior, divided by the evidence.** You start from the prior, *reweight* each value of `θ` by how well it predicted what you saw (the likelihood), and renormalize. A value of `θ` that both was plausible to begin with *and* predicts the data well gets a large posterior; a value that was rare or predicts the data poorly gets a small one.

### Where the normalizer comes from, and why it can often be dropped

The denominator `P(D)` is not a new mystery — it is fixed by the requirement that the posterior be a genuine [[probability-distribution]], i.e. that it sum (or integrate) to 1 over all values of `θ`. We can compute it directly. The data `D` can arise *together with* any one of the mutually exclusive values of `θ`, and these joint cases cover every way `D` could happen, so by the disjoint-addition rule of [[probability]] the total probability of `D` is the sum of those joint probabilities:

> `P(D) = Σ_θ P(D ∩ θ) = Σ_θ P(D | θ) · P(θ)`  (discrete `θ`),

or, for a continuous `θ` whose prior is a density, the same sum becomes an integral `P(D) = ∫ P(D | θ) · P(θ) dθ`. Either way, **`P(D)` is just the sum of the numerator over all `θ`.** That is why it normalizes: dividing each numerator `P(D | θ)·P(θ)` by their total forces the posterior values to sum to exactly 1.

Now the key practical observation. The denominator `P(D)` does *not* depend on `θ` — it is one fixed number, the same for every value of `θ`. So as `θ` varies, the posterior is just the numerator scaled by a constant:

> `P(θ | D) ∝ P(D | θ) · P(θ)`,

where `∝` means "proportional to." This is why, **for the *shape* of the posterior — which value of `θ` is most probable, how the probability is distributed across values — you can ignore `P(D)` entirely.** The relative heights are already settled by likelihood × prior. But the moment you need an *actual probability* — "what is the chance the patient is sick, as a number between 0 and 1?" — you must divide by `P(D)`, because only then do the pieces add to 1 and become real probabilities rather than unnormalized weights.

### Worked instance: the rare disease and the "99% accurate" test

Take a disease present in 1% of the population, tested by a kit that sounds excellent. Define the unknown `θ` to be one of two states: `D⁺` = "has the disease" or `D⁻` = "does not." The data is the test result; consider a single observed value, `+` = "test reads positive."

Given numbers (all are easy, forward-direction conditionals — the kind we can measure):

- **Prior** (prevalence): `P(D⁺) = 0.01`, so `P(D⁻) = 1 − 0.01 = 0.99`.
- **Likelihood if sick** (sensitivity): the test catches `99%` of sick people, `P(+ | D⁺) = 0.99`.
- **Likelihood if healthy** (false-positive rate): it wrongly fires on `5%` of healthy people, `P(+ | D⁻) = 0.05`.

We want the reverse conditional, the **posterior** `P(D⁺ | +)` — given a positive test, how probable is disease? Apply Bayes' rule with `A = D⁺`, `B = +`:

> `P(D⁺ | +) = P(+ | D⁺) · P(D⁺) / P(+)`.

Everything is in hand except `P(+)`, the evidence — the overall chance of a positive test. Compute it as the sum of the two joint ways a positive can occur (sick-and-positive, or healthy-and-positive):

- sick and positive: `P(+ | D⁺) · P(D⁺) = 0.99 × 0.01 = 0.0099`,
- healthy and positive: `P(+ | D⁻) · P(D⁻) = 0.05 × 0.99 = 0.0495`,
- total: `P(+) = 0.0099 + 0.0495 = 0.0594`.

Now divide:

> `P(D⁺ | +) = 0.0099 / 0.0594 ≈ 0.167`.

**Only about 17%.** Despite a test that catches 99% of the sick and is wrong only 5% of the time on the healthy, a positive result leaves you *more than 80% likely to be healthy*. The reason is visible in the two joint terms: the false positives `0.0495` outnumber the true positives `0.0099` by roughly five to one, because the healthy group (99% of people) is so much larger than the sick group (1%) that even its small 5% error rate produces more positives than the entire tiny sick group does. The small **prior** `P(D⁺) = 0.01` dominates the strong likelihood. This is exactly the work the prior does in `posterior ∝ likelihood × prior` — and the precise number `0.167` required the normalizer `P(+)`, whereas merely *ranking* the two joint terms (`0.0495` vs `0.0099`) needed only the unnormalized products.

As a sanity check the posterior must be a valid [[probability-distribution]] over the two states. The other branch, `P(D⁻ | +) = 0.0495 / 0.0594 ≈ 0.833`, and `0.167 + 0.833 = 1` — the same normalizer `P(+)` is what makes the two posterior probabilities sum to 1.

## Prerequisites

- [[probability]]
- [[probability-distribution]]
- [[likelihood]]

## Sources

_none_
