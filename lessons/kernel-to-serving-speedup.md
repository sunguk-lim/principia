# Kernel-to-Serving Speedup Transfer

## Meaning

A faster [[cuda-kernel]] does not automatically make an entire inference request faster by the same factor. The useful result is the change in the complete request path, at the same quality and workload, not the isolated component ratio.

## Mechanism

Locate the operation in the real request. [[prefill-vs-decode]] have different shapes and reuse. [[continuous-batching]] can change those shapes between iterations. A kernel that wins on one isolated shape can lose on the shapes or conversion path selected by the service.

For a fixed serial workload, split baseline time into unchanged work and the part improved. If total time is T, fraction f is improved and that part becomes s times faster, new time is T*((1-f)+f/s). The complete speed ratio is the reciprocal of the bracket. This formula assumes serial time attribution and unchanged work. Overlap, queueing and changed scheduling require new traces rather than blindly reusing the fraction.

## One example

A request takes 100 ms, including 40 ms in a kernel. Making the kernel twice as fast gives 60+20 = 80 ms, so overall speedup is 100/80 = 1.25. A new 5 ms conversion changes this to 85 ms, or about 1.18 times. Even eliminating the kernel entirely cannot beat the remaining 60 ms under this serial model.

## Check your understanding

Can a local two-times ratio predict service p95? No. Use [[measurement]] of matched offered load, first-token and inter-token latency, completion tails, throughput, errors and conversion/fallback frequency. Queueing can amplify or erase the change, and larger admitted batches can exchange latency for throughput. Report component and service results separately.
