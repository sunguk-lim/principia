# Normalizing Flow

## Meaning

A normalizing flow builds a flexible probability distribution by applying invertible, differentiable transformations to samples from a simple distribution. Invertibility lets a data point be mapped back to its base point; volume accounting supplies its density.

## Mechanism

For a base random vector z with density p_Z and an invertible map x=f(z), [[change-of-variables]] gives p_X(x)=p_Z(f^{-1}(x)) |det Df^{-1}(x)|. Here Df is the derivative matrix of f and det its volume-scaling factor. A sequence of maps composes expressive transformations while log-density corrections add. A [[neural-network]] may predict the transformation coefficients, but an unconstrained neural function is not automatically invertible or cheap to evaluate in both directions. Discrete flows often choose maps with tractable inverses and determinants. Continuous flows use a differential equation and a corresponding density-evolution calculation; learning a vector field by flow matching is a training construction, not a synonym for every flow architecture.

## One example

In one dimension let x=2z+3 with base density p_Z(z)=0.25 at z=1. The point maps to x=5, the inverse is (x-3)/2, and its derivative is 1/2. Therefore p_X(5)=0.25/2=0.125: expanding lengths by two halves density, preserving probability mass. A second map y=3x-1 maps 5 to 14 and divides density by three again, giving 1/24. Check inverse reconstruction and density normalization on tractable examples before trusting a trained system. Flexible densities trade off against restricted maps, inverse cost, and numerical conditioning.

## Check your understanding

Can the determinant correction be omitted because samples look plausible? No. Sampling behavior and correct density evaluation are separate properties; omitting volume change generally gives a wrong likelihood.
