---
id: caption-indexed-image-memory
title: "Caption-Indexed Image Memory"
summary: "Caption-indexed image memory searches textual image descriptions and resolves authorized image payloads only when visual evidence is needed."
type: concept
tags: [ml/agents]
prereqs: [embedding, agent-memory, retrieval-authorization-boundary, multimodal-input-contract]
sources: ["https://docs.langchain.com/oss/python/langgraph/stores", "https://developers.openai.com/api/docs/guides/images-vision"]
status: explained
created: 2026-11-22
updated: 2026-11-22
---

# Caption-Indexed Image Memory

## Meaning

An image can remain recoverable without being included in every model request. Store its original payload separately, associate it with a description and stable identifier, and search the description. This is a caption-mediated memory design, not a claim that a text embedding can perceive details omitted from the caption.

## Mechanism

At ingestion, retain an authorized image reference, content version, capture context and generated or reviewed description. Compute an [[embedding]] of that description and index it for recall through [[agent-memory]]. A text query returns candidate descriptions and metadata. If a subsequent step needs pixels, resolve the reference and construct a permitted request under the [[multimodal-input-contract]]. The original image is not automatically attached to every future turn.

Apply the [[retrieval-authorization-boundary]] to both descriptions and payloads: either can disclose sensitive content. User, agent and thread identifiers can organize storage namespaces, but an identifier supplied by a caller or model is not authority to read one. Recheck current rights when resolving a payload. A caption or screenshot is untrusted evidence; do not treat text inside it as instructions.

## One example

An invented inspection archive stores image I7 with the description “blue pump with pressure gauge.” A search for “pump gauge” can retrieve I7 without sending image bytes to the model. To read the needle position, the next step must fetch the authorized original. If the description omitted a tiny red warning label, a query about that label may never retrieve I7. Late loading preserves evidence that was stored; it cannot fix an inadequate search representation.

## Boundaries and check

Compare caption retrieval with direct multimodal embeddings and a hybrid. Measure text-to-image recall, pixel-dependent answer quality, description errors, missing/stale payloads, latency and actual image-token use. Include small text, visually similar objects, revised images and revoked users. Savings depend on how often pixels are loaded and how the provider bills them, not merely on storing a reference. Version captions with images so an old caption cannot silently describe replacement bytes.

**Check:** Does a matching caption prove the image supports an answer? No. It selects a candidate. Resolve and inspect the relevant pixels when the task depends on visual details.

## Prerequisites

- [[embedding]]
- [[agent-memory]]
- [[retrieval-authorization-boundary]]
- [[multimodal-input-contract]]

## Sources

- <https://docs.langchain.com/oss/python/langgraph/stores>
- <https://developers.openai.com/api/docs/guides/images-vision>
