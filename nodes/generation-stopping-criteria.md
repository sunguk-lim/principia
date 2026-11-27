---
id: generation-stopping-criteria
title: "Generation Stopping Criteria"
summary: "Generation stopping criteria terminate a decoding process on a budget, terminal token or matched sequence, without proving that the returned content is complete or valid."
type: concept
tags: [ml/llm/inference]
prereqs: [subword-tokenization, llm-sampling-controls]
sources: [https://huggingface.co/docs/transformers/main_classes/text_generation, https://platform.openai.com/docs/api-reference/chat/create]
status: explained
created: 2026-11-28
updated: 2026-11-28
---

# Generation Stopping Criteria

## Meaning

A stopping criterion decides when generation ends. It is separate from the model's prediction that an answer is good. A run may end because it reached an output budget, emitted an end token, matched a configured sequence, timed out or was cancelled. The application must distinguish these outcomes before accepting the response.

## Mechanism

A next-token generator repeatedly chooses a token using [[llm-sampling-controls]]. [[subword-tokenization]] determines how those tokens decode to text. After each relevant update, the generation controller checks its terminal conditions. A token limit bounds work; an end-of-sequence token is a model-produced termination signal; a stop string ends generation when the matching contract detects it. Streaming can require buffering enough trailing text to avoid exposing a sequence the API promises to exclude.

Read the exact budget definition. A maximum number of new tokens differs from a maximum total length including the prompt. Some reasoning APIs count internal reasoning and visible output together. A generous maximum is a ceiling, not a request to consume every token. Conversely, a low ceiling can cut a necessary answer short. Parameter support and finish-reason vocabulary vary by model and API.

## One example

Suppose the intended output is `{"city":"Oslo","days":3}`. A budget ending after `{"city":"Oslo"` returns an incomplete object, even if every generated token was plausible. Raising the ceiling permits completion but does not force it. Now configure a stop string `END`. A generated field value `WEEKEND` contains that substring, so a matcher with ordinary substring semantics can terminate inside the data. The correct test is the documented matching rule, not the developer's intention that `END` be a standalone marker.

## Boundaries and validation

Stop strings delimit output; they do not enforce balanced brackets, a schema, factual grounding or permission for a tool action. Inspect finish metadata, validate the completed content and reject or repair incomplete results using a bounded policy. A normal stop reason may combine end-token and configured-stop cases; do not infer more than the response exposes.

Test no-match, early-match, multiple-match, boundary-spanning and multibyte cases with the actual tokenizer and streaming path. Check whether the stop sequence is returned, whether partial buffered text leaks, and how limits count reasoning tokens. Measure completeness, invalid-output rate, actual tokens and latency across budget settings.

**Check:** Does a stop at a closing brace establish valid JSON? No. The preceding text may be malformed, truncated at an inner object or inconsistent with the required schema.

## Prerequisites

- [[subword-tokenization]]
- [[llm-sampling-controls]]

## Sources

- <https://huggingface.co/docs/transformers/main_classes/text_generation>
- <https://platform.openai.com/docs/api-reference/chat/create>
