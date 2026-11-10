---
id: reformer-lsh-attention
title: Reformer LSH Attention
summary: Reformer LSH attention hashes shared query-key representations into content-based neighborhoods, sorts them into bounded chunks and restores outputs to their original sequence positions.
type: concept
tags: [ml/llm/architecture]
prereqs: [sparse-attention-patterns, nearest-neighbor-search, matrix-multiplication]
sources: [https://arxiv.org/html/2001.04451v2]
status: explained
created: 2026-11-11
updated: 2026-11-11
---

# Reformer LSH Attention

## Meaning

Reformer's locality-sensitive hashing (LSH) attention chooses candidate keys from content similarity rather than a fixed positional window. A locality-sensitive hash makes nearby representations more likely to share a bucket. It is a probabilistic candidate rule, not an exact nearest-neighbor guarantee or a privacy hash.

## Mechanism

The primary construction shares the query/key projection and normalizes keys. For a row vector x of d features and an even bucket count b, choose a random d-by-(b/2) matrix R. Compute xR by [[matrix-multiplication]], concatenate xR and its negation, and use the largest coordinate's index as the bucket. Similar directions can share that index. Multiple independent rounds can recover neighbors missed by one hash, at extra cost.

Sort representations by bucket and original position, compute attention in fixed-size chunks with a preceding chunk available, apply bucket/causal masks and then restore original sequence order. Bucket sizes are uneven, so chunk boundaries and masks matter. Repeated pairs across hash rounds need the paper's duplicate-aware combination rather than counting the same key as extra evidence. Unlike fixed [[sparse-attention-patterns]], these neighborhoods depend on the current representations. [[nearest-neighbor-search]] explains the approximation being introduced.

## One example

For an illustrative hash, set d=2, b=4 and R to the 2-by-2 identity. For x=(0.8,0.6), the concatenated vector is (0.8,0.6,-0.8,-0.6), so bucket 0 wins. For y=(0.9,0.4), bucket 0 also wins. For z=(-0.8,0.6), the vector is (-0.8,0.6,0.8,-0.6), so bucket 2 wins. Identity is an illustrative possible projection, not the recommended randomized hash family.

If x occurs at original position 5 and y at position 8, the shared bucket alone does not let x read y in a causal model: original time still forbids that pair after sorting. A nearby vector across a bucket boundary can also be missed. Hash agreement is neither sufficient for permission nor necessary for true relevance.

## Check your understanding

Does Reformer compute exact dense attention faster? No: its LSH neighborhood approximates the interaction set. The paper's O(N log N) scaling depends on the hashing/sorting/chunk regime; varying rounds and chunk sizes changes costs. Test retrieval of important pairs, task quality, round count, masks, duplicate handling and sort overhead against dense and fixed-sparse baselines. Reversible layers are a separate Reformer contribution, not a consequence of LSH attention.

## Prerequisites

- [[sparse-attention-patterns]]
- [[nearest-neighbor-search]]
- [[matrix-multiplication]]

## Sources

- <https://arxiv.org/html/2001.04451v2>
