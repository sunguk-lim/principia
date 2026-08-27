# Figure spec — `address-space-layout` (Step 0)

> Derived from `nodes/address-space-layout.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader who understands virtual addresses but not how one process arranges them.

**Single job:** Show the fixed low-to-high region order, opposing heap/stack growth, and per-region permission separation in one private address space.

**Visual thesis:** Position decides a virtual address's purpose; permissions decide allowed access; heap and stack consume slack from opposite directions.

**Traced object:** One vertical address column from `0x0` to `0x7fff…`.

**Subject visual vocabulary:** Address ruler, stacked region bands, unmapped gaps, growth arrows, and direct R/W/X labels.

**Signature moment:** Stack grows downward and heap grows upward into the unmapped middle, while neither writable region is executable.

**Anti-template test:** The ordered null/text/data/heap/mmap/stack bands and opposite growth directions specifically encode a process address-space layout.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Position** | region order | one high-to-low address column |
| **Form** | mapped versus unmapped | solid region bands versus hatched slack/null page |
| **Direction** | dynamic boundaries | stack-down and heap-up arrows |
| **Text** | permissions | direct `R+X not W` or `R+W not X` labels |
| **Anchors** | representative starts | `0x0`, `0x400000`, `0x601000`, `0x602000`, `0x7f…`, `0x7fff…` |

**Progressive disclosure:** First view shows the ordered floor plan and opposing arrows. Direct labels then reveal contents, permissions, example addresses, and the stable ASLR invariant.

**Comprehension test:** The reader can locate code versus mutable data, state which direction heap and stack grow, and explain why writable bytes cannot execute.

**First-view constraints:** 720 px square; essential labels at least 15 px; static figure; region heights explicitly schematic rather than quantitative.

**Plan critique:** The former five-act 1200×1210 animation allocated most space to program traces, numeric pointer updates, and a recursion crash branch. Those are consequences and examples, not the layout's irreducible structure.

**Rendered critique:** Native-size inspection confirms the complete `0x0 → 0x7fff…` order, clear mapped versus hatched-unmapped bands, and opposing heap/stack boundary arrows that do not obscure content. Permission labels, the no-W+X security rule, and the ASLR invariant remain readable without overlap or clipping.

**Reduced-motion result:** Static figure; no motion required.

## Genre & spine

Address map. One vertical axis carries the entire explanation from lowest to highest virtual addresses.

## Figure trigger

- **SHAPE:** fixed ordered region bands.
- **DIRECTION:** heap and stack boundaries move toward the middle.
- **CONSTRAINT:** permissions differ by region and never grant W+X.

## Dynamics

Static growth arrows describe possible boundary movement without simulating individual allocations or calls. Exact starts may change under ASLR; ordering, role, and permissions persist.

## Worked instance

The null page begins at `0x0`; text near `0x400000`; data near `0x601000`; heap near `0x602000`; mappings near `0x7f…`; and stack near `0x7fff…`. Values establish order only and are not drawn to scale.

## Caption/text

Keep R/W/X rules on their regions and ASLR in one compact callout. Stack-overflow behavior and detailed allocator/call traces remain in prose.
