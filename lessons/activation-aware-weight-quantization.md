# Activation-Aware Weight Quantization

## Meaning

**Goal:** explain how input-channel rescaling can change quantization error without changing the original layer function.

AWQ is weight-only [[post-training-quantization]] guided by representative activations. A weight's importance depends partly on the input multiplying it. “Activation-aware” therefore describes how the transformation is chosen, not a requirement that activations themselves use the low-bit weight format.

## Mechanism

For column input $x$ and weight matrix $W$, choose positive channel scales in a diagonal matrix $S$. The identity $Wx=(WS)(S^{-1}x)$ preserves the unquantized [[matrix-multiplication]]. Quantizing $WS$ changes rounding behavior; multiplying the input by the inverse scales compensates for the transformation, not for every rounding error.

Large-activation channels can be protected with suitable scales, but scaling one channel may enlarge a shared quantization range and hurt others. The reference implementation searches candidate scales and measures calibration output differences. Compatible transformations can be folded into neighboring operations. Scaling only the weights without compensating the input changes the model even before quantization.

## One example

Two input coordinates commonly have magnitudes $10$ and $0.1$. The same weight error, $0.02$, contributes approximately $0.2$ and $0.002$ to the output. Equal weight errors therefore need not be equally important. That observation motivates activation-aware scaling, but it does not prescribe an unlimited scale for the first channel.

## Check your understanding

Is an AWQ model guaranteed to be faster because its weights use four bits?

**Answer:** no. Compare against equal-bit unscaled rounding, then measure held-out task quality, memory including scales, packing compatibility, and actual target-kernel latency and throughput. Test equivalence before rounding and inspect errors afterward. Calibration examples and deployment inputs may differ.

Reference: [AWQ paper](https://arxiv.org/abs/2306.00978).
