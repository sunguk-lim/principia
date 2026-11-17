---
id: periodic-agent-workflow
title: "Periodic Agent Workflow"
summary: "A periodic agent workflow binds each scheduled occurrence to a durable bounded run with explicit timezone, overlap, missed-run and duplicate-effect policies."
type: concept
tags: [ml/agents]
prereqs: [durable-agent-execution, idempotent-operation-key]
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/"]
status: explained
created: 2026-11-06
updated: 2026-11-18
---

# Periodic Agent Workflow

## Meaning

A periodic agent workflow asks an execution system to begin bounded work on recurring clock occurrences. The schedule defines when work is due; it does not prove that the work started, finished or produced the intended external result. An event-triggered workflow instead begins because an observed event meets a rule.

## Mechanism

Specify cadence, timezone, allowed lateness, maximum runtime and overlap policy. Distinguish the intended occurrence time from the actual start time. A logical occurrence identifier joins the workflow identity with that intended time, while each retry receives its own attempt identifier. [[durable-agent-execution]] stores completed steps, artifacts and uncertain effects so a later attempt resumes evidence rather than a promise.

Clock-triggered delivery is not automatically exactly once. A scheduler may miss an occurrence or create duplicate workers. Use an [[idempotent-operation-key]] for the logical effect and reconcile ambiguous remote outcomes before retrying. A local running flag alone cannot atomically commit both a checkpoint and an external publication. Kubernetes CronJob documentation explicitly describes missed and duplicate creation possibilities and requires suitable idempotent jobs; its per-CronJob overlap setting is not a global lock across independent schedules.

## One example

An invented report is due at 07:30 in Asia/Tokyo. The occurrence is recorded for that local date and time even if a busy worker starts at 07:34. Two workers receive that occurrence. Both may prepare calculations, but they must not independently publish the same report twice. A stable publication identity lets the later worker query whether the logical report already exists. If a worker crashes after publication but before its receipt is stored, the result is unknown until that query—not automatically failed.

Choose whether a run still active at the next occurrence should overlap, skip the new occurrence or be replaced. Each has consequences for stale results, lost work and duplicated effects. Check daylight-saving transitions for zones that use them, clock skew, missed deadlines and recovery after outages. Do not impose catch-up work without a bounded policy.

## Check your understanding

Does a scheduler's success flag prove a report was published? No. Verify the run's artifact and external receipt separately from trigger acceptance and process exit.

## Notification quality is a separate acceptance criterion

Waking on schedule does not imply that a user should receive a message on every run. Define outcomes such as a useful update, explicit no-notification decision, or a precisely bound approval request. Persist which outcome was delivered so retries do not repeat an old alert. Where local state and a notification intent must commit together, use a transactional outbox; the delivery endpoint still needs duplicate-safe or reconcilable effects.

Evaluate the notification policy on events with independently labeled urgency and usefulness. Measure missed actionable events, delay, duplicate notices, irrelevant notices and user interruption burden separately. A quiet policy can look precise by missing important events; a noisy policy can maximize coverage while becoming unusable. Compare at a fixed event set and declared time budget, including overnight delivery rules and genuinely urgent exceptions. These are application-specific objectives, not a universal optimal message count. An invented ten-event test with two urgent events requires checking both whether those two were delivered on time and whether eight unrelated events were suppressed; total message count alone cannot distinguish success from a reversed policy.

## Prerequisites

- [[durable-agent-execution]]
- [[idempotent-operation-key]]

## Sources

- <https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/>
