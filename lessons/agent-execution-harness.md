# Agent Execution Harness

## Meaning

A harness is the application-owned control layer around model and tool calls. The model proposes actions; the runtime controls authority, budgets, state, retries, recovery and completion. A prompt and a tool list do not implement all of those boundaries.

## Mechanism

Bind each action to its resource and identity, distinguish reads from writes, validate arguments and record outcomes. Checkpoint recoverable state, and reconcile an uncertain external effect before retrying. Approval for one write must not become permission for a different resumed operation. Treat repository and retrieved instructions as untrusted data rather than new authorization.

Ground proposed changes in actual observations. A filename in a request is not a file read. Expose the working directory and revision, obtain a bounded inventory and inspect existing code and acceptance checks before mutation. A listed tool, a selected call and a confirmed result are different evidence states.

## One example

A task asks for a change in project A, but the shell starts in project B. An agent can invent a plausible replacement in B and pass a test it also invented without changing A. The harness should bind the checkout, artifact revision, diff and executed acceptance command to A. A denied read or missing target is an explicit blocker, not permission to manufacture a substitute project.

## Check your understanding

Does a stronger model remove the need for these checks? No. Compare model choices with the harness held fixed and grounded observations with the model fixed. Require independently defined task outcomes and test unauthorized writes, wrong directories, malformed calls, duplicate results, timeouts, approval denial and budget exhaustion. Report completion, mistaken acceptance, escaped effects, recovery cost and latency; self-reported confidence is not the enforcement or success criterion.
