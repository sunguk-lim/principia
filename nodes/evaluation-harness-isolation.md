---
id: evaluation-harness-isolation
title: "Evaluation Harness Isolation"
summary: "Evaluation harness isolation keeps editable candidate code from modifying or reading protected grading logic, hidden answers and score aggregation through externally enforced boundaries."
type: concept
tags: [software/testing]
prereqs: [sandboxed-code-execution, execution-benchmark-validity]
sources: [https://inspect.aisi.org.uk/sandboxing.html, https://www.swebench.com/SWE-bench/guides/evaluation/]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# Evaluation Harness Isolation

## Meaning

A candidate allowed to edit its implementation must not automatically gain authority over the instrument used to judge it. Harness isolation protects grading logic, hidden labels, splits and result aggregation from candidate control. Accidentally changing a loss denominator can invalidate a comparison even without malicious intent.

## Mechanism

Use [[sandboxed-code-execution]] to give candidate code explicit inputs and writable work areas, while a trusted supervisor owns protected evaluation state. Read-only mounting protects integrity, not confidentiality: hidden answers must not be readable from the candidate environment at all. Separate scoring processes, credentials, network routes and artifact permissions according to the required boundary. Inspect documents that sandbox provisioning alone does not place every tool or scorer inside the sandbox; only delegated sandbox operations execute there.

[[execution-benchmark-validity]] additionally requires a correct, versioned scoring contract. Hashes and commit diffs detect some changes but do not prevent them. The trusted side should select the evaluated artifact, validate result formats and compute the score itself, rather than trusting a number printed by candidate code. Restrict detailed feedback if repeated observations would reveal protected labels.

## One example

A fictional training agent writes weights and reports validation loss. If its script can replace the scorer's denominator from 100 examples to 1,000, a displayed loss falls tenfold without improving predictions. Moving aggregation outside the editable environment prevents that path. If hidden labels are merely mounted read-only beside training inputs, the agent can still copy them into its predictions; integrity protection alone was insufficient. Keep labels on the trusted scoring side and send only allowed inputs to the candidate.

## Check your understanding

Does a clean diff prove isolation? No. It may miss runtime filesystem, process or network access. Test attempts to overwrite scoring files, read labels, forge results and leak information through logs. Record the evaluated artifact and harness versions. Isolation preserves an instrument's authority; it does not prove its tests measure the intended outcome or that every score improvement is genuine.

## Prerequisites

- [[sandboxed-code-execution]]
- [[execution-benchmark-validity]]

## Sources

- <https://inspect.aisi.org.uk/sandboxing.html>
- <https://www.swebench.com/SWE-bench/guides/evaluation/>
