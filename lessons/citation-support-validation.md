# Citation Support Validation

## Meaning

Citation support validation checks a generated answer against its cited evidence. A citation marker proves only that a string refers to something. It does not prove that the referenced passage exists, is accessible to the user, or supports the attached claim.

## Mechanism

A [[retrieval-augmented-generation]] pipeline selects evidence before generation. After generation, split the answer into material claims, resolve citation identifiers to the exact source version and span, and assess whether each claim follows from its cited evidence. Keep citation correctness—whether a cited source supports the attached claim—separate from citation completeness—whether claims needing support actually have it.

Several sources may jointly support one statement. A source can also support only one clause of a compound statement. Evaluate scope, qualifiers, units and dates rather than matching shared keywords. A passage saying a policy applies to one region cannot support a global claim. Citation validation is also separate from source truth or currency: a perfectly attributed obsolete policy can still be the wrong answer for today.

ALCE introduces reproducible evaluation of answers with citations, separating fluency, answer correctness and citation quality. Automated support judges are measurements with errors, not infallible logical oracles. Use [[measurement]] with human-adjudicated slices, including partial support, contradiction, fabricated identifiers and multiple-source composition. Authorization must already restrict which evidence may enter and leave the system.

## Worked example

Passage A says application logs are retained for 30 days. Passage B says backups are retained for 35 days. An answer states, “Logs and backups are retained for 30 days [A].” The reference exists, but it supports only the logs clause and contradicts the backup duration when B is considered.

A supported revision separates the claims: logs for 30 days [A], backups for 35 days [B], with the relevant policy date preserved. An uncited claim about model training still lacks support even if both duration citations are correct. Check claim coverage before requesting approval, then bind the reviewed answer and evidence versions if publication can happen later.

## Check your understanding

**Question:** Is 100% valid citation-ID resolution enough? **Answer:** No. Resolve identifiers, assess actual support, check claim coverage and preserve source scope separately.
