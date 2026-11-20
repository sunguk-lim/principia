---
id: centralized-data-authorization
title: "Centralized Data Authorization"
summary: "Centralized data authorization applies one policy contract at every trusted data-access path rather than relying on each application to reproduce its own filters."
type: concept
tags: [security/authorization]
prereqs: [row-level-security, agent-workload-identity]
sources: [https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html]
status: explained
created: 2026-11-21
updated: 2026-11-21
---

# Centralized Data Authorization

## Meaning

Centralized data authorization separates the rule deciding who may access which data from the code that displays or requests it. A trusted enforcement point checks a principal, operation, resource and relevant context before releasing data or applying a write. Centralization concerns the policy contract and its ownership; it need not mean one physical server.

## Mechanism

[[agent-workload-identity]] distinguishes the executing service from the requesting human. Bind both to verified server state. A client-supplied user or tenant string cannot establish authority. Evaluate an explicit policy and deny requests without a matching permission; a failure to obtain policy is not an implicit grant.

[[row-level-security]] is one database-owned enforcement mechanism. Middleware and data gateways are other placements, but every reachable path must preserve the same boundary. This requirement is **complete mediation**: checking most requests is insufficient when one unchecked export, background job, direct connection or administrator endpoint can disclose the same resource. UI hiding is not mediation because the unauthorized data can already have reached the browser.

A central policy can be evaluated by several trusted components. Version their rules and authenticated context, constrain direct credentials and define revocation behavior. Caching an allow decision creates another place where old authority can survive. A shared connection alone supplies neither trustworthy end-user identity nor correct row permissions.

## One example

A fictional compensation service permits a manager to read only their own department and HR to read all departments. Three apps request the same table. All calls enter a server-side boundary that derives the caller's group and applies the policy. An export endpoint bypassing this boundary would invalidate the architecture even if all three screens were correct. A shared service account with unrestricted direct access also remains an escape route unless separately constrained.

## Boundaries and check

This architecture reduces duplicated policy logic but concentrates trust and can create a shared outage or misconfiguration domain. It does not make every policy correct, validate query meaning, secure logs or replace execution isolation. OWASP recommends default deny, least privilege and permission validation on every request; it does not prescribe that every system use one vendor or layer.

Test allowed and denied operations through all interfaces, forged principals, stale roles, revocation, unavailable policy state and alternate connection paths. A successful read proves availability for that caller, not absence of bypasses.

**Check:** Can removing an app's WHERE clause be safe? Only if an independently enforced boundary still applies the intended policy on every relevant path.

## Sources

- <https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html>
