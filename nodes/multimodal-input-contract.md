---
id: multimodal-input-contract
title: Multimodal Model-Input Contract
summary: A multimodal input contract specifies how images, audio, text, and files are encoded, bounded, ordered, and interpreted at a model API boundary.
type: concept
tags: [ml/model-portability]
prereqs: [structured-output, embedding]
sources: [https://developers.openai.com/api/docs/guides/images-vision, https://developers.openai.com/api/docs/guides/audio, https://platform.claude.com/docs/en/build-with-claude/vision]
status: explained
created: 2026-10-03
updated: 2026-10-03
---

# Multimodal Model-Input Contract

## Summary

“Supports vision” or “supports audio” is too coarse for an application. The **multimodal input contract** specifies accepted content parts, encodings, size limits, timing, and output semantics for each model and endpoint.

## Grounded explanation

For vision, a request may carry an image as encoded bytes, a URL, or a provider file reference. Each choice has different retention, access, size, and failure behavior. Image resolution and preprocessing affect whether small text or spatial details survive. For audio, distinguish a completed-file transcription, streaming transcript, and live bidirectional conversation; they have different latency and turn-taking contracts. The model may internally form an [[embedding]], but the API contract concerns observable input and output, not an assumed shared representation.

Document content-part order, supported MIME types, file-size ceilings, truncation, timestamps, and whether the provider fetches remote URLs. A URL may be inaccessible, change after submission, or expose private data to a different service. Test with controlled fixtures, not personalized links. Use [[structured-output]] only for the response shape; it cannot guarantee that the model perceived the relevant frame or sound correctly.

Evaluate modality-specific errors: OCR accuracy at small type, chart interpretation, accented speech, background noise, overlapping speakers, and mixed text-plus-image reasoning. Compare with an explicit pipeline such as OCR or transcription followed by a text model. Measure quality, latency, privacy exposure, and cost under the same task set. Recheck model and endpoint revisions because a shared API family does not imply shared modality support.

## Prerequisites

- [[structured-output]]
- [[embedding]]

## Sources

- [OpenAI Images and vision](https://developers.openai.com/api/docs/guides/images-vision): image input paths and endpoint distinction.
- [OpenAI Audio and voice](https://developers.openai.com/api/docs/guides/audio): separate transcription, realtime, and speech workflows.
- [Anthropic Vision](https://platform.claude.com/docs/en/build-with-claude/vision): image content blocks and source options.
