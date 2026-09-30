---
id: coding-agent-workflow-composition
title: Coding-Agent Workflow Composition
summary: Coding-agent workflow composition combines planning, persistent instructions, deterministic checks, and isolated execution according to the failure mode each addresses.
type: concept
tags: [ml/agents]
prereqs: [multi-agent-orchestration, measurement, agent-plan-artifact, repository-agent-instructions, agent-validation-hooks, worktree-isolation-for-agents]
sources: [https://code.claude.com/docs/en/features-overview, https://code.claude.com/docs/en/common-workflows]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Coding-Agent Workflow Composition

## Summary

A coding-agent workflow combines separate controls only when the task calls for them. An [[agent-plan-artifact]] makes intended steps inspectable; [[repository-agent-instructions]] convey stable local conventions; [[agent-validation-hooks]] run event-triggered checks; [[worktree-isolation-for-agents]] separates concurrent edits. [[multi-agent-orchestration]] adds delegation and handoff rules when work can be split.

## Grounded explanation

These controls solve different problems, so merely enabling all of them is not a method. Start from a failure mode: an agent edits before understanding dependencies, repeatedly violates a repository convention, forgets to run a check, or collides with another worker. Choose the corresponding control, define who can change it, and inspect its output. Instructions guide behavior but are not enforcement; a hook can enforce a deterministic check, while a worktree protects file state rather than answer quality.

Evaluate the composition against a single-agent baseline with equivalent tasks and budgets. [[measurement]] should track accepted changes, defects, recovery time, latency, and total cost. More controls can add context and coordination overhead. No productivity multiplier follows from the saved promotional excerpt; this node is grounded in the linked primary documentation instead.

## Prerequisites

- [[multi-agent-orchestration]]
- [[measurement]]
- [[agent-plan-artifact]]
- [[repository-agent-instructions]]
- [[agent-validation-hooks]]
- [[worktree-isolation-for-agents]]

## Sources

- [Claude Code features overview](https://code.claude.com/docs/en/features-overview): distinguishes instructions, subagents, and hooks by role.
- [Claude Code common workflows](https://code.claude.com/docs/en/common-workflows): documents plans and parallel worktrees.
