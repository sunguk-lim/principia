# Version-Controlled Agent Memory

## Meaning

Version-controlled memory makes a durable fact store behave as a sequence of inspectable revisions rather than a mutable record with only its latest value. Each worker can propose changes in an isolated branch, and a publication step decides whether those changes become shared memory. This is an architecture, not merely a version field on one row.

## Mechanism

Bind a workspace to a base revision and stable fact identities. Let a worker accumulate a change set, including additions, superseded decisions and relation updates. A [[three-way-merge]] compares its base, proposal and current published revision. Validate schema, permissions and semantic invariants before committing the accepted result as one [[transaction]]. A branch does not itself guarantee atomic publication or prevent external side effects.

[[agent-memory]] should retain provenance and scope. [[authenticated-change-provenance]] records parents, authenticated author, source references, validation and reviewer decision. A [[snapshot-read-consistency]] contract chooses one immutable revision, so related facts are not assembled from incompatible points in time. Historical read access still needs authorization; retention of old private facts is a deliberate policy, not a free debugging feature.

## One example

At revision R4, component C uses Redis and has no owner. Worker A branches to change the store and supersede an old decision. Worker B branches to assign an owner. Publish A as R5 only if the component and decision remain consistent. Then compare B with R4 and R5, preserve A's store change, and validate the owner assignment before creating R6. A read pinned to R4 still returns the old facts and must label them historical, not current.

## Boundaries and check

Test multi-record invariants, stale bases, branch permissions, crash-before-publication and retention. Review storage growth, merge contention and proposal lifetime. Conventional databases can also supply multi-row transactions and history; a Git-inspired interface does not prove better throughput or serializability. A clean branch merge is not a substitute for validating the resulting knowledge.


## Check your understanding

Does an isolated branch guarantee valid publication? No; validate base changes, invariants, authority and the atomic publication boundary.
