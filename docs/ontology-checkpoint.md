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

1. Focused roadmap and lesson-splitting tests completed (Stage 2 below).
   Browser interaction verification, save-error handling, and actual language
   selection remain to be checked before release.
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

## Stage 2 — reading and roadmap regression checkpoint (2026-09-13)

- Six new frontend cases cover shared prerequisite deduplication, optional
  relationship exclusion, learned-ancestry pruning, completed goals, cycles,
  missing dependencies, intact Markdown blocks, literal math delimiters in
  code, empty input, and Korean text (some cases cover multiple conditions).
- Reproduced and fixed code-block `$$` incorrectly opening a math block and
  swallowing subsequent lesson headings.
- Roadmap errors no longer display the false claim that a goal is completed.
- `npm test`: 9/9 pass. `npm run typecheck` and `npm run build:ui` pass.
- Korean text preservation is tested; a language selector is NOT verified.
- No live browser test, deployment, Neo4j setup, or source article edits.
- Next: reconcile typed-relation authoring rules, then reviewed short lessons;
  retain browser/save-state review as a release gate. Stage 1 Python/audit
  results remain applicable: no Python or ontology data changed in this stage.

## Stage 3 — authoring contract reconciled (2026-09-13)

- Updated repository guidance, node model, and explanation protocol to distinguish
  prerequisite closure from optional typed relationships; added identity admission
  and short-lesson authoring instructions.
- Documented verified legacy limitations: merge ignores catalog/lessons, reindex
  strips removed links, and reground lexical matches require editorial judgment.
- Corrected the audit docstring; no runtime behavior or node data changed.
- Full graph audit and git diff --check passed.
- Next: write/review the four attention-sequence lessons, then verify lesson links
  and Neo4j integration. Whole-catalog editorial review remains incomplete.
