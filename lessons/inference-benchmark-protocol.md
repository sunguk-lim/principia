# Reproducible Inference Benchmark Protocol

## Meaning

A serving number is conditional on a workload and executable system. A benchmark protocol states those conditions and preserves enough evidence to rerun the measurement. It is not merely a high-concurrency demonstration or the best throughput observed during tuning.

## Mechanism

Use [[load-testing]] to declare arrivals, concurrency, prompt and output-length distributions, caching/warmup, run duration and failure handling. Pin model and tokenizer revisions, runtime and kernel versions, precision, hardware, parallel layout and scheduling limits. State the output-quality contract before changing precision or algorithms. Distinguish client-observed time from server timing and report [[llm-serving-metric-triangulation]] measures for comparable request populations.

Preserve machine-readable configuration, workload or its reproducible generator, per-request outcomes and aggregate computation. [[measurement]] must keep failures, rejected requests, retries and incomplete streams visible. A maximum generation length is not the same as the actual output-length distribution. Warm-cache and cold-cache workloads answer different questions and should not be silently mixed.

## One example

Suppose two invented runs each complete 100 requests in ten seconds: ten requests per second. Run A emits 20 tokens per request; run B emits 200. Their output throughput is 200 versus 2,000 tokens per second, but this does not establish a tenfold better engine: the workloads differed. Likewise, excluding ten failed requests from a latency sample can make its percentiles look better without improving the service. Compare identical input/output contracts, retain every attempted request and report success separately. Pin a seed when useful, but store the realized traffic because a random seed alone may not reproduce timing across clients and versions.

## Check your understanding

Does publishing an exact command make the result reproducible? Only partly. Missing checkpoints, data, dependencies, hardware configuration or measurement scope can still prevent meaningful repetition. Repeat runs, quantify variation and compare changed configurations on a held-out workload rather than tuning on the final report. Primary vLLM benchmarking interfaces and MLCommons inference implementations exemplify explicit workloads and measurements; neither supplies a universal hardware capacity guarantee. The accepted outcome is quality and latency under the stated load, not a context-free leaderboard number.
