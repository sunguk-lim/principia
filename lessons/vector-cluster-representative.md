# Vector Cluster Representative

## Meaning

A group of vectors can be represented by one summary vector for a cheap first-stage comparison. The representative is not the same as every member or a promise that its score bounds every member’s score. This distinction matters whenever a group is discarded before its individual records are examined.

## Mechanism

For n vectors x_1 through x_n of equal dimension, a centroid is their coordinatewise mean c=(x_1+...+x_n)/n. If only direction matters, an implementation can normalize the sum or mean to unit length when it is nonzero. Let q be a query vector. [[vector-dot-product]] scores q against c or its normalized direction. The choice changes the score: normalizing removes representative magnitude, while an unnormalized mean retains cancellation and scale.

How members were grouped is a separate algorithmic decision. K-means repeatedly updates arithmetic centroids; other methods build groups bottom-up or use fixed assignments. LSA’s primary design uses normalized sums for bucket representatives after bounded bottom-up grouping, not Lloyd’s K-means updates. A representative plus a member-position table lets a selected group expand back into its original records.

## One example

Take x_1=[1,0] and x_2=[0,1]. Their mean is [0.5,0.5], and the normalized mean is [1/sqrt(2),1/sqrt(2)]. For q=[1,0], the individual dot products are 1 and 0, the mean score is 0.5 and the normalized representative score is about 0.7071. A threshold of 0.8 on the normalized representative would reject the group despite a member scoring 1. This is why coarse selection can miss a relevant member.

## Check your understanding

Can every nonempty group be normalized safely? No. Opposite vectors [1,0] and [-1,0] have a zero mean. Define fallback handling, outlier limits and group sizes, then measure member recall after coarse pruning. A useful representative reduces search work; it does not make the summary lossless or guarantee that a chosen grouping algorithm is suitable.
