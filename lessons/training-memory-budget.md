# Training Memory Budget

## Meaning

Training memory is not the checkpoint file size. It is the peak coexistence of weights, gradients, optimizer state, activations, temporary work, and runtime reservations.

## Mechanism

For a mixed-precision Adam run, one may have low-precision weights, an FP32 master copy, gradients, and two moment arrays. Their exact byte counts depend on implementation. Activations grow with sequence length and microbatch; [[activation-checkpointing]] reduces what is stored by recomputing part of the forward pass. Sharding partitions state across devices. Allocator-reserved memory can exceed live tensor memory, so measure both.

Profile the actual optimizer, shapes, hardware, and precision. Change one lever at a time while keeping effective batch and quality criteria fixed. A headline “bytes per parameter” estimate is a starting bound, not a proof of fit.

## One example

A 3-GB 16-bit checkpoint can require much more than 3 GB for training because gradients and Adam states coexist with activations. Reducing microbatch or checkpointing layers may fit the run, but both change runtime and must be measured.

## Check your understanding

**Question:** Why can a model load for inference yet fail to train? **Answer:** Training retains gradients, optimizer state, and backward activations that inference does not.
