# Gated Delta Network

## Meaning

A Gated Delta Network is a sequence layer that remembers the past in a fixed-size state. It does not keep a separate key–value pair for every previous token. That makes its decode-state footprint independent of context length, but it must compress many events into one representation.

## Mechanism

In [[linear-transformer-attention]], the state summarizes key–value associations. A new key can ask what value the state currently predicts. The delta rule computes the difference between that prediction and the new value, then uses it to correct the state. A learned gate can reduce stale memory before or during that update. The two controls play different roles: forgetting and targeted correction.

The update can be run recurrently, one token at a time, for decoding. Its fixed state size is a resource property, not a guarantee that it remembers arbitrary earlier details. An exact identifier mentioned once near the start may be difficult to recover if later updates compete for the same state.

## One example

A long support conversation repeatedly changes a delivery preference and mentions one tracking number early. A recurrent state may be useful for maintaining the latest preference. Whether it can reproduce the exact tracking number is a separate test, not something the architecture guarantees.

## Check your understanding

**Question:** What does the gate add to a delta update? **Answer:** It controls retention of old state; the delta rule corrects the state for the current key–value observation.
