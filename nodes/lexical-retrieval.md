---
id: lexical-retrieval
title: Lexical Retrieval
summary: Lexical retrieval finds and ranks documents from explicit query-term overlap, using an inverted index and a term-weighting rule such as BM25.
type: concept
tags: [ml/information-retrieval]
prereqs: [inverted-index, bm25]
sources: [https://nlp.stanford.edu/IR-book/html/htmledition/boolean-retrieval-1.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Lexical Retrieval

## Summary

**Lexical retrieval** returns documents based on explicit overlap between normalized query terms and indexed document terms, using an [[inverted-index]] for candidates and a ranking function such as [[bm25]] for relevance.

## Grounded explanation

The process has three stages: normalize the query with the same rules used at indexing, fetch each term's postings from the [[inverted-index]], then combine or rank the candidate documents. Boolean retrieval requires terms to be present; ranked retrieval lets several weak and strong matches compete through [[bm25]].

### Worked example

Query `red fox` retrieves postings for `red` and `fox`. D1 contains both terms once; D2 contains only `red`; D3 contains `fox` twice. Under strict `AND`, only D1 survives. Under ranked retrieval, all three may survive, but D1 receives contributions from both terms. If `red` appears in almost every document while `fox` is rare, the rare term contributes more.

Lexical retrieval preserves exact evidence: a query containing an error code, symbol, or product identifier can find the same character sequence even when no semantic model represents it well. Its failure mode is vocabulary mismatch: “automobile” does not directly match “car” unless normalization or expansion connects them.

## Prerequisites

- [[inverted-index]]
- [[bm25]]

## Sources

- Manning, Raghavan, and Schütze, *Introduction to Information Retrieval*, Boolean and ranked retrieval chapters.
