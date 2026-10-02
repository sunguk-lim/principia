# Model-Provider Capability Matrix

## Meaning

A common chat endpoint can hide materially different capabilities. A **provider capability matrix** is a tested mapping from a workload's requirements to each model, provider, and endpoint revision, rather than a table copied from marketing pages.

## Mechanism

Start with requirements: accepted text, image, or audio formats; output constraints through [[structured-output]]; tool-call behavior under [[tool-call-execution-contract]]; context limits; training or fine-tuning support; privacy terms; availability; and cost. Mark each cell supported, unsupported, conditional, or untested, and attach the exact model revision, endpoint, provider route, and test date. A model can support image input through one API while another route accepts only text or URL-hosted images. A uniform JSON shape does not make those routes equivalent.

Use a small conformance suite with valid and invalid examples. For tool calls, compare schema adherence, call IDs, parallel calls, timeout, retry, and result ordering. For modalities, test file type, size, encoding, and provider-specific content blocks. For structured outputs, test refusals and malformed input. Price comparisons must include input/output mix, cache, retries, and rejected work under [[measurement]], not just a quoted token rate.

## Worked example

A project needs image input and parallel tool calls. Provider A accepts inline image bytes but serializes tool calls; provider B supports parallel calls but only fetches image URLs. A common chat schema conceals this difference. The matrix marks each exact endpoint conditionally supported and ties it to passing tests.

**Understanding check:** Why is an OpenAI-compatible request format insufficient evidence of workload portability?
