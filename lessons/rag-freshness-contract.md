# RAG Freshness Contract

## Meaning

A retrieval-augmented system has at least two freshness obligations: make newly eligible information discoverable and stop using information that is no longer eligible. Those obligations can progress at different rates. A **RAG freshness contract** states which source revisions and permissions may be used at each boundary and what happens while components disagree.

## Mechanism

Record an observed source revision, a completely published searchable generation and the current evidence-eligibility state. [[background-document-indexing]] explains why accepting an update is not the same as publishing its searchable representation. [[retrieval-authorization-boundary]] decides what a caller may receive even if the old vectors still exist. [[ml-system-freshness]] supplies measurement of the complete path rather than only endpoint latency.

Measure source-change-to-discovery separately from revocation-to-denial. A system can deny access immediately yet take time to index a replacement; secure exclusion does not imply current recall. Conversely, fast indexing does not prove old cached answers were invalidated. Declare whether readers may use an explicitly labeled old generation, require an at-least revision, wait for catch-up or fail closed when eligibility cannot be established.

## One example

For a hypothetical policy document, revision 4 is searchable. At 10:00, revision 5 changes its text. At 10:01, the connector observes it; at 10:04, the replacement becomes searchable. Discovery lag is four minutes from the source change, not one minute from the poll. At 10:02, a reader's permission is revoked. If an authoritative read-path check denies that reader at 10:02, revocation need not wait for the 10:04 content rebuild. Other permitted readers may still receive an identified old revision if the contract allows it.

A multi-document answer raises another boundary: individually current-looking passages need not represent one coherent cross-document snapshot. State the consistency scope rather than promising atomicity across independent services.

## Check your understanding

Does a successful recent poll prove a fresh answer? No. Trace the relevant source revision through publication, eligibility and reuse.
