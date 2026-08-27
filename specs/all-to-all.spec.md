# Figure spec — `all-to-all` (Step 0)

> Derived from `nodes/all-to-all.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader who knows scatter and gather but has not used personalized collectives.

**Single job:** Show that all-to-all transposes source-owned outgoing rows into destination-owned incoming rows without combining values.

**Visual thesis:** Every source partitions its row by destination; after the collective, every destination owns one piece from every source.

**Traced object:** `a₂`, which begins in source P0's destination-P2 column and ends in destination P2's source-P0 column.

**Subject visual vocabulary:** Source×destination matrix, destination×source matrix, source-colored cells, row ownership, and transpose.

**Signature moment:** The same sixteen chunks change ownership layout from source rows to destination rows.

**Anti-template test:** The input and output matrices contain personalized `i→j` chunks; the row-to-column identity specifically distinguishes all-to-all from all-gather and reduction.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | chunks are moved intact | same labels appear before and after |
| **Space** | source/destination indices exchange axes | stacked matrices with explicit axis labels |
| **Colour** | source identity | one stable color per source across both matrices |
| **Trace** | one concrete transfer | gold outline around `a₂` in both states |
| **Operation** | transpose, not arithmetic | direct central rule; no crossing network edges |

**Progressive disclosure:** First view shows colored source rows becoming mixed destination rows. Axis labels and `a₂: P0 → P2` then make the indexing precise.

**Comprehension test:** P2 receives `[a₂,b₂,c₂,d₂]`, one P2-bound piece from each source; it does not receive every chunk or sum anything.

**First-view constraints:** 720 px canvas; essential labels at least 15 px; no edge web or animation.

**Plan critique:** The previous sixteen-wire fan-out was accurate but made correspondence harder to see as the figure scaled down. Matrix position already encodes every transfer more efficiently.

**Rendered critique:** Native-size inspection confirms that all four source and destination rows remain visible, the headline and axis labels fit, and `a₂` is traceable by both text and a gold outline. Stable source colors turn from rows into columns while cell labels remain unchanged, so the transpose is readable without crossing edges or color-only inference. No text overlaps or clips.

**Reduced-motion result:** Static figure; no motion required.

## Genre & spine

Before/after matrix transformation. The vertical spine is source-owned rows → transpose rule → destination-owned rows.

## Figure trigger

- **SHAPE:** the two matrix axes swap.
- **FLOW:** every cell changes owner according to its destination index.
- **CHANGE:** source-grouped storage becomes destination-grouped storage.

## Dynamics

No payload changes in transit. All sixteen transfers occur conceptually in parallel, but the static transpose encodes them without routing clutter.

## Worked instance

P0 begins with `[a₀,a₁,a₂,a₃]`. After the collective, P2 owns `[a₂,b₂,c₂,d₂]`. The highlighted `a₂` demonstrates the rule for every other cell.

## Caption/text

Keep “transpose, never sum” and the traced transfer directly between the states. The node prose carries performance and cost details.
