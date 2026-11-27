---
id: online-feature-lookup
title: "Online Feature Lookup"
summary: "Online feature lookup retrieves entity-keyed current feature values outside model weights under explicit schema, freshness, failure and latency contracts."
type: concept
tags: [ml/systems]
prereqs: [hash-map, categorical-data-encoding, measurement]
sources: [https://docs.feast.dev/getting-started/components/online-store.md]
status: explained
created: 2026-11-28
updated: 2026-11-28
---

# Online Feature Lookup

## Meaning

Online feature lookup separates a model's learned computation from mutable attributes needed at prediction time. A service retrieves feature values using an entity key and feeds them through the model's fixed input contract. This can keep metadata current without encoding every change in weights, but it adds a dependency to the serving path.

## Mechanism

A [[hash-map]] provides the basic key-to-value abstraction: entity identifier in, feature record or missing result out. A production online store adds ingestion, materialization, timestamps, access control and availability behavior. Feast documents a store that holds the latest feature values per entity rather than historical versions. “Latest” in that store is not proof of freshness relative to the real event; ingestion may lag.

Apply [[categorical-data-encoding]] and other required transformations consistently with training. A returned category unknown to the fitted encoder still needs an explicit policy. A lookup solves attribute access, not automatic model understanding of a new identifier. Define schema version, missing-value semantics, freshness bounds, timeout and fallback before serving. Requests without approved access must not fetch another tenant's entity simply because the key exists.

## One example

A fictional model accepts product category and price band. A newly added product has no learned ID representation, but the store returns category `lamp` and band `medium`. The fitted encoder can use those attributes if their mapping is supported. If the key is absent, the service applies its trained unknown policy or declines the prediction. It must not silently use another product's record or wait indefinitely.

For an invented 20-millisecond request target, local processing takes 5 milliseconds and the lookup deadline is 8, leaving 7 for other work and variability. These toy allocations are not a latency guarantee. Under concurrency, queueing, retries and network tails can consume the margin even if the store's typical lookup is fast. An asynchronous API does not make waiting for a required result free.

## Validation and boundaries

Use [[measurement]] to record end-to-end tail latency, per-stage time, missing rate, staleness, cache behavior, quality and fallback frequency. Replay unknown keys, stale records, schema mismatches, dependency failure and recovery under load. Compare with embedded static attributes or a simpler local snapshot when their freshness and capacity suffice.

A latest-value online store is not a historical training dataset. Reproducing earlier decisions requires retaining the relevant values or versions under a separate record policy; current values alone can introduce future information into retrospective training.

## Prerequisites

- [[hash-map]]
- [[categorical-data-encoding]]
- [[measurement]]

## Sources

- <https://docs.feast.dev/getting-started/components/online-store.md>
