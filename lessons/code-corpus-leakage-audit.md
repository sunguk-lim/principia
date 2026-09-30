# Code-Corpus Leakage Audit

A code model can score well on a test set because it saw close relatives of the test code during training. The question is not simply whether any two files have identical bytes. Forks, vendored packages, templates, and edited copies can cross a random file split even when hashes differ. That makes the test partly a recognition task when the product claim is about unfamiliar code.

Start with provenance. Record each file's repository family, ingestion snapshot, time, and transformations. Compute exact hashes and approximate similarities over token shingles. MinHash can cheaply suggest similar pairs; manually check a sample and measure how often the search misses meaningful copies. Put verified copy/fork families in the same split group. Then reserve a later, group-disjoint holdout. A chronological cut is useful only if it reflects what the training pipeline actually knew at the cutoff; later copies of old code still need overlap checks.

Imagine a model rises from 40% to 55% exact-match completion accuracy on a random file holdout. Break the result down by nearest training-example similarity. If the new model wins mostly on files with a near-twin in training and stays near 40% on genuinely low-overlap files, the original 55% score overstates evidence for novel-code capability. It does not prove that every improved completion was memorized: high-overlap examples may also be easier, so compare difficulty and use matched examples.

A good report includes group definitions, duplicate-search recall, overlap buckets and their sizes, low-overlap performance, uncertainty, and a newly authored slice where feasible. Statistical deduplication does not settle code licensing or privacy questions.

**Understanding check:** Why does splitting by repository still fail if two unrelated repositories vendor the same library? What additional grouping or audit would detect it?
