# Agent Task Cost

## Meaning

Agent task cost asks how much an entire attempted task consumes, rather than how many tokens occur in one prompt. A task can include model calls, tools, verification, summaries and recovery. Local savings matter only if they survive this complete accounting boundary.

## Mechanism

First choose the task cohort and a concrete completion rule. For every attempt, sum the actual priced categories on every model call, including cache reads, cache creation, new input and output. Include the summarizer and any billed retry, not only the final successful call. Add tool or runtime charges without double counting shared services. Report resources that lack a monetary conversion separately.

There are two useful denominators. Divide total cohort cost by attempts to measure cost per attempt. Divide the same total, including failed attempts, by successful outcomes to measure cost per success. Always show success rate too. Omitting failed runs from the numerator makes an unreliable system look cheap. If there are no successes, a success-normalized ratio is undefined.

Specify whether retries are independent attempts or part of one task's fixed retry policy. Otherwise two systems can appear comparable while receiving different opportunities to finish.

## One example

A handles 100 issues for $0.08 each and resolves 80. Total spending is $8, so cost per success is $0.10. B reduces its main call to $0.05, but summaries and recovery add $0.03 per issue. It also spends $8, while resolving 64 issues. Its cost per success is $0.125. The local main-call saving did not survive the complete workflow.

The numbers are illustrative. Traces must establish whether extra work actually came from missing summary details, cache misses or some other cause.

## Check your understanding

Can the average prompt shrink while cost per successful issue increases? **Yes.** More calls, changed prices or fewer valid successes can outweigh the saving. Inspect both resource use and outcomes on matched tasks.
