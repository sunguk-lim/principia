# 🧠 Learning Brain — a recursive concept graph

<p align="center">
  <img src="web/how-it-grows.svg" alt="How the graph grows — a concept enters as a root and grows its prerequisite tree down toward axioms; a second concept grows its own tree but reuses an already-existing prerequisite (the gold shared node), and that reuse is the closed-world graph." width="640">
</p>

A second brain for **learning technical concepts**, with one strict rule:

> **Closed-world grounding:** a concept may only be explained using prerequisite
> concepts that already exist in the brain. Missing prerequisites must be
> archived first — recursively — until reaching **axioms** (e.g. arithmetic),
> which are stored explicitly as the recursion floor.

Each concept is one Markdown file (a *node*) in `nodes/`. The brain is an **agentic graph database** —
entities are **nodes** (concepts) and **edges** (prerequisites), and the LLM agent issues **tool-calls**
that the `brain.py` CLI runs as **CRUD** operations on the graph (also a package manager for concepts).

> **What this README is — and where the rest lives.** This README is **reference**: the *pieces* —
> the engine, the data model, the schema, the taxonomy, the commands. Two things deliberately live
> elsewhere, each with a single home, so nothing is duplicated:
> - **The workflow** — *how an install actually runs, step by step* (the lifecycle, the loop, the
>   action table) — is declared in the **`install-concept` skill**
>   (`.claude/skills/install-concept/SKILL.md`).
> - **The authoring rules** that workflow obeys — closed-world law, the Depth rule, the `sync`/`lock`
>   discipline, the `explain()` decomposition — live in
>   **[`protocols/EXPLAIN.md`](protocols/EXPLAIN.md)**.

## The two layers — deterministic engine vs. LLM authoring

The single most important thing to understand: the system has **two layers**, and every
operation belongs to exactly one of them.

- **Deterministic — `brain.py`** (a CLI): pure tool calls, *same input → same output, no
  judgment*. It stores files, validates (`audit`), regenerates the manifest and dashboard,
  lists/removes. It **enforces**; it never reasons.
- **LLM (Claude)**: *judgment*. It **chooses** which concept to install, its prerequisites
  (= edges), and its tag, and **writes** the prose. Everything it produces is checked by `audit`
  before commit — the one correctness check that does **not** depend on the LLM.

**Rule of thumb:** anything that must be *correct and reproducible* (validation, indexing,
rendering) is a `brain.py` command; anything that requires *understanding* (which concept, which
prerequisites, the prose) is the LLM. Every argument the CLI receives — the id, title,
`--requires`, `--tags`, and the entire node body — is **injected by the LLM**.

> One sentence to remember: **the LLM decides *what the knowledge is* — every concept, every edge
> (`prereqs` / `[[links]]`), and every sentence of prose. `brain.py` is the *scribe and inspector*:
> it records the LLM-chosen metadata, validates the edges, indexes, and renders — but originates
> *none* of the knowledge (not a title, not an edge, not a sentence). git distributes it.**

So "the graph's" **topology** (which nodes exist, which edges connect them) is **LLM-decided**;
`brain.py` chooses no edge — it only **records and enforces** them and computes the **derived**
structure (`MANIFEST.md`, levels, the dashboard).

## Mechanism, resources & cost

**Exact mechanism.** "Graph database" is the *model*, not an engine: there is **no DB server, no
network, no daemon** — `brain.py` operates purely over the `nodes/` directory, and every command (a
CRUD tool-call) is a *pure function of the files on disk* (the full set of actions and their typed
signatures is the action table in the `install-concept` skill). The data model: a node is
`nodes/<id>.md` — YAML frontmatter
(`id`, `title`, `summary`, `type` ∈ {concept, paper, axiom}, `tags`, `prereqs`, `sources`, `status`,
`created`, `updated`) + a Markdown body; a `[[id]]` wikilink in the body **is a graph edge**, and
the closed-world law requires body links ⊆ declared `prereqs`. The **only** non-deterministic step
is the LLM authoring the body.

**Required resources.**
- **Python 3**, run via `uv` — `brain.py` and `web/render.py` use the **standard library only**;
  **zero third-party packages**.
- **A web browser** — `web/graph.html` is fully self-contained (inline CSS/JS, no requests); no
  server, works offline.
- **git** — versioning and distribution.
- **Claude (Claude Code)** — the LLM authoring layer + the `install-concept` skill; the only
  "intelligent" requirement.

**Cost.**
- **Deterministic ops (`brain.py`): effectively free** — local, no network, no tokens; a full
  `audit` over all **226** nodes runs in **~0.07 s**.
- **Storage: tiny, plain text** — `nodes/` ≈ 2.6 MB (Markdown + 27 SVG figures), `MANIFEST.md` ≈ 28 KB,
  `graph.html` ≈ 80 KB. Versioned in git like code.
- **LLM authoring — the dominant cost** (tokens). Each node body is one authoring pass; a cluster ≈
  one pass per node plus recursion over new prerequisites.
- **Figures (optional, heaviest)** — `draw-brain-figure` runs best-of-N drawers + gate reviewers
  per figure.

**Where the knowledge lives.** `nodes/*.md` is the **source of truth** (one file per concept, plus
its Korean body companion `<id>.ko.md` and an optional `<id>.svg` figure). `MANIFEST.md` and `web/graph.html` are **generated** and
reproducible from the nodes — disposable; if they drift, `manifest` + `graph` rebuild them.
**Distribution is git** — pushed to a remote, the knowledge is versioned and shared like code.

> **No query index.** `MANIFEST.md` is a **manifest / catalog** (a generated table of contents, the
> *`uv`-lockfile* sense), **not** a graph-database query index (a B-tree/hash lookup structure). The
> brain has no lookup-acceleration structure and needs none — the whole graph is read in full on
> every command (a complete `audit` ≈ 0.07 s).

## Node schema

```yaml
---
id: lora
title: LoRA (Low-Rank Adaptation)
summary: Adapts a frozen pretrained model with a small low-rank weight update ΔW = B·A.  # the folded view
type: concept        # concept | paper | axiom
tags: [ml/deep-learning]  # one hierarchical home (path with '/') — see Taxonomy below
prereqs: [low-rank-factorization, fine-tuning, transformer-attention]
sources: [arxiv:2106.09685]
status: explained    # stub | explained
created: 2026-06-18
updated: 2026-06-18
---
```

Prerequisites are written as `[[id]]` wikilinks in the body — that *is* the graph. Papers
(`type: paper`) additionally carry `authors:` and `year:`, and use the paper template (the
paper-ingestion procedure is in the `install-concept` skill). A node may also carry a **transient**
`review:` list — `type=target` feedback notes written by `sync` and cleared by `lock` (see
`protocols/EXPLAIN.md` → *the two authoring passes*); it is absent on a settled node.

Every node also carries a one-line **`summary:`** — its **folded view**: a self-contained sentence
saying *what the node is*, phrased to disambiguate a generic title (`stack` the structure vs the
network stack). `sync` writes it while authoring; `lock`/`dupes` read it to reason about a node
**without unfolding the body** (progressive disclosure: title → summary → rare body peek).

## Visual protocols

The canonical rules for drawing node figures — global rules, plus the **Equations** and
**Mechanism / dataflow** genres — live in
**[protocols/VISUAL_PROTOCOLS.md](protocols/VISUAL_PROTOCOLS.md)**. The `draw-brain-figure` skill
loads and enforces them.

## Taxonomy — cut the graph by field

Every node carries exactly **one** `tags:` entry: its **primary home** in a hierarchical,
path-style taxonomy where `/` separates levels — e.g. `os/memory`, `ml/llm/inference`. The
hierarchy gives both views at once: the granular leaf (`os/memory`) and, rolled up, the whole
field (`os`).

- **One home per node.** Cross-field membership is *not* expressed by piling on tags — it is
  already carried by the `prereqs:` edges (`cosine-similarity` depends on `vector-dot-product`,
  bridging linear-algebra and retrieval). The tag says where a concept *lives*; the edges say what
  it *connects to*.
- **Roll-up.** `MANIFEST.md` groups leaves under their top-level root with summed counts, and `audit`
  prints the same `root(total): leaf(n), …` tree — so an oversized leaf is visible at a glance.
- **Query by prefix.** `list --tag os` matches everything under `os/*`; `list --tag os/memory`
  narrows to that one leaf.

Current roots: `math` · `ml` · `os` · `gpu` · `parallel-computing` · `networking` · `algorithms` · `databases`.

## Command reference (uv-style — a package manager for concepts)

The CLI mirrors `uv`: concepts are packages, prerequisites are dependencies, the frontier is
unresolved deps, axioms are the base system. *(These are the deterministic `brain.py` commands; how
they are sequenced into an install is the `install-concept` skill's lifecycle.)*

```bash
# install (create) a concept, paper, or axiom
uv run python brain.py add lora --title "LoRA" \
    --requires low-rank-factorization,fine-tuning --tags ml/deep-learning --sources arxiv:2106.09685 --explained
uv run python brain.py add arithmetic --type axiom
uv run python brain.py add flashattention-3 --type paper \
    --title "FlashAttention-3" --authors "Shah et al." --year 2024 \
    --requires transformer-attention,online-softmax --sources arxiv:2407.08608

# inspect · validate · regenerate
uv run python brain.py tree lora              # dependency tree
uv run python brain.py audit                  # deep validation (the commit gate)
uv run python brain.py missing                # list the recursion frontier
uv run python brain.py feedback               # list pending structural feedback (review notes)
uv run python brain.py remove <id> [--force]  # uninstall (refuses if depended on)
uv run python brain.py show lora              # print one node
uv run python brain.py list --tag ml/llm      # cut by field — prefix-matches the whole subtree
uv run python brain.py manifest               # regenerate the catalog (MANIFEST.md)
uv run python brain.py graph                  # regenerate the dashboard (web/graph.html)
uv run python brain.py diff <ref1> [<ref2>]   # structural graph delta between two git revisions (nodes/edges +/-, restructured)
uv run python brain.py graph --diff <base>    # that delta rendered in the dashboard (Before/After toggle)

# lock primitives (deterministic screens/executors; the lock skill orchestrates them)
uv run python brain.py review <id> --add overlaps=foo   # record sync's structural feedback
uv run python brain.py dupes [--tag T]        # screen for redundancy candidates (for lock to judge)
uv run python brain.py reground [<id>]        # screen for stranded axioms the grown graph can now ground
uv run python brain.py merge <from> <into>    # fold one node into another (redirect edges + links)
```

`brain.py graph` delegates to `web/render.py`, which injects the live node/edge data into
`web/graph.template.html` and writes a **self-contained** `web/graph.html` — a directed view of the
dependency DAG: two layouts (layered-DAG / tag-force), **hue = root field, lightness = sub-field**,
size by #dependents, every node labelled (collision-aware), hover-traces a node's full
ancestor/descendant chain, a hierarchical field filter, search, and stats. `--fragment` emits a
head/body-less version for embedding. Aliases: `--requires` = `--prereqs`, `new` = `add`.

`brain.py diff <ref1> [<ref2>]` reports the **structural delta** between two git revisions (or a
revision vs. the working tree) — nodes/edges added·removed plus existing nodes whose edge set changed
(**`restructured`**, the interleave/prune signal); it reconstructs each graph from `nodes/` at that
revision (no checkout) and supports `--json` and `--context` (1-hop neighbourhood). `brain.py graph
--diff <base>` renders that same delta in the dashboard (added green · removed red · restructured
amber, with a **Before / After** toggle that blinks the change in place). On every pull request the
**report-only** `.github/workflows/graph-gate.yml` posts the text delta to the Checks **Summary** and
uploads a self-contained `graph-diff` HTML artifact — it surfaces structural change for review, never
blocking the merge.

```bash
# handy alias
alias brain='uv run python ./brain.py'   # run from the repo root
```

## Layout

```
brain/
  brain.py             graph engine + CLI (Python stdlib only)
  README.md            this file — reference: pieces, data model, schema, taxonomy, commands
  protocols/           the canonical rule docs (skills point here, never duplicate)
    EXPLAIN.md         node-authoring rules (closed-world law, Depth, decomposition, sync/lock)
    VISUAL_PROTOCOLS.md  canonical rules for drawing node figures
  .claude/skills/
    install-concept/   the install WORKFLOW (lifecycle, action table, step checklist)
    lock/              the settle (lock) pass
  .github/workflows/
    pages.yml          deploy the dashboard to GitHub Pages (on push to main)
    graph-gate.yml     report-only PR gate: posts the graph diff + a visual artifact
  MANIFEST.md             auto-generated: stats + frontier + node list
  web/                 web frontend — graph rendering (and future hosted pages)
    render.py          builds {nodes,edges} + injects into the template
    graph.template.html  the dashboard shell (style + canvas renderer; __DATA__ token)
    graph.html         auto-generated: self-contained interactive graph dashboard
  nodes/               one Markdown file per concept (+ <id>.ko.md Korean body, optional <id>.svg figure)
```
