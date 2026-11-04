# Layer Normalization

## Meaning

Layer normalization centers and rescales the features of one activation vector, then applies learned feature-wise gain and offset. Its statistics are local to that vector rather than computed across the examples in a batch. It therefore does not need other examples to define its training or inference normalization.

## Mechanism

For a vector with d features, compute the average feature value and the average squared deviation from that average. Subtract the average from each coordinate, then divide by the square root of the variance plus a small positive epsilon. Finally multiply each coordinate by its learned gain and add its learned offset. Epsilon keeps the denominator defined when the vector has no feature variation. Gain and offset allow useful output scales and shifts instead of permanently forcing all features into one standardized output range.

The normalized axes are part of the contract. Normalizing one token's channel vector differs from combining tokens or examples in the statistics. Holding the vector and parameters fixed while changing unrelated batch members should not change this operation's result. That locality does not establish that an entire network is unaffected by all batching decisions.

## One example

Take x=(2,4,6). The mean is 4 and the squared deviations are 4, 0 and 4, giving variance 8/3. Ignoring a tiny epsilon for this example, divide deviations (-2,0,2) by the square root of 8/3 to obtain approximately (-1.225,0,1.225). Gains (2,1,1) and offsets (1,0,-1) produce approximately (-1.449,0,0.225). The normalization removed a shared shift and scale, but learned parameters deliberately restored unequal feature ranges.

## Check your understanding

Must a constant input vector produce an all-zero final output? No. Its centered values are zero, but learned offsets may be nonzero. Inspect normalized axes, epsilon and numerical precision; normalization alone does not guarantee stable training or make different placements in a network equivalent.
