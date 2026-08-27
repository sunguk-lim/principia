# Figure spec — `laplacian` (Step 0)

> Derived from `nodes/laplacian.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader who knows partial derivatives but wants intuition for the Laplacian.

**Single job:** Connect the continuous operator to a neighbor stencil, its sign, and one diffusion update.

**Visual thesis:** The Laplacian measures whether a point sits above or below its neighbors; diffusion moves the value in the direction that reduces that curvature.

**Traced object:** Center value `8` among four neighbors `4`, producing `∇²f≈−16` and then `6.4` after a rate-0.1 diffusion step.

**Subject visual vocabulary:** Continuous formula, five-point grid stencil, center/neighbor contrast, signed curvature, and smoothing arrow.

**Signature moment:** `16−32=−16` directly turns the hot center `8` into `6.4`.

**Anti-template test:** The center-minus-neighbor stencil and signed diffusion update specifically encode the Laplacian rather than a generic derivative pipeline.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | scalar neighborhood | cross-shaped five-point stencil |
| **Contrast** | center versus neighbors | warm center and cool neighbor cells with direct values |
| **Quantity** | discrete approximation | neighbor sum minus four times center |
| **Sign** | peak/flat/pit meaning | direct sign labels |
| **Change** | diffusion consequence | attached `8 → 6.4` smoothing step |

**Progressive disclosure:** First view shows a hot center surrounded by cooler neighbors. Arithmetic then names the negative curvature, and the final arrow shows why diffusion cools the peak.

**Comprehension test:** The reader can calculate `−16`, identify a local peak, and explain why the diffusion update lowers 8 toward 4.

**First-view constraints:** 720 px canvas; essential labels at least 15 px; static figure; continuous and discrete formulas clearly distinguished by `=` versus `≈`.

**Plan critique:** The former figure correctly expanded `∇·∇` but began with context-dependent “Yes —” and never visualized the neighbor-average intuition that motivates heat flow and smoothing.

**Rendered critique:** Native-size inspection confirms that the continuous formula fits, the five-point stencil is immediately legible, and `16−32=−16` is directly identified as a local peak. The attached `8 + 0.1×(−16) = 6.4` arrow makes diffusion concrete; the sign legend fits; and no text overlaps or clips.

**Reduced-motion result:** Static figure; no motion required.

## Genre & spine

Worked mechanism. The spine is continuous definition → local stencil → signed result → diffusion update.

## Figure trigger

- **SHAPE:** a center and its four axial neighbors.
- **QUANTITY:** curvature comes from a signed local difference.
- **CHANGE:** diffusion updates the center toward its neighborhood.

## Dynamics

The static arrow shows one explicit-Euler diffusion step `f_new=f+α∇²f` with `α=0.1`. It is a single worked consequence, not an animation.

## Worked instance

North, south, east, and west are all 4; center is 8; grid spacing is 1. The five-point Laplacian is `4+4+4+4−4×8=−16`, so one rate-0.1 step yields `8−1.6=6.4`.

## Caption/text

Keep the exact continuous formula, discrete approximation, and sign legend on canvas. Higher-dimensional discretization details remain in prose.
