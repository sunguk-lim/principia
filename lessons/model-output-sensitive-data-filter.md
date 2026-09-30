# Model Output Sensitive Data Filter

An output filter checks text, structured fields, or tool arguments before they leave the application. Exact patterns can catch known formats, and learned detectors can catch some semantic variations. Both make errors. Streaming makes timing important: a secret can leak in the first chunk before a full-response check runs.

Treat the filter as a backstop. Remove unneeded data before training, authorize retrieval before prompt assembly, and inspect the release path independently. Test synthetic canaries, paraphrases, benign lookalikes, multilingual cases, partial streams, and false blocks. Restrict any logs that contain blocked content.

**Understanding check:** What failure remains even if a filter catches every exact card number in a test set?
