# Infini Attention Compressive Memory

## Meaning

Infini-attention combines exact local attention with a bounded summary of earlier segments. Bounded size is a memory property, not a promise of lossless infinite context.

## Mechanism

Each segment updates a fixed-size associative state; the current segment can read that state while also attending locally. Distant details compete for finite representation capacity.

## Example

After many segments, a common theme may remain accessible while a rare exact number is lost. An external retrieval index would make a different accuracy–memory trade-off.

## Boundaries and trade-offs

A bounded associative state is a lossy summary of arbitrarily many earlier segments. Local attention preserves high-resolution nearby detail while the compressed path provides a possible signal from far away. As more evidence accumulates, two facts can interfere in the same finite state. This is a different trade-off from storing all old keys for nearest-neighbor retrieval: the former fixes memory, the latter spends storage and lookup time.

## Validation

Build tests that plant exact facts, recurring themes, and later contradictions at known distances. Compare the same model without the compressive path, a recurrent segment model, and an external-retrieval baseline. Measure exact recall, answer quality, memory, and throughput while growing input length. Pay attention to overwriting: if a later correction is lost but an earlier value survives, the model may answer confidently with stale information. “Infinite context” describes bounded execution memory, not unlimited factual fidelity.

## Understanding check

Which distance-sliced test would reveal compression interference, and what should be measured besides maximum accepted input length?
