---
id: authorization-audit-log
title: "Authorization Audit Log"
summary: "An authorization audit log records attributable access decisions and their context without confusing a recorded permission decision with enforcement or successful data delivery."
type: concept
tags: [security/authorization]
prereqs: [centralized-data-authorization, log-record]
sources: [https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html]
status: explained
created: 2026-11-21
updated: 2026-11-21
---

# Authorization Audit Log

## Meaning

An authorization audit log preserves evidence about access decisions: who requested what, which policy was applied and what was permitted or denied. It supports investigation and policy review. It is not an enforcement mechanism, and a record saying allowed does not prove that the underlying query completed or that data reached a user.

## Mechanism

At the trusted boundary of [[centralized-data-authorization]], emit a structured [[log-record]]. Include event time and recording time when they differ; authenticated actor and workload; resource and operation identity; policy revision; decision and reason category; and a correlation identifier connecting the decision to execution. Record execution success or failure separately so an allow decision followed by a database outage does not masquerade as completed disclosure.

Choose coverage from the security objective. Denials and sensitive-data access can matter even when a request returns no rows. Query identifiers and bounded metadata are usually safer than complete SQL literals or returned records, which may contain secrets and personal data. Protect the log's own access rights, sanitize untrusted fields, define retention and monitor for gaps or tampering.

## One example

At 09:00, a verified manager requests export E of department D. The boundary records request R, principal M, policy revision 12 and decision allow. The export subsequently fails because storage is unavailable. A linked execution record says failed; no success claim is inferred from the allow record. At 09:05, the same principal asks for department Q, receives deny, and produces no protected export. Both paths need attributable evidence, not only successful application responses.

If R's record contains a browser-provided user name rather than verified identity, attribution is weak even if its JSON is well formed. If recording stops, a quiet log does not establish that nobody accessed data.

## Boundaries and check

OWASP distinguishes security-event logging from other transaction and operational trails. Use their purpose to determine fields and retention rather than merging everything into one unrestricted dump. Restrict log administration, preserve integrity and test collection outages, disk exhaustion, injection and unauthorized reads. A deployment must explicitly decide whether particular operations can proceed when required audit evidence cannot be durably recorded; silently losing records is not a decision.

**Check:** Does an allow event prove a successful export? No. Policy decision, execution and observed delivery are different events with linked identities.

## Sources

- <https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html>
