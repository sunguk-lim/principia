# Quantized Lora Training

## Meaning

**Quantized LoRA training** stores a frozen pretrained model in low precision and trains only low-rank adapter weights. It is useful when full-precision base weights would consume too much accelerator memory, but a claimed “single-GPU fit” remains dependent on sequence length, image tokens, batch size, optimizer state, and runtime implementation.

## Mechanism

[[lora]] avoids updating most base parameters. [[quantization]] reduces the bytes used to store those frozen parameters. The forward pass uses the low-precision base plus the trainable adapter; the gradient path updates adapter parameters, not quantized base weights. In QLoRA-style methods, compute may occur in a higher precision than storage, so [[mixed-precision-training]] and numerical stability still matter.

A memory budget must account separately for quantized weights and metadata, adapter weights and optimizer state, activations, image or text tokens, temporary kernels, and safety headroom. Offloading selected components to CPU can lower peak GPU memory but add transfer latency. A model that loads successfully may still fail on a long example during backward propagation. Rank, target modules, gradient accumulation, checkpointing, and batch shape all change the trade-off.

## One example

A model loads in 4-bit storage and trains low-rank adapters, yet backward activations on long image-text examples still exhaust GPU memory.

## Check your understanding

**Question:** Does fitting base weights prove the training run fits?

**Answer:** No. Activations, adapters, optimizer, runtime, and headroom also need memory.
