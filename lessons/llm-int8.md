# LLM.int8 Mixed-Precision Decomposition

## Meaning

**Goal:** explain how separating a few outlier feature dimensions protects the rest of an 8-bit product.

Large activations can force a shared quantization range to become coarse for ordinary values. LLM.int8 combines vector-wise [[post-training-quantization]] for most dimensions with a higher-precision path for selected outliers. The relevant distinction is between [[numeric-precision-formats]], not a claim that training must occur.

## Mechanism

Let $X$ have shape $n\times d$ and $W$ shape $d\times r$. Their [[matrix-multiplication]] contracts the $d$ feature dimension. Divide those indices into outlier set $O$ and remaining set $N$. Then $XW=X_{:,N}W_{N,:}+X_{:,O}W_{O,:}$ exactly before approximation.

The first term uses vector-wise 8-bit quantization, with separate scales for activation rows and weight columns. The outlier term uses higher precision. Combining them preserves the decomposition; discarding outliers would instead remove part of the mathematical product. Threshold choice trades error against the amount of extra higher-precision work and conversion overhead.

## One example

For activation row $[1,2,100]$ and weight column $[3,4,5]^\top$, isolate the final coordinate. The ordinary contribution is $1\cdot3+2\cdot4=11$, and the outlier contribution is $100\cdot5=500$. They sum to $511$. The ordinary path no longer needs an activation range covering $100$, although its own quantization can still introduce error.

## Check your understanding

Should every large coordinate be moved to the higher-precision path?

**Answer:** not without measuring the trade-off. Too many selected dimensions can erode compression and increase execution overhead. Evaluate held-out quality, outlier prevalence, peak memory, and batch-dependent throughput on the real runtime. A paper's measured preservation of quality is not a universal guarantee.

Reference: [LLM.int8 paper](https://arxiv.org/abs/2208.07339).
