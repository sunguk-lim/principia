# Looped Transformer

## Meaning

A looped Transformer applies the same learned block repeatedly across depth. The block contains [[transformer-attention]] and usually other transformations, including a [[residual-connection]]. Sharing parameters separates the number of stored weight tensors from the number of times those tensors are applied.

## Mechanism

Let $E$ be an encoded input sequence, $H_0$ an initial hidden-state array, $F_\theta$ a shared block with parameter set $\theta$, and $K$ the chosen number of iterations. Compute

$$H_{k+1}=F_\theta(H_k,E),\qquad k=0,\ldots,K-1.$$

A prediction head reads $H_K$. Some designs reinject $E$ every iteration; others use step information or different state initialization. These details are architecture choices, not consequences of parameter sharing alone. The same function can produce a new result because its state input changes. Calling a deterministic function repeatedly on an identical state would not do that.

The iteration index $k$ is computational depth, not token position. With a causal attention mask, known sequence positions can be processed together within each iteration, while the iterations themselves depend on earlier states. Generating new tokens introduces a separate autoregressive dependency. Increasing $K$ changes execution without changing stored weights, but it still costs operations and elapsed time.

## One example

Suppose a fixed prelude has two layers, a shared core has three, and a fixed output stage has one. Four core iterations execute $2+4\times3+1=15$ layer applications while storing six distinct layer parameter sets. Seven iterations execute 24 applications with the same six sets. This arithmetic counts transformations, not equal-cost FLOPs across unlike layers.

Evaluate quality and latency across depth, both inside and outside the training range, and inspect state growth, repeated-state cycles, and stopping failures. Compare with an untied model and explicit reasoning-token generation at matched useful quality and total compute. A parameter-count comparison alone cannot establish serving efficiency.

## Check your understanding

Does drawing four copies of a shared block imply four independently trained weight sets? No. It represents four applications of the same parameters to successive states.
