---
id: inference-cost-break-even
title: Inference Cost Break-Even
summary: Inference cost break-even is the sustained useful utilization at which a fixed-cost local serving system becomes cheaper per accepted token than a metered API under the same quality and latency requirements.
type: concept
tags: [ml/llm/inference]
prereqs: [arithmetic, continuous-batching, prefix-caching, latency-percentile]
sources: [https://www.linkedin.com/pulse/250-server-replaces-up-7900-api-tokens-michael-braverman-mdxof]
status: explained
created: 2026-09-08
updated: 2026-09-08
---

# Inference Cost Break-Even

## Summary

A metered inference API charges for each input, cached-input, and output token, while a
self-hosted server costs money even when no request is running. **Inference cost
break-even** is the sustained fraction of time that the local system must do useful work
before its fixed monthly cost, divided over the accepted tokens it serves, falls below
the API's blended per-token price. The comparison is valid only when both paths meet the
same model-quality and [[latency-percentile]] targets; a cheaper answer that must be
rejected or escalated is not an equivalent unit of work.

## Grounded explanation

### Normalize both choices to the same accepted workload

Let $C_L$ be the local system's monthly fixed cost: hardware rental or depreciation,
power, storage, networking, and attributable operations. Let $r$ be its measured active
throughput in accepted tokens per second, $T$ the seconds in the billing period, and $u$
the fraction of those seconds during which useful inference is actually running. Using
ordinary [[arithmetic]], the local system serves approximately

$$N_L = r u T$$

accepted tokens, so its effective unit cost is

$$c_L(u) = \frac{C_L}{r u T}.$$

This denominator must count accepted work rather than raw generated tokens. Failed
requests, retries, low-quality outputs that are discarded, and local outputs escalated to
a stronger model consume capacity without completing the compared task. Their cost stays
in $C_L$, but they do not increase $N_L$.

For the API, let $n_i$, $n_c$, and $n_o$ be ordinary input, cached-input, and output-token
counts, with prices $p_i$, $p_c$, and $p_o$. Its blended cost per accepted token is

$$c_A = \frac{n_i p_i + n_c p_c + n_o p_o + C_{\text{other}}}{N_A},$$

where $C_{\text{other}}$ includes request fees or other usage-linked charges and $N_A$
uses the same acceptance rule as $N_L$. Keeping the real prompt/output mix matters:
input-heavy extraction and output-heavy generation can have very different blended API
prices even at the same total token count.

### Solve for utilization, then treat the result as a threshold

Ignoring overflow for the moment, the break-even point sets $c_L(u^*) = c_A$:

$$u^* = \frac{C_L}{r T c_A}.$$

If measured useful utilization $u$ is below $u^*$, metered service is cheaper because the
local machine's idle time is spread over too few accepted tokens. Above $u^*$, fixed
capacity can be cheaper because each additional token reuses capacity already purchased.
If $u^* > 1$, the local system cannot break even under the measured throughput and cost;
if it is far below 1, the result still needs capacity, quality, and reliability checks
before it justifies deployment.

Throughput $r$ is not a hardware nameplate value. It depends on the workload and serving
policy. [[continuous-batching]] can increase it by replacing completed sequences with
queued work so expensive weight loads serve more live tokens. [[prefix-caching]] can
avoid repeated prefill for identical leading tokens, increasing useful work per unit of
compute; an API may also discount cached input, so the same workload transformation must
be reflected on both sides. Measure these mechanisms under the actual request-length,
arrival, and cache-hit distributions rather than inserting a short burst's peak rate.

### Cost is constrained by service quality, not optimized alone

A local model and a hosted model are substitutes only for the requests on which they meet
the same acceptance criteria. Compare task success, factual or structured-output
validity, safety requirements, and the chosen [[latency-percentile]] limits alongside
cost. Batch size can raise throughput while worsening time to first token; queueing can
make an apparently cheap saturated server miss its p95 or p99 target. A valid cost point
therefore lies inside the quality and latency constraints, not merely at the maximum
tokens per second.

A hybrid system adds a useful third option. Predictable requests that the local model can
serve within bounds use the fixed server; bursts, failures, and harder requests overflow
or escalate to an API. Its monthly cost is

$$C_H = C_L + N_{\text{overflow}} c_A,$$

which can beat both pure choices by keeping a smaller local server busy without sizing it
for rare peaks. The trade-off is routing complexity and the need to measure escalation
rates honestly.

### Worked instance

Suppose a local server costs $250 for a 30-day month, sustains 2,000 accepted tokens per
second while active, and is compared with an API whose real input/output mix costs
$0.10 per million accepted tokens. Then $T = 2{,}592{,}000$ seconds and
$c_A = 10^{-7}$ dollars per token. The threshold is

$$u^* = \frac{250}{2{,}000 \times 2{,}592{,}000 \times 10^{-7}}
      \approx 0.482.$$

The local server must therefore do useful accepted work about 48.2% of the month to match
the API on unit cost. At 20% utilization it serves about 1.04 billion accepted tokens and
costs roughly $0.241 per million, so the API wins. At 70% it serves about 3.63 billion and
costs roughly $0.069 per million, so the local server wins before any overflow or
operations adjustment. If only 80% of local outputs pass the acceptance rule, the useful
throughput is 1,600 rather than 2,000 tokens per second and the threshold rises to about
60.3%.

### Measurement discipline

Run the comparison over a representative billing cycle. Record request arrivals, accepted
input and output tokens, cache hits, active throughput, queue depth, failures, escalation,
power, operator time, and p50/p95/p99 latency. Recompute $u^*$ across plausible API-price,
demand, model-quality, and hardware-cost ranges. This sensitivity analysis is what turns
a one-month anecdote into a deployment decision: the break-even value is not a universal
property of a GPU or model, but a threshold induced by one workload, one quality bar, and
one cost structure.

## Prerequisites

- [[arithmetic]]
- [[continuous-batching]]
- [[prefix-caching]]
- [[latency-percentile]]

## Sources

- https://www.linkedin.com/pulse/250-server-replaces-up-7900-api-tokens-michael-braverman-mdxof
