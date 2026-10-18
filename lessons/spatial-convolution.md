# Spatial Convolution

## Meaning

A spatial convolution reuses one local filter at many grid locations. Each output depends on a neighborhood rather than the whole image, giving a local, weight-sharing computation.

## Mechanism

An input [[tensor]] has channels and spatial coordinates. Each output location takes a weighted sum over a chosen window and its input channels, plus an optional bias. [[matrix-multiplication]] describes the same local weighted sums after arranging windows into rows, although an implementation need not materialize that arrangement. Stride sets how far the window moves, padding defines boundary values, and dilation spaces its sampled positions. Deep-learning libraries commonly implement cross-correlation without reversing the filter; it is conventionally called convolution. Grouped filters restrict channel connections. In depthwise convolution, each input channel is filtered separately, optionally producing several outputs per input channel; a later channel projection can mix them.

## One example

Take a one-channel 3×3 grid with rows (1,2,3), (4,5,6), (7,8,9). A 2×2 filter with rows (1,0), (0,2), stride one, and no padding gives a 2×2 output. Its upper-left value is 1+2×5=11; upper-right is 2+2×6=14; lower-left is 4+2×8=20; lower-right is 5+2×9=23. The same filter weights act at every location, but different neighborhoods produce different outputs. Padding changes edge behavior and may reveal position. Check output dimensions, channel grouping, boundary values, and numerical agreement before benchmarking an optimized kernel.

## Check your understanding

Does a depthwise filter mix information between channels? Not in the filter itself: it mixes spatial neighbors within each channel. A separate projection supplies cross-channel mixing.
