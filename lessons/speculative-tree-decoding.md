# Speculative Tree Decoding

## Meaning

A draft tree proposes alternative continuations, allowing one target-model verification step to evaluate several possible token paths. Only a valid accepted path is committed.

## Mechanism

Each tree node must see its own ancestor tokens, not siblings or future branches. Breadth hedges against an early rejected draft; depth aims for a long accepted prefix. Stateful layers need branch-specific temporary state so rejected proposals do not corrupt the live state. Count draft cost, target verification cost, and actual accepted tokens together.

## One example

A single draft chain proposes four tokens and the target rejects token two. A tree that also proposed an alternative at token two may still accept a different continuation, but only if verification scores it under the right prefix.

## Check your understanding

**Question:** Why can more accepted tokens per target pass still fail to lower latency? **Answer:** The drafter, tree construction, masking, or state handling may cost more than the passes saved.
