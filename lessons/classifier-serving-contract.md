# Classifier Serving Contract

## Meaning

A saved checkpoint is only one input to a deployed classifier. The observable decision also depends on the feature encoder, class order, and score-to-label rule.

## Mechanism

Version preprocessing, vocabulary and hash parameters, class mapping, threshold, and runtime configuration together. Replay a fixed request through both deployments and locate the first differing intermediate value before blaming model drift.

## Example

The same score vector can become a different label when the class map is swapped. A renamed vocabulary index can change the numeric feature vector while leaving the weights file byte-identical.

## Boundaries and trade-offs

The contract is wider than the serialized model, but narrower than every possible service dependency. Ask which values can change the predicted score or its interpretation. A retraining job changes learned parameters; a revised tokenizer, class map, or threshold can alter results without that job. Keeping these parts versioned together makes rollback reproducible.

## Validation

A useful canary set contains ordinary inputs, capitalization variants, unknown tokens, missing fields, and exact threshold ties. Log intermediate values for those fixtures in a non-sensitive test environment. If old and new scores agree but labels differ, inspect decoding. If feature vectors differ, inspect preprocessing first. Only after serving behavior is stable should a live-traffic change be analyzed as input drift or concept drift.

## Understanding check

If predictions changed but checkpoint bytes did not, which intermediate artifacts would you compare first, and what evidence would make retraining reasonable?
