# Lossy Context Compaction

## Meaning

Lossy context compaction replaces detailed history with a smaller representation that cannot preserve every original detail. It helps an agent work within a bounded context window, but a summary is useful only if it retains the state needed for later decisions.

## Mechanism

Separate three things: the live working state, exact evidence that must survive, and history that can be retrieved later. A compact record should distinguish what was observed from what the model inferred. Keep completed steps, unresolved effects, exact paths or record identifiers, important constraints and uncertainty. Stable references let a later step inspect omitted details without pretending the summary is complete.

A summary can be fluent and still be operationally harmful. Dropping a failed-test location can force another search; dropping a successful check can cause repeated work; dropping a rejected hypothesis can send the agent down the same dead end. Conversely, retaining every old result defeats the purpose of compaction. Decide according to the task, not a universal instruction to keep everything.

Detailed session records also serve recovery and tool-call reconciliation. A natural-language summary should not be the only proof that an external action finished. Summarizing external instructions does not turn them into trusted instructions.

## One example

The original result reports that test T failed at alpha.py line 28 and beta.py passed. The summary says only “a parser test failed.” A later worker must search both files and repeat checks. A structured note keeps `T failed, alpha.py:28`, `beta.py passed`, and a reference to the original result. It is slightly longer but preserves the next decision's evidence.

## Freshness boundary

Recovering an old observation differs from repeating a tool action. Retrieve a 09:00 report when asked what it said; obtain fresh evidence when asked whether the service is healthy now. Bind an artifact to its tool inputs, observation time, version and access scope. If a payment request timed out, an absent local receipt does not prove that no payment occurred. Reconcile under the remote retry contract before repeating an effect.

## Check your understanding

Is the shortest faithful-sounding summary necessarily the best compaction? **No.** Test downstream completion and recovery. Important details may become necessary only later. Compare structured notes, raw windows and recoverable originals under the same task and resource budget.
