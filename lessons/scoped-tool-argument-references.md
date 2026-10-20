# Scoped Tool-Argument References

## Meaning

A scoped tool-argument reference replaces model-generated copies of known payloads with a short handle. The model selects an entry; trusted application code retrieves the original bytes. This shrinks a generation surface without granting the model new resource authority.

## Mechanism

The application creates a [[key-value]] mapping from handles to permitted objects for a particular request. The [[tool-call-execution-contract]] validates the selected handle, verifies its request, actor and tenant scope, resolves it, and checks the resulting operation before execution. The handle is a locator, not a capability to bypass permissions.

Keep the mapping immutable or versioned while a decision is pending. Reject unknown, expired or cross-scope handles; do not interpret an invalid handle as a global object identifier. The application should bind any approval to the resolved object version and relevant arguments. Authorization can change while a run is paused, so current effect permission still needs checking.

OpenAI's function-calling guidance recommends not asking the model to supply arguments already known in code. Scoped references apply that principle when the model must choose among several known objects. Fewer tokens can reduce copying mistakes and cost, but ambiguous choices remain semantic errors. Reference generation, storage and expiry are additional application responsibilities.

## Worked example

A request is allowed to compare two shipping destinations. The host maps `a` to destination version 4 and `b` to destination version 7. The model proposes `ship_to("b")`; the host resolves version 7 without retyping the address.

A concurrent request can also use `b`, but its mapping belongs to another request namespace. Copying that handle into the first request must not expose the other destination. If version 7 changes before approval, the host either retains the approved snapshot or requires a new decision; it must not silently ship to newly substituted bytes.

Test wrong choices separately from malformed handles. Include expiration, duplicate labels, tenant crossover, stale versions and concurrent updates, then compare complete task success, output tokens, latency and failure recovery against direct payload generation.

## Check your understanding

**Question:** Does a valid handle prove permission? **Answer:** No. Resolve it only within the validated scope and enforce the actual operation's policy.
