# Continuous Integration

## Meaning

Continuous integration checks each proposed code change with an automated build and test pipeline, linking the result to a specific commit.

## Mechanism

The workflow prepares an environment, builds artifacts, runs checks, and reports distinct outcomes. An isolated [[container]] can reproduce dependencies and service wiring, but only if versions and external inputs are controlled. Unit tests find local mistakes quickly; integration tests exercise connections between components. A green result means the checks passed, not that all possible behavior is correct.

Classify build failures, failed assertions, timeouts, and infrastructure outages separately. Keep credentials scoped away from untrusted pull-request code. Measure signal by defects caught, false failures, and time to diagnosis rather than pass rate alone.

## One example

For Flask plus Redis, CI starts both services, waits for readiness, sends a request through the web service, checks the expected Redis-backed result, and tears down isolated test data. A Flask unit test alone would miss a broken service hostname.

## Check your understanding

**Question:** Why can a green build still be misleading? **Answer:** The pipeline may not test the relevant integration or may run against a different environment.
