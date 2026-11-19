# Persistent Kernel Execution

## Meaning

A persistent kernel processes multiple work units within one [[cuda-kernel]] launch rather than launching a new program for every unit. It can amortize launch or setup work and reuse selected state. Persistence describes execution lifetime; it does not imply that all model weights remain in fast storage or that an entire request needs only one launch.

## Mechanism

Launch a resource-bounded set of programs. Each program iterates over assigned rows, tiles or tasks, obtains the next work item and writes its result. The primary Triton softmax example launches a limited number of programs based on device resources and has each program process rows separated by the program-count stride. That is a concrete loop inside a resident program, not a measured whole-model implementation.

[[occupancy]] constrains how many programs can remain active. A long-lived program can consume resources needed by other requests, increase cancellation latency or serialize work that previously ran concurrently. Cross-program [[thread-synchronization]] must have an actual progress guarantee: spinning until an unscheduled block runs can deadlock when all resident resources are occupied by waiters. A work queue adds atomicity, ordering and fairness obligations.

Looping over repeated neural-network layers is one possible schedule, but identical layer shapes do not imply shared weights. Every iteration must select the correct parameters and attention state, respect dependencies and handle required communication. A compiler transformation that removes repeated control dispatch does not prove that intermediate storage fits or that weight loads disappear. The achieved gain depends on the original fraction of time spent in launch/control, not the number of layers alone.

## One example

For eight hypothetical work units, suppose separate launches each cost 2 microseconds of non-overlapped submission and 10 of useful execution. That serial baseline takes 96 microseconds. One launch looping over the same eight units would take 2+80=82 if useful execution were unchanged. This isolates at most 14 microseconds of launch saving; it does not predict a device result where submissions overlap or resource pressure changes execution.

## Check your understanding

Is persistence equivalent to recording and replaying a launch graph? No: replay reduces repeated host submission of a sequence, while persistence moves repeated work into a longer-lived device program. Fusion can combine operations inside that program, but is a separate choice. Validate results, progress, cancellation, fairness, resource use and representative latency before accepting the longer lifetime. Profile launch gaps and execution independently so removed calls are not mistaken for proportional speedups.
