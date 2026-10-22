# Backpropagation Through Time

## Meaning

Backpropagation through time (BPTT) is differentiation of a recurrent model after exposing each time step as a separate operation. The weights are shared across those operations, so learning must sum their contributions. Unrolling creates distinct intermediate states, not distinct trainable copies of the same weight.

## Mechanism

For a [[recurrent-neural-network]], let h_t=F(h_(t-1),x_t,θ), with shared parameter vector θ and total scalar loss L equal to the sum of per-step losses. The [[chain-rule]] propagates sensitivities from later losses through earlier transitions. At each occurrence of θ, compute its local contribution and add it into the same [[gradient]] accumulator. A reverse traversal also adds direct loss at a state to influence arriving from its future consumers.

Exact differentiation requires the relevant forward intermediate values. Saving all states consumes memory that grows with sequence length. Recomputing some values trades additional operations for lower retained memory. Truncated BPTT instead stops the derivative path across selected temporal boundaries; preserving the forward state does not preserve the omitted gradient path. The truncated result is generally not the exact full-sequence gradient.

## Worked example

Use a scalar linear recurrence h_t=w h_(t-1)+x_t, h_0=1, inputs x_1=2 and x_2=3, shared w=2, and loss L=h_2²/2. Forward values are h_1=4, h_2=11 and L=60.5. The final loss derivative is dL/dh_2=11. The second occurrence of w contributes 11h_1=44. Propagating to h_1 gives 11w=22; the first occurrence contributes 22h_0=22. The shared derivative is 44+22=66.

Direct expansion h_2=w²+2w+3 gives dh_2/dw=2w+2=6 and dL/dw=11×6=66, confirming the reverse traversal. If the h_1 boundary is detached, only the second occurrence contributes and the answer is 44. That may be an intentional memory/training choice, but it changes the credit assignment. Validate gradients on short sequences with analytic or finite-difference checks before testing long runs.

## Check your understanding

**Question:** Should the two time steps update separate w parameters? **Answer:** No. They contribute to one shared parameter's gradient.
