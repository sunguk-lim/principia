---
id: embedding
title: Embedding
summary: An embedding is a dense vector — an ordered list of real numbers, often a few hundred to a couple thousand of them (for example 768 or 1536 numbers) — that represents the meaning…
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Embedding

## Summary

An **embedding** is a dense vector — an ordered list of real numbers, often a few hundred to a couple thousand of them (for example 768 or 1536 numbers) — that represents the *meaning* of some input, such as a word, a sentence, an image, or a catalogue item. A [[neural-network]] produces it, having been trained so that inputs with similar meaning are placed at nearby points in this vector space and inputs with different meaning are placed far apart. The slogan is: distance in the vector space stands for difference in meaning.

## Grounded explanation

Start with the problem an embedding solves. The crudest way to feed a discrete thing — say the word *cat* — into a computer is to assign it an identity number, or equivalently a **one-hot vector**: a list as long as the entire vocabulary, all zeros except a single 1 in the slot reserved for *cat*. This representation is **sparse** (almost every entry is 0) and, more importantly, it carries no notion of similarity. The one-hot vector for *cat* and the one for *kitten* differ in exactly the same way as *cat* and *quarterly*: each pair shares no nonzero positions, so by any geometric measure every distinct word is equally far from every other. The representation knows the words apart but knows nothing about how they relate.

An embedding fixes this by replacing that long sparse vector with a short **dense** one — a vector in which the numbers are mostly nonzero and each coordinate is a real-valued direction the model can tune freely. Crucially, the *position* of that vector in the space is chosen to carry meaning. We want *cat* and *kitten* to sit close together and *quarterly* to sit far from both. The packing of meaning into geometry is the whole idea: instead of meaning being an opaque label, it becomes a location, and locations can be compared by how near or far they are.

Where do these positions come from? They are learned by a [[neural-network]]. Recall that such a network maps inputs to outputs through layers of weight matrices, and that those weight matrices are the parameters adjusted during training to make the network do well at some task. An embedding is exactly the output of an early stage of such a network: each input is converted into its dense vector by a learned transformation, and that vector is then fed forward to the rest of the network. Because the embedding vectors are themselves built from the network's parameters, training adjusts them too. So the network is free to *move* each input's vector around the space, and it moves them wherever doing so helps it succeed at the training task.

This is the key insight, and it explains why the geometry ends up meaningful rather than arbitrary. Suppose the task is to predict the next word from the words around it. Words that are used in similar contexts — *cat* and *kitten* both appear near *purred*, *litter*, *fur* — must lead the network to similar predictions. The cheapest way for the network to produce similar predictions for two inputs is to hand them similar vectors going in, so training pressure pushes *cat* and *kitten* toward the same region of the space. *Quarterly*, which appears near *revenue* and *earnings*, gets pushed elsewhere. No one labels the space by hand; the similarity structure falls out of the network arranging inputs so the geometry serves the task. The meaning is a side effect of usefulness.

A striking consequence is that not only *positions* but *directions* in the space can become meaningful. In well-trained word embeddings the vector arithmetic *king* minus *man* plus *woman* lands very close to the vector for *queen*. Reading that literally: the step from *man* to *woman* is some particular direction-and-distance in the space (a fixed offset, the "gender" direction), and the same offset applied starting from *king* arrives near *queen*. The model was never told about gender or royalty as categories; it placed the words so that consistent relationships became consistent geometric moves, because that regular arrangement is what let it model language efficiently. This is the sharpest evidence that the space encodes structure, not just clustering.

Now a worked instance with three sentences, to see the geometry do its job. Feed each sentence through a network that produces a sentence embedding:

- A: *the cat sat on the mat*
- B: *a kitten rested on the rug*
- C: *quarterly revenue rose 4%*

Sentences A and B describe nearly the same scene — a small feline at rest on a floor covering — using almost entirely different words: they share only the function word *on*, and no content word in common (*cat* versus *kitten*, *sat* versus *rested*, *mat* versus *rug*). A keyword match would call them nearly unrelated. But the network was trained on enough text to learn that *cat* and *kitten* mean nearly the same thing, that *sat* and *rested* describe the same posture, and that *mat* and *rug* are both floor coverings; so it places A and B at close-together points in the space. Sentence C is about money and is built from words the network learned belong to a different region entirely; its vector lands far from both A and B. A downstream system comparing these three vectors by their geometric closeness will report A and B as a related pair and C as the outlier — and it reaches that conclusion with zero shared content words, purely from proximity in the space.

That last point is why embeddings matter in practice. Once every word, sentence, or item is turned into a comparable vector, you can find what is relevant to a query by looking for the vectors nearest to the query's vector, rather than by matching exact keywords. The numerical measure usually used for "nearness" is cosine similarity — essentially, how closely two vectors point in the same direction — and large collections of embedding vectors are kept in specialized stores, often called vector databases, built to answer "which stored vectors are closest to this one?" quickly. This nearest-neighbor search over embeddings is the foundation of meaning-based search and of retrieval systems that fetch relevant passages by topic instead of by literal word overlap. In every case the move is the same one this node describes: convert meaning into a position in a continuous space, then let distance do the comparing.

## Prerequisites

- [[neural-network]]

## Sources

_none_
