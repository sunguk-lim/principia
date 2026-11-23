# Socket-Mode Event Delivery

## Meaning

Socket mode replaces an application's public inbound event endpoint with a persistent connection initiated by the application. It can help a local worker receive collaboration events without exposing an inbound request URL. It does not remove credentials, provider connectivity, recovery or authorization requirements.

## Mechanism

A [[socket]] is an endpoint for communication. Slack's Socket Mode establishes an authenticated WebSocket connection using a URL obtained through the provider's connection API. The connection carries event payloads inside envelopes. An envelope identifier lets the application acknowledge receipt; that acknowledgment tells the delivery protocol something narrower than “the requested job succeeded.”

Choose an explicit durable-acceptance boundary. An application can validate the event's expected workspace and routing scope, persist an accepted work record, then acknowledge promptly. If it acknowledges before that record survives a process failure, it risks losing work after the provider stops retrying. If processing is slow, waiting for the whole agent task before acknowledgment can trigger redelivery. The service contract determines the allowed timing; durable admission is distinct from finishing the task.

An [[idempotent-operation-key]] binds one logical work item to its recorded outcome. Envelope identifiers belong to transport delivery; choose and document a stable event/task identity for logical deduplication rather than assuming all retries and reconnects have identical envelope metadata. A task that sends a reply or changes a repository needs its own effect-reconciliation boundary.

## One example

A fictional mention event E asks a coding agent to inspect issue 42. Delivery envelope A arrives, and the receiver persists task E in accepted state before acknowledging A. The worker starts, then the connection refreshes. If E appears again, the dispatcher finds the existing task instead of starting an independent second owner. The task may still fail to read the repository; acknowledging A never established success.

If the host sleeps after acknowledgment, another worker can resume only if the task record and required workspace/evidence survive. Reopening a WebSocket does not reconstruct unrecorded in-memory progress. If a reply was posted before a crash, reconcile its provider receipt before posting again.

## Check your understanding

Does no public inbound URL mean an offline or authorization-free system? No. The application still depends on an authenticated provider connection and explicit processing policy.
