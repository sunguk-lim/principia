# GPU Allocation Fragmentation

## Meaning

Free GPU bytes are not always usable for the next allocation. A caching allocator may hold memory in blocks that do not satisfy a new request; live tensors and external processes are separate constraints.

## Mechanism

Compare live tensor bytes with allocator-reserved bytes, then inspect the failing request and peak allocation trace. A large reserved-minus-allocated gap suggests investigating fragmentation but is not proof. Releasing cached blocks cannot free tensors still in use. Keep model, shapes, and microbatch fixed when testing allocator changes.

## One example

A training step succeeds at one sequence length but fails on a longer example. The checkpoint is unchanged; activations and transient workspaces have grown, and the allocator may have split reservations. Profile the peak before changing settings.

## Check your understanding

**Question:** Will an empty-cache call make a model that exceeds physical memory fit? **Answer:** No. It only releases unoccupied cached reservations.
