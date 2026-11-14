# Runtime Secret Injection

## Meaning

Runtime injection separates a stored credential reference from the credential value used by an authorized operation. A workflow can retain the reference without embedding the secret in source, prompts or ordinary artifacts. This reduces exposure; it does not make the receiving program untrusted-safe.

## Mechanism

Authenticate the [[agent-workload-identity]], check its credential scope, then resolve the reference through a trusted component near the point of use. Choose the receiving channel deliberately. A [[process-environment]] can deliver the value, but receiving code, descendants and diagnostics may read it. A restricted file or direct in-memory integration has different propagation risks.

Retrieval permission, destination permission and operation permission are distinct. Possessing a credential does not authorize sending it to any host or performing every operation. Record the reference version and access outcome without the value. Expiry and revocation must be enforced where the credential is accepted; restarting a worker does not invalidate a stolen copy.

## One example

A reporting worker can read inventory from service S. Its task artifact names `inventory-reader`. The trusted execution boundary resolves the permitted version and constructs the authenticated request in memory. It records request ID, service, operation and status. A redirect to unrelated service T must not automatically receive the same authentication.

If the credential expires, the worker follows an explicit refresh and retry policy. If the secret manager is unavailable, it reports the operation blocked instead of falling back to a plaintext credential copied into the repository. Test denied scope, missing references, expiry, manager outage and error paths with fake values.

## Check your understanding

Does avoiding a hardcoded credential prevent arbitrary code in the worker from reading the injected value? No. Injection limits stored and incidental exposure. Recipient trust, least privilege, propagation limits and credential lifecycle remain necessary boundaries. A successful lookup is also not proof that the requested business action was authorized or completed.
