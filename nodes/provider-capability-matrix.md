---
id: provider-capability-matrix
title: Model-Provider Capability Matrix
summary: A model-provider capability matrix records verified request, response, modality, tool, training, cost, and failure semantics for a workload instead of assuming API-shape compatibility implies portability.
type: concept
tags: [ml/model-portability]
prereqs: [tool-call-execution-contract, structured-output, measurement]
sources: [https://developers.openai.com/api/docs/guides/images-vision, https://platform.claude.com/docs/en/build-with-claude/vision, https://openrouter.ai/docs/guides/features/server-tools]
status: explained
created: 2026-10-03
updated: 2026-10-03
---

# Model-Provider Capability Matrix

## Summary

A common chat endpoint can hide materially different capabilities. A **provider capability matrix** is a tested mapping from a workload's requirements to each model, provider, and endpoint revision, rather than a table copied from marketing pages.

## Grounded explanation

Start with requirements: accepted text, image, or audio formats; output constraints through [[structured-output]]; tool-call behavior under [[tool-call-execution-contract]]; context limits; training or fine-tuning support; privacy terms; availability; and cost. Mark each cell supported, unsupported, conditional, or untested, and attach the exact model revision, endpoint, provider route, and test date. A model can support image input through one API while another route accepts only text or URL-hosted images. A uniform JSON shape does not make those routes equivalent.

Use a small conformance suite with valid and invalid examples. For tool calls, compare schema adherence, call IDs, parallel calls, timeout, retry, and result ordering. For modalities, test file type, size, encoding, and provider-specific content blocks. For structured outputs, test refusals and malformed input. Price comparisons must include input/output mix, cache, retries, and rejected work under [[measurement]], not just a quoted token rate.

Choose a minimal subset that meets the application contract, then run representative task evaluations for accuracy and latency. Re-run the matrix after model, SDK, API version, or routing changes. Keep unknown cells unknown: a provider documentation page is a claim about support, not evidence that a specific application path passes its acceptance tests.

## Prerequisites

- [[tool-call-execution-contract]]
- [[structured-output]]
- [[measurement]]

## Sources

- [OpenAI vision guide](https://developers.openai.com/api/docs/guides/images-vision): modality and endpoint distinctions.
- [Anthropic vision guide](https://platform.claude.com/docs/en/build-with-claude/vision): provider-specific image input forms.
- [OpenRouter Server Tools](https://openrouter.ai/docs/guides/features/server-tools): hosted versus user-defined tool behavior.
