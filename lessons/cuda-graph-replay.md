# CUDA Graph Replay for Inference

## Meaning

CUDA graph replay reduces recurring host submission work for a compatible device-operation sequence. It records work structure, not the result of a model forward pass. Every replay still executes the kernels on current input data.

## Mechanism

Warm up eagerly to establish initialization and allocations, then capture eligible work with the framework's documented stream ordering. Retain input and output storage: replay uses captured pointers, so rebinding a variable to a different tensor does not update those pointers. Copy new data into stable buffers before replay and wait appropriately before consuming or overwriting output. CPU logic is not automatically replayed.

PyTorch's ordinary replay path expects compatible shapes and arguments. CUDA's lower-level graph-update APIs can change supported parameters under compatibility rules; they do not make arbitrary topology changes free. Handle update failure with re-instantiation or eager fallback. Multiple shape buckets exchange preparation time and graph memory for better request coverage; padding also spends device work.

For changing LLM state, update supported token, position and cache metadata inside retained buffers. Full capture replays the whole compatible path; piecewise capture leaves unsupported regions eager and replays safe regions around them. A batch dispatcher chooses an actually compatible captured variant or eager fallback. Compilation and capture are different mechanisms, and backend support is version-specific.

## One example

Assume a measured eager interval takes 120 microseconds: 80 of device work plus 40 of attributable gaps. Replay takes 88: the same 80 plus 8 of gaps. The saving is 32 microseconds. An 8,000-microsecond preparation cost is recovered after 250 replays; more than 250 is needed for a net win under those fixed assumptions. Include copies, synchronization and output handling in both measured paths. These are toy timings, not a universal speedup.

## Check your understanding

**Question:** Does replaying on new inputs reuse old predictions? **Answer:** No, it reruns the recorded work. Profile launch gaps and compare eager/replay at matched model, shape, precision and quality. If long device kernels dominate the request, removing small host gaps has limited headroom. Report actual bucket coverage, memory and cold-start cost alongside steady-state latency.
