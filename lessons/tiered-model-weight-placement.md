# Tiered Model-Weight Placement

## Meaning

Tiered weight placement keeps model parameters in different memory tiers and arranges for each operator's weights to be available where that operator executes. Unlike loading a checkpoint progressively, it can require transfers during repeated forward passes. Unlike moving attention history, the retained objects are model parameters shared across requests.

## Mechanism

Construct a placement map and an execution schedule. Resident parameters remain on the device; offloaded parameters may be staged from storage through host memory and transferred to an accelerator before their layer runs. Release or retain them afterward according to the residency policy. Hugging Face Accelerate documents device maps and execution hooks that implement these paths. Its documented capacity-first mapping is not a guarantee of optimal inference throughput or automatic prefetch.

The [[llm-inference-memory-budget]] includes more than stored weights: active attention state, activations and temporary transfer buffers also need room. [[gpu-data-flow]] makes transfer ordering part of correctness; a kernel cannot read weights before the copy completes or after their storage is reclaimed. The [[memory-hierarchy]] explains the trade: slower tiers expand capacity while adding service time. Dense layers may need the same offloaded weights on every token step; sparse activation can have different reuse.

## One example

Suppose an invented model needs 30 GiB of parameter storage, while only 20 GiB is available for weights after reserving runtime state. Offload 10 GiB to host memory. If every decode iteration needs those 10 GiB and the transfer path sustains 20 GiB/s, transfer service alone takes at least 0.5 seconds per iteration. An additional 2 GiB staging buffer still needs a budget. These assumptions do not describe an overlapped critical path: useful prefetch or reuse may reduce exposed wait, while contention can increase it.

## Check your understanding

Does storing ten GiB outside the GPU imply those bytes are read only once? No. Their reuse and placement schedule determine how often they cross the transfer path.
