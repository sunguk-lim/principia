# Gated Recurrent Unit

## Meaning

A gated recurrent unit (GRU) is a [[recurrent-neural-network]] whose update gate chooses how much previous hidden state to retain and whose reset gate controls how the previous state influences candidate content. It carries one hidden-state vector rather than defining a separate retained cell vector and exposed hidden vector.

## Mechanism

Let $x_t$ be the input at position $t$, $h_{t-1}$ the previous width-$d$ state, and $r_t,z_t$ two width-$d$ gates with coordinates between zero and one. Learned affine maps of input and prior state followed by $\sigma(a)=1/(1+e^{-a})$ produce the reset gate $r_t$ and update gate $z_t$. Here $e$ denotes the natural exponential's base. In the PyTorch convention, the candidate $n_t$ and new state are

$$n_t=\tanh(W_{in}x_t+b_{in}+r_t\odot(W_{hn}h_{t-1}+b_{hn})),\qquad h_t=(1-z_t)\odot n_t+z_t\odot h_{t-1}.$$

The input matrix $W_{in}$ maps input width to $d$; the recurrent matrix $W_{hn}$ is $d\times d$; each bias $b$ has width $d$; $\odot$ multiplies coordinates. Tanh bounds each candidate coordinate between minus one and one. The gate $z_t$ close to one retains state in this convention; some descriptions reverse the naming or mixture convention, so verify equations before moving weights or interpreting a gate plot.

The direct retained-state derivative with gates held fixed contains $z_t$, but the gates and candidate also depend on past state. [[recurrent-gradient-stability]] therefore still depends on full derivative products. Gating provides a controllable path, not an unconditional cure for every long-range optimization failure. Reset placement also matters: masking a recurrent projection is not generally the same as projecting an already masked state.

## One example

For a single coordinate, take old state $0.8$, candidate $-0.2$, and update gate $0.75$. The candidate contributes $0.25\times(-0.2)=-0.05$ while retention contributes $0.75\times0.8=0.6$. The new value is $0.55$. Reducing the gate to $0.25$ gives $0.75\times(-0.2)+0.25\times0.8=0.05$: the same candidate now has more influence.

Compare gate saturation, delayed recall, state/gradient norms, parameter count, latency, and memory at matched task quality. Fewer carried vectors or gates do not automatically establish lower total service cost or superior quality.

## Check your understanding

Does a large update gate always mean a large overwrite? No. Under the equations above it weights retention; check the exact implementation's convention.
