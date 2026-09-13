# Ontology implementation checkpoint

## Stage 1 — draft validated (2026-09-13)

Branch: `feat/learning-ontology`; worktree: `principia-ontology`.
This is an implementation checkpoint, not a deployed release.

- Saved existing alias/identity, typed-relation, cycle-detection, lesson-view,
  and Neo4j projection drafts.
- Added five regression tests: alias resolution, identity disambiguation,
  optional relations excluded from prerequisites, cycles, missing prerequisites.
- Corrected audit output to describe the new relationship rule.
- Graph audit: 435 canonical concepts, no ontology errors.
- Python suite: 13 tests passed using `uv run --group dev python -m unittest discover -s tests -v`.
- Frontend: typecheck, 3 existing math tests, production build passed.
- Manifest and legacy graph regenerated. UI output is build-generated/ignored.
- Existing test warnings: deprecated Starlette/httpx integration and unclosed SQLite connections.
- No service configuration changed; no deployment or Neo4j live sync performed.

## Next stages, in order

1. Add focused roadmap and lesson-splitting tests; review UI handling of errors,
   completion state, equations/code blocks and language selection.
2. Reconcile authoring docs/protocols with typed relations. Review remaining
   commands that still assume every body link is a direct prerequisite.
3. Write and review the small attention lesson sequence. Currently **zero**
   reviewed lessons exist; 232 source articles exceed 500 words. Do not claim
   whole-catalog editorial completion. Preserve full source articles.
4. Verify Neo4j Community deployment/version/API compatibility and local-only
   configuration, then test projection sync and prerequisite parity. Current
   `neo4j.py` is an unverified integration draft, not an operational database.
5. Inspect UI, run final checks, then publish/deploy within authorized scope.

Keep stages bounded, commit each verified checkpoint, and update this document
with exact evidence and next action before any quota interruption. Do not
restart the completed Letters historical backfill or alter its ledger.
