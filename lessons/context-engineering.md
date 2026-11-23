# Context Engineering

## Meaning

Context engineering manages what a model sees at each inference step: trusted instructions, tool definitions, conversation state, retrieved evidence and observations. It is broader than rewriting an instruction and broader than one retrieval algorithm. The objective is sufficient, current, authorized information for the next decision—not the shortest prompt or the largest possible context.

## Mechanism

Separate input classes by origin and authority before choosing their representation. The [[agent-execution-harness]] owns tool permissions and execution state; model-visible text does not grant those permissions. Keep a compact account of the current goal, known state, unresolved questions and evidence references, then retrieve detailed permitted evidence when the next decision requires it.

[[effective-context-utilization]] distinguishes available tokens from information actually used. A longer input can increase evidence coverage or introduce distraction and contradictions. Choose context by measured task utility and keep important negative evidence, not only passages supporting the current plan. [[lossy-context-compaction]] explains the trade when older details become a summary: preserve recoverable origin references and explicit uncertainty rather than inventing complete memory.

## One example

An invented 1,200-token total limit reserves 300 for output, leaving 900 for input. The proposed input allocates 200 to instructions, 100 to tool contracts, 200 to current task state, 300 to evidence and 100 to the new request: 900 in total. These are toy counts, not a recommended universal ratio.

If the decisive evidence requires 500 tokens, blindly truncating it to 300 can invalidate the task. Reclaim redundant history, retrieve a better bounded span, split the decision into recoverable steps or state that the present budget is insufficient. Keep the relevant source revision and contradiction. A smaller prompt that drops the decisive exception is not a successful optimization.

At the next turn, the evidence or tool state may change. Rebuild the packet from current authorized observations rather than append every historical tool output forever. A cached summary is a view with a freshness obligation, not a new authority.

## Check your understanding

Is moving all old messages into a summary sufficient context engineering? No. The next decision still needs current state, applicable evidence and enforced authority boundaries.
