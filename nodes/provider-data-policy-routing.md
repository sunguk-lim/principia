---
id: provider-data-policy-routing
title: Provider Data-Policy Routing
summary: Provider data-policy routing filters eligible inference endpoints by retention, training, and logging rules before applying availability or cost preferences.
type: concept
tags: [ml/model-portability]
prereqs: [load-balancing, api-key-usage-guardrail]
sources: [https://openrouter.ai/docs/guides/features/zdr, https://openrouter.ai/docs/guides/features/guardrails]
status: explained
created: 2026-10-03
updated: 2026-10-03
---

# Provider Data-Policy Routing

## Summary

A gateway may offer several providers for one model, but they can have different retention, training-use, cache, and logging terms. **Data-policy routing** removes endpoints that violate a declared policy before optimizing price or latency.

## Grounded explanation

Represent policy at endpoint granularity, not as a blanket property of the model slug. A zero-data-retention request can require a provider whose current endpoint terms permit no post-response storage, while account policy may additionally prohibit training use. An [[api-key-usage-guardrail]] can enforce defaults, and a per-request constraint can narrow them. The effective candidate set is their intersection; [[load-balancing]] chooses only among eligible endpoints. If the set is empty, fail visibly rather than silently relaxing the policy.

The path also includes gateway logs, caches, observability, server tools, and downstream processors. “No training” and “zero retention” are not synonyms, and neither says whether transient processing, abuse monitoring, billing records, or legal holds are in scope. Document those boundaries from current primary terms and a contract where stakes require it.

Test endpoint metadata refresh, provider fallback, unavailable eligible routes, per-request override, key-level policy, and mixed regions. Audit actual endpoint selection and data flows without logging private prompts unnecessarily. A policy flag is a routing input and enforcement claim, not by itself proof that every organization in the path complied.

## Prerequisites

- [[load-balancing]]
- [[api-key-usage-guardrail]]

## Sources

- [OpenRouter Zero Data Retention](https://openrouter.ai/docs/guides/features/zdr): endpoint-level ZDR semantics and controls.
- [OpenRouter Guardrails](https://openrouter.ai/docs/guides/features/guardrails): policy assignment and enforcement scope.
