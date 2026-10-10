---
id: agent-edit-interface
title: Agent Edit Interface
summary: An agent edit interface turns a proposed file change into a validated, uniquely targeted, reviewable filesystem mutation with explicit failure results.
type: concept
tags: [ml/agents]
prereqs: [tool-call-execution-contract, agent-execution-harness, measurement]
sources: [https://git-scm.com/docs/git-apply, https://developers.openai.com/api/docs/guides/function-calling]
status: explained
created: 2026-10-11
updated: 2026-10-11
---

# Agent Edit Interface

## Summary

A coding agent needs more than permission to run a shell: it needs a predictable contract for changing files. An **agent edit interface** accepts a structured change request, validates its target and expected old content, applies the change or rejects it without a partial write, and returns a result the agent can inspect. This is a specialization of the [[tool-call-execution-contract]] enforced by an [[agent-execution-harness]].

## Mechanism

A content-anchored replacement can take `path`, `old_text`, and `new_text`. The executor counts exact matches in the current file. If the count is one, it replaces that occurrence and reports the resulting diff; if zero or more than one, it makes no change and reports the count. The caller can then reread the file and choose a larger context or another method. The unique-match rule prevents a plausible-looking edit from silently changing the wrong occurrence. The tool must also bound file size, path scope, encoding behavior, and concurrent modification. A version or content-hash precondition prevents a read–edit race from overwriting a newer file.

A patch-based interface instead supplies context lines and hunks. It is useful for multi-location edits, review, and interoperating with Git. Git's `apply --check` and atomic application behavior illustrate preflight validation; a patch does not inherently require the model to count exact current line numbers, since context helps locate hunks. Neither interface is universally reliable: content replacement is ambiguous for repeated text; contextual patches can fail after surrounding lines change. A new-file operation should be explicit and reject accidental overwrite. The harness should keep exploratory commands separate from authorized writes, then require syntax checks and tests after edits where appropriate.

## Example and validation

Suppose `retries = 3` occurs in both development and production settings. A request replacing that string globally is ambiguous. The tool returns “2 matches, no write.” The agent reads the containing section and supplies a unique surrounding block. If another process modifies the file meanwhile, the version precondition rejects the stale edit. A successful tool response proves only that the requested bytes changed, not that the program is correct.

Compare structured replacement, contextual patching, and shell editing on the same model, repository tasks, and time budget. With [[measurement]], record failed or ambiguous applications, unintended file changes, valid final patches, test outcomes, repair attempts, latency, and cost. Training-format familiarity may affect results, but that is a separate held-out harness-transfer question, not a property proved by any one edit failure.

## Prerequisites

- [[tool-call-execution-contract]]
- [[agent-execution-harness]]
- [[measurement]]

## Sources

- [Git `apply`](https://git-scm.com/docs/git-apply): patch validation, context, and application semantics.
- [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling): application-owned execution of structured tool calls.
