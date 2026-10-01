---
id: document-input-api
title: Document Input API
summary: A document-input API accepts a file such as a PDF as model input, with endpoint-specific upload, parsing, page, size, and retention behavior that must be validated separately from answer quality.
type: concept
tags: [ml/agents]
prereqs: [structured-output, retrieval-augmented-generation]
sources: [https://developers.openai.com/api/docs/guides/file-inputs]
status: explained
created: 2026-10-02
updated: 2026-10-02
---

# Document Input API

## Summary

A **document-input API** lets an application submit a file to a model endpoint. This differs from first extracting text or indexing the file for [[retrieval-augmented-generation]]: the provider may parse, render, or select file content under endpoint-specific rules. An accepted upload is not proof that the model saw every page or interpreted tables and figures correctly.

## Grounded explanation

Inspect the endpoint's supported MIME types, file-size and page limits, input method, cost accounting, retention policy, and error format before choosing an integration. OpenAI's official file-input guide documents that support differs between its Responses and Chat Completions APIs, and that PDFs can be supplied under a particular file content contract. A generic “supports PDF” checkbox loses these operational distinctions.

For a scanned PDF, text extraction may be absent or OCR may misread a table. For a long PDF, context limits or internal truncation can hide the relevant page. For a private file, decide whether uploading it to that provider is authorized before model invocation. [[structured-output]] can shape the answer but cannot recover missing source content or enforce document permissions.

Validate with a small labeled document set containing ordinary text, scanned pages, tables, figures, multi-column layout, and long files. Record which pages were represented, answer accuracy, citation support, latency, cost, and failure modes. Compare direct file input with an explicit parse-and-retrieve pipeline under the same tasks; neither path is universally superior.

## Prerequisites

- [[structured-output]]
- [[retrieval-augmented-generation]]

## Sources

- [OpenAI file inputs guide](https://developers.openai.com/api/docs/guides/file-inputs): endpoint- and file-type-specific input contracts.
