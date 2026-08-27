# Figure spec — `three-dimensional-parallelism`

## Visual teaching contract

- **Audience:** An engineer who already knows data, pipeline, and tensor parallelism separately.
- **Single job:** Make orthogonal nesting, multiplication, and communication-aware placement visible in one structure.
- **Visual thesis:** TP partitions matrices and communicates every layer on the fastest inner links; PP partitions the layer stack and exchanges adjacent activations/gradients; DP replicates the whole TP×PP structure and synchronizes once per step on outer links.
- **Traced object:** One amber GPU coordinate: tensor shard 7, pipeline stage 0, data replica 0.
- **Signature moment:** The final equation counts the visible nested groups: `8 × 4 × 2 = 64`.

**Comprehension test:** The reader should point to what each axis partitions, derive the GPU count, and match TP/PP/DP traffic frequency to inner/adjacent/outer links.

**Rendered constraints:** Static 720×720 canvas; hierarchy is encoded by containment and repetition, not color alone; labels remain at least 17 px.

## Communication overlay

- **TP:** one bidirectional line spans the eight shards inside every stage; this stands for frequent per-layer all-reduce on the fastest intra-node links.
- **PP:** paired downward/upward arrows occupy each adjacent stage boundary; activations move forward and gradients backward over medium links.
- **DP:** one bidirectional bridge joins the two whole replica containers; gradient synchronization occurs once per training step on outer links.

The three path styles are redundant with direct labels and spatial scope, so meaning never depends on color alone.

**Rendered critique:** Native-size inspection confirms identical bidirectional TP lines inside all eight stages, paired PP arrows only at adjacent stage boundaries, and one DP bridge between whole replicas. Frequency and relative-link labels fit, scopes match the nesting, the `8×4×2=64` equation remains dominant, and no text or paths overlap or clip.
