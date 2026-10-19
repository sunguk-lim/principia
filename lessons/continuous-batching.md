# Continuous Batching

## Meaning

Continuous batching changes request membership between model iterations. A completed request releases its place so eligible queued work can join before every original request finishes. Each request keeps its own cache and generation state.

## Mechanism

Ordinary one-token decoding already returns control after each step. The scheduler can remove completed or cancelled requests, check work and cache budgets, and admit waiting requests. A new prompt may first require prefill; an empty nominal slot is not proof that there is enough memory or compute to admit it. Speculative decoding may advance several tokens per iteration while still allowing membership changes at safe boundaries.

A fixed-membership baseline can skip some completed-row computation yet still prevent queued requests from joining. Keep that distinction separate from whether every GPU step takes the same time. Real step duration depends on active work and context lengths.

## One example

Two slots initially serve A, needing two steps, and B, needing five. C waits and needs three. Assume equal steps, prepared prompt state and enough cache capacity. Fixed membership runs A and B until step five, then C through step eight. Continuous membership admits C at step three when A finishes, so B and C both finish at step five. Both do ten useful token steps. The difference comes from earlier admission, not different model outputs.

The trace omits prefill and scheduling overhead. Its occupancy numbers are not measured GPU utilization. Evaluate actual first-token and inter-token latency, tail latency, throughput, fairness and preemptions on the same model, hardware and traffic. Similar-length requests may leave much less waste to recover.

## Check your understanding

Does continuous batching guarantee a full batch whenever work waits? No. KV capacity, token budgets, priorities and prompt processing can prevent admission. The key invariant is correct request state, not unconditional occupancy.
