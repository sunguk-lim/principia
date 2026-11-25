---
id: shannon-entropy
title: "Shannon Entropy"
summary: "Shannon entropy is the expected information content of a discrete outcome under a specified probability distribution and logarithm base."
type: concept
tags: [math/probability]
prereqs: [probability-distribution, logarithm, expectation]
sources: [https://www.princeton.edu/~wbialek/rome/refs/shannon_48.pdf, https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.entropy.html]
status: explained
created: 2026-11-26
updated: 2026-11-26
---

# Shannon Entropy

## Meaning

Shannon entropy summarizes how spread out the outcomes of a discrete [[probability-distribution]] are. It is an average information quantity, not a measure of whether a prediction is true or whether an uncertain example is useful to label. The same probabilities can describe model predictions, observed frequencies or a committee's votes; those interpretations must remain explicit.

## Mechanism

Let X be a discrete outcome with probabilities p_i that sum to one. Using a [[logarithm]] with base b greater than one, define information content for outcome i as minus log_b(p_i). The [[expectation]] of that quantity is entropy:

$$H(X)=-\sum_i p_i\log_b p_i.$$

Base two gives bits; base e gives nats. A certain outcome has zero information because log(1)=0. Less likely outcomes have greater information; weighting by their probabilities yields an average, not the surprise of a particular observed outcome. A zero-probability outcome contributes zero by the limit of p log p as p approaches zero.

Independent outcomes multiply their probabilities, and logarithms convert that multiplication into addition. This gives the information quantity an additive interpretation. Entropy is largest for the uniform distribution over a fixed finite number of outcomes and decreases as probability concentrates. Comparing different outcome spaces without stating them can mislead.

## One example

A hypothetical source has probabilities 1/2, 1/4 and 1/4 for three symbols. Their information contents in bits are 1, 2 and 2. Expected information is (1/2)×1+(1/4)×2+(1/4)×2=1.5 bits. A uniform three-symbol source has log_2(3), approximately 1.585 bits; a source emitting one certain symbol has zero.

For votes split evenly between two labels, entropy is one bit even if every voter shares a mistaken task formulation. Conversely, unanimous wrong votes have zero vote entropy. The numeric uncertainty describes the declared distribution, not correctness.

## Validation and boundaries

Check probability normalization, outcome enumeration, units and zero handling. Do not mix entropy of averaged predictions with average prediction entropy: they answer different questions. SciPy documents the discrete formula and relative-entropy distinction; its normalization behavior is an API policy, not permission to omit defining the distribution.

## Check your understanding

Does high entropy mean the most likely answer is wrong? No. It describes predictive spread and says nothing by itself about the actual outcome.

## Prerequisites

- [[probability-distribution]]
- [[logarithm]]
- [[expectation]]

## Sources

- <https://www.princeton.edu/~wbialek/rome/refs/shannon_48.pdf>
- <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.entropy.html>
