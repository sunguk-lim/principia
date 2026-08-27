# Figure spec — `continuous-batching`

## Visual teaching contract

- **Audience:** An engineer who understands a request queue and KV cache but not iteration-level scheduling.
- **Single job:** Make the reader see that a finished sequence releases a slot between token steps and queued work can occupy it immediately.
- **Visual thesis:** Fixed membership turns early finishes into dead slots; continuous membership evicts the finished request and admits the next queued request while long requests keep running.
- **Traced object:** Request D, amber throughout, moves from waiting into A's released slot.
- **Signature moment:** At the step-2/step-3 boundary, slot 1 changes directly from blue A to amber D while B remains continuous beneath it.

**Comprehension test:** The reader should identify the dead-slot problem, the membership change, the per-request state that makes it safe, and the resulting reduction in idle capacity.

**Rendered constraints:** Static 720×720 comparison; no label below 17 px; request identity uses both color and letters; no animation is required because the aligned step columns already spatialize time.
