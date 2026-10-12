# Verifiable Reward Design

## Meaning

A verifiable reward is an executable check that assigns a score to a generated answer or action. It makes repeated evaluation possible, but the code of the checker becomes part of the task definition.

## Mechanism

For arithmetic, parse a final number and compare it with a reference. For code, run pinned tests under an [[execution-benchmark-validity]] contract. Neither check sees everything: a parser can be tricked, and tests can miss untested behavior. Because [[reward-hacking]] can increase the score without improving the real outcome, separate verifier development from held-out evaluation.

## One example

A coding model learns to satisfy one visible test while breaking another behavior. Require both the original failing test to pass and previously passing tests to remain green, then inspect independent held-out cases.

## Check your understanding

**Question:** Does a deterministic reward guarantee a correct task outcome? **Answer:** No. It guarantees repeatable scoring under that verifier, which can still be incomplete or exploitable.
