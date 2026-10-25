# Model-Provider Capability Matrix

## Meaning

A provider capability matrix is a tested mapping from application requirements to exact model, endpoint and provider revisions. It records supported, unsupported, conditional and untested behavior instead of assuming that one request shape makes models interchangeable.

## Mechanism

Include modalities and content formats, output schemas, tool-call execution semantics, input/context/output ceilings, privacy and retention, availability, training support and cost. Attach the tested route, revision and date. Check invalid as well as valid requests: refusal, malformed inputs, timeouts and partial tool results matter alongside the happy path.

Context and output limits can have distinct accounting rules. An endpoint may count input plus generated tokens against a combined ceiling, while another model has an additional output cap. Reasoning or formatting tokens can consume generated-token allowances without appearing as visible prose. Verify the actual endpoint rather than copying another model's settings.

The mechanism of fine-tuning continues training model weights; whether a particular account can create that training job is a separate lifecycle capability. Eligibility, base model, method, deployment and retirement conditions need current primary evidence, not a historical vendor list.

## One example

A hypothetical combined allowance is 16,000 tokens. A 12,000-token input plus a 5,000-token output request totals 17,000 and exceeds it by 1,000. Requesting 3,000 instead leaves 1,000 headroom, assuming no additional accounting. Passing the smaller case does not certify the larger one or any real model's limit. Separately, a model can accept image URLs on one route yet fail inline images on another despite both using a chat schema.

## Check your understanding

**Question:** Is changing only a model slug enough to establish a safe migration? **Answer:** No. Re-run conformance and representative task quality, safety, latency and total-cost tests. Unknown cells stay unknown; a documented feature is not proof that the application's exact route meets its acceptance contract.
