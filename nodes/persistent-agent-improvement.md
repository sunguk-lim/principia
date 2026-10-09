---
id: persistent-agent-improvement
title: Persistent Agent Improvement
summary: Persistent agent improvement turns observed task failures into a retained system or model change and promotes that change only after independent future-task evaluation.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, agent-memory, agent-verification-loop, execution-benchmark-validity]
sources: [https://arxiv.org/abs/2305.16291, https://docs.langchain.com/oss/python/langgraph/persistence, https://www.swebench.com/SWE-bench/guides/evaluation/]
status: explained
created: 2026-10-10
updated: 2026-10-10
---

# Persistent Agent Improvement

## Summary

An agent does not improve across runs merely by reflecting inside one discarded conversation. Something must persist, be selected on a future run, change behavior, and pass an evaluation that was not used to construct the change.

## Grounded explanation

The durable change can live in the system—an instruction, tool interface, retrieval rule, or executable skill—or in model weights after training. An [[agent-execution-harness]] must actually load the retained artifact. [[agent-memory]] can preserve observations and skills, but storage alone does not prove their use. A new model checkpoint likewise has no effect until deployed. The Voyager paper provides one concrete skill-library and environment-feedback example without fine-tuning weights; its reported gains are specific to its environment.

Use traces to turn failures into hypotheses: a tool schema is confusing, a retrieved fact is stale, or the model misuses test feedback. Propose the smallest change, replay representative failures, and then run held-out tasks. An executable environment supplies initial state, actions, observations, and outcome checks; a saved transcript contains only one historical trajectory and cannot test alternative actions by itself. A curriculum can sample harder or more diverse tasks from outcomes, but the promotion set must remain independent of the curriculum, or repeated tuning overfits the evaluator.

The [[agent-verification-loop]] checks each trial, while [[execution-benchmark-validity]] checks the task oracle and environment. Compare against a no-update control and a simple fixed baseline. Measure future-task success, regression slices, invalid actions, latency, cost, and safety violations. Version the proposed change, training/evaluation data, test environment, and promotion decision. If a change helps only the replayed failures or if its artifact is never retrieved, call it a local repair or an unused note—not persistent improvement.

## Sources

- [Wang et al., Voyager](https://arxiv.org/abs/2305.16291): automatic curriculum, executable skill library, and environment feedback as one implementation.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): state persistence mechanism, not itself a learning guarantee.
- [SWE-bench evaluation guide](https://www.swebench.com/SWE-bench/guides/evaluation/): executable task-evaluation example.
