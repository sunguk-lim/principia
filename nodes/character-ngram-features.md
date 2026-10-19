---
id: character-ngram-features
title: Character N-Gram Features
summary: Character n-gram features count short character spans, sharing surface-form evidence across words without assuming semantic equivalence.
type: concept
tags: [ml/feature-engineering]
prereqs: [bag-of-words]
sources: [https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction]
status: explained
created: 2026-10-20
updated: 2026-10-20
---

# Character N-Gram Features

## Meaning

Character n-grams represent text with overlapping spans of characters instead of only whole words. Related spellings can activate common coordinates even when a complete word was absent from the training vocabulary. This is surface-form sharing, not a learned guarantee of shared meaning.

## Mechanism

Choose normalization, boundary handling and span lengths before fitting the count vocabulary. Count each overlapping character span using the same vector construction as [[bag-of-words]]. A within-word analyzer can pad each word with boundaries and avoid spans crossing spaces; an unrestricted analyzer may include cross-word spans. Those are different contracts. Accents, case and Unicode normalization affect which spans coincide. Small spans generalize broadly but also mix unrelated words; large spans become more specific and sparse. Hashing can bound dimensions but adds collision behavior. Neither strategy automatically recognizes synonymy or long-range order.

## Worked example

Ignoring boundary padding for illustration, character trigrams of “help” are [hel, elp]. “helpful” produces [hel, elp, lpf, pfu, ful]. Both share two coordinates, allowing a classifier to transfer evidence about the common stem. “assist” produces [ass, ssi, sis, ist] and shares none of those coordinates even though its meaning may be related. Conversely, a shared span can occur in words with different meanings. Compare whole-word features, character spans and their combination on held-out inflections, spelling variants, typos and unrelated lookalikes. Keep feature selection inside training folds and measure quality, vocabulary size, nonzero counts and serving cost. Semantic embeddings or explicit normalization rules are alternatives when surface sharing is insufficient; they require their own validation.

## Check your understanding

Does sharing the span “hel” prove two words should have the same label? No. The representation supplies overlapping evidence; labels, other features and training determine how it is used.

## Prerequisites

- [[bag-of-words]]

## Sources

- <https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction>
