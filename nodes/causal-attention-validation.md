---
id: causal-attention-validation
title: Causal Attention Validation
summary: Causal attention validation checks prefix invariance and exact mask conventions rather than inferring information leakage from a low training loss.
type: concept
tags: [ml/llm/training]
prereqs: [causal-language-model-training, metamorphic-testing]
sources: [https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html, https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html]
status: explained
created: 2026-10-31
updated: 2026-10-31
---

# Causal Attention Validation

## Meaning

A causal mask is correct only if the executed model obeys the prefix-only contract of [[causal-language-model-training]]. Inspecting a triangular array is not enough: an API can invert its meaning, broadcast it incorrectly, or combine it incorrectly with padding. Low loss is a diagnostic clue, not proof of future-token leakage.

## Mechanism

Use [[metamorphic-testing]]: hold a token prefix fixed, replace only its suffix, and require earlier output logits to remain equal within a declared numerical tolerance. A logit is the model's score for a possible next token. Disable dropout, including explicitly passing zero dropout to functional scaled-dot-product attention, and hold model state, positions and execution configuration fixed. Prefix invariance is a necessary property of this causal path, not proof of model quality or correct target alignment.

First test a tiny, hand-constructed mask against an explicit reference. In PyTorch's documented MultiheadAttention boolean attention and padding masks, True excludes a position. In functional scaled_dot_product_attention, True includes it. Floating masks instead add a bias to attention scores; they are not boolean arrays with the same polarity. Verify shape and broadcasting as well as polarity, using documentation for the installed version.

## Worked example

Compare token sequences `[red, fox, runs, fast]` and `[red, fox, sleeps, now]`. Outputs at positions zero and one should be invariant: both can read the same prefix, and the output at position one predicts the third token without observing it. Output at position two may change, because its input token changed. For the first two query positions against four keys, an allowed-position mask is `[[1,0,0,0],[1,1,0,0]]`; the equivalent MHA boolean block mask reverses those bits. Reusing one array in both APIs changes the model's accessible information.

A positive control deliberately allows future attention in a small reference case and confirms that the test detects a changed prefix output. An insensitive model might otherwise pass even with a broken mask. Repeat across padding layouts, packed-document boundaries, broadcasted batches and cached versus uncached paths. Check prefix logits rather than sampled strings: random sampling can differ without a causal violation, and identical sampled tokens can hide changed scores.

## Boundaries

A failing test establishes unwanted suffix dependence under the controlled setup, not its unique cause. Inspect mask composition, preprocessing, state reuse and target shifting separately. Passing a finite collection of examples does not prove all shapes, backends or document-boundary policies correct. Keep these cases alongside held-out loss and generation evaluation.

## Sources

- <https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html>
- <https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html>
