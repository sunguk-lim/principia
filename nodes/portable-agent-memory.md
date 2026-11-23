---
id: portable-agent-memory
title: "Portable Agent Memory"
summary: "Portable agent memory separates an authorized user memory namespace and its versioned semantics from harness-specific sessions and interchangeable storage adapters."
type: concept
tags: [ml/agents]
prereqs: [agent-memory-reconciliation, agent-harness-interoperability, adapter-pattern]
sources: [https://docs.langchain.com/oss/python/concepts/memory, https://docs.mem0.ai/core-concepts/memory-operations/add, https://agentclientprotocol.com/protocol/session-setup]
status: explained
created: 2026-11-24
updated: 2026-11-24
---

# Portable Agent Memory

## Meaning

Portable memory lets different authorized agent runtimes read and contribute to the same deliberately retained knowledge without transferring ownership of that knowledge to each runtime. A shared task API does not by itself provide this memory contract. Portability includes meaning, scope and lifecycle—not merely exporting a list of strings.

## Mechanism

[[agent-harness-interoperability]] separates runtime session identity and capabilities from a common task interface. Memory needs another stable identity: the authenticated owner or namespace, independent of the current harness session. Keep a record's origin, timestamps, applicability, schema revision and retention state. A runtime-specific transcript may remain private to its session while selected facts are available across permitted sessions.

Define read, search, propose-write, correction and deletion behavior. [[agent-memory-reconciliation]] explains why a new assertion is not automatically the current truth. An [[adapter-pattern]] can translate a common request into backend-specific operations, but translation does not make different backends equivalent. One may store only additive facts; another may track time intervals or graph relationships. Declare unsupported behavior and information loss rather than pretending an adapter preserves semantics it cannot represent.

“User-owned” must be operationalized. Who authorizes a new runtime, exports retained evidence, corrects an error, revokes access and requests deletion? Derive owner scope from trusted application identity, not a model-supplied name. A useful export carries stable record IDs, provenance, validity and deletion state; a search result may expose less. Recalled text remains reference data and cannot grant tool authority.

## One example

User U permits runtime A and runtime B to use namespace U/preferences. A proposes a dated preference for vegetarian meals. The application validates and stores record P7 at revision 3. A fresh B session searches that namespace and receives P7 with origin and applicability, without importing A's full transcript.

Now U corrects P7 to apply only to weekday meals, and later revokes B. A compliant B adapter must not return the old unrestricted preference or continue to read after revocation. If backend C cannot preserve validity intervals, migration must retain that limitation or reject it. Returning a similar sentence is not enough to pass the contract.

## Validation and alternatives

Run the same fixtures through two adapters: new fact, repeated fact, scoped correction, uncertain conflict, concurrent write, export/import, deletion, revoked runtime and unauthorized namespace. Compare record identity, provenance, permitted results, staleness, failure signals and cost, not byte-identical similarity rankings. Preserve an immutable origin reference only within the chosen retention and erasure policy.

LangGraph documents cross-thread namespaces and store operations; Mem0 documents identifiers and an additive add path. These are primary examples of distinct contracts, not evidence that all memory engines implement a universal protocol or identical reconciliation. A small application-owned store may be simpler than a general broker when only one runtime and one data model are needed.

**Check:** Does replacing a backend adapter prove equivalent memory behavior? No. Verify the declared semantics and document what cannot be preserved.

## Prerequisites

- [[agent-memory-reconciliation]]
- [[agent-harness-interoperability]]
- [[adapter-pattern]]

## Sources

- <https://docs.langchain.com/oss/python/concepts/memory>
- <https://docs.mem0.ai/core-concepts/memory-operations/add>
- <https://agentclientprotocol.com/protocol/session-setup>
