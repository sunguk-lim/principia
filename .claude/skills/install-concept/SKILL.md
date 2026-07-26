---
name: install-concept
description: >
  MANDATORY entry point for installing, explaining, or ingesting ANY concept or paper
  into the learning brain (brain.py). Invoke whenever the user asks to add, install,
  explain, or ingest a concept/paper, to explain stubs, or to build an install queue
  from a source. Routes to the closed-world install -> explain -> audit -> manifest ->
  graph -> commit -> PR loop.
---

# Install / explain a concept — the install workflow

This skill is **the workflow**: *how* an install runs, step by step — the lifecycle, the action
table, and the ordered checklist. Two things it does **not** restate (single source of truth):

- **Authoring rules** — closed-world law, the Depth rule, the `sync`/`lock` discipline, the
  `explain()` decomposition — are canonical in **`brain/protocols/EXPLAIN.md`**.
- **Reference** — commands, node schema, taxonomy — is in **`brain/README.md`**.

> **brain.py is the engine; the LLM is the author.** `brain.py` records / validates / indexes /
> renders — it never reasons; **you** supply every argument (`id`, `--title`, `--requires`,
> `--tags`) and the entire node body. The full model is `README.md` → *The two layers*. The `audit`
> gate is the one correctness check that does **not** depend on your judgment, so it is non-negotiable.

## When to invoke

The user asks, in any phrasing, to: *install / add / explain* a concept; *ingest* a paper or a
source file; *explain the stubs*; or *build an install queue* from an artifact. Natural-language
intent is enough — no exact command required.

## The lifecycle — the shape of the workflow

The brain is an **agentic graph database**: entities are **nodes** (concepts) + **edges**
(prerequisites), and its actions are **CRUD tool-calls** — the LLM agent decides
(`prompt → tool-call`) and the `brain.py` CLI executes (`tool-call → CRUD on the graph`). Each action
below is tagged **C**reate · **R**ead · **U**pdate · **D**elete, sits in one layer (*who* runs it), and
either reshapes **structure** (node/edge topology) or only fills **content** (a node's prose) — never
both at once.

> **It starts with a prompt.** The graph has exactly **one entry point — a plain-language request
> prompt** (*"what is LoRA?"*). You never hand-write frontmatter, draw an edge, or call `reindex`
> directly; you *ask*, and the agent (`prompt → tool-call`) + `brain.py` (`tool-call → CRUD`) turn that
> single request into grounded nodes and edges. Everything below is downstream of that one ask.

| Action | Layer · touches | What it does | Status |
|---|---|---|---|
| **compose** | LLM · *decides structure* (no write) | recurse `get_children` + `already_have` → the **add-queue**: every node **and** its edges, **nothing created yet** | skill |
| **scaffold** (`add` / `remove`) | LLM decides → CLI records · *structure* | **C / D** · create/delete the **queued** nodes with their declared edges (`--requires` from compose) | live |
| **sync** | LLM · *content* | **U** (returns ∅) · fill each stub's prose (closed-world) **+ its full Korean companion body `nodes/<id>.ko.md`** (format: `EXPLAIN.md` → *The Korean companion*) — the **only pass that unfolds a body**, so it also writes that body's **folded metadata**: a one-line **`summary:`** (the folded view) and **typed `review:` feedback** (`missing-prereq=<id>`, `unused-prereq=<id>`, `overlaps=<id>`, `mislink=<id>`, `regrounding=self`) for `lock`. **Never reshapes** the graph. | skill \* |
| **lock** | LLM · *structure* | **R → U/D** · **FOLDED** — reads only metadata (the `review:` feedback **+** the skeleton **+** node `summary`s), **never a body**. *Progressive disclosure:* title → summary → rare body peek. **Re-indexes** each node from feedback **+** `reground` (missing edges) **+** `reground --prune` (wrong / homonym edges) **+** a skeleton/summary dedup: declare its correct prereq set via one **`reindex`** (**adds + prunes** in one diff), plus **scaffold** a missing node, **merge** a duplicate, or **demote** a stranded axiom (changed nodes re-enter `sync`, so the lifecycle **loops until settled**); reviewable diff, `audit`-gated | skill \* |
| **audit** | `brain.py` · *validate* | **R** · closed-world + body-links ⊆ prereqs + tags + YAML — the commit gate | live |
| **feedback** | `brain.py` · *list* | **R** · list pending `review:` notes — the deterministic worklist `lock` consumes (like the frontier) | live |
| **review / dupes / reground / reindex / merge** | `brain.py` · *the lock executors* | the deterministic primitives the `lock` skill drives: `review` records `sync`'s notes (**U**) · `dupes` screens redundancy (**R**) · `reground` screens missing edges & `reground --prune` suspect/wrong ones (**R**) · **`reindex`** sets a node's prereq set, diffing **add + remove** (**U**, internally **C**/**D**) — the single declarative edge interface · `merge` folds one node into another (**D**) | live |
| **manifest** | `brain.py` · *derive* | **R** · regenerate `MANIFEST.md` (the catalog) | live |
| **graph** | `brain.py` · *render* | **R** · regenerate `web/graph.html` | live |

\* `sync` and `lock` are **LLM passes**, implemented as **explicit skills** (`install-concept` =
compose + scaffold + `sync`; `lock` = settle) that drive the deterministic primitives — *named procedures*,
not single `brain.py` commands. The judgment stays with the LLM; everything mechanical is a `brain.py`
call. *(A legacy deterministic `brain.py sync` — a closed-world check — still exists but is subsumed
by `audit`.)*

**The flow.** That entry prompt is a **concept** (*"what is LoRA?"*), an **academic paper**
(*"explain FlashAttention-3"*), or a **framework / webpage to ingest** — all funnel into one flow: compose the sub-graph, then scaffold it:

```
 prompt  ("what is X?")
   │
   ▼
 compose   [LLM]  — decide the whole sub-graph, BEFORE any `add`
   recurse get_children + already_have → every node + its --requires;
   nothing created yet
   │
   ▼  then, per queued node (order doesn't matter):
 scaffold ──► sync
 [add·CLI]    [LLM]   create node (--requires=children) · fill prose + ko companion, summary, review
   │
   ▼  once the whole queue has landed:
 audit ──────► manifest ──────► graph ──────► diff ──────► commit
 [brain.py]    [brain.py]       [brain.py]    [brain.py]   [git]
  closed-world  regen           render        Δ review     versioned,
  gate          MANIFEST.md     graph.html    (PR gate)    shared

 reground / lock = the RARE settle-loop safety-net — the queue was
 pre-grounded at compose, so it seldom fires (rules: EXPLAIN → the two passes)
```

Actors: **`[LLM]`** = judgment (decides/authors) · **`[brain.py]`** = deterministic engine
(records/validates/derives) · **`[git]`** = distribution. The settle pass is its own skill
(**`lock`**); the authoring *rules* every step obeys live in `protocols/EXPLAIN.md`.

## Compose the add-queue (do this BEFORE scaffolding)

An install is a **sub-graph**, not one node: `add C` pulls in C's prerequisites recursively. So
**compose the whole queue first — deciding every node AND its edges — then `add` one-by-one.** Once
the queue is right, addition needs no further judgment.

```python
def compose_add_queue(root):
    add_queue, work = [], [root]
    while work:
        cur = work.pop(0)
        if already_have(cur, graph, add_queue):   # [LLM] already covered? -> reuse, skip
            continue                              # don't add, don't recurse
        add_queue.append(cur)                     # worth adding
        cur.children = get_children(cur)          # [LLM] its direct prerequisites (none -> a floor)
        work += cur.children
    return add_queue

for node in compose_add_queue(concept):           # then, mechanically:
    add(node)                                     #   brain.py add <id> --requires <node.children>
```

Edges (`--requires`) are decided **once**, at compose time, and merely *recorded* at `add` — no
re-deciding children during addition. Order doesn't matter: `add` tolerates not-yet-created prereqs
(they sit in `missing` until their turn), and `audit` is the final gate after the whole queue lands.

**The two `[LLM]` steps are the judgment core — NOT string comparison:**
- **`already_have` — semantic identity.** A concept may already exist under a *different name*
  (synonym), the *same name* may denote a *different* concept (homonym — disambiguate by the node's
  `summary`; see `EXPLAIN.md` dedup), or an existing node may *subsume* it. Narrow candidates with
  `dupes` / `list`, then decide on **meaning** (titles + summaries) — never on id equality.
- **`get_children` — semantic decomposition.** The concept's genuine *load-bearing* prerequisites
  (Depth rule: load-bearing → node, incidental → prose), at the right **granularity**, derived
  **graph-blind** — do not shrink the decomposition to whatever already exists (the
  convenience-grounding trap). The hardest call in the system; rules in `EXPLAIN.md` → *Depth* and
  *Decomposition*.

The loop below is the mechanical realization: steps 1–2 create the queued nodes; their `--requires`
come from each node's already-decided `children`.

## The loop (each step is a `Bash` call to `brain.py`)

0. **Branch first (the default landing flow).** Concept installs land via **branch → PR → merge to
   `main`** — `main` auto-deploys GitHub Pages, so a half-finished, audit-failing state must never sit
   on it. Start on a fresh branch: `git checkout main && git pull && git checkout -b concept/<id>` (the
   **`concept/`** hierarchy; `<id>` = the primary node being installed).
1. **Compose the add-queue — no `add` yet.** Run the *Compose the add-queue* procedure above:
   recurse `get_children` / `already_have` (screen reuse with `dupes` / `list --tag`, decide by
   `summary`) until the queue holds every node to create, each carrying its `children` (= its
   `--requires`). Structure is decided here, once. (Rules: `EXPLAIN.md` → *Depth* + *Decomposition*.)
2. **Scaffold the queue — add one by one.** For each queued node:
   `uv run python brain.py add <id> --title "…" --requires <node.children> --tags <path>`
   (`--type paper --authors … --year …` for a paper; `--type axiom` for a floor — empty `children`).
   Then `uv run python brain.py missing` is a **sanity check** — it should come back **empty**, since
   the queue was composed closed. A non-empty result means *compose missed something*, not a cue to
   patch reactively.
3. **Author each body (`sync`)** per `protocols/EXPLAIN.md` (closed-world, Depth, and the folded
   `summary:`+`review:` the pass must leave), **and its Korean companion `nodes/<id>.ko.md`**
   (format: `EXPLAIN.md` → *The Korean companion*). Record any structural issue you hit while reading the
   prose — **never reshape the graph while filling**:
   `uv run python brain.py review <id> --add missing-prereq=… | overlaps=… | unused-prereq=… | mislink=… | regrounding=self`.
4. **Ground-check (`reground`) — now the rare safety-net** (compose already reused existing nodes via
   `already_have`, so this is usually empty), **run before audit so each node leaves `add` fully
   grounded:** for each node you authored, run `uv run python brain.py reground <id>`. Each candidate it surfaces is an **existing
   node your prose leans on but didn't declare** → judge it by its `summary`, fold the real ones into the
   node's **complete correct prereq set**, and **`reindex`** to that set:
   `uv run python brain.py reindex <id> <all its prereqs…>` (it diffs — adds new edges, removes wrong
   ones); then wire each new `[[link]]` into the body. Repeat until `reground <id>` comes back empty.
   **This does NOT replace child-spawning** — it *complements* it: a load-bearing concept that is **not
   yet a node** is still **scaffolded now** via steps 1–2, and a spawned child re-enters this same loop.
   `reground` only catches the *other* miss: leaning on a concept that **already exists** without
   declaring it. (Rule: `EXPLAIN.md` → *Depth*.)
5. **Gate:** `uv run python brain.py audit` — MUST exit clean before committing.
6. **Manifest:** `uv run python brain.py manifest` (regenerate the catalog `MANIFEST.md`).
7. **Dashboard:** `uv run python brain.py graph` (regenerate `web/graph.html`) when the visual
   should stay current.
8. **Review the delta — text AND visual, BEFORE the PR:** `uv run python brain.py diff <base>`
   (e.g. `diff HEAD~1`, or `diff main` from a branch) — confirm the change adds/removes exactly the
   intended nodes/edges, and inspect the **`restructured`** block for any interleave/prune. Then render
   the same delta visually: `uv run python brain.py graph --diff <base> --out web/graph-diff.html` and
   inspect the Before/After view. **Both the text delta and the visual diff graph are mandatory on
   every install — the author's own required pre-PR check, never skipped.** The report-only
   `graph-gate.yml` re-surfaces this delta on the PR (Summary + a `graph-diff` artifact), but that is
   for *reviewers*, never a substitute for checking before you publish. **Always pass `--out`**:
   without it the diff render overwrites `web/graph.html` (the regular dashboard) and dirties the
   tree; leave `web/graph-diff.html` untracked — a review artifact matching the CI artifact, and now
   `.gitignore`d so it can never be committed by accident.
9. **Commit & land:** commit via the **ke-commit** conventions (stage files individually), then
   `git push -u origin concept/<id>` → `gh pr create --base main --fill` → **merge once `audit` is
   clean, as a merge commit** (`gh pr merge <id> --merge` — **never `--squash`**) → `git checkout main && git pull`.
10. **Prune the merged branch — the epilogue.** PRs land by **merge commit** (`--merge`, never
    `--squash`): the branch is a genuine ancestor of `main`, so `git branch -d` recognizes it as
    merged. GitHub deletes the remote branch on merge — leaving a stale local branch, a `gone`
    remote-tracking ref, and (if the install used one) a worktree. Prune them so they don't pile up
    as orphans:
    `git branch -d concept/<id>` →
    `git fetch --prune` (drop the auto-deleted remote branch's stale tracking ref) →
    `git worktree remove <path>` *(only if the install used a worktree)*.

## Paper ingestion (the `type: paper` entry)

When the entry point is an academic paper, step 1's stub is `--type paper` and the loop is richer:

```
ingest(paper P):
  1. resolve P to its canonical source (arXiv id / PDF)
  2. fetch & read it — ground the node in the real paper, cite the source
  3. extract: problem, key idea, contributions, key equations
  4. decompose into prerequisites:
       - concepts it relies on     → explain() each (recurse, closed-world)
       - earlier papers it extends → link as paper prerequisites [[id]]
  5. archive P; render key equations with the visual protocol
```

**Sourcing:** always fetch and ground in the real paper (web), and cite it in `sources:`
(e.g. `arxiv:2407.08608`) — do not rely on memory, especially for recent papers. A paper node uses a
richer template — *Problem · Key idea · Contributions · Key equations · Builds on (papers) ·
Prerequisites · Sources* — plus `authors:` and `year:` frontmatter (schema in `README.md`).

## Invariants

**Operational (this skill owns these — they have no other home):**
- **Audit-gated commits.** Never commit unless `brain.py audit` exits 0. Gate with
  `if uv run python brain.py audit; then …` — **never pipe `audit` to `tail`/`head`**, which masks
  the exit code and has let real leaks through.
- **Commit hygiene & landing.** Conventional Commits + Korean What/Why + the AI footer; stage files
  individually (no `git add -A`/`.`); no `--amend`, no `--no-verify`. **Branch-first on `concept/<id>`;
  default landing is push → PR → merge to `main`** (auto-deploys Pages), then pull — **never land an
  audit-failing state on `main`**. Enforcement is this documented default (no git/settings hook).

**The rules each step obeys (canonical elsewhere — do not restate, follow the pointer):**
- Closed-world law · Depth rule · `sync`-only-unfolder / progressive disclosure · ground-on-insertion
  · scope (durable concepts only) → **`protocols/EXPLAIN.md`**.
- Engine-vs-policy (two layers) · one-hierarchical-tag-per-node · node schema → **`README.md`**.

**Definition of done:** the requested concept(s) are installed and explained closed-world,
**every explained node has its Korean companion `nodes/<id>.ko.md`** (audit's missing-ko hint is empty),
**`reground <id>` comes back empty** (fully grounded — no prose-parked edge left for `lock` to find),
`brain.py audit` is clean, `MANIFEST.md` (and `web/graph.html` when relevant) are regenerated, the
**diff graph is rendered (`graph --diff <base> --out web/graph-diff.html`) and reviewed** (both the
text delta and the Before/After visual) before the PR, the work is committed, and — once the PR
merges — the branch is **pruned** (`git branch -d concept/<id>` + `git fetch --prune`; a **merge
commit** keeps the branch a real ancestor, so `git branch -d` detects the merge).
