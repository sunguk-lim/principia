# Hadamard Outlier Mixing for Quantization

## Meaning

An orthogonal Hadamard rotation mixes coordinates so one large outlier need not set the scale for an entire low-bit group. In exact arithmetic, a paired inverse transform leaves the linear operation unchanged.

## Mechanism

After quantization, rounding error remains; the benefit depends on block size, scale-sharing group, activation distribution, and kernel support. A transform can be folded into constant weights in some places, while dynamic activations may still require runtime work. Compare quality and end-to-end speed, not only reduced maxima.

## One example

For a group with one extreme value and many small values, a shared 4-bit scale gives the small values few useful integer levels. Mixing can spread that extreme across coordinates, permitting a finer effective scale.

## Check your understanding

**Question:** Does exact reversibility imply the quantized model is lossless? **Answer:** No. Quantization rounds transformed values, and execution may add overhead.
