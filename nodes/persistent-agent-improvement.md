---
id: persistent-agent-improvement
title: Persistent Agent Improvement
summary: Persistent agent improvement turns observed task failures into a retained system or model change and promotes that change only after independent future-task evaluation.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, agent-memory, agent-verification-loop, execution-benchmark-validity]
sources: [https://arxiv.org/abs/2305.16291, https://docs.langchain.com/oss/python/langgraph/persistence, https://www.swebench.com/SWE-bench/guides/evaluation/, https://docs.langchain.com/langsmith/evaluation-concepts]
status: explained
created: 2026-10-10
updated: 2026-10-25
---

# Persistent Agent Improvement

## Summary

An agent does not improve across runs merely by reflecting inside one discarded conversation. Something must persist, be selected on a future run, change behavior, and pass an evaluation that was not used to construct the change.

## Grounded explanation

The durable change can live in the system—an instruction, tool interface, retrieval rule, or executable skill—or in model weights after training. An [[agent-execution-harness]] must actually load the retained artifact. [[agent-memory]] can preserve observations and skills, but storage alone does not prove their use. A new model checkpoint likewise has no effect until deployed. The Voyager paper provides one concrete skill-library and environment-feedback example without fine-tuning weights; its reported gains are specific to its environment.

Use traces to turn failures into hypotheses: a tool schema is confusing, a retrieved fact is stale, or the model misuses test feedback. Propose the smallest change, replay representative failures, and then run held-out tasks. An executable environment supplies initial state, actions, observations, and outcome checks; a saved transcript contains only one historical trajectory and cannot test alternative actions by itself. A curriculum can sample harder or more diverse tasks from outcomes, but the promotion set must remain independent of the curriculum, or repeated tuning overfits the evaluator.

The [[agent-verification-loop]] checks each trial, while [[execution-benchmark-validity]] checks the task oracle and environment. Compare against a no-update control and a simple fixed baseline. Measure future-task success, regression slices, invalid actions, latency, cost, and safety violations. Version the proposed change, training/evaluation data, test environment, and promotion decision. If a change helps only the replayed failures or if its artifact is never retrieved, call it a local repair or an unused note—not persistent improvement.

## From traces to a proposed skill

A trace-to-skill pipeline first identifies a recurring task pattern, then extracts its inputs, preconditions, actions, observed outcomes and recovery branches. Remove accidental paths, environment-specific identifiers and credentials; retain provenance and state what the evidence does not cover. Produce a versioned proposal with a task trigger, prerequisites, bounded instructions and an understanding of which checks establish success. One successful trace supplies an example, not evidence that the same commands work in another repository or harness.

For example, three UI tasks use the same development server and screenshot check, but a fourth repository uses a different build command. A proposal that hard-codes the first command can replay the initial traces yet fail the held-out repository. Parameterize or explicitly scope the recipe, test its trigger and prerequisites, then compare successful future use with a no-skill control. Keep rejected candidates and rollback evidence separate from the published skill library. Repeated exposure to one flawed trace can amplify an error; repetition alone is not a quality gate.

## Reviewed interventions and independent acceptance

Product-side actions can reveal where a user corrected, redirected or took over from an agent, but intervention is not automatically a negative correctness label. Correlate it with the original goal and affected operation, distinguish changed intent from repair, and retain the observed final outcome or its uncertainty. Logging permission does not automatically authorize training reuse; apply consent, redaction, access and retention before deriving datasets.

For example, 100 episodes contain 20 manual edits. Review finds eight corrections, seven preference changes and five changes of task. Treating all 20 as mistakes contaminates labels. The eight corrections can become diagnosis and regression cases, but they cannot independently prove a change tuned on them. If a candidate fixes six of eight reused cases yet loses three of ten untouched authorization cases, it is a proposal, not an acceptable release. Keep held-out episodes separate by user or task family when continuations would otherwise leak, preserve source and artifact versions, and record rejected candidates and rollback evidence.

LangSmith's evaluation documentation distinguishes online production runs from offline curated examples and describes a loop where production failures become test cases. That mechanism supports controlled improvement; it does not guarantee every captured session helps. Current-policy sampling can overrepresent accepted actions and omit abandoned work. Record sampling rules, denominators and failure slices, then validate a retained prompt, skill or weight change against independent future tasks before promotion.

## Sources

- [Wang et al., Voyager](https://arxiv.org/abs/2305.16291): automatic curriculum, executable skill library, and environment feedback as one implementation.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): state persistence mechanism, not itself a learning guarantee.
- [SWE-bench evaluation guide](https://www.swebench.com/SWE-bench/guides/evaluation/): executable task-evaluation example.

- <https://docs.langchain.com/langsmith/evaluation-concepts>
