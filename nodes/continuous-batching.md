---
id: continuous-batching
title: Continuous Batching
summary: Continuous batching changes active request membership between model iterations while preserving independent per-request state.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache, queue]
sources: [https://www.usenix.org/conference/osdi22/presentation/yu, https://arxiv.org/abs/2309.06180]
status: explained
created: 2026-06-23
updated: 2026-10-20
---

# Continuous Batching

## Summary

Continuous batching changes which requests run together between model iterations instead of fixing batch membership until every original request finishes. It converts newly available capacity into progress for queued requests while preserving each request’s own state.

![Continuous batching replaces finished requests between decode steps so queued work fills newly available batch slots.](continuous-batching.svg)

## Grounded explanation

### Mechanism and invariant

In ordinary one-token autoregressive decoding, each active request advances one token per iteration. A request’s [[kv-cache]] records its own prefix; another request can have a different prefix length without reading that state. A scheduler regains control at an iteration boundary, removes completed or cancelled requests and admits eligible waiting work from a [[queue]]. The invariant is correct independent request state, not an unconditional promise that every nominal slot is always full. Prompt processing, token budgets, cache capacity, priorities and service limits can block admission even when demand exists. Speculative or multi-token decoding can advance several tokens per iteration without invalidating membership scheduling.

A fixed-membership baseline leaves completed requests’ reserved positions unavailable until the group drains. Implementations may skip some dead-row arithmetic; they need not literally pay the same full compute at every step. The useful distinction is whether queued requests can join ongoing work. Sharing weight reads among live requests can improve throughput, but step duration changes with batch size, sequence length, kernels, memory traffic and prefill interference. It is not automatically equal to a single-request step.

### Worked trace with explicit assumptions

Use a toy decoder with two request slots and equal-duration steps. At the start, A needs two steps, B needs five, and C waits in the queue needing three. Assume prompt state is already prepared, cache capacity is sufficient and admission overhead is omitted so the example isolates membership.

| Step | Fixed-membership active work | Continuous active work |
|---|---|---|
| 1 | A, B | A, B |
| 2 | A finishes, B | A finishes, B |
| 3 | B | C, B |
| 4 | B | C, B |
| 5 | B finishes | C finishes, B finishes |
| 6 | C | — |
| 7 | C | — |
| 8 | C finishes | — |

Both policies produce ten useful token steps: A contributes two, B five and C three. Fixed membership uses 2×8=16 available slot-steps, so useful occupancy is 10/16=62.5%. Continuous membership uses 2×5=10, yielding 100% in this deliberately simplified trace. Completion moves from step eight to step five because C starts after A releases its place. These are illustrative accounting values, not measured GPU utilization or a universal speedup. Real admission may first require prefill, which consumes additional work and can extend ongoing decode steps.

### Boundaries and validation

When requests end together, there may be little finished-slot waste to recover. Length variability, arrival timing, prompt work, memory limits and the baseline determine the gain; variance alone does not determine a throughput multiplier. A batch can also grow until compute, cache capacity or tail latency becomes limiting.

Compare policies using the same model, checkpoint, precision, sampling, traffic trace and hardware. Report time to first token, inter-token and end-to-end tail latency, throughput, fairness, cache occupancy, preemptions and task quality. Include uniform and mixed output lengths, prompt bursts, cancellations and memory pressure. Continuous admission and paged cache allocation solve different problems: request scheduling decides who runs, while cache layout determines where state fits. Orca grounds iteration-level scheduling; the PagedAttention paper describes the complementary allocation mechanism.

## Prerequisites

- [[kv-cache]]
- [[queue]]

## Sources

- <https://www.usenix.org/conference/osdi22/presentation/yu>
- <https://arxiv.org/abs/2309.06180>
