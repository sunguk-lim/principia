---
id: johnson-lindenstrauss-lemma
title: Johnson-Lindenstrauss Lemma
summary: The Johnson-Lindenstrauss lemma guarantees that a fixed finite set admits a lower-dimensional map preserving all pairwise squared Euclidean distances within a chosen relative distortion.
type: concept
tags: [math/linear-algebra]
prereqs: [random-projection, probability, logarithm]
sources: [https://scikit-learn.org/stable/modules/random_projection.html, https://scikit-learn.org/stable/modules/generated/sklearn.random_projection.johnson_lindenstrauss_min_dim.html]
status: explained
created: 2026-11-14
updated: 2026-11-14
---

# Johnson-Lindenstrauss Lemma

## Meaning

A large ambient coordinate count does not necessarily require an equally large representation of a fixed finite dataset. The Johnson-Lindenstrauss lemma says that all pairwise distances among n fixed points can be approximately preserved with output dimension proportional to log(n)/epsilon squared, where epsilon is an allowed relative distortion between zero and one. The constants and probability guarantee depend on the construction and theorem statement.

## Contract

Let x_i and x_j be any two of the n fixed input vectors and R the chosen map. Write ||u||_2 squared for squared Euclidean length, as defined by [[random-projection]]'s distance foundation. The desired simultaneous guarantee is

$$(1-\epsilon)\|x_i-x_j\|_2^2\leq\|R x_i-R x_j\|_2^2\leq(1+\epsilon)\|x_i-x_j\|_2^2.$$

Every pair must satisfy this inequality for a successful map. Suitable random constructions achieve high [[probability]] of success with enough coordinates; requesting smaller failure probability requires accounting for that budget too. The [[logarithm]] appears because the number of finite pairs must be protected at once while per-pair failure falls rapidly with dimension. This is intuition for the theorem, not a proof that any learned projection obeys its hypotheses.

## One example

With epsilon=.2 and a pair's original squared separation 25, allowed projected squared separation is between .8 times 25=20 and 1.2 times 25=30. The corresponding distances range from sqrt(20) to sqrt(30), not from 20 to 30. A map with this property on one pair is not yet certified on the whole dataset.

The scikit-learn implementation's conservative formula uses 4 ln(n)/(epsilon squared/2 - epsilon cubed/3), before choosing a sufficient integer dimension. For n=1000 and epsilon=.5, the denominator is .125-.0416667=.0833333 and the quotient is about 331.57, so choosing 332 satisfies that displayed sufficient bound. Such a bound can exceed the original dimension; a theorem-based request need not offer useful compression. Treat the library's bound as its documented sufficient-dimension convention, not a universal optimum.

## Boundaries and check

A fixed output dimension does not imply arbitrarily small error as n grows. Protecting more pairs generally requires more dimensions at the same distortion and confidence. Distance preservation does not automatically prove attention-output accuracy, causal masking, task quality or a guarantee for unseen adaptively chosen points. In particular, a learned sequence-axis projection must be justified under its own assumptions rather than borrowing the lemma's name.

## Prerequisites

- [[random-projection]]
- [[probability]]
- [[logarithm]]

## Sources

- <https://scikit-learn.org/stable/modules/random_projection.html>
- <https://scikit-learn.org/stable/modules/generated/sklearn.random_projection.johnson_lindenstrauss_min_dim.html>
