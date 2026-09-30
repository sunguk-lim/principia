---
id: code-corpus-leakage-audit
title: Code-Corpus Leakage Audit
summary: A code-corpus leakage audit tests whether copied or closely related code crosses training and evaluation boundaries, then reports performance on low-overlap, group-separated holdouts.
type: concept
tags: [ml/evaluation]
prereqs: [dataset-lineage, temporal-data-leakage, measurement]
sources: [https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html, https://ekzhu.com/datasketch/minhash.html, https://huggingface.co/datasets/bigcode/the-stack]
status: explained
created: 2026-10-01
updated: 2026-10-01
---

# Code-Corpus Leakage Audit

## Summary

A random file-level split can put closely related code on both sides of a train/test boundary. An audit measures that overlap and asks whether the reported improvement survives on examples whose repository family and near-duplicate cluster are absent from training. Overlap is a threat to the intended generalization claim, not automatic proof that the model memorized a particular test answer.

## Grounded explanation

Preserve each file's repository, fork relationship, snapshot time, and transformation history in [[dataset-lineage]]. Exact hashes catch byte-identical copies but miss files with renamed identifiers, changed headers, or minor edits. Normalize and tokenize code, form overlapping token shingles, and compare their sets. MinHash sketches approximate Jaccard similarity; locality-sensitive hashing can retrieve likely pairs without comparing every file. Both are candidate-finding tools: their thresholds, tokenization, and false negatives must be measured against a labeled pair sample. Semantically equivalent programs can also look dissimilar, so no single fingerprint proves independence.

Construct a graph whose edges connect verified near-duplicates, copies, or fork-related repositories. Split connected groups, not individual files, across train and test. GroupShuffleSplit is an example of group-disjoint splitting, but its guarantee is only as good as the supplied group IDs. Repository-level grouping misses copied code across repositories; file-level clusters can miss sibling files that share APIs and style. Compare both grouping policies and inspect their residual overlap.

Add a prospective slice: train only on artifacts available before a cutoff and test on later work, applying the point-in-time rules of [[temporal-data-leakage]]. A time split alone does not remove later copies of older code. Record when the corpus snapshot was taken, not merely a repository's nominal commit date.

For each test example, record nearest-training similarity and evaluate in overlap buckets. Suppose an apparent accuracy gain is concentrated in the highest-similarity bucket but disappears in the lowest; the original result has weak evidence for novel-code generalization. If the gain persists in a sufficiently large low-overlap bucket, that is stronger evidence, though distribution shift, task difficulty, and hidden duplicates remain possible. Use [[measurement]] to report bucket sizes, confidence intervals, and audit recall. Keep a separate newly authored or independently curated holdout when possible; do not publish private code or infer licensing permission from statistical deduplication.

## Prerequisites

- [[dataset-lineage]]
- [[temporal-data-leakage]]
- [[measurement]]

## Sources

- [scikit-learn GroupShuffleSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html): disjoint group assignment in evaluation splits.
- [datasketch MinHash](https://ekzhu.com/datasketch/minhash.html): approximate Jaccard similarity and its estimation limits.
- [BigCode The Stack dataset card](https://huggingface.co/datasets/bigcode/the-stack): primary dataset documentation and code-corpus curation context; no gated dataset files were accessed.
