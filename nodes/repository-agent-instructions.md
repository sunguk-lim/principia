---
id: repository-agent-instructions
title: Repository Agent Instructions
summary: Repository agent instructions provide persistent, versioned project conventions to a coding agent when it works in a repository.
type: concept
tags: [ml/agents]
prereqs: [agent-memory]
sources: [https://code.claude.com/docs/en/memory]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Repository Agent Instructions

## Summary

**Repository agent instructions** store stable project facts and conventions where coding agents can load them across sessions. They act as a scoped form of [[agent-memory]], not as a transcript or a substitute for tests.

## Grounded explanation

A project instruction file can name build commands, style rules, architectural constraints, and repository workflow. Claude Code supports project `CLAUDE.md` files and, under documented conditions, `AGENTS.md`. A shared file should contain durable project guidance rather than task-specific state or secrets. Loading rules and scope matter: an instruction in a subdirectory may be read only when work enters that directory.

Instructions influence model behavior but are not a hard enforcement mechanism. For a rule that must always hold, use repository checks or permissions and verify the result. Keep guidance concise and revise it when the repository changes; stale instructions can misdirect an otherwise capable agent.

## Prerequisites

- [[agent-memory]]

## Sources

- [Claude Code project memory](https://code.claude.com/docs/en/memory): project instructions, loading scope, and enforcement limits.
