---
id: agent-interaction-trajectories
title: Agent Interaction Trajectories
summary: Agent interaction trajectories correlate model and tool execution with user actions and interventions so observed behavior can become attributable evidence rather than an assumed learning signal.
type: concept
tags: [ml/agents]
prereqs: [trace-span, log-record, dataset-lineage]
sources: [https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-agent-spans.md, https://docs.langchain.com/langsmith/evaluation-concepts]
status: explained
created: 2026-10-25
updated: 2026-11-24
---

# Agent Interaction Trajectories

## Meaning

An interaction trajectory records what an agent and its user actually did over an episode. It combines execution evidence with product events such as edits, cancellations and human takeovers. An agent-only trace can miss the action that resolved the user's problem; a UI click alone cannot explain the model's preceding proposal.

## Mechanism

Use a stable episode identity and correlate bounded model/tool operations through [[trace-span]] records. Capture point-in-time user actions as [[log-record]] events with actor, operation identity, observed outcome and source sequence. Preserve occurrence and ingestion times separately. Link an intervention to the affected proposal or task, not merely the nearest timestamp. Overlapping browser tabs and concurrent tool calls can make time proximity misleading.

Record the versions of application, model, tools and data needed for [[dataset-lineage]]. Keep proposed, started, completed, independently verified and unknown outcomes distinct. A successful HTTP response does not prove task completion. Likewise, a user's manual edit can mean correction, stylistic preference or changed intent; it is not automatically a negative label for the original task.

## Worked example

Episode E contains tool call C proposing a draft, a result saying draft saved, and user action U replacing its destination folder. Linking U to C yields a candidate folder-selection correction. If U belongs to another open task, joining solely by timestamp would produce a false training example. Retain task identity and the original user goal; ask an annotation policy to decide whether the action is correction or new intent. If the final send was not observed, label its outcome unknown, not successful.

Capture only permitted fields. Apply consent, secret redaction, scoped access and retention before making traces reusable; a diagnostic logging permission is not automatically training permission. Missing UI or tool instrumentation should remain a visible coverage gap. Test dropped, duplicated, delayed and reordered events, cancelled sessions and ambiguous interventions. Trajectories are evidence containers: curated labels and held-out evaluation are separate steps, not consequences of collecting more events.

## Check your understanding

Does a user intervention by itself identify a correct target action? No. Its task, intent, outcome and annotation policy must establish what it means.


## Whole-conversation and tool-outcome evaluation

A multi-turn evaluator must preserve the episode's actual continuation policy. Replaying recorded user messages against a changed agent can create an incoherent conversation if those messages assumed different prior answers. Use a fixed scripted interaction when it remains valid, a controlled user simulator with its limitations declared, or separately adjudicated real conversations. A simulator agreeing with the agent is not independent proof of completion.

Score final task state, policy-critical intermediate actions and conversation coherence separately. For an invented three-turn task, the user supplies a destination, corrects the date and confirms the updated request. A response can repeat the corrected date accurately yet invoke a tool with the obsolete date. Trace the actual tool arguments and receipt, not only the final prose. Conversely, a harmless exploratory read need not match one reference trajectory exactly if it preserves the task's invariants.

LangSmith distinguishes individual runs from threads representing related multi-turn runs. Use that distinction to report per-turn defects and episode-level success without multiplying one conversation into independent observations. Retain cancellation, human takeover, missing receipts, retries and unknown outcomes. Compare on the same initial state and task distribution, with privacy/retention controls on transcripts and a held-out evaluation separate from prompt tuning.

## Prerequisites

- [[trace-span]]
- [[log-record]]
- [[dataset-lineage]]

## Sources

- <https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-agent-spans.md>
- <https://docs.langchain.com/langsmith/evaluation-concepts>
