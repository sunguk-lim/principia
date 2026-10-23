# Identity-Initialized ReLU Recurrence

## Meaning

An identity-initialized rectified recurrence starts its recurrent matrix as the identity, or a scaled identity, and uses rectification $\operatorname{ReLU}(z)=\max(0,z)$ coordinatewise. It is an initialization strategy for a [[recurrent-neural-network]], not a claim that changing an activation alone solves long-range learning.

## Mechanism

Let $h_t=\operatorname{ReLU}(W_hh_{t-1}+u_t)$, where $h_t$ is a width-$d$ state, $W_h$ is a $d\times d$ shared recurrent matrix, and $u_t$ contains the projected input and bias. Start with $W_h=\alpha I$, where $I$ leaves every vector unchanged and $\alpha$ is a chosen scalar. On a coordinate with positive preactivation, the local derivative with respect to its previous value is $\alpha$. On a negative coordinate it is zero. The activation's derivative at exactly zero requires an implementation convention.

For $\alpha=1$, an uninterrupted active path has derivative one at initialization. For $0<\alpha<1$, the same path decays as $\alpha^k$ after $k$ transitions. This gives a deliberate initial memory timescale. It does not keep the matrix fixed during training, prevent an input from switching a unit off, or bound the positive forward state. [[recurrent-gradient-stability]] must still be measured on the actual learned trajectories.

## One example

Use $h_0=(2,1)$, $W_h=I$, $u_1=(-0.5,-2)$ and $u_2=(0.25,0.5)$. The first preactivation is $(1.5,-1)$, giving $h_1=(1.5,0)$. The next is $(1.75,0.5)$, giving $h_2=(1.75,0.5)$. The first coordinate retains its sensitivity through both positive transitions. The second coordinate becomes positive again, but the first transition already erased its derivative connection to its initial value. Reactivation does not reconstruct that past path.

The original IRNN study reports results on specific benchmarks. It does not establish dominance on every sequence task. Compare identity and scaled-identity initialization with other initializations and gated models at matched width, budget, sequence length, and optimizer. Log dead-coordinate fraction, forward growth, gradient norms, clipping frequency, numerical failures, and task quality across seeds. A stable initialization is a starting condition, not an invariant imposed on every training update.

## Check your understanding

If the initial recurrent matrix is identity, are all long-horizon derivatives one? No. Activation masks and subsequent parameter updates can change or cut the path.
