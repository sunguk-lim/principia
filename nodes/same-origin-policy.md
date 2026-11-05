---
id: same-origin-policy
title: "Same-Origin Policy"
summary: "The same-origin policy restricts browser script access across scheme-host-port origins while permitting some cross-origin sends and embeddings."
type: concept
tags: [web/security]
prereqs: [http]
sources: ["https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy"]
status: explained
created: 2026-11-06
updated: 2026-11-06
---

# Same-Origin Policy

## Meaning

The same-origin policy is a browser isolation rule. For ordinary web URLs, an origin is the triple of scheme, host and effective port. Two pages sharing that triple can usually access each other's permitted document and data interfaces; changing any component creates a different origin. A URL path is not part of the origin.

## Mechanism

[[http]] separates sending a request from receiving and interpreting its response. The browser's same-origin restrictions apply differently to these actions. Cross-origin reads are generally restricted, while some navigations, form submissions and resource embeddings are allowed. A server therefore must not infer that a request is authorized merely because an unrelated page could not read its response.

Cross-Origin Resource Sharing, or CORS, is a server-controlled mechanism for permitting selected browser script reads and certain preflighted requests. It is not authentication, and it does not govern arbitrary non-browser clients. A browser may send a permitted simple request without first asking the destination for CORS permission. Other browser policies can additionally restrict particular requests; this is not a promise that every cross-origin request always succeeds.

## One example

Compare `https://example.test/a` with `https://example.test/b`: same origin. Changing the second URL to `http://example.test/b`, `https://example.test:8443/b` or `https://api.example.test/b` changes the scheme, port or host respectively. Those are different origins even if one organization operates them.

Now imagine a local HTTP administration service and an unrelated web page. If a browser can send a form request to the service, hiding its response from that page does not undo a state-changing action. The local server needs its own authorization and request-origin policy. Loopback binding limits network reachability but does not turn every browser-originated local request into user intent.

## Check your understanding

Does a CORS error prove the server performed no action? No. Inspect whether the error blocked dispatch or only response access. Use isolated browser/server tests and distinguish observed request receipt, side effect and script-readable response.

## Prerequisites

- [[http]]

## Sources

- <https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy>
