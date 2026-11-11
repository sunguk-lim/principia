# Recursive Synthetic-Data Feedback

## Meaning

Recursive synthetic-data feedback occurs when outputs of one trained model become training data for later models, whose outputs are reused again. The defining issue is the repeated data-distribution loop, not the mere presence of synthetic examples in one dataset.

## Mechanism

Start with an original [[probability-distribution]], train a generator, sample a finite synthetic set, and train its successor using that set. [[synthetic-training-data]] introduces generator error, selection and provenance concerns at each round. If a rare event is absent from a replacement dataset, the next model receives no direct evidence for that event. Its next synthetic dataset can underrepresent it still further. Approximation error, aggressive filtering and narrowing decoding can compound this loss.

The model-collapse paper studies loss of distributional tails under recursive generated-data training. Its findings do not prove that every use of synthetic data must fail: replacement versus accumulation, original-data retention, sampling and model assumptions matter. More synthetic tokens can help a task without recovering a missing mode that the generator no longer emits.

## One example

Suppose an original process emits a rare valid case with probability .1 and ordinary cases with probability .9. Even a perfect generator sampled only ten times misses the rare case with probability .9^10≈.349. If an idealized successor exactly fits that ten-item replacement histogram without smoothing or external data, a dataset with no rare cases gives it rare-case probability zero. Further samples cannot restore that case in this toy model. This calculation isolates finite-sample loss; it is not a claim that a real neural model exactly matches an empirical histogram or that collapse is inevitable.

## Boundaries and check

Keep generation version, prompt, sampling settings, filters and retained original-data fraction traceable. Compare replacement with mixed or accumulated data over several rounds at matched training budget. Evaluate rare-case coverage, diversity and real-data task slices, not only average performance on regenerated tests. Use an independently held-out original distribution: a test regenerated from the narrowed model can hide what was lost. Does filtering to only easy verified successes guarantee broad retention? No: high label precision can coexist with severe coverage bias.
