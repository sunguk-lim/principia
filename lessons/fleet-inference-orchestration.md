# Fleet Inference Orchestration

## Meaning

Fleet inference orchestration coordinates engine instances into one serving system. An engine can already use multiple GPUs; the distinction is between executing model work and coordinating requests, ready capacity and reusable state across instances.

## Mechanism

The request path uses [[cache-aware-inference-routing]] to choose a worker from reuse and load signals. The control path applies [[latency-driven-inference-scaling]] to adjust capacity over a slower interval. The state path uses mechanisms such as [[tiered-kv-cache]] to locate and restore reusable state. [[prefill-decode-disaggregation]] adds a state handoff between prompt and generation pools.

These paths must agree about worker readiness, model identity and state compatibility. More workers do not guarantee more useful cached prefixes. A cache index can lag eviction, and a requested scaling change may not yet be ready. Each boundary needs an observable failure and fallback policy.

## One example

Worker A has the request's prefix but a 70-millisecond queue and 5 milliseconds of remaining prefill. Worker B has a 10-millisecond queue but needs 40 milliseconds of prefill. Their simplified first-token estimates are 75 and 50 milliseconds, respectively. Choosing the cache hit alone would be wrong in this example.

If prompt and generation pools are separate, add their measured handoff and decode-queue costs to the same request estimate. A planner can address sustained overload, but newly requested workers do not help until ready.

## Check your understanding

Does optimizing one engine establish that the whole fleet is faster? No. Coordination adds routing, discovery and state-transfer work. Compare against a simpler load-balanced baseline at equal resources, and test stale state, worker failure and interrupted handoff. Measure end-to-end latency, recomputation, errors and cost rather than combining unrelated component benchmarks into a claimed system speedup.
