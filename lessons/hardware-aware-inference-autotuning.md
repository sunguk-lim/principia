# Hardware-Aware Inference Autotuning

## Meaning

Runtime autotuning searches configuration for a particular model, hardware and workload. It can vary threads, batching, device placement and memory settings. Choosing one kernel's fastest implementation is a narrower problem; it cannot by itself select the best complete inference path.

## Mechanism

Define a quality contract, objective and resource limits first. Reject invalid or unsafe-capacity settings. Measure feasible candidates on representative prompts, generation lengths and concurrency, separating setup, prefill and decode. Retain the chosen setting with its model, hardware and runtime key, and revalidate after relevant changes.

A prediction model can suggest configurations, but its estimate needs held-out validation. A brief startup probe is not enough to certify a long-context service. Bound search cost and preserve a valid fallback. Changes in model precision can also alter quality, so their eligibility requires more than timing.

llama-bench documents phase measurements and configuration sweeps, including thread counts and GPU-layer offload. Its timing excludes tokenization and sampling. A reported token rate therefore does not automatically equal complete user-request performance. These are measurement primitives, not proof of an always-optimal automatic tuner.

## One example

Two configurations fit a 7 GiB limit and preserve accepted quality. A needs 80 ms prefill plus 20 ms per decode step. B needs 140 ms prefill plus 12 ms per step. For 30 decode steps and 40 ms of other measured work, total times are 720 ms and 540 ms.

B is faster overall, but violates a 100 ms prefill constraint. The constrained tuner must choose A or search for another setting. Optimizing only decode rate would make the wrong admissibility decision.

## Check your understanding

Can the startup winner be cached forever? No. Model, runtime, workload and hardware conditions can change. Test held-out traffic, cold caches, contention and resource headroom. Include tuning cost when comparing the selected runtime with the default.
