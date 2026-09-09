---
id: subject-driven-generation
title: Subject-Driven Generation
summary: Subject-driven generation adapts a pretrained text-to-image model from a small reference set so a new identifier denotes one specific subject across novel contexts.
type: concept
tags: [ml/training]
prereqs: [denoising-diffusion-probabilistic-model, regularization, text-image-attribute-binding]
sources: [https://arxiv.org/abs/2208.12242]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Subject-Driven Generation

## Summary

**Subject-driven generation** learns a particular subject from a few reference images and binds it to a distinctive text identifier while preserving the base model's ability to render the broader class.

## Grounded explanation

DreamBooth adapts a pretrained [[denoising-diffusion-probabilistic-model]] using prompts that pair a rare identifier with a class noun. The target is not memorization of the training backgrounds: it is identity preservation across new poses, scenes, views, and styles.

Few examples create competing risks. Too little adaptation loses subject details; too much can reproduce backgrounds, collapse diversity, or shift the meaning of the whole class. DreamBooth's class-specific prior-preservation term generates class images from the frozen base and trains the adapted model to retain that prior. This is [[regularization]], not a guarantee against forgetting or language drift.

Parameter-efficient updates can reduce storage and make subject modules swappable, but low rank alone does not guarantee equal identity fidelity or prevent interference. Compare full, restricted-layer, and low-rank updates at matched quality and training budget rather than assuming one dominates.

Hold out views and backgrounds. During training, track subject similarity alongside generic class quality, prompt adherence, diversity, and memorization. Ablate identifier choice, caption variation, update scope, prior-loss weight, synthetic class set, learning rate, and checkpoint. Test prompts both with and without the identifier to detect leakage in [[text-image-attribute-binding]].

## Prerequisites

- [[denoising-diffusion-probabilistic-model]]
- [[regularization]]
- [[text-image-attribute-binding]]

## Sources

- [Ruiz et al., “DreamBooth”](https://arxiv.org/abs/2208.12242): introduces identifier binding, class-specific prior preservation, and evaluation for subject-driven text-to-image generation.
