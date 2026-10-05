# Multimodal Adapter Targeting

## Meaning

In a vision-language model, applying [[lora]] is not one binary choice. Adapters may update the vision tower, the language decoder, selected projections in either, or both. **Adapter targeting** decides where the task-specific trainable capacity goes while the pretrained weights remain frozen.

## Mechanism

An image-to-LaTeX error can arise from visual recognition, the mapping from perceived symbols to tokens, or output-format behavior. A mistaken Greek letter suggests a perception or cross-modal alignment problem; added commentary around otherwise correct LaTeX suggests an output-contract problem. Neither observation alone localizes the fault to one module. The [[multimodal-input-contract]] and processor must be held fixed while comparing adapter placements.

Start with a language-only adapter because it is often cheaper and easier to fit. Compare it with a vision-only or vision-plus-language adapter when held-out errors indicate that the image representation may need adaptation. Keep dataset, rank or parameter budget, training steps, optimizer, and decoding policy documented; extra trainable parameters are an alternative explanation for improvement. Larger adapter coverage raises memory and overfitting risk, especially with a small specialized dataset. Frozen-vision training may preserve broad perception but fail on unusual notation.

## One example

For equation OCR, compare language-only LoRA with adapters in both the vision and language modules under a matched parameter and compute budget.

## Check your understanding

**Question:** Can one mistaken symbol prove the vision tower needs training?

**Answer:** No. The error could arise in perception, alignment, or decoding; use ablations.
