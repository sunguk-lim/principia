# Agent-Memory Lifecycle Hooks

## Meaning

A memory lifecycle says **when** a runtime reads and changes durable knowledge. Session initialization, query-specific retrieval and post-turn promotion answer different questions. Attaching all three to vaguely named callbacks leaves uncertainty about repeated starts, failed turns and concurrent sessions.

## Mechanism

[[agent-session-state]] distinguishes conversation continuity from one run's execution progress. At session start, load only authorized bounded background context; this is not a fresh query result. Before a model step that needs historical evidence, retrieve against that step's actual question and applicability scope. After useful evidence is produced, propose a durable change through [[agent-memory-reconciliation]] rather than copying every utterance or tool result.

Specify the commit boundary. A proposed fact can be staged during a turn, but whether it becomes durable before the answer, after the answer or in a background worker is a policy decision. Synchronous writes increase response delay; asynchronous writes create a visibility lag. A failed answer does not imply every earlier observation was false, and a completed answer does not make every generated assertion worth retaining.

Use an [[idempotent-operation-key]] for one intended promotion, with a bound payload and owner. A retry of the same run should not create a second fact. A changed payload is a new operation or a conflict to resolve, not a reuse of an old success receipt. Concurrent turns must revalidate any state on which a correction depends.

## One example

An invented session S starts twice because a client reconnects. Both starts may reconstruct the same bounded view without writing duplicate preferences. Turn T then retrieves record P at revision 4 and learns a supported correction. Promotion W binds T, the owner, the proposed correction and observed revision 4.

| Boundary | Evidence available | Durable effect |
| --- | --- | --- |
| Start S | Authorized prior context | None required |
| Recall for T | Current scoped query results | None required |
| Stage W | Candidate correction plus origin | Not yet a current fact |
| Commit W | Validated change and current-state check | One attributable transition |
| Retry W | Same operation and payload | Existing outcome, not a second transition |

If another session changes P to revision 5 first, re-read before committing W. If the worker crashes after the commit but before acknowledging it, consult W's receipt. Replaying an end-of-turn callback is not evidence that a second change is intended.

## Check your understanding

Does running the save hook after a successful response prove a correct memory write? No. Validate evidence, scope, identity and the actual committed result separately.
