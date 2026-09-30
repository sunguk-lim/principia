# Training Data Minimization

Data minimization is a decision made before training, not a refusal style added afterward. Define the model's task, then ask which records and fields are actually necessary. Remove unneeded identifiers, secrets, duplicates, and expired data from the corpus and its copies. Preserve provenance so a later audit can identify what entered a particular model. Redaction can fail to find contextual identifiers and can erase useful task signal, so measure both residual exposure and task quality.

Imagine a support summarizer trained on tickets. It needs the problem category and resolution, but it does not need payment-card numbers. Strip those numbers before making examples. If an older model already saw them, a new input filter does not change its weights; evaluate retraining or another measured remediation.

**Understanding check:** Why does a perfect refusal score on a small test set not prove that sensitive training strings were removed?
