---
id: wordpiece-tokenization
title: WordPiece Tokenization
summary: WordPiece segments a pre-tokenized word by repeatedly taking the longest vocabulary piece valid at the current position, with continuation markers distinguishing internal pieces.
type: concept
tags: [ml/llm/architecture]
prereqs: [subword-tokenization, trie]
sources: [https://huggingface.co/learn/llm-course/chapter6/6, https://github.com/google-research/bert/blob/master/tokenization.py]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# WordPiece Tokenization

## Summary

**WordPiece** is a [[subword-tokenization]] family commonly associated with BERT. Its defining inference behavior is greedy longest-match segmentation of each pre-tokenized word using a fixed vocabulary. A marker such as `##` can distinguish a continuation piece from a word-initial piece.

## Grounded explanation

Suppose the vocabulary contains `play`, `##ing`, `player`, and `##er`. For `playing`, start at the beginning and choose the longest valid initial piece, `play`. Then choose the longest continuation matching the remaining suffix, `##ing`. A [[trie]] can accelerate longest-prefix lookup, but the result is defined by the vocabulary and boundary rules, not by the data structure used to implement it. If no required piece exists, some WordPiece implementations emit an unknown token for the entire word; check the particular tokenizer rather than assuming byte-level fallback.

Training and inference should not be conflated. Published tutorials often describe WordPiece training with a pair score that rewards association rather than raw pair frequency, contrasting it with BPE. Google's original WordPiece training implementation was not publicly released, so that reconstruction is not a universal specification. The observable, testable contract for a deployed model is its frozen vocabulary, normalization, pre-tokenization, and greedy encoding behavior. BPE instead saves an ordered merge list and applies those merge priorities; equal-looking vocabularies need not encode the same input identically.

A practical test suite should include unseen words, repeated punctuation, Unicode, casing and normalization, beginning-versus-continuation positions, and round-trip behavior. If the tokenizer may emit unknown tokens, report unknown rates by domain and their downstream effect. For a code editor, also test arbitrary cursor prefixes: longest matches on completed words do not imply stable segmentation when the last word is still being typed.

## Prerequisites

- [[subword-tokenization]]
- [[trie]]

## Sources

- [Hugging Face LLM Course, WordPiece tokenization](https://huggingface.co/learn/llm-course/chapter6/6): greedy encoding and explicit uncertainty about the unreleased original training algorithm.
- [Google Research BERT tokenizer implementation](https://github.com/google-research/bert/blob/master/tokenization.py): original open-source WordPiece inference behavior.
