# Kernel Feature Map

## Meaning

A feature map transforms an input into coordinates in which a dot product computes a chosen similarity. It is a representation of a kernel, not a promise that every similarity has a small exact representation or that the transformed coordinates must be larger than the original input.

## Mechanism

Use the following symbols before forming the equation:

| Symbol | Type and meaning |
| --- | --- |
| $x,y$ | Input vectors, each with $d$ real coordinates |
| $\phi(x),\phi(y)$ | Transformed vectors with $m$ real coordinates in a finite explicit map |
| $k(x,y)$ | Scalar similarity computed from the inputs |

With [[vector-dot-product]], an exact finite map satisfies

$$k(x,y)=\phi(x)^\top\phi(y).$$

Any real-valued explicit map defines a positive-semidefinite Gram matrix: for inputs $x_i$ and real coefficients $a_i$, the sum $\sum_{i,j}a_i a_j k(x_i,x_j)$ equals the squared length of $\sum_i a_i\phi(x_i)$, which cannot be negative. This condition is different from requiring every pairwise kernel value to be positive. An ordinary dot product can be negative for one pair while its Gram matrix still has this property. An exact representation for a general kernel need not be finite-dimensional.

## One example

For two-coordinate inputs define $\phi(x)=(x_1^2,\sqrt{2}x_1x_2,x_2^2)$. Its transformed dot product expands to $x_1^2y_1^2+2x_1x_2y_1y_2+x_2^2y_2^2=(x_1y_1+x_2y_2)^2$. Thus the three-coordinate map exactly represents the homogeneous degree-two polynomial kernel.

Take $x=(1,2)$ and $y=(3,1)$. The original dot product is $3+2=5$, so the kernel is 25. The mapped vectors are $(1,2\sqrt{2},4)$ and $(9,3\sqrt{2},1)$; their dot product is $9+12+4=25$. The interaction coordinate accounts for the cross term; dropping its square-root-of-two scale would produce a different kernel.

## Application boundary

A nonlinear feature map does not automatically preserve softmax attention. A chosen map defines its own kernel; random features may approximate a target kernel with error. Check the exact map identity first, then separately test any approximation and its numerical normalization. Positive-semidefinite does not mean that every pairwise value is nonnegative.

## Check your understanding

**Question:** Does choosing any nonlinear map preserve softmax attention? **Answer:** No. The map defines a particular similarity; matching another kernel requires an exact identity or a justified approximation.
