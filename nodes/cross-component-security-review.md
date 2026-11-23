---
id: cross-component-security-review
title: Cross-Component Security Review
summary: Cross-component security review follows untrusted data and authority across API, state, policy, tools, and rendering boundaries instead of judging files in isolation.
type: concept
tags: [software/testing]
prereqs: [tool-call-execution-contract, agent-execution-harness]
sources: ["https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/, "https://owasp.org/www-community/attacks/xss/", "https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control", "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html", https://genai.owasp.org/resource/genai-red-teaming-guide/]
status: explained
created: 2026-10-14
updated: 2026-11-24
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

## Identity, object scope and review freshness

Authentication at a gateway identifies a caller; it does not authorize every object identifier that caller can supply. For an ownership-based service, constrain reads and mutations to both the requested object and verified principal or tenant. An illustrative query is `SELECT ... WHERE order_id = :requested AND owner_id = :verified_user`. Never derive `verified_user` directly from a client-supplied header. A gateway may strip and replace such a header, but the downstream service must also authenticate the gateway or otherwise prevent direct callers from forging that assertion. Some domains use shared access or delegated roles rather than owner equality; apply the actual object policy on every relevant path.

Returning the same not-found response for nonexistent and inaccessible objects can reduce existence leakage, but differing timing, counts, caches or related endpoints may still reveal it. Test authorized and unauthorized reads, copies and mutations, forged identity assertions, direct downstream access and revoked rights. An ordinary successful test suite need not exercise any of these negative cases.

Review evidence is revision-scoped. Record the code revision, relevant configuration and traced path, and invalidate that evidence when its premises change. A change in an upstream identity mapper can stale an otherwise unchanged downstream authorization review. Mark that state stale or pending, not vulnerable or safe without analysis. Track the affected path and rerun the boundary checks. GitHub's stale-approval dismissal is a concrete diff-scoped example; broader cross-service evidence invalidation is an application-owned policy, not an automatic property of a scanner. A reviewed-point percentage does not establish the absence of unmodeled attack paths.


## Adversarial campaigns and reproducible findings

A red-team campaign deliberately probes an authorized system against a stated threat model. Review model behavior, application implementation, deployment infrastructure and runtime effects rather than treating a successful adversarial prompt as the whole assessment. OWASP's GenAI guide separates these four areas. A test that elicits disallowed text and a test that reaches an unauthorized external operation establish different findings.

Define the tested revision/configuration, attacker entry point, assumed access, protected property and stopping rules. Use synthetic or otherwise authorized test data and controlled effects. An invented campaign plants a hostile instruction in a retrieved document, then observes whether the agent merely quotes it, proposes an unauthorized action or actually executes one. Preserve the exact causal path and final effect evidence; a model's assertion that it sent data is not a network receipt.

Retain successful negative controls and legitimate tasks to assess false blocks. Reproduce findings on the target revision, validate remediation through the original entry point, and retain regression fixtures without exposing secrets. Attack-set pass rates estimate only tested coverage; they are not a certificate against every adaptive adversary. Findings need scope, preconditions, impact and next action, not merely a count of alarming responses.

## Prerequisites

- [[tool-call-execution-contract]]
- [[agent-execution-harness]]

## Sources

- [https://owasp.org/www-community/attacks/xss/](https://owasp.org/www-community/attacks/xss/)
- [https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control](https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control)

- <https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html>

- <https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/>

- <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches>

- <https://genai.owasp.org/resource/genai-red-teaming-guide/>
