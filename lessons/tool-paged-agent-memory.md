# Tool-Paged Agent Memory

## Meaning

Tool-paged memory makes reading more history an explicit agent action. A finite context holds the evidence currently available to the model; an external store can hold much more. The agent requests a small page, examines its evidence and decides whether another read is needed. This is different from always injecting the top fifty records.

## Mechanism

A search tool returns bounded records, their stable references and a continuation cursor. The application validates the request and permission scope; the model cannot grant itself access by naming a namespace. After a page arrives, the agent can continue, reformulate its search or answer. Every path obeys call, token and time limits. A cursor signals possible continuation, not guaranteed useful evidence.

Keep space for the next result and the answer. Earlier detail can be removed from live input while retaining permitted references for recovery. Summaries must preserve uncertainty and conflicts. External evidence remains data rather than instructions, and every continued read must honor current permissions. MemGPT illustrates this function-driven control loop; it does not give the underlying model infinite attention.

## One example

A 1,000-token input limit has 400 tokens of instructions and task state. Two 250-token pages fit in the remaining 600, leaving 100 tokens of headroom. The first page supplies an old deadline; the second supplies a later correction. The answer must use the applicable correction while retaining its origin. A third full page cannot simply be appended: something must be reclaimed or the read narrowed.

## Check your understanding

Does a searchable archive guarantee that the agent will find a fact on page ten? No. It might stop early, choose the wrong query or exhaust its budget. Compare paged access with fixed and reranked retrieval at equal budgets; test later-page evidence, duplicate results, revoked permissions and stale cursors. Measure task success as well as extra tool calls.
