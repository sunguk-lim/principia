# Streaming Voice-Agent Pipeline

## Meaning

A [[streaming-voice-agent-pipeline]] moves live audio through recognition, dialogue, and synthesis while people are still taking turns. Its output must be correct, timely, and interruptible. A smooth-sounding reply is not proof that the agent understood the caller or completed a task correctly.

## Mechanism

Incoming audio yields provisional partial transcripts and then a final interpretation. A partial can change; a booking action should use validated final fields or require confirmation. The dialogue layer records names, dates, corrections, and tool outcomes in [[agent-session-state]]. Text-to-speech streams the response, while turn detection and interruption logic decide when to speak, stop, or revise. The stages can be replaced independently, but their delays and errors accumulate.

Timestamp each boundary. The interval from speech start to final transcript includes the time the person spent talking; it is not a pure recognition benchmark. Separate end-of-turn detection, STT finalization, model generation, TTS first audio, and playback. Use [[pipeline-bottleneck-localization]] and tail-latency measurements to find the stage that actually hurts experience. Also test noisy calls, alphanumeric names, corrections, barge-in, and false consequential actions.

## One example

The caller says “October sixteenth—sorry, eighteenth.” A provisional transcript may briefly show the sixteenth. The application updates the pending date to the eighteenth, confirms it if needed, and makes one idempotent booking request. If the agent starts speaking too soon, an interruption should cancel or supersede the stale response.

## Check your understanding

**Question:** Why measure final-transcript-to-first-audio separately? **Answer:** It isolates the delay the caller experiences after finishing a turn from the duration of their own speech and the recognition stage.
