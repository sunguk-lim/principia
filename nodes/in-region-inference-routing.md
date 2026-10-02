---
id: in-region-inference-routing
title: In-Region Inference Routing
summary: In-region inference routing restricts request processing and eligible model endpoints to a declared geographic region and fails closed when no compliant route exists.
type: concept
tags: [ml/llm/inference]
prereqs: [load-balancing, tool-call-execution-contract]
sources: [https://openrouter.ai/docs/guides/features/in-region-routing, https://openrouter.ai/docs/guides/features/guardrails]
status: explained
created: 2026-10-03
updated: 2026-10-03
---

# In-Region Inference Routing

## Summary

A model's vendor address does not determine where an inference request is decrypted, processed, stored, or forwarded. **In-region inference routing** constrains the entire request path to permitted geography, including the gateway, provider endpoint, and any server-operated tools.

## Grounded explanation

The regional endpoint acts as an admission filter over eligible provider deployments. [[load-balancing]] may choose among those deployments, but must not silently fall back to a global endpoint when none is available. A fail-closed response makes that absence visible. A separate guardrail can prevent a key or workspace from accidentally using the global domain; merely offering a regional URL does not enforce that every caller uses it.

Trace the full path: client connection, TLS termination and decryption, routing service, inference host, tool execution, logs, caches, backup, and support access. A server tool is an external effect under a [[tool-call-execution-contract]], so it must be disabled or regionalized if its traffic could cross the boundary. The provider's current documentation and contract define the actual guarantee; a regional model catalog is a necessary availability check, not a legal attestation.

Test allowed and disallowed domains, unavailable models, fallbacks, server tools, and error paths. Audit region identifiers and endpoint inventory over time, and compare observed network and log destinations with the documented scope. Measure the latency, price, and availability trade-offs of the smaller regional pool. Do not infer compliance solely from a model name or an HTTP 200 response.

## Prerequisites

- [[load-balancing]]
- [[tool-call-execution-contract]]

## Sources

- [OpenRouter In-Region Routing](https://openrouter.ai/docs/guides/features/in-region-routing): regional endpoints, eligible providers, and fail-closed behavior.
- [OpenRouter Guardrails](https://openrouter.ai/docs/guides/features/guardrails): scope and assignment of data-region restrictions.
