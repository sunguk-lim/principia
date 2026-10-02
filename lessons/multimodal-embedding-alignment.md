# Multimodal Embedding Alignment

## Meaning

A text vector and an image vector are useful for cross-modal search only if their geometry was trained and tested to make relevant pairs comparable. Merely receiving both from APIs does not make their distances meaningful.

## Mechanism

A joint encoder maps inputs from different modalities into an [[embedding]] space and trains paired examples to bring matching items together while separating unrelated ones. CLIP is a well-known image-text example. A text query can then rank images, or an image can retrieve captions. This differs from concatenating independently trained text and image vectors: those coordinates have no shared metric by default.

Alignment is task-dependent. A pooled vector may capture broad semantics but miss tiny labels, diagrams, or spatial detail. [[multimodal-rag]] can instead use page-image multi-vectors and late interaction to preserve finer matching signals. The right representation depends on the retrieval objective and available paired data. A shared embedding space does not imply that a generated answer is faithful to retrieved evidence.

## Worked example

An image of a red bicycle and the caption “a red bicycle” should rank near each other in a joint image-text space. Two independently trained embedding models can each produce 768-number vectors, but equal length does not align their coordinates. Test paired retrieval before comparing those vectors.

**Understanding check:** Why does matching vector dimension not imply that text and image embeddings are comparable?
