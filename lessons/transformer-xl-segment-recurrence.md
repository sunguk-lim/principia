# Transformer Xl Segment Recurrence

## Meaning

Transformer-XL passes hidden-state memory between fixed-length text segments. It processes long streams without attending directly to every old token at once.

## Mechanism

Cache earlier layer states, detach them from the current gradient path, and let current attention read the retained states. Relative position handling avoids resetting the meaning of position at each segment.

## Example

For a document split into pages, page two can attend to retained states from page one. Later pages depend on information that survives through the recurrent state, not on an exact copy of the whole document.

## Boundaries and trade-offs

Segment recurrence changes the information path. Instead of reprocessing the entire prior document, the next segment reads cached representations computed earlier. Detaching the cache prevents gradient history from growing without bound, but it also limits direct optimization across very distant segments. Relative position handling lets a token distinguish distance across boundaries. Neither recurrence nor position treatment guarantees that all earlier details remain encoded.

## Validation

Place a named fact in segment one, then ask about it after two, ten, and many more segments with distractors. Compare with a fixed-window baseline under matched model size and compute. Measure both exact-answer success and throughput/memory. A system that accepts an arbitrarily long stream may still forget the old fact; separate operational input-length support from effective usable context. Inspect errors at segment boundaries, where a cache update or position bug is most visible.

## Understanding check

Why does sequentially accepting unlimited segments not imply perfect recall of a detail from the first segment?
