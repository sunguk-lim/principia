# Bounded and Unbounded Data Processing

## Meaning

A bounded input has a known finite extent for the computation. An unbounded input can continue growing without an end known to that computation. This distinction is about the input contract, not its size: a very large daily snapshot can be bounded, while a slow stream of occasional events can be unbounded.

## Mechanism

[[distributed-dataframe-execution]] can partition either kind of input. For a bounded sum, processing the complete specified input provides a natural completion point. For an unbounded sum, waiting for every future item never finishes. A service must instead define a finite query scope or publish updates under an explicit policy.

Apache Beam uses a unified collection model for both cases. A common unbounded aggregation groups events into time windows. Event time is the timestamp associated with an occurrence; processing time is when the system handles it. They can differ because events are delayed or arrive out of order. A watermark estimates progress in event time; it is not a universal guarantee that no older event can appear. A trigger decides when an intermediate or later result is emitted. These are supporting completion policies, not evidence that continuous processing always has lower total cost.

## One example

A fictional log export defines all records included in yesterday's completed snapshot. It contains 3 TB but can be processed as bounded data by tomorrow's deadline. A monitoring service receiving one event each minute has an ongoing input and needs a policy for when a five-minute count is emitted. An event timestamped 10:04 that arrives at 10:08 may revise a previously emitted window, be sent to a late-data path, or be discarded under a stated rule. Calling the system “streaming” does not choose that rule.

Micro-batching is an execution technique and can implement an ongoing logical computation. Conversely, chunking a finite file for memory safety does not make its input logically unbounded. Choose from delivery latency, correction requirements, state size and operational cost, not data volume alone.

## Check your understanding

Does a daily arrival schedule imply an unbounded computation? No. Define the dataset boundary and whether later records revise prior results. Test late and duplicate events, replay, finality rules and state growth against the declared contract.
