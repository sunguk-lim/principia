# Figure spec — `transformer-attention` (Step 0)

> Derived from `nodes/transformer-attention.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader who knows softmax, vector dot products, and matrix multiplication.

**Single job:** Show that one query’s query-key similarities become sum-to-one weights that mix corresponding value vectors into one context-aware output.

**Visual thesis — one sentence:**

> Because a token needs information from other positions, attention changes its query-key similarities into a contextual vector by softmax-normalizing one score row and using those weights to average the aligned value rows.

**Traced object:** The second query row and its three aligned key/value positions.

**Subject visual vocabulary:** Query row, key columns, score row, softmax weights, value-vector rows, weighted arrows, vector addition, and output row.

**Signature moment:** Three weighted value vectors visibly combine into `[0.3,0.9]`.

**Anti-template test:** Row-aligned query-key scores controlling a weighted sum of value vectors is specific to attention.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | scalar scores/weights versus value vectors | scalar cells and two-cell vector strips |
| **Space** | index correspondence and dataflow | each score, weight, and value stays in one column |
| **Scale** | attention weight | connector thickness and weight label proportional to `.1/.7/.2` |
| **Colour** | data position | blue/teal/purple position identity held through scores, weights, values |
| **Rhythm** | n/a — closed-form row derivation | static left-to-right/downstream DAG |

| level | what the reader sees | words/notation introduced | what remains unchanged |
|---|---|---|---|
| **Intuition** | one token gathers more from relevant positions | query, value, context | three aligned positions |
| **Mechanism** | dot products become softmax weights that scale values | score, softmax, weighted sum | same row and position colors |
| **Precision** | exact scores, weights, vectors, and output | shapes and numeric equation | same traced query |

**Comprehension test — intended answers from the figure alone:**

1. What problem exists? — One token’s own vector lacks surrounding context.
2. What changes? — It becomes a mixture of value vectors from all positions.
3. What causes the change? — Query-key matches become softmax weights.
4. Why is the result useful? — Relevant positions contribute more while weights still total one.

**First-view constraints:** The 720-pixel canvas uses no essential label below 15 px. The detailed row owns most ink; the full tensor-shape pipeline remains a compact top strip.

**Plan critique:** A matrix-only pipeline was rejected because it proved shapes but not semantics. A generic token graph was also rejected because it hid the weighted vector arithmetic.

**Rendered critique:** The first 1440 px render had no clipping or rest occlusion and made connector thickness, aligned value vectors, and the exact `[0.3,0.9]` result legible. Its softmax arrow ran between positions 1 and 2, so it was moved beneath the center of the complete score row to represent joint row normalization. Repeated full matrices and a separate legend remain removed; direct labels and aligned position colors carry identity.

**Reduced-motion result:** Static derivation; no motion required.

## Genre & spine

Equation/shape dataflow. One query row is the spine; the full `QKᵀ → P → PV` shapes form a subordinate overview.

## Figure trigger (EXPLAIN.md)

- **SHAPE/structure** — one score/weight per key aligns with one value-vector row.
- **FLOW/routing** — weights scale corresponding values before combination.
- **CHANGE over steps** — n/a; static closed-form derivation.

## (a) Entity inventory — name everything BEFORE drawing

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | actors / participants | n/a — math concept |
| WHAT-1 | data items with identity | one query, three keys, three two-component value vectors |
| WHAT-2 | computed / derived results | three scores, three weights, one output vector |
| WHAT-3 | running state | n/a — atomic weighted sum |
| WHAT-4 | persistent structure + invariant | each weight row is positive and sums to one |
| WHERE-1 | substrate / resource tiers | n/a — math concept |
| WHERE-2 | layout / addressing rule | token position aligns score, weight, and value column |
| WHEN-1 | ordered phases | dot products/scale → row softmax → weighted value sum |
| WHEN-2 | concurrency lanes / timeline | n/a — static derivation |
| WHEN-3 | before → after snapshots | query → contextual output |
| HOW-1 | algorithm over the structure | three parallel dot products, atomic normalization, atomic weighted sum |
| HOW-2 | protocol / message alphabet | n/a — math concept |
| WHY-1 | quantities / complexity | score matrix is `n×n`; caption-only |
| WHY-2 | failure / edge branch | n/a for this worked instance |
| WHY-3 | trade-off comparison | n/a — mathematical operation |
| ANCHOR-1 | worked numeric instance | scaled scores `[ln .1, ln .7, ln .2]` → weights `[.1,.7,.2]`; values `[1,0],[0,1],[1,1]` → output `[.3,.9]` |
| ANCHOR-2 | composition refs | vector dot product creates scores; softmax creates weights; matrix multiplication performs both batched stages |

| element | type | drawn as | level / role |
|---|---|---|---|
| tensor overview | matrices | compact shape strip | precision context |
| scaled score row | vector of scalars | three cells | query-key matches |
| weight row | probability vector | three proportional cells | routing strength |
| values | three vectors | aligned two-cell strips | content to mix |
| output | vector | two computed cells | visible answer |

## (b) Dynamics — provenance / derivation flow

Static score-to-weight arrows preserve position identity. Each weight connector lands on its aligned value vector; all three vectors converge on one labeled weighted-sum operator.

## (c) Static storyboard panels in DAG order

Compact overview: `Q(n×dₖ) · Kᵀ(dₖ×n) → scores(n×n) → row softmax P(n×n)`, then `P · V(n×dᵥ) → O(n×dᵥ)`. Dominant detail carries one row through scores, weights, scaled vectors, and exact output.

## (d) Color — ONE identity dimension + ONE accent

Identity dimension is token position: blue, teal, and purple persist across score, weight, value, and connector. Gold accents only the final contextual output. Column position and direct labels redundantly encode identity.

## (e) Worked instance carried to the visible answer

Softmax of `[ln .1, ln .7, ln .2]` is `[.1,.7,.2]`. Then `.1[1,0] + .7[0,1] + .2[1,1] = [.1+0+.2, 0+.7+.2] = [.3,.9]`.

## (f) Stays as caption / text

Projection matrices, scaling motivation, multi-head variants, and LoRA attachment remain in prose. One caption states that applying the same row operation to every query produces the full `n×dᵥ` output.
