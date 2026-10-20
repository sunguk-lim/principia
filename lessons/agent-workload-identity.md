# Agent Workload Identity

## Meaning

An agent workload identity is the identity of the software performing resource operations. It is not the model's personality, the chat participant's account or proof that a proposed action was approved. Separating these identities lets a platform attribute effects and limit what a compromised runtime can do.

## Mechanism

The [[agent-execution-harness]] checks actions before tool execution. The platform also checks a principal: an authenticated software identity to which resource permissions are granted. Authentication establishes who the caller is; authorization determines whether that caller may perform a particular operation on a resource. Neither proves that the operation matches the current user's intent.

Google Cloud documents service accounts, federated identities and managed agent identities as workload-identity options. Federation can exchange an external workload identity for short-lived credentials rather than embedding a long-lived service-account key. Exact issuer, deployment binding and supported resources are platform contracts that must be verified, not inferred from a product label.

Grant the runtime only required permissions, separate environments and resource scopes, and preserve both workload and requesting-user provenance in effect records. A workload may have technical permission to publish while application policy still requires approval. Conversely, user approval cannot grant a runtime permissions its platform principal lacks. Resuming a persisted run must reestablish the current execution identity and enforce any revoked or expired permissions.

## Worked example

A support agent reads product-policy documents and proposes a draft response. Its principal can read the policy bucket but cannot change billing settings. A tool call to update billing fails authorization even if the model emits valid arguments.

Publishing uses a separate authorized operation after the application validates the requested audience and approval. If publication permission is revoked during a pause, an old approval does not restore it. Records should identify the workload, user request, approved payload and observed result rather than attributing all activity to one shared administrator key.

Test wrong-environment credentials, cross-tenant resources, expired credentials, revocation during resume and confusing read versus write roles. Compare auditability and blast radius, not just successful API access.

## Check your understanding

**Question:** Does possessing a workload identity make every model-selected action authorized? **Answer:** No. Platform permissions and application-owned intent and approval checks are separate boundaries.
