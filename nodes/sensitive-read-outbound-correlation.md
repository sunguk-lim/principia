---
id: sensitive-read-outbound-correlation
title: Sensitive-Read Outbound Correlation
summary: Sensitive-read outbound correlation joins evidence of a sensitive resource read and a later network action within a scoped execution window to produce a reviewable security signal, not proof of exfiltration.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, log-record, trace-span, measurement]
sources: [https://www.elastic.co/docs/reference/query-languages/eql/eql-syntax, https://opentelemetry.io/docs/security/handling-sensitive-data/]
status: explained
created: 2026-10-22
updated: 2026-10-22
---

# Sensitive-Read Outbound Correlation

## Meaning

Two individually ordinary events can form a suspicious sequence: an agent reads a sensitive resource and then sends data to an external destination. A sequence detector retains enough identity and ordering to flag that combination for investigation. Correlation is an evidence filter, not proof that the second event contains the first event's bytes.

## Mechanism

An [[agent-execution-harness]] records resource access and outbound proposals or effects as distinct [[log-record]] events. Join on authenticated actor, workspace and run identities, with process or [[trace-span]] links when available. Require a bounded time interval and distinguish request, allowed dispatch, rejection and confirmed response. A model saying “I sent it” is not evidence of a network effect.

Elastic EQL provides a primary example of sequence matching with join keys and `maxspan`. A security rule can use that mechanism, but the policy defining sensitive resources and permitted destinations belongs to the application. Joining only on username or a recycled process number can mix unrelated sessions. Time order across machines can also be misleading; preserve causal and source sequence evidence where available.

## Worked example

Run R reads a protected configuration at time 10 s. At 14 s it requests an HTTP POST to an unapproved destination. A rule with the same run identity and a 30 s window raises a candidate alert because 14−10=4 s. If a broker rejects the request, classify an attempted prohibited effect rather than a confirmed leak. If dispatch succeeds, inspect authorized destination policy and bounded payload evidence through a protected investigation path.

An approved telemetry POST in the same interval can be a false positive. Conversely, a delayed upload at 50 s falls outside this particular window; encoding, another process or missing logs can evade the rule. Never store the actual credential merely to make the detector easier to write. Resource classification and synthetic markers can support tests without creating a second leak in the trace store.

Use [[measurement]] on seeded benign and malicious scenarios: count precision, recall, coverage gaps and time to detection. Test partial or encoded content, dropped events, duplicate delivery, process reuse, broker denial and legitimate approved egress. Keep prevention in independent permission and network controls: a detector that runs afterward cannot guarantee blocking the effect.

## Check your understanding

**Question:** Does a sensitive read followed by a successful POST prove exfiltration? **Answer:** No. It warrants investigation; payload provenance, destination policy and actual effect evidence determine the conclusion.

## Prerequisites

- [[agent-execution-harness]]
- [[log-record]]
- [[trace-span]]
- [[measurement]]

## Sources

- <https://www.elastic.co/docs/reference/query-languages/eql/eql-syntax>
- <https://opentelemetry.io/docs/security/handling-sensitive-data/>
