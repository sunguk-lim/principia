---
id: byte-pair-encoding-tokenization
title: Byte-Pair Encoding Tokenization
summary: Byte-pair encoding learns frequent adjacent-symbol merges and applies the learned merge order to segment new text into subword tokens.
type: concept
tags: [ml/llm/architecture]
prereqs: [subword-tokenization, hash-map]
sources: [https://arxiv.org/abs/1508.07909, https://huggingface.co/learn/llm-course/chapter6/5]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Byte-Pair Encoding Tokenization

## Summary

**Byte-pair encoding (BPE)** builds a token vocabulary by repeatedly merging adjacent symbols that occur together frequently in a training corpus. The saved merge order is then used to encode new text. This is one way to construct [[subword-tokenization]], not a guarantee that the shortest possible token sequence is selected.

## Grounded explanation

Begin with a base alphabet after normalization and any pre-tokenization. Count adjacent symbol pairs across the training corpus, often with a [[hash-map]] of pair frequencies. Add the most frequent pair as a new symbol, replace its occurrences, recount, and repeat until the vocabulary budget is reached. A toy corpus with frequent `l` followed by `o` may learn `lo`; a later merge may join `lo` and `w` into `low`. The count and merge order come from that corpus, not a universal linguistic rule.

At inference time, the tokenizer applies its frozen merge rules. A word may be one piece in one vocabulary and several pieces in another. Pre-tokenization boundaries matter: a method that never merges across whitespace behaves differently from one allowed to merge a leading space with a word. Byte-level BPE uses bytes as its base alphabet, avoiding an unknown Unicode character at the cost of possibly splitting one character into several byte pieces. Other BPE variants use characters or explicit unknown-token handling; do not transfer a byte-level claim to every implementation.

BPE optimizes a local frequency-based construction objective. It does not directly optimize autocomplete, semantic structure, or model quality. A merge that reduces token count on complete files can create awkward boundaries at arbitrary editor cursor positions. Test `decode(encode(x)) == x` for the intended normalization contract, token-length distributions on held-out domains, and downstream outcomes under matched training and inference budgets. Compare byte-normalized loss, not only loss per token, when vocabularies differ.

## Prerequisites

- [[subword-tokenization]]
- [[hash-map]]

## Sources

- [Sennrich et al., subword units for neural machine translation](https://arxiv.org/abs/1508.07909): adaptation of BPE-style merging to text segmentation.
- [Hugging Face LLM Course, BPE tokenization](https://huggingface.co/learn/llm-course/chapter6/5): training and application of merge rules, including byte-level variation.
