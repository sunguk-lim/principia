# Cache Aware Inference Routing

## Meaning

A load balancer that treats LLM replicas as interchangeable may send a repeated prompt to a replica without its cached prefix. **Cache-aware routing** estimates which replica can reuse the prefix and balances that benefit against the replica's current queue. It is a cluster-level choice, distinct from the [[inference-request-scheduling]] performed inside one server.

## Mechanism

[[prefix-caching]] stores KV blocks for identical token prefixes. Reuse is local to a replica unless blocks are shared or transferred. The router therefore needs an estimate of cache residency, request prefix identity, and server load. It can score a warm replica higher when saved prefill work exceeds the extra wait; when that replica is saturated, a cold replica may finish sooner despite recomputation. [[load-balancing]] is still necessary, but request count alone is a poor proxy when prompt lengths and cache states differ.

For example, two replicas serve a chat application. A returning conversation's system prompt and history are warm on A, while B has no matching blocks. Routing to A can reduce time to first token if A has headroom. If A already has a long queue, B may be preferable. The exact crossover depends on prefix length, model, batch composition, and queue dynamics. A router's cache index may lag eviction; it should tolerate stale entries and fall back safely rather than promising a hit.

## One example

Replica A has a cached shared prompt but a long queue; B is cold but idle. The router compares saved prefill time with extra waiting rather than always choosing A.

## Check your understanding

**Question:** Can a higher cache-hit rate by itself prove better routing?

**Answer:** No. It may increase queueing and tail latency.
