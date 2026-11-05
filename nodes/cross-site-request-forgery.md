---
id: cross-site-request-forgery
title: "Cross-Site Request Forgery"
summary: "Cross-site request forgery induces a browser to send a state-changing request using authority the destination implicitly trusts, without establishing the user intended that action."
type: concept
tags: [web/security]
prereqs: [same-origin-policy]
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html"]
status: explained
created: 2026-11-06
updated: 2026-11-06
---

# Cross-Site Request Forgery

## Meaning

Cross-site request forgery, or CSRF, makes a browser carry an attacker-chosen request to a service that mistakes ambient authority for the user's intent. A common case uses automatically attached session cookies. A related local-service case trusts every request reaching a loopback listener even without a logged-in cookie.

## Mechanism

The [[same-origin-policy]] does not prohibit every cross-origin send. Browsers permit ordinary form submissions using certain request types without a CORS preflight. If the destination changes state solely because such a request arrived, an unrelated page may trigger that effect without reading the response. Modern browser network restrictions and application configuration affect actual reachability, so test the specific environment rather than treating every localhost endpoint as exploitable.

Use the framework's maintained CSRF defenses when suitable. For cookie-authenticated state changes, validate a session-bound unpredictable token or another appropriate maintained defense. Verify request origin or Fetch Metadata under an explicit policy, with deliberate handling of missing headers and legitimate cross-origin clients. Do not mutate state through GET. SameSite cookie settings can help but do not replace all other boundaries.

A JSON-only API that rejects simple form media types can require preflighted browser requests, but permissive CORS rules or permissive parsing can undo that protection. Request validation, authentication and authorization remain distinct requirements. Origin headers are not authentication for arbitrary clients, which can manufacture headers.

## One example

An invented local settings endpoint accepts a text/plain form, parses its contents as JSON and writes configuration. A separate page submits that form. Even if its script cannot read the reply, the write may already have happened. The service should reject the unsupported media type and require the intended authorized operation, with browser-origin defenses appropriate to its interface. No real installation or secret change is needed to test the path: use a harmless isolated state counter.

## Check your understanding

Why is “the browser cannot read our response” insufficient? CSRF targets the effect of the request. Validate that untrusted-origin state changes are rejected before the effect, while permitted same-origin and supported non-browser clients still work.

## Prerequisites

- [[same-origin-policy]]

## Sources

- <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html>
