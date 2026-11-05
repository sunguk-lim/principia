---
id: ssrf-destination-validation
title: "SSRF Destination Validation"
summary: "SSRF destination validation constrains the actual outbound connection and every redirect to approved destinations, avoiding separate unchecked name resolution between validation and use."
type: concept
tags: [web/security]
prereqs: [http]
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html"]
status: explained
created: 2026-11-06
updated: 2026-11-06
---

# SSRF Destination Validation

## Meaning

Server-side request forgery, or SSRF, occurs when attacker-influenced input makes a server send a request using network reachability or authority the attacker should not control. A URL-fetching feature must constrain where the server actually connects, not only whether the submitted text resembles a valid URL.

## Mechanism

[[http]] depends on resolving a hostname and opening a connection. Apply a deliberate scheme, hostname, port and destination-network policy using maintained URL and address parsers. An allowlist of expected services is easier to reason about than unrestricted fetching with a growing list of exceptions. Account for IPv4, IPv6 and alternate textual address representations; do not use string prefixes as a network-membership test.

A separate DNS check creates a time-of-check/time-of-use gap. If validation resolves a name to an approved address but the HTTP client resolves it again, a changing answer can select a different destination. Ensure the client connects only to validated addresses, while retaining the original hostname for HTTP routing, TLS server-name indication and certificate verification. Do not disable TLS checks to make address binding work. Apply the policy again to redirects, retries and fallback connections; a permitted first hop does not authorize its next hop.

Network egress restrictions provide an additional enforcement boundary. They do not replace application context: two publicly reachable services can still have different authorization and credential policies. Do not forward privileged headers across a redirect merely because both addresses are public.

## One example

An invented fetcher validates `docs.example.test`, whose first lookup returns an allowed public destination. A second unchecked lookup returns a loopback address. The original hostname check passed, but the connection crossed the intended network boundary. Binding connection selection to the validated address closes that particular race; rejecting forbidden redirect targets closes a different path.

## Check your understanding

Is hostname allowlisting sufficient against changing DNS answers? Not by itself. Test destination selection with an isolated resolver and harmless local fixtures, including mixed address families, redirects and retries. Record the actual peer and policy decision without contacting sensitive internal endpoints.

## Prerequisites

- [[http]]

## Sources

- <https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html>
