# Agent Side Effect Invariants

## Meaning

An agent can reach its requested goal and still violate a “do not” constraint. **Side-effect invariants** describe forbidden changes, such as “no order placed” while adding an item to a cart. Goal success and constraint preservation need separate evidence.

## Mechanism

Write the task as desired postconditions plus invariants. For a shopping task, `item in cart` is a postcondition; `orders unchanged`, `no payment attempt`, and `saved cards untouched` are invariants. In a controlled evaluation, compare relevant pre/post state and record the action-event log. A state diff alone can miss a transient side effect later reversed, while an event log alone may miss an uninstrumented external change. Both should be scoped to the task, because checking every unrelated field can create false failures.

At runtime, the [[agent-execution-harness]] must enforce high-impact constraints before an effect executes. The model's proposed tool name, reasoning, or click description is not authorization; the [[tool-call-execution-contract]] validates the actual target, arguments, and resource scope. Read-only actions, reversible writes, and irreversible commits can use different policies. A payment or external submission may require a deterministic deny rule or an approval bound to exact arguments. A later verifier cannot undo an already committed payment.

## One example

A shopping agent adds a mug to a cart but a payment endpoint remains forbidden. The cart goal can pass while the no-payment invariant fails.

## Check your understanding

**Question:** Why must an irreversible-action gate run before the tool call?

**Answer:** An end-of-run check cannot undo a payment already committed.
