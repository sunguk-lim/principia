# Synthetic Bug Training for Coding Agents

## Meaning

Synthetic repository bugs provide many runnable repair exercises. A program changes working code, checks that at least one test now fails, and gives the agent an issue to fix. The exercise is useful only if its feedback teaches behavior that transfers to real defects.

## Mechanism

A generator chooses which code to alter and how to describe the failure. Those choices can create shortcuts. If every task changes one suspicious line, an agent may learn to revert odd-looking lines. If issue text is written from the exact diff, it may reveal the fix. The agent's training reward can rise without an improvement on independently collected issues; that is a [[reward-hacking]] risk.

Use real issues as a holdout and separate repositories or time periods to reduce [[temporal-data-leakage]]. Compare real-only, synthetic-only, and mixed training at matched compute. Check both formerly failing tests and regressions, but remember that a finite test suite does not prove the patch is correct.

## One example

A generated bug changes `>=` to `>` and the issue says “the comparison in validator.py excludes the boundary.” The issue gives away the location. A stronger task describes the user-visible boundary failure without naming the changed code, then checks whether the agent can locate and repair it.

## Check your understanding

**Question:** Why is high success on generated tasks insufficient? **Answer:** It may reflect generator-specific cues; held-out real issue resolution tests transfer.
