---
id: idempotent-operation-key
title: Idempotent Operation Key
summary: An idempotent operation key binds retries of one logical action to one recorded outcome under an explicit scope, payload and retention contract.
type: concept
tags: [distributed-systems/reliability]
prereqs: [transaction, key-value-store]
sources: [https://docs.stripe.com/api/idempotent_requests]
status: explained
created: 2026-10-21
updated: 2026-10-21
---

# Idempotent Operation Key

## Meaning

An idempotent operation key identifies retries of the same intended action. It is not merely a hash of content: identical payloads can represent two distinct legitimate actions, while one action can have several network attempts.

## Mechanism

Persist a key before dispatch. A server-side [[key-value-store]] or equivalent record binds its namespace and key to an input fingerprint, execution state and eventual result. Concurrent claims require atomic coordination, such as a [[transaction]] enforcing a unique key. Define what a duplicate sees while an operation is running, after completion, after failure and after retention expires.

Reusing a key with a different input must follow an explicit contract, normally rejection rather than silently returning an unrelated result. Scope keys by relevant account and operation boundaries. A sequential check followed by an uncoordinated write is not atomic duplicate suppression.

The effect boundary matters. Recording a local claim cannot make a non-idempotent remote action exactly-once. A worker can die after the remote effect but before the local receipt. Use the provider's idempotency contract or a status reconciliation path; a stuck local record alone cannot reveal whether the effect occurred.

Stripe's API v1 documents cached outcomes, parameter comparison and retention of at least 24 hours; pruned keys can denote a new request. Its API v2 documents different retry semantics. These are concrete contracts, not universal properties of every header named Idempotency-Key.

## Worked example

A user requests a 20-unit refund. The host persists operation `refund-17` with the exact payment and amount, then sends that key to an API supporting deduplication. A timeout occurs after the provider commits the refund. Retrying with `refund-17` and the same payload retrieves the recorded outcome rather than creating another refund.

A second deliberate 20-unit refund needs a new logical-operation key. Reusing `refund-17` with a 30-unit payload must not be accepted as the same action. After provider retention expires, reconcile first rather than assuming the old protection still exists.

## Check your understanding

**Question:** Does checking a local completed table before sending guarantee exactly-once effects? **Answer:** No; races, crashes and remote execution require a coordinated contract.

## Prerequisites

- [[transaction]]
- [[key-value-store]]

## Sources

- <https://docs.stripe.com/api/idempotent_requests>
