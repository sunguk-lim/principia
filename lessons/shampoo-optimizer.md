# Shampoo Optimizer

## Meaning

Shampoo preserves the shape of a parameter matrix while transforming its gradient. It keeps one square statistic per matrix axis rather than one huge statistic for every pair of flattened parameter coordinates. This captures cross-coordinate structure that elementwise scaling cannot represent, while introducing matrix computations and extra storage.

## Mechanism

Let W and gradient G be m-by-n matrices. Define L as an m-by-m row statistic and R as an n-by-n column statistic, initialized with positive damping times identity. One original accumulated-statistic form updates L=L_previous+G*G transpose and R=R_previous+G transpose*G. With learning rate eta, use

$$W_{new}=W-\eta L^{-1/4}G R^{-1/4}.$$

[[symmetric-eigendecomposition]] explains the matrix inverse powers; they are not entrywise powers. [[gradient-descent]] supplies the underlying loss-directed step. Storing L and R requires m^2+n^2 values instead of m^2*n^2 for a full flattened statistic. This can still be expensive for large axes. Blocking, exponential averaging, momentum, refresh cadence and magnitude matching produce implementation variants; do not silently substitute their formulas for the original one.

## One example

Consider a state with L=diag(16,81), R=diag(1,16) and G=[[2,4],[3,6]]. L^(-1/4)=diag(1/2,1/3), and R^(-1/4)=diag(1,1/2). The transformed gradient is [[1,1],[1,1]]. Each entry's divisor combines its row and column scales. This chosen diagonal-state example makes arithmetic visible; general L and R have off-diagonal entries and can also mix coordinates.

## Check your understanding

Are these gradient-statistic matrices the exact Hessian? No. Matrix preconditioning need not be exact curvature. Check positive damping, decomposition accuracy, refresh cost and large-axis memory. Compare actual time-to-quality, not just steps, under tuned baselines. A theoretical result for stochastic convex optimization does not automatically guarantee convergence or speedup for a particular deep-network workload.
