---
id: durable-event-inbox
title: Durable Event Inbox
summary: A durable event inbox records accepted triggers before dispatch and tracks recoverable attempts without confusing input deduplication with exactly-once external effects.
type: concept
tags: [distributed-systems/reliability]
prereqs: [queue, transaction, idempotent-operation-key]
sources: [https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html, https://docs.temporal.io/workflow-execution/timers-delays]
status: explained
created: 2026-11-18
updated: 2026-11-18
---

# Durable Event Inbox

## Meaning

A durable event inbox is the persisted boundary between accepting a trigger and executing work. A webhook, user message or due timer becomes a recoverable record before a worker treats it as accepted. A [[queue]] decouples arrival from processing; durability and explicit state add recovery rather than keeping the trigger only in a process's memory.

## Mechanism

Record an event identity scoped by its source, permitted payload, destination partition, arrival time and processing state. A uniqueness constraint can reject duplicate delivery of one source event without merging distinct events with equal text. Accept and commit before acknowledging receipt. A local [[transaction]] can atomically record acceptance or change an event from pending to claimed.

Workers claim attempts with an owner, expiry and monotonically advancing attempt or version. On success, commit the result and completion state. If a worker crashes, an expired claim becomes eligible for bounded retry. A visibility timeout is one concrete queue mechanism: AWS documents that undeleted SQS messages become visible again and that standard queues can still duplicate delivery during the timeout. “In flight” is therefore not proof of exclusive execution.

For ordered conversational state, enforce one active committer per partition or an equivalent version-checked protocol. A stale worker can remain alive after its claim expires. Reject its stale commits, and do not assume a local version can fence an arbitrary remote API. An [[idempotent-operation-key]] or outcome reconciliation must handle effects across that boundary. Source-event deduplication and effect deduplication solve different problems.

## Timer delivery through the same inbox

A one-shot timer names a future event, not a continuously running model. Persist its due time, target and stable identity, then enqueue the due event through the same acceptance path. A recurring schedule additionally needs an occurrence identity for each intended time. If the scheduler crashes after enqueueing but before recording dispatch, the repeated dispatch must retain that identity. Record intended and actual times separately. Define cancellation versus dispatch races and reject obsolete timer generations when appropriate; deleting an in-memory timer cannot retract work already accepted elsewhere.

## Worked example

Source event E arrives twice. The inbox stores one pending record for E. Worker A claims attempt 1 and calls an external service. The service succeeds, but A loses its acknowledgement and its claim expires. Worker B claims attempt 2. The inbox cannot infer whether the external operation happened. B must query the stable operation identity or retry under the provider's deduplication contract; blindly executing a new operation could duplicate the effect. A's late completion must not overwrite B's newer attempt state.

## Boundaries and validation

Choose retry limits, delayed retries, handling for permanently failing events, retention, and treatment of late or out-of-order arrivals. Preserve enough evidence to distinguish failed from unknown effects. A poison event should not silently disappear or block every unrelated partition forever. A persisted row alone is not proof the requested outcome occurred.

Crash-test before acceptance commit, after commit before dispatch, after a remote effect, and before completion commit. Deliver duplicates concurrently, expire a claim while its old worker is alive, and inspect committed ordering. Measure oldest pending age, retry and unknown-effect counts, processing delay and recovery time. The inbox adds storage and coordination overhead; a synchronous call remains simpler when losing or replaying the trigger is explicitly acceptable.

## Sources

- <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html>

- <https://docs.temporal.io/workflow-execution/timers-delays>
