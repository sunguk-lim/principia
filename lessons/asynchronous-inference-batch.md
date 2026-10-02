# Asynchronous Inference Batch

## Meaning

A **batch inference API** accepts many requests for later processing. Submission acknowledges durable receipt, not completion of every request. The user trades per-request responsiveness for throughput or pricing, subject to the provider's actual limits.

## Mechanism

Each item needs a stable client ID so unordered results can be matched back to inputs. The service validates and enqueues the batch in a [[queue]], then exposes lifecycle states such as validating, running, completed, failed, or expired. A successful submission is not a successful batch. Poll status or consume a completion notification, inspect every item result, and retry only failed items under idempotent rules. A [[transaction]] analogy is useful for reconciliation: distinguish submitted, accepted, executed, and committed downstream effects; batch APIs rarely give atomic all-or-nothing behavior across items.

Group requests only when they share the endpoint shape and model constraints required by the provider. Preserve input versions and output IDs so a resumed worker does not duplicate downstream writes. Budget for the completion window and the possibility that the provider rejects unsupported modalities after initial submission. Never submit latency-sensitive work to a queue merely because its nominal token price is lower.

## Worked example

A team submits 5,000 nightly labeling requests. The service returns an accepted batch ID immediately, while 100 items later fail validation. Stable per-item IDs let the team join results to inputs and retry only those failures. Reporting the initial acceptance as 5,000 completed labels would corrupt the dataset.

**Understanding check:** What must be checked after an asynchronous batch submission succeeds?
