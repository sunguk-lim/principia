---
id: snapshot-change-monitoring
title: "Snapshot-Based Change Monitoring"
summary: "Snapshot-based change monitoring compares identified, timestamped source captures under a stable extraction policy and reports evidence-backed differences with bounded observation time."
type: concept
tags: [software/monitoring]
prereqs: [periodic-agent-workflow, dataset-lineage]
sources: [https://github.com/dgtlmoon/changedetection.io, https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/]
status: explained
created: 2026-11-15
updated: 2026-11-15
---

# Snapshot-Based Change Monitoring

## Meaning

A change monitor compares observations, not an omniscient stream of the source's true state. Save a baseline, obtain a later comparable capture, identify relevant differences and publish a bounded claim about what was observed. A manual second capture demonstrates comparison but not continuous monitoring.

## Mechanism

Record source identity, capture time, retrieval outcome, extraction policy version and the accepted evidence revision. This is [[dataset-lineage]] applied to observations and transforms. A failed or partial retrieval must not silently replace a successful baseline with an empty page. Distinguish “not observed” from “observed and absent.” Decide whether a baseline advances after a valid capture or only after review, and retain the compared revisions.

Normalization removes irrelevant presentation variation before comparison: for example whitespace or a documented navigation region. Field extraction can compare equivalent quantities, such as monthly price in a stated currency. A textual difference is not automatically a semantic business change; a model summary can help interpret it but must remain tied to the actual before-and-after evidence. Overbroad filters can hide an important deletion, and an extraction change can manufacture a difference.

[[periodic-agent-workflow]] supplies the observation schedule and recovery rules. With valid captures at times t0 and t1, a difference establishes only that the observed states differ at those times. If one persistent transition occurred between captures, its occurrence lies after t0 and no later than t1. A source may change and revert between polls without either capture showing it. Retrieval and notification delay extend time-to-alert beyond the nominal polling interval.

## One example

At 09:00 a page shows a basic plan at 12 units per month and a timestamp in its footer. At 09:15 it shows 15 units; at 09:30 retrieval fails. A filter ignores the footer but preserves the plan label, price, currency and billing interval. The valid comparison reports 12 to 15 between 09:00 and 09:15, not “the price changed at 09:15.” The failed 09:30 capture records an outage and leaves the accepted 09:15 baseline intact.

If an alert attempt fails after submission, reconcile its delivery identifier before resending. Keep comparison identity separate from delivery attempts so a retry does not create a second claimed source change.

## Check your understanding

Can unchanged captures prove the page never changed between them? No. Test transient changes, reordered fields, missing sections, unit changes, extraction upgrades and downtime. Evaluate false alerts, missed relevant changes and observed delivery delay separately. The cited open-source monitor documents filters, scheduled rechecks and notifications; no installation or product-specific reliability guarantee is implied.

## Prerequisites

- [[periodic-agent-workflow]]
- [[dataset-lineage]]

## Sources

- <https://github.com/dgtlmoon/changedetection.io>
- <https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/>
