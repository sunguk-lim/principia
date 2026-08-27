# Figure spec — `tensor-parallelism` (Step 0)

> Derived from `nodes/tensor-parallelism.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader familiar with matrix multiplication and GPU collectives.

**Single job:** Show how matched column/row sharding lets four GPUs compute one MLP locally until four full-shaped partial sums require exactly one all-reduce.

**Visual thesis:** Because one layer’s matrices are too large for one GPU, tensor parallelism splits `A` by columns and matching `B` by rows, so each GPU computes a local activation shard and full-shaped partial output before one SUM reconstructs the true result.

**Traced object:** GPU 1’s teal path `A₁ → Y₁ → GeLU(Y₁)·B₁ → Z₁ → Z`.

**Subject visual vocabulary:** Matrix grids, column shards, row shards, per-GPU lanes, replicated input, local elementwise transform, partial vectors, and many-to-one SUM.

**Signature moment:** Four full-shaped partial `Zᵢ(1×4)` vectors converge into one true `Z(1×4)`.

**Anti-template test:** Matched column shards of the first weight and row shards of the second weight, joined by one all-reduce, specifically encode tensor-parallel MLP algebra.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | matrix/vector/shard shape | gridded matrices, shard boundaries, and direct shape labels |
| **Space** | shard correspondence | matching GPU index and color persist across Aᵢ, Yᵢ, Bᵢ, and Zᵢ |
| **Scale** | shard/full dimensions | A is 4×8 split into 4×2; B is 8×4 split into 2×4; every Zᵢ is 1×4 |
| **Colour** | GPU ownership | four stable shard colors |
| **Rhythm** | two local stages then one collective | static stage bands in dependency order |

**Progressive disclosure:** First view shows four local colored lanes converging once. Mechanism labels column split, local GeLU, row split, partial sum. Precision adds all shapes and a small unsharded reference result; layout and identities stay fixed.

**Comprehension test:** The layer is split within each matrix; A columns create Y shards, matching B rows consume them locally, and only full-shaped partial Z values communicate once to recover the reference result.

**First-view constraints:** 720 px canvas; essential labels at least 15 px. The unsharded reference is one compact equation, never a duplicate pipeline.

**Plan critique:** The former side-by-side full and sharded pipelines were rejected because duplication consumed half the canvas and forced unreadable labels.

**Rendered critique:** Native-size inspection confirms that each A column shard connects vertically to its matching Y shard, the same ownership identities recur in the B rows and partial Z outputs, and all four partials converge only at the SUM. Essential labels remain readable, arrows stay attached, the compact reference equation fits, and no text overlaps or clips. Redundant one-GPU matrices, repeated captions, and tiny per-cell labels are absent.

**Reduced-motion result:** Static figure; no motion required.

## Genre & spine

Dataflow with four GPU ownership lanes. One large A/B matrix pair supplies the structural spine; local vector products lead to one atomic combine.

## Figure trigger

- **SHAPE:** A column split must match B’s row split.
- **FLOW:** each GPU’s local shard path remains independent until one all-reduce.
- **CHANGE:** static ordered stages; no animation needed.

## (a) Entity inventory

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | actors | GPUs 0–3 |
| WHAT-1 | data identity | replicated X; A/B shards by GPU |
| WHAT-2 | derived results | Yᵢ shards, partial Zᵢ, true Z |
| WHAT-3 | running state | n/a — atomic matrix operations |
| WHAT-4 | persistent invariant | matching A-column/B-row ownership per GPU |
| WHERE-1 | resource tiers | one lane per GPU; communication boundary at all-reduce |
| WHERE-2 | addressing rule | A columns and B rows share hidden-dimension shard index |
| WHEN-1 | phases | replicate X; local X·Aᵢ; local GeLU; local ·Bᵢ; SUM all-reduce |
| WHEN-2 | concurrency | four GPU lanes operate independently before combine |
| WHEN-3 | before/after | four partials → one true result |
| HOW-1 | algorithm | concurrent local chains feeding atomic SUM |
| HOW-2 | protocol | one all-reduce SUM |
| WHY-1 | quantities | shapes shown directly |
| WHY-2 | edge case | n/a |
| WHY-3 | trade-off | model memory improves; communication occurs once per block, caption-only |
| ANCHOR-1 | instance | `X(1×4),A(4×8),Yᵢ(1×2),Bᵢ(2×4),Zᵢ(1×4),Z(1×4)` across 4 GPUs |
| ANCHOR-2 | composition | matrix multiplication and all-reduce |

## (b) Dynamics

Static arrows remain within each colored ownership lane until four partial vectors converge on the all-reduce. No payload changes in transit.

## (c) Ordered phases

Stage 1: replicated X multiplies four A column shards. Stage 2: local GeLU requires no communication. Stage 3: each Yᵢ multiplies matching B row shard to form full-shaped partial Zᵢ. Stage 4: one SUM all-reduce reconstructs Z.

## (d) Color

Identity dimension is GPU ownership, held across Aᵢ, Yᵢ, Bᵢ, and Zᵢ. Gold accents only the final true Z. Direct GPU labels and fixed lane position make ownership redundant with hue.

## (e) Worked instance

Four 4×2 A shards concatenate to A(4×8); four 2×4 B shards stack to B(8×4). Each Yᵢ(1×2)·Bᵢ(2×4) yields a full-shaped Zᵢ(1×4), and `Z=ΣᵢZᵢ` matches the unsharded result.

## (f) Caption/text

Keep “local GeLU · no communication,” “full shape · partial sum,” and “one SUM all-reduce” directly anchored to their stages. Detailed numeric multiplication remains in prose.
