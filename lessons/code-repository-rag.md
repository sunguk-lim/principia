# Code-Repository RAG

## Meaning

Code-repository RAG retrieves source-code evidence from a pinned repository revision before generating an answer.

## Mechanism

Enumerate files at a commit, parse supported text, preserve path and revision, split into retrievable code spans, and index them. Retrieval can use exact symbol search, embeddings, or both. The answer cites the retrieved path and span, and authorization is checked before private code reaches the model. A whole-repository text dump may be useful for small examples but can flatten structure or omit code when the context limit is reached.

## One example

A developer asks where a retry timeout is set. Retrieve the configuration symbol and its call sites at the same commit, cite their file paths and line spans, and state when the index has not caught up to the latest commit.

## Check your understanding

**Question:** Why is a repository digest not automatically a reliable code RAG system? **Answer:** It may lose provenance or omit files, and it does not by itself provide retrieval evaluation, freshness, or access control.
