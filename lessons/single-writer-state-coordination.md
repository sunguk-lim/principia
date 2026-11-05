# Single-Writer State Coordination

## Meaning

Single-writer coordination gives one owner the authority to change a particular state partition. Other participants send proposed changes instead of editing independent copies. It is an ownership protocol, not the claim that only one participant may read or compute.

## Mechanism

An owner receives commands through a [[queue]], checks each against its current state and commits a valid transition before handling the next mutation. This avoids a lost update caused by two writers reading one value and overwriting each other's results. [[atomic-operation]] explains the indivisibility boundary; serial command handling supplies one ordering without requiring every worker to coordinate every read-modify-write step.

Akka's actor documentation provides a concrete example: each actor handles messages sequentially while different actors run concurrently. The useful property is exclusive access to that actor's internal state. An asynchronous callback or external writer that mutates the same data outside the protocol can break it. Read replicas may also lag, so stale observations must not override the owner without a version check.

## One example

A task is `ready`, version 4. Two workers propose `claim(task, expected_version=4)`. The owner processes A first, records `running, owner=A, version=5`, then rejects B's stale proposal. B must refresh rather than overwrite A. A later completion must name the task, attempt and relevant version; merely receiving the word “done” is not enough.

Serialization does not guarantee persistence or exactly-once effects. If the owner acknowledges before durable recording, a crash can lose the accepted transition. Duplicate commands still need stable identities, and a remote action can succeed even if its acknowledgement is lost. Restart and ownership transfer must restore state and prevent an old owner from continuing writes. A second live owner defeats the central assumption.

Partition ownership when one writer becomes a bottleneck, but define how operations spanning partitions coordinate. Measure queue delay and availability, and test duplicate delivery, stale versions, restart and overlapping owners. Single-writer simplicity trades away some write parallelism.

## Check your understanding

Can every worker safely write its own complete board snapshot? No. That bypasses the authoritative owner and can overwrite changes that were not in the snapshot.
