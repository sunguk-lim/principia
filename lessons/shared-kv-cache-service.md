# Shared KV-Cache Service

## Meaning

A shared KV-cache service manages reusable attention state outside any one inference worker. Several workers can consult the same store instead of each recomputing and retaining a private copy. It changes the ownership and lifetime of cached state, not the mathematics that permits [[prefix-caching]]. Tiering describes where state lives; sharing describes which workers can access it.

## Mechanism

An independent [[process]] receives lookup, store and retrieve operations. A worker identifies a compatible prefix, checks availability, restores its blocks into usable device state and computes the unmatched suffix. The cache service can outlive an engine restart, provided its own state survives; a separate process alone does not guarantee persistence or availability. A node-local shared service also does not automatically create a cluster-wide store.

Keys must distinguish model and adapter revisions, exact tokens, relevant positional/mask state and cache representation. A [[retrieval-authorization-boundary]] restricts which callers may reuse the evidence-derived state. A match without compatible representation or permission is not a usable hit. The [[tiered-kv-cache]] cost model still applies: restored bytes have to traverse a real path before computation can consume them.

## Worked example

Assume worker A computed a compatible prefix and then exited. Worker B receives the same authorized prefix. Recomputing would cost 180 ms. A shared service needs 10 ms lookup, 65 ms restoration and 15 ms setup: 90 ms total, saving 90 ms on this assumed serial path. If congestion raises restoration to 210 ms, the total is 235 ms and recomputation wins by 55 ms. The same cache hit can therefore help or hurt depending on measured movement cost. Neither example includes suffix processing or queueing, so neither is a complete request-time prediction.

## Check your understanding

Does a separate cache process guarantee a warm request after any crash? No. The service, backend, index, compatible representation and authorization must all still permit restoration; otherwise fall back safely.
