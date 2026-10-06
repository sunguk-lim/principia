---
id: decision-actuation-consistency
title: Decision–Actuation Consistency
summary: Decision–actuation consistency requires a computed decision, the downstream actuator's reported state, and the user-visible state to agree within an explicit lag and failure policy.
type: concept
tags: [ml/ai-systems]
prereqs: [ml-system-freshness]
sources: [https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html, https://developers.google.com/machine-learning/guides/rules-of-ml#rule_8_know_the_freshness_requirements_of_your_system]
status: explained
created: 2026-10-07
updated: 2026-10-07
---

# Decision–Actuation Consistency

## Summary

A computed decision is not an applied decision. A service can produce a new value while a physical device, downstream database, human operator, or customer-facing channel still exposes the old one. Consistency requires an explicit rule for when the new decision becomes visible and how the system knows that the intended change actually happened.

## Grounded explanation

Separate at least three timestamps or versions: decision computed, actuator acknowledged or reported, and user-visible state published. [[ml-system-freshness]] measures the age of information used at a decision boundary; this concept extends the boundary to the effect. For a device, a *desired* state is a command or intent and a *reported* state is evidence about what the device says it has applied. AWS IoT Device Shadows document this separation. An acknowledgment that a command was accepted is weaker than confirmation that the physical or user-visible state changed.

For example, a pricing service may compute a new number before all shelf labels and checkout systems can display it. Publishing one channel first can create a mismatch even if the prediction itself is fresh. A safer policy might stage a version, wait for relevant acknowledgments, then expose it within an update window; another policy might allow bounded temporary mismatch with a defined fallback. Neither daily batching nor real-time streaming is universally required. The choice depends on actuator capacity, consistency obligations, customer expectations, and measured benefit from faster decisions.

Model the effect path as a state machine: proposed, accepted, applied, observed, and retired or rolled back. Use version identifiers and idempotent updates so retries do not silently apply a different decision. Timeouts and missing acknowledgments must have an explicit policy rather than being interpreted as success. For human-operated changes, observation may be delayed or sampled; state clearly which claims are verified and which remain inferred.

Validate by injecting delayed, duplicated, rejected, and partially applied updates. Measure compute-to-apply and compute-to-visible lag, mismatch duration, stale display rate, failed updates, and actual task outcomes. Compare a faster policy against a bounded-cadence baseline under the same workload. Do not infer an exact optimal cadence or customer response from an unsourced newsletter scenario.

## Prerequisites

- [[ml-system-freshness]]

## Sources

- [AWS IoT, Device Shadow service](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html): separates desired and reported device state.
- [Google, Rules of Machine Learning, Rule 8](https://developers.google.com/machine-learning/guides/rules-of-ml#rule_8_know_the_freshness_requirements_of_your_system): determine freshness requirements from actual system behavior.
