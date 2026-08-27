# Explaining a node — primary guidance

A brain node teaches one concept. **This is the primary protocol** for writing a node's
explanation (its prose body). A figure is an *optional, subsidiary* aid — see
`VISUAL_PROTOCOLS.md`, which covers visual design and figure mechanics and is subordinate to this file.

## The entry point — a simple request prompt

The whole protocol has **one entry point: a plain-language request prompt** — *"what is X?"*, *"explain
this paper"*, *"ingest this page"*. Everything in this document is what the agent does **in response to
that single ask**: it chooses the concept, its prerequisites (= edges), and writes the prose, recursing
until the world is closed. The human only *asks*; the agent + `brain.py` turn that one prompt into a
grounded sub-graph. A node exists because a prompt — directly, or by recursion from one — called for it.

## The closed-world law (the brain's defining rule)

Explain a concept using **ONLY** concepts that already exist as prerequisite nodes, linked as
`[[id]]`. If a prerequisite is missing, **archive it first — recursively — until you reach axioms**
(`type: axiom`, no prerequisites). `brain.py audit` enforces this: the world must stay **closed**
(every referenced prerequisite resolves, and body links ⊆ declared prereqs). The reasoning —
choosing prerequisites and writing the grounded explanation — is yours; `brain.py` only stores,
resolves, and validates the graph.

**An axiom is provisional — the law cuts upward too.** `type: axiom` marks a *chosen* recursion floor:
*where we currently stop*, not a claim that nothing lies beneath. So the descent's stop condition has
a dual. When a newly archived field grows a genuine foundation under an old axiom — an OS-kernel field
(process, thread, scheduler, context switch) appearing beneath `parallel-process`, say — that axiom
has become **stranded**, and should be demoted to a `concept` and re-grounded on the field below it.
`brain.py reground` screens for stranded axioms; `lock` acts on them. Without this re-ascent check,
axioms freeze wherever the *order* of field-building happened to leave them, not where they truly
bottom out.

## Decomposition — the `explain(C)` recursion

When the entry point is a bare concept (*"what is X?"*), decomposition is the closed-world law run as
an algorithm:

```
explain(C):
  1. if node(C) exists and status=explained → explain it from its node,
     citing each prerequisite as [[id]].
  2. else:
     a. identify C's prerequisites P1..Pn
     b. for each Pi:
          - if Pi is fundamental (arithmetic, set membership, …)
              → create it as `type: axiom` and STOP (record the floor)
          - else if Pi not in brain
              → explain(Pi)        # recurse: archive the prerequisite first
     c. create node(C) grounded in its now-existing prerequisites
  3. after archiving, run `missing` — the frontier must only contain
     concepts you deliberately deferred, never silent gaps.
```

Default depth: **deep** — dig to true axioms. Worked example, *"what is LoRA?"*:

```
lora
    low-rank-factorization
        matrix-rank
            matrix-multiplication
                arithmetic  🛑 axiom   ← recursion floor, archived explicitly
```

### The frontier — three states of a prerequisite

Every `[[id]]` referenced in a `prereqs:` list is in exactly one state:

| State | Meaning | Shown where |
|-------|---------|-------------|
| **explained** | node exists with a full grounded body | a node in `MANIFEST.md` |
| **stub** | node exists but its body is still a template | a node _(stub)_ in `MANIFEST.md` |
| **missing** | referenced as a prerequisite, but no node file yet | `brain.py missing` |

The **frontier** is the set of *missing* prerequisites — the recursion's to-do list. It must only
hold concepts you **deliberately deferred**, never silent gaps. The world is *closed* when the
frontier is empty: every prerequisite is archived or is an axiom.

> In the `install-concept` skill this recursion is realized **up front**: compose the whole add-queue
> (the prerequisite sub-graph) *before* any `add`, then add one-by-one — so the frontier is resolved at
> compose time, not patched reactively.

## The two authoring passes — `sync` (fill) and `lock` (settle)

A node is born empty (`scaffold`: its id, edges, and tag are decided; the body is a template). Two
**LLM passes** then realize it — both governed by the rules in this document, both bounded by the
layer discipline in the `install-concept` skill's *lifecycle*. Everything below (Depth, the explanation
principles, self-contained notation) is **how `sync` fills a body**; this section adds the two
passes' own discipline: what `sync` *reports* and what `lock` *acts on*.

### `sync` — fill the body (EN + KO), write the summary, report structure (never reshape it)

`sync` is the **only pass that unfolds a node** — it reads and authors the full prose, so it is also
the pass that *discovers* the node's true structure. Fill the stub per this whole document
(closed-world, Depth, the principles). `sync` is **content-only on the graph**: it must **never** add,
remove, merge, or relink a node or edge — reshaping structure is `lock`'s job. What `sync` *does* do,
while it has the body open, is leave **two pieces of metadata** so `lock` can act later *without ever
re-opening the body*:

1. **`summary:` — the node's folded view.** One self-contained sentence saying *what the node is*,
   written to disambiguate a generic title (`stack` → "LIFO structure: push/pop at one end", never the
   network stack). This is the representation `lock`, dedup, and the graph reason over while the body
   stays **folded**. Re-author the body → refresh the summary so it never drifts from the prose.
2. **`review:` structural feedback.** You are the pass actually reading the prose, so this is where
   missing or wrong structure is *seen*. When filling surfaces such a problem, **record it and move
   on** — don't reshape. Each observation is a `type=target` note in the `review:` frontmatter list
   (the deterministic worklist `brain.py feedback` shows). Use `=`, not `: ` (it must survive the parser):

- **`missing-prereq=<id>`** — you needed a concept that is *not* a declared prerequisite to ground
  the explanation, and caught yourself prose-parking it (the Depth red flag). The single most
  reliable structural signal: you are the node that just tried, and failed, to ground it.
- **`unused-prereq=<id>`** — a declared prerequisite you never actually needed.
- **`overlaps=<id>`** — this node substantially restates a node you know already exists.
- **`mislink=<id>`** — a `[[link]]` whose target is wrong, or a prerequisite at the wrong granularity.
- **`regrounding=self`** — the concept cannot be adequately grounded with its current prerequisites
  at all (it needs restructuring, not just one more edge).

**Optional Korean companion — `nodes/<id>.ko.md`.** The English node is canonical. When a Korean
translation is requested or already exists, author or update its **full Korean version** in the same
pass. The companion is like the figure `<id>.svg`: subsidiary to the node, **no frontmatter, never a
node**. It mirrors the English body one-to-one:

- **Headings**: `# <한국어 제목>` · `## 요약` (= `## Summary`) · `## 상세 설명`
  (= `## Grounded explanation`); any other `##` section mirrors likewise (a paper node mirrors
  its own template the same way).
- **Same graph symbols**: every `[[id]]` link and the `![…](<id>.svg)` figure embed appear
  **verbatim** — ids and file names are never translated (the figure's alt text may be Korean).
  `audit` holds the companion to the same closed-world law: its links ⊆ the owning node's
  prereqs, no dead links.
- **Terminology**: translate the prose; on first use keep the established English term in
  parentheses — `문맥 교환(context switch)` — then use the Korean form. LaTeX, code, and
  identifiers stay verbatim.
- Re-author the English body → re-author any existing or requested companion **in the same pass**, so
  the two never drift (the summary rule, applied to the translation).

### `lock` — settle the structure, **folded**

Run over the whole graph to reconcile it into a coherent, non-redundant, well-grounded state, reading
**only the folded view** of each node — its `{title, type, tags, prereqs}` + the one-line `summary:` —
plus the `review:` feedback `sync` left. **`lock` never routinely unfolds a body**; that is `sync`'s
job. It instead **exploits progressive disclosure**: decide at the shallowest layer that suffices.
`lock` is a **re-index** — for each node it re-derives the *correct* prerequisite set and applies it
with **one declarative `reindex`** call that diffs against the current set: **adding** missing edges
and **pruning** wrong ones (a homonym, an unused edge). add and remove are internal to `reindex`; the
LLM only ever declares the desired set.

> **title → summary → body.** Most pairs separate on the **title** alone; the rest on the **`summary`**
> (which exists precisely to disambiguate a generic title — `stack` the structure vs the network
> stack); only the *few* a summary still can't resolve earn a minimal **body peek** — never a
> wholesale re-read of the graph.

Three inputs:

1. **Local feedback** — the `review:` notes `sync` accumulated (`brain.py feedback`): `missing-prereq`,
   `overlaps`, `unused-prereq`, `mislink`, `regrounding=self`. This is the **primary** channel — the
   structure `sync` *saw* while it had the body open, handed to `lock` as metadata.
2. **Global dedup** — over the **skeleton + summaries** (name + tag + prereq-overlap + summary
   similarity): screen for near-duplicate identities, then confirm a merge by **comparing the two
   summaries** (the folded peek), unfolding a body only if the summaries are genuinely inconclusive.
3. **Edge-validation (the prune direction)** — `brain.py reground --prune` flags suspect *declared*
   edges: **declared-but-unlinked** (the body never uses the prereq) or **homonym-suspect** (cross-field
   + a generic name, e.g. `heap`/algorithms → `container`/OS). Confirm by summary; a wrong edge is
   dropped by `reindex`ing the node without it. (`reground` adds; `reground --prune` removes.)

*(Bootstrap recovery: `brain.py reground` scans prose to re-derive `missing-prereq` feedback for
**legacy** nodes authored before this channel existed — it reconstructs what their `sync` should have
emitted. It is a one-time recovery that feeds input 1, **not** a routine lock-time prose scan; because
it matches on bare names, confirm any hit against the candidate's `summary` before acting.)*

Act on each signal — **every change is a reviewable diff, `audit`-gated, never silent**:

The edge edits all collapse into **one declarative `reindex <node> <correct set>`** (it diffs — adds,
removes, strips dropped `[[links]]`):

- **`missing-prereq=X` (X already a node)** · **`unused-prereq=Y`** · **`mislink=W`** · **a wrong /
  homonym edge (a prune hit)** → fold into the node's correct prereq set and `reindex` it (adds `X`,
  drops `Y` / `W` / the homonym). One call, both directions.
- **`missing-prereq=X` (X not yet a node)** → **scaffold `X`** (`add` + `sync`); the new stub re-enters
  the loop. *This is the recursion the lifecycle loops on.*
- **`overlaps` / a dedup hit** → **merge**: choose the keeper, redirect dependents' edges, ensure the
  keeper's body covers what the other taught, then `remove` the duplicate.
- **`regrounding=self` / a stranded axiom** → `reindex <id> <its correct foundation>` (add `--demote`
  for an axiom → concept), then re-`sync` the body.

Clear each `review:` note you resolve. After every structural change the **closed-world law must
still hold** — run `audit` (body links ⊆ prereqs, no dead links, world closed).

**Convergence.** `lock` and `sync` iterate: a scaffold from `lock` needs a `sync`, which may emit new
feedback, which `lock` acts on again. Stop when no feedback is pending and `lock` makes no new change
— *the graph is settled*. Only then `manifest` + `graph` + commit.

## Depth — a load-bearing mention is a missing node, not prose

The closed-world law cuts both ways: it tells you to *archive missing prerequisites*, but it
does **not** permit flattening a concept you actually lean on into an unexplained prose mention
just to avoid growing the graph. That shortcut — **"prose-parking"** — yields a graph far
**shallower** than its sources: broad headline nodes resting on a thin layer of hand-waved
terms. Resist it.

Classify every technical term in your explanation:

- **Load-bearing** — the reader cannot follow you without it, and you catch yourself
  half-explaining it inline → it is a **missing prerequisite node**. Archive it and link
  `[[it]]`; recurse down to the axioms. *This is the recursion the brain exists for.*
- **Incidental** — a passing analogy, a one-off example, a tool / product / version name, or a
  "shows up later in…" pointer → plain prose, no node, no link.

**Match the source's granularity.** If the source treats X as its own teachable idea (its own
section or worked example), X almost certainly deserves a node, not a clause. Conversely,
operational or version detail (specific tools, flags, file formats) is *reference*, not a
concept — leave it out.

**Check yourself — the ground-check, run at `add`.** After writing a node, two kinds of prerequisite
may be missing, and **both are resolved now, not deferred**:

- a load-bearing term that is **not yet a node** → **archive it** and recurse to axioms (*the recursion
  the brain exists for*);
- a term whose concept **already exists as a node** but you didn't declare → `brain.py reground <id>`
  surfaces it deterministically (it scans your prose for existing nodes you lean on but never linked);
  judge each by its `summary` and **`require`** the real ones.

Repeat until `reground <id>` is empty — the node is then fully grounded. **`lock` is a periodic
safety-net** (dedup + the rarer "a new field landed *beneath* an old node" drift), **not** the routine
grounder: a well-`add`ed node never needs `lock` to discover its prerequisites.

## Self-contained notation

Define every symbol and term **before you use it.** Just as a concept may lean only on prerequisite
`[[nodes]]` (the closed-world law, at the *concept* level), an explanation may use only notation it has
already introduced (at the *symbol* level) — no undefined variable, symbol, or piece of jargon. The
reader meets each one with its meaning already in hand. *(For a math node this takes the form of a
symbol table; in prose, define the term inline on first use.)*

## Explanation principles (apply to the prose first; a figure must honor them too)

1. **Explain the concept ITSELF — its defining structure/contribution — not a prerequisite
   sub-mechanism.** Identify what the concept *is* (its central object and contribution) and make
   that the spine. An enabling sub-part, however essential, is not the concept; a node that explains
   only the sub-part teaches the prerequisite instead.

2. **Teach the WHY, not just the what.** Make a reader who does *not* yet know the concept understand
   *why it works* — its key insight, the invariant it maintains, and the justification for the one
   non-obvious ("magic-looking") step. Give the justifying identity, not a bare result. An account
   that only makes sense to someone who already gets it is a *display, not an explanation*.

3. **Be concrete — a non-degenerate worked instance.** Run a specific small example with real values;
   derive every number from prior ones (no unexplained jumps). Avoid *degenerate* instances (a factor
   collapsing to `1`, a term to `0`, a branch never taken) that hide part of the mechanism — enumerate
   the branches/cases/symmetries first, then pick an instance that triggers them (or show the general
   rule and say which case the numbers illustrate).

4. **Coordinate levels when the concept is rich.** A deep concept lives at once as its conceptual
   **structure** (*what*), its **algorithm** (*how*), and its physical **substrate** (*where it runs*).
   Explain them as coordinated views of **one** worked example, tied by a shared step and a shared
   traced element — not one facet in isolation.

## Explaining a quantity (math) node

A math node is a *quantity* ("what shape is this?"). Present it, **in the prose**, self-contained from
symbol to shape:

1. **Symbols first** — the math form of *self-contained notation* (above): a table naming every symbol
   with its **type/shape** (🟦 scalar · 🟩 vector · 🟧 matrix), in inline LaTeX (`$W$`, `$\Delta W$`, `$d \times r$`).
2. **The equation** — a LaTeX block `$$ … $$` (renders in GitHub / Obsidian / VS Code).
3. **A concrete instance** — real example values ($d = 4096$, $r = 8$), and be **honest about shape and
   relative dimension sizes** (a rank-$r$ factor beside a $d$-sized matrix is a thin sliver; the reader
   should *know* $r \ll d$). Abstract letters blur (`d` vs `n`) — the value says *which* symbol it is.

(The other genre is a *process / mechanism* node — "who sends what to whom?" — covered by principles
1–4 above: defining structure, the why, a worked instance, coordinated levels.)

Most math nodes need only this prose. A **shape figure** is optional; when it helps, render it per the
Equations genre in `VISUAL_PROTOCOLS.md`.

## The figure — draw one whenever it helps deliver the meaning

A figure is subsidiary to the prose, but the trigger is **helpfulness, not necessity**: draw one
**whenever a figure materially helps a reader grasp the concept** — not only when the meaning is
*inherently* visual. When in doubt and a figure would help, lean toward drawing it.

Figures help most when the meaning involves:

- **shape / structure** — true matrix/vector shape, containment, layered stacks;
- **flow / routing** — who sends what to whom (dataflow, collectives, comms);
- **change over steps / time** — a process unfolding, a running state, a schedule;
- …but also any **relationship, comparison, or process** that a visual scaffold makes click faster
  than prose alone.

### Design the visual explanation before drawing the figure

A technically complete diagram is not automatically an explanation. Before choosing panels, SVG
blocks, or animation phases, write the figure's **visual thesis**: one sentence naming the problem,
the decisive transformation, and the payoff. A useful form is:

> Because `<problem>`, `<concept>` changes `<before>` into `<after>` by `<decisive action>`, so
> `<payoff>`.

Name the **audience** and the figure's **single job**. “Teach the whole node” is not a job; “make the
reader see why reuse changes the bottleneck” is. Ground the visual language in the subject's own world:
its real shapes, materials, instruments, spatial relations, operations, and characteristic motion.
Generic boxes and arrows are valid only when boxes and routes encode those facts; they are not a
default aesthetic. If replacing the concept's labels would let the same composition explain an
unrelated node, the design is templated rather than derived.

Choose one **traced object** the reader can follow through that sentence. It may be a value, request,
token, region, or other concrete instance from the node's worked example. The object keeps its
identity across every view; changing examples between panels makes the reader reconstruct the story
instead of learning the concept.

Reveal the thesis progressively, in this order:

1. **Intuition — what and why.** One dominant picture makes the problem and payoff recognizable with
   few words. It assumes no knowledge of the target concept, but it must not use an analogy whose
   mapping to the real mechanism is hidden.
2. **Mechanism — how.** The same picture and traced object expose the decisive transformation through
   one small, non-degenerate worked instance. Introduce only the technical names needed to follow it.
3. **Precision — where the simplification stops.** Exact shapes, values, equations, boundaries, or
   substrate labels qualify the mechanism. Precision may live in a later act, a subordinate panel, or
   the prose; do not crowd it into the intuitive first view merely to make the figure exhaustive.

These are **levels of disclosure, not three mandatory panels**. A simple concept may express all three
in one static composition; a changing mechanism may use three clock-aligned acts. Every later level
must refine the same visual model rather than replace it with an unrelated diagram.

Treat the decisive transformation as the figure's **signature moment**: the one use of dominant scale,
contrast, or motion that the reader should remember. Keep supporting elements quiet. Structure,
spacing, colour, scale, and rhythm must each encode a true relationship or yield to neutral restraint;
decoration that carries no meaning competes with the explanation.

Before rendering, state the intended answers to the **comprehension test**: after seeing the figure,
an unfamiliar reader should be able to say (1) what problem exists, (2) what changed, (3) what caused
the change, and (4) why the result is useful. If the figure cannot support those answers, revise the
visual thesis or traced object before polishing its mechanics. After rendering, inspect every dwell
and transition at mobile and laptop fit-to-screen sizes, then make a subtraction pass: remove one
non-essential label, ornament, panel, or motion and keep it removed unless comprehension worsens.

**The one guardrail (so a figure *adds*, not decorates):** don't draw what a single sentence,
equation, or table **fully** conveys — a bare number, a one-line rule, or a clean derivation belongs
in text, not lettered onto a figure. A figure must *add* comprehension beyond the prose, never just
restate it.

When a figure is warranted, **derive it from this prose** (not from a separately invented spec), and
draw it per `VISUAL_PROTOCOLS.md`.
