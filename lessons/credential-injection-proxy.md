# Credential Injection Proxy

## Meaning

A credential injection proxy places provider authentication outside the agent runtime. The agent sends a proposed request to a trusted mediator, which checks permission and adds the provider credential before forwarding. This reduces exposure of a valuable token to the model and executable workspace, but it does not eliminate misuse of the authority granted through the proxy.

## Mechanism

Authenticate the runtime with a limited session identity. Bind that identity to allowed resources and operations, not merely a hostname. Validate the destination, method and relevant payload before injecting authentication. Remove caller-controlled authorization fields, prevent credentials appearing in responses or logs, and ensure the runtime cannot simply bypass the mediator.

Redirects need a new forwarding decision: authorization for one origin must not leak to a different recipient. Revoked or expired session authority must stop working even if a task was previously approved. The mediator is therefore an enforcement component, not just a convenience that adds a header.

## One example

A session may read project P but not project Q. The proxy accepts the permitted read, attaches its provider credential internally and returns the permitted response. It rejects the request for Q before injection. If P's endpoint redirects elsewhere, the original approval does not automatically authorize that new destination. Returned project content remains untrusted reference data even though the transport was authenticated.

## Understanding check

Does hiding a token make arbitrary calls safe? No. A compromised agent can still exercise every operation its session permits. Test wrong resources and methods, scope expiry, redirect handling, direct-egress attempts and credential reflection. Keep secret non-disclosure distinct from permission checks and the user's authorization for a specific action.
