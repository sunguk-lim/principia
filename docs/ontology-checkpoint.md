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

## Stage 10 — complete prerequisite evidence baseline (2026-09-14)

- Added a deterministic edge-evidence pass. It reads every full node body and
  records whether each declared prerequisite is explicitly linked in the
  explanation, separately from whether its learning rationale has been reviewed.
- Baseline: all 981 prerequisite edges are linked in source bodies; none can be
  removed mechanically as a frontmatter-only artifact. 972 edges still lack a
  concise, reviewed statement of why the learning objective requires them.
- This establishes that the remaining consolidation requires editorial judgment
  of learning necessity, not a destructive text cleanup. The evidence pass is
  local and consumes no model tokens when rerun.

## Stage 11 — application edges removed from required database paths (2026-09-14)

- Reviewed the complete `pgai` and `llm-from-sql` articles. Both describe
  retrieval-augmented generation as an application assembled from their
  capabilities, rather than knowledge required to understand those concepts.
- Reclassified both direct RAG edges as `APPLIES_TO`, with explicit rationale.
  Kept the source links and full reference prose intact.
- Measured effect: pgai's required ancestor set dropped from 64 to 60 concepts;
  Calling LLMs from SQL dropped from 19 to 13. Removed detours are RAG-specific
  (`retrieval-augmented-generation`, `vector-database`, `context-window`, and
  `transformer-attention` where applicable), not deleted knowledge.
- Full validation passed: 18 Python tests, ontology audit, Neo4j sync, 10
  frontend tests, typecheck, and production builds.

## Stage 12 — prompt-caching identity resolution (2026-09-14)

- Reviewed the complete `prefix-caching`, `prompt-caching`, and `kv-cache`
  articles. `prefix-caching` and `prompt-caching` describe the same
  cross-request reuse of a shared KV prefix; `kv-cache` remains a distinct
  within-sequence mechanism.
- Kept both source articles, made `prefix-caching` canonical, and registered
  “prompt caching” as an alias. The reader and Neo4j projection resolve the
  legacy title to that one learning entity.
- The ontology now has 436 source concepts, 434 canonical learning entities,
  and two resolved entities. This does not claim a completed semantic review of
  the full catalog; remaining candidate decisions require the same full-content
  comparison.
- Full validation passed: 18 Python tests, ontology audit, Neo4j sync, 10
  frontend tests, typecheck, and production builds.

## Stage 13 — optional mechanism context and database-path correction (2026-09-14)

- Added `USES` as a directed optional relationship. It records a mechanism or
  cost model that enriches an explanation without making it a required roadmap
  step. `USES`, like the other optional relation types, never enters
  prerequisite traversal.
- Reclassified Write-Ahead Logging's block-layer I/O cost model as `USES`:
  durability and crash recovery require transactions, cached pages, and deferred
  writeback; low-level sequential-versus-scattered I/O economics remains an
  optional explanation. WAL's required ancestor set fell from 30 to 25.
- Corrected Database Index's prerequisite from `key-value-store` to the atomic
  `key-value` mapping. A durable, distributed key-value database is a distinct
  primary architecture, not background required to understand a secondary index
  entry. The distinction is retained as `CONTRASTS_WITH`; Database Index's
  required ancestor set fell from 31 to 25 and Query Planning's from 34 to 28.
- Full validation passed: 11 Python ontology tests, audit, 10 frontend tests,
  typecheck, production data build, production UI build, and whitespace check.

## Stage 14 — storage-substrate detours removed from required paths (2026-09-14)

- Reviewed the complete B-tree article. Its required learning objective is the
  high-fan-out generalization of a binary search tree; virtual-memory pages and
  OS block-layer internals explain *why the production cost model matters*, but
  are not necessary prior knowledge for that mechanism.
- Reclassified B-tree's `page` and `block-layer` dependencies as optional
  `USES` relationships with explicit reasons. The full article, examples, and
  source links remain unchanged.
- Measured effect: B-tree's required ancestry fell from 22 to 3 concepts,
  Database Index from 31 to 6, Query Planning from 34 to 9, PostgreSQL from 44
  to 38, pgvector from 56 to 50, and pgai from 60 to 54. These changes remove
  OS-internals detours rather than database foundations.
- Full validation passed: 20 Python tests, ontology audit, 10 frontend tests,
  typecheck, production data build, production UI build, and whitespace check.

## Stage 15 — globally reduced learner projection (2026-09-14)

- The static reader and Neo4j projection now use a deterministic transitive
  reduction of required-learning relationships. A direct edge is hidden only
  when another required route already entails the same concept, so every
  prerequisite closure is preserved. Markdown keeps all source links and full
  articles for reference.
- The catalog contains 976 source prerequisite links but only 704 required
  learner edges: 272 redundant direct arcs no longer inflate the graph, direct
  prerequisite lists, or relationship focus view.
- `post-training-quantization` is covered by regression tests: its source
  article still links `quantization`, while the learner sees only the direct
  foundations not already implied by another selected prerequisite.
- The audit now reports source links, learner edges, and suppressed redundancy
  separately. This reduction is structural; it does not claim the remaining
  955 unreviewed learning rationales have received editorial adjudication.
- Full validation passed: 22 Python tests, 10 frontend tests, typecheck,
  production data build, production UI build, and ontology audit.

## Stage 16 — calculus identity roadmap correction (2026-09-15)

- Reviewed the complete `curl-of-gradient-zero` article and its `curl`, `gradient`, `hessian`, `partial-derivative`, `vector-field`, and `differential-operators` dependencies. The identity's mechanism is cancellation of symmetric mixed partials by curl; the operator-family survey only places that mechanism in broader context.
- Reclassified the direct Differential Operators link as `USES`, retaining the source article link and adding an explicit rationale. Optional context remains outside required learner traversal. No identity candidate was merged: complete-content comparisons of RNN-T/TDT and the two zero identities found distinct objectives and mechanisms.
- Its required ancestor closure fell from 19 to 16, removing `differential-operators`, `divergence`, and `laplacian`. The globally reduced learner projection changed from 704 to 705 direct required edges: dropping the umbrella edge exposes the direct `curl` and `hessian` requirements that it had transitively suppressed; reachability now reflects the narrower objective.
- Full validation passed: 23 Python tests, ontology audit, 10 frontend tests, typecheck, production data build, production UI build, and whitespace check. This remains a bounded review, not a claim that catalog-wide identity or prerequisite review is complete.

## Stage 17 — catalog-wide semantic entity-resolution review (2026-09-15)

- Read every canonical source body through the authored-boundary audit and recorded a hash-pinned editorial decision for all 1,281 candidates. The completed record contains 3 `resolve` decisions (existing Softmax, Online Softmax, and Jacobian entities) and 1,278 `retain` decisions. No candidate established a distinct identity, objective, and graph placement, so no fragment entities, aliases, provenance edges, or speculative new nodes were created.
- The audit now reports completeness, and projection sync refuses an incomplete manifest. This makes stale hashes, invalid targets, duplicate decisions, and incomplete semantic review release blockers.
- Fixed the private Neo4j transaction client to bypass ambient HTTP proxies after a proxy returned 502 for the loopback-only endpoint. The endpoint validator still restricts the connection to local HTTP with no embedded credentials.
- Live Neo4j sync was run twice: both snapshots produced digest `f93c69b535489e68f1addb3e6c2357dbd23f424109480643784f5bbffdaea170`, 434 canonical entities, and 974 typed closed-set relations (972 `REQUIRES`, 2 `CONTRASTS_WITH`). All 434 Cypher `REQUIRES` closures exactly matched independent source traversal; the reader projection contains 434 nodes and 972 required edges.
- Python tests, semantic audit, static ontology validation (aliases, cycles, missing prerequisites, and closed relation vocabulary), frontend tests/typecheck/build, and whitespace checks passed. Existing `principia audit` body-link warnings are legacy optional-context links and Korean mirrors; this review adds none.

## Stage 18 — numeric-performance foundation rationale review (2026-09-15)

- Reviewed the complete `quantization`, `arithmetic-intensity`, and `memory-hierarchy` articles and their six direct foundation edges. Added objective-specific learning rationales for arithmetic, numeric precision formats, and arithmetic intensity; all three concepts require the stated foundations to calculate or interpret their central mechanisms.
- Source Markdown, source links, canonical identities, and typed relations are unchanged. No optional context was admitted to prerequisite traversal and no edge was removed: each reviewed relationship is necessary to the article's stated learning objective.
- Measured effect: reviewed prerequisite rationales rise from 21 to 27; unreviewed edges fall from 954 to 948. The learner projection remains 434 canonical concepts and 972 required edges, with identical reachability.

## Stage 19 — restored contextual prerequisite classification (2026-09-15)

- Rechecked the complete B-tree, WAL, pgai, Calling LLMs from SQL, and Curl of a Gradient is Zero articles against their stated objectives. Their previously reviewed storage-cost, RAG-application, and operator-family references are explanatory context, not required learner foundations.
- Restored those source links and represented the six contextual relationships as closed-vocabulary `USES` or `APPLIES_TO` edges. The projection and TypeScript schema carry both types, while roadmap traversal continues to follow only `REQUIRES`; regression coverage now asserts that `USES` never becomes a required path step.
- Measured against the current checkpoint: required source links fell 979 → 975 and learner `REQUIRES` edges 976 → 972; optional typed context rose 2 → 8. Required ancestor closures fell pgai 63 → 54, WAL 30 → 25, and B-tree 22 → 3. The canonical learner set remains 434 entities; no identity resolution changed.
- Validation passed: 30 Python tests, ontology audit (zero errors, zero unreviewed prerequisite rationales), 10 frontend tests, typecheck, production data/UI build, and whitespace check. This corrects a bounded regression; it is not a new claim of whole-catalog prerequisite adjudication.
