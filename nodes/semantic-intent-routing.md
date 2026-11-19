---
id: semantic-intent-routing
title: "Semantic Intent Routing"
summary: "Semantic intent routing selects an eligible workflow from a request representation using explicit matching, ambiguity and fallback rules without granting execution authority."
type: concept
tags: [ml/agents]
prereqs: [embedding, cosine-similarity, decision-score-action-gate, agent-workflow-graph]
sources: [https://github.com/redis/redis-vl-python/blob/main/docs/user_guide/08_semantic_router.ipynb, https://docs.langchain.com/oss/python/langgraph/workflows-agents]
status: explained
created: 2026-11-20
updated: 2026-11-20
---

# Semantic Intent Routing

## Meaning

Semantic intent routing maps a request to a workflow using meaning-related features rather than only exact keywords. A route is an eligible task path, not a permission grant. Classifying “change my address” does not authorize a write or identify which person's record may be changed.

## Mechanism

One implementation uses an [[embedding]] for example requests for each route and compares the incoming request with those references using [[cosine-similarity]]. RedisVL's primary tutorial describes per-route references, distance thresholds and aggregation over matches. A model classifier is another implementation; the common design issue is turning uncertain evidence into a bounded dispatch decision.

A [[decision-score-action-gate]] separates matching, eligibility and action. First restrict routes to those allowed for the current user, deployment and tool capabilities. Then apply calibrated thresholds, conflict rules and an abstain/fallback path. A similarity distance is not automatically a probability of correct intent. Multiple plausible routes may require clarification or a deliberately bounded common procedure instead of selecting the nearest result unconditionally.

The selected [[agent-workflow-graph]] validates inputs and effects independently. Keep route references and workflow versions aligned, and make failures observable. A default route must not bypass region, data-policy, cost or tool constraints that disqualified the intended route. Untrusted request content may resemble an example closely while asking for a forbidden action; linguistic similarity cannot override authorization.

## One example

Suppose a router offers “check order status” and “cancel order.” A query says “don't cancel it; is it still shipping?” Nearest-neighbor matching may over-weight the word “cancel.” A held-out negation case reveals this error before deployment. If both route scores are plausible, a read-only status lookup or a clarification can be an authorized fallback, while silently calling cancellation is not. The appropriate fallback comes from the application contract, not the router's confidence alone.

## Check your understanding

Is a single correct paraphrase demonstration enough to tune a router? No. Evaluate confusion among similar intents, negation, changed identifiers, multi-intent requests, unsupported languages, distribution shift and out-of-scope inputs. Measure task-level wrong dispatch, abstentions, fallback cost and latency, including rare high-impact errors. Compare keyword rules, a small classifier, embedding references and a general model under the same eligible-route set. More elaborate routing is useful only when its errors and overhead are preferable to a simpler dispatch rule.

## Prerequisites

- [[embedding]]
- [[cosine-similarity]]
- [[decision-score-action-gate]]
- [[agent-workflow-graph]]

## Sources

- <https://github.com/redis/redis-vl-python/blob/main/docs/user_guide/08_semantic_router.ipynb>
- <https://docs.langchain.com/oss/python/langgraph/workflows-agents>
