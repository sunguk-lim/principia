---
id: context-window
title: Context Window
summary: The context window is the largest number of tokens — the small chunks of text (words or word-pieces) a language model reads as its atomic units — that the model can take as input…
type: concept
tags: [ml/llm/inference]
prereqs: [transformer-attention]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Context Window

## Summary

The **context window** is the largest number of **tokens** — the small chunks of text (words or word-pieces) a language model reads as its atomic units — that the model can take as input and process together in a single turn. It is a hard ceiling: everything the model is allowed to "see" right now must fit inside it, and anything past the limit simply does not exist for the model unless it is supplied again. Typical sizes are quoted in thousands of tokens (8K, 128K, even 1M). The window exists, and costs what it costs, because of how [[transformer-attention]] works.

## Grounded explanation

Start from what the model is fed. A language model does not consume raw characters; it consumes a sequence of **tokens**, each token being a short chunk of text. The number of tokens in the current input is the quantity written as $n$ in [[transformer-attention]]. The context window is the maximum value $n$ is allowed to take.

Why is there a maximum at all? Because of the central operation in [[transformer-attention]]. There, every token forms a *query* and a *key*, and the model compares **every token's query against every other token's key**. With $n$ tokens, that comparison produces an $n \times n$ matrix of similarity scores — one entry for each ordered pair of tokens. The model must compute, store, and run softmax over all $n^2$ of those entries before it can mix information across the sequence. So the work and the memory the model needs grow with the **square** of the number of tokens, not in proportion to it. This quadratic growth, inherited directly from [[transformer-attention]], is the reason the input cannot simply be unbounded: at some token count the $n \times n$ score matrix no longer fits in the available memory or finishes in acceptable time. The context window is where the system draws that line.

The square law also explains why a larger window is so expensive. Doubling the window does not double the cost. If $n$ doubles, then $n^2$ — the size of the attention score matrix — becomes $(2n)^2 = 4n^2$, four times as large. So each doubling of context length roughly **quadruples** the attention compute and memory. That is why long context is treated as a scarce, costly resource rather than something handed out freely, and why the jump from an 8K window to a 1M window is an enormous engineering and hardware difference, not a small one.

It helps to think of the context window as the model's **working memory**, or short-term memory, for the current turn. Within a single conversation, the model "remembers" only what is currently sitting inside the window — the system instructions, the earlier messages, any documents pasted in, and the latest question, all measured together in tokens. There is no separate store the model quietly keeps on the side. When a conversation grows long enough that older content no longer fits, that content **scrolls out** of the window and is, from the model's point of view, forgotten: on the next turn it is as if those words were never said. The only way the model can use them again is for some outside mechanism to put them back into the window as fresh input. Techniques that fetch relevant past text and re-insert it (retrieval-augmented generation), and the broader idea of an external agent memory that persists facts across turns and re-supplies them when needed, all exist precisely to fill this gap — they are ways of feeding the right tokens back into a finite window. (Those techniques are their own subjects; here they are only the answer to "what happens to what scrolled out.")

A concrete instance makes the limit vivid. Suppose a model has an **8K-token** context window — it can attend over at most about 8,000 tokens at once — and you hand it a document that is **20,000 tokens** long. The document does not fit. The model physically cannot place all 20,000 tokens into the $n \times n$ attention comparison at the same time, because that would require $n = 20{,}000$, well above the 8,000 ceiling. So you have no choice but to **truncate** the document (drop part of it) or **chunk** it (split it into pieces of at most 8K tokens and process each piece separately, then somehow combine the results) — the model never sees the whole thing in one view, and any reasoning that depends on connecting the start to the end may break. Now suppose you upgrade that model to a **16K** window — double the length. Following the square law above, the attention score matrix grows from $8\text{K} \times 8\text{K}$ to $16\text{K} \times 16\text{K}$, which is $2^2 = 4$ times as many entries. You bought twice the room for tokens, but you paid roughly four times the attention cost to get it. That trade — capacity rising linearly while the dominant cost rises quadratically — is the defining tension of the context window.

## Prerequisites

- [[transformer-attention]]

## Sources

_none_
