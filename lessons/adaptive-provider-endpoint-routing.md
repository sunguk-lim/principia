# Adaptive Provider-Endpoint Routing

## Meaning

Provider-endpoint routing chooses where a selected model request runs. It is distinct from choosing the model itself. Two providers serving the same model identifier can differ in availability, cache behavior, request support and effective latency. Adaptive routing changes their traffic shares as measurements change, without treating every endpoint as an interchangeable policy fallback.

## Mechanism

First construct the eligible endpoint set from required capabilities, price ceilings and [[provider-data-policy-routing]]. Apply selection only inside that set. Recent observations can include time to first token, output throughput, failed requests, capacity rejections and effective billed cost after cache effects. [[latency-percentile]] distinguishes a typical response from the slower tail; optimizing only a mean can hide unacceptable waits.

A policy can assign more traffic to endpoints with favorable measured outcomes and retain bounded exploration traffic so previously poor endpoints can demonstrate recovery. Exploration still obeys every hard constraint. Reduce or suspend traffic when failures or capacity rejections rise, then reassess with explicit freshness and recovery rules. Delayed observations and feedback between assigned load and observed latency can make a formerly good endpoint poor. More aggressive adaptation is not automatically more stable.

The current OpenRouter documentation describes recent-traffic-based scoring, weighted selection, small exploration shares, failure suppression and warm-conversation affinity. These are documented implementation choices, not a reproducibility guarantee or a requirement that every router use the same weights. Explicit order or sorting settings may bypass the default policy.

## One example

In an invented workload, eligible endpoints A and B have typical first-token delays of 0.4 and 0.7 seconds. A's price is lower, but a capacity incident raises its rejection rate to 30%; B remains at 1%. A price-only rule continues sending traffic to A, causing retries and possible tail growth. A constrained adaptive rule can shift traffic toward B while retaining a small allowed probe share for A's recovery. If B violates the request's retention rule, however, it is not an eligible rescue: the request must fail or wait under the declared contract. No scoring preference may erase that constraint.

## Check your understanding

Is a preferred latency threshold a hard service guarantee? No. Distinguish preferences from rejection conditions in the actual API. Test stale signals, overload bursts, recovery, cold caches and an empty eligible set. [[provider-failover-semantics]] governs whether and how a failed attempt may be retried. Compare fixed-provider, simple balancing and adaptive policies on complete attempts, including failures, cache misses, total billed cost and tail latency; do not certify application quality from well-formed tool calls alone.

