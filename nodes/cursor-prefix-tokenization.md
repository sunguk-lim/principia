---
id: cursor-prefix-tokenization
title: Cursor-Prefix Tokenization
summary: Cursor-prefix tokenization tests whether a tokenizer's representation of a half-typed prompt is usable for continuation, even when its complete-document compression and loss look favorable.
type: concept
tags: [ml/llm/inference]
prereqs: [subword-tokenization, byte-pair-encoding-tokenization, context-window]
sources: [https://huggingface.co/learn/llm-course/chapter6/5, https://huggingface.co/docs/transformers/main/en/llm_tutorial]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Cursor-Prefix Tokenization

## Summary

An editor sends a model the text **before the cursor**, not necessarily a complete word, line, or file. **Cursor-prefix tokenization** examines how that truncated text becomes tokens and whether generation can continue it faithfully. This is a different evaluation distribution from full-document tokenization.

## Grounded explanation

A deterministic tokenizer encodes the supplied prefix as it exists. The sequence for `import num` need not be a prefix of the token sequence for `import numpy`: after more characters arrive, a [[byte-pair-encoding-tokenization]] merge may span what used to be the cursor boundary. Thus a model trained mostly on completed code may see unusual terminal tokens or token combinations during autocomplete. The mere existence of a mid-token cursor does not prove failure; measure the mismatch and the model's response.

The relevant unit is a character or byte offset in the source file, not an arbitrary token boundary. Sample real code at offsets after indentation, inside identifiers and strings, before newline, and at completed statement boundaries. Compare the old and proposed [[subword-tokenization]] under matched model and training budgets. Token count and per-token cross-entropy alone are misleading across different vocabularies: report total negative log probability divided by the same number of source bytes (bits per byte), plus completion exact match, edit similarity, syntactic validity, accepted suggestions, and latency. Preserve round-trip bytes for tabs, spaces, Unicode, and line endings.

A possible mitigation is *token healing*: back off a terminal token and constrain early generated text to reproduce the already typed suffix before free continuation. It needs careful alignment between bytes and tokens and can increase decoding work or delay. A boundary-aware tokenizer or training mixture with random prefixes is another alternative. Stopping is a separate issue: if one emitted token includes a newline and following indentation, a line-completion UI must define whether to reject, trim, or buffer that token without corrupting text. Evaluate clean stopping and truncation, not just model loss.

A longer prompt uses more of the [[context-window]], but a shorter sequence is useful only if the product's completion quality, stop behavior, and keystroke latency remain acceptable. The tokenizer choice is therefore a workload decision.

## Prerequisites

- [[subword-tokenization]]
- [[byte-pair-encoding-tokenization]]
- [[context-window]]

## Sources

- [Hugging Face LLM Course, BPE tokenization](https://huggingface.co/learn/llm-course/chapter6/5): frozen merge rules and segmentation that motivate the prefix-boundary analysis.
- [Hugging Face Transformers text generation guide](https://huggingface.co/docs/transformers/main/en/llm_tutorial): token-by-token continuation and generation controls. Cursor-offset evaluation and mitigation trade-offs here are independent derivations, not results claimed by those sources.
