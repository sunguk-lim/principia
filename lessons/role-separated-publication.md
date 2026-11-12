# Role-Separated Publication

## Meaning

A worker may be allowed to prepare a change without being allowed to publish it. Role-separated publication enforces that distinction in the trusted service. Calling a model “reviewer” or accepting an --as reviewer string is not access control.

## Mechanism

Authenticate the principal through [[agent-workload-identity]], then authorize a specific action on a specific resource. With [[version-controlled-agent-memory]], bind approval to the branch, base revision and exact content digest. A subsequent edit requires renewed validation; an earlier approval must not authorize a different payload. Enforce the publication gate server-side through a [[tool-call-execution-contract]], not only a cooperative client prompt.

Cedar illustrates principal, action, resource and context evaluation. Its authorizer defaults to deny without a matching permit, and a matching forbid overrides permits. Policy evaluation errors appear in diagnostics and are skipped by Cedar, so the embedding application must decide how to handle those errors; do not describe the language as universally failing closed on every malformed policy. Authentication and trustworthy request attributes remain the application's responsibility.

## One example

An invented worker can edit branch draft-A but cannot write main or invoke merge. A reviewer can approve revision D8. A request using the worker's credential but a claimed reviewer name is denied. If draft-A advances to D9 after review, the old D8 approval cannot publish D9. A reviewer authorized for project P must also be denied a merge into project Q.

## Boundaries and check

Test direct-write bypasses, cross-branch actions, expired credentials, changed content, replayed approvals and policy errors. Protect authorization attributes from caller manipulation and record both decision and actual published revision. A human reviewer is one possible principal; separation concerns authority and independent checks, not a promise that any reviewer is infallible.


## Check your understanding

Is a client-supplied reviewer name an identity? No; authentication and server-side authorization are separate requirements.
