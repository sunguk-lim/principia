# Model Alias Pinning

## Meaning

A model identifier can name a fixed snapshot or an alias whose target changes. Model alias pinning is the practice of choosing an explicit revision for a production path when repeatable behavior matters. It is not a rule that all dateless names move: each provider defines its own naming contract.

## Mechanism

A moving alias makes upgrades convenient. The cost is that the effective model can change while the application code and request string stay the same. A new target may alter tool calls, output format, context limits, latency, price, or refusal behavior. A pinned revision is easier to compare and roll back, but it can be deprecated; pinning is a controlled-upgrade policy, not a way to avoid maintenance. Keep the requested ID and, when the API exposes it, the resolved model identity in a [[provider-capability-matrix]]. Evaluate a candidate revision on representative traffic before using a [[progressive-model-rollout]] to promote it.

## One example

A support agent uses a “latest” alias and passes its refund-tool contract today. After the alias moves, the model emits a different tool argument form. A staging conformance run would catch this; a production pinned ID would remain unchanged until the team explicitly promoted the new revision. Conversely, a noncritical exploratory app may rationally accept the moving alias.

## Check your understanding

**Question:** Does a dateless model ID always mean a moving alias?

**Answer:** No. Some providers use dateless IDs for fixed snapshots. Read that provider's versioning contract and record the resolved revision when available.
