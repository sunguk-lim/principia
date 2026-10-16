---
id: rate-limiting
title: Rate Limiting
summary: Rate limiting bounds requests or work admitted for an identity or resource over time, protecting shared capacity while introducing fairness and burst-policy trade-offs.
type: concept
tags: [networking/performance]
prereqs: [measurement, load-balancing]
sources: [https://developers.cloudflare.com/waf/rate-limiting-rules/]
status: explained
created: 2026-10-17
updated: 2026-10-17
---

# Rate Limiting

## Summary

**Rate limiting** decides whether a request may consume a shared service now. A rule needs a scope (user, credential, tenant, route, or provider), a measured quantity, a time policy, and a response when the allowance is exhausted. For AI APIs, requests alone can be a poor proxy for work: prompt and output tokens, concurrent generations, and GPU time can differ sharply.

## Grounded explanation

A fixed window counts events in an interval but can admit two bursts near a boundary. A sliding window smooths that artifact. A token bucket replenishes allowance at a rate and permits a bounded burst until its capacity is spent. These are admission policies, not [[load-balancing]]: distributing requests across workers does not enforce a customer's total allowance.

Choose the key from authenticated identity when available; client-supplied labels or IP address alone can mix distinct users or let one actor rotate identities. Define whether rejected work is queued, returned with a retry signal, or degraded to a cheaper tier. Distributed limiters need a consistency policy: local counters can temporarily oversubscribe a global cap, while centralized counters add latency or an availability dependency.

## Validation

Use [[measurement]] to test sustained rate, boundary bursts, fairness between tenants, retry behavior, and failure of the counter store. Measure accepted work, rejection rate, queue delay, tail latency, and downstream saturation. A low request rejection rate does not mean a token-heavy workload is within capacity.

## Prerequisites

- [[measurement]]
- [[load-balancing]]

## Sources

- [Cloudflare rate limiting rules](https://developers.cloudflare.com/waf/rate-limiting-rules/): match scope, counting, and action when a limit is exceeded.
