# Prefill vs Decode

## Meaning

Prefill processes a prompt and constructs its [[kv-cache]]. Decode extends generated state. The phases often have different shapes, but compute-bound and memory-bound are workload findings, not unconditional labels attached to their names.

## Mechanism

Many prompt positions can reuse a dense layer's weights. Ordinary autoregressive decode supplies one new row per active request, but a batch can contain many requests. The resulting token count, context length, architecture and kernels determine the point in the [[roofline-model]]. Short prompts need not saturate arithmetic, and a large decode batch need not remain weight-bandwidth-limited.

A conventional decoder's final prompt position already produces the first output distribution. Sampling that first output does not inherently need another complete weight pass. The following decode step consumes that output to generate the next distribution. Prompt chunking, speculative methods and sparse experts introduce further schedule differences that must be stated explicitly.

## One example

A hypothetical dense region has one million sixteen-bit weights: 2 MB. Assume one token row needs about two million operations and ignore other traffic. One row gives roughly one operation per weight byte. Sixty-four rows sharing the traversal give 128 million operations over 2 MB, or 64 operations/byte. Those rows can be prompt positions or independent decode requests. This demonstrates weight reuse, not equivalence of complete phases or a measured speed prediction.

## Check your understanding

Does one new token per request mean a single-row device workload? No. Count all active requests and retained context. Measure queueing, first-token and inter-token latency, memory and communication before choosing a schedule. Chunking or greater concurrency can exchange throughput, latency, reuse and cache demand rather than improve everything at once.
