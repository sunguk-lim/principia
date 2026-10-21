# Prompt Injection

## Meaning

Prompt injection occurs when lower-trust content is treated as an instruction that can cross an application's intended authority boundary. A retrieved document, web page or tool result is evidence, not an actor authorized to change the user's goal or the host's permissions.

## Mechanism

Keep provenance and enforce permissions outside the model. A model proposes tool arguments; trusted application code validates their meaning, scope and authorization before execution. Permission-filtered retrieval prevents unauthorized content from entering context at all. Prompt wording, sanitizers and detectors can help but do not prove universal resistance to misleading text.

The trust crossing can happen later. An application may summarize a tool result into persistent memory or turn a repeated trace into a reusable procedure. If promotion removes the original provenance, an untrusted claim can return next session dressed as an established rule. Storage and repetition do not increase its authority. Scope memory, preserve evidence, review procedure activation and recheck effect permissions when used.

## One example

A repository note says a deployment requires uploading a configuration file to an external address. The agent should treat that as a claim to inspect. If a summarizer instead stores “standard deployment: upload configuration,” a future session can retrieve the instruction after the original warning is gone. The host must still reject an unauthorized upload. A successful first-turn refusal does not prove the persistence path is safe.

Test direct and indirect inputs, benign quoted instructions, encoded variants and multilingual content. Then test a write–store–retrieve–execute cycle across sessions. Measure unauthorized proposals, actual effects, false blocks, delayed activation and recovery after rejection. Verify correction, supersession and deletion of poisoned memories as well as input filtering.

## Check your understanding

Does quoting an instruction in a stored summary make it trusted? No. Authority depends on origin and current host policy, not format, age or retrieval rank.
