---
id: lost-in-the-middle
title: Lost in the Middle
summary: Lost in the middle is position-sensitive long-context behavior in which a language model uses relevant evidence less reliably when it occurs in the middle rather than near either end of its input.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-augmented-generation, context-window]
sources:
  - https://arxiv.org/abs/2307.03172
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Lost in the Middle

## Summary

**Lost in the middle** describes a long-context failure mode where a language model's accuracy can fall when answer-bearing evidence is placed in the middle of its input rather than at the beginning or end.

## Grounded explanation

[[Retrieval-augmented-generation]] must fit selected evidence into a finite [[context-window]]. It is tempting to treat that window as a neutral budget: retrieve more passages, concatenate them, and expect relevant evidence to remain equally usable wherever it lands. Position-sensitive evaluation contradicts that assumption. Liu et al. found that, in multi-document question answering and key-value retrieval, tested models often performed best when the relevant information was at the beginning or end of a long input and worse when it was in the middle.

The result is an empirical behavior, not a law that every model, task, and prompt must obey. It does show why context length alone is not a reliable retrieval metric. A system can keep the answer-bearing record inside the window yet still answer poorly if competing passages, document order, or prompt structure make that record hard for the model to use. Conversely, moving a passage can change measured accuracy without changing the corpus or retriever.

Suppose a retriever returns eight passages and passage five contains the needed date. Evaluate the same eight passages in several orders: date evidence first, last, middle, and randomized. If accuracy drops only in the middle condition, the failure is context use rather than retrieval recall—every condition retrieved the same evidence. That distinction prevents an incorrect fix such as enlarging the index or retraining the embedder when the immediate issue is context assembly.

Treat ordering and evidence budget as evaluated design choices. Measure answer accuracy, citation support, retrieval recall, and latency across document counts, evidence positions, distractor counts, and representative query types. Use a calibrated ranker, remove duplicates and contradictions, and retain enough provenance to inspect failures. Reordering or extracting evidence may help, but each transformation can omit qualifiers or distort document structure; compare it with a simple ordered baseline before adopting it.

## Prerequisites

- [[retrieval-augmented-generation]]
- [[context-window]]

## Sources

- [Liu et al., “Lost in the Middle: How Language Models Use Long Contexts”](https://arxiv.org/abs/2307.03172): evaluates multi-document QA and key-value retrieval and reports position-sensitive performance in long contexts.
