---
id: worktree-isolation-for-agents
title: Worktree Isolation for Coding Agents
summary: Worktree isolation gives concurrent coding agents separate Git checkouts and branches so their uncommitted edits do not collide.
type: concept
tags: [ml/agents]
prereqs: [multi-agent-orchestration]
sources: [https://git-scm.com/docs/git-worktree, https://code.claude.com/docs/en/common-workflows]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Worktree Isolation for Coding Agents

## Summary

A **Git worktree** is another checkout associated with the same repository. Giving each concurrent coding agent a separate worktree and branch prevents them from editing the same working directory while [[multi-agent-orchestration]] coordinates their tasks.

## Grounded explanation

The isolation boundary is the checkout, index, and branch—not the repository history or the final integration. Agents can work on independent changes without overwriting each other's uncommitted files, but overlapping changes may still conflict when merged. Assign bounded ownership, inspect each diff, run checks in each worktree, and integrate branches deliberately. Worktrees do not isolate credentials, processes, or external services unless separate controls do so.

Use worktrees when tasks are genuinely parallel and file-state collisions matter. A sequential or tightly coupled task may be simpler in one checkout because coordination and merge costs can exceed the benefit.

## Prerequisites

- [[multi-agent-orchestration]]

## Sources

- [Git worktree documentation](https://git-scm.com/docs/git-worktree): checkout and branch mechanics.
- [Claude Code parallel sessions with worktrees](https://code.claude.com/docs/en/common-workflows#run-parallel-sessions-with-worktrees).
