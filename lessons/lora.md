# LoRA (Low-Rank Adaptation)

## Meaning

LoRA adapts a pretrained model by keeping its original weight matrix fixed and training a low-rank update. It reduces trainable parameters when the needed change can be represented with two narrow matrices.

## Mechanism

From [[low-rank-factorization]], write the update as `ΔW = B·A`, with rank much smaller than the weight dimensions. [[fine-tuning]] adjusts `A` and `B`; the base weight remains frozen. In a transformer, these updates can be attached to linear projections used by [[transformer-attention]] and other layers.

## One example

Serve one base model with two task adapters. If an adapter is merged into the weight, its extra matrix multiplication disappears for that deployed copy. If the runtime switches unmerged adapters per request, it may avoid duplicating the base model but perform extra work. Measure both routes at the same precision, batch size, and request mix.

## Check your understanding

**Question:** Does LoRA always add zero inference latency? **Answer:** No. A merged adapter can have no extra low-rank operation, but an unmerged adapter route may incur runtime overhead; actual cost depends on serving design.
