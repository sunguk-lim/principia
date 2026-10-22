# Transformer FLOP Estimation

## Meaning

FLOPs count arithmetic work under a stated convention. They do not directly report latency, energy, or memory use.

## Mechanism

Count matrix multiplies using their dimensions. With two FLOPs per multiply-add, a dense layer's projection and feed-forward leading terms are $8nd^2+4ndf$, with roughly $4n^2d$ for attention scores and value mixing. During KV-cached decode, one new token compares against the existing prefix rather than recomputing the whole attention matrix. Backward passes and optimizer updates add training work beyond forward inference.

## One example

Doubling sequence length roughly doubles projection work but can quadruple dense prefill attention work. If a kernel computes dense scores and masks most of them afterward, a sparse *mask* alone does not deliver sparse arithmetic.

## Check your understanding

**Question:** Can a lower FLOP estimate make a system slower? **Answer:** Yes. Irregular memory accesses, launch overhead, padding, or insufficient accelerator utilization can dominate.

## Shape and execution boundary

With ideal one-read FP16 inputs and weights, a 1×1024 by 1024×1024 multiply has about 0.998 FLOP/byte. Stacking 128 known input rows raises the idealized value to 102.4 by amortizing the weight read. [[arithmetic-intensity]] describes this reuse, not a latency guarantee. Profile actual traffic, tile use, launches and matched-quality tokens/s; increasing batch size can also increase latency and memory.
