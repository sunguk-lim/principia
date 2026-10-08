---
id: streaming-voice-agent-pipeline
title: Streaming Voice-Agent Pipeline
summary: A streaming voice-agent pipeline coordinates audio transport, provisional and final speech recognition, dialogue state, response generation, and speech synthesis under turn-taking and latency constraints.
type: concept
tags: [ml/speech]
prereqs: [agent-session-state, pipeline-bottleneck-localization, latency-percentile]
sources: [https://docs.livekit.io/agents/multimodality/audio/, https://docs.livekit.io/agents/logic/turns/]
status: explained
created: 2026-09-30
updated: 2026-10-09
---

# Streaming Voice-Agent Pipeline

## Summary

A voice agent must convert live audio into a stable user intent, decide what to do, and return audible speech while the conversation continues. The **streaming voice-agent pipeline** separates transport, speech-to-text (STT), dialogue, and text-to-speech (TTS) so each stage can be observed and changed without confusing its latency or correctness with another stage's.

## Grounded explanation

Audio arrives in frames. STT can emit provisional partial transcripts before a final turn. Partials are useful for responsiveness but may be revised; consequential actions should use a validated final interpretation or an explicit confirmation policy. The dialogue layer maintains reservation fields, corrections, and tool outcomes in [[agent-session-state]] rather than inferring them anew from a polished reply. TTS then streams audio back. Turn detection decides when speech has ended; interruption handling cancels or revises an in-progress response when the caller starts speaking again.

A booking caller might first say “October sixteenth,” then correct to “eighteenth.” A robust application records the correction, verifies the resulting date, and only then asks a booking service to commit. A partial transcript must not trigger a second reservation. Design idempotent action boundaries and expose whether a response was queued, spoken, interrupted, or superseded.

Measure a timeline: first speech to detected end of turn, end of turn to final transcript, final transcript to first generated text, first text to first audio, and first audio to playback. The first interval includes the user's speaking time, so it is not an STT speed benchmark. [[pipeline-bottleneck-localization]] distinguishes recognition, model inference, synthesis, network jitter, and queueing. Report [[latency-percentile]]s as well as median latency, word/field error on noisy and accented samples, task completion, corrected-field accuracy, interruptions, and false action rate.

The STT–dialogue–TTS decomposition is not the only architecture: realtime speech-to-speech models can merge stages, trading interchangeability and inspectability for potentially different latency and interaction quality. Evaluate both under the same scenarios and privacy requirements. Provider-specific language or millisecond claims require separate evidence; they do not follow from the pipeline design.

A custom recognition vocabulary can improve application-specific names, product identifiers, and alphanumeric codes, but it can also bias unrelated words. Keep the lexicon versioned with the application and test it on accented, noisy, and code-heavy speech. Report named-entity and critical-field error separately from overall word error, plus latency and false corrections. Do not promote a vendor's language-count or post-utterance latency claim into a pipeline guarantee.

## Prerequisites

- [[agent-session-state]]
- [[pipeline-bottleneck-localization]]
- [[latency-percentile]]

## Sources

- [LiveKit Agents, speech and audio](https://docs.livekit.io/agents/multimodality/audio/): STT–LLM–TTS and realtime-model options.
- [LiveKit Agents, turn detection and interruptions](https://docs.livekit.io/agents/logic/turns/): turn-boundary and interruption mechanisms.
