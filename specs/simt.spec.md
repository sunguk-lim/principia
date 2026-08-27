# Figure spec — `simt` (Step 0)

> Derived from `nodes/simt.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A programmer who writes GPU kernels but is new to the SIMT execution model.

**Single job:** Show how scalar per-thread code becomes one warp-wide instruction stream and how masking serializes a 16/16 branch before reconvergence.

**Visual thesis:** The programmer thinks in one thread; hardware issues one instruction to 32 threads, using masks when their program counters disagree.

**Traced groups:** Lanes 0–15 execute the ADD arm in cycle 2; lanes 16–31 execute the SUB arm in cycle 3.

**Subject visual vocabulary:** Scalar code, one warp, four cycle rows, two 16-lane bands, executing versus masked states, and reconvergence.

**Signature moment:** Active/masked bands flip between cycles 2 and 3, then both return active in cycle 4.

**Anti-template test:** The fixed 32-thread warp, per-lane masking, branch serialization, and scalar-code entry specifically encode SIMT.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | hardware grouping | scalar-code card flows into one 32-thread warp card |
| **Space** | branch predicate | stable bands for lanes 0–15 and 16–31 |
| **Time** | issue order | four aligned cycle rows |
| **State** | active versus masked | solid versus pale dashed bands with direct labels |
| **Quantity** | divergence cost | two branch rows and one explicit `1+1=2` cost line |

**Progressive disclosure:** First view shows scalar code becoming a warp. The four rows then reveal full width, mask split, mask flip, and reconvergence.

**Comprehension test:** The reader can explain why cycles 2 and 3 cannot occur together, which lanes produce the SUB results, and why the branch costs two cycles.

**First-view constraints:** 720 px canvas; essential labels at least 15 px; two readable 16-lane bands instead of 32 narrow columns; no animation or legend.

**Plan critique:** The former 1660 px figure repeated hundreds of lane cells, a four-item legend, numeric input rows, control sidebar, and four footer paragraphs. Literal detail displaced the scalar-code-to-warp thesis and failed on phones.

**Rendered critique:** Native-size inspection confirms that scalar code flows clearly into one 32-thread warp, all four cycle rows fit, and the two 16-lane bands flip between active and masked states without ambiguity. Representative ADD/SUB endpoints, the two-cycle cost, and reconvergence invariant remain readable with no overlap or clipping.

**Reduced-motion result:** Static four-row trace; no motion required.

## Genre & spine

Cycle-by-group execution trace. Rows encode time; two fixed columns encode the predicate halves of one warp.

## Figure trigger

- **SHAPE:** 32 scalar threads are bundled into one warp.
- **CHANGE:** masks switch active ownership between branch arms.
- **TIME:** divergent paths execute serially, then reconverge.

## Dynamics

Cycle 1 issues ADD to all lanes. Cycle 2 issues the branch's ADD arm with the upper half masked. Cycle 3 flips masks for SUB. Cycle 4 clears masks for the next shared instruction.

## Worked instance

With `a[i]=10(i+1)` and `b[i]=i+1`, ADD yields lane 0 = 11 and lane 15 = 176; the upper-half ADD endpoints are 187 and 352. SUB for lanes 16–31 yields 153 through 288.

## Caption/text

Keep representative boundary values, the two-cycle cost, and the retire-together invariant. Wider SIMD comparison and worst-case divergence remain in prose.
