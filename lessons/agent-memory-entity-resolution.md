# Entity Resolution in Agent Memory

## Meaning

Entity resolution decides whether a newly observed mention refers to an existing real-world entity. An [[agent-memory]] system needs this before attaching new facts: merging two different people combines their histories, while keeping two names for one person fragments retrieval. Stable [[knowledge-graph]] identity is the output; matching text labels is only one source of evidence.

## Mechanism

Separate candidate retrieval from identity judgment. Retrieve plausible existing entities by names, aliases and descriptive similarity. An [[embedding]]-based [[cosine-similarity]] search can improve candidate recall, but a large score is not a proof of identity. Compare type, identifiers, organization, relationships, episode context and contradictory attributes before choosing a match.

Graphiti's paper describes embedding and full-text candidate retrieval followed by contextual resolution. That is one implementation, not a guarantee against false merges. Keep mention provenance and the resolution version so a mistaken merge can be inspected and corrected. When evidence is ambiguous, preserve distinct candidates or abstain instead of silently forcing a match. Resolving the identity of a person is separate from deciding which claims about that person are current or true.

## Worked example

Three episodes mention “Mina Park at North Lab,” “M. Park, North Lab, author ID 42,” and “Mina Park at South Clinic, author ID 91.” Shared name tokens make all three plausible lexical candidates. Matching identifier 42 and compatible context can support linking the first two if additional evidence actually establishes that ID for the first mention. Different organizations alone do not prove different people: one person can change jobs. Conflicting stable identifiers and simultaneous incompatible context support keeping the third distinct. If the first mention has no confirming evidence, leave its link uncertain rather than infer identifier 42 from name similarity.

## Check your understanding

Does a nearest-neighbor result establish that two names are the same entity? No. It proposes a candidate; identifiers and episode context must support the identity decision, and uncertainty may require abstention.
