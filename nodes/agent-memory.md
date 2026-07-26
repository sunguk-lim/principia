---
id: agent-memory
title: Agent Memory
summary: Agent memory is the machinery by which an AI agent — a language model that takes actions and holds conversations over many turns — retains information it has seen and recalls it…
type: concept
tags: [ml/agents]
prereqs: [retrieval-augmented-generation, context-window]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Agent Memory

## Summary

**Agent memory** is the machinery by which an AI agent — a language model that takes actions and holds conversations over many turns — **retains** information it has seen and **recalls** it later, across turns, tasks, and whole sessions, beyond what fits in a single [[context-window]]. The problem it solves is that the [[context-window]] is finite working memory: it holds only so many tokens (the small chunks of text a model reads as its atomic units), and once a conversation or task grows past that limit, or a fresh session begins, earlier content scrolls out of the window and is, from the model's point of view, forgotten. Agent memory adds a second tier — an external store the agent **writes** salient facts and events to and later **reads back** when they become relevant — plus the bookkeeping needed to keep the live window from overflowing. In essence it is [[retrieval-augmented-generation]] turned inward, onto the agent's own history, combined with summarization that respects the finite window.

## Grounded explanation

Begin from the constraint that forces the whole design. By [[context-window]], the model can attend over at most a fixed number of tokens at once — call it the window size — and everything the model is allowed to "see" on the current turn must fit inside that ceiling: the system instructions, the earlier messages, any pasted documents, and the latest question, all counted together. There is no separate store the model quietly keeps on the side. When the running conversation grows longer than the window, the oldest content **scrolls out** and the model behaves on the next turn as if those words were never said. The *only* way old content influences a later turn is for some outside mechanism to place the relevant tokens back into the window as fresh input. Agent memory is the name for that outside mechanism, organized as a deliberate system rather than left to chance.

The architecture has two tiers, distinguished by *where the information physically lives*.

The first tier is **short-term memory**: whatever is currently sitting inside the [[context-window]] — the live conversation and any scratch notes the agent has written to itself this turn. It is instant to use, because the model reads it directly with no extra step, but it is bounded (it cannot exceed the window) and volatile (anything that scrolls out is gone). Short-term memory is exactly the model's working memory for the current turn; agent memory does not invent it, it inherits it from [[context-window]].

The second tier is **long-term memory**: an external store — a database living outside the model — that the agent **writes** to and later **recalls** from. Two operations define it. On the *write* side, as the agent works, it selects salient items — a stated user preference, a decision reached, a fact learned, an event that occurred — and saves them to the store, so they survive even after they scroll out of the window. On the *recall* side, when the agent later faces a new situation, it must find the few stored items relevant *now* among possibly thousands, and this is precisely [[retrieval-augmented-generation]] applied to the agent's own past: embed the current situation into a vector (a list of numbers capturing its meaning), search the store for the stored items whose vectors are most similar, and inject those top matches back into the [[context-window]] before the model generates its next response. The crucial reframing is that [[retrieval-augmented-generation]] is normally pointed at an external corpus of documents; here the "corpus" is the agent's *own* accumulated history. That single substitution — retrieve from my own past instead of from a document collection — is what turns plain [[retrieval-augmented-generation]] into long-term memory.

Two kinds of content commonly populate the long-term store, and the distinction is worth naming because it changes what gets written. **Episodic memory** records *specific past events* — "on the last turn the user asked me to book a 9 a.m. flight," "in the previous session the build failed with error X." It is a log of particular happenings, each tied to a time and a context. **Semantic memory** records *distilled, timeless facts and preferences* — "the user prefers metric units," "this project uses Python." Semantic memory is often produced by *condensing* many episodes into a stable generalization, so that the agent need not re-derive the same preference from raw history every time.

That leaves the third piece, **memory management**, which exists because the window is finite and the conversation is not. Two jobs fall under it. The first is **compaction**: rather than carry every old turn verbatim until it scrolls out and is lost, the agent periodically **summarizes** a stretch of older turns into a much shorter gist and keeps the gist in the window in place of the originals — trading fine detail for tokens, so the running context still fits under the ceiling. The second is **eviction with persistence**: deciding, for content about to leave short-term memory, what to first **write** to the long-term store (so it can be recalled later) versus what to simply drop as unimportant. Compaction keeps the live window affordable; eviction-with-persistence makes sure that what is dropped from the window was either saved or genuinely disposable.

Now the *why*, stated plainly. Long-horizon agents — a multi-session assistant, an agent grinding through a task that spans far more text than any window holds — must in practice remember more than the [[context-window]] can hold at once. By [[context-window]]'s square law, you cannot simply make the window arbitrarily large: doubling the token capacity roughly quadruples the attention cost, so unbounded context is not the escape hatch. The resolution is to stop trying to hold everything live and instead **offload** the bulk to a cheap external store and pull back only the small, relevant slice when needed — which is exactly what the two tiers plus [[retrieval-augmented-generation]] provide. Compaction handles the residual: even the slice you keep live must be kept small, so old turns are summarized rather than carried in full. Agent memory is therefore not a single trick but the disciplined combination of *offload-and-retrieve* (to escape the capacity limit) and *summarize-to-fit* (to respect it).

A worked instance ties the tiers together. Early in a long assistant session the user mentions, in passing, "I prefer metric units, and I'm allergic to peanuts." The agent recognizes these as durable preferences and **writes** them to long-term memory as semantic facts. The conversation then continues for tens of thousands of tokens about unrelated topics. Suppose the window holds 8,000 tokens; by the time the running conversation has accumulated, say, 50,000 tokens of dialogue, those early sentences scrolled out of the [[context-window]] long ago — short-term memory has completely forgotten them, and memory management has by now **compacted** that early stretch into a few summary lines so the live context still fits under 8,000. The user now asks, "give me a dinner recipe." The agent embeds this request, runs [[retrieval-augmented-generation]] against its long-term store, and the two stored preference facts surface as the most relevant items; they are injected back into the [[context-window]] alongside the request. The model, now seeing "prefers metric units" and "allergic to peanuts" as live tokens again, produces a peanut-free recipe with metric quantities — instead of obliviously suggesting a peanut sauce measured in cups. Without long-term memory the facts were unrecoverable once they scrolled out; without [[retrieval-augmented-generation]] the agent could not have found *those* two facts among everything it had ever stored; without compaction the running context would have overflowed the window long before the recipe question arrived.

One closing note: this very brain — its store of concept nodes that an assistant writes to and later retrieves from to answer questions across separate sessions — is itself an instance of long-term agent memory.

## Prerequisites

- [[context-window]]
- [[retrieval-augmented-generation]]

## Sources

_none_
