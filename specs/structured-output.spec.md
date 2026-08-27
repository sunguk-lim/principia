# Figure spec — `structured-output` (Step 0)

> Derived from `nodes/structured-output.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader familiar with softmax and probability distributions but new to grammar-constrained generation.

**Single job:** Show that a grammar state removes illegal tokens and renormalizes probability across multiple legal survivors without changing their relative preference.

**Visual thesis — one sentence:**

> Because unconstrained sampling can choose an illegal favorite, structured output changes the vocabulary distribution into a legal-only distribution by masking invalid logits to `−∞` and renormalizing, so every sampled token advances along a valid grammar path.

**Traced object:** The digit decision after `{"x":`, especially illegal favorite `}` and legal digits `7` and `4`.

**Subject visual vocabulary:** Grammar states, legal-set gate, vocabulary rows, crossed-out logits, probability bars, sampling, and a growing JSON string.

**Signature moment:** `}` drops from `0.612` to `0`, while `7` and `4` become `0.622` and `0.378` and retain their ordering.

**Anti-template test:** A grammar-state gate feeding a masked vocabulary distribution and advancing a JSON automaton cannot be relabeled into an unrelated process.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | token/logit/probability/state | aligned token rows, bars, and state circles |
| **Space** | grammar order and per-token correspondence | automaton left-to-right; each token stays on one row |
| **Scale** | probability | bar length proportional to probability within each distribution |
| **Colour** | legality | teal legal survivors, coral illegal tokens, gold sampled token |
| **Rhythm** | n/a — static storyboard | three named stages shown simultaneously |

| level | what the reader sees | words/notation introduced | what remains unchanged |
|---|---|---|---|
| **Intuition** | illegal favorite blocked; legal digits remain | legal, blocked | token rows and grammar state |
| **Mechanism** | illegal logits become `−∞`, then softmax renormalizes | mask, renormalize | same rows and identities |
| **Precision** | exact before/after probabilities and preserved ratio | numeric logits/probabilities | same worked decision |

**Comprehension test — intended answers from the figure alone:**

1. What problem exists? — The model’s favorite token can violate the grammar.
2. What changes? — Illegal probabilities become zero; legal probabilities expand to total one.
3. What causes the change? — The current grammar state masks illegal logits before softmax.
4. Why is the result useful? — Sampling cannot leave the valid grammar path.

**First-view constraints:** A 720-pixel canvas uses essential labels of at least 15 px. The automaton and three distribution columns stack conceptually without animation; detailed exponential arithmetic stays in prose.

**Plan critique:** The former 21-second seven-step animation was rejected because singleton legal sets made renormalization trivial and required readers to wait for the important state. A static two-survivor decision shows problem, transformation, and payoff at once.

**Rendered critique:** The first 1440 px render had no clipping or text occlusion and made the illegal favorite plus two legal survivors immediately legible. Its stage arrows aligned with the sampled-token row, so they were moved into the header gap to show that each operation transforms the whole vocabulary vector. The full legend and repeated singleton opener/closer decisions remain removed because direct row labels and the automaton already carry those facts.

**Reduced-motion result:** The static storyboard is the complete figure.

## Genre & spine

State-machine spine with a subordinate before/mask/after dataflow for the active digit transition. The grammar state owns legality; the aligned probability rows prove its effect.

## Figure trigger (EXPLAIN.md)

- **SHAPE/structure** — grammar position determines the legal subset.
- **FLOW/routing** — raw logits pass through the grammar mask before softmax sampling.
- **CHANGE over steps** — before, masked, and renormalized values differ per token; shown as a static storyboard.

## (a) Entity inventory — name everything BEFORE drawing

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | actors / participants | one model and one constraint engine |
| WHAT-1 | data items with identity | tokens `{"x":`, `7`, `4`, `}`, `cat` |
| WHAT-2 | computed / derived results | unconstrained and constrained probability distributions |
| WHAT-3 | running state | current grammar state `expect digit` |
| WHAT-4 | persistent structure + invariant | grammar automaton; only legal tokens can advance it |
| WHERE-1 | substrate / resource tiers | n/a — no relevant hardware hierarchy |
| WHERE-2 | layout / addressing rule | vocabulary index preserves one row across stages |
| WHEN-1 | ordered phases | model logits → grammar mask → softmax renormalization → sample → advance |
| WHEN-2 | concurrency lanes / timeline | n/a — sequential decoding step |
| WHEN-3 | before → after snapshots | unconstrained distribution → legal-only distribution |
| HOW-1 | algorithm over the structure | conditional legal-set gate followed by atomic normalization |
| HOW-2 | protocol / message alphabet | n/a — local mechanism |
| WHY-1 | quantities / complexity | n/a for the figure |
| WHY-2 | failure / edge branch | unmasked `}` would produce invalid `{"x":}` |
| WHY-3 | trade-off comparison | n/a — fixed guarantee |
| ANCHOR-1 | worked numeric instance | logits `(2,1,0.5,3,0)` → `(.225,.083,.050,.612,.030)` → mask → `(0,.622,.378,0,0)` |
| ANCHOR-2 | composition refs | softmax renormalizes survivors; probability distribution supplies the unit-total invariant |

| element | type | drawn as | level / role |
|---|---|---|---|
| automaton | state machine | four circles and labeled edges | grammar spine |
| token rows | vocabulary | five aligned rows | stable identity |
| unconstrained probabilities | distribution | labeled bars | problem state |
| masked logits | values | legal values or `−∞` | decisive action |
| constrained probabilities | distribution | labeled bars | payoff state |
| sampled `7` | token | gold-ringed cell and advance arrow | visible result |

## (b) Dynamics — provenance / derivation flow

Static connectors route logits through the grammar mask to softmax. Row alignment carries each token’s identity; no payload moves or mutates in transit.

## (c) Static storyboard panels in DAG order

`MODEL SCORES` shows the illegal favorite. `GRAMMAR MASK` shows state `expect digit`, legal set `{7,4}`, and `−∞` replacements. `LEGAL DISTRIBUTION` shows two survivors totaling one, sampling `7`, and advancing to `expect closer`.

## (d) Color — ONE identity dimension + ONE accent

Identity dimension is legality: teal for legal survivors and coral for illegal tokens. Gold accents only the sampled `7`. Labels, check/cross glyphs, and row position make the encoding redundant without color.

## (e) Worked instance carried to the visible answer

Raw logits `(2,1,0.5,3,0)` yield probabilities `(0.225,0.083,0.050,0.612,0.030)`. State `expect digit` keeps logits `1` and `0.5`, masks the rest, and produces `(0,0.622,0.378,0,0)`. Sampling `7` grows `{"x":` into `{"x":7` and advances toward the closer.

## (f) Stays as caption / text

The exponential arithmetic, implementation libraries, and singleton opener/closer decisions remain in prose. One caption states that the ratio between legal survivors is preserved.
