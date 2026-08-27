# Figure spec — `scan` (Step 0)

> Derived from `nodes/scan.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader familiar with associative reduction but new to parallel prefix algorithms.

**Single job:** Show how inclusive scan produces every prefix through simultaneous offset-doubling rounds.

**Visual thesis:** Each parallel round reads the previous state and doubles the prefix distance represented at every position.

**Traced object:** P2's state: input `2`, then `5+2=7` at offset 1, then `3+7=10` at offset 2.

**Subject visual vocabulary:** Rank-aligned state rows, offset rounds, carry cells, computed prefix cells, and previous-row snapshots.

**Signature moment:** `[3,5,2,7] → [3,8,7,9] → [3,8,10,17]` in two rounds.

**Anti-template test:** The doubling offsets and one different prefix per rank specifically distinguish scan from reduce and broadcast.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | state at one synchronization point | one aligned four-card row per round |
| **Space** | rank ownership | fixed P0–P3 vertical lanes |
| **Time** | parallel propagation | input, offset-1, and offset-2 snapshots |
| **Change** | prefix equations | direct prior-row additions inside each updated card |
| **Invariant** | synchronous reads | explicit “read previous row, then update together” rule |

**Progressive disclosure:** First view shows three state rows and four stable rank lanes. Card equations then reveal which previous-row values combine and why two rounds cover four ranks.

**Comprehension test:** The reader can explain why P2 becomes 7 in round 1, 10 in round 2, and why P1 remains 8 in the second round.

**First-view constraints:** 720 px canvas; essential labels at least 15 px; no crossing fan; no animation.

**Plan critique:** The former triangular fan encoded final dependencies but not the synchronized rounds that make prefix scan parallel, while ten edges and 10 px equations competed for attention.

**Rendered critique:** Native-size inspection confirms three aligned state snapshots, unobstructed rank lanes, and readable equations for both parallel rounds. “Read 1 lane left” and “read 2 lanes left” make the dependencies explicit; P2 traces `2 → 7 → 10`; the synchronous previous-row rule and reduce contrast fit without overlap or clipping.

**Reduced-motion result:** Static figure; no motion required.

## Genre & spine

Staged state transformation. The vertical spine is input snapshot → offset-1 snapshot → offset-2 final prefixes.

## Figure trigger

- **CHANGE:** every round updates some rank-local states.
- **TIME:** the offset doubles from 1 to 2.
- **FLOW:** each rank lane persists through synchronized snapshots.

## Dynamics

All eligible ranks update concurrently from the previous row. Round 1 reads one position left; round 2 reads two positions left. Carries remain unchanged when no predecessor exists at that offset.

## Worked instance

Input `[3,5,2,7]` becomes `[3,8,7,9]` at offset 1 and `[3,8,10,17]` at offset 2. Final values belong to P0 through P3 respectively.

## Caption/text

Keep equations inside state cards, the synchronous-read invariant below the outputs, and one concise comparison with reduce.
