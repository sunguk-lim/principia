# Gated Linear Unit

## Meaning

A gated linear unit (GLU) controls the flow of a content vector with a separately learned, input-dependent gate. It is not a gated recurrent unit: a GLU does not inherently preserve recurrent state or blend old and new state across time.

## Mechanism

For input vector x with d coordinates, two learned projections produce content a and gate logits b with m coordinates each. In a dense implementation, [[matrix-multiplication]] gives a=W_a x+c_a and b=W_b x+c_b, with W_a and W_b of shape m by d and biases of length m. A convolutional implementation produces equal-shaped tensors instead. Define the scalar sigmoid sigma(t)=1/(1+exp(-t)), where exp is the [[exponential-function]]. Apply it coordinatewise and form

$$y_i=a_i\,\sigma(b_i).$$

The content path is linear in a when the gate is held fixed; the complete mapping is nonlinear because the gate depends on x. This creates an input-dependent multiplier inside a [[neural-network]]. A packed projection can return 2m coordinates and split them into the two halves. The split dimension must have even size, and the output has half its size.

## One example

Let a=[2,-3] and b=[0,1.0986123]. Sigmoid values are [1/2,3/4], approximately, because exp(-1.0986123) is approximately 1/3. The output is [1,-2.25]. The second gate attenuates a negative content value; it does not turn all outputs positive. For fixed b, the [[derivative]] of y_i with respect to a_i is sigma(b_i), so the content gradient can pass without differentiating through an activation applied directly to a_i.

## Boundaries and check

Gate saturation can still reduce gradients through b; GLU is not a universal cure for optimization. Variants replacing the gate's nonlinearity or adding output projections have different formulas and parameter budgets. Check shapes, split axes and matched parameter counts before comparing quality or speed. The gate is a learned numerical transformation, not a separate recurrent memory.


## Check your understanding

Does a sigmoid gate force positive outputs? No; it can attenuate a negative content value.
