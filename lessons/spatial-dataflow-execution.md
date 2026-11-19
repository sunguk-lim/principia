# Spatial Dataflow Execution

## Meaning

Spatial dataflow execution places different operators of a [[computation-graph]] on different hardware resources and connects them with channels. A consumer proceeds when required values and output capacity are available. The distinguishing idea is where operations live and how values flow, not a guarantee that a particular device is faster than a programmable processor.

## Mechanism

A compiler or hardware design assigns arithmetic, storage and communication resources to stages. A producer can pass bounded pieces of an intermediate directly to a consumer rather than materializing an entire array in a distant level of the [[memory-hierarchy]]. Several stages may operate concurrently on different pieces. AMD's primary HLS example instantiates a splitter and two worker tasks connected by local streams: each task owns a distinct role, and the channels carry values between them.

The placement needs a feasible resource and rate contract. A slow consumer fills its input queue, forcing upstream work to wait; a fast consumer can starve. A bounded [[queue]] preserves ordered handoff. Finite buffers absorb a temporary mismatch, not an indefinitely higher production rate. Cyclic dependencies and poorly arranged buffering can prevent progress. [[pipeline-bottleneck-localization]] separates steady-state throughput from initial fill, final drain and synchronization. Dynamic shapes or unsupported operations may need another placement, a fallback or a different schedule.

This is broader than fusing two GPU operations into one launch: a fused program may time-share the same execution resources rather than establish separately active hardware stages. Conversely, a spatial pipeline may still read weights and retained attention state from external memory. No finite on-chip store makes every model resident, and passing intermediates locally does not eliminate capacity, interconnect or compiler constraints.

## One example

Suppose three hypothetical stages require 2, 5 and 3 microseconds per item, with independent resources, sufficient buffers and no transfer overhead. Serial execution takes 10 microseconds per item. The ideal pipeline completes its first item after 10 microseconds and thereafter one every 5, limited by the middle stage. Ten items then take 10+9×5=55 microseconds, not 20 or 50. Increasing only the last stage's speed does not improve that steady-state limit.

## Check your understanding

Can a larger buffer fix a permanent stage-rate mismatch? No. Measure per-stage rates, queue occupancy, stalls, actual transferred bytes, numerical equivalence and whole-request latency. Compare a feasible placed graph with optimized software under matched model, precision, load and system boundaries. Treat device-specific memory sizes and headline speedups as separately sourced deployment facts, not properties of dataflow itself.
