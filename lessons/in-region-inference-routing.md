# In-Region Inference Routing

## Meaning

A model's vendor address does not determine where an inference request is decrypted, processed, stored, or forwarded. **In-region inference routing** constrains the entire request path to permitted geography, including the gateway, provider endpoint, and any server-operated tools.

## Mechanism

The regional endpoint acts as an admission filter over eligible provider deployments. [[load-balancing]] may choose among those deployments, but must not silently fall back to a global endpoint when none is available. A fail-closed response makes that absence visible. A separate guardrail can prevent a key or workspace from accidentally using the global domain; merely offering a regional URL does not enforce that every caller uses it.

Trace the full path: client connection, TLS termination and decryption, routing service, inference host, tool execution, logs, caches, backup, and support access. A server tool is an external effect under a [[tool-call-execution-contract]], so it must be disabled or regionalized if its traffic could cross the boundary. The provider's current documentation and contract define the actual guarantee; a regional model catalog is a necessary availability check, not a legal attestation.

## Worked example

An EU service calls a model available globally but not from any EU provider. The regional endpoint must return an explicit failure. Sending the same request to the global endpoint and receiving a good answer would violate the location constraint, even if the model company has EU offices.

**Understanding check:** Why does a regional model name alone fail to establish end-to-end residency?
