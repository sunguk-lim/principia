---
id: secret-output-redaction
title: "Secret Output Redaction"
summary: "Secret output redaction removes or transforms sensitive fields before they cross logging, tracing, artifact or response boundaries without substituting for access control."
type: concept
tags: [security/credentials]
prereqs: [trace-span, log-record]
sources: [https://opentelemetry.io/docs/security/handling-sensitive-data/, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]
status: explained
created: 2026-11-15
updated: 2026-11-15
---

# Secret Output Redaction

## Meaning

Redaction prevents sensitive content from appearing in an output that has a broader audience or retention policy than the original operation. Secrets include credentials; personal or confidential data can require similar treatment. A display that hides a field after its raw form was already exported is too late for that export boundary.

## Mechanism

Start by not collecting unnecessary sensitive data. Define allowed fields and transformations before emitting a [[log-record]] or [[trace-span]]. Structured filtering can drop an authorization header while retaining method, destination class and status. Free-form bodies, stack traces and subprocess output need their own policy: a clean attributes map does not sanitize an exception message.

Apply protection before durable storage and before each independent export. A downstream filter cannot undo disclosure to an earlier collector. An allowlist of permitted output fields can be easier to reason about than an expanding blacklist. Pattern matching remains useful defense in depth, but encodings, multiline values, partial values and new credential formats limit any claim of universal detection.

Replacing a value with a fixed marker removes its diagnostic detail. Hashing preserves equality for correlation but is not guaranteed anonymization: low-entropy values can be guessed and hashes compared. Store a non-sensitive credential reference or version when that suffices instead of a derivative of the credential itself. Redaction also does not revoke a credential or repair an earlier authorization failure.

## One example

A worker receives a denied API response. Its ordinary success log contains only request ID and status, but the HTTP exception serializes request headers. The error path would therefore expose the credential even though the success path looks clean. A structured boundary retains `request_id=r17`, `status=403` and `credential_ref=reader-v3`, and omits the authorization field and raw exception body before the record reaches storage.

Use a deliberately fake canary in a test response, an error, a nested JSON field and subprocess stderr. Assert both that the canary is absent from every exported artifact and that useful status fields remain. A test that only checks the terminal display misses a trace exporter retaining the original payload.

## Check your understanding

Is a redaction rule permission to send confidential input to an unauthorized model and filter its final answer? No. The input has already crossed the boundary. Redaction limits output exposure and complements, rather than replaces, authorization and minimization.

## Prerequisites

- [[trace-span]]
- [[log-record]]

## Sources

- <https://opentelemetry.io/docs/security/handling-sensitive-data/>
- <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>
