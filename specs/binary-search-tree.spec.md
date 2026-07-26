# Figure spec — binary-search-tree (Step 0)

> Derived FROM `nodes/binary-search-tree.md`. Genre: **hierarchy / tree** (the concept's
> defining shape) carrying a **flow** overlay (the root-down compare-and-descend walk) animated
> as **change over steps** (the tree growing, then a lookup walk, then a contrast chain).
> Self-contained SMIL/CSS SVG, no JS. One master clock.

## Figure trigger (EXPLAIN.md)

**Draw — strongly warranted.** The node's three load-bearing ideas are all visual:
- **SHAPE/structure** — a branching tree of linked nodes vs. a flat sorted array; the BST property
  (left-smaller / right-larger) is a *spatial* invariant best seen, not read.
- **FLOW/routing** — lookup is a root-down walk that *discards a whole branch* per comparison; the
  "one comparison kills half" mechanism is a path through the tree.
- **CHANGE over steps** — insertion *builds* the tree link-by-link with no shifting; this is a
  process unfolding, and the degenerate sorted-insert case is a second evolution to contrast.

Guardrail check: none of these is fully conveyed by one sentence/equation/table. The cost facts
(`O(log n)` vs `O(n)`, comparison counts) **stay as caption text** — they are one-line rules.

## (a) Components / actors — type and level

| element | type | drawn as | level / role |
|---|---|---|---|
| **node** | record (one key) | circle with the key number inside | the tree's atom; level = its depth (root = depth 0) |
| **left/right child link** | pointer | straight edge from parent to child (left edge slants down-left, right down-right) | connects depth *d* to depth *d+1* |
| **empty link** | absent pointer | short dashed stub ending in a small hollow square | the insertion target / lookup-miss endpoint |
| **root** | node | top circle, labeled "root" | depth 0, the single entry point |
| **leaf** | node | node with no outgoing edges | bottom of a branch |
| **the wanted/new key** | traveling token | a small pill carrying the number, riding the path | the element traced through the walk |
| **sorted-array strip** (context panel) | array | a row of numbered cells | the baseline being beaten; shown only to motivate the contrast |

Layout is by tree geometry (parent above children), **not** reading order — this *is* the DAG here.

## (b) Routing / shape-evolution

Two coordinated dynamics, one shared element (the traveling key token):

1. **Descend routing (lookup & insert share it):** token starts at root. At each node, a compare
   badge shows `want ? key`. Outcome routes the token:
   - `=` → stop, node flashes accent (FOUND).
   - `want < key` → the node's **right branch dims out** (discarded), token slides down the **left** edge.
   - `want > key` → the **left branch dims out**, token slides down the **right** edge.
   - reach an empty link → for lookup: ABSENT; for insert: the dashed stub *materializes into a new
     circle* holding the key (one link filled, nothing else moves).
2. **Shape evolution:** the tree grows one node per insert phase; existing nodes never reposition
   (mirrors "no shifting"). A second mini-tree shows the **degenerate** rightward chain.

## (c) Ordered phases → animation frames, with control structure

The worked instance from the prose is the spine. **Control structure is the descend LOOP** —
"at each node: compare, dim a branch, step down" — repeated until equal or empty. Every level of
every walk is a frame (not just the landing).

**ACT 1 — build the tree (insert 5, 3, 8, 1, 4):** one outer iteration per key; inner = the descend loop.
- F1 `insert 5`: empty tree → 5 becomes root.
- F2 `insert 3`: at 5, `3<5` (dim right=none yet), step left, empty → 3 = left child of 5.
- F3 `insert 8`: at 5, `8>5` (dim left), step right, empty → 8 = right child of 5.
- F4 `insert 1`: at 5 `1<5` step left → at 3 `1<3` step left → empty → 1 = left child of 3. (two loop turns)
- F5 `insert 4`: at 5 `4<5` step left → at 3 `4>3` step right → empty → 4 = right child of 3.
- F6 `BST-property check`: highlight root 5; left branch {3,1,4} all <5 (tint cool), right branch {8} >5
  (tint warm). Then node 3: {1}<3, {4}>3. Invariant holds everywhere — caption states the rule.

**ACT 2 — lookup 4 (the discard-a-branch walk):** the loop, traced.
- F7 at root 5: `4<5` → right branch (8) **dims**, token slides left to 3.
- F8 at 3: `4>3` → left branch (1) **dims**, token slides right to 4.
- F9 at 4: `4=4` → FOUND, accent flash. Caption: 3 comparisons, one per level.

**ACT 3 — in-order read:** sweep left-branch → node → right-branch recursively; emit `1,3,4,5,8` into
an output strip, one cell per emit, in tree order. Caption: sorted, with no sort step.

**ACT 4 — insert 6 (no-shift proof):** at 5 `6>5` step right to 8 → at 8 `6<8` step left → empty →
new circle 6 appears as left child of 8. Two comparisons, one link filled, every old node stationary
(freeze-flash the unchanged nodes to show none moved).

**ACT 5 — the catch (degenerate chain):** small side panel. Insert `1,2,3,4` already-sorted: each
attaches as a right child → a straight rightward chain of height 3. Caption: lookup now walks all `n`,
`O(n)` — why balancing exists. (This is the non-degenerate-vs-degenerate contrast the prose draws.)

Loop visibility: the descend loop's "back to compare at the next node" must be visible across ≥2
levels (F4, F5, F7→F8 all show two turns) — satisfies the "carry state across ≥2 iterations" rule.

## (d) Color — ONE identity dimension + ONE accent

- **Identity dimension = position relative to the current/comparison node:** cool teal `#3F9B86` for
  the **left / smaller** half, warm slate `#5B7FA6` for the **right / larger** half. This is the single
  consistent meaning (left-smaller vs right-larger = the BST property) held across the whole figure.
- Idle nodes: neutral `#FBF0DB` fill, `#C79A3E` stroke (house amber).
- Opacity = state: bright = active/now, **dim = discarded branch or done/past**, faint = future scaffold.
- **ACCENT (reserved, one only) = gold `#E8A02E`** for **the key event of the moment**: the node that
  just matched (FOUND), the new circle the instant it is spliced in, the emitted cell. Nothing else
  ever takes the accent.

## (e) Worked instance carried to the visible answer

- Tree built from `5,3,8,1,4` → drawn explicitly: root 5; 5.left=3, 5.right=8; 3.left=1, 3.right=4.
- Lookup `4` → visible FOUND flash at the 4 node after 2 descents.
- In-order output strip literally fills to `1 3 4 5 8`.
- Insert `6` → 6 appears as 8's left child; old nodes demonstrably unmoved.
- Degenerate panel → chain `1→2→3→4` height 3.
All numbers on-canvas derive from prior on-canvas numbers (compares shown explicitly).

## (f) Stays as caption / text (not lettered onto the spine)

- Cost facts: lookup/insert `~log2(n)` when balanced; degenerate `O(n)`; sorted-array insert up to `n`
  shifts. One-line rules → captions only.
- The BST-property statement (one sentence) → step caption in F6, not a wall of text on nodes.
- Trade-off summary (static array = fast lookup/slow insert; balanced BST = both fast) → footer line.
- `STEP n/m` indicator + a one-line caption per frame; small legend for the teal/slate/gold code.
