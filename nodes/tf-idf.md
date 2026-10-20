---
id: tf-idf
title: TF-IDF
summary: TF-IDF weights token counts by corpus rarity and optionally normalizes the resulting vector for lexical similarity or classification.
type: concept
tags: [ml/information-retrieval]
prereqs: [bag-of-words, logarithm, cosine-similarity]
sources: [https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting]
status: explained
created: 2026-10-21
updated: 2026-10-21
---

# TF-IDF

## Meaning

TF-IDF means term frequency times inverse document frequency. It reweights a [[bag-of-words]] vector so a term's contribution depends on both its occurrences in a document and its rarity across the indexed corpus. It does not represent arbitrary word order or semantic equivalence.

## Mechanism

Let n be the number of fitted corpus documents, df(t) the number containing term t, and tf(t,d) the count of t in document d. One common smoothed convention, used by scikit-learn defaults, is:

$$idf(t)=\ln\frac{1+n}{1+df(t)}+1,\qquad w(t,d)=tf(t,d)\,idf(t).$$

Here ln is the natural [[logarithm]]. Smoothing keeps the denominator positive; the additive constant means a term appearing in every fitted document has idf=1 rather than zero. Other implementations choose different smoothing, sublinear term counts and normalization, so record the convention.

For nonzero vectors, divide weights by their Euclidean length if unit normalization is desired. [[cosine-similarity]] then compares query and document directions; with unit vectors it equals their dot product. Fit vocabulary and corpus frequencies on the intended indexing or training data, and transform queries using the same fitted mapping. A missing query term cannot contribute through a vocabulary coordinate that does not exist.

## Worked example

Three corpus documents use vocabulary [common,rare]. The common term appears in all three, while rare appears in only one. Smoothed weights are idf(common)=ln(4/4)+1=1 and idf(rare)=ln(4/2)+1≈1.693.

A document containing common twice and rare once has raw vector (2,1.693). Its length is sqrt(4+1.693²)≈2.620, giving normalized vector (0.763,0.646). A query containing only rare normalizes to (0,1), so cosine similarity is approximately 0.646. A document with only common has similarity zero to this query. These scores express lexical overlap under this representation, not a probability that the document supports an answer.

## Check your understanding

**Question:** Does a high TF-IDF score certify answerability? **Answer:** No. Test evidence support separately. Evaluate tokenization, rare identifiers, synonyms, negation, corpus changes and out-of-vocabulary queries against a simple count or BM25 baseline.

## Prerequisites

- [[bag-of-words]]
- [[logarithm]]
- [[cosine-similarity]]

## Sources

- <https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting>
