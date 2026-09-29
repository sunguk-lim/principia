# Tool-Call Execution Contract

## Meaning

A model's tool call is a *proposal* to use application functionality. The [[tool-call-execution-contract]] defines how the application turns that proposal into a validated, authorized, recorded operation and returns the result. A valid JSON object alone grants no authority.

## Mechanism

The application advertises a tool name and argument schema. The model selects a tool and supplies arguments. The application checks that the tool exists, parses arguments against the real schema, applies identity and resource permissions, enforces budgets, and executes the implementation it owns. [[structured-output]] can help produce parseable arguments, but it cannot guarantee that a request is true or permitted.

Give every execution an identity. Persist the call, outcome, and side-effect receipt in [[agent-session-state]] before relying on it in later reasoning. If execution might have happened but the response was lost, mark it unknown and reconcile before retrying. Idempotency keys or status queries prevent a network interruption from turning one requested action into two actions.

A common `tools` array can reduce adapter code, yet providers differ in parallel calls, schema enforcement, errors, cancellation, and result ordering. Portability is a tested property of the whole loop, not of one JSON shape.

## One example

A model proposes `search_books({"query":"graphs"})`. The host validates a bounded query, performs a read-only search, records the call ID and result, then shows the result to the model. If the model instead proposes `delete_book`, a parser must not invent authority to run it. If a write call times out, the host checks its receipt before retrying.

## Check your understanding

**Question:** What does a syntactically valid tool call prove? **Answer:** Only that it matches a permitted shape under the chosen parser. Authorization, truth, execution, and external outcome require separate checks.
