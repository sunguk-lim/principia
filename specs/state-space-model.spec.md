# Figure spec — `state-space-model` (Step 0)

> Derived from `nodes/state-space-model.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader who knows neural-network parameters but is new to recurrent sequence models.

**Single job:** Show a fixed-size state carrying history through three steps and prove that the equivalent convolution produces the same outputs.

**Visual thesis — one sentence:**

> Because a sequence model needs bounded memory of its past, an SSM changes each old state and new input into one same-sized next state by a linear recurrence, so inference uses constant state while training may use an exactly equivalent convolution.

**Traced object:** The scalar state `h: 0 → 2 → 1 → 4.5` for input `[1,0,2]`.

**Subject visual vocabulary:** Equal-size state registers, input injection, decay, recurrence arrows, output readout, lag kernel, and lower-triangular convolution sums.

**Signature moment:** At `x₂=0`, `h₂=1` and `y₂=3` remain nonzero because prior state survives; the bottom convolution row independently reaches the same result.

**Anti-template test:** Equal-size carried registers with `A hₜ₋₁+B xₜ` and lag weights `CAᵏB` are specific to a linear state-space recurrence.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | input/state/output/kernel roles | equal scalar cells in the 1-D example, explicitly labeled as vector/matrix generalization |
| **Space** | time order and recurrence dependence | three timestep columns connected left-to-right |
| **Scale** | fixed state size | every state register has identical dimensions |
| **Colour** | data role | teal input, coral state, gold output/kernel |
| **Rhythm** | ordered recurrence | static STEP 1–3 columns; time already spatial |

| level | what the reader sees | words/notation introduced | what remains unchanged |
|---|---|---|---|
| **Intuition** | one same-size memory cell moves through time | input, state, output | three columns |
| **Mechanism** | old state decays, input enters, output reads state | A, B, C | same carried state |
| **Precision** | exact recurrence and convolution arithmetic | h/y/k values | same instance and columns |

**Comprehension test — intended answers from the figure alone:**

1. What problem exists? — Sequence history must persist without growing memory.
2. What changes? — One fixed-size state is updated at each token.
3. What causes the change? — Linear blend `A hₜ₋₁+B xₜ`, then readout `C hₜ`.
4. Why is the result useful? — Constant-state recurrence and parallel convolution are exactly equivalent.

**First-view constraints:** The 720-pixel canvas uses no essential label below 15 px. The recurrence receives most ink; the convolution proof is one compact aligned band.

**Plan critique:** The former 16-second loop was rejected because an arbitrary screenshot hid most arithmetic and delayed the equality proof. A static timeline exposes order without requiring motion.

**Rendered critique:** The first 1440 px render exposed captions crossing between adjacent state boxes and an initial-state arrow landing on `x₁` instead of the state update. Redundant in-box invariant captions were removed, the middle label was shortened, and `h₀` now curves directly into `h₁` while `x₁` enters vertically as its co-input. The second render has no occlusion or clipping and keeps the recurrence/convolution equality legible. The parameter sidebar, animation cursor, repeated legends, and separate cost bullets remain removed.

**Reduced-motion result:** Static storyboard is the complete result.

## Genre & spine

Timeline/state-carrying recurrence with a subordinate convolution comparison. Time is the drawn horizontal axis; no animation is required.

## Figure trigger (EXPLAIN.md)

- **SHAPE/structure** — state cells keep identical size while time grows.
- **FLOW/routing** — old state and current input jointly create next state; state creates output.
- **CHANGE over steps** — three different inputs evolve the carried state, shown as static ordered columns.

## (a) Entity inventory — name everything BEFORE drawing

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | actors / participants | n/a — math mechanism |
| WHAT-1 | data items with identity | inputs `x₁=1,x₂=0,x₃=2` |
| WHAT-2 | computed / derived results | states `2,1,4.5`; outputs `6,3,13.5`; kernel `6,3,1.5` |
| WHAT-3 | running state | `hₜ`, same-size carried register |
| WHAT-4 | persistent structure + invariant | state register; fixed size regardless of sequence length |
| WHERE-1 | substrate / resource tiers | n/a — no hardware hierarchy |
| WHERE-2 | layout / addressing rule | timestep column `t` aligns input, state, output, and convolution result |
| WHEN-1 | ordered phases | for each t: scale old state; scale input; add; read out |
| WHEN-2 | concurrency lanes / timeline | one column per timestep |
| WHEN-3 | before → after snapshots | `hₜ₋₁ → hₜ` inside each column |
| HOW-1 | algorithm over the structure | sequential fold across three timesteps |
| HOW-2 | protocol / message alphabet | n/a — local math |
| WHY-1 | quantities / complexity | `O(1)` state per inference step; caption-only |
| WHY-2 | failure / edge branch | zero input at t=2 still carries a decayed echo |
| WHY-3 | trade-off comparison | n/a — recurrence/convolution is an exact identity |
| ANCHOR-1 | worked numeric instance | `A=.5,B=2,C=3,D=0,x=[1,0,2],h₀=0` |
| ANCHOR-2 | composition refs | neural-network weights may supply A/B/C/D; not drawn internally |

| element | type | drawn as | level / role |
|---|---|---|---|
| inputs | scalar example of vectors | teal cells | per-column co-input |
| states | scalar example of vectors | equal coral registers | recurrence spine |
| outputs | scalar example of vectors | gold cells | readout row |
| kernel | scalar lag weights | gold strip | convolution proof |
| calculations | equations | directly beneath their cells | exact derivation |

## (b) Dynamics — routing / shape evolution

Static persistent arrows show `hₜ₋₁` and `xₜ` feeding each next-state equation. Vertical readout arrows connect each state to its output. No values move; time is already unfolded spatially.

## (c) Static storyboard panels in DAG order

Three columns labeled STEP 1/3 through STEP 3/3. Each shows `xₜ`, the full `hₜ` arithmetic, and `yₜ`. A bottom convolution band derives `k=[6,3,1.5]` and reproduces all three outputs.

## (d) Color — ONE identity dimension + ONE accent

Identity dimension is data role: teal inputs, coral state, gold output/kernel. The zero-input echo at `h₂` gets the one gold accent ring. Labels and vertical row position redundantly encode roles.

## (e) Worked instance carried to the visible answer

`h₁=.5(0)+2(1)=2,y₁=3(2)=6`; `h₂=.5(2)+2(0)=1,y₂=3`; `h₃=.5(1)+2(2)=4.5,y₃=13.5`. Kernel `k=[CB,CAB,CA²B]=[6,3,1.5]` reproduces `[6,3,13.5]` by causal convolution.

## (f) Stays as caption / text

General vector/matrix dimensions, `O(n)` total cost, attention comparison, Mamba extensions, and direct term `D xₜ` (zero here) remain in prose or one short header note.
