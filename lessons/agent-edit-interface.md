# Agent Edit Interface

## Meaning

An agent edit interface is the contract between a coding model's proposed change and an actual file mutation. Shell access gives capability, but the application must still decide which file may change, whether the proposal matches current contents, and how failure is reported.

## Mechanism

One option is exact search-and-replace: accept a path, old text, and new text as structured arguments. Count the old-text occurrences. Apply only when the count is exactly one; otherwise leave the file untouched and return the count. A file version or hash can reject edits based on stale reads. Show a diff after a successful change so the agent can inspect what happened.

Contextual patches are another legitimate interface. They can describe several changes at once and Git can check them before application. They may fail when context drifts; exact replacement may fail when text repeats. Choose by measured task outcomes, not by declaring one format universally best.

## One example

A configuration contains `retries = 3` twice. A replacement request targeting only that text returns “2 matches; no write.” The agent reads more context and submits a unique block around the intended setting. A subsequent test checks behavior; successful replacement alone is not proof of correctness.

## Check your understanding

**Question:** Why reject a non-unique replacement? **Answer:** Because applying it would leave the target ambiguous; rejection preserves the file and gives the agent actionable feedback.
