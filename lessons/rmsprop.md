# RMSprop

## Meaning

RMSprop makes the scale history used by [[gradient-descent]] forget old observations. It divides each coordinate's gradient by a running root-mean-square scale. This changes effective steps without storing a full matrix or directly estimating the Hessian.

## Mechanism

Let g_t be one coordinate's gradient, v_t its square average, alpha a decay between zero and one, eta the learning rate and epsilon a positive stabilizer. The uncentered, no-momentum form is

$$v_t=\alpha v_{t-1}+(1-\alpha)g_t^2,\qquad
\theta_t=\theta_{t-1}-\eta g_t/(\sqrt{v_t}+\epsilon).$$

The new square gets weight 1-alpha; a square k updates old gets an additional alpha^k factor. Thus the denominator can fall when recent gradients become smaller. This differs from accumulating all past squares. A large alpha responds slowly to a changed scale; a small alpha is responsive but noisy. PyTorch places epsilon after the square root, while the documentation notes that TensorFlow uses a different convention. Centered scaling and momentum are additional variants, not invisible details.

## One example

Take theta=2, eta=0.1, epsilon=0.01, alpha=0.5 and v_previous=4. With gradient 2, the new average is 0.5*4+0.5*4=4; the decrement is 0.2/2.01, about 0.09950. If the next gradient is -1, the average becomes 0.5*4+0.5*1=2.5 and the update increases the parameter by 0.1/(sqrt(2.5)+0.01), about 0.06285. The state decreased even though it remained positive.

## Check your understanding

Does v estimate second derivatives? No: it averages squared first derivatives. Validate learning rate, decay, epsilon and initialization together, especially early in training and after distribution changes. Include optimizer-state memory and actual kernel execution in comparisons; smoothing a noisy scale is not a convergence or speed guarantee.
