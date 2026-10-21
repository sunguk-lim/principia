---
id: agent-skill-package
title: Agent Skill Package
summary: An agent skill package bundles task-scoped instructions and optional resources for discoverable, reusable agent behavior without granting authority beyond the host runtime.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, repository-agent-instructions]
sources: [https://agentskills.io/specification]
status: explained
created: 2026-10-17
updated: 2026-10-22
---

# Agent Skill Package

## Summary

An **agent skill package** gives an [[agent-execution-harness]] a discoverable recipe for a bounded class of tasks. It may include instructions, scripts, references, and assets. It differs from a model's weights, a one-off user prompt, and a lifecycle hook: the skill tells the agent *how to approach a task*; the host still decides when it is available and what tools or permissions may be used.

## Grounded explanation

The Agent Skills specification defines a directory with `SKILL.md`, metadata such as name and description, Markdown instructions, and optional resources. Metadata supports discovery without loading every full procedure into the live context. When a task matches, the agent loads the relevant instructions and follows them subject to higher-priority policy. Scripts can make a procedure reproducible, while reference files keep detailed knowledge out of the initial prompt.

A skill is an execution aid, not an authority boundary. A repository's [[repository-agent-instructions]] may describe local conventions, but neither those files nor a skill can authorize a network request, secret access, or public write that the host forbids. Version the package with its dependencies and verify actual behavior: an instruction that mentions a tool not present in the current runtime is incomplete. Beware of stale paths, implicit platform assumptions, untrusted bundled text, and overbroad trigger descriptions that load the wrong recipe.

## Validation

Test discovery on tasks that should and should not activate the skill. Run a representative task end-to-end in the supported environment, check resource paths and tool availability, and compare output quality with the base workflow. Review bundled scripts and updates as code, not as harmless prose.

## Lifecycle utility is not invocation frequency

A growing skill library needs a utility decision as well as a package format. Track owner, version, source evidence, supported environment, activation cases, measured outcomes and replacement history. Candidate states can distinguish proposed, validated, active, superseded and retired. An obsolete command should be replaced or scoped rather than left beside a contradictory active instruction.

Suppose a routine formatting skill activates on 100 tasks and saves one minute each, while a recovery skill activates twice and prevents two hours of manual repair each time. Invocation count alone ranks the formatter higher; observed time benefit is 100 minutes versus 240 minutes. These illustrative numbers also omit mistakes and maintenance costs. Rare but important recovery procedures should not be deleted solely for low usage, while an automatically injected skill can have high activation without benefit. Compare appropriate activation, held-out task success, harmful regressions, false triggers, cost and maintenance burden; review merging or retirement with versioned rollback.

## Prerequisites

- [[agent-execution-harness]]
- [[repository-agent-instructions]]

## Sources

- [Agent Skills specification](https://agentskills.io/specification): package layout, metadata, and optional resources.
