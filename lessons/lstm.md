# Long Short-Term Memory

## Meaning

A long short-term memory network (LSTM) is a [[recurrent-neural-network]] with two carried vectors: a cell state for retained content and a hidden state exposed to the next computation. Its defining mechanism is a gated additive cell update, not simply a different activation in a vanilla recurrence.

## Mechanism

At sequence position $t$, let $x_t$ be the input, $h_{t-1}$ the previous hidden vector, and $c_{t-1}$ the previous cell vector, both carried vectors of width $d$. Learned affine maps of $(x_t,h_{t-1})$ produce input, forget, and output gates $i_t,f_t,o_t$ and candidate content $g_t$. Gates use the elementwise sigmoid $\sigma(z)=1/(1+e^{-z})$, giving values between zero and one; the candidate uses $\tanh(z)$, bounded between minus one and one. Here $e$ is the base of the natural exponential. With $\odot$ meaning coordinatewise multiplication,

$$c_t=f_t\odot c_{t-1}+i_t\odot g_t,\qquad h_t=o_t\odot\tanh(c_t).$$

The forget gate scales retained content; the input gate scales a proposed write; the output gate controls exposure. A cell can retain content without exposing all of it at every position. This separates storage from the visible state.

For [[recurrent-gradient-stability]], the direct cell-to-cell derivative with gate values held fixed is $\operatorname{diag}(f_t)$. A near-one forget gate can preserve this route across many steps. This is a partial path, not the full coupled derivative: gates depend on previous hidden state, and output nonlinearities introduce other paths. Gates near zero can erase content; LSTMs do not guarantee arbitrarily long useful memory or eliminate exploding gradients everywhere.

## One example

For one coordinate take $c_{t-1}=2$, $f_t=0.8$, $i_t=0.25$, $g_t=-0.4$, and $o_t=0.6$. Retention contributes $0.8\times2=1.6$ and the new write contributes $0.25\times(-0.4)=-0.1$. Thus $c_t=1.5$ and $h_t=0.6\tanh(1.5)\approx0.543$. None of the retention, write, or exposure operations disappears in this example. The cell is not itself constrained to the range of tanh.

With the same forget value across ten steps, the direct retained-cell sensitivity is $0.8^{10}\approx0.107$, not one. Inspect state and gradient norms by temporal distance, gate saturation, delayed-recall quality, and runtime/memory cost. Compare a vanilla or other gated recurrence under matched training conditions. More gates add parameter and execution cost; their usefulness depends on the task.

## Check your understanding

Does an additive cell route guarantee an unchanged gradient? No. Forget gates can attenuate it, and the full recurrent system contains additional derivative paths.
