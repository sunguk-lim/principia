---
id: interprocedural-taint-analysis
title: "Interprocedural Taint Analysis"
summary: "Interprocedural taint analysis tracks untrusted influence across calls and transformations from defined input sources to sensitive sinks, subject to explicit barrier and library models."
type: concept
tags: [software/testing]
prereqs: [graph, first-class-function]
sources: ["https://codeql.github.com/docs/codeql-language-guides/analyzing-data-flow-in-python/"]
status: explained
created: 2026-11-06
updated: 2026-11-06
---

# Interprocedural Taint Analysis

## Meaning

Interprocedural taint analysis follows untrusted influence beyond one function. A source is where relevant input enters, a sink is a security-sensitive use, and a barrier is a check that genuinely removes the relevant unsafe influence. The analysis asks whether a modeled path connects source to sink; a path is a candidate explanation, not an automatic exploit proof.

## Mechanism

Represent program values and transfers as a [[graph]]. Local edges follow assignments and expressions. Interprocedural edges cross arguments into parameters and returned values back into callers. Because [[first-class-function]] permits callable behavior to be passed as a value, dynamic targets and callbacks require appropriate models instead of assuming every target is known.

Ordinary dataflow may track unchanged values. Taint analysis additionally follows non-value-preserving transformations: adding a fixed prefix to untrusted text changes the exact value but can preserve its dangerous influence. CodeQL distinguishes these operations and exposes source, sink, barrier and additional-flow predicates. A library call missing from the analysis can hide a real path, while a coarse model can invent an infeasible one. Global analysis also costs more time and memory than a local query.

## One example

A fictional request handler reads `target`, passes it to `prepare(target)`, and passes the result to an installer wrapper in another module. The wrapper is the sink. Checking each file separately can miss that remote input selects what is installed. Adding a constant package-name prefix is not a barrier if the target grammar still permits alternate sources or options. A barrier must reject the unsafe forms for this exact sink before the operation runs.

Conversely, a reported graph path might pass through a branch that the deployed configuration can never take. Inspect control conditions and the actual validator before declaring exploitability. Authentication alone does not sanitize an argument; its relevance depends on who the threat model allows to submit it.

## Check your understanding

Does serialization to a new string make data trusted? No. Influence can survive transformation. Validate candidate paths using known vulnerable and blocked fixtures, including wrappers, unsupported libraries and missed branches; state the coverage limits of the model.

## Prerequisites

- [[graph]]
- [[first-class-function]]

## Sources

- <https://codeql.github.com/docs/codeql-language-guides/analyzing-data-flow-in-python/>
