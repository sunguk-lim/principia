---
id: api-key-usage-guardrail
title: API-Key Usage Guardrail
summary: An API-key usage guardrail binds spending, model access, provider, and data-policy limits to a credential's request path with explicit assignment and fail-closed enforcement.
type: concept
tags: [ml/model-portability]
prereqs: [capabilities, measurement]
sources: [https://openrouter.ai/docs/guides/features/guardrails]
status: explained
created: 2026-10-03
updated: 2026-10-03
---

# API-Key Usage Guardrail

## Summary

An API key authenticates a caller, but a **usage guardrail** narrows what that caller may spend or invoke. A declared policy is not effective until it is assigned to the key, member, or workspace that serves the request.

## Grounded explanation

Treat a key as a scoped [[capabilities|capability]]: it should authorize only the required models, providers, regions, and budget. A policy may cap spend per period and intersect allowlists across account, workspace, member, and key scopes. More specific assignments should narrow, not silently broaden, the effective authority. The gateway needs an explicit precedence rule and a fail-closed response for a disallowed model, provider, region, or exhausted budget.

Budget accounting is not trivial. Decide whether limits include cached tokens, retries, batch requests, provider-billed BYOK traffic, and in-flight usage that has not yet settled. A daily cap that checks only completed invoices can overshoot under concurrent calls. Separate hard rejection limits from alerts; an alert is observability, not enforcement. Record the policy version and effective scope with each authorization decision, without logging the secret key itself.

Test assignment and inheritance, lower-level restriction, period reset, concurrent overspend, rotated keys, unavailable providers, and denied requests. Use [[measurement]] to compare billable usage with policy counters and audit logs. Verify the provider's current implementation and contract before relying on a particular budget or privacy rule. The design protects the request path; it does not establish that downstream providers obey a retention promise.

## Prerequisites

- [[capabilities]]
- [[measurement]]

## Sources

- [OpenRouter Guardrails](https://openrouter.ai/docs/guides/features/guardrails): assignment, budget, allowlist, privacy, and region policy behavior.
