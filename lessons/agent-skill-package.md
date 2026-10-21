# Agent Skill Package

## Meaning

A skill package is a reusable, task-scoped procedure that an agent harness discovers and loads when relevant. It may include instructions, scripts, references and assets. It does not modify model weights or grant permissions beyond the host runtime.

## Mechanism

The package's name and description support discovery without loading every full procedure into context. Once selected, the agent loads the instructions and the resources needed for that task. Scripts can make repeated steps reproducible; references keep detailed material out of the initial prompt. The package must name its platform and tool assumptions. A recipe for a missing command is not executable merely because its prose is clear.

Treat updates as code review. Track owner, evidence, supported environment, version and replacement history. Distinguish proposals from validated active packages, and supersede contradictory instructions rather than keeping both active. Host authority remains external: a skill cannot authorize access that the user or runtime did not grant.

## One example

A formatting skill runs on 100 tasks and saves one minute each, for 100 minutes. A recovery skill runs only twice but saves two hours each time, for 240 minutes. Frequency alone ranks them incorrectly by this illustrative benefit measure. Real decisions must also include mistakes, task consequence and maintenance burden. Automatic activation can inflate invocation counts even when a skill adds no value.

Test both matching and nonmatching tasks, confirm paths and available tools, then compare held-out task success, false activation, latency and regressions with the base workflow. Retire or merge with a versioned rollback path, not simply because a procedure is rarely needed.

## Check your understanding

Does a valid package format prove utility or permission? No: discovery, executable compatibility, measured benefit and authority are different contracts.
