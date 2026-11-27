---
id: repository-agent-instructions
title: Repository Agent Instructions
summary: Repository agent instructions provide scoped, versioned project knowledge whose discovery, maintenance and task value must be checked independently of enforcement.
type: concept
tags: [ml/agents]
prereqs: [agent-memory]
sources: [https://code.claude.com/docs/en/memory, https://developers.openai.com/codex/guides/agents-md, https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents]
status: explained
created: 2026-09-30
updated: 2026-11-28
---

# Repository Agent Instructions

## Summary

**Repository agent instructions** store stable project facts and conventions where coding agents can load them across sessions. They act as a scoped form of [[agent-memory]], not as a transcript or a substitute for tests.

## Grounded explanation

A project instruction file can name build commands, style rules, architectural constraints, and repository workflow. Claude Code supports project `CLAUDE.md` files and, under documented conditions, `AGENTS.md`. A shared file should contain durable project guidance rather than task-specific state or secrets. Loading rules and scope matter: an instruction in a subdirectory may be read only when work enters that directory.

A multi-turn language migration illustrates the scope boundary: a one-task request to port a component to Rust does not necessarily constrain later tasks. Put a repository-wide language rule in a loaded project instruction file, keep examples and build commands consistent with it, and use build or policy checks to catch drift. Preserve explicit exceptions for legitimate mixed-language migration work.

Instructions influence model behavior but are not a hard enforcement mechanism. For a rule that must always hold, use repository checks or permissions and verify the result. Keep guidance concise and revise it when the repository changes; stale instructions can misdirect an otherwise capable agent.


## Scope, maintenance and measured instruction value

Persistent instructions consume part of the same finite input budget needed for the task and its evidence. Reducing file size is therefore a resource intervention, not proof of better task success. Retain high-value repository facts—actual build commands, incompatible paths, data contracts and non-obvious exceptions—rather than replacing them with generic style advice. A generated rewrite can be useful, but review its diff against these facts instead of trusting fluency as preservation.

Use the agent's documented discovery and precedence rules. A nested file is not universally loaded on every later file access: Codex's documented instruction chain follows the repository-root-to-working-directory path at run initialization, whereas other agents can use different loading rules. Moving a required rule into an undiscovered folder loses it. Treat byte caps, overrides and working directory as observed configuration, not assumptions based on a familiar filename.

An invented repository has a root build rule and a nested payments exception. Starting a session in payments should expose the intended exception under that agent's actual loading contract. Starting at root may produce another instruction chain. Verify the loaded sources and task behavior in both cases. Keep global invariants short and put discoverable detail behind stable references when the workflow can retrieve it.

Incident-driven additions need maintenance: record scope and rationale, remove stale duplicates, reconcile contradictory commands and preserve justified exceptions in version history. Replay the original failure after pruning, then run normal tasks so a fix does not cause constant false restrictions. File length and rule count are diagnostic signals, not compliance laws.

Compare no-file, maintained-file and proposed generated-file variants on held-out repository tasks with model, tools, permissions and budgets fixed. Track valid task completion, regressions, relevant-fact retention, unnecessary work, tokens and latency over repeated trials. This is an evaluation design, not a claim that one authorship style always wins or that an unnamed study establishes a universal effect. Enforce hard requirements outside model prose.

## Prerequisites

- [[agent-memory]]

## Sources

- [Claude Code project memory](https://code.claude.com/docs/en/memory): project instructions, loading scope, and enforcement limits.

- <https://developers.openai.com/codex/guides/agents-md>
- <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
