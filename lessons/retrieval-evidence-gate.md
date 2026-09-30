# Retrieval Evidence Gate

A search result can be about the right topic yet fail to answer the question. In retrieval-augmented generation, the first retrieval stage selects candidate passages using lexical or vector similarity. An evidence gate then checks which passages contain supporting facts and whether the retained group is sufficient for an answer. If the first stage never found a supporting passage, a later reranker cannot invent it.

Suppose a user asks, “What is the cancellation deadline for my plan?” A page about cancellation fees may score highly because it uses the same words, but it may say nothing about the deadline. Another passage may specify a deadline yet omit which plan it applies to. A useful gate checks passage-level support and set-level sufficiency separately. The application can then ask for a plan name, retrieve more evidence, or abstain rather than make up a date.

Test this stage with labeled questions and supporting passages. Measure first-stage recall, how often the gate accidentally removes decisive evidence, final answer faithfulness, abstention, latency, and cost. Calibrate any probability scores on held-out cases; a score is not automatically a reliable confidence. Compare against a no-gate baseline and a conventional reranker. Packing many judgments into one request may reduce overhead, but that must be measured for the actual workload.

Keep quality control separate from security. A model's “not prompt injection” score cannot authorize the passage; access control must have happened before retrieval, and the passage remains untrusted when shown to the generator.

**Understanding check:** Why can a high reranking score not repair a first-stage search that omitted the only policy page containing the deadline?
