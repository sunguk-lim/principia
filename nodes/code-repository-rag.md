---
id: code-repository-rag
title: Code-Repository RAG
summary: Code-repository RAG indexes versioned source files with path and revision provenance so retrieved code can support grounded answers without losing repository structure or access boundaries.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-augmented-generation, retrieval-authorization-boundary, dataset-lineage]
sources: [https://github.com/coderamp-labs/gitingest, https://docs.github.com/en/rest/git/trees, https://arxiv.org/abs/2005.11401]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Code-Repository RAG

## Summary

**Code-repository RAG** applies [[retrieval-augmented-generation]] to a versioned codebase. It needs more than a flat text dump: an answer should identify which repository revision, path, and code span support it, and whether the caller may see that file.

## Grounded explanation

Start by pinning a repository and commit. Enumerate the tree, select supported text files, and record each file's path, revision, language, and ownership or access scope. A tool such as GitIngest can create a prompt-friendly digest, but a digest is not necessarily a reliable retrieval index: it may omit files, flatten symbols, lose line boundaries, or exceed the context budget. Keep parse failures and excluded files visible. [[dataset-lineage]] preserves the relationship between derived chunks and their source revision.

Chunk by code structure where useful—functions, classes, or bounded line spans—then index text and optional embeddings. At question time, retrieve candidate spans, keep their paths and commit IDs, and ask the generator to cite those spans. A lexical baseline can outperform embeddings on exact symbol names, so compare lexical, semantic, and hybrid retrieval. Enforce [[retrieval-authorization-boundary]] before a private span enters model context; a successful OAuth connection or repository clone does not grant every user access to every branch or file.

Evaluate path and span recall on questions with known answer-bearing code, citation faithfulness, answer correctness, stale-revision behavior, deleted-file behavior, cross-user leakage, latency, and cost. Re-index after changes or label the snapshot as stale. The choice of parser, local model, vector store, or UI is an implementation detail; none alone proves that the code answer is grounded.

## Prerequisites

- [[retrieval-augmented-generation]]
- [[retrieval-authorization-boundary]]
- [[dataset-lineage]]

## Sources

- [GitIngest project](https://github.com/coderamp-labs/gitingest): repository-to-text digest implementation and scope.
- [GitHub Git Trees API](https://docs.github.com/en/rest/git/trees): versioned file hierarchy and path identity.
- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401): retrieval and generation separation.
