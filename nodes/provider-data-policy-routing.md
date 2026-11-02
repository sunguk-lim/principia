---
id: provider-data-policy-routing
title: Provider Data-Policy Routing
summary: Provider data-policy routing filters eligible inference endpoints by retention, training, and logging rules before applying availability or cost preferences.
type: concept
tags: [ml/model-portability]
prereqs: [load-balancing, api-key-usage-guardrail]
sources: [https://openrouter.ai/docs/guides/features/in-region-routing, https://openrouter.ai/docs/guides/features/zdr, https://openrouter.ai/docs/guides/features/guardrails]
status: explained
created: 2026-10-03
updated: 2026-11-03
---

# Provider Data-Policy Routing

## Summary

A gateway may offer several providers for one model, but they can have different retention, training-use, cache, and logging terms. **Data-policy routing** removes endpoints that violate a declared policy before optimizing price or latency.

## Grounded explanation

Represent policy at endpoint granularity, not as a blanket property of the model slug. A zero-data-retention request can require a provider whose current endpoint terms permit no post-response storage, while account policy may additionally prohibit training use. An [[api-key-usage-guardrail]] can enforce defaults, and a per-request constraint can narrow them. The effective candidate set is their intersection; [[load-balancing]] chooses only among eligible endpoints. If the set is empty, fail visibly rather than silently relaxing the policy.

The path also includes gateway logs, caches, observability, server tools, and downstream processors. “No training” and “zero retention” are not synonyms, and neither says whether transient processing, abuse monitoring, billing records, or legal holds are in scope. Document those boundaries from current primary terms and a contract where stakes require it.

Test endpoint metadata refresh, provider fallback, unavailable eligible routes, per-request override, key-level policy, and mixed regions. Audit actual endpoint selection and data flows without logging private prompts unnecessarily. A policy flag is a routing input and enforcement claim, not by itself proof that every organization in the path complied.

## Scope, exceptions and current policy

The current OpenRouter documentation makes request-level ZDR enforcement additive: a request can enable the restriction but cannot switch off an account or guardrail requirement. “ZDR enabled” still needs its exact policy profile. The documentation distinguishes strict zero retention from a separately allowed safety-retention mode; a route accepted under the latter is not evidence of strict zero retention. In-memory prompt caching is also treated separately by that policy.

Gateway retention and upstream endpoint retention are separate checks. OpenRouter documents exceptions for content flagged for CSAM review, reporting and required legal preservation, with an October 27, 2026 screening update notice. That statement is a documented policy scope, not an independent audit that screening or deletion behaved as promised on a particular request. The routing restriction does not generally cover separately enabled plugins and server tools. Verify current terms, endpoint-specific classification, organizational settings and the complete processing path rather than repeating a blanket “nothing is retained” assertion.

For a concrete eligibility test, suppose endpoints A and B both advertise no training use, but only A meets the required strict-retention rule. If A becomes unavailable, B is still ineligible; no-training status does not repair a retention-policy violation. If an operator separately permits safety retention, record that changed contract instead of describing the fallback as an unchanged strict policy.

## Regional processing is an independent constraint

Retention and processing location are distinct policy dimensions. Filter for both before cost or availability selection; a zero-retention endpoint can still process data in an unacceptable jurisdiction. OpenRouter documents regional ingress domains that restrict shared inference endpoints and fail when an eligible route is unavailable rather than silently moving shared inference elsewhere. Its current Europe boundary includes the EU/EEA, the UK and Switzerland, not only EU member states. Check the exact contractual geography rather than inferring it from a hostname.

The boundary is not every related record or destination. Account and operational records are handled separately, and customer-configured trace destinations and bring-your-own-key deployments require their own location checks. A regional gateway cannot relocate a cloud resource provisioned by the customer. Provider-specific routing and declaration rules differ; verify the actual deployment and invocation path rather than relying only on a region label. Regional availability of tools also differs from inference availability.

For a simple intersection test, endpoint A meets retention but not region, B meets region but not retention, and C meets both. Only C is eligible. If C fails, neither A nor B is an unchanged-policy fallback. Test empty intersections, ingress restrictions and observed endpoint selection, while distinguishing a documented vendor guarantee from independent evidence of compliance.

## Prerequisites

- [[load-balancing]]
- [[api-key-usage-guardrail]]

## Sources

- [OpenRouter Zero Data Retention](https://openrouter.ai/docs/guides/features/zdr): endpoint-level ZDR semantics and controls.
- [OpenRouter Guardrails](https://openrouter.ai/docs/guides/features/guardrails): policy assignment and enforcement scope.

- <https://openrouter.ai/docs/guides/features/in-region-routing>
