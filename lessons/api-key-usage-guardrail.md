# API-Key Usage Guardrail

## Meaning

An API key authenticates a caller, but a **usage guardrail** narrows what that caller may spend or invoke. A declared policy is not effective until it is assigned to the key, member, or workspace that serves the request.

## Mechanism

Treat a key as a scoped [[capabilities|capability]]: it should authorize only the required models, providers, regions, and budget. A policy may cap spend per period and intersect allowlists across account, workspace, member, and key scopes. More specific assignments should narrow, not silently broaden, the effective authority. The gateway needs an explicit precedence rule and a fail-closed response for a disallowed model, provider, region, or exhausted budget.

Budget accounting is not trivial. Decide whether limits include cached tokens, retries, batch requests, provider-billed BYOK traffic, and in-flight usage that has not yet settled. A daily cap that checks only completed invoices can overshoot under concurrent calls. Separate hard rejection limits from alerts; an alert is observability, not enforcement. Record the policy version and effective scope with each authorization decision, without logging the secret key itself.

## Worked example

A workspace defines a $100 daily cap but never assigns the guardrail to its production key. Calls keep succeeding; the policy document alone enforced nothing. After assignment, test concurrent requests near the limit and verify whether provider-billed traffic counts toward the cap.

**Understanding check:** What is the difference between a budget alert and a fail-closed spend limit?
