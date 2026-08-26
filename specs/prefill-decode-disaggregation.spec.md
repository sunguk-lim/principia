# Figure spec — `prefill-decode-disaggregation`

> Derived from `nodes/prefill-decode-disaggregation.md`; governed by
> `protocols/EXPLAIN.md` and `protocols/VISUAL_PROTOCOLS.md`.

## Visual teaching contract

- **Audience:** An engineer who understands LLM prefill, decode, and KV caching but has not seen a
  disaggregated serving topology.
- **Single job:** Make the reader see that the phases become independent worker pools only by handing
  the request's KV state across a new transport boundary.
- **Visual thesis:** Because a large prefill disrupts small decode steps when both share one worker,
  disaggregation moves them into phase-specific pools and transfers the completed KV cache between
  them, so first-token and inter-token service can be controlled independently.
- **Traced object:** One request: blue prompt tokens become one amber KV-cache slab, which crosses to
  the teal decode pool and continues as output tokens.
- **Subject visual vocabulary:** token strips, GPU workers, scheduler queue, KV-cache grid, worker
  pools, transfer link, streamed output tokens.
- **Signature moment:** The amber KV grid rides the only inter-pool arrow; it is visibly the state that
  makes continuation on another worker possible.
- **Anti-template test:** Removing the prompt/decode workload shapes or replacing the KV grid with a
  generic message destroys the explanation; this is not a relabeled two-stage pipeline.

| channel | semantic job |
|---|---|
| Form | long strip = token-heavy prefill; small repeated cells = decode steps; grid = KV state |
| Space | shared enclosure = interference; separate enclosures = independent pools; arrow = handoff |
| Scale | the co-located bottleneck and two phase pools dominate; annotations remain subordinate |
| Colour | blue = prefill, teal = decode, amber = transferred request state |
| Rhythm | one long prefill block contrasts with several short decode steps |

| disclosure | figure treatment |
|---|---|
| Intuition | one mixed worker becomes two specialized pools |
| Mechanism | prompt creates KV state; KV state crosses; decode resumes and emits tokens |
| Precision | labels identify compute-heavy prefill, memory-heavy decode, TTFT, and ITL |

**Comprehension test — intended answers:**

1. **Problem:** A large prefill delays small decode steps when they share one worker.
2. **Change:** Prefill and decode run in separate worker pools.
3. **Cause:** The completed KV cache is transferred at the phase boundary.
4. **Usefulness:** The pools can be scheduled and scaled independently for TTFT and ITL.

**First-view constraints:** The square 720×720 canvas uses no label below 18 px and scales without a
wide horizontal overflow on a phone. The exact cache-size calculation and network trade-off stay in
the node prose.

**Plan critique:** A generic client → prefill → decode pipeline was rejected because it would show
sequence but not the co-location problem or the state that licenses migration. The final storyboard
contrasts the shared enclosure with separated pools and gives the KV cache the only accent.

**Reduced-motion result:** The figure is static; its fallback is the complete before/after mechanism.

## Figure trigger and spine

Drawing is warranted.

- **SHAPE/structure:** one mixed worker enclosure changes into two separately provisioned pools.
- **FLOW/routing:** prompt tokens enter prefill, the KV cache crosses the handoff link, and output
  tokens leave decode.
- **CHANGE over steps:** the before/after storyboard shows coupled scheduling becoming independent
  phase service.

Genre: **comparison with a dataflow overlay**. The upper and lower states share the same request
identity but expose different serving topology.

## Entity inventory

| entity | drawn as | role |
|---|---|---|
| Mixed worker | neutral containing region | co-located baseline and interference boundary |
| Long prefill | long blue token strip | token-heavy compute burst occupying the shared worker |
| Queued decodes | repeated small teal cells | next-token work delayed behind the burst |
| Prefill pool | blue region with prompt strip and compute tiles | produces the first-token state |
| KV cache | amber mini-grid | persistent per-request state and traced handoff object |
| Decode pool | teal region with cache slot and token cells | resumes token generation |
| Transfer | persistent labeled arrow | new cost/boundary introduced by disaggregation |

## Rendered critique

The 720×720 render remains legible at laptop and phone fit-to-width sizes. The KV grid sits directly on
the attached inter-pool arrow, the prefill strip is visually distinct from the repeated decode cells,
and no text or entity overlaps. **Subtraction pass:** a clipped inbound prompt arrow was removed because
its source was outside the canvas and the labeled prompt strip already identifies the input. A separate
legend was also omitted because every shape is labeled inline.
