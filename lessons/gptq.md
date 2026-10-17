# GPTQ Weight Quantization

## Meaning

**Goal:** explain why quantization error can be compensated using representative layer inputs.

GPTQ is a [[post-training-quantization]] method that tries to preserve layer outputs, rather than rounding every stored weight independently. It uses calibration inputs, but it does not require their task labels or ordinary full-model gradient training. The target is a local reconstruction objective, not a guarantee of unchanged behavior on every task.

## Mechanism

Let weight matrix $W$ act on calibration columns $X$. Original outputs are $WX$, a [[matrix-multiplication]]. GPTQ seeks quantized weights $\widehat W$ keeping the entries of $(W-\widehat W)X$ small. The [[hessian]] of this squared-error objective is proportional to $XX^\top$ for each weight row.

That curvature describes input sensitivities and relationships. GPTQ rounds a column, then adjusts remaining unquantized columns to compensate for some resulting output error. Blockwise updates make the work practical. Damping improves numerical robustness when calibration directions are poorly represented. Neither compensation nor damping guarantees that the calibration sample represents future inputs.

## One example

A scalar output is $w_1x_1+w_2x_2$. Suppose calibration inputs have $x_2=x_1$. Rounding $w_1$ down by $0.1$ can be compensated locally by increasing still-free $w_2$ by $0.1$. If deployment instead has $x_2=0$, that compensation does not cancel the first error. Later rounding of $w_2$ can also introduce additional error.

## Check your understanding

Why is a low calibration reconstruction error insufficient to accept a GPTQ deployment?

**Answer:** it measures a surrogate on specific inputs. Check held-out task quality and domain changes, plus conversion time, peak memory, and real inference speed. Compare equal-bit simple rounding and use kernels compatible with the packed checkpoint. Fewer stored bits alone are not evidence of faster execution.

Reference: [GPTQ paper](https://arxiv.org/abs/2210.17323).
