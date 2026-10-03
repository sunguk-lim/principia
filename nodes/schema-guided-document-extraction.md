---
id: schema-guided-document-extraction
title: Schema-Guided Document Extraction
summary: Schema-guided document extraction maps evidence in a document to declared fields and types, with explicit missing values and field-level validation rather than treating parseable JSON as correct data.
type: concept
tags: [ml/data]
prereqs: [structured-output, measurement]
sources: [https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/train/custom-model]
status: explained
created: 2026-10-04
updated: 2026-10-04
---

# Schema-Guided Document Extraction

## Summary

**Schema-guided document extraction** identifies requested fields in a document and maps them into a declared data structure. The schema states what the application wants; it does not prove the value was present, read correctly, or assigned to the right field.

## Grounded explanation

A pipeline may render pages, run text recognition, locate candidate spans, normalize values, and populate fields. Some systems combine these steps in one model; others use separate OCR, layout, and extraction stages. A field can be absent, illegible, ambiguous, or spread across pages. In each case the application needs an explicit policy for missing values, confidence, evidence location, and human review. [[structured-output]] can constrain the response shape, but a valid object may still contain an incorrect amount or invent a value.

For example, an invoice extractor might return `invoice_date`, `total`, and `currency`. Check whether the total corresponds to the payable amount rather than a line subtotal, whether dates use the intended locale, and whether the currency was visible. Multi-page input requires linking evidence across pages without duplicating the same field. A `null` output is safer than a guess only when the model reliably abstains for truly missing fields and does not over-abstain on present ones.

Evaluate per-field precision, recall, exact or tolerance-aware value accuracy, missing-field detection, and document-level acceptance with [[measurement]]. Hold out layouts, languages, scan quality, and multi-page cases. Compare a modular OCR-plus-extractor baseline with a unified model under matched data and latency constraints; a vendor's headline score or speed ratio is not portable evidence.

## Prerequisites

- [[structured-output]]
- [[measurement]]

## Sources

- [Azure Document Intelligence custom models](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/train/custom-model): field labeling, extraction, and model evaluation boundaries.
