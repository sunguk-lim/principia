---
id: staged-candidate-validation
title: "Staged Candidate Validation"
summary: "Staged candidate validation applies cheap feasibility gates before expensive quality evaluation without treating an early pass as proof of final task success."
type: concept
tags: [software/testing]
prereqs: [execution-benchmark-validity, agent-validation-hooks, multi-fidelity-model-selection]
sources: [https://arxiv.org/abs/2507.19457, https://code.claude.com/docs/en/hooks-guide, https://www.swebench.com/SWE-bench/guides/evaluation/]
status: explained
created: 2026-11-10
updated: 2026-11-10
---

# Staged Candidate Validation

## Meaning

Most expensive evaluation is wasted if a proposed program cannot load or call its tools. Staged validation first rejects clearly infeasible candidates, then spends more resources on candidates that might satisfy the real task. A feasibility gate asks “can this candidate participate safely and correctly in the protocol?”; a quality gate asks “does it achieve the intended outcome?”

## Mechanism

Order bounded checks by cost and their ability to reject invalid candidates: parse or load the artifact, verify required interfaces and forbidden effects, run representative smoke cases, then evaluate the full task and regression suite. [[agent-validation-hooks]] can trigger checks, but their event timing and blocking semantics must be explicit. [[execution-benchmark-validity]] keeps infrastructure errors and candidate failures distinct.

Resource-based screening in [[multi-fidelity-model-selection]] is related but different: a short quality run predicts performance at a larger budget, whereas a syntax gate checks a necessary eligibility condition. Neither an early quality ranking nor a smoke test proves final correctness. Stages can be combined, but retain their meanings and denominators. A gate should not silently convert missing evidence or infrastructure unavailability into a low-quality score.

## One example

An invented search proposes ten harnesses. A one-unit load/interface check rejects four. Running that gate on all ten costs ten units. Evaluating the six survivors costs twenty units each, giving total cost 10+120=130 units. Running the expensive evaluation on all ten would cost 200 units under the same simplified accounting. The saving is meaningful only if the cheap gate does not reject viable candidates; inspect false rejections and include both formerly passing and newly failing task families in the final stage.

## Check your understanding

Can a smoke-test winner be deployed immediately? No. Passing one representative tool call does not establish complete-task quality, side-effect preservation or held-out generalization. Test gate coverage with deliberately invalid candidates and known-valid alternatives. Compare final accepted quality, escaped defects, false rejections and total search cost, not merely the proportion surviving each stage.

## Prerequisites

- [[execution-benchmark-validity]]
- [[agent-validation-hooks]]
- [[multi-fidelity-model-selection]]

## Sources

- <https://arxiv.org/abs/2507.19457>
- <https://code.claude.com/docs/en/hooks-guide>
- <https://www.swebench.com/SWE-bench/guides/evaluation/>
