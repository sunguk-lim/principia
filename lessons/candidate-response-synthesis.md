# Candidate Response Synthesis

## Meaning

A selector returns one candidate. A synthesizer may construct an answer that no candidate supplied intact. Its objective is a coherent solution under the original task constraints, not maximal inclusion of sentences. The distinction matters when useful fragments rely on incompatible assumptions.

## Mechanism

Use [[multi-agent-orchestration]] to collect bounded proposals, their assumptions, evidence and critiques. Treat them as fallible inputs. Identify the task's acceptance conditions, resolve conflicting claims against evidence, choose compatible components, then verify the resulting whole through an [[agent-verification-loop]]. A critique is evidence to examine, not an automatic instruction to modify the answer. When one candidate already satisfies the contract, keeping it can be better than synthesis.

Mixture-of-Agents is a primary example of conditioning a model on other models' responses. Its layered design motivates this mechanism; its benchmark results do not establish that any arbitrary aggregator improves any task. A stronger aggregator and a better synthesis contract are separate interventions.

## One example

Suppose an original scheduling problem requires completing jobs A and B under a six-unit capacity. Proposal one assigns A four units and B one; it meets capacity but violates B's two-unit minimum. Proposal two assigns A three and B three; it meets both minimums but gives up a separately required fourth unit for A. Copying the locally attractive allocations A=4 and B=3 uses seven units and fails. A synthesis A=4, B=2 uses six and meets both minimums. The acceptance check is arithmetic and the declared constraints, not whether the paragraph sounds comprehensive. If evidence instead requires B=3, there is no feasible combination under six; report the conflict rather than invent capacity.

## Check your understanding

Is high copying necessarily a bad synthesis? No. An existing correct proof or tested implementation may need no rewrite. Compare direct selection, a deployable verifier or reranker, and synthesis on identical candidate pools. Track correctness, constraint violations, evidence survival, destructive revisions, tokens and latency. An oracle selecting the best candidate with hidden answers is a diagnostic ceiling for selection, not an available production policy. Synthesis can sometimes exceed that ceiling because it creates a new answer, but improvement must be demonstrated independently.

