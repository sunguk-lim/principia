# Figure spec — `softmax` (Step 0)

> Derived from `nodes/softmax.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader who knows arithmetic, exponentials, and probability distributions but has not seen softmax.

**Single job:** Show that softmax exponentiates every logit and divides every result by one shared total, producing positive shares that sum to one.

**Visual thesis — one sentence:**

> Because unrestricted logits are not probabilities, softmax changes them into positive shares by exponentiating and dividing every entry by the same exponential sum, so the output is ordered like the input and totals exactly one.

**Traced object:** `[2, 1, 0.1, −1]`, especially `2 → 7.389 → 0.638`.

**Subject visual vocabulary:** Aligned vector cells, exponentiation, one converging sum, a shared denominator, division, and proportional probability bars.

**Signature moment:** Four exponentials converge into `Σeᶻ = 11.580`, which normalizes every output row.

**Anti-template test:** The aligned exponentials, common denominator, and sum-to-one bars specifically depict conversion of logits into a categorical distribution.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | scalar versus vector entries | aligned vector cells; one scalar sum cell |
| **Space** | per-index correspondence and shared normalization | one row per index; all rows converge on one denominator |
| **Scale** | probability magnitude | output bar length proportional to probability |
| **Colour** | given versus computed data | teal input; coral derived values; gold only for the common sum |
| **Rhythm** | n/a — closed-form derivation | static left-to-right DAG |

| level | what the reader sees | words/notation introduced | what remains unchanged |
|---|---|---|---|
| **Intuition — what and why** | scores become positive shares totaling one | logits, probabilities | four aligned rows |
| **Mechanism — how** | exponentials converge to one reused total | `eᶻ`, `Σeᶻ` | row identity and flow |
| **Precision — limits/exactness** | exact exponentials, denominator, quotients, and rounded total | values to three decimals | same input and output |

**Comprehension test — intended answers from the figure alone:**

1. What problem exists? — Logits are unrestricted scores, not probabilities.
2. What changes? — Each score becomes a positive share.
3. What causes the change? — Exponentiation followed by division by one shared sum.
4. Why is the result useful? — Outputs preserve ranking and sum to one.

**First-view constraints:** The 720-pixel canvas uses no essential label below 16 px. Four rows, the common sum, and final bars remain legible at mobile fit-to-screen size; the general formula stays in prose.

**Plan critique:** A generic input-arrow-output diagram was rejected because it hid the common denominator and could not prove the unit total.

**Rendered critique:** The first 1440 px render exposed detached normalization arrows; a visible bus now connects the shared denominator to all four output rows. The second render has no occlusion or clipping, preserves clear hierarchy, and remains readable when reduced. The redundant legend stays removed because stage labels and aligned forms already distinguish given and computed values.

**Reduced-motion result:** Static derivation; no motion is required.

## Genre & spine

Equation/shape figure with a static dataflow DAG. Per-index rows are the spine; the converging sum is the shared subordinate operation.

## Figure trigger (EXPLAIN.md)

- **SHAPE/structure** — co-indexed values remain aligned while one denominator is shared.
- **FLOW/routing** — every exponential contributes to the total, which normalizes every entry.
- **CHANGE over steps** — n/a; this closed-form transform is a static derivation.

The general formula and differentiability stay in prose.

## (a) Entity inventory — name everything BEFORE drawing

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | actors / participants | n/a — math concept |
| WHAT-1 | data items with identity | four input logits aligned by index |
| WHAT-2 | computed / derived results | four exponentials, their sum, four probabilities |
| WHAT-3 | running state | n/a — atomic sum, no asserted order |
| WHAT-4 | persistent structure + invariant | output vector; positive entries total one |
| WHERE-1 | substrate / resource tiers | n/a — math concept |
| WHERE-2 | layout / addressing rule | index `i` stays on one horizontal row |
| WHEN-1 | ordered phases | exponentiate all; sum; divide all by the sum |
| WHEN-2 | concurrency lanes / timeline | n/a — static derivation |
| WHEN-3 | before → after snapshots | logits → probabilities |
| HOW-1 | algorithm over the structure | parallel exponentiation, atomic sum, parallel division |
| HOW-2 | protocol / message alphabet | n/a — math concept |
| WHY-1 | quantities / complexity | n/a for the figure |
| WHY-2 | failure / edge / degenerate branch | n/a — finite exponentials keep the denominator positive |
| WHY-3 | trade-off comparison | n/a — identity, not a design knob |
| ANCHOR-1 | worked numeric instance | `[2,1,0.1,−1] → [7.389,2.718,1.105,0.368] → 11.580 → [0.638,0.235,0.095,0.032]` |
| ANCHOR-2 | composition refs | exponential function creates positive weights; arithmetic sums/divides; probability distribution supplies the invariant |

| element | type | drawn as | level / role |
|---|---|---|---|
| `z` | vector | four teal cells | given logits |
| `eᶻ` | vector | four coral cells | positive weights |
| `Σeᶻ` | scalar | one gold cell fed by all weights | shared denominator |
| `p` | vector | values plus proportional coral bars | visible answer |

## (b) Dynamics — provenance / derivation flow

Static arrows connect each input row to its exponential. Four connectors converge on the shared sum; a common normalization route leads to aligned output rows.

## (c) Static storyboard panels in DAG order

One continuous static DAG: logits → exponentials → shared sum → normalized probabilities. No STEP chips because no time axis exists.

## (d) Color — ONE identity dimension + ONE accent

Identity dimension is derivation role: teal = given input and coral = computed values. Gold accents only the common normalization sum. Labels and alignment redundantly encode identity.

## (e) Worked instance carried to the visible answer

`e²=7.389`, `e¹=2.718`, `e⁰·¹=1.105`, `e⁻¹=0.368`; displayed sum `11.580`. Division yields `0.638`, `0.235`, `0.095`, and `0.032`, with `Σp ≈ 1.000` after rounding.

## (f) Stays as caption / text

Differentiability, smooth-maximum interpretation, and the general `n`-class formula remain in prose. One caption states that a shared denominator preserves ranking while forcing a unit total.
