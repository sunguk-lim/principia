# SmoothQuant Activation Smoothing

## Meaning

SmoothQuant makes activation quantization less difficult by moving large input-channel magnitudes into corresponding weights. It does not change the exact linear function before rounding. Its purpose differs from weight-only compression: both operands must remain manageable for the intended lower-precision matrix execution.

## Mechanism

For a column input x and weight matrix W, choose positive channel scales in diagonal matrix S. Replace the input by S inverse times x and the weights by WS. Multiplying gives WS times S inverse times x, which equals Wx because each scale cancels. After quantizing both transformed operands, this exact cancellation no longer removes rounding error.

Calibration observes representative activation maxima and weight magnitudes per input channel. A smoothing parameter controls how much range is transferred. Too little leaves activation outliers difficult; too much makes weights harder to quantize. The calibration sample must represent deployment inputs, and settings must be checked on separate held-out tasks.

## One example

With input [20,2] and weights [0.5,3], the output is 16. Divide input channels by [5,2], obtaining [4,1], and multiply matching weights by [5,2], obtaining [2.5,6]. Their product is still 16. The largest activation fell from 20 to 4 while the largest weight rose from 3 to 6: the difficulty moved rather than vanished.

A coarse activation grid can still change the answer. With scale 4/3, transformed input 1 rounds to 4/3. Even exact transformed weights then produce 18, not 16. This is an intentionally coarse teaching example, not a measured W8A8 result.

## Check your understanding

Does exact rescaling prove exact quantized inference? **No.** Validate equivalence before rounding, then reconstruction and task error afterward. Finally measure the supported kernel on the actual hardware and shapes; a smoothing identity alone proves no speedup.
