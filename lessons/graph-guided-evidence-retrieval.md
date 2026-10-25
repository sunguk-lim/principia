# Graph-Guided Evidence Retrieval

## Meaning

Graph-guided evidence retrieval selects answer evidence by following typed relationships among identified entities. It helps when a bridge fact does not resemble the original question, but a connected path is still only as sound as its source records.

## Mechanism

Index entities and relation claims with stable identities, source text units and revisions. At query time, find a starting entity, choose relevant relation types, expand within a bound, and recover the supporting passages. Rank and filter this context before generation. Similarity search may locate starting entities; graph-guided retrieval need not replace it. A knowledge graph is the representation, while this concept owns the evidence-selection pipeline built on it.

The crucial invariant is that every relationship used in an answer has accessible, current support. Authorization must cover bridge evidence as well as the entities the user named. Do not expose restricted relation counts or infer hidden facts merely because the endpoints are public. A hop limit bounds work, not permission.

## One example

Three fictional documents say V supplies C, P contains C, and P has a pending audit. To answer which vendors contribute components to pending-audit products, begin at P, move to C, then recover V. Cite all three documents: the answer depends on the bridge, not just the first and last records. If the P-to-C document is deleted, stale or restricted, that particular supported answer disappears. If the supplier record is uncertain, preserve that uncertainty.

## Check your understanding

**Question:** Why not stop once a two-hop path is found? **Answer:** Connectivity does not certify entity identity, relation truth, freshness or authorization. Recover and check the supporting evidence. Compare bridge recall and answer support with a simpler retrieval baseline; extra graph indexing cost is justified only by measured benefits.
