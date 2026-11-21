# Mini-Batch K-Means

## Meaning

Mini-batch k-means targets the squared-distance clustering objective while updating after small batches instead of waiting for a complete Lloyd assignment pass. It changes the optimization trajectory, not the definition of a meaningful real-world cluster.

## Mechanism

Begin with the centroids and nearest-centroid assignments of [[k-means-clustering]]. Sample a batch, assign its points using the current centroids, and update each touched centroid from the assigned observations. One standard streaming-mean update tracks a cumulative count n and mean c. After a new assigned point x, n becomes n+1 and c becomes c+(x-c)/n, using the new n. Batch implementations can combine equivalent sums and counts. Over many updates, an old high-count centroid changes more slowly.

This cumulative mean is not the same as replacing a centroid with the current batch mean or using a fixed exponential decay. Those rules weight history differently. Sampling order and centroid movement also mean that old assignments need not remain nearest under the final centers. Reassign the evaluation data when reporting final distortion or labels. Initialization, low-count reassignment and stopping criteria belong to the chosen implementation.

## One example

A one-dimensional centroid represents two prior assigned points with mean 4. The next assigned point is 10. Updating the count to 3 gives c=4+(10-4)/3=6. Replacing the centroid with 10 would forget earlier points; averaging 4 and 10 equally would give 7 and underweight the earlier two observations. If a competing center moves meanwhile, a final nearest-center pass can change which points belong here.

## Boundaries and check your understanding

Smaller batches can provide cheaper frequent progress but noisier directions, weaker device utilization and worse final distortion. Compare time to a declared distortion target and downstream utility, not only update count or epochs. Use held-out samples, repeated initializations, representative geometry and explicit memory/timing boundaries. Test tiny or duplicate datasets, skewed cluster sizes and batches that touch no member of some cluster.

**Check:** Does optimizing the same objective guarantee the same partition as Lloyd's algorithm? No. Initialization, stochastic batches and nonconvex optimization can lead to different local solutions.
