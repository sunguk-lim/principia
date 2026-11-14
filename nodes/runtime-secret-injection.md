---
id: runtime-secret-injection
title: "Runtime Secret Injection"
summary: "Runtime secret injection resolves a credential reference for an authorized workload at an execution boundary while limiting its recipients, lifetime and recorded exposure."
type: concept
tags: [security/credentials]
prereqs: [agent-workload-identity, process-environment]
sources: [https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]
status: explained
created: 2026-11-15
updated: 2026-11-15
---

# Runtime Secret Injection

## Meaning

Runtime secret injection keeps a credential value out of ordinary source and workflow artifacts until the authorized operation needs it. The persisted configuration names a reference; a trusted execution component resolves that reference into the channel consumed by the application. A reference is not itself proof that retrieval or use is authorized.

## Mechanism

Bind retrieval to an [[agent-workload-identity]], intended resource and minimum permission scope. A secret manager can return a scoped credential to application memory, a restricted file or another deliberately selected input channel. A [[process-environment]] is a common channel, but descendants and diagnostics can receive it; it is not an encrypted vault. Code that can read the injected value must be treated as a recipient.

Separate three decisions: may this workload retrieve the credential, may it send the credential to this destination, and may it perform this operation? A permitted retrieval does not justify placing the value in a model prompt, an arbitrary URL or a log. Resolve close to use, restrict propagation and record credential identity/version and access outcome rather than the value.

Lifecycle matters after injection. Short-lived credentials can reduce reuse windows; static values need a deliberate rotation and revocation strategy. Refreshing a local reference does not invalidate a stolen copy. Only enforcement at the accepting service, such as expiry or revocation, stops that copy from working. If the secret manager is unavailable, report an explicit blocked operation instead of falling back to a committed plaintext copy.

## One example

A reporting worker has permission to read inventory from service S but not modify it. Its task artifact contains reference `inventory-reader`, not the credential. At the request boundary the trusted worker obtains the permitted version, constructs the authenticated request in memory and records service, operation, status and reference version. A retry to unrelated service T must not carry the same authentication merely because the first endpoint redirected there.

If the credential expires midway, the worker can retrieve a new authorized version and retry only under the operation's failure policy. Restarting the worker alone is not evidence that the expired or compromised version was revoked.

## Check your understanding

Does hiding a secret from a workflow file protect it from arbitrary code in the receiving worker? No. Injection reduces stored and incidental exposure; recipient trust, destination enforcement and lifecycle checks remain separate controls. Test missing references, denied scope, expiry, manager outage, redirects and exception paths without printing a live secret.

## Prerequisites

- [[agent-workload-identity]]
- [[process-environment]]

## Sources

- <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>
