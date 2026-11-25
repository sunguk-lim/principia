# Importance-Triggered Reflection

## Meaning

An importance trigger determines *when* to consolidate memory, independently of what the consolidation infers. It accumulates the estimated significance of new events and starts synthesis after enough evidence has arrived. [[reflective-memory-consolidation]] defines the synthesis; [[memory-importance-estimation]] supplies fallible weights rather than an objectively measured amount of learning.

## Mechanism

Maintain an accumulator A and threshold T. For each newly admitted event with importance i, add i to A. When A reaches the declared boundary, schedule one bounded reflection over a defined evidence interval. After successful completion, mark the interval consumed and reset or subtract the processed amount according to the policy. The Generative Agents paper describes a threshold of 150 for its simulation; this is not an optimal default for other systems. Its public reflection module checks a countdown and resets counters after reflection.

Operational implementation needs an explicit contract for duplicate events, failures and events arriving during synthesis. Consuming a failed interval can lose learning opportunities; retrying a successful interval without a durable completion record can duplicate memories. These are application-design consequences, not reliability guarantees of the prototype. Limit call count, token use and maximum wait separately from the threshold.

## One example

In an invented system with T=12, successive new-event scores 3, 5 and 6 raise A to 3, 8 and 14. The third event crosses the threshold. A reset-to-zero policy discards the excess 2 for scheduling purposes; a subtract-12 policy retains it. Both need documentation. If another event arrives during reflection, keep its score outside the completed interval so it is not accidentally cleared.

## Check your understanding

Can raising the threshold guarantee better memories? No. It changes cadence and accumulated evidence, not the validity of an inference.
