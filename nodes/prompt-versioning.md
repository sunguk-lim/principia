---
id: prompt-versioning
title: "Prompt Versioning"
summary: "Prompt versioning identifies immutable prompt revisions and promotes tested compatible model-input configurations through named environments with attributable rollback."
type: concept
tags: [ml/llm/operations]
prereqs: [dataset-lineage, progressive-model-rollout]
sources: [https://docs.langchain.com/langsmith/manage-prompts]
status: explained
created: 2026-11-24
updated: 2026-11-24
---

# Prompt Versioning

## Meaning

A prompt is executable application behavior even when it is stored as text. Versioning preserves the exact template and message roles used for a result, while release control determines which revision a deployment selects. A moving production label is a routing pointer, not an immutable record of what ran.

## Mechanism

Use [[dataset-lineage]] to bind an output to its prompt revision, rendered inputs, model revision, tool schemas and retrieval configuration. Keep sensitive rendered values only under their own access and retention policy; reproducing a template need not require putting private transcripts in a public repository. Changing a variable name or a tool argument can break compatibility without changing the model.

Separate immutable content identity from environment labels. A label such as staging or production can point to one revision and later move. Resolve and log the actual revision for each run; logging only production loses the ability to explain an earlier outcome. Promotion should bind tested bytes and a compatible configuration, not merely the latest draft.

Apply [[progressive-model-rollout]] reasoning to the assembled configuration: compare representative held-out tasks, check critical failures, limit initial exposure where appropriate and retain a rollback target. A prompt-only change can alter tool use and disclosure behavior, so tests must cover those effects as well as answer style.

## One example

An invented refund template P4 expects variable order_id and tool lookup_order. P5 changes the variable to purchase_id and assumes a revised tool schema. Both versions are valid text. Moving production from P4 to P5 while a client still supplies order_id can produce a missing-value error or a misleading request.

A release record pairs P5 with client/schema revision C8 and its test results. An old run records P4/C7 even after the production label moves. If P5 fails, selecting P4 is safe only if C7 or a compatible client/tool path remains available; changing the label alone cannot undo an incompatible schema migration.

## Validation and check

Test missing and extra variables, role ordering, rendering escapes, tool compatibility, adversarial retrieved text and output parsing. Compare complete task outcomes under fixed data/model conditions, retaining regression slices rather than optimizing only an aggregate score. Re-run acceptance when a dependency changes even if the prompt text does not.

LangSmith documents immutable commits, movable commit tags, environment promotion and rollback history as one concrete implementation. These features are not a guarantee that an application pins models, validates tools or enforces release permissions. Git and an application-owned release manifest can supply a simpler contract when a managed prompt service is unnecessary.

**Check:** Does a log entry saying prompt=production reproduce an old response? No. It needs the resolved prompt content and the relevant configuration and evidence versions.

## Prerequisites

- [[dataset-lineage]]
- [[progressive-model-rollout]]

## Sources

- <https://docs.langchain.com/langsmith/manage-prompts>
