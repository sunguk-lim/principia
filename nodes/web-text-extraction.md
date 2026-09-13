---
id: web-text-extraction
title: Web Text Extraction
summary: Web text extraction converts an archived HTTP representation into training text, choosing which visible content and repeated page chrome survive and thereby changing every content-based filter that follows.
type: concept
tags: [ml/data]
prereqs: [precision-recall, dataset-lineage]
sources:
  - "https://commoncrawl.org/blog/web-archiving-file-formats-explained"
  - "https://arxiv.org/abs/2406.11794"
status: explained
created: 2026-09-14
updated: 2026-09-14
---

# Web Text Extraction

## Summary

A web archive can preserve the HTTP response and HTML, while a language-model corpus needs a text representation. **Web text extraction** performs that conversion: it selects text-bearing regions, removes markup and repeated page chrome, preserves or discards structure, and emits a document for later filtering and training. This is a data-selection step, not a neutral change of file format. Two extractors can start from the same archived pages yet produce different document lengths, retained domains, duplicate patterns, and model results.

## Grounded explanation

Common Crawl distinguishes WARC files, which store raw crawl records and response data, from WET files, which store extracted plain text. A locally chosen extractor can instead read the archived HTML from WARC and decide which navigation, cookie notices, tables, code, headings, or main-body passages to retain. Those decisions alter the examples seen by every content-based stage downstream.

Measure extraction against labeled page regions with [[precision-recall]]. Here, precision is the fraction of emitted text regions judged useful for the intended corpus, while recall is the fraction of useful source regions that survive. Removing more aggressively may raise precision by dropping repeated menus and notices, but it may lower recall when it also drops code, tables, headings, or short answers. Neither “more text” nor “cleaner text” is sufficient by itself; the preferred operating point depends on the intended domains and training objective.

Extraction also changes the input to later rules. A document-length threshold sees a new length. A language or quality classifier sees a new vocabulary and boilerplate ratio. Exact and approximate deduplication receive different strings and boundaries. Therefore, holding downstream code constant does not hold the effective pipeline constant: the same thresholds can accept a different population after extraction changes.

### Worked instance: the same page, two corpora

Suppose a manually annotated page contains 100 useful text regions. Extractor A emits 100 regions: 80 useful and 20 navigation or notice regions. Its extraction precision is $80/100=0.80$, and its recall is $80/100=0.80$.

Extractor B is stricter. It emits 75 regions: 70 useful and 5 boilerplate regions. Its precision rises to $70/75\approx0.93$, while recall falls to $70/100=0.70$. B is not simply “better”: it removes fifteen unwanted regions but also loses ten useful ones that A retained.

Now suppose a downstream rule rejects documents shorter than 80 emitted regions. A's output passes with 100 regions; B's fails with 75. The URL, archived response, and threshold are unchanged, yet the accepted corpus differs because extraction changed the measurement consumed by the rule. Reusing the threshold without reevaluation confounds the extractor's direct selection with the downstream rejection it triggers.

### How to compare extractors

Version the extractor, configuration, source snapshot, and output hashes with [[dataset-lineage]] so a result can be replayed. Build a stratified labeled sample across ordinary prose, documentation, forums, code, tables, mathematics, languages, and page templates. Report region- or token-level precision and recall, empty and truncated outputs, document-length distributions, boilerplate repetition, domain retention, and extraction throughput.

Then replay each candidate output through the same downstream filters and deduplication stages. Compare acceptance rates and rejection reasons by domain, recalibrate thresholds only when justified, and train equal-compute proxy models with the same architecture, tokenizer, schedule, and evaluation. Repeat enough runs to distinguish a stable extractor effect from training variation. The DataComp-LM study used this controlled pattern: it compared Common Crawl WET, Trafilatura, and Resiliparse extraction before the same RefinedWeb-style heuristic filters, then trained and evaluated matched models. Its reported ranking is evidence for that experimental setting, not a universal ranking of extractors.

## Sources

- Common Crawl, *Web Archiving File Formats Explained*: WARC stores archived web resources and metadata; WET stores extracted body text without HTML or other media.
- Li et al., *DataComp-LM: In search of the next generation of training sets for language models* (arXiv:2406.11794), §4.2 and Appendix K: controlled comparison of WET, Trafilatura, and Resiliparse extraction with matched downstream filtering and model evaluation.
- The worked page-region example and validation procedure are independent constructions.
