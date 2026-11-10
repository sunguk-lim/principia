---
id: scheduled-artifact-refresh
title: Scheduled Artifact Refresh
summary: Scheduled artifact refresh computes and validates a new artifact revision before advancing its stable publication identity while preserving freshness and audience boundaries.
type: concept
tags: [ml/agents]
prereqs: [periodic-agent-workflow, durable-interactive-artifact, single-writer-state-coordination]
sources: [https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/, https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html]
status: explained
created: 2026-11-11
updated: 2026-11-11
---

# Scheduled Artifact Refresh

## Meaning

A stable report can point to evolving content. Scheduled artifact refresh separates the recurring attempt to produce a revision from the reader-visible act of making that revision current. An unchanged link can conceal new data, stale output or a widened audience unless those boundaries are explicit.

## Mechanism

A [[periodic-agent-workflow]] creates a bounded attempt for an intended occurrence. Read the required sources, build a candidate revision, validate its evidence and rendering contract, then advance the current revision of a [[durable-interactive-artifact]]. Keep source cutoff, completed-at time, publication time and last successful revision distinct. A new scheduler tick is not a fresh report.

Under [[single-writer-state-coordination]], the publisher accepts a new revision against the expected current version. A late worker from yesterday must not overwrite today's accepted result because it finished last. Store the prior good revision and expose failed or partial refreshes. A documented partial-coverage policy can be useful, but a failed source must not be relabeled unchanged or silently omitted.

Audience is part of the artifact contract, not a property of the refresh timestamp. An automated editor should not gain sharing rights just because it can update data. Recheck the intended view/edit boundary when replacing embedded resources or publishing a new revision. Generated content remains data requiring validation; refreshing it does not authorize arbitrary executable code.

## One example

Report R currently publishes revision 8 from a Monday source cutoff. Tuesday's attempt builds revision 9 but one required source fails. The policy says all required inputs must validate, so readers keep revision 8 with a visible stale-data notice. A retry completes and publishes revision 9. A delayed Monday worker then tries to publish against revision 8; the coordinator rejects its stale version rather than making the report go backward.

PostgreSQL's documented materialized-view refresh illustrates the distinction between stored results and recomputation, while Kubernetes documents missed and duplicate scheduled jobs. Neither alone supplies this whole artifact-publication contract; the composition is an explicit system design.

## Check your understanding

Does editing the same page every morning guarantee current evidence? No. Test overlapping attempts, source failure, outdated writes, publication failure and permission changes. Measure source-to-publication lag and observed current revision rather than merely successful process exits.

## Prerequisites

- [[periodic-agent-workflow]]
- [[durable-interactive-artifact]]
- [[single-writer-state-coordination]]

## Sources

- <https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/>
- <https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html>
