# Code-Generation Quality Reward

## Meaning

A generated program can pass tests and still be slow, insecure, wasteful, or hard to maintain. A **code-generation quality reward** makes these outcomes separate measurements rather than assuming that test pass rate is a complete proxy for useful code.

## Mechanism

A task's executable tests supply evidence about behavior on tested inputs, subject to [[execution-benchmark-validity]]. They do not certify runtime, memory, security, maintainability, or correctness on untested inputs. Record these dimensions separately before combining them. For example, a policy may receive a resource-use bonus only after it passes a pinned functional test suite. This correctness gate prevents a large style score from directly compensating for failing tests, but it cannot repair weak tests or capture every valid implementation.

Measure properties where possible: benchmark latency under fixed hardware and inputs, cap memory, and run targeted static and dynamic security checks. Use blinded expert ratings for subjective readability, with a rubric and agreement analysis. A learned judge may approximate those ratings, but optimization can exploit its blind spots; [[reward-hacking]] predicts that the judge's score may rise while human quality falls. Comments are neither automatically good nor bad: penalizing comment volume may suppress useful explanations, while rewarding it can produce filler.

## Worked example

A code generator passes a hidden test suite but allocates ten times the expected memory. The functional gate says its output is eligible for quality scoring; a measured memory cap can reject or penalize it without asking a readability judge to guess resource use. Compare this policy to the functional-only baseline on held-out repositories.

**Understanding check:** Why can a correctness-gated reward still optimize a program that fails an important user requirement?
