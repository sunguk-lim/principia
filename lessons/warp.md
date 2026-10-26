# Warp

## Meaning

A warp groups 32 CUDA threads for SIMT execution on a [[streaming-multiprocessor]]. Each thread has its own logical lane and state. Instructions apply to participating lanes selected by an active mask. The group does not imply that every thread physically executes every instruction on one clock cycle.

## Mechanism

When lanes take different branches, instructions execute with different active masks. This can waste issue capacity, but the runtime cost depends on branch lengths, compiler transformations, memory behavior and other work. A simple half-and-half branch is not a universal two-times slowdown.

NVIDIA devices from compute capability 7.0 maintain per-thread execution state and support independent thread scheduling. Code cannot safely substitute an assumption of perpetual warp lockstep for documented synchronization. If threads communicate, use the correct primitive and participation mask; same-warp membership alone is not a memory-order guarantee.

## One example

In a toy serial issue model, 16 lanes take a four-step path and 16 take a twelve-step path. Useful lane-steps are 16*4 + 16*12 = 256. The full issue width across both paths has 32*16 = 512 lane-steps, so useful participation is 50%. This is accounting under explicit assumptions. It does not establish elapsed time relative to an unspecified alternative.

Regrouping similar inputs may remove some divergent issue, but data movement and changed locality can consume the saving. Compare the complete kernel, not only branch structure.

## Check your understanding

Can threads exchange data without synchronization because they belong to one warp? Not in general. Verify the target architecture, active participants and synchronization contract. Profile useful participation and stalls along with runtime before deciding whether a layout change helps.
