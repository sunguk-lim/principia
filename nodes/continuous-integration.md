---
id: continuous-integration
title: Continuous Integration
summary: Continuous integration automatically builds and checks each proposed code change in a reproducible environment so defects are found before changes are combined.
type: concept
tags: [software/testing]
prereqs: [measurement, container]
sources: [https://docs.github.com/en/actions/about-github-actions/about-continuous-integration-with-github-actions, https://docs.github.com/en/actions/tutorials/build-and-test-code/python]
status: explained
created: 2026-10-08
updated: 2026-10-08
---

# Continuous Integration

## Summary

**Continuous integration (CI)** checks proposed code changes with an automated build/test pipeline before they are combined. The useful contract is not “a green badge” but a reproducible statement about a specific commit, environment, and set of checks. A passing pipeline proves only what its checks actually exercised.

## Grounded explanation

A CI run starts from a commit and declared workflow. It prepares dependencies, builds artifacts, runs tests and static checks, records logs, and reports a result tied to that commit. GitHub Actions' official guides show this structure for Python projects. A [[container]] can make the runtime and service dependencies more repeatable, but it is not inherently required and does not freeze external APIs, floating image tags, secrets, or nondeterministic tests.

For a multi-container web application, a meaningful integration check starts the service and its dependencies with isolated test data, waits for health readiness, exercises a request through the actual network path, then tears the environment down. Unit tests alone cannot reveal incorrect service wiring; an integration test alone can be slow and poor at locating a defect. Keep both, with narrow failure messages. Pin dependency and image versions when reproducibility matters; isolate credentials and use least privilege for pull-request code.

Treat build failure, test assertion failure, timeout, unavailable dependency, and infrastructure failure as different outcomes. Retry only after diagnosing which category failed; retrying flaky tests into green can hide defects. Compare CI signal with escaped defects and time-to-diagnosis, not just pass rate. Measure duration and false-failure frequency with [[measurement]], and remove checks that no longer provide evidence. A protected branch may require successful checks, but branch policy cannot make weak tests strong.

## Sources

- [GitHub, Continuous integration](https://docs.github.com/en/actions/about-github-actions/about-continuous-integration-with-github-actions): definition and workflow model.
- [GitHub, Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python): concrete build/test workflow example.
