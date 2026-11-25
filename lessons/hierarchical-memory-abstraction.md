# Hierarchical Memory Abstraction

## Meaning

A memory hierarchy organizes observations and inferences at several levels of abstraction. Higher records summarize relationships among lower records, not merely shorter versions of their words. [[reflective-memory-consolidation]] explains how one inference is produced; the hierarchy explains how several such inferences compose without losing the route back to observations.

## Mechanism

Treat base observations as leaves. A first-level reflection points to the observations used to infer it. A later reflection can point to earlier reflections, producing a [[directed-acyclic-graph]] of support, with a tree as the no-sharing special case. Retrieval may select a high-level record for a broad question and descend to its support for a detailed or contested question. The Generative Agents paper explicitly describes reflections over reflections and a reflection tree.

Abstraction reduces how much evidence must fit in the live context, but each inference can discard conditions. The reader must be able to distinguish “observed twice” from “inferred once, then summarized twice.” Shared support is not independent confirmation. Record scope and derivation, detect circular support, and revisit leaves when a high-impact conclusion depends on an uncertain intermediate claim. Those are application safeguards, not guarantees supplied by the paper's language model.

## One example

In a hypothetical equipment log, observations A and B show pump P failing under high inlet temperature. Reflection R says P is temperature-sensitive under those tested conditions. Another pump has a separately supported reflection S. A higher inference T proposes that cooling capacity deserves investigation across both pumps. T must not silently become “all pumps fail when warm”: only two devices and specific conditions were observed.

If A is later found to have an incorrect sensor value, R and T need review; S may remain supported. Retaining only T would hide which conclusions were affected. A shared leaf cited by two reflections still counts as one observation.

## Check your understanding

Can two higher-level memories corroborate each other when both rely entirely on one event? No. Their apparent agreement adds no independent evidence.
