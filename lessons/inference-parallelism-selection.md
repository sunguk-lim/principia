# Inference Parallelism Selection

## Meaning

Select a parallel layout by the measured inference bottleneck, not by a fixed ranking of techniques.

## Mechanism

Replicas help independent request throughput. Tensor and pipeline partitions can fit model weights across devices but require communication or enough work to fill stages. Context partitions help long prefill or large decode KV histories. Expert placement addresses mixture-of-experts capacity and routing. These dimensions can combine, but each adds network traffic, idle work, and coordination risk.

## One example

A model fits and one replica meets latency targets, but queue delay rises at peak traffic. Add a second replica first. Tensor splitting would add collectives without addressing the real bottleneck. If the model later fails to fit, revisit tensor or pipeline partitioning using the available interconnect.

## Check your understanding

**Question:** Why is “four GPUs” not enough information to choose a layout? **Answer:** The limiting resource, model shape, link topology, request mix, and latency target determine which partition helps.

Prefill and decode can use different attention-replica and expert-group widths. Wider groups need sufficient offered load; compare their per-GPU efficiency and tail latency rather than treating a published cluster size as a minimum deployment requirement.
