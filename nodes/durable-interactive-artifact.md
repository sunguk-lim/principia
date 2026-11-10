---
id: durable-interactive-artifact
title: Durable Interactive Artifact
summary: A durable interactive artifact persists a versioned document and its interaction contract independently of the conversation or live process that produced it.
type: concept
tags: [ml/agents]
prereqs: [agent-session-state, reactive-user-interface, dataset-lineage]
sources: [https://nbformat.readthedocs.io/en/latest/format_description.html, https://ipywidgets.readthedocs.io/en/stable/embedding.html]
status: explained
created: 2026-11-11
updated: 2026-11-11
---

# Durable Interactive Artifact

## Meaning

A durable interactive artifact is a reopenable result with its own identity and state: an analysis page, notebook or dashboard rather than a message that merely describes one. Persistence concerns the saved document and required data; interactivity concerns how a viewer's actions affect it. A stable URL alone proves neither.

## Mechanism

Keep artifact identity, revision, schema, content, data references and interaction configuration outside transient [[agent-session-state]]. A [[reactive-user-interface]] may derive the visible chart from saved data and a selected filter, but its current browser state is not automatically stored. Decide whether controls belong to the shared document, a user's saved view or an unsaved session. Record input provenance with [[dataset-lineage]] so reopening the artifact does not silently change which data its conclusions describe.

Jupyter's notebook format is a primary example of a saved document carrying cells, outputs and format versions. Jupyter widgets can embed saved widget state and views. These mechanisms have boundaries: a static export may support client-side interactions from saved state but not an arbitrary callback that needs a live Python process. External libraries, referenced data and permissions can also affect reopening. Preserve or explicitly declare those dependencies rather than calling every exported HTML file self-contained.

## One example

An agent creates report R, revision 3, from data snapshot D7. The saved report includes a table, chart definition and a default region filter. Viewer A selects East. If that selection is session-local, viewer B and a new session still open the default. If it is a shared edit, the server creates revision 4 and can reject A's stale update against revision 3. Both are reasonable policies; silently mixing them causes one person's exploration to change everyone else's report.

Reopening R after the chat ends should recover its accepted revision and evidence. If a control needs an unavailable execution service, show that limitation instead of leaving a convincing but inert control. A report's saved output is not proof its original computation can still execute.

## Check your understanding

Is a task board or conversation plan the same concept? No: those organize work; this artifact is a persistent result and interaction contract. Test cold reopening, unavailable dependencies, revisions, view/edit separation, keyboard access and schema migration. Compare a plain snapshot when interactivity adds no useful decision.

## Prerequisites

- [[agent-session-state]]
- [[reactive-user-interface]]
- [[dataset-lineage]]

## Sources

- <https://nbformat.readthedocs.io/en/latest/format_description.html>
- <https://ipywidgets.readthedocs.io/en/stable/embedding.html>
