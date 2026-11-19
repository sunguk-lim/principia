# Block Diffusion Language Model

## Meaning

A block diffusion language model divides a sequence into blocks, generates those blocks in order and performs denoising within the current block. It combines the within-block parallel prediction of a [[masked-diffusion-language-model]] with an across-block dependency order. The learning objective is distinct from merely shortening the number of denoising steps in a full-sequence sampler.

## Mechanism

A [[decoder-only-transformer]] ordinarily preserves earlier token states because causal attention prevents them from reading future tokens. A [[kv-cache]] can reuse those stable keys and values. Fully bidirectional denoising can instead change a position's representation when another position changes—even if the first position's token stays fixed. A frozen token ID is not proof that all of its layer states are reusable.

In a block-autoregressive construction, tokens in a completed block do not depend on later blocks. Within the active block, positions can use bidirectional information while denoising; across blocks, the attention and training contract maintain the declared causal order. Completed-block state can then be cached while active-block state is recomputed as required. The Block Diffusion paper and author implementation provide a primary example with explicit block size and a cache-enabled sampler. This does not license arbitrary cache reuse in another diffusion architecture.

Block size changes the trade-off. Small blocks expose less within-step parallel work but more often finalize a reusable prefix; larger blocks permit more joint prediction but can repeat more computation and complicate length or stopping policy. Block-by-block generation also supports extending the sequence beyond one initially masked output region, subject to the model and implementation's supported context.

## One example

Consider two blocks of four output positions. After completing positions 1–4, a block-causal model can retain their state while denoising 5–8. Revising position 6 may change other active-block representations, so those states cannot automatically be reused. If the attention mask instead allowed positions 1–4 to read 5–8, their old cached states could become invalid too. The mask and dependency graph—not the name “diffusion”—settle validity.

## Check your understanding

Do fewer denoising steps guarantee faster text generation? No. Each step's width, recomputation, cache behavior and quality matter. Compare cached and uncached execution under the same architecture, seed and sampler contract; test block boundaries, masks, stopping, long outputs and numerical tolerances. Report wall time, memory, model evaluations and task quality against matched autoregressive and full-sequence diffusion baselines. The paper's own benchmark results remain conditional on its setup.
