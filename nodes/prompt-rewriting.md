---
id: prompt-rewriting
title: Prompt Rewriting
summary: Prompt rewriting transforms a user's request into conditioning better suited to a target model while attempting to preserve the user's intent.
type: concept
tags: [ml/llm/inference]
prereqs: [text-image-attribute-binding, image-preference-modeling]
sources: [https://arxiv.org/abs/2212.09611]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Prompt Rewriting

## Summary

**Prompt rewriting** is an inference-time translation layer that maps raw user language to model-facing conditioning. It can add specificity or model-compatible phrasing without changing model weights.

## Grounded explanation

Promptist trains a language model on manually engineered text-to-image prompts and then optimizes generated prompts with a reward that combines visual appeal and preservation of original intent. This demonstrates prompt adaptation, not the stronger claim that every short prompt is out of distribution or that expansion always improves an image.

The rewrite must preserve hard constraints: entities, counts, relations, negation, requested style, and exclusions. Those constraints include [[text-image-attribute-binding]]. Added details should be distinguishable from the user's words, controllable, and reversible. Otherwise a rewriter may homogenize style, erase ambiguity the user intended, introduce stereotypes, or alter safety meaning.

Compare raw input, transparent rewrite, clarification UI, and model adaptation. Rewriting adds latency and another failure surface but can be changed without retraining the generator. It should preserve the original prompt for auditing and offer an opt-out or editable result when user agency matters.

Evaluate on representative anonymized prompts across lengths, languages, and domains. Use blinded human judgments of intent preservation, prompt adherence, aesthetics, diversity, and unwanted additions; report rewrite latency and failure rate. A learned [[image-preference-modeling|preference model]] can assist development, but final validation must not rely only on the same reward used to train the rewriter.

## Prerequisites

- [[text-image-attribute-binding]]
- [[image-preference-modeling]]

## Sources

- [Hao et al., “Optimizing Prompts for Text-to-Image Generation”](https://arxiv.org/abs/2212.09611): introduces prompt adaptation with supervised training and reward optimization designed to improve images while preserving user intent.
