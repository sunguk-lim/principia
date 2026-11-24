# Parallel Transformer Block

## Meaning

A parallel Transformer block lets its attention and feedforward branches read the same input state, then adds their updates. The word “parallel” names the dependency structure. It does not guarantee execution on separate devices or simultaneous GPU scheduling.

## Mechanism

Let x be the token-state array and N its [[layer-normalization]]. Let A be [[transformer-attention]] and F the [[position-wise-feed-forward-network]], each returning the same shape as x. The block computes y=x+A(N(x))+F(N(x)). The [[residual-connection]] carries x into the output while both branches contribute updates.

A common serial block instead computes u=x+A(N(x)), then y=u+F(N(u)). Its feedforward branch needs the attention-updated state u. Removing this dependency generally changes the function, so converting arbitrary serial pretrained weights is not an exact implementation optimization.

The shared branch input may permit combined input projections or a shorter execution path. Attention, nonlinear activation and output combination still have real costs. Hardware scheduling, matrix shape and intermediate memory determine whether the implementation benefits. Architecture and projection fusion are different decisions.

## One example

Use scalar stand-ins only to expose the dependency: normalization is the identity, x=2, A(t)=3t and F(t)=t². The parallel form returns 2+6+4=12. The serial form first obtains u=8, then returns 8+64=72. These are not trained attention computations; they are a non-degenerate counterexample to universal equivalence.

For actual models, compare fused and unfused implementations of the same parallel equation for numerical agreement. Compare serial and parallel architectures separately after appropriate training at matched budgets.

## Check your understanding

Can two execution streams remove a serial branch's mathematical dependency? No. Scheduling cannot make the needed updated state exist earlier. Verify normalization placement, branch shapes, scaling and measured latency rather than assuming that more apparent concurrency guarantees speed.
