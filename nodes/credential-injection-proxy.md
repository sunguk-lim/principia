---
id: credential-injection-proxy
title: Credential Injection Proxy
summary: A credential injection proxy keeps provider credentials outside an agent runtime while authorizing scoped outbound operations and attaching credentials only at the trusted forwarding boundary.
type: concept
tags: [security/credentials]
prereqs: [agent-workload-identity, http]
sources: [https://www.anthropic.com/engineering/claude-code-sandboxing, https://code.claude.com/docs/en/security]
status: explained
created: 2026-11-18
updated: 2026-11-18
---

# Credential Injection Proxy

## Meaning

A credential injection proxy lets a constrained agent request an authorized operation without receiving the provider's long-lived credential. A trusted component validates the request and adds the credential just before forwarding it. The model can propose a request; it does not decide which destination or operation deserves authority.

## Mechanism

Unlike [[runtime-secret-injection]], which can deliver a secret into the consuming workload, the mediation boundary keeps the upstream credential outside that workload. [[ssrf-destination-validation]] explains the separate requirement to constrain the actual outbound connection and each redirect.

The runtime authenticates to the mediator using a constrained session capability or equivalent [[agent-workload-identity]]. The proxy binds that caller to allowed accounts, resources and operations. It validates the resolved [[http]] destination, method and relevant payload, removes untrusted authorization fields, and attaches the appropriate provider credential only for the approved upstream request. Responses and diagnostic logs must not reflect the injected value back to the runtime.

Keeping the credential elsewhere is only one part of the boundary. If the agent can bypass the proxy, choose arbitrary recipients, or ask for every operation at an approved host, it may still misuse the user's authority. Restrict direct egress, scope resources and operations, recheck revocation, and treat redirects as new forwarding decisions rather than blindly carrying authorization to a different origin. Host approval alone is not authorization for every account or method on that host.

Anthropic's sandboxing report describes a concrete Git proxy: the isolated client uses a scoped credential; the mediator validates the interaction before attaching the GitHub credential. This is an example of the mechanism, not proof that every sandbox or proxy has equivalent enforcement. Current deployment policy must be checked independently of an older product description.

## Worked example

An isolated assistant may read project P through mediator session S but may not delete branches or access project Q. A read request for P passes validation and receives a provider-authenticated response without exposing the provider token. A request for Q fails before injection. A redirect to another host must not inherit P's authorization merely because the initial URL was allowed. A legitimate read can still return untrusted data; authentication of the transport does not promote that data into instructions.

## Boundaries and validation

The proxy becomes a trusted, security-sensitive component and needs protected credential storage, minimal logs, restricted administration and tested rotation. A compromised runtime may still exercise every operation that S permits. Short-lived narrowly scoped runtime credentials limit that exposure but do not make the runtime harmless.

Test wrong caller, expired scope, wrong account, forbidden method, payload substitution, redirects, direct-egress attempts and header reflection. Audit whether the intended operation actually reached the intended upstream without recording its credential. Distinguish secret non-disclosure, policy enforcement and task approval: successful mediation proves neither that the user wanted the action nor that its result is correct.

## Sources

- <https://www.anthropic.com/engineering/claude-code-sandboxing>
- <https://code.claude.com/docs/en/security>
