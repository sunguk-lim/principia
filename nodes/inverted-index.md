---
id: inverted-index
title: Inverted Index
summary: An inverted index maps each term to the documents and positions containing it, reversing the document-to-terms representation to make term lookup direct.
type: concept
tags: [ml/information-retrieval]
prereqs: [hash-map]
sources: [https://nlp.stanford.edu/IR-book/html/htmledition/inverted-indexes-1.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Inverted Index

## Summary

An **inverted index** reverses a document collection: instead of storing only each document's terms, it maps each term to a postings list of the documents—and often positions—where that term occurs.

## Grounded explanation

The term dictionary can use a [[hash-map]] from a normalized term to its postings. A posting records a document identifier and may also store term frequency and positions. Query work then grows with the matching postings rather than with every document in the collection.

### Worked example

For documents D1 = “red fox”, D2 = “red bird”, and D3 = “blue fox fox”, the index is:

- `red → [(D1,1), (D2,1)]`
- `fox → [(D1,1), (D3,2)]`
- `bird → [(D2,1)]`
- `blue → [(D3,1)]`

The number after each document is term frequency. Searching `red AND fox` intersects the `red` and `fox` document lists and returns D1 without reading D2 or D3's text. Phrase search needs stored positions, while ranked retrieval uses frequencies and collection statistics.

Index construction pays storage and update cost so query-time lookup is sparse and direct. Normalization choices—case folding, token boundaries, and stemming—determine which surface forms share a dictionary entry.

## Prerequisites

- [[hash-map]]

## Sources

- Manning, Raghavan, and Schütze, *Introduction to Information Retrieval*, “Inverted indexes.”
