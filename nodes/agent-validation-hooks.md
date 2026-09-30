---
id: agent-validation-hooks
title: Agent Validation Hooks
summary: Agent validation hooks run configured checks at agent lifecycle events and return results or block an action according to the hook contract.
type: concept
tags: [ml/agents]
prereqs: [measurement]
sources: [https://code.claude.com/docs/en/hooks-guide]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Agent Validation Hooks

## Summary

**Agent validation hooks** attach a check to a defined event in a coding agent's workflow. The event trigger and hook result are more reliable than asking the model to remember a check, though the check itself may still be incomplete.

## Grounded explanation

For example, a post-edit hook can run a formatter or linter and return diagnostics; a pre-tool hook can reject an operation that violates an explicit rule. The hook contract must specify its event, input, command or handler, exit behavior, and how diagnostics reach the agent. A check that runs after an edit reports or repairs a problem but does not retroactively prevent the edit.

Choose deterministic, bounded checks for hooks. Slow or noisy hooks add latency and can obscure useful feedback. Track false blocks and escaped defects with [[measurement]]; do not treat a successful hook execution as proof that the whole change is correct.

## Prerequisites

- [[measurement]]

## Sources

- [Claude Code hooks guide](https://code.claude.com/docs/en/hooks-guide): lifecycle events, hook types, and validation examples.
