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

## Stage 4 — first reviewed lesson sequence (2026-09-13)

- Added four core lessons: softmax, online-softmax, transformer-attention,
  flash-attention. Each is 200–214 whitespace-delimited words with one objective,
  mechanism, worked example, understanding check, and public primary reference.
  Kept these shorter than the guideline because formulas add reading effort.
- Preserved full articles; corrected FlashAttention's linear-traffic/bitwise-equality
  claims and clarified that online normalization alone cannot emit all probabilities
  after discarding scores.
- Verified every lesson wikilink against allowed prerequisite/optional relations.
- Graph audit passed; manifest/legacy graph regeneration produced no tracked changes.
- All 13 Python tests passed; existing SQLite/deprecation warnings remain.
- uv generated a lockfile change during verification; inspect separately, not staged
  with editorial work. No dependencies intentionally changed.
- No deployment. Next: live Neo4j compatibility/sync verification, then browser and
  status-saving review. Four lessons are reviewed, not the entire 435-concept catalog.

## Stage 5 — live reader save verification (2026-09-14)

- Found and fixed uncaught save failures in both progress actions. A visible alert
  now reports failure, the draft stays intact, and retry remains available.
- Mark understood now saves the current note draft instead of reverting to the
  previously persisted note.
- Verified in headless installed Chrome using an isolated browser profile and
  intercepted status API: failed save, retained draft, successful completion with
  the draft note, lesson navigation, and no uncaught page errors. No real study
  status was modified. Inspected the resulting reader screenshot.
- Frontend: 9 tests, typecheck, full production build passed. Python: 13 tests
  passed; graph audit clean at 435 concepts. Existing warnings unchanged.
- Language review: no language selector exists in the current React reader;
  earlier Korean text-splitting test does not imply bilingual UI support.
- The old Java and Neo4j archives were both truncated. Java has now downloaded
  successfully and matches the publisher's SHA-256. Neo4j download is continuing;
  no database or production service changes yet. Existing uv.lock preserved.

## Stage 6 — live Neo4j and device persistence verified (2026-09-14)

- Completed and checksum-verified Neo4j Community 5.26.30 and Temurin Java
  21.0.12.1 downloads; extracted under the existing local installation directory.
  Compatibility reference: https://neo4j.com/docs/operations-manual/current/installation/requirements/
- Ran an isolated database bound to 127.0.0.1:17474, with Bolt disabled and no
  production service configuration changes. Used 512 MB maximum heap / 128 MB page cache.
- Existing transactional HTTP integration works against this release without a
  Python driver. Synced 435 concepts / 980 relationships (979 REQUIRES + 1 optional).
- Repeated sync returned identical projection metadata. Compared Neo4j prerequisite
  traversal with an independent Markdown adjacency traversal for ALL 435 concepts:
  exact parity, including each target itself. Snapshot digest:
  f90ed714b64b10159d8ddd146ed52dd927922d3ef0c010f31ba1a7a1ec15b6c8.
- Separate isolated Chrome context at 820×1180 verified device note persistence
  across reload; screenshot inspected. No user browser profile or real notes touched.
- Test-only HTTP and Neo4j processes stopped after verification. Installation and
  projection remain on disk; no always-on database service claimed.
- Remaining release scope: decide/implement production lifecycle for the optional
  projection, review upstream differences before publication, and deploy. The reader
  currently serves English articles; Korean language selection is not implemented.
  Only four core lessons are editorially reviewed. No push/deployment in this stage.

## Stage 7 — production integration prepared (2026-09-14)

- Merged latest upstream including web-text-extraction, preserving all 436 concepts.
  Regenerated the conflicted derived graph rather than choosing either old version.
- Neo4j installed in a stable per-user directory with a dedicated launchd service;
  loopback HTTP only, Bolt disabled, usage reporting disabled. Installation is
  separate from Principia and private SQLite study data.
- Added optional private ontology status/ancestry endpoints that refresh the
  projection from current source. Unconfigured/unavailable database returns 503
  without affecting graph or notes. Documented lifecycle and snapshot semantics.
- Synced 436 concepts / 982 typed relationships; repeated sync stable, all 436
  prerequisite ancestry sets exactly match independent source traversal.
- Live development API verified for status and web-text-extraction prerequisites.
- 14 Python tests, 9 frontend tests, typecheck, full build, graph audit, generated
  outputs, and diff checks passed. Chrome save/navigation checks passed against
  this build. Tablet note reload verified with the isolated test SQLite database.
- Pages trigger now includes lesson/catalog/ontology-export edits. Screenshot at
  docs/images/ontology-reader.png uses isolated synthetic study state.
- No concepts removed; graph diff removes two redundant direct prerequisite edges.
  uv.lock and original-worktree identity files remain untouched.

## Stage 8 — linear foundations remaster (2026-09-14)

- Platform PR #53 deployed; private ontology verified at 436 concepts / 982 relations.
- Added reviewed dot-product and matrix-multiplication core lessons, with defined notation, worked arithmetic and understanding checks. Full articles and graph preserved.
- Audit and data build pass; six reviewed lessons now exist. Whole-catalog editorial consolidation remains incomplete.
- Next editorial sequence: probability foundations supporting softmax; review prerequisite necessity separately from mere mentions.

## Stage 9 — global canonical identity resolution (2026-09-14)

- Added non-destructive `canonicalId` support to the ontology catalog. A duplicate
  source article is retained in Git, but its title and aliases resolve to one
  canonical learning entity; direct canonical chains are rejected.
- Resolved the first confirmed global duplicate: `bayes-theorem` now resolves to
  canonical `bayes-rule`. Both source nodes remain present in the repository and
  Neo4j; `Bayes theorem` and `Bayes' theorem` resolve to `bayes-rule`.
- The ontology now reports 436 source concepts, 435 canonical concepts, and one
  resolved entity. Neo4j contains a `RESOLVES_TO` relationship and prerequisite
  lookup through `bayes-theorem` returns the canonical Bayes roadmap.
- Full verification passed: 16 Python tests, ontology audit, Neo4j sync, 9
  frontend tests, typecheck, production build, and generated artifacts.
- This is the first verified entity-resolution result, not a claim that the
  entire catalog has been content-reviewed. Next: create deterministic global
  content fingerprints and review the resulting cross-subject candidates.

## Stage 9 — global content screening and canonical reader routing (2026-09-14)

- Added a local complete-node TF-IDF screen. It reads all 436 Markdown articles
  on disk and ranks potential identity candidates without an LLM call; results
  are review hints and never create a redirect automatically.
- The reader graph now collapses resolved aliases: source nodes remain in the
  reference projection, but alias nodes are excluded from the default learner
  graph, and alias links/roadmaps resolve to their canonical concept.
- The Bayes resolution reduces the learner graph to 435 visible concepts and
  979 learner edges while retaining 436 source records and 980 typed Neo4j
  relationships. A dedicated frontend regression test proves an alias cannot
  become a second roadmap step.
- Full verification passed: 17 Python tests, ontology audit, Neo4j sync, 10
  frontend tests, typecheck, production data build, and production UI build.
- Remaining work: editorially review the globally ranked candidates and then
  reclassify only justified prerequisite edges. No broad automatic merge is
  permitted from similarity scores.
