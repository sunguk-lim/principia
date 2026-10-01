---
id: connector-oauth-scope-management
title: Connector OAuth Scope Management
summary: Connector OAuth scope management requests and retains only the third-party permissions needed for a user's selected data source and rechecks them when access changes.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-authorization-boundary, measurement]
sources: [https://developers.google.com/identity/protocols/oauth2/scopes, https://developers.google.com/identity/protocols/oauth2/web-server]
status: explained
created: 2026-10-02
updated: 2026-10-02
---

# Connector OAuth Scope Management

## Summary

A user-data connector needs delegated access to a third-party source. **OAuth scope management** defines which operations the application requests, what the user consented to, how the grant is stored, and what happens when consent expires or is revoked. A successful token exchange is not blanket authority over the user's files.

## Grounded explanation

For a document-retrieval connector, start with the smallest provider scope that supports the selected documents and operations. Google publishes distinct OAuth scopes with different access breadth and sensitivity; choose the current provider-defined scope rather than infer rights from a display label. Bind the callback to the initiating session, validate the authorization response, store tokens outside model context, and make the connector act as the authorized user. A refresh token extends access only within the grant's scope; it does not make a previously indexed document perpetually available.

A [[retrieval-authorization-boundary]] must still check document-level permissions before content reaches a model. OAuth scopes grant API-level capability, while folder selection, per-file ACLs, and tenant membership can impose narrower limits. If a user disconnects a source or a provider revokes access, stop sync and make stale indexed copies unavailable according to the data-retention policy.

For example, a user grants read access to one drive folder. A broad token may technically list other folders, but the application must keep the chosen resource boundary and the user's identity attached to every indexed chunk. Test denied grants, expired tokens, revoked access, scope upgrades, cross-tenant callbacks, and stale index visibility. With [[measurement]], track unauthorized retrieval (target zero in tested scopes), reconnect failures, and sync delay without logging tokens or document bodies.

## Prerequisites

- [[retrieval-authorization-boundary]]
- [[measurement]]

## Sources

- [Google OAuth 2.0 scopes](https://developers.google.com/identity/protocols/oauth2/scopes): provider-defined permission scopes and sensitivity.
- [Google web-server OAuth flow](https://developers.google.com/identity/protocols/oauth2/web-server): authorization flow and token handling.
