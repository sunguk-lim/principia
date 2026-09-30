---
id: model-output-sensitive-data-filter
title: Model-Output Sensitive-Data Filter
summary: A model-output sensitive-data filter inspects generated content before release as a fallible defense layer, not a substitute for data minimization or access control.
type: concept
tags: [ml/agents]
prereqs: [training-data-extraction-risk, retrieval-authorization-boundary, measurement]
sources: [https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview]
status: explained
created: 2026-10-01
updated: 2026-10-01
---

# Model-Output Sensitive-Data Filter

## Summary

An **output filter** can catch some sensitive strings before a response is shown or streamed to a user. It is a backstop, not proof that the model lacks the data or that the request was authorized. Exact patterns miss paraphrases; learned classifiers can miss unusual formats and can block harmless text.

## Grounded explanation

Define protected data classes and the user's permitted disclosure scope. Inspect generated chunks before release, including streamed partial output, tool-call arguments, and structured fields when relevant. A rule can reliably match a known synthetic canary or a specified identifier format, but context matters for names, financial figures, or customer-specific facts. A classifier may capture semantic variants while adding calibration, model drift, and false-positive problems. Policy must distinguish “contains a number” from “contains an unauthorized secret.”

For example, a support assistant may quote a payment-card-like sequence from a retrieved document. A pattern filter can block the literal sequence, but the safer design is to exclude it during [[retrieval-authorization-boundary]] enforcement and minimize upstream records. If the sequence originated from weights, investigate [[training-data-extraction-risk]] and remediation. Output filtering alone cannot identify the origin.

With [[measurement]], test precision and recall on authorized synthetic examples, paraphrases, partial streams, role-crossing attacks, multilingual formats, and benign lookalikes. Measure false blocks, latency, and what was already emitted before the decision. Keep blocked content out of diagnostic logs or restrict those logs. Document the policy and escalation path; never advertise the filter as deterministic prevention of all sensitive disclosure.

## Prerequisites

- [[training-data-extraction-risk]]
- [[retrieval-authorization-boundary]]
- [[measurement]]

## Sources

- [Azure AI Content Safety overview](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview): primary description of content-analysis controls; the sensitive-data egress policy here is an independent systems application, not a claimed product guarantee.
