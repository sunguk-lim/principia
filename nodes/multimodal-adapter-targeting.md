---
id: multimodal-adapter-targeting
title: Multimodal Adapter Targeting
summary: Multimodal adapter targeting chooses whether LoRA updates the vision encoder, language decoder, or both, based on observed perception versus output-format errors and matched-budget ablations.
type: concept
tags: [ml/training]
prereqs: [lora, multimodal-input-contract, fine-tuning]
sources: [https://huggingface.co/docs/peft/main/package_reference/lora, https://huggingface.co/docs/peft/main/en/task_guides/lora_based_methods]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Multimodal Adapter Targeting

## Summary

In a vision-language model, applying [[lora]] is not one binary choice. Adapters may update the vision tower, the language decoder, selected projections in either, or both. **Adapter targeting** decides where the task-specific trainable capacity goes while the pretrained weights remain frozen.

## Grounded explanation

An image-to-LaTeX error can arise from visual recognition, the mapping from perceived symbols to tokens, or output-format behavior. A mistaken Greek letter suggests a perception or cross-modal alignment problem; added commentary around otherwise correct LaTeX suggests an output-contract problem. Neither observation alone localizes the fault to one module. The [[multimodal-input-contract]] and processor must be held fixed while comparing adapter placements.

Start with a language-only adapter because it is often cheaper and easier to fit. Compare it with a vision-only or vision-plus-language adapter when held-out errors indicate that the image representation may need adaptation. Keep dataset, rank or parameter budget, training steps, optimizer, and decoding policy documented; extra trainable parameters are an alternative explanation for improvement. Larger adapter coverage raises memory and overfitting risk, especially with a small specialized dataset. Frozen-vision training may preserve broad perception but fail on unusual notation.

For equation OCR, stratify held-out formulas by symbol, layout, resolution, and notation. Report exact-match and rendered-equivalence rates, specific symbol confusions, latency, peak memory, and robustness after domain shift. Inspect a baseline before training and run ablations rather than assuming that adapting both towers is always best. [[fine-tuning]] on private images also requires the usual data governance checks; local execution alone does not prove privacy or security.

## Prerequisites

- [[lora]]
- [[multimodal-input-contract]]
- [[fine-tuning]]

## Sources

- [PEFT LoRA reference](https://huggingface.co/docs/peft/main/package_reference/lora): configurable target modules.
- [PEFT LoRA methods guide](https://huggingface.co/docs/peft/main/en/task_guides/lora_based_methods): adapter training in vision tasks.
