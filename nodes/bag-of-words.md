---
id: bag-of-words
title: Bag of Words
summary: Bag of words represents text by token occurrence counts while discarding the ordering between occurrences.
type: concept
tags: [ml/feature-engineering]
prereqs: [tensor, arithmetic]
sources: [https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction]
status: explained
created: 2026-10-20
updated: 2026-10-20
---

# Bag of Words

## Meaning

A bag-of-words representation turns a variable-length document into one count per vocabulary token. It is a representation, not a classifier: many prediction rules can consume the same counts. Its useful simplicity is also a hard information boundary.

## Mechanism

First choose normalization and token boundaries, then fit a vocabulary on training documents. Coordinate j counts occurrences of vocabulary token j, forming a one-dimensional [[tensor]]. Counts combine through [[arithmetic]] addition, which is insensitive to the order of terms. Any permutation preserving these token counts has the same representation. A downstream classifier cannot distinguish such inputs without additional features, no matter how well its weights are tuned. Binary occurrence indicators or frequency weighting change values but do not restore discarded order. Unknown vocabulary items may disappear unless the transformation provides a separate policy.

## Worked example

Choose vocabulary [bright, not, dull]. The token sequences “bright not dull” and “dull not bright” both map to [1,1,1], despite contrasting interpretations. “bright bright dull” maps to [2,0,1]; it is distinguishable because its counts differ. A linear classifier with weights [2,-1,-2] gives the first two sequences the same score, -1, and the third score 2. Changing weights cannot break the first collision. Adding local word-pair features may distinguish it, but would create a different representation. Keep tokenization and vocabulary fixed across training and serving. Validate unseen-word rate, normalization, negation and order-sensitive examples, held-out quality, memory and extraction latency. Counts are cheap and inspectable, but do not intrinsically share learned behavior across synonyms.

## Check your understanding

Would a deeper classifier recover the lost ordering from the identical vector? No. It can learn richer functions of retained counts, not information absent from its input.

## Prerequisites

- [[tensor]]
- [[arithmetic]]

## Sources

- <https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction>
