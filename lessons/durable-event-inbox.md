# Durable Event Inbox

## Meaning

A durable event inbox separates accepting a trigger from completing its work. Instead of starting a worker directly from an incoming webhook or timer, the application first commits a record that can survive process loss. Acknowledging acceptance then means “the trigger is durably recorded,” not “the task succeeded.”

## Mechanism

Give each source event a stable, source-scoped identity. Persist the payload, state and target partition. A worker claims an attempt with an owner and expiry, processes it, and records a verifiable outcome. A crashed worker leaves a recoverable record rather than an event that existed only in memory. Retry limits and a separate path for persistent failures keep one poison event from circulating indefinitely.

Deduplicating inputs does not make downstream effects exactly once. A claim can expire while the original worker remains alive, and a remote action can succeed before its local receipt is committed. Version-checked commits reject stale workers locally. Remote operations need their own stable identity and duplicate-safe or queryable outcome contract. A conversation may also need ordered commits even when unrelated conversations run concurrently.

## One example

Event E is accepted once despite duplicate delivery. Worker A sends an external update, then crashes before saving its result. Worker B later claims the expired event. B cannot conclude that the missing receipt means failure. It must reconcile the original operation or reuse its supported idempotency identity, not invent a new update.

## Understanding check

Does a visibility timeout guarantee no duplicate processing? No. Queue delivery and claim expiry have explicit failure contracts. Test duplicate arrivals, overlapping workers, late completions and crashes around both local commits and external effects. Measure pending age and unknown outcomes separately from successful completions.
