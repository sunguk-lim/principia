---
id: cross-component-security-review
title: Cross-Component Security Review
summary: Cross-component security review follows untrusted data and authority across API, state, policy, tools, and rendering boundaries instead of judging files in isolation.
type: concept
tags: [software/testing]
prereqs: [tool-call-execution-contract, agent-execution-harness]
sources: ["https://owasp.org/www-community/attacks/xss/", "https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control", "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html"]
status: explained
created: 2026-10-14
updated: 2026-11-06
---

# Cross-Component Security Review

## Summary

Cross-component security review follows untrusted data and authority across API, state, policy, tools, and rendering boundaries instead of judging files in isolation.

## Grounded explanation

A component can be locally correct while an unsafe path exists through several components. **Cross-component security review** traces where data enters, how it is stored or transformed, which authority it carries, and where it is rendered or used for a side effect. This is especially important for agent-built changes that add an API, model response parser, policy, tool, and dashboard in one patch.

For example, incident text accepted by an API can be stored in shared state and later inserted into dashboard HTML. The rendering line is the XSS sink, but the exploit path starts at the API and crosses storage. A separate path may let the API read another user's incident because ownership checks are missing. A [[tool-call-execution-contract]] and [[agent-execution-harness]] also require checks before a model-suggested action becomes a tool call; merely validating JSON or passing unit tests does not enforce authority.

Four distinct boundary checks illustrate the method. Render stored incident text with output encoding appropriate to its HTML context so it cannot become script. Check object ownership at every API read and write, not only whether the caller is logged in. Restrict an outbound model-client URL to approved schemes and destinations so an attacker cannot redirect credentials or server requests. In fixture mode, a missing fixture must fail closed rather than silently using a live client. Each check needs an end-to-end adversarial test through the entry point, not only a helper-level unit test.

Review a change by drawing a data-and-authority path, then test malicious input at the entry point and observe the final sink or action. Cover output encoding, object-level authorization, URL/destination allowlists, fixture-to-live fallback, and logs that might expose sensitive data. Static findings are hypotheses: reproduce exploitability and check that the fix closes the entire path without blocking legitimate use.

## Review scope and migration invariants

Diff-scoped review asks what a change introduces or modifies; whole-repository review asks which relevant paths exist in the committed system, including unchanged entry points and sensitive operations. Neither scope guarantees complete coverage. Inventory routes, configuration and sensitive calls, then record which paths and deployment assumptions were actually examined. A finding outside the changed lines still needs reachability and impact evidence.

A framework migration can preserve feature behavior while dropping a security check that lived in old middleware. Express invariants as executable boundary contracts: unauthorized state changes are rejected, unsupported body formats are rejected before parsing, and every sensitive effect observes its intended origin and permission checks. Run these through the new entry point rather than assuming the replacement framework inherits the old defaults.

For an invented settings route, a legitimate JSON update still passes after migration. That proves only its happy path. Add isolated negative cases for missing authority, disallowed request origin, unsupported media type and a malformed body; observe that no mutation reaches the settings writer. Keep the previous invariant suite and an explicit map from each old enforcement point to its new owner. A larger passing test count does not compensate for losing these specific properties.

## Prerequisites

- [[tool-call-execution-contract]]
- [[agent-execution-harness]]

## Sources

- [https://owasp.org/www-community/attacks/xss/](https://owasp.org/www-community/attacks/xss/)
- [https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control](https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control)

- <https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html>
