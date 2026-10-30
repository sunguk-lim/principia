# Latency-Driven Inference Scaling

## Meaning

Latency-driven inference scaling changes worker capacity to meet declared first-token and inter-token targets. It is not equivalent to maximizing GPU utilization. With [[prefill-decode-disaggregation]], prompt processing and token generation can require different replica counts.

## Mechanism

Use [[measurement]] of representative traffic and worker behavior to compare candidate configurations. Input/output lengths, prefix reuse, batch composition and cache pressure affect capacity. [[inference-request-scheduling]] explains why a fixed request rate can produce different queueing and token delays across workloads.

Separate target, requested and ready replica counts. A controller can choose the correct eventual capacity yet react too late because model startup takes time. Predictive policies estimate future demand; reactive policies respond to current queue or memory pressure. Both need a resource budget, bounded changes and validation of the actual resulting latency.

## One example

For one measured prompt mix, a prefill replica sustains 40 requests per second at the chosen target. Demand becomes 90. Two nominal replicas provide 80 and three provide 120, assuming the measured capacity scales well enough. If the third replica takes 20 seconds to become ready, a constant-rate approximation accumulates `(90-80)*20=200` queued requests. Eventual capacity does not prevent a temporary target violation.

Now let response lengths double. Decode capacity may become the limiting stage even with adequate prefill capacity. Adding more prefill replicas does not necessarily improve inter-token latency.

## Check your understanding

Does a desired count of three prove three useful workers are serving? No. Verify readiness and successful requests. Compare fixed, reactive and predictive policies on the same traffic traces; measure target attainment, queueing, rejection, startup time, oscillation and ready resource cost. Service estimates and linear arithmetic are hypotheses to test, not universal throughput guarantees.
