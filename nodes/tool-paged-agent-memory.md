---
id: tool-paged-agent-memory
title: "Tool-Paged Agent Memory"
summary: "Tool-paged agent memory retrieves successive bounded portions of external history through validated tool calls, making context selection an explicit control-flow decision."
type: concept
tags: [ml/agents]
prereqs: [agent-memory, tool-call-execution-contract]
sources: [https://arxiv.org/html/2310.08560v2]
status: explained
created: 2026-11-27
updated: 2026-11-27
---

# Tool-Paged Agent Memory

## Meaning

Tool-paged memory lets an agent request another bounded slice of external history when its present evidence is insufficient. Unlike an automatic fixed top-k injection, the next read is an explicit action inside the task. It changes the read-control policy of [[agent-memory]], not the model's physical context capacity.

## Mechanism

Expose a search operation returning a limited result page, stable record references and a continuation cursor. The [[tool-call-execution-contract]] validates the query, permitted namespace and cursor outside the model. Append the returned evidence to live context, assess what remains unresolved, then either request another page, reformulate the search or answer with the available support. Bound total calls, returned tokens and elapsed time. A continuation cursor means more results may exist, not that they necessarily contain the answer.

The controller must budget space for both the next result and subsequent reasoning or output. When earlier pages are displaced, retain permitted source references and unresolved conflicts so they can be recovered. Searching an external archive does not make its text trusted instructions. Pagination must preserve authorization on every request, including after a cursor was issued.

MemGPT provides a primary example of function-driven movement between external storage and finite main context, with paginated retrieval and chained calls. Its virtual-context analogy is not literal unlimited attention: the model can only reason directly over the current input, and may fail to ask for the right page.

## One example

Assume a toy input budget of 1,000 tokens. Instructions and current task use 400, leaving 600 for evidence. The first page uses 250 tokens and contains records R1–R3 but no current effective date. A second 250-token page fits, leaving 100 tokens of input headroom. It contains R4, which explicitly supersedes R2. The controller retains both the correction and their provenance before answering. A third full page would require reclaiming space or changing the request; blindly appending it would violate the budget.

## Boundaries and validation

Compare fixed retrieval, reranked fixed retrieval and paged access on identical tasks and total budgets. Measure decisive-evidence recall, answer support, unnecessary calls, premature stopping and latency. Test an answer on a later page, duplicate pages, invalid or expired cursors, permission revocation and contradictory dates. The ability to continue is not proof that continuing is useful.

**Check:** Can a huge external store compensate for an agent that never requests the decisive record? No. Storage capacity and retrieval-control success are separate.

## Sources

- <https://arxiv.org/html/2310.08560v2>
