# Sequence-Level Reliability

## Meaning

Sequence-level reliability asks whether a whole output or operation meets its acceptance contract. It distinguishes token correctness, syntax validity, correct arguments and a successfully completed external task. These events are related but are not interchangeable metrics.

## Mechanism

First define success. An exact reference string rejects harmless paraphrases; a schema checker accepts syntactically valid but wrong values; an external postcondition can reveal an unsuccessful effect despite flawless JSON. Count complete outcomes with [[measurement]] and keep these contracts separate.

The [[probability-chain-rule]] can factor the probability of one complete sequence into next-token probabilities conditioned on the exact preceding tokens. It does not turn a marginal token-accuracy average into a sequence-success probability. Token errors can be correlated, length distributions can differ, and several sequences can be valid.

System interventions target particular failure surfaces: constrain supported syntax, remove unnecessary generated fields, resolve identifiers in code, validate semantics and reconcile tool outcomes. Shorter generation is a hypothesis to test, not a monotonic reliability law: deleting an important disambiguating field can make a call shorter and less correct. Decomposing one decision can introduce new cross-stage errors.

## Worked example

Consider 100 calls of 100 tokens each: 10,000 token positions. In system A, every call has exactly one erroneous token. There are 100 errors and 99% token accuracy, but zero completely correct calls.

In system B, one call has all 100 tokens wrong while the other 99 calls are fully correct. There are again 100 errors and 99% token accuracy, but 99% completely correct calls. Equal token accuracy permits radically different call-level reliability because error dependence differs.

This example uses exact-token correctness for clarity. A real tool evaluation must additionally distinguish equivalent valid outputs and business correctness. Report whole-call success by tool, argument type and length, with sample sizes, uncertainty, unsafe effects, retries, latency and cost on held-out and shifted traffic.

## Check your understanding

**Question:** Is a 99% average token score enough to predict long-call success? **Answer:** No. Measure the complete contract and inspect dependence and acceptable alternatives.
