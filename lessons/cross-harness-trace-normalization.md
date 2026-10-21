# Cross-Harness Trace Normalization

## Meaning

A shared trace format makes historical activity from different agent runtimes searchable and comparable. Its invariant is evidence fidelity: a converted event must not claim a stronger outcome, ordering or authority than the source supports. This is a data architecture, distinct from a common live task API or a portable executable continuation.

## Mechanism

An adapter maps each source event into a versioned envelope: source runtime and schema version, source event ID, actor/workspace/run identities, event kind, operation/call ID, parent or causal links, occurrence and ingestion times, outcome, and a bounded reference to the original evidence. Preserve source and normalized values when mappings are lossy. [[log-record]] supplies structured point events; [[trace-span]] supplies bounded operations and parent relationships. OpenTelemetry's GenAI conventions offer shared vocabulary, but instrumentation coverage and convention versions still vary.

The same word can hide different contracts. One runtime's `tool_done` might mean a subprocess exited; another's might mean an edit was independently verified. Map these to different outcome states or annotate the missing evidence. A command request is not a command result. Retain repeated attempts under distinct event IDs while linking them to one logical operation. Deduplicate retransmitted events by stable source identity, not by identical text, which can represent legitimate repeated work.

## Worked example

Harness A records call `A/7`, then an exit code 0 for its shell command. Harness B imports only a message saying “build succeeded.” The normalized records can share `operation.kind=build`, but A has observed process completion and B has only a textual claim. Neither alone proves deployment. If A's result is exported twice, its source event ID identifies a duplicate; if the build genuinely runs twice, the second invocation keeps a different ID.

A receiver may ingest A's result before its start event. Do not reorder solely by wall-clock timestamps from different machines; retain source sequence and causal IDs, permit incomplete records, and reconcile late arrivals. [[agent-harness-interoperability]] additionally tests live cancellation and resume semantics, which normalization cannot manufacture from absent events.

Validate adapter fixtures with dropped/duplicate/out-of-order records, reused call IDs across runs, clock skew, unknown event kinds and schema upgrades. Measure coverage, false outcome promotion and source-to-normalized round-trip fidelity. Apply access and retention policy before making the shared history searchable; normalization is not permission to capture everything.

## Check your understanding

**Question:** Can a normalized success label restore a live tool handle? **Answer:** No. It is evidence under a documented mapping, not executable runtime state.
