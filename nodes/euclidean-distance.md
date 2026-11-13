---
id: euclidean-distance
title: Euclidean Distance
summary: Euclidean distance measures straight-line separation between coordinate vectors as the square root of the sum of squared coordinate differences.
type: concept
tags: [math/linear-algebra]
prereqs: [vector-dot-product]
sources: [https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.euclidean.html]
status: explained
created: 2026-11-14
updated: 2026-11-14
---

# Euclidean Distance

## Meaning

For two vectors x and y with d real coordinates in the same units and coordinate system, Euclidean distance is their straight-line separation. It is a scalar, not another coordinate vector.

## Mechanism

Let u=x-y be the coordinate displacement. The [[vector-dot-product]] u dot u sums the squared coordinate differences. Define the Euclidean norm of u, written ||u||_2, as the nonnegative square root of that sum. Then

$$d(x,y)=\|x-y\|_2=\sqrt{\sum_{j=1}^{d}(x_j-y_j)^2}.$$

Here j indexes a coordinate and d is the number of coordinates; d(x,y) denotes distance rather than the dimension. The squared form avoids taking a square root when comparing distortion ratios, but squared distance and distance are different quantities with different units. Squaring each component prevents opposite signs from canceling. Taking the root returns to the original coordinate units.

## One example

For x=(1,2,3) and y=(4,6,3), displacement is (-3,-4,0). Squared separation is 9+16+0=25, giving distance 5. The zero third difference contributes no separation; both nonzero differences matter. Swapping x and y changes the signs, not the result.

Scaling every coordinate by two doubles the distance and quadruples squared distance. Scaling only one coordinate changes the geometry: converting one measured feature's units without adjusting the others can change which samples are nearest. Compare coordinates only after deciding what their units and relative scales should mean.

## Check your understanding

If squared separation changes from 25 to 30, did distance increase by 20 percent? No. Squared separation did; distance changes from 5 to sqrt(30), about 5.477, or roughly 9.5 percent.

## Prerequisites

- [[vector-dot-product]]

## Sources

- <https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.euclidean.html>
