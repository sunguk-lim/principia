# Cluster Fair-Share Scheduling

## Meaning

Fair sharing asks which tenant should receive the next scarce allocation, not just which individual task fits. Entitlements, demand, and actual usage all matter. A Linux CPU fair scheduler is not sufficient coverage for a cluster policy over GPU jobs and queues.

## Mechanism

A policy compares tenant allocation or historically accumulated usage with configured shares, then admits or reclaims eligible work. [[kubernetes-pod]] requests provide the accounting units. Instantaneous fairness and time-based fairness are different: a tenant can currently hold few GPUs yet have consumed many GPU-hours. Historical [[measurement]] needs a time window or decay rule. Multi-resource policies may compare each tenant’s largest normalized resource share rather than equating one CPU with one GPU. Borrowing can improve utilization when another tenant has no demand, but reclaim and minimum-runtime rules determine how quickly guarantees can be restored. Job indivisibility and topology make exact fractional shares infeasible at every instant.

## One example

Two teams share 12 GPUs with equal entitlements, six each. If A requests two and B requests ten, a work-conserving policy can grant A two and B ten. When A later requests six, B is four above its nominal share. The policy needs an explicit reclaim path or must wait for B’s jobs to finish; declaring six does not instantly free hardware. A non-preemptible eight-GPU job may make the target temporarily impossible. Evaluate queue wait, completion time, interruptions, and time-window usage by tenant as well as fleet utilization. Pin job sizes and arrival traces when comparing policies.

## Check your understanding

Is equal GPU count necessarily equal service? No: GPU type, job duration, topology, and additional resource bottlenecks differ. Define the accounting unit and fairness objective first.
