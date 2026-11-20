# Centralized Data Authorization

## Meaning

Centralized data authorization separates the rule deciding who may access which data from the code that displays or requests it. A trusted enforcement point checks a principal, operation, resource and relevant context before releasing data or applying a write. Centralization concerns the policy contract and its ownership; it need not mean one physical server.

## Mechanism

[[agent-workload-identity]] distinguishes the executing service from the requesting human. Bind both to verified server state. A client-supplied user or tenant string cannot establish authority. Evaluate an explicit policy and deny requests without a matching permission; a failure to obtain policy is not an implicit grant.

[[row-level-security]] is one database-owned enforcement mechanism. Middleware and data gateways are other placements, but every reachable path must preserve the same boundary. This requirement is **complete mediation**: checking most requests is insufficient when one unchecked export, background job, direct connection or administrator endpoint can disclose the same resource. UI hiding is not mediation because the unauthorized data can already have reached the browser.

A central policy can be evaluated by several trusted components. Version their rules and authenticated context, constrain direct credentials and define revocation behavior. Caching an allow decision creates another place where old authority can survive. A shared connection alone supplies neither trustworthy end-user identity nor correct row permissions.

## One example

A fictional compensation service permits a manager to read only their own department and HR to read all departments. Three apps request the same table. All calls enter a server-side boundary that derives the caller's group and applies the policy. An export endpoint bypassing this boundary would invalidate the architecture even if all three screens were correct. A shared service account with unrestricted direct access also remains an escape route unless separately constrained.

## Check your understanding

Can removing an app's WHERE clause be safe? Only if an independently enforced boundary still applies the intended policy on every relevant path.
