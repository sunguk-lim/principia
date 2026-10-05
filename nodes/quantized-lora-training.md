---
id: quantized-lora-training
title: Quantized LoRA Training
summary: Quantized LoRA training freezes low-precision pretrained weights while optimizing small adapters, reducing base-weight memory but not eliminating activation, optimizer, or modality-specific memory costs.
type: concept
tags: [ml/training]
prereqs: [lora, quantization, mixed-precision-training]
sources: [https://arxiv.org/abs/2305.14314, https://huggingface.co/docs/peft/main/developer_guides/quantization]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Quantized LoRA Training

## Summary

**Quantized LoRA training** stores a frozen pretrained model in low precision and trains only low-rank adapter weights. It is useful when full-precision base weights would consume too much accelerator memory, but a claimed “single-GPU fit” remains dependent on sequence length, image tokens, batch size, optimizer state, and runtime implementation.

## Grounded explanation

[[lora]] avoids updating most base parameters. [[quantization]] reduces the bytes used to store those frozen parameters. The forward pass uses the low-precision base plus the trainable adapter; the gradient path updates adapter parameters, not quantized base weights. In QLoRA-style methods, compute may occur in a higher precision than storage, so [[mixed-precision-training]] and numerical stability still matter.

A memory budget must account separately for quantized weights and metadata, adapter weights and optimizer state, activations, image or text tokens, temporary kernels, and safety headroom. Offloading selected components to CPU can lower peak GPU memory but add transfer latency. A model that loads successfully may still fail on a long example during backward propagation. Rank, target modules, gradient accumulation, checkpointing, and batch shape all change the trade-off.

Compare a full-precision adapter baseline when feasible, a quantized-base adapter, and smaller-model alternatives on the same held-out task. Report peak allocated and reserved memory, throughput, training stability, output quality, and total cost. Vary sequence/image sizes and inspect rare failures. Quantization is a capacity technique, not proof that a particular checkpoint, license, or benchmark figure from a newsletter is correct.

## Prerequisites

- [[lora]]
- [[quantization]]
- [[mixed-precision-training]]

## Sources

- [QLoRA paper](https://arxiv.org/abs/2305.14314): quantized frozen base with trainable adapters.
- [PEFT quantization guide](https://huggingface.co/docs/peft/main/developer_guides/quantization): implementation considerations.
