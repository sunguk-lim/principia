# Page Cache Figure Specification

## Audience and job

- Audience: readers who know files and RAM but may equate a successful `write` with durable storage.
- Job: show how the page cache accelerates repeated reads and why dirty writes remain vulnerable until flush.
- Thesis: **the page cache serves file pages from RAM and lets writes finish before disk catches up.**

## Visual grammar

- Use three stable lanes: **Program**, **Page cache · RAM**, and **Disk**.
- Trace one 1 MB file containing 256 × 4 KB pages; follow page/block zero when it changes from `v0` to `v1`.
- Use four directly labeled states: `MISS`, `HIT`, `WRITE`, then the `FLUSH / CRASH` fork.
- Pair every color with lane names, state labels, and values; no legend is required.

## Required mechanism

1. `MISS`: disk supplies 256 blocks, the cache retains 256 `v0` pages, and the program receives 1 MB.
2. `HIT`: the same read returns from the resident pages while disk is idle.
3. `WRITE`: the program changes 512 B; cached `p0` becomes `v1 DIRTY`, disk `b0` remains `v0 STALE`, and the write returns.
4. `FLUSH / fsync`: disk reaches `v1` and the cached page becomes clean.
5. `CRASH first`: volatile cached `v1` disappears and disk still contains `v0`.

## Constraints

- Static SVG, `720 × 700`, readable at mobile scale.
- No controls, carousel, timing animation, detached legend, or separate control-structure panel.
- Keep arrows attached to the exact source and destination boxes.
- End with the explicit conclusion: `write success ≠ durable storage`.

## Verification

- Confirm that only the miss touches disk before the write.
- Confirm that the write arrow stops at the page cache.
- Confirm that both future outcomes begin from the same dirty state.
- Render and inspect for clipped labels, overlapping arrows, and mobile legibility.

## Rendered critique

- The three lanes remain aligned across every state, so the reader can compare RAM and disk without consulting a legend.
- All transfer arrows terminate at their boxes, and the write visibly stops at the cache.
- The shared dirty-state band makes the flush/crash fork causal rather than decorative.
- Labels remain unclipped and readable in the 720 px rendered preview.
