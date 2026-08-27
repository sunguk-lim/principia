# Figure spec — `reduce` (Step 0)

> Derived from `nodes/reduce.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader familiar with collective calls and associative operations.

**Single job:** Show how reduce forms partial results in a balanced tree and stores the final computed value only at the root.

**Visual thesis:** Associativity changes an all-to-one combine from a serial fold into logarithmic tree steps.

**Traced object:** The contribution `5` from P1, which joins P0's `3` to form partial `8`, then joins partial `9` to form root result `17`.

**Subject visual vocabulary:** Process contributions, paired partial sums, balanced tree levels, computed-result color, and designated root.

**Signature moment:** `3+5=8` and `2+7=9` appear side by side before `8+9=17`.

**Anti-template test:** The balanced associative combine and root-only receive state distinguish reduce from gather and all-reduce.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | original versus computed values | source-colored inputs; gold partial/result boxes |
| **Space** | associative tree | two parallel branches merge at one final node |
| **Time** | logarithmic stages | explicit Step 1 and Step 2 bands |
| **Ownership** | root-only output | attached final path to P0; empty receive states for P1–P3 |
| **Quantity** | worked SUM | `3,5,2,7 → 8,9 → 17` directly labeled |

**Progressive disclosure:** First view shows four contributions collapsing through two tree levels. Labels then reveal simultaneous partials and root-only ownership.

**Comprehension test:** The reader can state that both pair sums happen concurrently, the partials combine once more, and only P0 receives 17.

**First-view constraints:** 720 px canvas; labels at least 15 px; every tree edge remains attached; no animation.

**Plan critique:** The previous single central SUM box showed the arithmetic but hid the associative parallelism and forced four curved inputs into one crowded target.

**Rendered critique:** Native-size inspection confirms two unobstructed first-level branches, attached connectors through `8+9=17`, and an attached final path to P0. The Step 1 label occupies the clear gap between branches, every equation remains readable, P1–P3 are explicitly marked as receiving no result, and no text overlaps or clips.

**Reduced-motion result:** Static figure; no motion required.

## Genre & spine

Balanced reduction tree. The vertical spine is contributions → parallel partials → final partial → root receive state.

## Figure trigger

- **FLOW:** four inputs converge through attached tree edges.
- **CHANGE:** original values become new computed partials.
- **TIME:** two tree stages replace four serial additions.

## Dynamics

The two first-level pairs combine concurrently. Their results become the only inputs to the second level, whose result is delivered to the designated root.

## Worked instance

P0=3, P1=5, P2=2, and P3=7 under SUM. Step 1 forms 8 and 9; step 2 forms 17; P0 receives 17.

## Caption/text

Keep stage labels and equations directly on the tree. Performance detail and contrasts with gather/all-reduce remain in prose.
