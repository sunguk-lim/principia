---
id: subword-tokenization
title: Subword Tokenization
summary: Subword tokenization maps text into reusable pieces between characters and whole words, trading vocabulary size and sequence length against how reliably unfamiliar text can be represented.
type: concept
tags: [ml/llm/architecture]
prereqs: [probability-distribution]
sources: [https://arxiv.org/abs/1508.07909, https://huggingface.co/learn/llm-course/chapter6/4]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Subword Tokenization

## Summary

A language model receives discrete token IDs, not raw text. **Subword tokenization** constructs a vocabulary of reusable fragments and a rule for converting text to IDs and back. Its unit sits between a single character or byte and an entire word.

## Grounded explanation

A whole-word vocabulary is compact for common phrases but cannot represent every new name, spelling, or code identifier without a fallback. A character-level vocabulary covers more strings but requires many more model steps. Subword units let frequent fragments use one ID while rare forms are assembled from several IDs. The base alphabet and normalization rules determine whether every input can round-trip; byte-level methods can cover arbitrary UTF-8 bytes, while a character inventory without fallback may emit an unknown token.

Vocabulary construction and application are separate operations. Training on a corpus chooses pieces; encoding a new input applies the frozen vocabulary and segmentation algorithm. Two tokenizers may encode the same text into different numbers and boundaries of tokens even when decoding restores identical bytes. That changes the model's sequence lengths, available [[probability-distribution]] at each step, and where a prompt can end. It does not by itself establish better task performance.

For example, `unhelpful` could be one token, `un` + `helpful`, or several character pieces. A shorter segmentation reduces the number of decode steps for that string, but a larger vocabulary increases the output layer and may give rare pieces little training evidence. For code, whitespace, indentation, and partial identifiers can be task-critical; compression of finished files need not predict behavior when a user pauses mid-word.

Compare tokenizers on a fixed byte corpus, explicit normalization and round-trip tests, token counts by domain, memory and decoding cost, and downstream task quality. Normalize model loss to bytes or characters before comparing vocabularies: mean loss per token changes its denominator when token boundaries change. Evaluate complete documents and arbitrary prefixes separately.

## Prerequisites

- [[probability-distribution]]

## Sources

- [Sennrich, Haddow, and Birch, “Neural Machine Translation of Rare Words with Subword Units”](https://arxiv.org/abs/1508.07909): subword representation for open-vocabulary text.
- [Hugging Face LLM Course, normalization and pre-tokenization](https://huggingface.co/learn/llm-course/chapter6/4): model vocabulary, normalization, and tokenization stages.
