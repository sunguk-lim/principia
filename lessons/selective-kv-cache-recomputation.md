# Selective KV-Cache Recomputation

## Meaning

Selective KV-cache recomputation reuses independently prepared context blocks while recomputing some token states under their new surrounding context. Its objective is to recover useful cross-chunk interaction without paying full prefill. It is not ordinary [[prefix-caching]]: an identical chunk appearing after a different earlier chunk does not in general produce identical deeper-layer attention state.

## Mechanism

In [[transformer-attention]], a token can incorporate preceding tokens. If chunks A and B were cached separately, B's cached higher-layer states did not incorporate A. Simply moving or concatenating those states cannot establish the omitted interaction. Adjusting positions is necessary for some representations but does not supply the missing contextual computation.

CacheBlend processes layers while updating a selected subset of token states. Selected queries attend to the assembled context; refreshed keys and values replace their stale counterparts, while other positions reuse stored state. The paper investigates selection using state deviations and propagates a bounded recomputation set through the layerwise procedure. The selection fraction is a quality/cost parameter, not an exactness theorem. A [[tiered-kv-cache]] can fetch upcoming layers while computation updates the current layer, but overlap helps only if the measured critical path shrinks.

## Worked example

Use a hypothetical prompt with two 100-token chunks. B defines “the winner” by referring to a name stated in A. Independently cached B cannot have incorporated that name. Full prefill computes all 200 token states per layer; a toy selective policy refreshes 20 and reuses 180. That is 10% of positions refreshed, not a tenfold speedup: selected attention still reads context, fetching and selection take time, and 20 poorly chosen positions can miss the dependency. Evaluate answers to both a within-chunk question and the cross-chunk question.

## Check your understanding

Why is non-prefix reuse not justified by the exact-prefix invariant? Earlier context differs. Reusing a chunk's bytes does not recreate its missing earlier-context interactions; selective recomputation is an approximation whose quality must be checked.
