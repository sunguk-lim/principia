# Roofline Model

## Meaning

The roofline model is a performance envelope, not a promise of actual speed. It compares the maximum compatible arithmetic rate with the rate that memory traffic can support. A point below the envelope still needs diagnosis.

## Mechanism

Define work W in operations and traffic D in bytes at one memory level. Their ratio I=W/D is [[arithmetic-intensity]]. If compute ceiling is P operations per second and bandwidth is B bytes per second, the modeled rate is at most min(P, B*I). Arithmetic needs at least W/P seconds and transfer needs at least D/B seconds; even ideal overlap cannot beat the larger time requirement.

The [[memory-hierarchy]] matters: cache traffic must use a cache-level bandwidth, while main-memory traffic uses main-memory bandwidth. Match the numeric format, sparsity and operation-count convention to the compute ceiling. Otherwise the plotted comparison mixes incompatible quantities.

## One example

With hypothetical compute of 100 trillion operations/s and bandwidth of 3 trillion bytes/s, the ridge is 33.3 operations/byte. Adding two four-byte values and writing one uses 12 bytes per operation. Its bandwidth ceiling is 0.25 trillion operations/s. If the measurement is only 0.05 trillion, the kernel is five times below that roof. Dependencies, insufficient parallel work, access inefficiency or launch overhead could explain the gap; its position left of the ridge does not prove saturated bandwidth.

## Check your understanding

Does a high-intensity kernel require faster hardware to improve? Not necessarily. If its achieved point is below the compute ceiling, better tiling, parallelism or instruction use may help. First identify the gap using matched work and traffic, then verify whether the kernel matters to the complete application.
