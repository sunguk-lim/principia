---
id: parameter-patch-manifest
title: "Parameter-Patch Manifest"
summary: "A parameter-patch manifest binds a tensor intervention to an exact base checkpoint, ordered operations and verified loaded artifact so the change is reproducible and reversible."
type: concept
tags: [ml/model-portability]
prereqs: [model-parameter-editing, dataset-lineage]
sources: [https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html, https://huggingface.co/docs/safetensors/index]
status: explained
created: 2026-11-10
updated: 2026-11-10
---

# Parameter-Patch Manifest

## Meaning

A parameter-patch manifest records what to change, what artifact to change and how to verify the result. A model name or an edit script alone is insufficient: the same tensor name can have a different shape, dtype or value in another checkpoint. This is an intervention contract, not a proof of model quality.

## Mechanism

Bind the patch to the exact checkpoint and tokenizer/configuration revisions, with retrievable content hashes. For each ordered operation record tensor name, expected shape and dtype, index convention, update data and whether the operation adds, replaces or scales values. Specify preconditions, operation order and expected post-edit tensor or artifact hashes. [[model-parameter-editing]] explains the behavioral intervention; [[dataset-lineage]] motivates preserving inputs, transformation identity and outputs rather than mutable names alone.

PyTorch's state dictionary maps named parameters and registered buffers to tensors; preserving weights does not necessarily preserve every inference setting or optimizer state. Safetensors provides a tensor storage format, not an application-level patch protocol or semantic validation. The manifest described here is a general design pattern, not a claim that either library standardizes every field above. Preserve a baseline or original slices for rollback, and verify a fresh load of the final artifact.

## One example

An invented patch adds 0.25 to column 3 of a named tensor in checkpoint A. Reapplying it changes the value by 0.50 overall, so addition is not idempotent. A manifest requiring A's original tensor hash rejects the second application. A replacement patch can be idempotent in value yet still target the wrong revision; its base precondition remains necessary. Record the index as zero-based and verify the shape before writing, because “column 3” alone does not settle those choices.

## Check your understanding

Does a matching artifact hash guarantee identical generated text? No. It verifies preserved bytes, not runtime determinism or correctness. Record evaluation code, precision, hardware-relevant settings and random-generation protocol separately. A reverse arithmetic update can lose information after rounding; restoring preserved original values is stronger than assuming subtraction always recovers the baseline.

## Prerequisites

- [[model-parameter-editing]]
- [[dataset-lineage]]

## Sources

- <https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html>
- <https://huggingface.co/docs/safetensors/index>
