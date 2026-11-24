# Agent Memory

## Meaning

Agent memory retains information beyond one live [[context-window]] and selects what should return to the model later. A useful design separates what information means, where it is stored, when it changes and who may use it.

## Mechanism

A current context is bounded working information. An external store can preserve facts, episodes or procedures across contexts; [[retrieval-augmented-generation]] selects relevant records to place back into the current input. Compaction summarizes older material to keep the working context bounded, trading detail for space.

Semantic memory describes facts; episodic memory describes particular experiences; procedural memory describes how to act. Those labels do not dictate storage. Procedures can live in reviewed prompts or code, while learned weights can contain factual associations. With [[fine-tuning]], demonstrations update model behavior, but a particular rule is not necessarily an individually editable record with a reliable citation or deletion path.

External records offer explicit versions and provenance, but can still be stale, badly retrieved or ignored. Decide placement using update frequency, access control, auditability, cost and held-out performance. A procedure can change as readily as a fact, so “train skills, retrieve facts” is a heuristic to test, not a universal law.

## One example

An invented support assistant must know today's return window and how to process a return. Put the changing window in an approved versioned record. Express the workflow in trusted code, examples or tuned behavior, but still check current order eligibility before acting.

A successful past interaction is not automatically a durable procedure. Promotion should check support, scope, duplication and retention rights, then add, update, defer or discard the candidate. Keep provenance so later corrections can supersede stale entries.

## Check your understanding

Does retrieval guarantee that the agent follows the current rule? No. Retrieval supplies evidence; current authority, generation behavior and execution checks remain distinct. Evaluate changed rules, failed recall, unauthorized reuse and corrections, not only similarity scores.
