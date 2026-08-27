# FlashAttention Figure Specification

## Audience and job

- Audience: readers who know transformer attention and softmax but not GPU memory-aware tiling.
- Job: explain why FlashAttention is exact while avoiding the full score-matrix write.
- Thesis: **stream one score tile through SRAM, merge it into `(m, ℓ, O)`, discard it, and write only the final output.**

## Visual grammar

- Make SRAM the dominant workspace and HBM the lower storage layer.
- Use one persistent identity for a transient score/value tile, one for the running carry, and one for the final output.
- Directly label every state; do not require a legend or animated cursor.
- Cross out the `N × N score matrix` specifically inside HBM, not the score calculation itself.

## Worked trace

Use the node’s single-query, two-tile example:

1. Tile 1: `S=[1,3]`, `V=[10,20]` produces `m=3`, `ℓ=1.14`, `O=21.4`.
2. Tile 2: `S=[2,5]`, `V=[30,40]` raises the max to five.
3. Rebase the old carry once with `α=e^(3−5)=0.135`, then merge the new tile.
4. The final carry is `m=5`, `ℓ=1.20`, `O=44.4`; normalize to `O/ℓ=36.9`.

## Required mechanism

- K/V tiles travel from HBM into SRAM on a visible arrow.
- Each tile is folded into the persistent `(m, ℓ, O)` state and then discarded.
- The rebase multiplier is attached to the transition where a larger maximum appears.
- The final output travels back to HBM exactly once.
- State the invariant: `O/ℓ` equals exact attention over the keys processed so far.

## Constraints

- Static SVG, `720 × 700`, readable at mobile scale.
- No pseudocode panel, loop counters, carousel, live line pointer, detached legend, or full multi-query numeric trace.
- Do not imply approximate attention; the exact-output equivalence must be explicit.
- Keep every transfer arrow attached to its source and destination.

## Verification

- Confirm that tiles are computed in SRAM while the crossed-out matrix is only the avoided HBM allocation.
- Confirm that tile 1’s carry feeds tile 2’s rebase.
- Confirm the numerical trace matches the node.
- Render and inspect text, paths, crossings, and mobile-scale hierarchy.

## Rendered critique

- SRAM is the clear focal workspace, while HBM reads as the source, avoided allocation, and final destination.
- Both streamed-tile paths terminate on their tile boxes, and the output path terminates on its HBM slot.
- The two-tile carry and `0.135` rebase remain numerically complete without competing pseudocode or counters.
- The `N × N` cross-out cannot be mistaken for skipping score computation because it is labeled specifically as an HBM write.
- The final 720 px preview has no clipped equations, path-label collisions, or detached transfers.
