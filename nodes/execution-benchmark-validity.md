---
id: execution-benchmark-validity
title: Execution Benchmark Validity
summary: An execution benchmark is valid only when its environment, test oracle, patch application, and scoring protocol measure the intended program behavior reproducibly.
type: concept
tags: [software/testing]
prereqs: [measurement, hypothesis-testing]
sources: [https://www.swebench.com/SWE-bench/guides/evaluation/]
status: explained
created: 2026-10-02
updated: 2026-10-02
---

# Execution Benchmark Validity

## Summary

An **execution benchmark** runs candidate code against tests. Its score is evidence about the candidate only if the harness consistently runs the intended program under the intended conditions. A change in score can reflect a change in the model, the tasks, the environment, the test oracle, or the scoring path.

## Grounded explanation

A test-runner is a measuring instrument. Fix the container image and dependency versions using pinned artifact digests, the task set, timeout, resource limits, patch format, test command, and scoring version. SWE-bench's official evaluation guide illustrates the chain: apply a predicted patch to a repository, run tests in a container, and interpret the resulting task outcome. If patch application fails, no assertion about the patch's behavior has been tested.

Start a regression investigation with paired runs of old and new candidates on the same task and pinned harness. Run reference solutions as a sanity check, but recognize their limit: a gold patch passing does not show that the tests accept *every* valid alternative or reject every invalid one. Review ambiguous task specifications and sample apparently surprising failures; use mutation or adversarial cases to probe weak tests. Classify infrastructure failures, patch failures, timeouts, and assertion outcomes separately. An assertion failure is evidence about the candidate only after checking that the assertion matches the task contract.

Suppose a new candidate solves a task but takes longer to install dependencies. If a shared 60-second timeout includes installation for one run but not the other, a lower pass rate is not a clean quality comparison. Pin the environment, separate setup from test time, and rerun paired tasks with a documented policy.

Use [[measurement]] to report per-category counts, paired differences, repeated-run variance where nondeterminism exists, and uncertainty intervals rather than one total score. [[hypothesis-testing]] distinguishes a plausible small fluctuation from stronger evidence of a change; neither statistical significance nor a passing gold patch repairs an invalid test oracle.

## Prerequisites

- [[measurement]]
- [[hypothesis-testing]]

## Sources

- [SWE-bench evaluation guide](https://www.swebench.com/SWE-bench/guides/evaluation/): documented patch application, containerized execution, and result inspection.
