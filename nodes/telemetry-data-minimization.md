---
id: telemetry-data-minimization
title: Telemetry Data Minimization
summary: Telemetry data minimization limits captured and exported fields to the evidence needed for observability instead of treating full prompts, payloads and credentials as default trace content.
type: concept
tags: [observability/collection]
prereqs: [opentelemetry]
sources: [https://opentelemetry.io/docs/security/handling-sensitive-data/]
status: explained
created: 2026-10-22
updated: 2026-10-22
---

# Telemetry Data Minimization

## Meaning

Telemetry data minimization designs useful observation without routinely copying sensitive application content. A structured trace is not harmless merely because it is called metadata: attributes, error bodies, URLs and propagated fields can contain credentials or personal information. This concerns operational telemetry, not selection of a model-training corpus.

## Mechanism

[[opentelemetry]] creates and transports evidence; it cannot determine every application's sensitive fields automatically. Begin with a diagnostic question, then allow only the fields necessary to answer it. Prefer operation kind, stable scoped identifiers, status, size and duration over full request/response bodies. Exclude secrets before instrumentation serializes them when possible. Collector-side deletion, allowlist redaction and transformations are additional controls, not a way to undo exposure in local SDK buffers or earlier exporters.

Trace every destination: process logs, temporary queues, crash reports, Collector, backend and any cloud export. Enforce access scope, encryption, retention and deletion on each retained copy. Redact exception strings and nested attributes as well as ordinary fields. [[context-propagation]] can send sensitive baggage beyond the intended service; a local-only model does not make its telemetry local-only.

## Worked example

A team needs to diagnose slow tool calls. Instead of storing a full command that contains a token, record `operation=report.lookup`, `duration_ms=420`, `outcome=timeout` and a scoped operation ID. These fields support latency and failure analysis without the credential. If exact command replay is necessary for a particular investigation, use a separately authorized, short-lived artifact with explicit access controls rather than silently widening the default trace.

Hashing a small predictable identifier is not anonymization: someone can enumerate candidate values and compare hashes. Even a high-entropy correlation identifier can reveal behavior through repeated joins. Choose whether correlation is necessary, who can perform it and for how long. The OpenTelemetry sensitive-data guidance explicitly warns about predictable-input hashes and recommends avoiding unnecessary collection first.

Test with synthetic canary secrets in prompts, tool arguments, errors, headers and baggage. Inspect the actual exported payloads and intermediate sinks, including failure paths, rather than only a final dashboard. Measure diagnostic sufficiency and leakage together; a completely empty trace is private but may fail its operational purpose.

## Check your understanding

**Question:** Does deleting a field in the backend remove it from earlier exporters? **Answer:** No. Minimize before capture and separately verify every retained or exported copy.

## Prerequisites

- [[opentelemetry]]

## Sources

- <https://opentelemetry.io/docs/security/handling-sensitive-data/>
