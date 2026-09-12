---
id: crawl-frontier
title: Crawl Frontier
summary: A crawl frontier turns discovered web links into eligible fetch work while preventing duplicate requests and enforcing independent per-origin pacing, so aggregate parallelism cannot overload one server.
type: concept
tags: [distributed-systems/web]
prereqs: [graph, queue, hash-set, http]
sources:
  - "https://www.rfc-editor.org/rfc/rfc9309.html"
  - "https://www.rfc-editor.org/rfc/rfc9110.html"
  - "https://www.rfc-editor.org/rfc/rfc3986.html"
status: explained
created: 2026-09-13
updated: 2026-09-13
---

# Crawl Frontier

## Summary

A web crawler repeatedly fetches a page, extracts links, and follows those links, so its pending work grows like a [[graph]] traversal. The **crawl frontier** is the control layer between link discovery and network fetching. It decides whether a discovered URI is already represented, whether the crawler is allowed to request it, which origin may receive a request now, and which eligible URI should go next. Its central invariant is that global worker parallelism never bypasses an origin's local request budget: one busy site can contribute a million pending links without receiving more simultaneous or more frequent requests than its own policy permits.

## Grounded explanation

### Why one global queue is insufficient

Suppose 200 workers share one FIFO [[queue]]. If its first 200 entries all name resources on `https://docs.example`, all workers can issue an [[http]] request to that origin at once. The queue preserves discovery order, but it expresses no constraint shared by requests to the same server. A global limit of 200 concurrent requests therefore says nothing about whether one origin receives 1 request or all 200.

The frontier separates two decisions:

1. **Membership:** should this discovered URI become work at all?
2. **Eligibility:** if it is work, when may its origin issue another request?

For membership, the frontier stores a normalized request key in a [[hash-set]]. Safe normalization applies equivalences defined by URI and HTTP semantics, such as normalizing a scheme or host's case where allowed and removing dot segments. It does **not** blindly remove query parameters or merge paths: two syntactically similar URIs can identify different resources, so application-specific equivalence needs evidence. Content fingerprints can detect duplicate representations after retrieval, but they cannot recover the bandwidth or server work already spent; known URI aliases are therefore best collapsed before enqueueing.

For eligibility, the frontier groups pending URIs by **origin**—the HTTP tuple of scheme, host, and port—and keeps one local queue plus state for each origin. That state includes a next-eligible time, current in-flight count, retry or backoff state, and the cached result of the Robots Exclusion Protocol. RFC 9309 defines how a crawler selects and applies `robots.txt` groups, handles access results, and caches the file; it also states that those rules are not access authorization. Robots handling is consequently one input to the frontier, not a substitute for permission, authentication, contractual policy, or operator-defined load limits.

A second queue contains only origins that are eligible now. A worker removes one eligible origin, removes at most one URI from that origin's local queue, records the request as in flight, and sends it. When the request finishes, the frontier updates that origin's state and schedules its next eligibility. This two-level structure preserves high aggregate throughput across many origins while bounding pressure on each origin independently.

### Worked instance: six workers, one popular origin

Assume six workers and the following discovered work after safe normalization:

- origin `A`: `/a1`, `/a2`, `/a3`, `/a4`, `/a5`, `/a6`;
- origin `B`: `/b1`, `/b2`;
- origin `C`: `/c1`.

Each origin permits one in-flight request, and its next request becomes eligible two time units after the previous request starts. At time `0`, the eligible-origin queue is `[A, B, C]`. Only three of the six workers receive work:

| time | dispatched | remaining local queues | next eligible |
|---|---|---|---|
| `0` | `A:/a1`, `B:/b1`, `C:/c1` | `A:[a2..a6]`, `B:[b2]`, `C:[]` | `A=2`, `B=2`, `C=2` |
| `1` | nothing | unchanged | unchanged |
| `2` | `A:/a2`, `B:/b2` | `A:[a3..a6]`, `B:[]` | `A=4`, `B=4` |
| `4` | `A:/a3` | `A:[a4..a6]` | `A=6` |

The popular origin `A` has six times as much queued work as `C`, but it never has two requests in flight and never starts requests less than two units apart. Unused global workers remain available for other origins that become eligible; they are not permission to violate `A`'s local bound. This is the invariant a single global queue lacks.

### Completion, failures, and recrawling

A response does not always mean the same resource bytes should be stored again. HTTP validators such as `ETag` and `Last-Modified` let a later request be conditional; a `304 Not Modified` response confirms that the stored representation is still current without retransmitting its content. The frontier can schedule revisits from observed change intervals and freshness requirements, then use validators where available. A frequently changing resource may return sooner than a stable one, while repeated errors or overload responses should delay further attempts under a bounded retry policy.

The crawler should measure both usefulness and imposed load. Useful frontier metrics include newly accepted canonical resources per request, duplicate classes, conditional-request outcomes, and freshness lag. Load metrics include requests and in-flight connections per origin, response latency, error and retry rates, and the maximum request rate observed for any one origin. Aggregate pages per second is still useful for capacity planning, but it cannot prove deduplication quality or per-origin restraint.

## Prerequisites

- [[graph]]
- [[queue]]
- [[hash-set]]
- [[http]]

## Sources

- RFC 9309, *Robots Exclusion Protocol*.
- RFC 9110, *HTTP Semantics* (origins, URI comparison, validators, and conditional requests).
- RFC 3986, *Uniform Resource Identifier (URI): Generic Syntax* (normalization and comparison).
