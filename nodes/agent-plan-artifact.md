---
id: agent-plan-artifact
title: Agent Plan Artifact
summary: An agent plan artifact records proposed steps, dependencies, and checks for review before a coding agent changes files.
type: concept
tags: [ml/agents]
prereqs: [agent-session-state]
sources: [https://code.claude.com/docs/en/common-workflows]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Agent Plan Artifact

## Summary

An **agent plan artifact** is a reviewable representation of intended work: objective, files or components likely to change, sequence, assumptions, and verification. It externalizes part of [[agent-session-state]] before implementation.

## Grounded explanation

The plan is useful when a change has dependencies or a costly wrong turn. In Claude Code plan mode, the agent can inspect and propose changes without editing until approval. The plan makes scope disagreements visible early; it is not evidence that the proposed implementation is correct. A short fix may not justify the planning overhead.

Keep the plan current as evidence changes, and distinguish proposed checks from checks actually run. After execution, compare the resulting diff and test results with the plan instead of treating approval of the plan as approval of the result.

## Prerequisites

- [[agent-session-state]]

## Sources

- [Claude Code common workflows: plan before editing](https://code.claude.com/docs/en/common-workflows#plan-before-editing).
