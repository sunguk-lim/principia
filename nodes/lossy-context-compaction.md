---
id: lossy-context-compaction
title: Lossy Context Compaction
summary: Lossy context compaction replaces detailed history with bounded state while explicitly managing omitted evidence and the ability to recover it.
type: concept
tags: [ml/agents]
prereqs: [context-window, agent-session-state]
sources: [https://www.anthropic.com/research/effective-context-engineering-for-ai-agents, https://docs.stripe.com/api/idempotent_requests]
status: explained
created: 2026-11-02
updated: 2026-11-16
---

# Lossy Context Compaction

## Meaning

Compaction replaces some detailed context with a shorter representation. It is lossy when that representation cannot reconstruct every original detail. The design problem is not merely producing a fluent summary: it is preserving the evidence needed for later decisions under a bounded [[context-window]].

## Mechanism

Partition material into current working state, exact evidence worth retaining, and recoverable history stored outside the prompt. A summary can preserve the current hypothesis while dropping a filename, error location or disconfirming result that a later step needs. If the original remains retrievable by a stable reference, the agent can recover it; if it was deleted, a confident narrative cannot recreate it reliably.

[[agent-session-state]] keeps ordered records and tool-call reconciliation separate from the summary. Preserve completed actions, unresolved actions, exact identifiers, constraints, evidence references and uncertainty. A model-generated conclusion should remain distinguishable from an observed result. External text remains untrusted after summarization: rewriting an instruction does not give it authority.

## Worked example

A tool result says test T failed in file alpha.py at line 28, while beta.py passed. A 20-word summary says only that a test failed in the parser. The next agent searches both files and reruns both tests because it lacks the location and prior passing evidence. A structured replacement retains `failed: T, alpha.py:28`, `passed: beta.py`, and a reference to the complete result. It uses more tokens than the vague summary but supports the next repair without repeating the same investigation.

This is an illustrative failure path, not a claim that all summaries cause extra calls. Some old details are genuinely irrelevant.

## Validation

Compare raw history, bounded raw excerpts, structured extraction and summaries on the same tasks. Inspect whether identifiers, negative evidence and unresolved state survive; compare valid completion, repeated actions, recovery reads and total cost. Test a later question that requires a detail which appeared unimportant when summarized. Retaining exact originals has storage, access and privacy costs; selective recovery must still respect permissions and retention limits. Tune compression for downstream evidence utility, not shortest text or stylistic quality alone.

## Recoverable evidence is not replay permission

Masking a prompt observation, retaining its original in an artifact store and caching a fresh tool read are distinct operations. A stable artifact reference can recover what was observed earlier; it cannot establish that a mutable external resource still has the same value. Bind a retained observation to the tool, relevant inputs, data version, time and access scope. Reuse it only when the task accepts that observation's freshness. A newly granted or revoked permission must not be bypassed by an old local reference.

Suppose a report was captured at 09:00 and offloaded. At 09:10 the task asks which error appeared in that report: retrieve the artifact. At 10:00 it asks whether the service is healthy now: an old report alone is insufficient. If the masked result instead concerned a payment request that timed out, neither absence from the prompt nor absence of a local receipt proves the payment did not occur. Reconcile the remote operation under its retry contract before repeating an effect. Local summaries are not duplicate-effect protection.

Measure retained-token reduction together with recovery reads, repeated tool calls, successful task completion and total trajectory cost. A policy can shrink each prompt while increasing the number of turns. The choice should follow the full-task evidence, including failures, not an assumption that compression must help or that summaries must fail.

## Prerequisites

- [[context-window]]
- [[agent-session-state]]

## Sources

- <https://docs.stripe.com/api/idempotent_requests>: a concrete remote retry contract, distinct from local compaction or cached evidence.

- <https://www.anthropic.com/research/effective-context-engineering-for-ai-agents>
