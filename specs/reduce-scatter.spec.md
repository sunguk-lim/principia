# Figure spec — `reduce-scatter` (Step 0)

> Derived from `nodes/reduce-scatter.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader who understands reduce and scatter separately.

**Single job:** Show that equal-length vectors reduce independently by column and that reduced slice j becomes the sole output of process j.

**Visual thesis:** Reduce-scatter computes every reduced slice collectively but partitions the resulting vector across ranks.

**Traced object:** Slice 1's teal lane: `[2,3,7,1] → 13 → P1`.

**Subject visual vocabulary:** Process-by-slice matrix, destination-colored columns, independent SUM lanes, computed slices, and rank ownership.

**Signature moment:** Four readable column equations become four different rank outputs in the same horizontal lanes.

**Anti-template test:** The combination of element-wise column reduction and one-slice-per-index ownership specifically distinguishes reduce-scatter from reduce, scatter, and all-reduce.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | equal-length vectors align by slice | one 4×4 matrix with direct row/column labels |
| **Space** | slice j belongs to Pj | four fixed vertical lanes from input column to output rank |
| **Colour** | slice identity | one stable color per column and output border |
| **Change** | values are computed | gold SUM and output surfaces |
| **Quantity** | worked reduction | four equations yielding `[12,13,10,15]` |

**Progressive disclosure:** First view shows four colored matrix columns continuing into four outputs. Equations then reveal the reductions, and the footer locates the operation within all-reduce.

**Comprehension test:** The reader can trace column 1 to 13 at P1 and state why no rank owns `[12,13,10,15]` yet.

**First-view constraints:** 720 px canvas; essential labels at least 15 px; straight attached lanes; no crossing edges or animation.

**Plan critique:** The previous sixteen-line fan-in encoded every transfer literally but obscured the column independence already visible in the matrix.

**Rendered critique:** Native-size inspection confirms four straight, attached lanes from matrix columns through complete SUM equations to their matching process outputs. The teal `[2,3,7,1] → 13 → P1` trace remains stable by position, color, and labels; the all-reduce identity fits; and no edges cross or text overlaps or clips.

**Reduced-motion result:** Static figure; no motion required.

## Genre & spine

Four aligned transformation lanes. The vertical spine is process vectors → per-column reductions → one slice per rank.

## Figure trigger

- **SHAPE:** a matrix reduces to one value per column.
- **FLOW:** each column remains in its destination lane.
- **CHANGE:** four source values become one computed slice.

## Dynamics

All column reductions can run concurrently. The scatter phase changes ownership, not value, and keeps slice j in lane j until process Pj.

## Worked instance

Rows are `[1,2,3,4]`, `[5,3,1,2]`, `[2,7,4,1]`, and `[4,1,2,8]`. Column sums are `[12,13,10,15]`; P0 through P3 receive those values respectively.

## Caption/text

Keep each equation inside its lane and the all-reduce identity in one compact footer. Broader performance detail remains in prose.
