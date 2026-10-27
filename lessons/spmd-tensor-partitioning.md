# SPMD Tensor Partitioning

## Meaning

Single-program-multiple-data (SPMD) tensor partitioning runs the same generated program on several devices, each holding a different slice of global tensor data. Its objective is to preserve the meaning of a global [[computation-graph]] while distributing storage and work. “Same program” does not mean identical local values or no communication.

## Mechanism

Start with global tensor shapes and layout annotations describing which dimensions are divided and which values are replicated. For each global operation, derive a local operation on the device's slice. If the local data is insufficient, insert the required exchange or combination. All devices can execute the same instruction sequence while their device indices select different slices.

A sum along a partitioned dimension needs results from more than one device. An [[all-reduce]] can add those local partial sums and return the global result to each participating device. A sum over a dimension kept entirely local does not need that same collective. Thus communication follows the operation and layout together, not simply the number of devices. Layout changes between operations can introduce extra movement even if each local arithmetic operation is efficient.

## Worked example

Take a global dot product with x=[1,2,3,4] and w=[2,1,1,2]. Its result is 1*2+2*1+3*1+4*2=15. Split the four-element contracting dimension evenly over two devices. Device 0 holds x=[1,2], w=[2,1] and computes partial sum 4. Device 1 holds x=[3,4], w=[1,2] and computes 11. Both run the same local multiply-and-sum program, then an all-reduce adds 4+11=15. Returning either local sum alone would change the global program's meaning. If the result is needed only on one device, a different output-layout contract could avoid replicating it everywhere.

## Check your understanding

Can dividing the inputs always eliminate communication? No. Partitioning the contracting dimension of this dot product creates partial results that must be combined to recover the global output.
