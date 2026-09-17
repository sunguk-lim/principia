# LLM Inference Memory Budget

## Meaning

A model fitting in VRAM does not mean its serving workload fits. Plan for five allocations that may coexist:

$$M_{required}=M_{weights}+M_{KV}+M_{temporary}+M_{runtime}+M_{headroom}.$$

Weights are mostly fixed. The [[kv-cache]] grows with cached tokens and active sequences. Temporary workspace peaks with the phase, batch, and kernels. Runtime libraries and caching allocators reserve additional memory. Headroom protects against fragmentation and traffic variation.

## Mechanism

For a dense KV cache, use the estimate

$$M_{KV}=2LTH_{kv}D_hCB,$$

where the factor 2 counts keys and values; $L$ is layers, $T$ cached tokens per sequence, $H_{kv}$ KV heads, $D_h$ head width, $C$ concurrent sequences, and $B$ bytes per value. [[paged-attention]] reduces wasted or duplicated blocks but does not remove the live data. [[post-training-quantization]] reduces weight bytes, while [[prefill-vs-decode]] explains why temporary peaks differ between prompt processing and generation.

## One example

An 8-billion-parameter model budgeted at 16 GiB for 16-bit weights runs with 32 layers, 4096 cached tokens, 8 KV heads, head width 128, 16 active sequences, and 2-byte KV values. Its KV estimate is 8 GiB. Add 3 GiB temporary workspace, 1.5 GiB runtime reservation, and 3 GiB headroom: the total is 31.5 GiB on a 40-GiB GPU.

Doubling context to 8192 tokens doubles only the KV term, producing a 39.5-GiB total. The weights still fit, but the workload no longer has safe capacity.

## Check your understanding

**Question:** If concurrency doubles while every other variable stays fixed, which term changes first, and by how much?

**Answer:** The dense KV-cache term doubles because it is linear in active sequences $C$. Temporary workspace may also change under the real scheduler, so confirm the estimate with a warmed-up peak-memory measurement.
