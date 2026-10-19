---
id: word-ngram-features
title: Word N-Gram Features
summary: Word n-gram features count contiguous token sequences to preserve local ordering without representing arbitrary sentence structure.
type: concept
tags: [ml/feature-engineering]
prereqs: [bag-of-words, regularization]
sources: [https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction]
status: explained
created: 2026-10-20
updated: 2026-10-20
---

# Word N-Gram Features

## Meaning

A word n-gram is a contiguous sequence of n tokens. Counting these sequences extends a unigram bag with local order. The resulting bag still discards where each occurrence appears in the document and how distant occurrences relate.

## Mechanism

With n=2, move a two-token window across the normalized sequence and treat each ordered pair as a feature name. A combined unigram-and-bigram vector retains individual words plus adjacent pairs. As in [[bag-of-words]], learned vocabulary and preprocessing define the coordinates. The possible pair space grows rapidly, but actual width depends on observed pairs, frequency thresholds and vocabulary caps; there is no universal feature-count multiplier. Rare pairs can encourage memorization, so use [[regularization]] and choose the vocabulary using training data only. Stop-word removal can erase negators or turn nonadjacent tokens into apparent neighbors: preprocessing is part of the feature definition.

## Worked example

Tokenize “not very helpful” as three tokens. Its bigrams are [not very, very helpful], not [not helpful]. “not helpful” activates the latter feature but lacks the first two. Thus a weight on “not helpful” cannot by itself handle negation separated by “very”. A trigram adds “not very helpful”, but an even longer insertion can escape that fixed window again. Compare unigrams, bounded word n-grams and an order-aware encoder on identical held-out cases, including adjacent negation, distant scope, reordered words and domain shift. Report feature count, nonzero entries, train/dev gap, artifact bytes and latency alongside quality. More local features can help without supplying general syntax or synonym equivalence.

## Check your understanding

Does a successful bigram patch establish that negation is solved? No. It establishes a measured improvement on the tested local patterns; scope and unseen constructions remain separate tests.

## Prerequisites

- [[bag-of-words]]
- [[regularization]]

## Sources

- <https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction>
