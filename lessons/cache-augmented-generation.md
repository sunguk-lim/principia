# Cache-Augmented Generation

## Meaning

Cache-augmented generation preloads a bounded document collection into reusable model context, then answers questions without selecting a fresh document subset each time. The model weights need not change. This is an evidence-provisioning architecture, not simply another name for any cache hit.

## Mechanism

Create an authorized corpus snapshot with stable document and citation IDs. Render a fixed prefix, compute compatible attention state, then append an independent question. Preserve the shared prefix and isolate or reset each request's suffix. Prefix caching saves repeated prefix prefill, but subsequent queries still attend to the retained state. A changed document, model or permission can invalidate reuse.

The corpus must both fit the endpoint's capacity contract and remain usable by the model. Long-context tests should vary evidence position, distractors and absent answers. Loading every document avoids selection misses but does not guarantee correct synthesis. Each caller must be allowed to see every included source; output filtering does not repair an unauthorized preloaded context.

## One example

For an illustrative 16,000-token combined allowance, let the stable prefix contain 10,000 tokens, the question/history allowance 1,000 and output reserve 2,000. The 13,000 total leaves 3,000 headroom. Forty questions recomputing the prefix would process 400,000 prefix positions; reusing it after one computation avoids 390,000 of those positions. That is not a fortyfold runtime speedup: suffix computation, generation, cache loading and later attention remain. A source change requires a new valid snapshot, even if an old cache still exists.

## Check your understanding

**Question:** When might ordinary retrieval be preferable? **Answer:** When the corpus is too large, frequently changing, distracts the model, or has per-user permissions that prevent sharing the full prefix. Compare cold/warm latency, memory, update lag and supported answer quality under the same tasks rather than choosing from a benchmark slogan.
