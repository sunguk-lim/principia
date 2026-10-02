# Multimodal Model-Input Contract

## Meaning

“Supports vision” or “supports audio” is too coarse for an application. The **multimodal input contract** specifies accepted content parts, encodings, size limits, timing, and output semantics for each model and endpoint.

## Mechanism

For vision, a request may carry an image as encoded bytes, a URL, or a provider file reference. Each choice has different retention, access, size, and failure behavior. Image resolution and preprocessing affect whether small text or spatial details survive. For audio, distinguish a completed-file transcription, streaming transcript, and live bidirectional conversation; they have different latency and turn-taking contracts. The model may internally form an [[embedding]], but the API contract concerns observable input and output, not an assumed shared representation.

Document content-part order, supported MIME types, file-size ceilings, truncation, timestamps, and whether the provider fetches remote URLs. A URL may be inaccessible, change after submission, or expose private data to a different service. Test with controlled fixtures, not personalized links. Use [[structured-output]] only for the response shape; it cannot guarantee that the model perceived the relevant frame or sound correctly.

## Worked example

A vision API accepts a URL image, but the batch endpoint rejects that source type. An audio API accepts a completed WAV file but cannot stream partial transcripts. Both vendors can advertise “multimodal” while failing these concrete workflows. Specify encoding and timing before selecting the model.

**Understanding check:** Which test distinguishes file transcription from a live audio conversation contract?
