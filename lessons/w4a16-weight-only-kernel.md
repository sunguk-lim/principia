# W4A16 Weight-Only Kernel

## Meaning

W4A16 describes four-bit stored weights and sixteen-bit activations. A compatible kernel turns packed weight codes into the multiplication the model requires. Choosing the codes is [[quantization]]; efficiently consuming the resulting representation is the kernel's separate job.

## Mechanism

A [[cuda-kernel]] loads packed codes and scale metadata, reconstructs the values for a small matrix region, and multiplies them with activation values. A [[tensor-core]] can consume an appropriate reconstructed format. Four-bit storage is therefore not a promise of native four-bit arithmetic or a fixed accumulator format.

Reconstructing near the arithmetic can avoid writing an entire expanded weight matrix to main memory. Bit extraction, scale traffic, conversions and reductions still cost time. Codes and scales often need a kernel-specific arrangement. A checkpoint's advertised bit width alone is not an interoperability contract.

## One example

Codes [-2, 6] with scale 0.5 reconstruct [-1, 3]. Multiplying by activation [1, 2] gives -1 + 6 = 5. A second row [4, -4] at the same scale reconstructs [2, -2] and yields 2 - 4 = -2. Check the kernel against these reconstructed-weight results before evaluating the model's approximation error relative to original weights.

For 128 weights, four-bit codes use 512 bits. A sixteen-bit scale brings the group to 528 bits. The original sixteen-bit representation uses 2048 bits, so weight storage shrinks by about 3.88 times, not exactly four. Other metadata can reduce that further.

## Check your understanding

Why can the smaller representation fail to accelerate inference? The [[roofline-model]] may identify a different bottleneck; unpacking, unsupported shapes or service overhead may consume the saving. Measure the exact workload at matched numerical and task quality rather than converting a storage ratio into a token-rate promise.
