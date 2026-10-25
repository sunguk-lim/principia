# Agent Harness Interoperability

## Meaning

Agent harness interoperability lets a client start, observe, interrupt and continue tasks across runtimes with explicit shared semantics. Matching JSON method names is insufficient. The coordinator can remain in one conversation while workers retain their native harnesses and session identities.

## Mechanism

Map each task to runtime, session and attempt identifiers. Negotiate optional capabilities before using them: creating a session does not establish that loading it is supported. A history-replaying load differs from a supported reconnect without history replay. Neither guarantees that arbitrary live interpreter or tool-process state can transfer between runtimes.

Preserve event ordering and uncertainty, enforce each worker's actual authority, and define how files become accepted artifacts. A producer-local path is not automatically meaningful in another workspace. Record revision, digest, producer and read scope; a changed artifact is a new handoff. Separate worktrees prevent some editing collisions but do not isolate credentials or external side effects.

## One example

Worker A creates revision r7 of an analysis file. Worker B accepts that exact revision for a report. A later r8 must not silently replace B's input. Now the coordinator sends cancel and receives a file-completed update before the prompt's terminal cancelled response. Retain the observed completed artifact and the cancelled turn. Cancellation is not rollback and does not prove that every operation failed. Unknown effects require reconciliation, not invented success or failure.

## Check your understanding

**Question:** Should an adapter discard updates that arrive after it sends cancel? **Answer:** Not automatically. ACP permits pending updates before the terminal prompt response. Reconcile them and preserve the resulting evidence. Conformance tests should cover cancellation races, duplicate events, missing terminal responses, inaccessible artifacts, unsupported resume and permission-request cancellation. Only these tests establish what the shared interface actually promises.
