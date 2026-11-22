---
id: skill-procedure-consolidation
title: Skill Procedure Consolidation
summary: Skill procedure consolidation merges compatible reusable procedures into a shared contract while retaining explicitly selected environment-specific implementations.
type: concept
tags: [ml/agents]
prereqs: [agent-skill-package, reusable-agent-playbook]
sources: [https://agentskills.io/specification, https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills]
status: explained
created: 2026-11-23
updated: 2026-11-23
---

# Skill Procedure Consolidation

## Meaning

Consolidation turns several overlapping procedures into one discoverable task contract with scoped implementations. Its objective is not merely fewer files or shorter prompts: it reduces ambiguous selection without erasing differences needed for correct execution. An [[agent-skill-package]] supplies the discoverable packaging, while a [[reusable-agent-playbook]] supplies preconditions, live inputs, steps and outcome checks.

## Mechanism

Compare candidate procedures by goal, required inputs, environment, permissions, completion conditions and recovery behavior. Similar wording only identifies candidates for review. Extract a common contract where those obligations genuinely agree. Keep variable commands, tool schemas and environment assumptions in separately selected implementations. A small dispatcher chooses an applicable implementation from trusted environment information; an unknown environment is an explicit unsupported case, not permission to guess.

Load the shared instructions first and only the relevant implementation afterward. Agent Skills' progressive-disclosure mechanism supports this packaging: a main file references focused resources that need not all enter context at once. The standard does not automatically prove compatibility, select a correct variant, or validate consolidation. Those remain authored design and evaluation decisions.

A merge must preserve the behavior callers relied on, including failure boundaries. Do not widen permissions just because one original variant had greater authority. Preserve original versions and traceability until the merged procedure passes representative cases; retirement from discovery need not delete historical evidence.

## One example

Two fictional report-export procedures both accept an authorized report identifier and destination and require a readable file containing the requested report. Service A completes synchronously; service B returns a job identifier that must be polled with a bounded deadline. Consolidate the shared input and completion contract, but keep separate A and B execution resources. Treating B's accepted job as a completed file would lose a necessary distinction.

Test A success and rejected access, B success and expired polling, and an unsupported service C. The caller should see the same success contract but accurate service-specific failures. Five near-duplicate files becoming one misleading universal procedure is a regression, even if discovery becomes cheaper.

## Boundaries and check

Compare wrong-variant activation, full-task success, lost exceptions, context cost and maintenance effort before and after consolidation on tasks not used to author the merge. Use one shared contract only when it explains real common behavior; independent goals deserve independent skills. Metadata compression, exact duplicate removal and behavioral consolidation are different operations.

**Check:** Can two procedures be merged solely because their embeddings are close? No. Their preconditions, observable effects and failure contracts must also be compatible. This consolidation design is independent synthesis grounded in the primary packaging and evaluation mechanisms, not a claim about a named automatic-merging system.

## Prerequisites

- [[agent-skill-package]]
- [[reusable-agent-playbook]]

## Sources

- <https://agentskills.io/specification>
- <https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills>
