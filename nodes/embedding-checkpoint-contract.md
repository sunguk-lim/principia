---
id: embedding-checkpoint-contract
title: Embedding Checkpoint Contract
summary: An embedding checkpoint contract binds available encoders, projections, preprocessing and output geometry to the concrete artifact loaded rather than inheriting every capability of a model family.
type: concept
tags: [ml/model-portability]
prereqs: [text-embedding-api-contract, post-training-quantization, tensor]
sources: [https://huggingface.co/google/embeddinggemma-300m, https://github.com/openai/CLIP]
status: explained
created: 2026-11-11
updated: 2026-11-11
---

# Embedding Checkpoint Contract

## Meaning

A model family's capabilities are not the capabilities of every file distributed under its name. An embedding checkpoint is usable only when the loaded tensors, encoders, preprocessing and runtime implement the required input-to-vector contract. A text-only quantized export cannot acquire a vision encoder merely by changing an input field.

## Mechanism

Record artifact identity and revision, [[tensor]] inventory, tokenizer or image preprocessing, pooling or projection, output dimensions, normalization and supported input modalities. A [[text-embedding-api-contract]] checks observable batch identities and geometry; the checkpoint contract additionally asks whether the actual loaded model can produce that geometry from the intended input. A successful load is weaker than correct modality support.

[[post-training-quantization]] can change weight representation and numerical behavior. It does not add absent towers, projection layers or preprocessing. An export may deliberately include only one encoder of a multimodal family; another may retain the whole model under a different precision. Inspect its model card and execution path, then test the exact artifact on known paired inputs. Runtime format compatibility and retrieval compatibility are separate gates.

The official EmbeddingGemma 300M model card documents text input and text vectors; it is not evidence for a different checkpoint or a newer multimodal product. CLIP's official implementation instead exposes paired image/text encoders and image preprocessing. These are examples of explicit contracts, not a claim that their outputs can be mixed across families or revisions.

## One example

An invented model family has a text encoder, image encoder and joint projection. Export T contains only text-encoder tensors and returns 768 coordinates. Export M contains both encoders and the trained projections, also returning 768 coordinates. T passing a text embedding smoke test does not validate text-to-image retrieval. Feeding images requires the missing image path, and comparing T's query coordinates with M's stored image vectors requires an independently documented compatible geometry. Equal dimensions are only a shape check.

## Check your understanding

Does a four-bit file size establish full multimodal support? No. Verify components, actual preprocessing, model revision, finite outputs and held-out cross-modal matches. Compare with the unquantized artifact under the same query/corpus contract. Keep unsupported-modality errors explicit and re-embed when changing geometry; do not silently substitute text captions while reporting image embedding.

## Prerequisites

- [[tensor]]
- [[text-embedding-api-contract]]
- [[post-training-quantization]]

## Sources

- <https://huggingface.co/google/embeddinggemma-300m>
- <https://github.com/openai/CLIP>
